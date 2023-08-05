from ntscli_cloud_lib.stateful_session import stateful_session_mgr

# Implementation libs
from ntsjson.functions import make_basic_options_dict, set_log_levels_of_libs


def get_plan_impl(rae, esn, ip, serial, configuration, testplan):
    set_log_levels_of_libs()
    options = make_basic_options_dict(esn, ip, rae, serial, configuration)

    with stateful_session_mgr(**options) as session:
        session.get_test_plan()  # reminder: stored in the session object at session.plan_request
        plan_as_str: str = session.plan_request.to_json(indent=4)
        testplan.write(plan_as_str)
