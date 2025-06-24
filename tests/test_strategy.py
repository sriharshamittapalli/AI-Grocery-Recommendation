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

# Stub streamlit so importing modules does not fail
streamlit_stub = _types.ModuleType('streamlit')
streamlit_stub.secrets = {}

def _dummy(*args, **kwargs):
    return None

for name in [
    'set_page_config', 'title', 'subheader', 'text_input', 'multiselect',
    'checkbox', 'slider', 'text_area', 'button', 'status', 'success', 'error',
    'tabs', 'info', 'warning', 'dataframe', 'header', 'metric', 'markdown',
    'link_button', 'caption'
]:
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

import agents


# helper to build strategist with deterministic data

def _setup_strategist():
    items = ['milk', 'bread', 'eggs']
    stores = [
        {'name': 'Walmart', 'chain': 'Walmart', 'address': 'A', 'lat': 0, 'lng': 0},
        {'name': 'Target', 'chain': 'Target', 'address': 'B', 'lat': 0, 'lng': 0},
        {'name': 'Kroger', 'chain': 'Kroger', 'address': 'C', 'lat': 0, 'lng': 0},
    ]
    price_data = agents.estimate_prices_simple(items, stores)
    strategist = agents.ShoppingStrategist({'lat': 0, 'lng': 0}, items, price_data)
    return strategist, stores


def _patch_travel(monkeypatch):
    monkeypatch.setattr(
        agents,
        'get_trip_details_from_api',
        lambda loc, stores: {'distance_meters': 0, 'duration_seconds': 0, 'optimized_stores': stores},
    )
    monkeypatch.setattr(
        agents,
        'calculate_travel_costs',
        lambda dist, dur: {
            'gas_cost': 0,
            'time_cost': 0,
            'distance_miles': 0,
            'time_hours': 0,
            'total_travel_cost': 0,
        },
    )


def test_scenario_2_suggestions_mode(monkeypatch):
    strategist, stores = _setup_strategist()
    _patch_travel(monkeypatch)
    plan = strategist.find_best_strategy(stores, strict_mode=False, preferred_store_names=['Walmart', 'Target'])
    assert isinstance(plan, dict)
    assert plan['scenario'] == 'scenario_2_suggestions_mode'


def test_scenario_3_strict_mode(monkeypatch):
    strategist, stores = _setup_strategist()
    _patch_travel(monkeypatch)
    plan = strategist.find_best_strategy(stores, strict_mode=True, preferred_store_names=['Walmart', 'Target'])
    assert isinstance(plan, dict)
    assert plan['scenario'] == 'scenario_3_strict_mode'
