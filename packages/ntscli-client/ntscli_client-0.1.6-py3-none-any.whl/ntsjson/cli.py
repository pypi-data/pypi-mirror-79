#!/usr/bin/env python3
#  Copyright (c) 2020 Netflix.
#  All rights reserved.
#
import platform
import sys

import click
import click_completion.core
import click_log
from ntscli_cloud_lib import click_sanitize_rae_names
from ntscli_cloud_lib.stateful_session import stateful_session_mgr

# Implementation libs
import ntsjson
from ntsjson import __version__
from ntsjson.batch_result_impl import batch_result_impl
from ntsjson.cancel_impl import cancel_impl
from ntsjson.completion_group import completion, custom_startswith
from ntsjson.config import config_set_group
from ntsjson.filter_impl import filter_impl
from ntsjson.functions import nonblock_target_write, set_log_levels_of_libs
from ntsjson.get_device_list_impl import get_device_list_impl
from ntsjson.get_plan_impl import get_plan_impl
from ntsjson.log import logger
from ntsjson.run_impl import run_impl
from ntsjson.ssl_click_group import ssl_group
from ntsjson.status_impl import status_impl

if platform.system() != "Windows":
    pass

mydir = ""
last_message = {}

RAE_HELP_STR = "The Netflix RAE device serial to connect to, such as r3010203. Defaults to environment variable 'RAE'."
ESN_HELP_STR = "The ESN of the target device."
IP_HELP_STR = "The IP address of the target device."
SERIAL_HELP_STR = "The serial number of the target device."
SSL_CONFIG_HELP_STR = "The security configuration directory to use from ~/.config/netflix."
SSL_ENV_VAR = "NTS_SSL_CONFIG_DIR"


@click.group(name="default")
@click.version_option(__version__.__version__)
def default():
    """
    NTS CLI 2.0 reference implementation

    Each command has its own --help option to show its usage.

    Tab completion is available for fish, Zsh, Bash and PowerShell. Run:

    nts completion print

    or

    nts completion install --help

    for more information.
    """
    set_log_levels_of_libs()


@default.command(name="has-eyepatch", short_help="Does an ESN have an EyePatch config?")
@click.option(
    "--rae",
    type=str,
    required=True,
    help=RAE_HELP_STR,
    envvar="RAE",
    callback=click_sanitize_rae_names,
)
@click.option(
    "--config",
    "configuration",
    type=str,
    default="cloud",
    show_default=True,
    help=SSL_CONFIG_HELP_STR,
    envvar=SSL_ENV_VAR,
)
@click.option(
    "--esn",
    type=str,
    required=True,
    help=ESN_HELP_STR,
    envvar="ESN",
)
@click.option(
    "--save-to",
    type=click.File("w", encoding="utf-8"),
    help="Defaults to stdout. Optionally a file to save to instead.",
    default=sys.stdout,
)
@click_log.simple_verbosity_option(logger, default=ntsjson.VERBOSE_DEFAULT_LEVEL, help=ntsjson.VERBOSE_HELP)
def is_esn_connected_to_eyepatch(rae, configuration, esn, save_to):
    """
    Test whether a device has an EyePatch configuration.
    """

    with stateful_session_mgr(rae=rae, configuration=configuration, esn=esn) as session:
        has_eyepatch = session.is_esn_connected_to_eyepatch()
        if has_eyepatch is None:
            logger.critical(
                "The request failed to reach the Automator due to a bug in the sample code. Definitely contact Netflix about this."
            )
        elif has_eyepatch:
            logger.info("This ESN has a configured EyePatch.")
            nonblock_target_write(save_to, "true")
            sys.exit(0)
        else:
            logger.info(
                "This ESN is not in the list of devices with a configured EyePatch, but could simply be missing. You can check with get-"
                "device-list."
            )
            nonblock_target_write(save_to, "false")
            sys.exit(1)


@default.command(name="get-devices", short_help="List devices behind a RAE")
@click.option(
    "--rae",
    type=str,
    required=True,
    help=RAE_HELP_STR,
    envvar="RAE",
    callback=click_sanitize_rae_names,
)
@click.option(
    "--config",
    "configuration",
    type=str,
    default="cloud",
    show_default=True,
    help=SSL_CONFIG_HELP_STR,
    envvar=SSL_ENV_VAR,
)
@click.option(
    "--save-to",
    type=click.File("w", encoding="utf-8"),
    help="Defaults to stdout. Optionally a file to save to instead.",
    default=sys.stdout,
)
@click_log.simple_verbosity_option(logger, default=ntsjson.VERBOSE_DEFAULT_LEVEL, help=ntsjson.VERBOSE_HELP)
def get_device_list(*args, **kwargs):
    """
    List devices on a remote RAE.
    """
    get_device_list_impl(*args, **kwargs)


