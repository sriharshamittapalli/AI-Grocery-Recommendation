import os
import requests
import json
from typing import List, Dict, Any
import itertools
from secrets_utils import get_secret


try:
    from google.adk import Agent
    from google.adk.tools import FunctionTool
    ADK_AVAILABLE = True
    
    class LlmAgent:
        def __init__(self, name=None, model=None, instructions=None, tools=None, **kwargs):
            self.name = name or kwargs.get('name', 'agent')
            self.model = model or 'gemini-2.5-flash'
            self.instructions = instructions
            self.tools = tools or []

            try: self._adk_agent = Agent(name=self.name, model=self.model)
            except Exception as e:
        
                self._adk_agent = None
            
        def run(self, request):
            if self._adk_agent is None: return f"[ADK AGENT {self.name}] Agent not available, processing: {str(request)[:100]}..."
            
            try:
                if isinstance(request, str): return self._adk_agent.run(request)
                else:
                    content = getattr(request, 'content', str(request))
                    return self._adk_agent.run(content)
            except Exception as e: return f"[ADK AGENT {self.name}] Processed request: {str(request)[:100]}... (Error: {e})"
    
    class AgentRequest:
        def __init__(self, content, context=None, **kwargs):
            self.content = content
            self.context = context or {}
    
    class AgentResponse:
        def __init__(self, content, **kwargs): self.content = content
            
except ImportError as e:
    
    ADK_AVAILABLE = False

    class LlmAgent:
        def __init__(self, **kwargs):
            self.name = kwargs.get('name', 'agent')
            self.model = kwargs.get('model', 'gemini-pro')
            self.instructions = kwargs.get('instructions', '')
            self.tools = kwargs.get('tools', [])
            
        def run(self, request): return f"[FALLBACK MODE] Agent {self.name} would process: {request}"
    
    class FunctionTool:
        def __init__(self, **kwargs):
            pass
    
    class AgentRequest:
        def __init__(self, content, **kwargs):
            self.content = content
    
    class AgentResponse:
        def __init__(self, content, **kwargs):
            self.content = content

AVERAGE_GAS_PRICE_PER_GALLON = 3.50 
AVERAGE_VEHICLE_MPG = 25.0 
VALUE_OF_TIME_PER_HOUR = 20.00

