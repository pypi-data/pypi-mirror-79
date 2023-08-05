import sys

from ntscli_cloud_lib.stateful_session import stateful_session_mgr

# Implementation libs
from ntsjson.functions import make_basic_options_dict, set_log_levels_of_libs
from ntsjson.log import logger


def cancel_impl(rae, esn, ip, serial, configuration):
    """
    Cancel any pending tests for a specified device.
    """
    if not esn and not ip and not serial:
        logger.critical("No device identifier was set. cancel requires a device ID (--esn, --ip, or --serial) and a RAE number. ")
        sys.exit(1)
    set_log_levels_of_libs()
    options = make_basic_options_dict(esn, ip, rae, serial, configuration)

    with stateful_session_mgr(**options) as session:
        session.cancel()

    sys.exit(0)