@default.command(name="run", short_help="Run a test plan")
@click.option(
    "--rae",
    type=str,
    required=True,
    help=RAE_HELP_STR,
    envvar="RAE",
    callback=click_sanitize_rae_names,
)
@click.option(
    "--esn",
    type=str,
    help=ESN_HELP_STR,
    envvar="ESN",
)
@click.option(
    "--ip",
    type=str,
    help=IP_HELP_STR,
    envvar="DUT_IP",
)
@click.option(
    "--serial",
    type=str,
    help=SERIAL_HELP_STR,
    envvar="DUT_SERIAL",
)
@click.option(
    "--wait/--no-wait",
    default=True,
    help="Should this process block until tests are done?",
)
@click.option(
    "--testplan",
    type=click.File("r", encoding="utf-8"),
    default=sys.stdin,
    help="JSON formatted test plan. Accepted from file or stdin.",
)
@click.option("--batch", type=str, help="A batch name to locate this run in NTS")
@click.option(
    "--names",
    type=str,
    help="Filter your tests to only names in a CSV list: 'AUDIO-001-TC1,DRS-AL1-25FPS-HEAAC-DWN'",
)
@click.option("--names-re", type=str, help="Filter your test names by regex: DRS.*")
@click.option(
    "--categories",
    type=str,
    help="An optional CSV field (remember quotes for spaces). Filter your test plan to these categories.",
)
@click.option(
    "--config",
    "configuration",
    type=str,
    default="cloud",
    show_default=True,
    help=SSL_CONFIG_HELP_STR,
    envvar=SSL_ENV_VAR,
)
@click.option("--force-keep-eyepatch", is_flag=True, help="Keep EyePatch tests, even if you do not have a configured EyePatch.")
@click.option("--print-during", is_flag=True, help="Print status updates while tests run.")
@click.option("--skip-print-after", is_flag=True, help="Skip printing the final status updates.")
@click.option(
    "--save-to",
    "result_file",
    type=click.File("w", encoding="utf-8"),
    help="Defaults to stdout. Optionally a file to save to instead.",
    default=sys.stdout,
)
@click.option(
    "--tags",
    type=str,
    help="An optional CSV field. Filter your test plan to only include these tags.",
)
@click.argument("testnames", type=str, nargs=-1)
@click_log.simple_verbosity_option(logger, default=ntsjson.VERBOSE_DEFAULT_LEVEL, help=ntsjson.VERBOSE_HELP)
def run(*args, **kwargs):
    """Sample code for what could be a much more intricate CI client."""
    run_impl(*args, **kwargs)


@default.command(name="filter", short_help="Filter a test plan")
@click.option(
    "--rae",
    type=str,
    help="Rewrite the destination RAE",
    callback=click_sanitize_rae_names,
)
@click.option(
    "--esn",
    type=str,
    help="Rewrite the destination ESN",
)
@click.option(
    "--ip",
    type=str,
    help="Rewrite the destination IP",
)
@click.option(
    "--serial",
    type=str,
    help="Rewrite the ADB serial number",
)
@click.option(
    "--testplan",
    type=click.File("r", encoding="utf-8"),
    default=sys.stdin,
    help="JSON formatted test plan. Accepted from file or stdin.",
)
@click.option("--batch", type=str, help="A batch name to locate this run in NTS")
@click.option("--names-re", type=str, help="Filter your test names by regex: DRS.*")
@click.option(
    "--categories",
    type=str,
    help="An optional CSV field (remember quotes for spaces). Filter your test plan to these categories.",
)
@click.option("--eyepatch", is_flag=True)
@click.option(
    "--save-to",
    "result_file",
    type=click.File("w", encoding="utf-8"),
    help="Defaults to stdout. Optionally a file to save to instead.",
    default=sys.stdout,
)
@click.option(
    "--tags",
    type=str,
    help="An optional CSV field. Filter your test plan to only include these tags.",
)
@click.argument("names", type=str, nargs=-1)
@click_log.simple_verbosity_option(logger, default=ntsjson.VERBOSE_DEFAULT_LEVEL, help=ntsjson.VERBOSE_HELP)
def filter_(*args, **kwargs):  # filter is a reserved word in python. careful!
    """Filter tests out of a test plan."""
    filter_impl(*args, **kwargs)


@default.command(name="cancel", short_help="Cancel the currently running test plan")
@click.option(
    "--rae",
    type=str,
    required=True,
    help=RAE_HELP_STR,
    envvar="RAE",
    callback=click_sanitize_rae_names,
)
@click.option(
    "--esn",
    type=str,
    help=ESN_HELP_STR,
    envvar="ESN",
)
@click.option(
    "--ip",
    type=str,
    help=IP_HELP_STR,
    envvar="DUT_IP",
)
@click.option(
    "--serial",
    type=str,
    help=SERIAL_HELP_STR,
    envvar="DUT_SERIAL",
)
@click.option(
    "--config",
    "configuration",
    type=str,
    default="cloud",
    show_default=True,
    help=SSL_CONFIG_HELP_STR,
    envvar=SSL_ENV_VAR,
)
@click_log.simple_verbosity_option(logger, default=ntsjson.VERBOSE_DEFAULT_LEVEL, help=ntsjson.VERBOSE_HELP)
def cancel(*args, **kwargs):
    """
    Cancel any pending tests for a specified device.
    """
    cancel_impl(*args, **kwargs)


