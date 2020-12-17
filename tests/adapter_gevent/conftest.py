import pytest
import webtest

from testing_support.fixtures import (collector_agent_registration_fixture,
    collector_available_fixture)

_default_settings = {
    'transaction_tracer.explain_threshold': 0.0,
    'transaction_tracer.transaction_threshold': 0.0,
    'transaction_tracer.stack_trace_threshold': 0.0,
    'debug.log_data_collector_payloads': True,
    'debug.record_transaction_failure': True,
    'debug.disable_harvest_until_shutdown': False,
}

collector_agent_registration = collector_agent_registration_fixture(
        app_name='Python Agent Test (adapter_gevent)',
        default_settings=_default_settings)

@pytest.fixture(autouse=True, scope='session')
def target_application():
    import _application
    port = _application.setup_application()
    return webtest.TestApp('http://localhost:%d' % port)

@pytest.fixture(scope='session')
def session_initialization(collector_agent_registration):
    pass

@pytest.fixture(scope='function')
def requires_data_collector(collector_available_fixture):
    pass