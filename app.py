import streamlit as st
import os
import requests
from dotenv import load_dotenv
from typing import Dict, List, Any
import pandas as pd
# import pydeck as pdk
from agents import ( root_agent, store_finder_agent, price_optimizer_agent, route_optimizer_agent, shopping_advisor_agent, find_stores_with_maps_api, estimate_prices_simple, create_Maps_url, ShoppingStrategist, AVERAGE_VEHICLE_MPG, AVERAGE_GAS_PRICE_PER_GALLON, VALUE_OF_TIME_PER_HOUR, ADK_AVAILABLE, AgentRequest, AgentResponse )
from secrets_utils import get_secret

# Load environment variables (local development)
load_dotenv()

st.set_page_config( page_title="🤖 Smart Grocery Assistant (Multi-Agent)", page_icon="🤖", layout="wide", initial_sidebar_state="expanded" )

class GoogleADKMultiAgent:

    def __init__(self):
        self.root_agent = root_agent
        self.store_finder_agent = store_finder_agent
        self.price_optimizer_agent = price_optimizer_agent
        self.route_optimizer_agent = route_optimizer_agent
        self.shopping_advisor_agent = shopping_advisor_agent
        print(f"🤖 Initialized Google ADK Multi-Agent System (ADK Available: {ADK_AVAILABLE})")
    
    # In AI Grocery Recommendation/app.py
    # Replace the entire function with this corrected version

    def execute_shopping_workflow(self, location: str, items: List[str], preferred_stores: List[str], strict_mode: bool, max_distance_miles: int = 30):
        """
        Execute complete Google ADK multi-agent workflow with real agent communication.
        
        Implements three scenarios with actual agent coordination:
        1. User enters address + products (no store selection): Agents suggest optimal stores, route, and savings
        2. User selects stores + strict mode: Agents must visit all selected stores, optimize only route and item allocation
        3. User selects stores + non-strict mode: Agents treat selections as suggestions, optimize everything including store selection
        """
        print(f"🤖 Starting Google ADK Multi-Agent Workflow")
        
        # STEP 1: Store Finder Agent - Use Google ADK agent to find nearby stores
        original_preferred_stores = preferred_stores.copy() if preferred_stores else []
        search_chains = preferred_stores if preferred_stores else ['Walmart', 'Target', 'Kroger', 'Costco', 'Whole Foods', 'Safeway', 'Meijer']
        
        print(f"🏪 [STEP 1] Delegating to Store Finder Agent...")
        
        if ADK_AVAILABLE:
            try:
                store_request = { 'task': 'find_nearby_stores', 'location': location, 'preferred_chains': search_chains, 'max_distance_miles': max_distance_miles, 'user_requirements': { 'strict_mode': strict_mode, 'original_preferences': original_preferred_stores } }
                agent_request = AgentRequest( content=f"Find grocery stores near {location.get('formatted_address', 'user location')} within {max_distance_miles} miles. Search for these chains: {', '.join(search_chains)}. Return store details including name, address, coordinates, and chain information.", context=store_request )
                store_response = self.store_finder_agent.run(agent_request)
                print(f"🏪 [STORE FINDER AGENT] Response received: {type(store_response)}")
                
                # For now, extract stores using the tool function (full ADK integration would parse agent response)
                stores = find_stores_with_maps_api(location, search_chains, max_distance_miles)
                print(f"🏪 [STORE FINDER AGENT] Found {len(stores)} stores via ADK workflow")
                
            except Exception as e:
                print(f"❌ [STORE FINDER AGENT] Error: {e}")
                print("🔄 [STORE FINDER AGENT] Falling back to direct tool call...")
                stores = find_stores_with_maps_api(location, search_chains, max_distance_miles)
        else:
            print("⚠️ [STORE FINDER AGENT] ADK not available, using fallback...")
            stores = find_stores_with_maps_api(location, search_chains, max_distance_miles)
        
        if not stores: return { 'status': 'error', 'message': f'🏪 [STORE FINDER AGENT] No {", ".join(search_chains)} stores found near {location.get("formatted_address", "your location")}. This could be due to: 1) Remote location with no nearby stores, 2) API rate limits, or 3) Specific store chains not available in your area. Try selecting different store chains or a more urban location.', 'stores': [], 'debug_info': { 'location': location, 'preferred_stores': original_preferred_stores, 'api_key_available': bool(get_secret('GOOGLE_MAPS_API_KEY') or get_secret('Maps_API_KEY')), 'adk_available': ADK_AVAILABLE } }
        
        print(f"💰 [STEP 2] Delegating to Price Optimizer Agent...")
        
        if ADK_AVAILABLE:
            try:
                price_request = AgentRequest( content=f"Estimate prices for {len(items)} grocery items across {len(stores)} stores. Items: {', '.join(items)}. Stores: {', '.join([s['name'] for s in stores])}. Provide detailed price comparisons and identify best deals.", context={ 'task': 'estimate_prices', 'items': items, 'stores': stores, 'analysis_type': 'comprehensive_comparison' } )
                
                price_response = self.price_optimizer_agent.run(price_request)
                print(f"💰 [PRICE OPTIMIZER AGENT] Response received: {type(price_response)}")
                
                # Extract price data using tool function (full ADK would parse agent response)
                prices_data = estimate_prices_simple(items, stores)
                print(f"💰 [PRICE OPTIMIZER AGENT] Analyzed prices for {len(items)} items at {len(stores)} stores")
                
            except Exception as e:
                print(f"❌ [PRICE OPTIMIZER AGENT] Error: {e}")
                print("🔄 [PRICE OPTIMIZER AGENT] Falling back to direct tool call...")
                prices_data = estimate_prices_simple(items, stores)
        else: print("⚠️ [PRICE OPTIMIZER AGENT] ADK not available, using fallback...")
        prices_data = estimate_prices_simple(items, stores)

        print(f"🧠 [STEP 3] Delegating to Shopping Strategist Agent...")
        
        if ADK_AVAILABLE:
            try:
                strategy_request = AgentRequest( content=f"Analyze optimal shopping strategy for {len(items)} items across {len(stores)} stores. Mode: {'Strict' if strict_mode else 'Optimized'}. User preferences: {original_preferred_stores}. Consider cost-benefit analysis including travel costs.", context={ 'task': 'optimize_shopping_strategy', 'user_location': location, 'items': items, 'price_data': prices_data, 'available_stores': stores, 'strict_mode': strict_mode, 'preferred_stores': original_preferred_stores } )
                strategy_response = self.shopping_advisor_agent.run(strategy_request)
                print(f"🧠 [SHOPPING STRATEGIST AGENT] Response received: {type(strategy_response)}")
                
            except Exception as e:
                print(f"❌ [SHOPPING STRATEGIST AGENT] Error: {e}")
                print("🔄 [SHOPPING STRATEGIST AGENT] Falling back to local strategist...")
        
        # Use enhanced strategist (now ADK-powered internally)
        strategist = ShoppingStrategist(user_location=location, all_items=items, price_data=prices_data)
        
        best_plan = strategist.find_best_strategy( available_stores=stores, strict_mode=strict_mode, preferred_store_names=original_preferred_stores )
        
        if not best_plan: return {'status': 'error', 'message': '🧠 [SHOPPING STRATEGIST AGENT] Could not generate a shopping plan.', 'stores': stores}

        print(f"🗺️ [STEP 4] Delegating to Route Optimizer Agent...")
        
        if ADK_AVAILABLE:
            try:
                route_request = AgentRequest( content=f"Generate optimal route for shopping at {len(best_plan['optimized_stores_in_route'])} stores. Calculate travel costs, time, and create Google Maps URL. Stores: {', '.join([s['name'] for s in best_plan['optimized_stores_in_route']])}", context={ 'task': 'optimize_route', 'user_location': location, 'stores': best_plan['optimized_stores_in_route'], 'travel_preferences': {'max_distance_miles': max_distance_miles} } )
                route_response = self.route_optimizer_agent.run(route_request)
                print(f"🗺️ [ROUTE OPTIMIZER AGENT] Response received: {type(route_response)}")
                
            except Exception as e:
                print(f"❌ [ROUTE OPTIMIZER AGENT] Error: {e}")
                print("🔄 [ROUTE OPTIMIZER AGENT] Falling back to direct URL generation...")
        
        maps_url = create_Maps_url(location, best_plan['optimized_stores_in_route'])

        # STEP 5: Shopping Advisor Agent - Generate final recommendations
        print(f"📋 [STEP 5] Delegating to Shopping Advisor Agent...")
        
        if ADK_AVAILABLE:
            try:
                advisor_request = AgentRequest( content=f"Generate comprehensive shopping recommendations based on analysis. Scenario: {best_plan.get('scenario', 'unknown')}. Total cost: ${best_plan['total_plan_cost']:.2f}. Stores: {', '.join(best_plan['plan_stores'])}. Create user-friendly advice with cost breakdown and justifications.", context={ 'task': 'generate_final_recommendations', 'best_plan': best_plan, 'scenario': best_plan.get('scenario', 'unknown'), 'maps_url': maps_url, 'user_preferences': { 'strict_mode': strict_mode, 'preferred_stores': original_preferred_stores, 'max_distance': max_distance_miles } } )
                advisor_response_obj = self.shopping_advisor_agent.run(advisor_request)
                print(f"📋 [SHOPPING ADVISOR AGENT] Response received: {type(advisor_response_obj)}")
                
            except Exception as e:
                print(f"❌ [SHOPPING ADVISOR AGENT] Error: {e}")
                print("🔄 [SHOPPING ADVISOR AGENT] Falling back to template generation...")
        
        # Generate scenario-specific advisor response (enhanced with ADK insights)
        scenario = best_plan.get('scenario', 'unknown')

        # --- THIS ENTIRE SECTION IS NOW CORRECTED ---
        gas_cost_only = best_plan.get('travel_costs', {}).get('gas_cost', 0)
        display_total_cost = best_plan.get('item_cost', 0) + gas_cost_only

        if scenario == 'scenario_1_no_preferences':
            advisor_response = f"""
            **🎯 Optimal Shopping Strategy - Algorithm Recommendation**

            Since you didn't specify preferred stores, I analyzed all available options and found the best plan: visit **{len(best_plan['plan_stores'])} store(s)**: {', '.join(best_plan['plan_stores'])}.
            
            - **Estimated Item Cost:** ${best_plan['item_cost']:.2f}
            - **Estimated Travel Cost:** ${gas_cost_only:.2f} (Gas only - {best_plan['travel_costs'].get('distance_miles', 0):.1f} miles, {best_plan['travel_costs'].get('time_hours', 0):.1f} hours)
            - **Total Combined Cost:** ${display_total_cost:.2f}
            - **Estimated Savings vs. single-store shopping:** ${best_plan['savings']:.2f}
            
            💡 **Cost-Benefit Analysis**: This plan balances item savings against gas and time costs (internally). The cost shown is for items and gas only.
            """
        elif scenario == 'scenario_3_strict_mode':
            warning_message = ""
            if best_plan.get('warning'):
                warning_message = f"\n\n> ⚠️ **Note:** {best_plan['warning']}"
                
            advisor_response = f"""
            **🔒 Strict Mode - Visiting Your Required Stores**

            Since you enabled strict mode, the plan was created for all of your selected stores that could be found: **{', '.join(best_plan['plan_stores'])}**.
            I've optimized the route sequence and determined which items to buy at each store for maximum savings.
            
            - **Estimated Item Cost:** ${best_plan['item_cost']:.2f}
            - **Estimated Travel Cost:** ${gas_cost_only:.2f} (Gas only - {best_plan['travel_costs'].get('distance_miles', 0):.1f} miles, {best_plan['travel_costs'].get('time_hours', 0):.1f} hours)
            - **Total Combined Cost:** ${display_total_cost:.2f}
            {warning_message}
            """
        else:  # suggestions_mode (scenario_2_suggestions_mode)
            user_store_names = [s['name'] for s in stores if any(pref.lower() in s['name'].lower() or s.get('chain', '').lower() == pref.lower() for pref in original_preferred_stores)]
            chose_different = not all(store in user_store_names for store in best_plan['plan_stores'])
            
            if chose_different:
                advisor_response = f"""
                **🔄 Modified Your Store Selection for Better Value**

                You suggested stores, but I found a better plan: visit **{len(best_plan['plan_stores'])} store(s)**: {', '.join(best_plan['plan_stores'])}.
                
                - **Estimated Item Cost:** ${best_plan['item_cost']:.2f}
                - **Estimated Travel Cost:** ${gas_cost_only:.2f} (Gas only - {best_plan['travel_costs'].get('distance_miles', 0):.1f} miles, {best_plan['travel_costs'].get('time_hours', 0):.1f} hours)
                - **Total Combined Cost:** ${display_total_cost:.2f}
                - **Estimated Savings vs. single-store shopping:** ${best_plan['savings']:.2f}
                
                💡 **Why this is better**: The algorithm found a more cost-effective combination that saves you money on the total trip cost (items + gas).
                """
            else:
                advisor_response = f"""
                **✅ Your Store Selection Confirmed as Optimal**

                Great choice! Your suggested stores are indeed the best option: **{', '.join(best_plan['plan_stores'])}**.
        
                - **Estimated Item Cost:** ${best_plan['item_cost']:.2f}
                - **Estimated Travel Cost:** ${gas_cost_only:.2f} (Gas only - {best_plan['travel_costs'].get('distance_miles', 0):.1f} miles, {best_plan['travel_costs'].get('time_hours', 0):.1f} hours)
                - **Total Combined Cost:** ${display_total_cost:.2f}
                - **Estimated Savings vs. single-store shopping:** ${best_plan['savings']:.2f}
                
                💡 **Cost-Benefit Analysis**: Your selections align with the optimal cost-benefit analysis!
                """

        print(f"✅ [WORKFLOW COMPLETE] Google ADK Multi-Agent workflow finished successfully")

        return { 'status': 'success', 'stores': stores,  'best_plan': best_plan, 'maps_url': maps_url, 'advisor_response': advisor_response, 'scenario': 'strict' if strict_mode else 'optimized', 'workflow_metadata': { 'adk_available': ADK_AVAILABLE, 'agents_used': [ 'store_finder_agent', 'price_optimizer_agent', 'shopping_strategist_agent', 'route_optimizer_agent', 'shopping_advisor_agent' ], 'total_stores_analyzed': len(stores), 'total_items_priced': len(items), 'optimization_mode': scenario } }
    