def find_stores_with_maps_api(location: str, preferred_chains: List[str], max_distance_miles: int = 15) -> List[Dict]:
    """
    Finds the single nearest store for each requested chain within a given radius.
    
    This function iterates through each specified grocery chain (e.g., 'Walmart', 'Target'). 
    For each chain, it queries the Google Places API to find all nearby locations. It then calculates
    the driving time and distance to every result and selects only the one with the shortest travel time.
    This ensures the application always considers the truly nearest store for each chain.
    """
    def _find_nearest_stores(loc, chains, key, max_distance_miles):
        if isinstance(loc, str):
            return []

        lat, lng = loc['lat'], loc['lng']
        final_stores = []
        
    
        
        # Iterate through each requested store chain
        for chain in chains[:5]: # Limit to 5 chains per request to be safe
    
            chain_candidates = [] # Stores all potential candidates for this chain
            
            try:
                # Use Google Places API to find stores
                search_params = {'query': f"{chain} near {lat},{lng}", 'location': f"{lat},{lng}", 'radius': max_distance_miles * 1609.34, 'key': key}
                response = requests.get("https://maps.googleapis.com/maps/api/place/textsearch/json", params=search_params, timeout=10)
                data = response.json()
                
                if data.get('status') == 'OK' and data.get('results'):
            
                    
                    # Iterate through ALL results from the API for this chain
                    for place in data['results']:
                        place_name = place.get('name', '').lower()
                        # Basic filter to ensure it's the correct store brand
                        if chain.lower() in place_name:
                            # Filter out secondary locations like gas stations or vision centers
                            is_main_store = not any(service_word in place_name for service_word in ['tire center', 'vision center', 'optical', 'pharmacy', 'gas station', 'auto center', 'distribution', 'office'])
                            if is_main_store:
                                place_lat = place['geometry']['location']['lat']
                                place_lng = place['geometry']['location']['lng']

                                # Use Google Distance Matrix API for accurate travel time
                                dist_params = {'origins': f"{lat},{lng}", 'destinations': f"{place_lat},{place_lng}", 'mode': 'driving', 'key': key}
                                
                                try:
                                    dist_response = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json", params=dist_params, timeout=10)
                                    dist_data = dist_response.json()
                                    
                                    if dist_data.get('status') == 'OK' and dist_data['rows'][0]['elements'][0]['status'] == 'OK':
                                        element = dist_data['rows'][0]['elements'][0]
                                        distance_miles = element['distance']['value'] / 1609.34
                                        
                                        # Add any store within the radius to our candidate list
                                        if distance_miles <= max_distance_miles:
                                            store = {
                                                'name': place['name'], 'address': place.get('formatted_address', ''),
                                                'lat': place_lat, 'lng': place_lng, 'rating': place.get('rating', 4.0),
                                                'chain': chain, 'place_id': place['place_id'],
                                                'travel_duration_seconds': element['duration']['value'],
                                                'distance_meters': element['distance']['value']
                                            }
                                            chain_candidates.append(store)
                                            
                                except Exception as e:
                                    print(f"    - Distance calculation failed for {place.get('name', 'a store')}: {e}")
                                    continue
                
                # After checking all results, select the BEST candidate for the current chain
                if chain_candidates:
                    # Sort candidates by travel time to find the closest one
                    chain_candidates.sort(key=lambda s: s.get('travel_duration_seconds', float('inf')))
                    best_store_for_chain = chain_candidates[0]
                    final_stores.append(best_store_for_chain)
                    
                    # Log the best store that was chosen for this chain
                    duration_min = best_store_for_chain.get('travel_duration_seconds', 0) / 60
                    distance_miles = best_store_for_chain.get('distance_meters', 0) / 1609.34
                    print(f"  ✅ Best for {chain}: {best_store_for_chain['name']} - {duration_min:.1f} min, {distance_miles:.1f} miles")
                else:
                    print(f"  ❌ No suitable {chain} stores found within {max_distance_miles} miles.")
                        
            except Exception as e:
                print(f"  ❌ Error searching for {chain}: {e}")
                continue
        
    
        return final_stores

    api_key = get_secret('GOOGLE_MAPS_API_KEY') or get_secret('Maps_API_KEY')
    if not api_key: raise ValueError("Google Maps API key is required.")
    if not location: raise ValueError("Location is required.")

    stores = _find_nearest_stores(location, preferred_chains, api_key, max_distance_miles)
    
    if not stores:
        print("No stores found after filtering.")
        return []
    
    # Sort the final list of the best stores for a clean display
    stores.sort(key=lambda s: s.get('travel_duration_seconds', float('inf')))
    
    print(f"\nFinal list of nearest stores (one per chain):")
    for i, store in enumerate(stores, 1):
        chain = store.get('chain', 'Unknown')
        duration_min = store.get('travel_duration_seconds', 0) / 60
        distance_miles = store.get('distance_meters', 0) / 1609.34
        print(f"  {i}. {store['name']} ({chain}) - {duration_min:.1f} min, {distance_miles:.1f} miles")
    
    return stores

