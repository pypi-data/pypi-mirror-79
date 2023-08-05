import sys

from ntscli_cloud_lib.stateful_session import stateful_session_mgr

# Implementation libs
from ntsjson.functions import make_basic_options_dict, set_log_levels_of_libs


def cancel_impl(rae, esn, ip, serial, configuration):
    """
    Cancel any pending tests for a specified device.
    """
    set_log_levels_of_libs()
    options = make_basic_options_dict(esn, ip, rae, serial, configuration)

    with stateful_session_mgr(**options) as session:
        session.cancel()

    sys.exit(0)