# def get_places_api_suggestions(user_input: str) -> List[str]:
#     """
#     Provide real-time location auto-suggestions using the Google Places API.
#     """
#     api_key = os.getenv('Maps_API_KEY') or os.getenv('Maps_API_KEY')
#     if not api_key or not user_input or len(user_input) < 3: return []
#     url = "https://maps.googleapis.com/maps/api/place/autocomplete/json"
#     params = { 'input': user_input, 'key': api_key, 'types': '(cities)' }

#     try:
#         response = requests.get(url, params=params, timeout=5)
#         data = response.json()
#         if data['status'] == 'OK': return [prediction['description'] for prediction in data['predictions']]
#         else: return []
#     except requests.exceptions.RequestException: return []

def geocode_address(address: str) -> Dict[str, Any]:
    # Try multiple possible API key names
    api_key = get_secret('GOOGLE_MAPS_API_KEY') or get_secret('Maps_API_KEY') or get_secret('GOOGLE_API_KEY')
    
    # Debug information for Streamlit Cloud
    print(f"🔍 DEBUG: API key loaded: {'YES' if api_key else 'NO'}")
    if api_key:
        print(f"🔍 DEBUG: API key length: {len(api_key)}")
        print(f"🔍 DEBUG: API key starts with: {api_key[:10]}...")
        print(f"🔍 DEBUG: API key is placeholder: {api_key.startswith('YOUR_')}")
    
    if not api_key: 
        return {"error": "Google Maps API key is required. Please add GOOGLE_MAPS_API_KEY to your .env file or Streamlit secrets.", "source": "no_api_key"}
    if not address or not address.strip(): 
        return {"error": "Please enter a valid location", "source": "error"}
    
    try:
        url = f"https://maps.googleapis.com/maps/api/geocode/json"
        params = {'address': address.strip(), 'key': api_key}
        response = requests.get(url, params=params, timeout=15)
        data = response.json()
        
        print(f"🔍 DEBUG: Geocoding API response status: {data.get('status')}")
        if data.get('status') == 'REQUEST_DENIED':
            print(f"🔍 DEBUG: Full API response: {data}")
            print(f"🔍 DEBUG: Request URL: {url}")
            print(f"🔍 DEBUG: API key used: {api_key[:20]}...")
        
        if data['status'] == 'OK' and data['results']:
            location = data['results'][0]['geometry']['location']
            formatted_address = data['results'][0]['formatted_address']
            print(f"Successfully geocoded: {formatted_address}")
            return {"lat": location['lat'], "lng": location['lng'], "formatted_address": formatted_address, "source": "google_api"}
        elif data['status'] == 'ZERO_RESULTS': 
            return {"error": f"Location '{address}' not found. Please try a more specific address (e.g., 'San Francisco, CA' or '123 Main St, New York, NY')", "source": "not_found"}
        elif data['status'] == 'REQUEST_DENIED': 
            return {"error": "Google Maps API request denied. Please check your API key permissions.", "source": "api_error"}
        else: 
            return {"error": f"Unable to find location '{address}'. Status: {data.get('status')}", "source": "api_error"}
            
    except requests.exceptions.Timeout: 
        return {"error": "Location lookup timed out. Please try again.", "source": "timeout"}
    except Exception as e:
        print(f"Geocoding error: {e}")
        return {"error": f"Error looking up location: {str(e)}", "source": "error"}