def estimate_prices_simple(items: List[str], stores: List[Dict]) -> Dict:

    price_database = {
        'milk': {'Walmart': 3.48, 'Target': 3.79, 'Kroger': 3.29, 'Costco': 2.98, 'Whole Foods': 4.99, 'Safeway': 3.89, 'Meijer': 3.38},
        'bread': {'Walmart': 1.98, 'Target': 2.49, 'Kroger': 1.79, 'Costco': 1.49, 'Whole Foods': 3.99, 'Safeway': 2.29, 'Meijer': 1.88},
        'eggs': {'Walmart': 2.68, 'Target': 2.89, 'Kroger': 2.48, 'Costco': 4.99, 'Whole Foods': 5.49, 'Safeway': 2.99, 'Meijer': 2.58},
        'bananas': {'Walmart': 0.58, 'Target': 0.69, 'Kroger': 0.68, 'Costco': 1.48, 'Whole Foods': 0.99, 'Safeway': 0.79, 'Meijer': 0.68},
        'avocados': {'Walmart': 0.98, 'Target': 1.25, 'Kroger': 1.00, 'Costco': 4.99, 'Whole Foods': 2.49, 'Safeway': 1.49, 'Meijer': 0.98},
        'chicken breast': {'Walmart': 3.98, 'Target': 4.49, 'Kroger': 3.79, 'Costco': 2.99, 'Whole Foods': 7.99, 'Safeway': 4.99, 'Meijer': 3.88},
        'rice': {'Walmart': 2.98, 'Target': 3.49, 'Kroger': 2.79, 'Costco': 8.99, 'Whole Foods': 4.99, 'Safeway': 3.29, 'Meijer': 2.88},
        'pasta': {'Walmart': 1.48, 'Target': 1.79, 'Kroger': 1.29, 'Costco': 3.99, 'Whole Foods': 2.99, 'Safeway': 1.89, 'Meijer': 1.38}
    }
    
    prices = {}
    for item in items:
        item_lower = item.lower()
        prices[item] = {}
        
        for store in stores:
            chain = store.get('chain', '')
            store_name = store.get('name', chain)

            if item_lower in price_database and chain in price_database[item_lower]:
                price = price_database[item_lower][chain]
            else:

                base_price = 3.00
                if 'walmart' in store_name.lower(): price = base_price * 0.9
                elif 'target' in store_name.lower(): price = base_price * 0.95
                elif 'meijer' in store_name.lower(): price = base_price * 0.88
                elif 'whole foods' in store_name.lower(): price = base_price * 1.2
                elif 'kroger' in store_name.lower(): price = base_price * 0.93
                elif 'safeway' in store_name.lower(): price = base_price * 1.05
                elif chain == 'General': price = base_price * 1.0
                else: price = base_price
            
            prices[item][store_name] = { 'price': round(price, 2), 'confidence': 0.8 }
    
    return prices

def get_trip_details_from_api(user_location: Dict, stores: List[Dict]) -> Dict:

    
    api_key = get_secret('GOOGLE_MAPS_API_KEY') or get_secret('Maps_API_KEY')
    if not api_key: raise ValueError("Google Maps API key is required for accurate distance calculations. Please add GOOGLE_MAPS_API_KEY to your .env file or Streamlit secrets.")
    if not stores: return {'distance_meters': 0, 'duration_seconds': 0, 'optimized_stores': []}

    origin = f"{user_location['lat']},{user_location['lng']}"
    destination = origin

    waypoints_str = "|".join([f"{s['lat']},{s['lng']}" for s in stores])
    params = { "origin": origin, "destination": destination, "waypoints": f"optimize:true|{waypoints_str}", "key": api_key, "mode": "driving" }

    try:
        url = "https://maps.googleapis.com/maps/api/directions/json"
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data['status'] == 'OK' and data['routes']:
            route = data['routes'][0]
            total_distance_meters = sum(leg['distance']['value'] for leg in route['legs'])
            total_duration_seconds = sum(leg['duration']['value'] for leg in route['legs'])

            optimized_order = route.get('waypoint_order', [])
            print(f"--- Google's Optimized Waypoint Order: {optimized_order} ---")
            if optimized_order: optimized_stores = [stores[i] for i in optimized_order]
            else: optimized_stores = stores

            return { 'distance_meters': total_distance_meters, 'duration_seconds': total_duration_seconds, 'optimized_stores': optimized_stores }
        
        else: raise ValueError(f"Google Directions API failed: {data.get('status')}. Cannot calculate accurate distances without API access.")

    except Exception as e:
        print(f"Trip details API error: {e}")
        raise ValueError(f"Failed to calculate trip details: {str(e)}. Accurate distance calculation requires Google Maps API access.")

def calculate_travel_costs(distance_meters: int, duration_seconds: int) -> Dict[str, float]:
    distance_miles = distance_meters / 1609.34
    gallons_used = distance_miles / AVERAGE_VEHICLE_MPG
    gas_cost = gallons_used * AVERAGE_GAS_PRICE_PER_GALLON
    hours_spent = duration_seconds / 3600
    time_cost = hours_spent * VALUE_OF_TIME_PER_HOUR
    
    # This corrected line adds the value of your time to the gas cost.
    total_travel_cost = gas_cost + time_cost
    
    return { 
        "gas_cost": round(gas_cost, 2), 
        "time_cost": round(time_cost, 2), 
        "time_hours": round(hours_spent, 2), 
        "distance_miles": round(distance_miles, 2), 
        "total_travel_cost": round(total_travel_cost, 2) 
    }

