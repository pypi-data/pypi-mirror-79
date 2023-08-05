import json
from json import JSONDecodeError
import platform
import re
import sys
from typing import Optional, TextIO, Tuple

import colorama
from ntscli_cloud_lib.automator import DeviceIdentifier, TestPlanRunRequest

# Implementation libs
from ntsjson.functions import set_log_levels_of_libs
from ntsjson.log import logger

if platform.system() != "Windows":
    import fcntl
    from os import O_NONBLOCK


def filter_impl(
    rae,
    esn,
    ip,
    serial,
    testplan: TextIO,
    batch: str,
    names: Tuple[str, ...],
    names_re: str,
    eyepatch: bool,
    categories: Optional[str],
    tags: Optional[str],
    result_file: Optional[TextIO],
):
    """Filter tests out of a test plan."""
    set_log_levels_of_libs()

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
            logger.info(f"There was no data in {testplan.name}. Aborting.")
            sys.exit(1)
        else:
            try:
                chosen_plan = TestPlanRunRequest().from_dict(value=(json.loads(source_str, encoding="utf-8")))
                # now you can inspect the test plan loaded from file to see if it looks like it's valid
                logger.info(f"Loaded {len(chosen_plan.testplan.testcases)} tests from file.")
            except (JSONDecodeError, KeyError, TypeError) as err:
                logger.critical("The source file did not parse as JSON:")
                logger.critical(err)
                sys.exit(1)

    if rae or ip or esn or serial:
        chosen_plan.target = DeviceIdentifier(rae=rae, ip=ip, esn=esn, serial=serial)
        logger.info("Replacing the target device with:")
        logger.info(chosen_plan.target.to_json())

    logger.info(
        f"Before editing, test plan included {colorama.Fore.BLUE}{len(chosen_plan.testplan.testcases)}{colorama.Style.RESET_ALL} tests."
    )
    if batch is not None:
        chosen_plan.testplan.batch_name = batch

    # add a name filter
    if names:
        nlist = list(names)
        logger.info(f"Removing tests with names not in {', '.join(names)} at the user's request.")
        chosen_plan.testplan.testcases = [elt for elt in chosen_plan.testplan.testcases if elt.name in nlist]

    # add a name regex filter
    if names_re:
        logger.info(f"Removing tests with names not matching {names_re} at the user's request.")
        try:
            pattern = re.compile(names_re)
            chosen_plan.testplan.testcases = [elt for elt in chosen_plan.testplan.testcases if pattern.match(elt.name)]
        except re.error:
            logger.critical("Could not compile your regex.")
            sys.exit(1)

    # add a category filter
    if categories:
        logger.info(f"Removing tests with categories not in {categories} at the user's request.")
        clist = categories.split(",")
        if len(clist) > 0:
            chosen_plan.testplan.testcases = [elt for elt in chosen_plan.testplan.testcases if elt.category in clist]

    if tags:
        logger.info(f"Removing tests without any of the tags in {tags} at the user's request.")
        user_tag_set = set(tags.split(","))
        if len(user_tag_set) > 0:
            chosen_plan.testplan.testcases = [
                elt for elt in chosen_plan.testplan.testcases if elt.tags if len(set(elt.tags.split(",")).intersection(user_tag_set)) > 0
            ]

    if eyepatch:
        logger.info("Removing EyePatch tests at the user's request.")
        chosen_plan.testplan.testcases = [
            elt
            for elt in chosen_plan.testplan.testcases
            if (elt.tags is None or (elt.tags is not None and "batch_ep" not in elt.tags.split(",")))
        ]

    # BUT make sure you didn't remove -all- the tests.
    if len(chosen_plan.testplan.testcases) == 0:
        logger.critical(
            "We removed all the tests from the test plan. Instead of waiting for the "
            "Automator to tell us the test plan was empty, we will abort here."
        )
        sys.exit(1)

    logger.info(
        f"After editing, the test plan included {colorama.Fore.BLUE}{len(chosen_plan.testplan.testcases)}{colorama.Style.RESET_ALL} "
        f"tests with device target '{chosen_plan.target.to_json()}'. "
    )

    plan_as_str: str = chosen_plan.to_json(indent=4)
    result_file.write(plan_as_str)