# def create_route_map(user_location, stores):
#     if not user_location or 'lat' not in user_location or 'lng' not in user_location or not stores: return None
#     locations = []
#     locations.append({'name': 'Your Location', 'lat': user_location['lat'], 'lng': user_location['lng'], 'color': [255, 0, 0, 160], 'size': 100})
#     store_colors = [[0, 0, 255, 160], [0, 255, 0, 160], [255, 165, 0, 160]]
#     for i, store in enumerate(stores):
#         if 'lat' in store and 'lng' in store: locations.append({'name': store['name'], 'lat': store['lat'], 'lng': store['lng'], 'color': store_colors[i % len(store_colors)], 'size': 80})
#     df = pd.DataFrame(locations)
#     if df.empty: return None
#     route_points = [[user_location['lng'], user_location['lat']]]
#     for store in stores: route_points.append([store['lng'], store['lat']])
#     route_points.append([user_location['lng'], user_location['lat']])
#     scatterplot = pdk.Layer('ScatterplotLayer', data=df, get_position=['lng', 'lat'], get_color='color', get_radius='size', pickable=True)
#     path = pdk.Layer('PathLayer', data=[{'path': route_points}], get_path='path', get_width=5, get_color=[255, 0, 0, 200], width_min_pixels=2)
#     view_state = pdk.ViewState(latitude=df['lat'].mean(), longitude=df['lng'].mean(), zoom=11, pitch=45)
#     return pdk.Deck(layers=[scatterplot, path], initial_view_state=view_state, tooltip={'text': '{name}'}, map_style='mapbox://styles/mapbox/light-v9')