@default.command(name="get-plan", short_help="Get the test plan for a device")
@click.option(
    "--rae",
    type=str,
    required=True,
    help=RAE_HELP_STR,
    envvar="RAE",
    callback=click_sanitize_rae_names,
)
@click.option(
    "--esn",
    type=str,
    help=ESN_HELP_STR,
    envvar="ESN",
)
@click.option(
    "--ip",
    type=str,
    help=IP_HELP_STR,
    envvar="DUT_IP",
)
@click.option(
    "--serial",
    type=str,
    help=SERIAL_HELP_STR,
    envvar="DUT_SERIAL",
)
@click.option(
    "--config",
    "configuration",
    type=str,
    default="cloud",
    show_default=True,
    help=SSL_CONFIG_HELP_STR,
    envvar=SSL_ENV_VAR,
)
@click.option(
    "--save-to",
    "testplan",
    type=click.File("w", encoding="utf-8"),
    help="Defaults to stdout. Optionally a file to save to instead.",
    default=sys.stdout,
)
@click_log.simple_verbosity_option(logger, default=ntsjson.VERBOSE_DEFAULT_LEVEL, help=ntsjson.VERBOSE_HELP)
def get_plan_from_device(*args, **kwargs):
    """
    Run the test on the device that retrieves and decodes a test plan as json.
    """
    get_plan_impl(*args, **kwargs)


@default.command(name="status", short_help="Get the Automator in-memory status")  # the wrappers taint the name, set it back
@click.option(
    "--config",
    "configuration",
    type=str,
    default="cloud",
    show_default=True,
    help=SSL_CONFIG_HELP_STR,
    envvar=SSL_ENV_VAR,
)
@click.option(
    "--rae",
    type=str,
    required=True,
    help=RAE_HELP_STR,
    envvar="RAE",
    callback=click_sanitize_rae_names,
)
@click.option(
    "--esn",
    type=str,
    help=ESN_HELP_STR,
    envvar="ESN",
)
@click.option(
    "--ip",
    type=str,
    help=IP_HELP_STR,
    envvar="DUT_IP",
)
@click.option(
    "--serial",
    type=str,
    help=SERIAL_HELP_STR,
    envvar="DUT_SERIAL",
)
@click.option(
    "--batch-id",
    "batch_id",
    type=str,
    help="The batch ID to get a result block for.",
)
@click.option(
    "--save-to",
    type=click.File("w", encoding="utf-8"),
    help="Defaults to stdout. Optionally a file to save to instead.",
    default=sys.stdout,
)
@click_log.simple_verbosity_option(logger, default=ntsjson.VERBOSE_DEFAULT_LEVEL, help=ntsjson.VERBOSE_HELP)
def status(**kwargs):
    """Get the status of the Automator instance on a given RAE."""
    status_impl(**kwargs)


@default.command(name="batch-result", short_help="Get the results of a batch on a device")  # the wrappers taint the name, set it back
@click.option(
    "--config",
    "configuration",
    type=str,
    default="cloud",
    show_default=True,
    help=SSL_CONFIG_HELP_STR,
    envvar=SSL_ENV_VAR,
)
@click.option(
    "--rae",
    type=str,
    required=True,
    help=RAE_HELP_STR,
    envvar="RAE",
    callback=click_sanitize_rae_names,
)
@click.option(
    "--esn",
    type=str,
    help=ESN_HELP_STR,
    envvar="ESN",
)
@click.option(
    "--ip",
    type=str,
    help=IP_HELP_STR,
    envvar="DUT_IP",
)
@click.option(
    "--serial",
    type=str,
    help=SERIAL_HELP_STR,
    envvar="DUT_SERIAL",
)
@click.option(
    "--save-to",
    type=click.File("w", encoding="utf-8"),
    help="Defaults to stdout. Optionally a file to save to instead.",
    default=sys.stdout,
)
@click.option("--skip-download", "-s", is_flag=True)
@click.argument("batch_id", type=str)
@click_log.simple_verbosity_option(logger, default=ntsjson.VERBOSE_DEFAULT_LEVEL, help=ntsjson.VERBOSE_HELP)
def batch_result(**kwargs):
    """Get the results of a batch on a device. Use 'latest' for the most recent."""
    batch_result_impl(**kwargs)


default.add_command(ssl_group)
default.add_command(config_set_group)
default.add_command(completion)

click_completion.core.startswith = custom_startswith
click_completion.init()

if __name__ == "__main__":  # pragma: no cover
    default()
