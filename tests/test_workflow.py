import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Provide a minimal stub for the requests package so agents.py can be imported
import types as _types
requests_stub = _types.ModuleType('requests')
def _dummy_get(*args, **kwargs):
    class _Resp:
        def json(self):
            return {}
    return _Resp()
requests_stub.get = _dummy_get
sys.modules.setdefault('requests', requests_stub)

# Stub streamlit so importing app does not fail
streamlit_stub = _types.ModuleType('streamlit')
streamlit_stub.secrets = {}
def _dummy(*args, **kwargs):
    return None
for name in ['set_page_config', 'title', 'subheader', 'text_input', 'multiselect', 'checkbox', 'slider', 'text_area', 'button', 'status', 'success', 'error', 'tabs', 'info', 'warning', 'dataframe', 'header', 'metric', 'markdown', 'link_button', 'caption']:
    setattr(streamlit_stub, name, _dummy)
sys.modules.setdefault('streamlit', streamlit_stub)

# stub dotenv
dotenv_stub = _types.ModuleType('dotenv')
def load_dotenv(*args, **kwargs):
    return None
dotenv_stub.load_dotenv = load_dotenv
sys.modules.setdefault('dotenv', dotenv_stub)

# stub pandas
pandas_stub = _types.ModuleType('pandas')
pandas_stub.DataFrame = object
pandas_stub.read_csv = lambda *a, **k: None
pandas_stub.__version__ = '0.0'
sys.modules.setdefault('pandas', pandas_stub)

import types
import agents
from app import GoogleADKMultiAgent
import mock_data


def test_llm_agent_fallback():
    agent = agents.LlmAgent(name="test")
    resp = agent.run("hello")
    assert isinstance(resp, str)


def test_execute_workflow_returns_dict(monkeypatch):
    import app
    monkeypatch.setattr(agents, "ADK_AVAILABLE", False)
    monkeypatch.setattr(app, "ADK_AVAILABLE", False)
    monkeypatch.setattr(agents, "find_stores_with_maps_api", lambda loc, chains, max_distance: [{
        'name': 'StoreA', 'address': 'A', 'lat': 0, 'lng': 0, 'chain': 'A'
    }])
    monkeypatch.setattr(app, "find_stores_with_maps_api", lambda loc, chains, max_distance: [{
        'name': 'StoreA', 'address': 'A', 'lat': 0, 'lng': 0, 'chain': 'A'
    }])
    price_data = mock_data.get_scenario1_data()
    first_item = next(iter(price_data))
    monkeypatch.setattr(agents, "estimate_prices_simple", lambda items, stores: price_data)
    monkeypatch.setattr(app, "estimate_prices_simple", lambda items, stores: price_data)
    dummy_plan = {
        'plan_stores': ['StoreA'],
        'optimized_stores_in_route': [{'name': 'StoreA', 'address': 'A', 'lat': 0, 'lng': 0}],
        'shopping_list': {'StoreA': [{'item': first_item, 'price': 1.0}]},
        'item_cost': 1.0,
        'travel_costs': {
            'gas_cost': 0,
            'time_cost': 0,
            'distance_miles': 0,
            'time_hours': 0,
            'total_travel_cost': 0,
        },
        'total_plan_cost': 1.0,
        'savings': 0,
        'scenario': 'scenario_1_no_preferences'
    }
    monkeypatch.setattr(agents.ShoppingStrategist, 'find_best_strategy', lambda self, **kw: dummy_plan)
    monkeypatch.setattr(app.ShoppingStrategist, 'find_best_strategy', lambda self, **kw: dummy_plan)
    monkeypatch.setattr(agents, 'create_Maps_url', lambda loc, stores: 'http://maps.example')
    monkeypatch.setattr(app, 'create_Maps_url', lambda loc, stores: 'http://maps.example')

    workflow = GoogleADKMultiAgent()
    result = workflow.execute_shopping_workflow(
        {'lat': 0, 'lng': 0, 'formatted_address': 'Test'},
        [first_item],
        [],
        False,
        max_distance_miles=5,
    )

    assert isinstance(result, dict)
    assert result['status'] == 'success'
    assert 'advisor_response' in result


def test_calculate_travel_costs():
    result = agents.calculate_travel_costs(1609, 3600)
    assert result['gas_cost'] == 0.14
    assert result['time_hours'] == 1.0
    assert result['total_travel_cost'] == 20.14