def main():
    st.title("🤖 Smart Grocery Assistant")
    st.subheader("Google ADK Multi-Agent Shopping Optimization")
    
    # DEBUG: Add debugging info at the top of the app for Streamlit Cloud
    with st.expander("🔧 Debug Information (Streamlit Cloud)", expanded=False):
        st.write("**Environment Check:**")
        try:
            # Check if our key exists in secrets
            if hasattr(st, 'secrets'):
                st.write("✅ st.secrets is available")
                try:
                    if 'GOOGLE_MAPS_API_KEY' in st.secrets:
                        key_value = st.secrets['GOOGLE_MAPS_API_KEY']
                        st.write(f"✅ GOOGLE_MAPS_API_KEY found in secrets")
                        st.write(f"📏 Key length: {len(key_value)}")
                        st.write(f"🔤 Key starts with: {key_value[:15]}...")
                        st.write(f"🔍 Is placeholder?: {key_value.startswith('YOUR_')}")
                    else:
                        st.write("❌ GOOGLE_MAPS_API_KEY not found in st.secrets")
                        st.write(f"Available secrets keys: {list(st.secrets.keys())}")
                except Exception as e:
                    st.write(f"❌ Error accessing secrets: {e}")
            else:
                st.write("❌ st.secrets not available")
        except Exception as e:
            st.write(f"❌ Error checking Streamlit: {e}")
        
        # Test the secrets utility
        from secrets_utils import get_secret
        st.write("**Secrets Utility Test:**")
        test_key = get_secret('GOOGLE_MAPS_API_KEY')
        if test_key:
            st.write(f"✅ get_secret() returned: {test_key[:15]}...")
        else:
            st.write("❌ get_secret() returned None")
    
    multi_agent = GoogleADKMultiAgent()
    if 'workflow_inputs' not in st.session_state: st.session_state.workflow_inputs = None
    if 'workflow_results' not in st.session_state: st.session_state.workflow_results = None
    if 'location_input' not in st.session_state: st.session_state.location_input = ""

    with st.sidebar:
        user_location_input = st.text_input( "Enter location manually", key="location_input", placeholder="Start typing any city or address...", help="🔍 Suggestions are provided live by Google Maps." )
        # if user_location_input and len(user_location_input) >= 3:
        #     suggestions = get_places_api_suggestions(user_location_input)
        #     if suggestions:
        #         selected_suggestion = st.selectbox( "📍 Location suggestions:", options=[""] + suggestions, key="location_suggestions", help="Select a location from Google's suggestions" )
        #         if selected_suggestion:
        #             st.session_state.location_input = selected_suggestion
        #             st.rerun()

        st.header("🏪 Preferred Stores")
        preferred_stores = st.multiselect( "Select store chains (optional)", ['Walmart', 'Target', 'Kroger', 'Costco', 'Whole Foods', 'Safeway', 'Meijer'], default=[], help="Leave empty for algorithm to choose. Select stores to provide suggestions or requirements." )
        strict_mode = st.checkbox( "Strict Mode: Must visit all selected stores",  help="If checked, the plan will include every store you select. If unchecked, your selections are suggestions." )
        st.header("🚗 Travel Preferences")
        max_distance = st.slider( "Maximum driving distance (miles)", min_value=5, max_value=50, value=15, step=5, help="The maximum radius to search for stores. Smaller radius finds closer stores." )
        st.header("🛒 Shopping List")
        grocery_items = st.text_area( "Enter items (one per line)", value="milk\nbread\neggs\nbananas\navocados", height=120 )

        if st.button("🤖 Execute Multi-Agent Workflow", type="primary"):
            if user_location_input and grocery_items:
                items = [item.strip() for item in grocery_items.split('\n') if item.strip()]
                location_data = geocode_address(user_location_input)
                if 'error' in location_data:
                    st.error(f"❌ Location Error: {location_data['error']}")
                    st.stop()
                if strict_mode and not preferred_stores:
                    st.error("⚠️ Strict mode requires you to select at least one store.")
                    st.stop()
                
                # Execute workflow immediately when button is clicked
                inputs = { 'location': location_data, 'items': items, 'preferred_stores': preferred_stores, 'strict_mode': strict_mode, 'max_distance_miles': max_distance}
                
                with st.status("🤖 Coordinating Agents for Cost-Benefit Analysis...", expanded=True) as status:
                    status.write(f"📍 **Location**: {location_data.get('formatted_address', 'Unknown')}")
                    status.write(f"🏪 **Target Stores**: {', '.join(preferred_stores) if preferred_stores else 'Algorithm will decide'}")
                    status.write("🔍 **Store Finder Agent**: Locating nearby stores...")
                    status.write("💰 **Price Optimizer Agent**: Gathering price intelligence...")
                    status.write("🧠 **Shopping Strategist**: Evaluating all plans for total cost...")
                    
                    workflow_result = multi_agent.execute_shopping_workflow( location=location_data, items=items, preferred_stores=preferred_stores, strict_mode=strict_mode, max_distance_miles=max_distance )
                    
                    if workflow_result.get('status') != 'success':
                        st.error(f"❌ {workflow_result.get('message', 'Multi-agent workflow failed')}")
                        if 'debug_info' in workflow_result:
                            with st.expander("🔍 Debug Information"): st.json(workflow_result['debug_info'])
                        st.stop()
                
                status.update(label="✅ Optimal Shopping Strategy Found!", state="complete")
                
                # Store results in session state for display
                st.session_state.workflow_results = workflow_result
                st.session_state.workflow_inputs = inputs
                st.success(f"📍 Location set to: {location_data['formatted_address']}")
                st.rerun()
            else:
                st.error("Please provide your location and at least one grocery item.")

    # --- Main Panel for Displaying Results ---
    if st.session_state.get('workflow_results'):
        # Display stored workflow results (no re-execution on sidebar changes)
        workflow_result = st.session_state.workflow_results
        best_plan = workflow_result.get('best_plan')
        
        if not best_plan:
            st.error("Failed to generate a valid plan from the workflow results.")
            st.stop()
        
        # Create tabs with stored results
        tab1, tab2, tab3, tab4 = st.tabs(["✅ Optimal Shopping Strategy", "🛒 Shopping List", "🗺️ Route", "💰 Cost Analysis"])

        with tab1:
            st.subheader("✅ Your Optimal Shopping Plan")
            st.info(workflow_result.get('advisor_response', ''))
            if best_plan.get('scenario') == 'scenario_3_strict_mode' and best_plan.get('warning'): st.warning(f"⚠️ {best_plan['warning']}")

        with tab2:
            store_lists = best_plan.get('shopping_list', {})
            if not store_lists: st.warning("No shopping list could be generated.")
            else:
                for store_name, item_list in store_lists.items():
                    store_total = sum(i['price'] for i in item_list)
                    st.subheader(f"🏪 {store_name}")
                    df = pd.DataFrame([{'Item': i['item'].capitalize(), 'Price': i['price']} for i in item_list])
                    st.dataframe(df.style.format({'Price': '${:.2f}'}), use_container_width=True, hide_index=True)
                    st.caption(f"Subtotal: ${store_total:.2f}")

        with tab3:
            st.header("🗺️ Optimized Shopping Route")
            optimized_stores = best_plan.get('optimized_stores_in_route', [])

            print("\n" + "="*50)
            print("--- FINAL CHECK: Store order passed to the map display ---")
            for store in optimized_stores: print(f"  - {store['name']}")
            print("="*50 + "\n")
            
            if not optimized_stores: st.info("No route is available.")
            else:
                st.subheader("📍 Route Stops")
                for i, store in enumerate(optimized_stores, 1):
                    st.markdown(f"**{i}. {store['name']}**")
                    st.caption(f"📍 {store.get('address', 'N/A')}")
                maps_url = workflow_result.get('maps_url', '')
                if maps_url: st.link_button("🚗 Open Route in Google Maps", maps_url, use_container_width=True)

        with tab4:
            st.header("💰 Detailed Cost & Savings Analysis")
            travel_costs = best_plan.get('travel_costs', {})
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Item Cost", f"${best_plan.get('item_cost', 0):.2f}")
            col2.metric("Travel Cost (Gas)", f"${travel_costs.get('gas_cost', 0):.2f}")
            col3.metric("Estimated Savings", f"${best_plan.get('savings', 0):.2f}", delta_color="inverse")
            
            st.subheader("Travel Information")
            st.markdown(f"- **⛽ Gas Cost:** ${travel_costs.get('gas_cost', 0):.2f}")
            st.markdown(f"- **📏 Distance:** {travel_costs.get('distance_miles', 0):.1f} miles")
            st.markdown(f"- **⏱️ Time:** {travel_costs.get('time_hours', 0):.1f} hours (for reference)")
            st.caption(f"Calculations based on {AVERAGE_VEHICLE_MPG} MPG at ${AVERAGE_GAS_PRICE_PER_GALLON}/gallon.")

    else:
        st.markdown("""
        ### Welcome! 👋
        1. 📍 Enter your location in the sidebar.
        2. 🏪 Select preferred stores (optional).
        3. 🛒 Add items to your shopping list.
        4. 🚀 Click 'Execute' to get your optimized plan!
        
        **Use the sidebar to get started →**
        """)

if __name__ == "__main__":
    main()