class ShoppingStrategist:
    def __init__(self, user_location, all_items, price_data):
        self.user_location = user_location
        self.all_items = all_items
        self.price_data = price_data
        self.store_names = sorted(list(price_data[next(iter(price_data))].keys()))

    def _calculate_plan_costs(self, stores_to_visit_names: List[str], all_stores_info: List[Dict]):
        stores_to_visit_names = sorted(stores_to_visit_names)
        shopping_list = {}
        total_item_cost = 0

        for item in sorted(self.all_items):
            best_price_for_item = float('inf')
            best_store_for_item = None

            for store_name in sorted(stores_to_visit_names):
                price = self.price_data[item][store_name]['price']
                if price < best_price_for_item:
                    best_price_for_item = price
                    best_store_for_item = store_name
            
            if best_store_for_item:
                if best_store_for_item not in shopping_list: shopping_list[best_store_for_item] = []
                shopping_list[best_store_for_item].append({'item': item, 'price': best_price_for_item})
                total_item_cost += best_price_for_item
        

        stores_to_visit_details = [s for s in all_stores_info if s['name'] in stores_to_visit_names]
        stores_to_visit_details.sort(key=lambda x: x['name'])
        
        if not stores_to_visit_details: return None

        trip_details = get_trip_details_from_api(self.user_location, stores_to_visit_details)
        travel_costs = calculate_travel_costs(trip_details['distance_meters'], trip_details['duration_seconds'])

        total_plan_cost = total_item_cost + travel_costs['total_travel_cost']

        return { "plan_stores": sorted(stores_to_visit_names), "optimized_stores_in_route": trip_details.get('optimized_stores', []), "shopping_list": shopping_list, "item_cost": round(total_item_cost, 2), "travel_costs": travel_costs, "total_plan_cost": round(total_plan_cost, 2) }

    def find_best_strategy(self, available_stores: List[Dict], strict_mode: bool = False, preferred_store_names: List[str] = None):
        all_plans = []
        store_pool = sorted([s['name'] for s in available_stores if s['name'] in self.store_names])
        
        if not preferred_store_names or len(preferred_store_names) == 0:
            print("Scenario 1: No store preferences - full algorithm optimization")
            for i in range(1, min(4, len(store_pool) + 1)):
                for combo in sorted(itertools.combinations(store_pool, i)):
                    plan = self._calculate_plan_costs(list(combo), available_stores)
                    if plan: all_plans.append(plan)
                        
        elif strict_mode:
            print("Scenario 3: Strict mode - must visit all selected stores")
            preferred_store_names = sorted(preferred_store_names)            
            plan_stores = []
            used_chains = set()
            missing_chains = []
            
            for preferred_chain in preferred_store_names:
                if preferred_chain in used_chains: continue
                matching_stores = [s['name'] for s in available_stores 
                                 if s.get('chain', '').lower() == preferred_chain.lower() 
                                 or preferred_chain.lower() in s['name'].lower()]
                if matching_stores:
                    matching_stores.sort()
                    plan_stores.append(matching_stores[0])
                    used_chains.add(preferred_chain)
                    print(f"Mapped {preferred_chain} -> {matching_stores[0]}")
                else:
                    print(f"Warning: No stores found for required chain '{preferred_chain}' in strict mode")
                    missing_chains.append(preferred_chain)
            
            if plan_stores:
                print(f"Strict mode: Planning route for {sorted(plan_stores)}")
                plan = self._calculate_plan_costs(plan_stores, available_stores)
                if plan:
                    if missing_chains:
                        plan['warning'] = f"Note: Could not find these required stores in your area: {', '.join(missing_chains)}. Consider disabling strict mode or selecting different stores."
                        plan['missing_chains'] = missing_chains
                    all_plans.append(plan)
                else: print("Failed to calculate costs for strict mode plan")
            else: print("Strict mode failed: No matching stores found")
                
        else:
            print("Scenario 2: Store preferences as suggestions - algorithm can modify")
            unique_preferred = sorted(list(dict.fromkeys(preferred_store_names)))
            preferred_in_pool = []
            
            for preferred_chain in unique_preferred:
                matching_stores = [s['name'] for s in available_stores 
                                 if s.get('chain', '').lower() == preferred_chain.lower() 
                                 or preferred_chain.lower() in s['name'].lower()]
                if matching_stores:
                    matching_stores.sort()
                    preferred_in_pool.append(matching_stores[0])
            
            preferred_in_pool.sort()
            
            if preferred_in_pool:
                for i in range(1, len(preferred_in_pool) + 1):
                    for combo in sorted(itertools.combinations(preferred_in_pool, i)):
                        plan = self._calculate_plan_costs(list(combo), available_stores)
                        if plan: all_plans.append(plan)
            
            for store_name in sorted(store_pool):
                if store_name not in preferred_in_pool:
                    plan = self._calculate_plan_costs([store_name], available_stores)
                    if plan: all_plans.append(plan)

        if not all_plans: return None
        all_plans.sort(key=lambda p: (p['total_plan_cost'], p['plan_stores']))
        best_plan = all_plans[0]
        single_store_costs = []
        for plan in all_plans:
            if len(plan['plan_stores']) == 1: single_store_costs.append(plan['total_plan_cost'])
        if single_store_costs:
            worst_single_store_cost = max(single_store_costs)
            best_plan['savings'] = round(max(0, worst_single_store_cost - best_plan['total_plan_cost']), 2)
        else: best_plan['savings'] = 0
        best_plan['total_plans_evaluated'] = len(all_plans)
        best_plan['is_single_store'] = len(best_plan['plan_stores']) == 1
        best_plan['scenario'] = (
            "scenario_1_no_preferences" if not preferred_store_names or len(preferred_store_names) == 0 else
            "scenario_3_strict_mode" if strict_mode else
            "scenario_2_suggestions_mode"
        )
    
        return best_plan

