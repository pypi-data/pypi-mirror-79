import json
from json import JSONDecodeError
import platform
import re
import sys
from typing import Optional, TextIO, Tuple

import colorama
from ntscli_cloud_lib.automator import DeviceIdentifier, TestPlanRunRequest
from ntscli_cloud_lib.stateful_session import stateful_session_mgr, StatefulSession

# Implementation libs
from ntsjson.functions import make_basic_options_dict, set_log_levels_of_libs
from ntsjson.log import logger
from ntsjson.monitors import BlockMainThreadUntilCompleteMonitor, PrintResultsWhenDoneClass, PrintResultsWhileRunningClass

if platform.system() != "Windows":
    import fcntl
    from os import O_NONBLOCK


def run_impl(
    rae,
    esn,
    ip,
    serial,
    no_wait: bool,
    testplan: TextIO,
    batch: str,
    names: str,
    names_re: str,
    force_keep_eyepatch: bool,
    print_during: bool,
    skip_print_after: bool,
    categories: Optional[str],
    tags: Optional[str],
    configuration: str,
    result_file: Optional[TextIO],
    testnames: Tuple[str, ...],
):
    set_log_levels_of_libs()
    options = make_basic_options_dict(esn, ip, rae, serial, configuration)

    if platform.system() != "Windows":
        # make stdin a non-blocking file so the process does not hang
        # this is apparently not possible like this in Windows, so we're putting a band-aid on it for today
        fd = testplan.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | O_NONBLOCK)

    chosen_plan: Optional[TestPlanRunRequest] = None
    if testplan:
        logger.info("Attempting to test plan from stdin or --testplan file")
        source_str: str = ""
        try:
            source_str = "".join([elt.strip() for elt in testplan.readlines()])
        except IOError:
            logger.error("There was no data to read")
        logger.info("Reading complete!")

        if source_str == "":
            logger.info(f"There was no data in {testplan.name}. Will attempt to get a test plan")
            logger.debug("You can get this dynamically with 'nts get-plan | nts run', or")
            logger.debug("nts run --testplan <file>")
        else:
            try:
                chosen_plan = TestPlanRunRequest().from_dict(value=(json.loads(source_str, encoding="utf-8")))
                # now you can inspect the test plan loaded from file to see if it looks like it's valid
                logger.info(f"Loaded {len(chosen_plan.testplan.testcases)} tests from file.")
            except (JSONDecodeError, KeyError, TypeError) as err:
                logger.critical("The source file did not parse as JSON:")
                logger.critical(err)
                sys.exit(1)

    with stateful_session_mgr(**options) as session:
        session: StatefulSession

        if chosen_plan is not None:
            session.plan_request = chosen_plan
            session.device = session.plan_request.target
            if rae or ip or esn or serial:
                session.device = DeviceIdentifier(rae=rae, ip=ip, esn=esn, serial=serial)
                logger.info("Replacing the target device with:")
                logger.info(session.device.to_json())
        else:
            session.get_test_plan()  # stored in the session at .plan_request

        logger.info(
            "Before editing, test plan included "
            f"{colorama.Fore.BLUE}{len(session.plan_request.testplan.testcases)}{colorama.Style.RESET_ALL} tests."
        )
        if batch is not None:
            session.plan_request.testplan.batch_name = batch

        # add a name filter
        if names:
            logger.info(f"Removing tests with names not in {names} at the user's request.")
            nlist = names.split(",")
            session.plan_request.testplan.testcases = [elt for elt in session.plan_request.testplan.testcases if elt.name in nlist]

        # add another name filter
        if testnames:
            nlist = list(testnames)
            logger.info(f"Removing tests with names not in {' '.join(nlist)} at the user's request.")
            session.plan_request.testplan.testcases = [elt for elt in session.plan_request.testplan.testcases if elt.name in nlist]

        # add a name regex filter
        if names_re:
            logger.info(f"Removing tests with names not matching {names_re} at the user's request.")
            try:
                pattern = re.compile(names_re)
                session.plan_request.testplan.testcases = [
                    elt for elt in session.plan_request.testplan.testcases if pattern.match(elt.name)
                ]
            except re.error:
                logger.critical("Could not compile your regex.")
                sys.exit(1)

        # add a category filter
        if categories:
            logger.info(f"Removing tests with categories not in {categories} at the user's request.")
            clist = categories.split(",")
            if len(clist) > 0:
                session.plan_request.testplan.testcases = [elt for elt in session.plan_request.testplan.testcases if elt.category in clist]

        if tags:
            logger.info(f"Removing tests with tags none of the tags in {tags} at the user's request.")
            user_tag_set = set(tags.split(","))
            if len(user_tag_set) > 0:
                session.plan_request.testplan.testcases = [
                    elt for elt in session.plan_request.testplan.testcases if user_tag_set.issubset(set(elt.tags.split(",")))
                ]

        if not force_keep_eyepatch:
            try:
                if esn is None:
                    # To see if a device has an EyePatch, we need its ESN. We take a brief detour to get as much information as we can about
                    # the devices behind this RAE, so we can find the matching ESN.
                    identifiers = session.get_device_list()
                    if identifiers is None:
                        logger.error(
                            "We were unable to get the list of device identifiers. This could be a connectivity issue, or the modules may "
                            "not be installed on the RAE."
                        )
                        raise ValueError("Skipping filtering of EyePatch tests.")
                    if ip:
                        id_list = [_id for _id in identifiers if ip == _id.ip]
                    elif serial:
                        id_list = [_id for _id in identifiers if serial == _id.serial]
                    else:
                        logger.critical("Automator could not find your device, we can not continue.")
                        sys.exit(1)

                    if len(id_list) == 0:
                        raise ValueError("Could not find a matching device. Not filtering EyePatch tests.")

                    session.device.esn = id_list[0].esn
                    logger.info(f"Using ESN {session.device.esn} for EyePatch filter check.")

                if session.device.esn is not None:
                    has_eyepatch = session.is_esn_connected_to_eyepatch()
                    if not has_eyepatch:
                        logger.info("Removing EyePatch tests, because this ESN does not have a configured EyePatch.")
                        session.plan_request.testplan.testcases = [
                            elt
                            for elt in session.plan_request.testplan.testcases
                            if (elt.tags is None or (elt.tags is not None and "batch_ep" not in elt.tags.split(",")))
                        ]
                    else:
                        logger.info("Not removing EyePatch tests because this device has a configured EyePatch.")
                else:
                    logger.info("Not removing EyePatch tests because we could not locate a matching device.")

            except (ValueError, KeyError):
                logger.info("There was a problem getting the list of EyePatch connected devices, so the test plan will be unchanged")

        # BUT make sure you didn't remove -all- the tests.
        if len(session.plan_request.testplan.testcases) == 0:
            logger.critical(
                "We removed all the tests from the test plan. Instead of waiting for the "
                "Automator to tell us the test plan was empty, we will abort here."
            )
            sys.exit(1)

        # create these whether or not we use them
        when_done_instance = PrintResultsWhenDoneClass(skip_download=False, result_file=result_file)
        waiter = BlockMainThreadUntilCompleteMonitor()

        if not no_wait:
            if not skip_print_after:
                session.status_watchers.append(when_done_instance)
            if print_during:
                session.status_watchers.append(PrintResultsWhileRunningClass(result_file=result_file))
            # put this one last so we wait for analysis to finish in other classes
            session.status_watchers.append(waiter)

        logger.info(
            f"Running {colorama.Fore.BLUE}{len(session.plan_request.testplan.testcases)}{colorama.Style.RESET_ALL} "
            f"tests with device target '{session.device.to_json()}'. "
        )
        session.run_tests()

        if not no_wait:
            waiter.finished.wait()
            if when_done_instance.my_thread:
                pending_thread = when_done_instance.my_thread
                pending_thread.join(timeout=15.0)