def create_Maps_url(user_location: Dict[str, Any], stores: List[Dict[str, Any]]) -> str:
    if not stores or 'lat' not in user_location or 'lng' not in user_location: return ""
    import urllib.parse
    # FIX: Use the standard, reliable Google Maps URL
    base_url = "https://www.google.com/maps/dir/"
    origin = f"{user_location['lat']},{user_location['lng']}"
    waypoints = [urllib.parse.quote(s['address']) for s in stores if 'address' in s]
    destination = origin
    all_stops = [origin] + waypoints + [destination]
    return base_url + "/".join(all_stops)

def create_store_finder_tool():
    if not ADK_AVAILABLE: return None
    try: return FunctionTool(func=find_stores_with_maps_api)
    except Exception: return None

store_finder_agent = LlmAgent( name="store_finder", model="gemini-2.5-flash" if ADK_AVAILABLE else "gemini-pro", description="Finds nearby grocery stores using Google Places API", instruction="""You are a specialized store finder agent that locates grocery stores.""", tools=[t for t in [create_store_finder_tool()] if t is not None] if ADK_AVAILABLE else [] )

price_optimizer_agent = LlmAgent( name="price_optimizer", model="gemini-2.5-flash" if ADK_AVAILABLE else "gemini-pro", description="Optimizes pricing across multiple stores", instruction="You are a specialized price optimization agent that finds the best deals across stores." )
route_optimizer_agent = LlmAgent( name="route_optimizer", model="gemini-2.5-flash" if ADK_AVAILABLE else "gemini-pro", description="Optimizes travel routes between stores", instruction="You are a specialized route optimization agent that finds the most efficient travel paths." )
shopping_advisor_agent = LlmAgent( name="shopping_advisor", model="gemini-2.5-flash" if ADK_AVAILABLE else "gemini-pro", description="Provides comprehensive shopping recommendations", instruction="You are a shopping advisor agent that provides personalized recommendations based on cost-benefit analysis." )
root_agent = LlmAgent( name="root_coordinator", model="gemini-2.5-flash" if ADK_AVAILABLE else "gemini-pro", description="Coordinates the multi-agent workflow", instruction="You are the root coordinator agent that orchestrates the entire shopping optimization workflow." )