# NLTK Approach


# import streamlit as st
# import nltk
# from nltk.tokenize import word_tokenize, sent_tokenize
# from nltk import pos_tag
# import re
# from datetime import datetime, timedelta
# import os

# # Set up NLTK data directory in the project folder
# NLTK_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'nltk_data')
# if not os.path.exists(NLTK_DATA_DIR):
#     os.makedirs(NLTK_DATA_DIR)
# nltk.data.path.append(NLTK_DATA_DIR)

# # Function to ensure NLTK resources are available
# @st.cache_resource
# def download_nltk_resources():
#     try:
#         # Download required NLTK data
#         nltk.download('punkt', download_dir=NLTK_DATA_DIR)
#         nltk.download('averaged_perceptron_tagger', download_dir=NLTK_DATA_DIR)
#         return True
#     except Exception as e:
#         st.error(f"Error downloading NLTK resources: {str(e)}")
#         return False

# def extract_duration(tokens):
#     nights, days = None, None
#     start_date, end_date = None, None

#     for i, token in enumerate(tokens):
#         # Case 1: Explicit "nights" and "days"
#         if token.lower() == "nights" and i > 0 and tokens[i - 1].isdigit():
#             nights = int(tokens[i - 1])
#         if token.lower() == "days" and i > 0 and tokens[i - 1].isdigit():
#             days = int(tokens[i - 1])

#         # Case 2: Terms like "a week"
#         if token.lower() == "week":
#             days = 7
#             nights = 6

#         # Case 3: Start and end dates in DD/MM/YY format
#         if re.match(r"\d{2}/\d{2}/\d{2}", token):
#             try:
#                 if start_date is None:
#                     start_date = datetime.strptime(token, "%d/%m/%y")
#                 elif end_date is None:
#                     end_date = datetime.strptime(token, "%d/%m/%y")
#             except ValueError:
#                 continue

#         # Case 4: Vague terms like "a short vacation" or "a long vacation"
#         if token.lower() in ["short", "long"] and i < len(tokens) - 1 and tokens[i + 1].lower() == "vacation":
#             return {"error": f"The term '{token} vacation' is too vague. Please specify the exact number of days."}

#     # Calculate days if start and end dates are provided
#     if start_date and end_date:
#         days = (end_date - start_date).days
#         nights = days - 1

#     # Ensure nights and days align
#     if nights is not None and days is None:
#         days = nights + 1
#     elif days is not None and nights is None:
#         nights = days - 1

#     return {
#         "nights": nights,
#         "days": days,
#         "start_date": start_date.strftime("%d/%m/%y") if start_date else None,
#         "end_date": end_date.strftime("%d/%m/%y") if end_date else None,
#     }

# def extract_budget(tokens):
#     for i, token in enumerate(tokens):
#         # Check for currency symbols and numbers
#         if token in ["$", "₹"] and i < len(tokens) - 1 and tokens[i + 1].replace(',', '').isdigit():
#             amount = int(tokens[i + 1].replace(',', ''))
#             currency = "USD" if token == "$" else "INR"
#             return {"amount": amount, "currency": currency}
        
#         # Check for currency words
#         if token.lower() in ["dollars", "rupees"] and i > 0 and tokens[i - 1].replace(',', '').isdigit():
#             amount = int(tokens[i - 1].replace(',', ''))
#             currency = "USD" if token.lower() == "dollars" else "INR"
#             return {"amount": amount, "currency": currency}
    
#     return None

# def extract_info(user_input):
#     try:
#         # Tokenize and tag parts of speech
#         tokens = word_tokenize(user_input)
#         tags = pos_tag(tokens)

#         # Extract destination
#         destination = None
#         travel_indicators = ["to", "in", "at"]
#         for indicator in travel_indicators:
#             if indicator in tokens:
#                 to_index = tokens.index(indicator)
#                 if to_index + 1 < len(tokens):
#                     destination_tokens = []
#                     for i in range(to_index + 1, len(tokens)):
#                         if tokens[i].lower() in ["for", "with", "and", "on"]:
#                             break
#                         destination_tokens.append(tokens[i])
#                     destination = " ".join(destination_tokens)
#                     break

#         # Extract budget
#         budget_info = extract_budget(tokens)

#         # Extract duration
#         duration_info = extract_duration(tokens)
#         if "error" in duration_info:
#             return {"error": duration_info["error"]}

#         # Extract interests
#         interests = []
#         interest_keywords = [
#             "romantic", "adventure", "relaxation", "nature", "shopping", 
#             "history", "food", "party", "crazy", "peaceful", "beach", "wildlife", 
#             "mountains", "culture", "luxury", "budget", "sports", "festivals", 
#             "photography", "hiking", "wellness", "spa", "family", "friends", 
#             "couples", "solo", "nightlife", "exploration", "art", "music", 
#             "technology", "science", "heritage", "island", "cityscape"
#         ]

#         for word in tokens:
#             if word.lower() in interest_keywords:
#                 interests.append(word.capitalize())

#         return {
#             "destination": destination.strip() if destination else None,
#             "budget": budget_info,
#             "duration": duration_info,
#             "interests": interests,
#         }
#     except Exception as e:
#         return {"error": f"Error processing input: {str(e)}"}

# def main():
#     st.title("Travel Itinerary Generator and Assistant")
    
#     # Ensure NLTK resources are downloaded before processing
#     if not download_nltk_resources():
#         st.error("Failed to initialize required resources. Please try again.")
#         return

#     st.write("Welcome! Describe your travel plans in one sentence, and I'll generate a personalized itinerary.")

#     # Input prompt
#     user_input = st.text_area(
#         "Enter your travel plans:", 
#         placeholder="e.g., I want to travel to the Maldives with my wife for a romantic vacation with a budget of $10,000 for 3 nights and 4 days."
#     )

#     # Submit button
#     if st.button("Generate Itinerary"):
#         if user_input:
#             travel_info = extract_info(user_input)
            
#             if "error" in travel_info:
#                 st.warning(travel_info["error"])
#             elif not travel_info["destination"]:
#                 st.warning("Could not extract destination. Please include it in your prompt.")
#             elif not travel_info["budget"]:
#                 st.warning("Could not extract budget. Please include it in your prompt.")
#             elif not travel_info["duration"]["days"]:
#                 st.warning("Could not extract duration. Please include it in your prompt.")
#             else:
#                 st.success("Information extracted successfully!")
#                 st.write("**Extracted Information**:")
#                 st.write(f"**Destination**: {travel_info['destination']}")
#                 st.write(f"**Budget**: {travel_info['budget']['currency']} {travel_info['budget']['amount']:,}")
#                 st.write(f"**Duration**: {travel_info['duration']['nights']} nights and {travel_info['duration']['days']} days")
#                 if travel_info['duration']['start_date']:
#                     st.write(f"**Dates**: {travel_info['duration']['start_date']} to {travel_info['duration']['end_date']}")
#                 st.write(f"**Interests**: {', '.join(travel_info['interests']) if travel_info['interests'] else 'Not specified'}")
#                 st.write("Your personalized itinerary will be generated here...")
#         else:
#             st.warning("Please enter your travel plans in the text area.")

# if __name__ == "__main__":
#     main()





# Normal Regex Approach


# import streamlit as st
# import re
# from datetime import datetime, timedelta

# def extract_destination(text):
#     # Common patterns for destination extraction
#     patterns = [
#         r"(?:travel|go|flying|heading|visiting|trip) (?:to|in) ([A-Za-z\s,]+?)(?=\s*(?:for|with|on|and|$))",
#         r"(?:visiting|explore) ([A-Za-z\s,]+?)(?=\s*(?:for|with|on|and|$))",
#         r"(?:vacation|holiday) (?:in|at) ([A-Za-z\s,]+?)(?=\s*(?:for|with|on|and|$))"
#     ]
    
#     for pattern in patterns:
#         match = re.search(pattern, text.lower())
#         if match:
#             return match.group(1).strip().title()
#     return None

# def extract_duration(text):
#     nights, days = None, None
    
#     # Extract nights
#     night_match = re.search(r'(\d+)\s*nights?', text.lower())
#     if night_match:
#         nights = int(night_match.group(1))
#         days = nights + 1
    
#     # Extract days
#     day_match = re.search(r'(\d+)\s*days?', text.lower())
#     if day_match:
#         days = int(day_match.group(1))
#         if nights is None:
#             nights = days - 1
    
#     # Extract date range (DD/MM/YY or DD-MM-YY)
#     dates = re.findall(r'(\d{2}[-/]\d{2}[-/]\d{2})', text)
#     start_date = end_date = None
    
#     if len(dates) >= 2:
#         try:
#             start_date = datetime.strptime(dates[0].replace('-', '/'), "%d/%m/%y")
#             end_date = datetime.strptime(dates[1].replace('-', '/'), "%d/%m/%y")
#             days = (end_date - start_date).days
#             nights = days - 1
#         except ValueError:
#             pass
    
#     # Handle week
#     if 'week' in text.lower():
#         days = 7
#         nights = 6
    
#     return {
#         "nights": nights,
#         "days": days,
#         "start_date": start_date.strftime("%d/%m/%y") if start_date else None,
#         "end_date": end_date.strftime("%d/%m/%y") if end_date else None
#     }

# def extract_budget(text):
#     # Handle currency symbols
#     budget_patterns = [
#         r'(?:budget of |cost of |spend |price |cost )?[\$₹](\d+[,\d]*)',
#         r'(\d+[,\d]*)\s*(?:dollars|rupees)',
#     ]
    
#     for pattern in budget_patterns:
#         match = re.search(pattern, text.lower())
#         if match:
#             amount = int(match.group(1).replace(',', ''))
#             # Determine currency
#             if '$' in text or 'dollars' in text.lower():
#                 currency = "USD"
#             elif '₹' in text or 'rupees' in text.lower():
#                 currency = "INR"
#             else:
#                 currency = "USD"  # Default currency
#             return {"amount": amount, "currency": currency}
#     return None

# def extract_interests(text):
#     interest_keywords = {
#         'romantic': ['romantic', 'honeymoon', 'couple'],
#         'adventure': ['adventure', 'exciting', 'thrill', 'trek', 'fun'],
#         'nature': ['nature', 'wildlife', 'outdoor', 'forest', 'mountain', 'beach'],
#         'culture': ['culture', 'history', 'museum', 'heritage', 'art'],
#         'food': ['food', 'cuisine', 'dining', 'gastronomy', 'culinary'],
#         'relaxation': ['relaxation', 'peaceful', 'quiet', 'spa', 'wellness'],
#         'shopping': ['shopping', 'market', 'mall'],
#         'nightlife': ['party', 'club', 'nightlife', 'bar'],
#         'family': ['family', 'kids', 'children'],
#         'luxury': ['luxury', 'premium', 'high-end', 'exclusive']
#     }
    
#     found_interests = set()
#     text_lower = text.lower()
    
#     for category, keywords in interest_keywords.items():
#         if any(keyword in text_lower for keyword in keywords):
#             found_interests.add(category.title())
    
#     return list(found_interests)

# def parse_travel_input(text):
#     if not text:
#         return {"error": "Please enter your travel plans."}
    
#     try:
#         destination = extract_destination(text)
#         budget = extract_budget(text)
#         duration = extract_duration(text)
#         interests = extract_interests(text)
        
#         return {
#             "destination": destination,
#             "budget": budget,
#             "duration": duration,
#             "interests": interests
#         }
#     except Exception as e:
#         return {"error": f"Error processing input: {str(e)}"}

# def main():
#     st.title("Travel Itinerary Generator and Assistant")
#     st.write("Welcome! Describe your travel plans in one sentence, and I'll generate a personalized itinerary.")

#     user_input = st.text_area(
#         "Enter your travel plans:",
#         placeholder="e.g., I want to travel to the Maldives with my wife for a romantic vacation with a budget of $10,000 for 3 nights and 4 days."
#     )

#     if st.button("Generate Itinerary"):
#         if user_input:
#             travel_info = parse_travel_input(user_input)
            
#             if "error" in travel_info:
#                 st.warning(travel_info["error"])
#             elif not travel_info["destination"]:
#                 st.warning("Could not extract destination. Please include it in your prompt.")
#             elif not travel_info["budget"]:
#                 st.warning("Could not extract budget. Please include it in your prompt.")
#             elif not travel_info["duration"]["days"]:
#                 st.warning("Could not extract duration. Please include it in your prompt.")
#             else:
#                 st.success("Information extracted successfully!")
#                 st.write("**Extracted Information**:")
#                 st.write(f"**Destination**: {travel_info['destination']}")
#                 st.write(f"**Budget**: {travel_info['budget']['currency']} {travel_info['budget']['amount']:,}")
#                 st.write(f"**Duration**: {travel_info['duration']['nights']} nights and {travel_info['duration']['days']} days")
#                 if travel_info['duration']['start_date']:
#                     st.write(f"**Dates**: {travel_info['duration']['start_date']} to {travel_info['duration']['end_date']}")
#                 st.write(f"**Interests**: {', '.join(travel_info['interests']) if travel_info['interests'] else 'Not specified'}")
#                 st.write("Your personalized itinerary will be generated here...")
#         else:
#             st.warning("Please enter your travel plans.")

# if __name__ == "__main__":
#     main()





# Good Code but after this adding Attractions, restaurants and Geos

# import streamlit as st
# import requests
# import re
# from datetime import datetime, timedelta
# import pandas as pd
# from math import radians, sin, cos, sqrt, atan2
# from streamlit_folium import st_folium
# import folium
# from polyline import decode  # Install via `pip install polyline`

# def extract_destination(text):
#     # Common patterns for destination extraction
#     patterns = [
#         r"(?:travel|go|flying|heading|visiting|trip) (?:to|in) ([A-Za-z\s,]+?)(?=\s*(?:for|with|on|and|$))",
#         r"(?:visiting|explore) ([A-Za-z\s,]+?)(?=\s*(?:for|with|on|and|$))",
#         r"(?:vacation|holiday) (?:in|at) ([A-Za-z\s,]+?)(?=\s*(?:for|with|on|and|$))"
#     ]
    
#     for pattern in patterns:
#         match = re.search(pattern, text.lower())
#         if match:
#             return match.group(1).strip().title()
#     return None

# def extract_duration(text):
#     nights, days = None, None
    
#     # Extract nights
#     night_match = re.search(r'(\d+)\s*nights?', text.lower())
#     if night_match:
#         nights = int(night_match.group(1))
#         days = nights + 1
    
#     # Extract days
#     day_match = re.search(r'(\d+)\s*days?', text.lower())
#     if day_match:
#         days = int(day_match.group(1))
#         if nights is None:
#             nights = days - 1
    
#     # Extract date range (DD/MM/YY or DD-MM-YY)
#     dates = re.findall(r'(\d{2}[-/]\d{2}[-/]\d{2})', text)
#     start_date = end_date = None
    
#     if len(dates) >= 2:
#         try:
#             start_date = datetime.strptime(dates[0].replace('-', '/'), "%d/%m/%y")
#             end_date = datetime.strptime(dates[1].replace('-', '/'), "%d/%m/%y")
#             days = (end_date - start_date).days
#             nights = days - 1
#         except ValueError:
#             pass
    
#     # Handle week
#     if 'week' in text.lower():
#         days = 7
#         nights = 6
    
#     return {
#         "nights": nights,
#         "days": days,
#         "start_date": start_date.strftime("%d/%m/%y") if start_date else None,
#         "end_date": end_date.strftime("%d/%m/%y") if end_date else None
#     }

# def extract_budget(text):
#     # Handle currency symbols
#     budget_patterns = [
#         r'(?:budget of |cost of |spend |price |cost )?[\$₹](\d+[,\d]*)',
#         r'(\d+[,\d]*)\s*(?:dollars|rupees)',
#     ]
    
#     for pattern in budget_patterns:
#         match = re.search(pattern, text.lower())
#         if match:
#             amount = int(match.group(1).replace(',', ''))
#             # Determine currency
#             if '$' in text or 'dollars' in text.lower():
#                 currency = "USD"
#             elif '₹' in text or 'rupees' in text.lower():
#                 currency = "INR"
#             else:
#                 currency = "USD"  # Default currency
#             return {"amount": amount, "currency": currency}
#     return None

# def extract_interests(text):
#     interest_keywords = {
#         'romantic': ['romantic', 'honeymoon', 'couple'],
#         'adventure': ['adventure', 'exciting', 'thrill', 'trek', 'fun'],
#         'nature': ['nature', 'wildlife', 'outdoor', 'forest', 'mountain', 'beach'],
#         'culture': ['culture', 'history', 'museum', 'heritage', 'art'],
#         'food': ['food', 'cuisine', 'dining', 'gastronomy', 'culinary'],
#         'relaxation': ['relaxation', 'peaceful', 'quiet', 'spa', 'wellness'],
#         'shopping': ['shopping', 'market', 'mall'],
#         'nightlife': ['party', 'club', 'nightlife', 'bar'],
#         'family': ['family', 'kids', 'children'],
#         'luxury': ['luxury', 'premium', 'high-end', 'exclusive']
#     }
    
#     found_interests = set()
#     text_lower = text.lower()
    
#     for category, keywords in interest_keywords.items():
#         if any(keyword in text_lower for keyword in keywords):
#             found_interests.add(category.title())
    
#     return list(found_interests)

# def get_hotel_photos(location_id, api_key):
#     """Fetch hotel photos from TripAdvisor API."""
#     url = f"https://api.content.tripadvisor.com/api/v1/location/{location_id}/photos"
#     params = {
#         "key": api_key,
#         "language": "en"
#     }
#     headers = {"accept": "application/json"}
    
#     try:
#         response = requests.get(url, params=params, headers=headers)
#         response.raise_for_status()
#         photos_data = response.json()
        
#         # Extract photo URLs from the response
#         photos = []
#         for photo in photos_data.get("data", [])[:3]:  # Limit to first 3 photos
#             if photo.get("images", {}).get("large", {}).get("url"):
#                 photos.append(photo["images"]["large"]["url"])
#         return photos
#     except requests.exceptions.RequestException as e:
#         st.error(f"Error fetching photos: {str(e)}")
#         return []

# def get_hotel_reviews(location_id, api_key):
#     """Fetch hotel reviews from TripAdvisor API."""
#     url = f"https://api.content.tripadvisor.com/api/v1/location/{location_id}/reviews"
#     params = {
#         "key": api_key,
#         "language": "en"
#     }
#     headers = {"accept": "application/json"}
    
#     try:
#         response = requests.get(url, params=params, headers=headers)
#         response.raise_for_status()
#         reviews_data = response.json()
        
#         # Extract relevant review information
#         reviews = []
#         for review in reviews_data.get("data", [])[:3]:  # Limit to first 3 reviews
#             review_info = {
#                 "title": review.get("title", "No Title"),
#                 "text": review.get("text", "No Review Text"),
#                 "rating": review.get("rating", "N/A"),
#                 "published_date": review.get("published_date", "N/A"),
#                 "username": review.get("user", {}).get("username", "Anonymous")
#             }
#             reviews.append(review_info)
#         return reviews
#     except requests.exceptions.RequestException as e:
#         st.error(f"Error fetching reviews: {str(e)}")
#         return []

# def get_weather_forecast(latitude, longitude, api_key):
#     """Fetch weather forecast from OpenWeatherMap API."""
#     url = f"http://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
    
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             forecast_data = response.json()
#             # Get the next 5 days forecast (data points every 3 hours, so we'll take one per day)
#             daily_forecasts = []
#             seen_dates = set()
            
#             for item in forecast_data['list']:
#                 date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
#                 if date not in seen_dates:
#                     seen_dates.add(date)
#                     daily_forecasts.append({
#                         'date': datetime.fromtimestamp(item['dt']).strftime('%d %b'),
#                         'temp': round(item['main']['temp']),
#                         'description': item['weather'][0]['description'],
#                         'icon': item['weather'][0]['icon']
#                     })
#                 if len(daily_forecasts) >= 5:
#                     break
            
#             return daily_forecasts
#     except Exception as e:
#         st.error(f"Error fetching weather data: {str(e)}")
#     return None

# # New functions for user location
# def get_user_ip():
#     """Get user's IP address."""
#     try:
#         response = requests.get("https://api.ipify.org?format=json")
#         if response.status_code == 200:
#             return response.json()['ip']
#         return None
#     except Exception as e:
#         print(f"Error getting IP: {e}")
#         return None

# def get_user_location(ip_address):
#     """Get location information from IP address."""
#     try:
#         url = f"http://ip-api.com/json/{ip_address}"
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             if data['status'] == 'success':
#                 return {
#                     "city": data.get('city'),
#                     "region": data.get('regionName'),
#                     "country": data.get('country'),
#                     "latitude": data.get('lat'),
#                     "longitude": data.get('lon')
#                 }
#         return None
#     except Exception as e:
#         print(f"Error getting location: {e}")
#         return None
    
# def calculate_distance(lat1, lon1, lat2, lon2):
#     """Calculate distance between two points using Haversine formula."""
#     try:
#         # Convert string inputs to float if necessary
#         lat1 = float(lat1)
#         lon1 = float(lon1)
#         lat2 = float(lat2)
#         lon2 = float(lon2)
        
#         R = 6371  # Earth's radius in kilometers

#         lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
#         dlat = lat2 - lat1
#         dlon = lon2 - lon1

#         a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
#         c = 2 * atan2(sqrt(a), sqrt(1-a))
#         distance = R * c

#         return distance
#     except (ValueError, TypeError) as e:
#         print(f"Error calculating distance: {e}")
#         return float('inf')  # Return infinity for invalid coordinates

# def find_multiple_nearest_airports(latitude, longitude, airports_df, max_airports=5, max_distance=300):
#     """Find multiple nearest airports within a reasonable distance."""
#     try:
#         # Convert coordinates to float
#         latitude = float(latitude)
#         longitude = float(longitude)
        
#         # Ensure lat and lon columns are float type
#         airports_df['lat'] = pd.to_numeric(airports_df['lat'], errors='coerce')
#         airports_df['lon'] = pd.to_numeric(airports_df['lon'], errors='coerce')
        
#         # Drop rows with invalid coordinates
#         airports_df = airports_df.dropna(subset=['lat', 'lon', 'iata'])
        
#         # Calculate distances for all airports
#         airports_df['distance'] = airports_df.apply(
#             lambda row: calculate_distance(
#                 latitude, longitude,
#                 row['lat'], row['lon']
#             ),
#             axis=1
#         )
        
#         # Get nearest airports within maximum distance
#         nearest_airports = airports_df[airports_df['distance'] <= max_distance].nsmallest(max_airports, 'distance')
        
#         if nearest_airports.empty:
#             print(f"No airports found within {max_distance} km")
#             return []
            
#         airports_list = []
#         for _, airport in nearest_airports.iterrows():
#             airports_list.append({
#                 'name': airport['name'],
#                 'iata': airport['iata'],
#                 'distance': airport['distance'],
#                 'lat': airport['lat'],
#                 'lon': airport['lon']
#             })
            
#         return airports_list
#     except Exception as e:
#         print(f"Error finding nearest airports: {e}")
#         return []

# def find_nearest_airport(latitude, longitude, airports_df):
#     """Find the single nearest airport to given coordinates."""
#     try:
#         airports = find_multiple_nearest_airports(latitude, longitude, airports_df, max_airports=1)
#         return airports[0] if airports else None
#     except Exception as e:
#         print(f"Error finding nearest airport: {e}")
#         return None
    
# def get_flight_options_with_fallback(destination_lat, destination_lon, airports_df, departure_airport_iata):
#     """Get flight options using SearchAPI with fallback to alternative airports."""
#     print("\nStarting enhanced flight search process...")
#     print(f"Input coordinates: lat={destination_lat}, lon={destination_lon}")
    
#     # Get multiple nearest airports
#     nearest_airports = find_multiple_nearest_airports(destination_lat, destination_lon, airports_df)
    
#     if not nearest_airports:
#         st.warning("No airports found within reasonable distance.")
#         return None
        
#     for airport in nearest_airports:
#         print(f"\nTrying airport: {airport['name']} ({airport['iata']}) - {airport['distance']:.2f} km away")
        
#         url = "https://www.searchapi.io/api/v1/search"
#         params = {
#             "engine": "google_flights",
#             "flight_type": "one_way",
#             "departure_id": departure_airport_iata,  # Use detected departure airport
#             "arrival_id": airport['iata'],
#             "outbound_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
#             "api_key": "UdxjESojjvM58CeEVvxTwr2S"
#         }
        
#         try:
#             response = requests.get(url, params=params)
#             response.raise_for_status()
#             flights_data = response.json()
            
#             if flights_data and 'best_flights' in flights_data and flights_data['best_flights']:
#                 print(f"Found flights for {airport['iata']}")
#                 flights_data['airport_info'] = {
#                     'name': airport['name'],
#                     'iata': airport['iata'],
#                     'distance': airport['distance']
#                 }
#                 return flights_data
#             else:
#                 print(f"No flights found for {airport['iata']}")
                
#         except requests.exceptions.RequestException as e:
#             print(f"Error in API request for {airport['iata']}: {str(e)}")
#             continue
    
#     st.warning("No flights found from any nearby airports.")
#     return None


# def get_directions(api_key, origin_city, destination_city, mode='driving'):
#     """Get directions from Google Maps API using city names."""
#     url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin_city}&destination={destination_city}&mode={mode}&key={api_key}"
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         st.error(f"Error fetching directions: {str(e)}")
#         return None

# def plot_route_on_map(directions_data, mode):
#     """Create a Folium map with the route plotted."""
#     if not directions_data or 'routes' not in directions_data or not directions_data['routes']:
#         return None

#     try:
#         # Extract route points from directions
#         route = directions_data['routes'][0]['overview_polyline']['points']
#         coordinates = decode(route)
        
#         # Create a map centered on the origin with reduced zoom
#         start_location = coordinates[0]
#         m = folium.Map(
#             location=start_location, 
#             zoom_start=8,  # Reduced zoom level
#             prefer_canvas=True  # Use canvas renderer for better performance
#         )
        
#         # Add route as a polyline with simplified styling
#         color = "blue" if mode == "driving" else "green"
#         folium.PolyLine(
#             coordinates, 
#             color=color, 
#             weight=3,  # Reduced line weight
#             opacity=0.6  # Reduced opacity
#         ).add_to(m)
        
#         # Add simplified markers
#         folium.Marker(
#             coordinates[0], 
#             tooltip="Airport",
#             icon=folium.Icon(color="green", icon="plane", prefix='fa', size=(20, 20))
#         ).add_to(m)
        
#         folium.Marker(
#             coordinates[-1], 
#             tooltip="Hotel",
#             icon=folium.Icon(color="red", icon="hotel", prefix='fa', size=(20, 20))
#         ).add_to(m)
        
#         # Fit bounds to show the entire route
#         m.fit_bounds([coordinates[0], coordinates[-1]])
        
#         return m
#     except Exception as e:
#         st.error(f"Error creating map: {str(e)}")
#         return None

# def display_flight_options(flights_data):
#     """Display flight options using Streamlit components with airline logos and INR prices."""
#     if not flights_data or 'best_flights' not in flights_data:
#         st.warning("No flight information available.")
#         return
    
#     st.divider()
#     st.subheader("Available Flights")
    
#     # Display airport information if available
#     if 'airport_info' in flights_data:
#         airport_info = flights_data['airport_info']
#         st.info(f"Showing flights to {airport_info['name']} ({airport_info['iata']}) - {airport_info['distance']:.1f} km from destination")
    
#     # USD to INR conversion rate
#     USD_TO_INR = 84.5
    
#     for best_flight in flights_data['best_flights'][:2]:  # Display top flight option
#         total_duration = best_flight.get('total_duration', 'N/A')
#         price_usd = best_flight.get('price', 0)
#         price_inr = price_usd * USD_TO_INR
        
#         # Create expander header with price in both currencies
#         expander_header = f"₹{price_inr:,.2f} (${price_usd}) - ⏱️ {total_duration} mins"
        
#         with st.expander(expander_header):
#             # Display each flight segment in the itinerary
#             for i, flight in enumerate(best_flight['flights'], 1):
#                 # Create columns for airline info and flight details
#                 col1, col2 = st.columns([1, 3])
                
#                 with col1:
#                     # Display airline logo if available
#                     if 'airline_logo' in flight:
#                         st.image(flight['airline_logo'], width=70)
#                     st.write(f"**{flight.get('airline', 'N/A')}**")
#                     st.write(f"Flight {flight.get('flight_number', 'N/A')}")
                
#                 with col2:
#                     # Create sub-columns for departure and arrival
#                     dep_col, arr_col = st.columns(2)
                    
#                     with dep_col:
#                         st.write("**Departure:**")
#                         dep = flight['departure_airport']
#                         st.write(f"🛫 {dep['name']} ({dep['id']})")
#                         st.write(f"📅 {dep['date']}")
#                         st.write(f"🕒 {dep['time']}")
                    
#                     with arr_col:
#                         st.write("**Arrival:**")
#                         arr = flight['arrival_airport']
#                         st.write(f"🛬 {arr['name']} ({arr['id']})")
#                         st.write(f"📅 {arr['date']}")
#                         st.write(f"🕒 {arr['time']}")
                
#                 # Flight details section
#                 st.write("**Flight Details:**")
#                 st.write(f"✈️ Aircraft: {flight.get('airplane', 'N/A')}")
#                 st.write(f"⏱️ Duration: {flight.get('duration', 'N/A')} mins")
                
#                 # Display any additional flight information from extensions
#                 if 'detected_extensions' in flight:
#                     ext = flight['detected_extensions']
#                     if 'seat_type' in ext:
#                         st.write(f"💺 Seat: {ext['seat_type']}")
#                     if 'legroom_long' in ext:
#                         st.write(f"🦵 Legroom: {ext['legroom_long']}")
#                     if 'carbon_emission' in ext:
#                         st.write(f"🌱 Carbon emission: {ext['carbon_emission']} kg")
                
#                 # Display layover information
#                 if i < len(best_flight['flights']) and 'layovers' in best_flight:
#                     layover = best_flight['layovers'][i-1]
#                     st.markdown("---")
#                     st.write(f"🕒 **Layover:** {layover.get('duration', 'N/A')} mins at {layover.get('name', 'N/A')}")
#                     st.markdown("---")

# def display_route_information(flights_data, hotels):
#     """Display route information from airport to hotel."""
#     if not hotels or len(hotels) == 0 or not flights_data:
#         return
        
#     google_maps_api_key = "AIzaSyA5QKrsVtwQa30vzOgZwo_p1ak5tyzgyE0"
    
#     st.divider()
#     st.subheader("🗺️ Ground Transportation to Destination")
    
#     # Get arrival city and destination city
#     arrival_city = flights_data['airports'][0]['arrival'][0]['city']
#     destination_city = hotels[0].get('address_obj', {}).get('city', '')
    
#     if arrival_city and destination_city:
#         # Display route information for both driving and transit
#         modes = ['driving', 'transit']
#         mode_icons = {'driving': '🚗', 'transit': '🚌'}
        
#         cols = st.columns(2)
#         for idx, mode in enumerate(modes):
#             with cols[idx]:
#                 st.write(f"**{mode_icons[mode]} {mode.title()} Option:**")
                
#                 directions_data = get_directions(google_maps_api_key, arrival_city, destination_city, mode)
                
#                 if directions_data and 'routes' in directions_data and directions_data['routes']:
#                     leg = directions_data['routes'][0]['legs'][0]
#                     st.write(f"📏 Distance: {leg['distance']['text']}")
#                     st.write(f"⏱️ Duration: {leg['duration']['text']}")
                    
#                     route_map = plot_route_on_map(directions_data, mode)
#                     if route_map:
#                         st_folium(
#                             route_map, 
#                             width=400,
#                             height=300,
#                             returned_objects=[],
#                             use_container_width=False
#                         )
#                 else:
#                     st.warning(f"No {mode} route available")
#     else:
#         st.warning("Could not determine city information for route mapping")

# def display_weather_forecast(forecasts):
#     """Display weather forecast using Streamlit components."""
#     if not forecasts:
#         return
    
#     st.divider()
#     st.subheader("5-Day Weather Forecast At the Destination")
#     cols = st.columns(len(forecasts))
    
#     for idx, forecast in enumerate(forecasts):
#         with cols[idx]:
#             st.write(f"**{forecast['date']}**")
#             icon_url = f"http://openweathermap.org/img/wn/{forecast['icon']}@2x.png"
#             st.image(icon_url, width=50)
#             st.write(f"{forecast['temp']}°C")
#             st.write(f"*{forecast['description'].capitalize()}*")

# def get_hotels_from_tripadvisor(destination):
#     """Fetch hotels from TripAdvisor API for a given destination."""
#     base_url = "https://api.content.tripadvisor.com/api/v1"
#     tripadvisor_api_key = "C5104F92E6354A079E0C6E424B3B1F06"
#     weather_api_key = "a73d2e9d5872429030175d780367cf35"
    
#     try:
#         # First, search for hotels in the destination
#         search_url = f"{base_url}/location/search"
#         search_params = {
#             "key": tripadvisor_api_key,
#             "searchQuery": destination,
#             "category": "hotels",
#             "language": "en"
#         }
        
#         # Make the initial search request
#         search_response = requests.get(
#             search_url, 
#             params=search_params, 
#             headers={"accept": "application/json"}
#         )
#         search_response.raise_for_status()
#         search_data = search_response.json()
        
#         # Extract location IDs from search results
#         location_ids = [
#             item.get("location_id") 
#             for item in search_data.get("data", [])
#         ]
        
#         hotels_details = []
#         weather_forecast = None
        
#         # Fetch details for each hotel (limited to first 5)
#         for location_id in location_ids[:5]:
#             details_url = f"{base_url}/location/{location_id}/details"
#             details_params = {
#                 "key": tripadvisor_api_key,
#                 "language": "en",
#                 "currency": "USD"
#             }
            
#             # Get detailed hotel information
#             details_response = requests.get(
#                 details_url, 
#                 params=details_params, 
#                 headers={"accept": "application/json"}
#             )
#             details_response.raise_for_status()
#             hotel_data = details_response.json()
            
#             # Extract coordinates
#             latitude = hotel_data.get("latitude")
#             longitude = hotel_data.get("longitude")
            
#             # Fetch weather data for the first hotel only
#             if len(hotels_details) == 0 and latitude and longitude:
#                 weather_forecast = get_weather_forecast(latitude, longitude, weather_api_key)
            
#             # Fetch photos and reviews
#             photos = get_hotel_photos(location_id, tripadvisor_api_key)
#             reviews = get_hotel_reviews(location_id, tripadvisor_api_key)
            
#             # Compile hotel information
#             hotel_info = {
#                 "name": hotel_data.get("name", "N/A"),
#                 "description": hotel_data.get("description", "No description available"),
#                 "web_url": hotel_data.get("web_url", "N/A"),
#                 "phone": hotel_data.get("phone", "N/A"),
#                 "price_level": hotel_data.get("price_level", "N/A"),
#                 "amenities": hotel_data.get("amenities", [])[:6],  # First 6 amenities
#                 "photos": photos,
#                 "reviews": reviews,
#                 "latitude": latitude,
#                 "longitude": longitude,
#                 "address_obj": hotel_data.get("address_obj", {})  # Include the complete address object
#             }
            
#             hotels_details.append(hotel_info)
        
#         # Return both hotels and weather data
#         return hotels_details, weather_forecast if len(hotels_details) > 0 else ([], None)
    
#     except requests.exceptions.RequestException as e:
#         st.error(f"Error fetching hotel data: {str(e)}")
#         return [], None

# def display_hotel_information(hotels):
#     """Display hotel information in a structured format using Streamlit components."""
#     st.subheader("Available Hotels")
    
#     for i, hotel in enumerate(hotels, 1):
#         price_desc = get_price_level_description(hotel['price_level'])
#         with st.expander(f"{i}. {hotel['name']}"):
#             # Display hotel photos in a horizontal arrangement
#             if hotel['photos']:
#                 cols = st.columns(min(len(hotel['photos']), 3))
#                 for idx, photo_url in enumerate(hotel['photos']):
#                     cols[idx].image(photo_url, use_container_width=True)
            
#             st.write("**Description:**")
#             st.write(hotel['description'])
            
#             st.divider()
            
#             st.write("**Price Level:**")
#             st.write(f"{hotel['price_level']}: {price_desc}")
            
#             st.divider()
            
#             st.write("**Contact Information:**")
#             st.write(f"🌐 [Visit Website]({hotel['web_url']})")
#             if hotel['phone'] != "N/A":
#                 st.write(f"📞 {hotel['phone']}")
            
#             if hotel['amenities']:
#                 st.divider()
#                 st.write("**Top Amenities:**")
#                 # Create two columns
#                 col1, col2 = st.columns(2)
                
#                 # Split the amenities list into two parts
#                 mid_point = len(hotel['amenities']) // 2
#                 amenities_col1 = hotel['amenities'][:mid_point]
#                 amenities_col2 = hotel['amenities'][mid_point:]
                
#                 # Display the amenities in the respective columns
#                 with col1:
#                     for amenity in amenities_col1:
#                         st.write(f"✓ {amenity}")
#                 with col2:
#                     for amenity in amenities_col2:
#                         st.write(f"✓ {amenity}")

            
#             if hotel['reviews']:
#                 st.divider()
                
#                 st.write("**Recent Reviews:**")
#                 for review in hotel['reviews']:
#                     # Using consistent formatting for all reviews
#                     st.write(f"⭐ **{review['rating']}/5**")
#                     st.write(f"*\"{review['title']}\"*")
#                     st.write(review['text'])
#                     st.write(f"— {review['username']} ({review['published_date']})")
#                     # st.write("---")

# def get_price_level_description(price_level):
#     """Convert price level symbols to descriptive text."""
#     price_descriptions = {
#         "$$$$": "Very Costly",
#         "$$$": "Costly",
#         "$$": "Affordable",
#         "$": "Great Bargain!!"
#     }
#     return price_descriptions.get(price_level, price_level)

# def parse_travel_input(text):
#     if not text:
#         return {"error": "Please enter your travel plans."}
    
#     try:
#         destination = extract_destination(text)
#         budget = extract_budget(text)
#         duration = extract_duration(text)
#         interests = extract_interests(text)
        
#         return {
#             "destination": destination,
#             "budget": budget,
#             "duration": duration,
#             "interests": interests
#         }
#     except Exception as e:
#         return {"error": f"Error processing input: {str(e)}"}

# def main():
#     st.title("Travel Itinerary Generator and Assistant")
    
#     # Load airports data
#     try:
#         airports_df = pd.read_csv('airports.csv')
#         airports_df['lat'] = pd.to_numeric(airports_df['lat'], errors='coerce')
#         airports_df['lon'] = pd.to_numeric(airports_df['lon'], errors='coerce')
#         airports_df = airports_df.dropna(subset=['lat', 'lon', 'iata'])
#     except Exception as e:
#         st.error(f"Error loading airports data: {e}")
#         return

#     # Get user's location and nearest airport
#     departure_airport_iata = "BOM"  # Default to Mumbai
#     user_ip = get_user_ip()
#     if user_ip:
#         location = get_user_location(user_ip)
#         if location:
#             st.write(f"📍 Detected your location: {location['city']}, {location['region']}, {location['country']}")
            
#             nearest_airport = find_nearest_airport(location['latitude'], location['longitude'], airports_df)
#             if nearest_airport:
#                 departure_airport_iata = nearest_airport['iata']
#                 st.write(f"✈️ Nearest Airport: {nearest_airport['name']} ({departure_airport_iata})")
#             else:
#                 st.info("Using Mumbai (BOM) as default departure airport.")
#         else:
#             st.info("Unable to determine your location. Using Mumbai (BOM) as default departure airport.")
#     else:
#         st.info("Unable to retrieve your IP address. Using Mumbai (BOM) as default departure airport.")

#     st.write("Describe your travel plans in one sentence, and I'll generate a personalized itinerary.")

#     user_input = st.text_area(
#         "Enter your travel plans:",
#         placeholder="e.g., I want to travel to the Maldives with my wife for a romantic vacation with a budget of $10,000 for 3 nights and 4 days."
#     )

#     if st.button("Generate Itinerary"):
#         if user_input:
#             travel_info = parse_travel_input(user_input)
            
#             if "error" in travel_info:
#                 st.warning(travel_info["error"])
#             elif not travel_info["destination"]:
#                 st.warning("Could not extract destination. Please include it in your prompt.")
#             elif not travel_info["budget"]:
#                 st.warning("Could not extract budget. Please include it in your prompt.")
#             elif not travel_info["duration"]["days"]:
#                 st.warning("Could not extract duration. Please include it in your prompt.")
#             else:
#                 st.success("Information extracted successfully!")
                
#                 # Display extracted information
#                 st.write("**Extracted Information**:")
#                 st.write(f"**Destination**: {travel_info['destination']}")
#                 st.write(f"**Budget**: {travel_info['budget']['currency']} {travel_info['budget']['amount']:,}")
#                 st.write(f"**Duration**: {travel_info['duration']['nights']} nights and {travel_info['duration']['days']} days")
#                 if travel_info['duration']['start_date']:
#                     st.write(f"**Dates**: {travel_info['duration']['start_date']} to {travel_info['duration']['end_date']}")
#                 st.write(f"**Interests**: {', '.join(travel_info['interests']) if travel_info['interests'] else 'Not specified'}")
                
#                 # Fetch hotel, weather, and flight information
#                 with st.spinner("Fetching destination information..."):
#                     hotels, weather_forecast = get_hotels_from_tripadvisor(travel_info['destination'])
                    
#                     st.divider()
#                     st.markdown("<h1 style='text-align: center;'> YOUR TRIP INFORMATION</h1>", unsafe_allow_html=True)
                    
#                     # Display weather forecast if available
#                     if weather_forecast:
#                         display_weather_forecast(weather_forecast)
#                         st.divider()

#                     # Display flight options if hotels are available
#                     if hotels and len(hotels) > 0:
#                         first_hotel = hotels[0]
#                         if first_hotel['latitude'] and first_hotel['longitude']:
#                             flights_data = get_flight_options_with_fallback(
#                                 first_hotel['latitude'],
#                                 first_hotel['longitude'],
#                                 airports_df,
#                                 departure_airport_iata
#                             )
#                             display_flight_options(flights_data)  # Removed hotels parameter
                            
#                             # Display route information separately
#                             display_route_information(flights_data, hotels)
#                         else:
#                             st.warning("Could not find coordinates for the destination.")
                    
#                     st.divider()
#                     # Display hotel information
#                     if hotels:
#                         display_hotel_information(hotels)
#                     else:
#                         st.warning("No hotels found for the specified destination.")
#         else:
#             st.warning("Please enter your travel plans.")

# if __name__ == "__main__":
#     main()





# Working and good without Proper structure


# import streamlit as st
# import requests
# import re
# from datetime import datetime, timedelta
# import pandas as pd
# from math import radians, sin, cos, sqrt, atan2
# from streamlit_folium import st_folium
# import folium
# from polyline import decode  # Install via `pip install polyline`

# def extract_destination(text):
#     # Common patterns for destination extraction
#     patterns = [
#         r"(?:travel|go|flying|heading|visiting|trip) (?:to|in) ([A-Za-z\s,]+?)(?=\s*(?:for|with|on|and|$))",
#         r"(?:visiting|explore) ([A-Za-z\s,]+?)(?=\s*(?:for|with|on|and|$))",
#         r"(?:vacation|holiday) (?:in|at) ([A-Za-z\s,]+?)(?=\s*(?:for|with|on|and|$))"
#     ]
    
#     for pattern in patterns:
#         match = re.search(pattern, text.lower())
#         if match:
#             return match.group(1).strip().title()
#     return None

# def extract_duration(text):
#     nights, days = None, None
    
#     # Extract nights
#     night_match = re.search(r'(\d+)\s*nights?', text.lower())
#     if night_match:
#         nights = int(night_match.group(1))
#         days = nights + 1
    
#     # Extract days
#     day_match = re.search(r'(\d+)\s*days?', text.lower())
#     if day_match:
#         days = int(day_match.group(1))
#         if nights is None:
#             nights = days - 1
    
#     # Extract date range (DD/MM/YY or DD-MM-YY)
#     dates = re.findall(r'(\d{2}[-/]\d{2}[-/]\d{2})', text)
#     start_date = end_date = None
    
#     if len(dates) >= 2:
#         try:
#             start_date = datetime.strptime(dates[0].replace('-', '/'), "%d/%m/%y")
#             end_date = datetime.strptime(dates[1].replace('-', '/'), "%d/%m/%y")
#             days = (end_date - start_date).days
#             nights = days - 1
#         except ValueError:
#             pass
    
#     # Handle week
#     if 'week' in text.lower():
#         days = 7
#         nights = 6
    
#     return {
#         "nights": nights,
#         "days": days,
#         "start_date": start_date.strftime("%d/%m/%y") if start_date else None,
#         "end_date": end_date.strftime("%d/%m/%y") if end_date else None
#     }

# def extract_budget(text):
#     # Handle currency symbols
#     budget_patterns = [
#         r'(?:budget of |cost of |spend |price |cost )?[\$₹](\d+[,\d]*)',
#         r'(\d+[,\d]*)\s*(?:dollars|rupees)',
#     ]
    
#     for pattern in budget_patterns:
#         match = re.search(pattern, text.lower())
#         if match:
#             amount = int(match.group(1).replace(',', ''))
#             # Determine currency
#             if '$' in text or 'dollars' in text.lower():
#                 currency = "USD"
#             elif '₹' in text or 'rupees' in text.lower():
#                 currency = "INR"
#             else:
#                 currency = "USD"  # Default currency
#             return {"amount": amount, "currency": currency}
#     return None

# def extract_interests(text):
#     interest_keywords = {
#         'romantic': ['romantic', 'honeymoon', 'couple'],
#         'adventure': ['adventure', 'exciting', 'thrill', 'trek', 'fun'],
#         'nature': ['nature', 'wildlife', 'outdoor', 'forest', 'mountain', 'beach'],
#         'culture': ['culture', 'history', 'museum', 'heritage', 'art'],
#         'food': ['food', 'cuisine', 'dining', 'gastronomy', 'culinary'],
#         'relaxation': ['relaxation', 'peaceful', 'quiet', 'spa', 'wellness'],
#         'shopping': ['shopping', 'market', 'mall'],
#         'nightlife': ['party', 'club', 'nightlife', 'bar'],
#         'family': ['family', 'kids', 'children'],
#         'luxury': ['luxury', 'premium', 'high-end', 'exclusive']
#     }
    
#     found_interests = set()
#     text_lower = text.lower()
    
#     for category, keywords in interest_keywords.items():
#         if any(keyword in text_lower for keyword in keywords):
#             found_interests.add(category.title())
    
#     return list(found_interests)

# def get_hotel_photos(location_id, api_key):
#     """Fetch hotel photos from TripAdvisor API."""
#     url = f"https://api.content.tripadvisor.com/api/v1/location/{location_id}/photos"
#     params = {
#         "key": api_key,
#         "language": "en"
#     }
#     headers = {"accept": "application/json"}
    
#     try:
#         response = requests.get(url, params=params, headers=headers)
#         response.raise_for_status()
#         photos_data = response.json()
        
#         # Extract photo URLs from the response
#         photos = []
#         for photo in photos_data.get("data", [])[:3]:  # Limit to first 3 photos
#             if photo.get("images", {}).get("large", {}).get("url"):
#                 photos.append(photo["images"]["large"]["url"])
#         return photos
#     except requests.exceptions.RequestException as e:
#         st.error(f"Error fetching photos: {str(e)}")
#         return []

# def get_hotel_reviews(location_id, api_key):
#     """Fetch hotel reviews from TripAdvisor API."""
#     url = f"https://api.content.tripadvisor.com/api/v1/location/{location_id}/reviews"
#     params = {
#         "key": api_key,
#         "language": "en"
#     }
#     headers = {"accept": "application/json"}
    
#     try:
#         response = requests.get(url, params=params, headers=headers)
#         response.raise_for_status()
#         reviews_data = response.json()
        
#         # Extract relevant review information
#         reviews = []
#         for review in reviews_data.get("data", [])[:3]:  # Limit to first 3 reviews
#             review_info = {
#                 "title": review.get("title", "No Title"),
#                 "text": review.get("text", "No Review Text"),
#                 "rating": review.get("rating", "N/A"),
#                 "published_date": review.get("published_date", "N/A"),
#                 "username": review.get("user", {}).get("username", "Anonymous")
#             }
#             reviews.append(review_info)
#         return reviews
#     except requests.exceptions.RequestException as e:
#         st.error(f"Error fetching reviews: {str(e)}")
#         return []

# def get_weather_forecast(latitude, longitude, api_key):
#     """Fetch weather forecast from OpenWeatherMap API."""
#     url = f"http://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
    
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             forecast_data = response.json()
#             # Get the next 5 days forecast (data points every 3 hours, so we'll take one per day)
#             daily_forecasts = []
#             seen_dates = set()
            
#             for item in forecast_data['list']:
#                 date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
#                 if date not in seen_dates:
#                     seen_dates.add(date)
#                     daily_forecasts.append({
#                         'date': datetime.fromtimestamp(item['dt']).strftime('%d %b'),
#                         'temp': round(item['main']['temp']),
#                         'description': item['weather'][0]['description'],
#                         'icon': item['weather'][0]['icon']
#                     })
#                 if len(daily_forecasts) >= 5:
#                     break
            
#             return daily_forecasts
#     except Exception as e:
#         st.error(f"Error fetching weather data: {str(e)}")
#     return None

# # New functions for user location
# def get_user_ip():
#     """Get user's IP address."""
#     try:
#         response = requests.get("https://api.ipify.org?format=json")
#         if response.status_code == 200:
#             return response.json()['ip']
#         return None
#     except Exception as e:
#         print(f"Error getting IP: {e}")
#         return None

# def get_user_location(ip_address):
#     """Get location information from IP address."""
#     try:
#         url = f"http://ip-api.com/json/{ip_address}"
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             if data['status'] == 'success':
#                 return {
#                     "city": data.get('city'),
#                     "region": data.get('regionName'),
#                     "country": data.get('country'),
#                     "latitude": data.get('lat'),
#                     "longitude": data.get('lon')
#                 }
#         return None
#     except Exception as e:
#         print(f"Error getting location: {e}")
#         return None
    
# def calculate_distance(lat1, lon1, lat2, lon2):
#     """Calculate distance between two points using Haversine formula."""
#     try:
#         # Convert string inputs to float if necessary
#         lat1 = float(lat1)
#         lon1 = float(lon1)
#         lat2 = float(lat2)
#         lon2 = float(lon2)
        
#         R = 6371  # Earth's radius in kilometers

#         lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
#         dlat = lat2 - lat1
#         dlon = lon2 - lon1

#         a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
#         c = 2 * atan2(sqrt(a), sqrt(1-a))
#         distance = R * c

#         return distance
#     except (ValueError, TypeError) as e:
#         print(f"Error calculating distance: {e}")
#         return float('inf')  # Return infinity for invalid coordinates

# def find_multiple_nearest_airports(latitude, longitude, airports_df, max_airports=5, max_distance=300):
#     """Find multiple nearest airports within a reasonable distance."""
#     try:
#         # Convert coordinates to float
#         latitude = float(latitude)
#         longitude = float(longitude)
        
#         # Ensure lat and lon columns are float type
#         airports_df['lat'] = pd.to_numeric(airports_df['lat'], errors='coerce')
#         airports_df['lon'] = pd.to_numeric(airports_df['lon'], errors='coerce')
        
#         # Drop rows with invalid coordinates
#         airports_df = airports_df.dropna(subset=['lat', 'lon', 'iata'])
        
#         # Calculate distances for all airports
#         airports_df['distance'] = airports_df.apply(
#             lambda row: calculate_distance(
#                 latitude, longitude,
#                 row['lat'], row['lon']
#             ),
#             axis=1
#         )
        
#         # Get nearest airports within maximum distance
#         nearest_airports = airports_df[airports_df['distance'] <= max_distance].nsmallest(max_airports, 'distance')
        
#         if nearest_airports.empty:
#             print(f"No airports found within {max_distance} km")
#             return []
            
#         airports_list = []
#         for _, airport in nearest_airports.iterrows():
#             airports_list.append({
#                 'name': airport['name'],
#                 'iata': airport['iata'],
#                 'distance': airport['distance'],
#                 'lat': airport['lat'],
#                 'lon': airport['lon']
#             })
            
#         return airports_list
#     except Exception as e:
#         print(f"Error finding nearest airports: {e}")
#         return []

# def find_nearest_airport(latitude, longitude, airports_df):
#     """Find the single nearest airport to given coordinates."""
#     try:
#         airports = find_multiple_nearest_airports(latitude, longitude, airports_df, max_airports=1)
#         return airports[0] if airports else None
#     except Exception as e:
#         print(f"Error finding nearest airport: {e}")
#         return None
    
# def get_flight_options_with_fallback(destination_lat, destination_lon, airports_df, departure_airport_iata):
#     """Get flight options using SearchAPI with fallback to alternative airports."""
#     print("\nStarting enhanced flight search process...")
#     print(f"Input coordinates: lat={destination_lat}, lon={destination_lon}")
    
#     # Get multiple nearest airports
#     nearest_airports = find_multiple_nearest_airports(destination_lat, destination_lon, airports_df)
    
#     if not nearest_airports:
#         st.warning("No airports found within reasonable distance.")
#         return None
        
#     for airport in nearest_airports:
#         print(f"\nTrying airport: {airport['name']} ({airport['iata']}) - {airport['distance']:.2f} km away")
        
#         url = "https://www.searchapi.io/api/v1/search"
#         params = {
#             "engine": "google_flights",
#             "flight_type": "one_way",
#             "departure_id": departure_airport_iata,  # Use detected departure airport
#             "arrival_id": airport['iata'],
#             "outbound_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
#             "api_key": "UdxjESojjvM58CeEVvxTwr2S"
#         }
        
#         try:
#             response = requests.get(url, params=params)
#             response.raise_for_status()
#             flights_data = response.json()
            
#             if flights_data and 'best_flights' in flights_data and flights_data['best_flights']:
#                 print(f"Found flights for {airport['iata']}")
#                 flights_data['airport_info'] = {
#                     'name': airport['name'],
#                     'iata': airport['iata'],
#                     'distance': airport['distance']
#                 }
#                 return flights_data
#             else:
#                 print(f"No flights found for {airport['iata']}")
                
#         except requests.exceptions.RequestException as e:
#             print(f"Error in API request for {airport['iata']}: {str(e)}")
#             continue
    
#     st.warning("No flights found from any nearby airports.")
#     return None


# def get_directions(api_key, origin_city, destination_city, mode='driving'):
#     """Get directions from Google Maps API using city names."""
#     url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin_city}&destination={destination_city}&mode={mode}&key={api_key}"
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         st.error(f"Error fetching directions: {str(e)}")
#         return None

# def plot_route_on_map(directions_data, mode):
#     """Create a Folium map with the route plotted."""
#     if not directions_data or 'routes' not in directions_data or not directions_data['routes']:
#         return None

#     try:
#         # Extract route points from directions
#         route = directions_data['routes'][0]['overview_polyline']['points']
#         coordinates = decode(route)
        
#         # Create a map centered on the origin with reduced zoom
#         start_location = coordinates[0]
#         m = folium.Map(
#             location=start_location, 
#             zoom_start=8,  # Reduced zoom level
#             prefer_canvas=True  # Use canvas renderer for better performance
#         )
        
#         # Add route as a polyline with simplified styling
#         color = "blue" if mode == "driving" else "green"
#         folium.PolyLine(
#             coordinates, 
#             color=color, 
#             weight=3,  # Reduced line weight
#             opacity=0.6  # Reduced opacity
#         ).add_to(m)
        
#         # Add simplified markers
#         folium.Marker(
#             coordinates[0], 
#             tooltip="Airport",
#             icon=folium.Icon(color="green", icon="plane", prefix='fa', size=(20, 20))
#         ).add_to(m)
        
#         folium.Marker(
#             coordinates[-1], 
#             tooltip="Hotel",
#             icon=folium.Icon(color="red", icon="hotel", prefix='fa', size=(20, 20))
#         ).add_to(m)
        
#         # Fit bounds to show the entire route
#         m.fit_bounds([coordinates[0], coordinates[-1]])
        
#         return m
#     except Exception as e:
#         st.error(f"Error creating map: {str(e)}")
#         return None

# def display_flight_options(flights_data):
#     """Display flight options using Streamlit components with airline logos and INR prices."""
#     if not flights_data or 'best_flights' not in flights_data:
#         st.warning("No flight information available.")
#         return
    
#     st.subheader("Available Flights")
    
#     # Display airport information if available
#     if 'airport_info' in flights_data:
#         airport_info = flights_data['airport_info']
#         st.info(f"Showing flights to {airport_info['name']} ({airport_info['iata']}) - {airport_info['distance']:.1f} km from destination")
    
#     # USD to INR conversion rate
#     USD_TO_INR = 84.5
    
#     for best_flight in flights_data['best_flights'][:2]:  # Display top flight option
#         total_duration = best_flight.get('total_duration', 'N/A')
#         price_usd = best_flight.get('price', 0)
#         price_inr = price_usd * USD_TO_INR
        
#         # Create expander header with price in both currencies
#         expander_header = f"₹{price_inr:,.2f} (${price_usd}) - ⏱️ {total_duration} mins"
        
#         with st.expander(expander_header):
#             # Display each flight segment in the itinerary
#             for i, flight in enumerate(best_flight['flights'], 1):
#                 # Create columns for airline info and flight details
#                 col1, col2 = st.columns([1, 3])
                
#                 with col1:
#                     # Display airline logo if available
#                     if 'airline_logo' in flight:
#                         st.image(flight['airline_logo'], width=70)
#                     st.write(f"**{flight.get('airline', 'N/A')}**")
#                     st.write(f"Flight {flight.get('flight_number', 'N/A')}")
                
#                 with col2:
#                     # Create sub-columns for departure and arrival
#                     dep_col, arr_col = st.columns(2)
                    
#                     with dep_col:
#                         st.write("**Departure:**")
#                         dep = flight['departure_airport']
#                         st.write(f"🛫 {dep['name']} ({dep['id']})")
#                         st.write(f"📅 {dep['date']}")
#                         st.write(f"🕒 {dep['time']}")
                    
#                     with arr_col:
#                         st.write("**Arrival:**")
#                         arr = flight['arrival_airport']
#                         st.write(f"🛬 {arr['name']} ({arr['id']})")
#                         st.write(f"📅 {arr['date']}")
#                         st.write(f"🕒 {arr['time']}")
                
#                 # Flight details section
#                 st.write("**Flight Details:**")
#                 st.write(f"✈️ Aircraft: {flight.get('airplane', 'N/A')}")
#                 st.write(f"⏱️ Duration: {flight.get('duration', 'N/A')} mins")
                
#                 # Display any additional flight information from extensions
#                 if 'detected_extensions' in flight:
#                     ext = flight['detected_extensions']
#                     if 'seat_type' in ext:
#                         st.write(f"💺 Seat: {ext['seat_type']}")
#                     if 'legroom_long' in ext:
#                         st.write(f"🦵 Legroom: {ext['legroom_long']}")
#                     if 'carbon_emission' in ext:
#                         st.write(f"🌱 Carbon emission: {ext['carbon_emission']} kg")
                
#                 # Display layover information
#                 if i < len(best_flight['flights']) and 'layovers' in best_flight:
#                     layover = best_flight['layovers'][i-1]
#                     st.markdown("---")
#                     st.write(f"🕒 **Layover:** {layover.get('duration', 'N/A')} mins at {layover.get('name', 'N/A')}")
#                     st.markdown("---")

# def display_route_information(flights_data, hotels):
#     """Display route information from airport to hotel."""
#     if not hotels or len(hotels) == 0 or not flights_data:
#         return
        
#     # Add custom CSS to control map container height
#     st.markdown("""
#         <style>
#         .stfolium-container {
#             height: 420px !important;
#             margin-bottom: 1rem;
#         }
#         iframe {
#             height: 420px !important;
#         }
#         </style>
#     """, unsafe_allow_html=True)
        
#     google_maps_api_key = "AIzaSyA5QKrsVtwQa30vzOgZwo_p1ak5tyzgyE0"
    
#     st.divider()
#     st.subheader("🗺️ Ground Transportation to Destination")
    
#     # Get arrival city and destination city
#     arrival_city = flights_data['airports'][0]['arrival'][0]['city']
#     destination_city = hotels[0].get('address_obj', {}).get('city', '')
    
#     if arrival_city and destination_city:
#         # Display route information for both driving and transit
#         modes = ['driving', 'transit']
#         mode_icons = {'driving': '🚗', 'transit': '🚌'}
        
#         for mode in modes:
#             st.write(f"**{mode_icons[mode]} {mode.title()} Option:**")
            
#             directions_data = get_directions(google_maps_api_key, arrival_city, destination_city, mode)
            
#             if directions_data and 'routes' in directions_data and directions_data['routes']:
#                 leg = directions_data['routes'][0]['legs'][0]
#                 st.write(f"📏 Distance: {leg['distance']['text']}")
#                 st.write(f"⏱️ Duration: {leg['duration']['text']}")
                
#                 route_map = plot_route_on_map(directions_data, mode)
#                 if route_map:
#                     st_folium(
#                         route_map,
#                         width=704,  # Match the container width you observed
#                         height=420,  # Match the map height you observed
#                         returned_objects=[],
#                         use_container_width=False
#                     )
#             else:
#                 st.warning(f"No {mode} route available")
#     else:
#         st.warning("Could not determine city information for route mapping")

# def display_weather_forecast(forecasts):
#     """Display weather forecast using Streamlit components."""
#     if not forecasts:
#         return
    
#     st.divider()
#     st.subheader("5-Day Weather Forecast At the Destination")
#     cols = st.columns(len(forecasts))
    
#     for idx, forecast in enumerate(forecasts):
#         with cols[idx]:
#             st.write(f"**{forecast['date']}**")
#             icon_url = f"http://openweathermap.org/img/wn/{forecast['icon']}@2x.png"
#             st.image(icon_url, width=50)
#             st.write(f"{forecast['temp']}°C")
#             st.write(f"*{forecast['description'].capitalize()}*")

# def get_destination_details(destination, categories=None):
#     """
#     Fetch details from TripAdvisor API for a given destination across multiple categories.
    
#     Args:
#         destination (str): Name of the destination
#         categories (list): List of categories to fetch. Defaults to ["hotels", "attractions", "restaurants", "geos"]
    
#     Returns:
#         tuple: (destination_details, weather_forecast)
#         - destination_details: dict containing details for each category
#         - weather_forecast: weather data for the destination
#     """
#     if categories is None:
#         categories = ["hotels", "attractions", "restaurants", "geos"]
    
#     base_url = "https://api.content.tripadvisor.com/api/v1"
#     tripadvisor_api_key = "C5104F92E6354A079E0C6E424B3B1F06"
#     weather_api_key = "a73d2e9d5872429030175d780367cf35"
    
#     try:
#         destination_details = {}
#         weather_forecast = None
#         first_location_coords = None

#         for category in categories:
#             # Search for locations in the category
#             search_url = f"{base_url}/location/search"
#             search_params = {
#                 "key": tripadvisor_api_key,
#                 "searchQuery": destination,
#                 "category": category,
#                 "language": "en"
#             }
            
#             search_response = requests.get(
#                 search_url,
#                 params=search_params,
#                 headers={"accept": "application/json"}
#             )
#             search_response.raise_for_status()
#             search_data = search_response.json()
            
#             # Extract location IDs
#             location_ids = [
#                 item.get("location_id")
#                 for item in search_data.get("data", [])
#             ]
            
#             category_details = []
            
#             # Fetch details for each location (limited to first 5)
#             for location_id in location_ids[:5]:
#                 details_url = f"{base_url}/location/{location_id}/details"
#                 details_params = {
#                     "key": tripadvisor_api_key,
#                     "language": "en",
#                     "currency": "USD"
#                 }
                
#                 details_response = requests.get(
#                     details_url,
#                     params=details_params,
#                     headers={"accept": "application/json"}
#                 )
#                 details_response.raise_for_status()
#                 location_data = details_response.json()
                
#                 # Extract coordinates
#                 latitude = location_data.get("latitude")
#                 longitude = location_data.get("longitude")
                
#                 # Store first valid coordinates for weather data
#                 if first_location_coords is None and latitude and longitude:
#                     first_location_coords = (latitude, longitude)
                
#                 # Fetch photos and reviews
#                 photos = get_hotel_photos(location_id, tripadvisor_api_key)
#                 reviews = get_hotel_reviews(location_id, tripadvisor_api_key)
                
#                 # Compile location information based on category
#                 location_info = {
#                     "name": location_data.get("name", "N/A"),
#                     "description": location_data.get("description", "No description available"),
#                     "web_url": location_data.get("web_url", "N/A"),
#                     "phone": location_data.get("phone", "N/A"),
#                     "latitude": latitude,
#                     "longitude": longitude,
#                     "address_obj": location_data.get("address_obj", {}),
#                     "photos": photos,
#                     "reviews": reviews
#                 }
                
#                 # Add category-specific information
#                 if category == "hotels":
#                     location_info.update({
#                         "price_level": location_data.get("price_level", "N/A"),
#                         "amenities": location_data.get("amenities", [])[:6]
#                     })
#                 elif category == "restaurants":
#                     location_info.update({
#                         "cuisine": location_data.get("cuisine", []),
#                         "price_range": location_data.get("price_range", "N/A"),
#                         "dietary_restrictions": location_data.get("dietary_restrictions", [])
#                     })
#                 elif category == "attractions":
#                     location_info.update({
#                         "attraction_types": location_data.get("attraction_types", []),
#                         "rating": location_data.get("rating", "N/A"),
#                         "ranking": location_data.get("ranking", "N/A")
#                     })
#                 elif category == "geos":
#                     location_info.update({
#                         "geo_type": location_data.get("geo_type", "N/A"),
#                         "ancestors": location_data.get("ancestors", []),
#                         "timezone": location_data.get("timezone", "N/A")
#                     })
                
#                 category_details.append(location_info)
            
#             destination_details[category] = category_details
        
#         # Fetch weather data if we have coordinates
#         if first_location_coords:
#             weather_forecast = get_weather_forecast(
#                 first_location_coords[0],
#                 first_location_coords[1],
#                 weather_api_key
#             )
        
#         return destination_details, weather_forecast
    
#     except requests.exceptions.RequestException as e:
#         st.error(f"Error fetching destination data: {str(e)}")
#         return {}, None

# def display_destination_details(destination_details):
#     """
#     Display the fetched destination details in the Streamlit app.
    
#     Args:
#         destination_details (dict): Dictionary containing details for each category
#     """
#     for category, items in destination_details.items():
#         if items:
#             st.subheader(f"{category.title()}")
            
#             for item in items:
#                 with st.expander(f"{item['name']}"):
#                     # Display photos first if available
#                     if item['photos'] and len(item['photos']) > 0:
#                         # st.write("**Photos:**")
#                         # Check the structure of the first photo to determine how to handle it
#                         if isinstance(item['photos'][0], str):
#                             # If photos are direct URLs
#                             cols = st.columns(min(3, len(item['photos'])))
#                             for idx, photo_url in enumerate(item['photos'][:3]):
#                                 try:
#                                     cols[idx].image(photo_url, use_container_width=True)
#                                 except Exception as e:
#                                     st.error(f"Error displaying photo: {str(e)}")
#                         else:
#                             # If photos are objects with URLs
#                             cols = st.columns(min(3, len(item['photos'])))
#                             for idx, photo in enumerate(item['photos'][:3]):
#                                 try:
#                                     photo_url = photo.get('url') if isinstance(photo, dict) else str(photo)
#                                     cols[idx].image(photo_url, use_container_width=True)
#                                 except Exception as e:
#                                     st.error(f"Error displaying photo: {str(e)}")

#                     st.write(f"**Description:** {item['description']}")
#                     st.write(f"**Phone:** {item['phone']}")
                    
#                     # Display address if available
#                     if item['address_obj']:
#                         address = item['address_obj']
#                         st.write("**Address:**")
#                         st.write(f"{address.get('street1', '')}")
#                         st.write(f"{address.get('city', '')}, {address.get('state', '')} {address.get('postalcode', '')}")
#                         st.write(f"{address.get('country', '')}")
                    
#                     # Display category-specific information
#                     if category == "hotels":
#                         st.write(f"**Price Level:** {item['price_level']}")
#                         if item['amenities']:
#                             st.write("**Amenities:**")
#                             st.write(", ".join(item['amenities']))
                    
#                     elif category == "restaurants":
#                         if item.get('cuisine'):
#                             st.write("**Cuisine:**")
#                             st.write(", ".join([c.get('name', '') for c in item['cuisine']]))
#                         st.write(f"**Price Range:** {item.get('price_range', 'N/A')}")
#                         if item.get('dietary_restrictions'):
#                             st.write("**Dietary Options:**")
#                             st.write(", ".join([d.get('name', '') for d in item['dietary_restrictions']]))
                    
#                     elif category == "attractions":
#                         if item.get('attraction_types'):
#                             st.write("**Attraction Types:**")
#                             st.write(", ".join([t.get('name', '') for t in item['attraction_types']]))
#                         st.write(f"**Rating:** {item.get('rating', 'N/A')}")
#                         st.write(f"**Ranking:** {item.get('ranking', 'N/A')}")
                    
#                     elif category == "geos":
#                         st.write(f"**Type:** {item.get('geo_type', 'N/A')}")
#                         st.write(f"**Timezone:** {item.get('timezone', 'N/A')}")
                    
#                     # Display reviews if available
#                     if item['reviews']:
#                         st.write("**Recent Reviews:**")
#                         for review in item['reviews'][:3]:
#                             if isinstance(review, dict):
#                                 st.markdown(f"⭐ **{review.get('rating', 'N/A')}/5** - {review.get('text', 'No review text')}")
#                             else:
#                                 st.markdown(f"⭐ {review}")
                    
#                     st.write(f"[View on TripAdvisor]({item['web_url']})")

# def get_hotel_photos(location_id, api_key):
#     """
#     Fetch photos for a specific location from TripAdvisor API.
    
#     Args:
#         location_id (str): TripAdvisor location ID
#         api_key (str): TripAdvisor API key
    
#     Returns:
#         list: List of photo URLs or photo objects
#     """
#     try:
#         base_url = "https://api.content.tripadvisor.com/api/v1"
#         photos_url = f"{base_url}/location/{location_id}/photos"
#         photos_params = {
#             "key": api_key,
#             "language": "en"
#         }
        
#         response = requests.get(
#             photos_url,
#             params=photos_params,
#             headers={"accept": "application/json"}
#         )
#         response.raise_for_status()
        
#         photos_data = response.json()
#         photos = []
        
#         # Extract photo URLs from the response
#         if isinstance(photos_data, dict) and 'data' in photos_data:
#             for photo in photos_data['data'][:3]:  # Limit to 3 photos
#                 if isinstance(photo, dict):
#                     # Extract the largest available image URL
#                     images = photo.get('images', {})
#                     if images:
#                         # Try to get the large image, fall back to original if not available
#                         photo_url = (images.get('large', {}) or images.get('original', {})).get('url')
#                         if photo_url:
#                             photos.append(photo_url)
        
#         return photos
    
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching photos: {str(e)}")
#         return []

# # def display_hotel_information(hotels):
# #     """Display hotel information in a structured format using Streamlit components."""
# #     st.subheader("Available Hotels")
    
# #     for i, hotel in enumerate(hotels, 1):
# #         price_desc = get_price_level_description(hotel['price_level'])
# #         with st.expander(f"{i}. {hotel['name']}"):
# #             # Display hotel photos in a horizontal arrangement
# #             if hotel['photos']:
# #                 cols = st.columns(min(len(hotel['photos']), 3))
# #                 for idx, photo_url in enumerate(hotel['photos']):
# #                     cols[idx].image(photo_url, use_container_width=True)
            
# #             st.write("**Description:**")
# #             st.write(hotel['description'])
            
# #             st.divider()
            
# #             st.write("**Price Level:**")
# #             st.write(f"{hotel['price_level']}: {price_desc}")
            
# #             st.divider()
            
# #             st.write("**Contact Information:**")
# #             st.write(f"🌐 [Visit Website]({hotel['web_url']})")
# #             if hotel['phone'] != "N/A":
# #                 st.write(f"📞 {hotel['phone']}")
            
# #             if hotel['amenities']:
# #                 st.divider()
# #                 st.write("**Top Amenities:**")
# #                 # Create two columns
# #                 col1, col2 = st.columns(2)
                
# #                 # Split the amenities list into two parts
# #                 mid_point = len(hotel['amenities']) // 2
# #                 amenities_col1 = hotel['amenities'][:mid_point]
# #                 amenities_col2 = hotel['amenities'][mid_point:]
                
# #                 # Display the amenities in the respective columns
# #                 with col1:
# #                     for amenity in amenities_col1:
# #                         st.write(f"✓ {amenity}")
# #                 with col2:
# #                     for amenity in amenities_col2:
# #                         st.write(f"✓ {amenity}")

            
# #             if hotel['reviews']:
# #                 st.divider()
                
# #                 st.write("**Recent Reviews:**")
# #                 for review in hotel['reviews']:
# #                     # Using consistent formatting for all reviews
# #                     st.write(f"⭐ **{review['rating']}/5**")
# #                     st.write(f"*\"{review['title']}\"*")
# #                     st.write(review['text'])
# #                     st.write(f"— {review['username']} ({review['published_date']})")
# #                     # st.write("---")

# def get_price_level_description(price_level):
#     """Convert price level symbols to descriptive text."""
#     price_descriptions = {
#         "$$$$": "Very Costly",
#         "$$$": "Costly",
#         "$$": "Affordable",
#         "$": "Great Bargain!!"
#     }
#     return price_descriptions.get(price_level, price_level)

# def parse_travel_input(text):
#     if not text:
#         return {"error": "Please enter your travel plans."}
    
#     try:
#         destination = extract_destination(text)
#         budget = extract_budget(text)
#         duration = extract_duration(text)
#         interests = extract_interests(text)
        
#         return {
#             "destination": destination,
#             "budget": budget,
#             "duration": duration,
#             "interests": interests
#         }
#     except Exception as e:
#         return {"error": f"Error processing input: {str(e)}"}

# def main():
#     st.title("Travel Itinerary Generator and Assistant")
    
#     # Load airports data
#     try:
#         airports_df = pd.read_csv('airports.csv')
#         airports_df['lat'] = pd.to_numeric(airports_df['lat'], errors='coerce')
#         airports_df['lon'] = pd.to_numeric(airports_df['lon'], errors='coerce')
#         airports_df = airports_df.dropna(subset=['lat', 'lon', 'iata'])
#     except Exception as e:
#         st.error(f"Error loading airports data: {e}")
#         return

#     st.write("Describe your travel plans in one sentence, and I'll generate a personalized itinerary.")

#     user_input = st.text_area(
#         "Enter your travel plans:",
#         placeholder="e.g., I want to travel to the Maldives with my wife for a romantic vacation with a budget of $10,000 for 3 nights and 4 days."
#     )

#     if st.button("Generate Itinerary"):
#         if user_input:
#             # First, get location info
#             departure_airport_iata = "BOM"  # Default to Mumbai
#             user_ip = get_user_ip()
#             location_info = {}
            
#             if user_ip:
#                 location = get_user_location(user_ip)
#                 if location:
#                     location_info['location'] = f"📍 Detected your location: {location['city']}, {location['region']}, {location['country']}"
                    
#                     nearest_airport = find_nearest_airport(location['latitude'], location['longitude'], airports_df)
#                     if nearest_airport:
#                         departure_airport_iata = nearest_airport['iata']
#                         location_info['airport'] = f"✈️ Nearest Airport: {nearest_airport['name']} ({departure_airport_iata})"
#                     else:
#                         location_info['airport'] = "Using Mumbai (BOM) as default departure airport."
#                 else:
#                     location_info['airport'] = "Unable to determine your location. Using Mumbai (BOM) as default departure airport."
#             else:
#                 location_info['airport'] = "Unable to retrieve your IP address. Using Mumbai (BOM) as default departure airport."

#             # Parse and validate travel input
#             travel_info = parse_travel_input(user_input)
            
#             if "error" in travel_info:
#                 st.warning(travel_info["error"])
#                 return
#             elif not travel_info["destination"]:
#                 st.warning("Could not extract destination. Please include it in your prompt.")
#                 return
#             elif not travel_info["budget"]:
#                 st.warning("Could not extract budget. Please include it in your prompt.")
#                 return
#             elif not travel_info["duration"]["days"]:
#                 st.warning("Could not extract duration. Please include it in your prompt.")
#                 return

#             # Display location info
#             st.write(location_info.get('location', ''))
#             st.write(location_info.get('airport', ''))
            
#             # Display success message and extracted info
#             st.success("Information extracted successfully!")
#             st.write("**Extracted Information**:")
#             st.write(f"**Destination**: {travel_info['destination']}")
#             st.write(f"**Budget**: {travel_info['budget']['currency']} {travel_info['budget']['amount']:,}")
#             st.write(f"**Duration**: {travel_info['duration']['nights']} nights and {travel_info['duration']['days']} days")
#             if travel_info['duration']['start_date']:
#                 st.write(f"**Dates**: {travel_info['duration']['start_date']} to {travel_info['duration']['end_date']}")
#             st.write(f"**Interests**: {', '.join(travel_info['interests']) if travel_info['interests'] else 'Not specified'}")

#             # Now show spinner while fetching trip details
#             with st.spinner("Generating your personalized travel itinerary..."):
#                 # Fetch all required data
#                 destination_details, weather_forecast = get_destination_details(travel_info['destination'])
                
#                 # Get coordinates for flight search
#                 destination_coords = None
#                 flights_data = None
#                 if destination_details.get('hotels') and len(destination_details['hotels']) > 0:
#                     first_hotel = destination_details['hotels'][0]
#                     if first_hotel['latitude'] and first_hotel['longitude']:
#                         destination_coords = {
#                             'latitude': first_hotel['latitude'],
#                             'longitude': first_hotel['longitude']
#                         }
#                         flights_data = get_flight_options_with_fallback(
#                             destination_coords['latitude'],
#                             destination_coords['longitude'],
#                             airports_df,
#                             departure_airport_iata
#                         )

#             # After spinner, display trip information
#             st.markdown("<h1 style='text-align: center;'>YOUR TRIP INFORMATION</h1>", unsafe_allow_html=True)
            
#             # Display weather information
#             if weather_forecast:
#                 display_weather_forecast(weather_forecast)
#                 st.divider()
            
#             # Display flight options if available
#             if flights_data:
#                 display_flight_options(flights_data)
#                 display_route_information(flights_data, destination_details.get('hotels', []))
#                 st.divider()
#             else:
#                 st.warning("Could not find coordinates for the destination.")
            
#             # Display destination details
#             if destination_details:
#                 display_destination_details(destination_details)
#             else:
#                 st.warning("No destination information found.")
                
#         else:
#             st.warning("Please enter your travel plans.")

# if __name__ == "__main__":
#     main()







# import streamlit as st
# import requests
# import re
# from datetime import datetime, timedelta
# import pandas as pd
# from math import radians, sin, cos, sqrt, atan2
# from streamlit_folium import st_folium
# import folium
# from polyline import decode  # Install via `pip install polyline`

# def extract_destination(text):
#     # Common patterns for destination extraction
#     patterns = [
#         r"(?:travel|go|flying|heading|visiting|trip) (?:to|in) ([A-Za-z\s,]+?)(?=\s*(?:for|with|on|and|$))",
#         r"(?:visiting|explore) ([A-Za-z\s,]+?)(?=\s*(?:for|with|on|and|$))",
#         r"(?:vacation|holiday) (?:in|at) ([A-Za-z\s,]+?)(?=\s*(?:for|with|on|and|$))"
#     ]
    
#     for pattern in patterns:
#         match = re.search(pattern, text.lower())
#         if match:
#             return match.group(1).strip().title()
#     return None

# def extract_duration(text):
#     nights, days = None, None
    
#     # Extract nights
#     night_match = re.search(r'(\d+)\s*nights?', text.lower())
#     if night_match:
#         nights = int(night_match.group(1))
#         days = nights + 1
    
#     # Extract days
#     day_match = re.search(r'(\d+)\s*days?', text.lower())
#     if day_match:
#         days = int(day_match.group(1))
#         if nights is None:
#             nights = days - 1
    
#     # Extract date range (DD/MM/YY or DD-MM-YY)
#     dates = re.findall(r'(\d{2}[-/]\d{2}[-/]\d{2})', text)
#     start_date = end_date = None
    
#     if len(dates) >= 2:
#         try:
#             start_date = datetime.strptime(dates[0].replace('-', '/'), "%d/%m/%y")
#             end_date = datetime.strptime(dates[1].replace('-', '/'), "%d/%m/%y")
#             days = (end_date - start_date).days
#             nights = days - 1
#         except ValueError:
#             pass
    
#     # Handle week
#     if 'week' in text.lower():
#         days = 7
#         nights = 6
    
#     return {
#         "nights": nights,
#         "days": days,
#         "start_date": start_date.strftime("%d/%m/%y") if start_date else None,
#         "end_date": end_date.strftime("%d/%m/%y") if end_date else None
#     }

# def extract_budget(text):
#     # Handle currency symbols
#     budget_patterns = [
#         r'(?:budget of |cost of |spend |price |cost )?[\$₹](\d+[,\d]*)',
#         r'(\d+[,\d]*)\s*(?:dollars|rupees)',
#     ]
    
#     for pattern in budget_patterns:
#         match = re.search(pattern, text.lower())
#         if match:
#             amount = int(match.group(1).replace(',', ''))
#             # Determine currency
#             if '$' in text or 'dollars' in text.lower():
#                 currency = "USD"
#             elif '₹' in text or 'rupees' in text.lower():
#                 currency = "INR"
#             else:
#                 currency = "USD"  # Default currency
#             return {"amount": amount, "currency": currency}
#     return None

# def extract_interests(text):
#     interest_keywords = {
#         'romantic': ['romantic', 'honeymoon', 'couple'],
#         'adventure': ['adventure', 'exciting', 'thrill', 'trek', 'fun'],
#         'nature': ['nature', 'wildlife', 'outdoor', 'forest', 'mountain', 'beach'],
#         'culture': ['culture', 'history', 'museum', 'heritage', 'art'],
#         'food': ['food', 'cuisine', 'dining', 'gastronomy', 'culinary'],
#         'relaxation': ['relaxation', 'peaceful', 'quiet', 'spa', 'wellness'],
#         'shopping': ['shopping', 'market', 'mall'],
#         'nightlife': ['party', 'club', 'nightlife', 'bar'],
#         'family': ['family', 'kids', 'children'],
#         'luxury': ['luxury', 'premium', 'high-end', 'exclusive']
#     }
    
#     found_interests = set()
#     text_lower = text.lower()
    
#     for category, keywords in interest_keywords.items():
#         if any(keyword in text_lower for keyword in keywords):
#             found_interests.add(category.title())
    
#     return list(found_interests)

# def get_hotel_photos(location_id, api_key):
#     """Fetch hotel photos from TripAdvisor API."""
#     url = f"https://api.content.tripadvisor.com/api/v1/location/{location_id}/photos"
#     params = {
#         "key": api_key,
#         "language": "en"
#     }
#     headers = {"accept": "application/json"}
    
#     try:
#         response = requests.get(url, params=params, headers=headers)
#         response.raise_for_status()
#         photos_data = response.json()
        
#         # Extract photo URLs from the response
#         photos = []
#         for photo in photos_data.get("data", [])[:3]:  # Limit to first 3 photos
#             if photo.get("images", {}).get("large", {}).get("url"):
#                 photos.append(photo["images"]["large"]["url"])
#         return photos
#     except requests.exceptions.RequestException as e:
#         st.error(f"Error fetching photos: {str(e)}")
#         return []

# def get_hotel_reviews(location_id, api_key):
#     """Fetch hotel reviews from TripAdvisor API."""
#     url = f"https://api.content.tripadvisor.com/api/v1/location/{location_id}/reviews"
#     params = {
#         "key": api_key,
#         "language": "en"
#     }
#     headers = {"accept": "application/json"}
    
#     try:
#         response = requests.get(url, params=params, headers=headers)
#         response.raise_for_status()
#         reviews_data = response.json()
        
#         # Extract relevant review information
#         reviews = []
#         for review in reviews_data.get("data", [])[:3]:  # Limit to first 3 reviews
#             review_info = {
#                 "title": review.get("title", "No Title"),
#                 "text": review.get("text", "No Review Text"),
#                 "rating": review.get("rating", "N/A"),
#                 "published_date": review.get("published_date", "N/A"),
#                 "username": review.get("user", {}).get("username", "Anonymous")
#             }
#             reviews.append(review_info)
#         return reviews
#     except requests.exceptions.RequestException as e:
#         st.error(f"Error fetching reviews: {str(e)}")
#         return []

# def get_weather_forecast(latitude, longitude, api_key):
#     """Fetch weather forecast from OpenWeatherMap API."""
#     url = f"http://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
    
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             forecast_data = response.json()
#             # Get the next 5 days forecast (data points every 3 hours, so we'll take one per day)
#             daily_forecasts = []
#             seen_dates = set()
            
#             for item in forecast_data['list']:
#                 date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
#                 if date not in seen_dates:
#                     seen_dates.add(date)
#                     daily_forecasts.append({
#                         'date': datetime.fromtimestamp(item['dt']).strftime('%d %b'),
#                         'temp': round(item['main']['temp']),
#                         'description': item['weather'][0]['description'],
#                         'icon': item['weather'][0]['icon']
#                     })
#                 if len(daily_forecasts) >= 5:
#                     break
            
#             return daily_forecasts
#     except Exception as e:
#         st.error(f"Error fetching weather data: {str(e)}")
#     return None

# # New functions for user location
# def get_user_ip():
#     """Get user's IP address."""
#     try:
#         response = requests.get("https://api.ipify.org?format=json")
#         if response.status_code == 200:
#             return response.json()['ip']
#         return None
#     except Exception as e:
#         print(f"Error getting IP: {e}")
#         return None

# def get_user_location(ip_address):
#     """Get location information from IP address."""
#     try:
#         url = f"http://ip-api.com/json/{ip_address}"
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             if data['status'] == 'success':
#                 return {
#                     "city": data.get('city'),
#                     "region": data.get('regionName'),
#                     "country": data.get('country'),
#                     "latitude": data.get('lat'),
#                     "longitude": data.get('lon')
#                 }
#         return None
#     except Exception as e:
#         print(f"Error getting location: {e}")
#         return None
    
# def calculate_distance(lat1, lon1, lat2, lon2):
#     """Calculate distance between two points using Haversine formula."""
#     try:
#         # Convert string inputs to float if necessary
#         lat1 = float(lat1)
#         lon1 = float(lon1)
#         lat2 = float(lat2)
#         lon2 = float(lon2)
        
#         R = 6371  # Earth's radius in kilometers

#         lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
#         dlat = lat2 - lat1
#         dlon = lon2 - lon1

#         a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
#         c = 2 * atan2(sqrt(a), sqrt(1-a))
#         distance = R * c

#         return distance
#     except (ValueError, TypeError) as e:
#         print(f"Error calculating distance: {e}")
#         return float('inf')  # Return infinity for invalid coordinates

# def find_multiple_nearest_airports(latitude, longitude, airports_df, max_airports=5, max_distance=300):
#     """Find multiple nearest airports within a reasonable distance."""
#     try:
#         # Convert coordinates to float
#         latitude = float(latitude)
#         longitude = float(longitude)
        
#         # Ensure lat and lon columns are float type
#         airports_df['lat'] = pd.to_numeric(airports_df['lat'], errors='coerce')
#         airports_df['lon'] = pd.to_numeric(airports_df['lon'], errors='coerce')
        
#         # Drop rows with invalid coordinates
#         airports_df = airports_df.dropna(subset=['lat', 'lon', 'iata'])
        
#         # Calculate distances for all airports
#         airports_df['distance'] = airports_df.apply(
#             lambda row: calculate_distance(
#                 latitude, longitude,
#                 row['lat'], row['lon']
#             ),
#             axis=1
#         )
        
#         # Get nearest airports within maximum distance
#         nearest_airports = airports_df[airports_df['distance'] <= max_distance].nsmallest(max_airports, 'distance')
        
#         if nearest_airports.empty:
#             print(f"No airports found within {max_distance} km")
#             return []
            
#         airports_list = []
#         for _, airport in nearest_airports.iterrows():
#             airports_list.append({
#                 'name': airport['name'],
#                 'iata': airport['iata'],
#                 'distance': airport['distance'],
#                 'lat': airport['lat'],
#                 'lon': airport['lon']
#             })
            
#         return airports_list
#     except Exception as e:
#         print(f"Error finding nearest airports: {e}")
#         return []

# def find_nearest_airport(latitude, longitude, airports_df):
#     """Find the single nearest airport to given coordinates."""
#     try:
#         airports = find_multiple_nearest_airports(latitude, longitude, airports_df, max_airports=1)
#         return airports[0] if airports else None
#     except Exception as e:
#         print(f"Error finding nearest airport: {e}")
#         return None
    
# def get_flight_options_with_fallback(destination_lat, destination_lon, airports_df, departure_airport_iata):
#     """Get flight options using SearchAPI with fallback to alternative airports."""
#     print("\nStarting enhanced flight search process...")
#     print(f"Input coordinates: lat={destination_lat}, lon={destination_lon}")
    
#     # Get multiple nearest airports
#     nearest_airports = find_multiple_nearest_airports(destination_lat, destination_lon, airports_df)
    
#     if not nearest_airports:
#         st.warning("No airports found within reasonable distance.")
#         return None
        
#     for airport in nearest_airports:
#         print(f"\nTrying airport: {airport['name']} ({airport['iata']}) - {airport['distance']:.2f} km away")
        
#         url = "https://www.searchapi.io/api/v1/search"
#         params = {
#             "engine": "google_flights",
#             "flight_type": "one_way",
#             "departure_id": departure_airport_iata,  # Use detected departure airport
#             "arrival_id": airport['iata'],
#             "outbound_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
#             "api_key": "UdxjESojjvM58CeEVvxTwr2S"
#         }
        
#         try:
#             response = requests.get(url, params=params)
#             response.raise_for_status()
#             flights_data = response.json()
            
#             if flights_data and 'best_flights' in flights_data and flights_data['best_flights']:
#                 print(f"Found flights for {airport['iata']}")
#                 flights_data['airport_info'] = {
#                     'name': airport['name'],
#                     'iata': airport['iata'],
#                     'distance': airport['distance']
#                 }
#                 return flights_data
#             else:
#                 print(f"No flights found for {airport['iata']}")
                
#         except requests.exceptions.RequestException as e:
#             print(f"Error in API request for {airport['iata']}: {str(e)}")
#             continue
    
#     st.warning("No flights found from any nearby airports.")
#     return None


# def get_directions(api_key, origin_city, destination_city, mode='driving'):
#     """Get directions from Google Maps API using city names."""
#     url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin_city}&destination={destination_city}&mode={mode}&key={api_key}"
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         st.error(f"Error fetching directions: {str(e)}")
#         return None

# def plot_route_on_map(directions_data, mode):
#     """Create a Folium map with the route plotted."""
#     if not directions_data or 'routes' not in directions_data or not directions_data['routes']:
#         return None

#     try:
#         # Extract route points from directions
#         route = directions_data['routes'][0]['overview_polyline']['points']
#         coordinates = decode(route)
        
#         # Create a map centered on the origin with reduced zoom
#         start_location = coordinates[0]
#         m = folium.Map(
#             location=start_location, 
#             zoom_start=8,  # Reduced zoom level
#             prefer_canvas=True  # Use canvas renderer for better performance
#         )
        
#         # Add route as a polyline with simplified styling
#         color = "blue" if mode == "driving" else "green"
#         folium.PolyLine(
#             coordinates, 
#             color=color, 
#             weight=3,  # Reduced line weight
#             opacity=0.6  # Reduced opacity
#         ).add_to(m)
        
#         # Add simplified markers
#         folium.Marker(
#             coordinates[0], 
#             tooltip="Airport",
#             icon=folium.Icon(color="green", icon="plane", prefix='fa', size=(20, 20))
#         ).add_to(m)
        
#         folium.Marker(
#             coordinates[-1], 
#             tooltip="Hotel",
#             icon=folium.Icon(color="red", icon="hotel", prefix='fa', size=(20, 20))
#         ).add_to(m)
        
#         # Fit bounds to show the entire route
#         m.fit_bounds([coordinates[0], coordinates[-1]])
        
#         return m
#     except Exception as e:
#         st.error(f"Error creating map: {str(e)}")
#         return None

# def display_flight_options(flights_data):
#     """Display flight options using Streamlit components with airline logos and INR prices."""
#     if not flights_data or 'best_flights' not in flights_data:
#         st.warning("No flight information available.")
#         return
    
#     st.subheader("Available Flights")
    
#     # Display airport information if available
#     if 'airport_info' in flights_data:
#         airport_info = flights_data['airport_info']
#         st.info(f"Showing flights to {airport_info['name']} ({airport_info['iata']}) - {airport_info['distance']:.1f} km from destination")
    
#     # USD to INR conversion rate
#     USD_TO_INR = 84.5
    
#     for best_flight in flights_data['best_flights'][:2]:  # Display top flight option
#         total_duration = best_flight.get('total_duration', 'N/A')
#         price_usd = best_flight.get('price', 0)
#         price_inr = price_usd * USD_TO_INR
        
#         # Create expander header with price in both currencies
#         expander_header = f"₹{price_inr:,.2f} (${price_usd}) - ⏱️ {total_duration} mins"
        
#         with st.expander(expander_header):
#             # Display each flight segment in the itinerary
#             for i, flight in enumerate(best_flight['flights'], 1):
#                 # Create columns for airline info and flight details
#                 col1, col2 = st.columns([1, 3])
                
#                 with col1:
#                     # Display airline logo if available
#                     if 'airline_logo' in flight:
#                         st.image(flight['airline_logo'], width=70)
#                     st.write(f"**{flight.get('airline', 'N/A')}**")
#                     st.write(f"Flight {flight.get('flight_number', 'N/A')}")
                
#                 with col2:
#                     # Create sub-columns for departure and arrival
#                     dep_col, arr_col = st.columns(2)
                    
#                     with dep_col:
#                         st.write("**Departure:**")
#                         dep = flight['departure_airport']
#                         st.write(f"🛫 {dep['name']} ({dep['id']})")
#                         st.write(f"📅 {dep['date']}")
#                         st.write(f"🕒 {dep['time']}")
                    
#                     with arr_col:
#                         st.write("**Arrival:**")
#                         arr = flight['arrival_airport']
#                         st.write(f"🛬 {arr['name']} ({arr['id']})")
#                         st.write(f"📅 {arr['date']}")
#                         st.write(f"🕒 {arr['time']}")
                
#                 # Flight details section
#                 st.write("**Flight Details:**")
#                 st.write(f"✈️ Aircraft: {flight.get('airplane', 'N/A')}")
#                 st.write(f"⏱️ Duration: {flight.get('duration', 'N/A')} mins")
                
#                 # Display any additional flight information from extensions
#                 if 'detected_extensions' in flight:
#                     ext = flight['detected_extensions']
#                     if 'seat_type' in ext:
#                         st.write(f"💺 Seat: {ext['seat_type']}")
#                     if 'legroom_long' in ext:
#                         st.write(f"🦵 Legroom: {ext['legroom_long']}")
#                     if 'carbon_emission' in ext:
#                         st.write(f"🌱 Carbon emission: {ext['carbon_emission']} kg")
                
#                 # Display layover information
#                 if i < len(best_flight['flights']) and 'layovers' in best_flight:
#                     layover = best_flight['layovers'][i-1]
#                     st.markdown("---")
#                     st.write(f"🕒 **Layover:** {layover.get('duration', 'N/A')} mins at {layover.get('name', 'N/A')}")
#                     st.markdown("---")

# def display_route_information(flights_data, hotels):
#     """Display route information from airport to hotel."""
#     if not hotels or len(hotels) == 0 or not flights_data:
#         return
        
#     # Add custom CSS to control map container height
#     st.markdown("""
#         <style>
#         .stfolium-container {
#             height: 420px !important;
#             margin-bottom: 1rem;
#         }
#         iframe {
#             height: 420px !important;
#         }
#         </style>
#     """, unsafe_allow_html=True)
        
#     google_maps_api_key = "AIzaSyA5QKrsVtwQa30vzOgZwo_p1ak5tyzgyE0"
    
#     st.divider()
#     st.subheader("🗺️ Ground Transportation to Destination")
    
#     # Get arrival city and destination city
#     arrival_city = flights_data['airports'][0]['arrival'][0]['city']
#     destination_city = hotels[0].get('address_obj', {}).get('city', '')
    
#     if arrival_city and destination_city:
#         # Display route information for both driving and transit
#         modes = ['driving', 'transit']
#         mode_icons = {'driving': '🚗', 'transit': '🚌'}
        
#         for mode in modes:
#             st.write(f"**{mode_icons[mode]} {mode.title()} Option:**")
            
#             directions_data = get_directions(google_maps_api_key, arrival_city, destination_city, mode)
            
#             if directions_data and 'routes' in directions_data and directions_data['routes']:
#                 leg = directions_data['routes'][0]['legs'][0]
#                 st.write(f"📏 Distance: {leg['distance']['text']}")
#                 st.write(f"⏱️ Duration: {leg['duration']['text']}")
                
#                 route_map = plot_route_on_map(directions_data, mode)
#                 if route_map:
#                     st_folium(
#                         route_map,
#                         width=704,  # Match the container width you observed
#                         height=420,  # Match the map height you observed
#                         returned_objects=[],
#                         use_container_width=False
#                     )
#             else:
#                 st.warning(f"No {mode} route available")
#     else:
#         st.warning("Could not determine city information for route mapping")

# def display_weather_forecast(forecasts):
#     """Display weather forecast using Streamlit components."""
#     if not forecasts:
#         return
    
#     st.divider()
#     st.subheader("5-Day Weather Forecast At the Destination")
#     cols = st.columns(len(forecasts))
    
#     for idx, forecast in enumerate(forecasts):
#         with cols[idx]:
#             st.write(f"**{forecast['date']}**")
#             icon_url = f"http://openweathermap.org/img/wn/{forecast['icon']}@2x.png"
#             st.image(icon_url, width=50)
#             st.write(f"{forecast['temp']}°C")
#             st.write(f"*{forecast['description'].capitalize()}*")


# def create_daily_itinerary(destination_details, duration_days):
#     """
#     Create a day-by-day itinerary from destination details.
    
#     Args:
#         destination_details (dict): Dictionary containing details for each category
#         duration_days (int): Number of days for the trip
    
#     Returns:
#         list: List of daily itineraries
#     """
#     # Ensure we have enough places for each day
#     required_places = duration_days
#     for category in ['hotels', 'attractions', 'restaurants']:
#         if category in destination_details:
#             while len(destination_details[category]) < required_places:
#                 # Duplicate last item if we don't have enough places
#                 if destination_details[category]:
#                     destination_details[category].append(destination_details[category][-1])
    
#     # Create daily itineraries
#     daily_itineraries = []
    
#     for day in range(duration_days):
#         daily_itinerary = {
#             'day': day + 1,
#             'hotel': destination_details.get('hotels', [])[day] if destination_details.get('hotels') else None,
#             'attraction': destination_details.get('attractions', [])[day] if destination_details.get('attractions') else None,
#             'restaurant': destination_details.get('restaurants', [])[day] if destination_details.get('restaurants') else None,
#             'geo_info': destination_details.get('geos', [None])[0]  # Use same geo info for all days
#         }
#         daily_itineraries.append(daily_itinerary)
    
#     return daily_itineraries

# def display_daily_itineraries(daily_itineraries):
#     """
#     Display comprehensive day-by-day itinerary in Streamlit with detailed information.
    
#     Args:
#         daily_itineraries (list): List of daily itinerary dictionaries
#     """
#     # Define price level mapping
#     price_level_map = {
#         "$$$$": "Very Expensive",
#         "$$$": "Expensive",
#         "$$": "Reasonable Stay",
#         "$": "Affordable",
#     }
    
#     st.divider()
#     st.subheader("📅 Day-by-Day Itinerary")
    
#     for itinerary in daily_itineraries:
#         day_num = itinerary['day']
        
#         with st.expander(f"Day {day_num}"):
#             # Display Hotel Information
#             if itinerary['hotel']:
#                 st.markdown("### 🏨 Accommodation")
#                 hotel = itinerary['hotel']
                
#                 # Display hotel photos
#                 if hotel['photos'] and len(hotel['photos']) > 0:
#                     cols = st.columns(min(3, len(hotel['photos'])))
#                     for idx, photo in enumerate(hotel['photos'][:3]):
#                         try:
#                             photo_url = photo if isinstance(photo, str) else photo.get('url', '')
#                             cols[idx].image(photo_url, use_container_width=True)
#                         except Exception as e:
#                             st.error(f"Error displaying hotel photo: {str(e)}")
                
#                 st.write(f"**{hotel['name']}**")
#                 st.write(f"**Description:** {hotel['description']}")
#                 st.write(f"**Phone:** {hotel['phone']}")
                
#                 if hotel['address_obj']:
#                     address = hotel['address_obj']
#                     st.write("**Address:**")
#                     st.write(f"{address.get('street1', '')}")
#                     st.write(f"{address.get('city', '')}, {address.get('state', '')} {address.get('postalcode', '')}")
#                     st.write(f"{address.get('country', '')}")
                
#                 # Display price level with description
#                 price_level = hotel['price_level']
#                 if price_level in price_level_map:
#                     st.write(f"**Price Level:** {price_level} - {price_level_map[price_level]}")
#                 else:
#                     st.write(f"**Price Level:** {price_level}")
                
#                 if hotel['amenities']:
#                     st.write("**Amenities:**")
#                     st.write(", ".join(hotel['amenities']))
                
#                 if hotel['reviews']:
#                     st.write("**Recent Reviews:**")
#                     for review in hotel['reviews'][:3]:
#                         if isinstance(review, dict):
#                             st.markdown(f"⭐ **{review.get('rating', 'N/A')}/5** - {review.get('text', 'No review text')}")
#                         else:
#                             st.markdown(f"⭐ {review}")
                
#                 st.write(f"[View on TripAdvisor]({hotel['web_url']})")
            
#             # Display Attraction Information
#             if itinerary['attraction']:
#                 st.markdown("### 🎯 Activity")
#                 attraction = itinerary['attraction']
                
#                 # Display attraction photos
#                 if attraction['photos'] and len(attraction['photos']) > 0:
#                     cols = st.columns(min(3, len(attraction['photos'])))
#                     for idx, photo in enumerate(attraction['photos'][:3]):
#                         try:
#                             photo_url = photo if isinstance(photo, str) else photo.get('url', '')
#                             cols[idx].image(photo_url, use_container_width=True)
#                         except Exception as e:
#                             st.error(f"Error displaying attraction photo: {str(e)}")
                
#                 st.write(f"**{attraction['name']}**")
#                 st.write(f"**Description:** {attraction['description']}")
#                 st.write(f"**Phone:** {attraction['phone']}")
                
#                 if attraction['address_obj']:
#                     address = attraction['address_obj']
#                     st.write("**Address:**")
#                     st.write(f"{address.get('street1', '')}")
#                     st.write(f"{address.get('city', '')}, {address.get('state', '')} {address.get('postalcode', '')}")
#                     st.write(f"{address.get('country', '')}")
                
#                 if attraction.get('attraction_types'):
#                     st.write("**Attraction Types:**")
#                     st.write(", ".join([t.get('name', '') for t in attraction['attraction_types']]))
#                 st.write(f"**Rating:** {attraction.get('rating', 'N/A')}")
#                 # st.write(f"**Ranking:** {attraction.get('ranking', 'N/A')}")
                
#                 if attraction['reviews']:
#                     st.write("**Recent Reviews:**")
#                     for review in attraction['reviews'][:3]:
#                         if isinstance(review, dict):
#                             st.markdown(f"⭐ **{review.get('rating', 'N/A')}/5** - {review.get('text', 'No review text')}")
#                         else:
#                             st.markdown(f"⭐ {review}")
                
#                 st.write(f"[View on TripAdvisor]({attraction['web_url']})")
            
#             # Display Restaurant Information
#             if itinerary['restaurant']:
#                 st.markdown("### 🍽️ Dining")
#                 restaurant = itinerary['restaurant']
                
#                 # Display restaurant photos
#                 if restaurant['photos'] and len(restaurant['photos']) > 0:
#                     cols = st.columns(min(3, len(restaurant['photos'])))
#                     for idx, photo in enumerate(restaurant['photos'][:3]):
#                         try:
#                             photo_url = photo if isinstance(photo, str) else photo.get('url', '')
#                             cols[idx].image(photo_url, use_container_width=True)
#                         except Exception as e:
#                             st.error(f"Error displaying restaurant photo: {str(e)}")
                
#                 st.write(f"**{restaurant['name']}**")
#                 st.write(f"**Description:** {restaurant['description']}")
#                 st.write(f"**Phone:** {restaurant['phone']}")
                
#                 if restaurant['address_obj']:
#                     address = restaurant['address_obj']
#                     st.write("**Address:**")
#                     st.write(f"{address.get('street1', '')}")
#                     st.write(f"{address.get('city', '')}, {address.get('state', '')} {address.get('postalcode', '')}")
#                     st.write(f"{address.get('country', '')}")
                
#                 if restaurant.get('cuisine'):
#                     st.write("**Cuisine:**")
#                     st.write(", ".join([c.get('name', '') for c in restaurant['cuisine']]))
#                 st.write(f"**Price Range:** {restaurant.get('price_range', 'N/A')}")
                
#                 if restaurant.get('dietary_restrictions'):
#                     st.write("**Dietary Options:**")
#                     st.write(", ".join([d.get('name', '') for d in restaurant['dietary_restrictions']]))
                
#                 if restaurant['reviews']:
#                     st.write("**Recent Reviews:**")
#                     for review in restaurant['reviews'][:3]:
#                         if isinstance(review, dict):
#                             st.markdown(f"⭐ **{review.get('rating', 'N/A')}/5** - {review.get('text', 'No review text')}")
#                         else:
#                             st.markdown(f"⭐ {review}")
                
#                 st.write(f"[View on TripAdvisor]({restaurant['web_url']})")
            
#             # # Display Location/Geographic Information once per day
#             # if itinerary['geo_info']:
#             #     st.markdown("### 📍 Location Information")
#             #     geo = itinerary['geo_info']
                
#             #     st.write(f"**{geo['name']}**")
#             #     st.write(f"**Description:** {geo['description']}")
#             #     if geo.get('geo_type'):
#             #         st.write(f"**Location Type:** {geo['geo_type']}")
#             #     if geo.get('timezone'):
#             #         st.write(f"**Timezone:** {geo['timezone']}")
                
#             #     if geo['reviews']:
#             #         st.write("**Area Reviews:**")
#             #         for review in geo['reviews'][:3]:
#             #             if isinstance(review, dict):
#             #                 st.markdown(f"⭐ **{review.get('rating', 'N/A')}/5** - {review.get('text', 'No review text')}")
#             #             else:
#             #                 st.markdown(f"⭐ {review}")
                
#             #     st.write(f"[View Area on TripAdvisor]({geo['web_url']})")

# def get_destination_details(destination, duration_days):
#     """
#     Modified version to fetch appropriate number of places based on trip duration.
#     """
#     base_url = "https://api.content.tripadvisor.com/api/v1"
#     tripadvisor_api_key = "C5104F92E6354A079E0C6E424B3B1F06"
#     weather_api_key = "a73d2e9d5872429030175d780367cf35"
    
#     categories = ["hotels", "attractions", "restaurants", "geos"]
    
#     try:
#         destination_details = {}
#         weather_forecast = None
#         first_location_coords = None

#         for category in categories:
#             # Search for locations
#             search_url = f"{base_url}/location/search"
#             search_params = {
#                 "key": tripadvisor_api_key,
#                 "searchQuery": destination,
#                 "category": category,
#                 "language": "en"
#             }
            
#             search_response = requests.get(
#                 search_url,
#                 params=search_params,
#                 headers={"accept": "application/json"}
#             )
#             search_response.raise_for_status()
#             search_data = search_response.json()
            
#             # Extract location IDs
#             location_ids = [
#                 item.get("location_id")
#                 for item in search_data.get("data", [])
#             ]
            
#             # Determine how many places to fetch based on category and duration
#             if category == "geos":
#                 places_to_fetch = 1  # We only need one geo entry
#             else:
#                 places_to_fetch = min(duration_days, len(location_ids))
            
#             category_details = []
            
#             # Fetch details for each location
#             for location_id in location_ids[:places_to_fetch]:
#                 details_url = f"{base_url}/location/{location_id}/details"
#                 details_params = {
#                     "key": tripadvisor_api_key,
#                     "language": "en",
#                     "currency": "USD"
#                 }
                
#                 details_response = requests.get(
#                     details_url,
#                     params=details_params,
#                     headers={"accept": "application/json"}
#                 )
#                 details_response.raise_for_status()
#                 location_data = details_response.json()
                
#                 # Extract coordinates
#                 latitude = location_data.get("latitude")
#                 longitude = location_data.get("longitude")
                
#                 # Store first valid coordinates for weather data
#                 if first_location_coords is None and latitude and longitude:
#                     first_location_coords = (latitude, longitude)
                
#                 # Fetch photos and reviews
#                 photos = get_hotel_photos(location_id, tripadvisor_api_key)
#                 reviews = get_hotel_reviews(location_id, tripadvisor_api_key)
                
#                 # Compile location information based on category
#                 location_info = {
#                     "name": location_data.get("name", "N/A"),
#                     "description": location_data.get("description", "No description available"),
#                     "web_url": location_data.get("web_url", "N/A"),
#                     "phone": location_data.get("phone", "N/A"),
#                     "latitude": latitude,
#                     "longitude": longitude,
#                     "address_obj": location_data.get("address_obj", {}),
#                     "photos": photos,
#                     "reviews": reviews
#                 }
                
#                 # Add category-specific information
#                 if category == "hotels":
#                     location_info.update({
#                         "price_level": location_data.get("price_level", "N/A"),
#                         "amenities": location_data.get("amenities", [])[:6]
#                     })
#                 elif category == "restaurants":
#                     location_info.update({
#                         "cuisine": location_data.get("cuisine", []),
#                         "price_range": location_data.get("price_range", "N/A"),
#                         "dietary_restrictions": location_data.get("dietary_restrictions", [])
#                     })
#                 elif category == "attractions":
#                     location_info.update({
#                         "attraction_types": location_data.get("attraction_types", []),
#                         "rating": location_data.get("rating", "N/A"),
#                         "ranking": location_data.get("ranking", "N/A")
#                     })
#                 elif category == "geos":
#                     location_info.update({
#                         "geo_type": location_data.get("geo_type", "N/A"),
#                         "ancestors": location_data.get("ancestors", []),
#                         "timezone": location_data.get("timezone", "N/A")
#                     })
                
#                 category_details.append(location_info)
            
#             destination_details[category] = category_details
        
#         # Fetch weather data if we have coordinates
#         if first_location_coords:
#             weather_forecast = get_weather_forecast(
#                 first_location_coords[0],
#                 first_location_coords[1],
#                 weather_api_key
#             )
        
#         return destination_details, weather_forecast
    
#     except requests.exceptions.RequestException as e:
#         st.error(f"Error fetching destination data: {str(e)}")
#         return {}, None

# def display_destination_details(destination_details):
#     """
#     Display the fetched destination details in the Streamlit app.
    
#     Args:
#         destination_details (dict): Dictionary containing details for each category
#     """
#     for category, items in destination_details.items():
#         if items:
#             st.subheader(f"{category.title()}")
            
#             for item in items:
#                 with st.expander(f"{item['name']}"):
#                     # Display photos first if available
#                     if item['photos'] and len(item['photos']) > 0:
#                         # st.write("**Photos:**")
#                         # Check the structure of the first photo to determine how to handle it
#                         if isinstance(item['photos'][0], str):
#                             # If photos are direct URLs
#                             cols = st.columns(min(3, len(item['photos'])))
#                             for idx, photo_url in enumerate(item['photos'][:3]):
#                                 try:
#                                     cols[idx].image(photo_url, use_container_width=True)
#                                 except Exception as e:
#                                     st.error(f"Error displaying photo: {str(e)}")
#                         else:
#                             # If photos are objects with URLs
#                             cols = st.columns(min(3, len(item['photos'])))
#                             for idx, photo in enumerate(item['photos'][:3]):
#                                 try:
#                                     photo_url = photo.get('url') if isinstance(photo, dict) else str(photo)
#                                     cols[idx].image(photo_url, use_container_width=True)
#                                 except Exception as e:
#                                     st.error(f"Error displaying photo: {str(e)}")

#                     st.write(f"**Description:** {item['description']}")
#                     st.write(f"**Phone:** {item['phone']}")
                    
#                     # Display address if available
#                     if item['address_obj']:
#                         address = item['address_obj']
#                         st.write("**Address:**")
#                         st.write(f"{address.get('street1', '')}")
#                         st.write(f"{address.get('city', '')}, {address.get('state', '')} {address.get('postalcode', '')}")
#                         st.write(f"{address.get('country', '')}")
                    
#                     # Display category-specific information
#                     if category == "hotels":
#                         st.write(f"**Price Level:** {item['price_level']}")
#                         if item['amenities']:
#                             st.write("**Amenities:**")
#                             st.write(", ".join(item['amenities']))
                    
#                     elif category == "restaurants":
#                         if item.get('cuisine'):
#                             st.write("**Cuisine:**")
#                             st.write(", ".join([c.get('name', '') for c in item['cuisine']]))
#                         st.write(f"**Price Range:** {item.get('price_range', 'N/A')}")
#                         if item.get('dietary_restrictions'):
#                             st.write("**Dietary Options:**")
#                             st.write(", ".join([d.get('name', '') for d in item['dietary_restrictions']]))
                    
#                     elif category == "attractions":
#                         if item.get('attraction_types'):
#                             st.write("**Attraction Types:**")
#                             st.write(", ".join([t.get('name', '') for t in item['attraction_types']]))
#                         st.write(f"**Rating:** {item.get('rating', 'N/A')}")
#                         st.write(f"**Ranking:** {item.get('ranking', 'N/A')}")
                    
#                     elif category == "geos":
#                         st.write(f"**Type:** {item.get('geo_type', 'N/A')}")
#                         st.write(f"**Timezone:** {item.get('timezone', 'N/A')}")
                    
#                     # Display reviews if available
#                     if item['reviews']:
#                         st.write("**Recent Reviews:**")
#                         for review in item['reviews'][:3]:
#                             if isinstance(review, dict):
#                                 st.markdown(f"⭐ **{review.get('rating', 'N/A')}/5** - {review.get('text', 'No review text')}")
#                             else:
#                                 st.markdown(f"⭐ {review}")
                    
#                     st.write(f"[View on TripAdvisor]({item['web_url']})")

# def get_hotel_photos(location_id, api_key):
#     """
#     Fetch photos for a specific location from TripAdvisor API.
    
#     Args:
#         location_id (str): TripAdvisor location ID
#         api_key (str): TripAdvisor API key
    
#     Returns:
#         list: List of photo URLs or photo objects
#     """
#     try:
#         base_url = "https://api.content.tripadvisor.com/api/v1"
#         photos_url = f"{base_url}/location/{location_id}/photos"
#         photos_params = {
#             "key": api_key,
#             "language": "en"
#         }
        
#         response = requests.get(
#             photos_url,
#             params=photos_params,
#             headers={"accept": "application/json"}
#         )
#         response.raise_for_status()
        
#         photos_data = response.json()
#         photos = []
        
#         # Extract photo URLs from the response
#         if isinstance(photos_data, dict) and 'data' in photos_data:
#             for photo in photos_data['data'][:3]:  # Limit to 3 photos
#                 if isinstance(photo, dict):
#                     # Extract the largest available image URL
#                     images = photo.get('images', {})
#                     if images:
#                         # Try to get the large image, fall back to original if not available
#                         photo_url = (images.get('large', {}) or images.get('original', {})).get('url')
#                         if photo_url:
#                             photos.append(photo_url)
        
#         return photos
    
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching photos: {str(e)}")
#         return []


# def get_price_level_description(price_level):
#     """Convert price level symbols to descriptive text."""
#     price_descriptions = {
#         "$$$$": "Very Costly",
#         "$$$": "Costly",
#         "$$": "Affordable",
#         "$": "Great Bargain!!"
#     }
#     return price_descriptions.get(price_level, price_level)

# def parse_travel_input(text):
#     if not text:
#         return {"error": "Please enter your travel plans."}
    
#     try:
#         destination = extract_destination(text)
#         budget = extract_budget(text)
#         duration = extract_duration(text)
#         interests = extract_interests(text)
        
#         return {
#             "destination": destination,
#             "budget": budget,
#             "duration": duration,
#             "interests": interests
#         }
#     except Exception as e:
#         return {"error": f"Error processing input: {str(e)}"}

# def main():
#     st.title("Travel Itinerary Generator and Assistant")
    
#     # Load airports data
#     try:
#         airports_df = pd.read_csv('airports.csv')
#         airports_df['lat'] = pd.to_numeric(airports_df['lat'], errors='coerce')
#         airports_df['lon'] = pd.to_numeric(airports_df['lon'], errors='coerce')
#         airports_df = airports_df.dropna(subset=['lat', 'lon', 'iata'])
#     except Exception as e:
#         st.error(f"Error loading airports data: {e}")
#         return

#     st.write("Describe your travel plans in one sentence, and I'll generate a personalized itinerary.")

#     user_input = st.text_area(
#         "Enter your travel plans:",
#         placeholder="e.g., I want to travel to the Maldives with my wife for a romantic vacation with a budget of $10,000 for 3 nights and 4 days."
#     )

#     if st.button("Generate Itinerary"):
#         if user_input:
#             # First, get location info
#             departure_airport_iata = "BOM"  # Default to Mumbai
#             user_ip = get_user_ip()
#             location_info = {}
            
#             if user_ip:
#                 location = get_user_location(user_ip)
#                 if location:
#                     location_info['location'] = f"📍 Detected your location: {location['city']}, {location['region']}, {location['country']}"
                    
#                     nearest_airport = find_nearest_airport(location['latitude'], location['longitude'], airports_df)
#                     if nearest_airport:
#                         departure_airport_iata = nearest_airport['iata']
#                         location_info['airport'] = f"✈️ Nearest Airport: {nearest_airport['name']} ({departure_airport_iata})"
#                     else:
#                         location_info['airport'] = "Using Mumbai (BOM) as default departure airport."
#                 else:
#                     location_info['airport'] = "Unable to determine your location. Using Mumbai (BOM) as default departure airport."
#             else:
#                 location_info['airport'] = "Unable to retrieve your IP address. Using Mumbai (BOM) as default departure airport."

#             # Parse and validate travel input
#             travel_info = parse_travel_input(user_input)
            
#             if "error" in travel_info:
#                 st.warning(travel_info["error"])
#                 return
#             elif not travel_info["destination"]:
#                 st.warning("Could not extract destination. Please include it in your prompt.")
#                 return
#             elif not travel_info["budget"]:
#                 st.warning("Could not extract budget. Please include it in your prompt.")
#                 return
#             elif not travel_info["duration"]["days"]:
#                 st.warning("Could not extract duration. Please include it in your prompt.")
#                 return

#             # Display location info
#             st.write(location_info.get('location', ''))
#             st.write(location_info.get('airport', ''))
            
#             # Display success message and extracted info
#             st.success("Information extracted successfully!")
#             st.write("**Extracted Information**:")
#             st.write(f"**Destination**: {travel_info['destination']}")
#             st.write(f"**Budget**: {travel_info['budget']['currency']} {travel_info['budget']['amount']:,}")
#             st.write(f"**Duration**: {travel_info['duration']['nights']} nights and {travel_info['duration']['days']} days")
#             if travel_info['duration']['start_date']:
#                 st.write(f"**Dates**: {travel_info['duration']['start_date']} to {travel_info['duration']['end_date']}")
#             st.write(f"**Interests**: {', '.join(travel_info['interests']) if travel_info['interests'] else 'Not specified'}")

#             # Now show spinner while fetching trip details
#             with st.spinner("Generating your personalized travel itinerary..."):
#                 # Fetch all required data with duration
#                 destination_details, weather_forecast = get_destination_details(
#                     travel_info['destination'], 
#                     travel_info['duration']['days']
#                 )
                
#                 # Get coordinates for flight search
#                 destination_coords = None
#                 flights_data = None
#                 if destination_details.get('hotels') and len(destination_details['hotels']) > 0:
#                     first_hotel = destination_details['hotels'][0]
#                     if first_hotel['latitude'] and first_hotel['longitude']:
#                         destination_coords = {
#                             'latitude': first_hotel['latitude'],
#                             'longitude': first_hotel['longitude']
#                         }
#                         flights_data = get_flight_options_with_fallback(
#                             destination_coords['latitude'],
#                             destination_coords['longitude'],
#                             airports_df,
#                             departure_airport_iata
#                         )

#             # After spinner, display trip information
#             st.markdown("<h1 style='text-align: center;'>YOUR TRIP INFORMATION</h1>", unsafe_allow_html=True)
            
#             # Display weather information
#             if weather_forecast:
#                 display_weather_forecast(weather_forecast)
#                 st.divider()
            
#             # Display flight options if available
#             if flights_data:
#                 display_flight_options(flights_data)
#                 display_route_information(flights_data, destination_details.get('hotels', []))
#             else:
#                 st.warning("Could not find flight information for the destination.")
            
#             # Create and display daily itineraries
#             if destination_details:
#                 daily_itineraries = create_daily_itinerary(
#                     destination_details, 
#                     travel_info['duration']['days']
#                 )
#                 display_daily_itineraries(daily_itineraries)
#             else:
#                 st.warning("No destination information found.")

# if __name__ == "__main__":
#     main()






import streamlit as st
import requests
import re
from datetime import datetime, timedelta
import pandas as pd
from math import radians, sin, cos, sqrt, atan2
from streamlit_folium import st_folium
import folium
from polyline import decode  # Install via `pip install polyline`
import streamlit as st
from typing import Optional, Dict, Any

def extract_destination(text):
    # Common patterns for destination extraction
    patterns = [
        r"(?:travel|go|flying|heading|visiting|trip) (?:to|in) ([A-Za-z\s,]+?)(?=\s*(?:for|with|on|and|$))",
        r"(?:visiting|explore) ([A-Za-z\s,]+?)(?=\s*(?:for|with|on|and|$))",
        r"(?:vacation|holiday) (?:in|at) ([A-Za-z\s,]+?)(?=\s*(?:for|with|on|and|$))"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            return match.group(1).strip().title()
    return None

def extract_duration(text):
    nights, days = None, None
    
    # Extract nights
    night_match = re.search(r'(\d+)\s*nights?', text.lower())
    if night_match:
        nights = int(night_match.group(1))
        days = nights + 1
    
    # Extract days
    day_match = re.search(r'(\d+)\s*days?', text.lower())
    if day_match:
        days = int(day_match.group(1))
        if nights is None:
            nights = days - 1
    
    # Extract date range (DD/MM/YY or DD-MM-YY)
    dates = re.findall(r'(\d{2}[-/]\d{2}[-/]\d{2})', text)
    start_date = end_date = None
    
    if len(dates) >= 2:
        try:
            start_date = datetime.strptime(dates[0].replace('-', '/'), "%d/%m/%y")
            end_date = datetime.strptime(dates[1].replace('-', '/'), "%d/%m/%y")
            days = (end_date - start_date).days
            nights = days - 1
        except ValueError:
            pass
    
    # Handle week
    if 'week' in text.lower():
        days = 7
        nights = 6
    
    return {
        "nights": nights,
        "days": days,
        "start_date": start_date.strftime("%d/%m/%y") if start_date else None,
        "end_date": end_date.strftime("%d/%m/%y") if end_date else None
    }

def extract_budget(text):
    # Handle currency symbols
    budget_patterns = [
        r'(?:budget of |cost of |spend |price |cost )?[\$₹](\d+[,\d]*)',
        r'(\d+[,\d]*)\s*(?:dollars|rupees)',
    ]
    
    for pattern in budget_patterns:
        match = re.search(pattern, text.lower())
        if match:
            amount = int(match.group(1).replace(',', ''))
            # Determine currency
            if '$' in text or 'dollars' in text.lower():
                currency = "USD"
            elif '₹' in text or 'rupees' in text.lower():
                currency = "INR"
            else:
                currency = "USD"  # Default currency
            return {"amount": amount, "currency": currency}
    return None

def extract_interests(text):
    interest_keywords = {
        'romantic': ['romantic', 'honeymoon', 'couple'],
        'adventure': ['adventure', 'exciting', 'thrill', 'trek', 'fun'],
        'nature': ['nature', 'wildlife', 'outdoor', 'forest', 'mountain', 'beach'],
        'culture': ['culture', 'history', 'museum', 'heritage', 'art'],
        'food': ['food', 'cuisine', 'dining', 'gastronomy', 'culinary'],
        'relaxation': ['relaxation', 'peaceful', 'quiet', 'spa', 'wellness'],
        'shopping': ['shopping', 'market', 'mall'],
        'nightlife': ['party', 'club', 'nightlife', 'bar'],
        'family': ['family', 'kids', 'children'],
        'luxury': ['luxury', 'premium', 'high-end', 'exclusive']
    }
    
    found_interests = set()
    text_lower = text.lower()
    
    for category, keywords in interest_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            found_interests.add(category.title())
    
    return list(found_interests)

def get_hotel_photos(location_id, api_key):
    """Fetch hotel photos from TripAdvisor API."""
    url = f"https://api.content.tripadvisor.com/api/v1/location/{location_id}/photos"
    params = {
        "key": api_key,
        "language": "en"
    }
    headers = {"accept": "application/json"}
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        photos_data = response.json()
        
        # Extract photo URLs from the response
        photos = []
        for photo in photos_data.get("data", [])[:3]:  # Limit to first 3 photos
            if photo.get("images", {}).get("large", {}).get("url"):
                photos.append(photo["images"]["large"]["url"])
        return photos
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching photos: {str(e)}")
        return []

def get_hotel_reviews(location_id, api_key):
    """Fetch hotel reviews from TripAdvisor API."""
    url = f"https://api.content.tripadvisor.com/api/v1/location/{location_id}/reviews"
    params = {
        "key": api_key,
        "language": "en"
    }
    headers = {"accept": "application/json"}
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        reviews_data = response.json()
        
        # Extract relevant review information
        reviews = []
        for review in reviews_data.get("data", [])[:3]:  # Limit to first 3 reviews
            review_info = {
                "title": review.get("title", "No Title"),
                "text": review.get("text", "No Review Text"),
                "rating": review.get("rating", "N/A"),
                "published_date": review.get("published_date", "N/A"),
                "username": review.get("user", {}).get("username", "Anonymous")
            }
            reviews.append(review_info)
        return reviews
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching reviews: {str(e)}")
        return []

def get_weather_forecast(latitude, longitude, api_key):
    """Fetch weather forecast from OpenWeatherMap API."""
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            forecast_data = response.json()
            # Get the next 5 days forecast (data points every 3 hours, so we'll take one per day)
            daily_forecasts = []
            seen_dates = set()
            
            for item in forecast_data['list']:
                date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
                if date not in seen_dates:
                    seen_dates.add(date)
                    daily_forecasts.append({
                        'date': datetime.fromtimestamp(item['dt']).strftime('%d %b'),
                        'temp': round(item['main']['temp']),
                        'description': item['weather'][0]['description'],
                        'icon': item['weather'][0]['icon']
                    })
                if len(daily_forecasts) >= 5:
                    break
            
            return daily_forecasts
    except Exception as e:
        st.error(f"Error fetching weather data: {str(e)}")
    return None

# New functions for user location
def get_user_ip():
    """Get user's IP address."""
    try:
        response = requests.get("https://api.ipify.org?format=json")
        if response.status_code == 200:
            return response.json()['ip']
        return None
    except Exception as e:
        print(f"Error getting IP: {e}")
        return None

def get_user_location(ip_address):
    """Get location information from IP address."""
    try:
        url = f"http://ip-api.com/json/{ip_address}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                return {
                    "city": data.get('city'),
                    "region": data.get('regionName'),
                    "country": data.get('country'),
                    "latitude": data.get('lat'),
                    "longitude": data.get('lon')
                }
        return None
    except Exception as e:
        print(f"Error getting location: {e}")
        return None
    
def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points using Haversine formula."""
    try:
        # Convert string inputs to float if necessary
        lat1 = float(lat1)
        lon1 = float(lon1)
        lat2 = float(lat2)
        lon2 = float(lon2)
        
        R = 6371  # Earth's radius in kilometers

        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = R * c

        return distance
    except (ValueError, TypeError) as e:
        print(f"Error calculating distance: {e}")
        return float('inf')  # Return infinity for invalid coordinates

def find_multiple_nearest_airports(latitude, longitude, airports_df, max_airports=5, max_distance=300):
    """Find multiple nearest airports within a reasonable distance."""
    try:
        # Convert coordinates to float
        latitude = float(latitude)
        longitude = float(longitude)
        
        # Ensure lat and lon columns are float type
        airports_df['lat'] = pd.to_numeric(airports_df['lat'], errors='coerce')
        airports_df['lon'] = pd.to_numeric(airports_df['lon'], errors='coerce')
        
        # Drop rows with invalid coordinates
        airports_df = airports_df.dropna(subset=['lat', 'lon', 'iata'])
        
        # Calculate distances for all airports
        airports_df['distance'] = airports_df.apply(
            lambda row: calculate_distance(
                latitude, longitude,
                row['lat'], row['lon']
            ),
            axis=1
        )
        
        # Get nearest airports within maximum distance
        nearest_airports = airports_df[airports_df['distance'] <= max_distance].nsmallest(max_airports, 'distance')
        
        if nearest_airports.empty:
            print(f"No airports found within {max_distance} km")
            return []
            
        airports_list = []
        for _, airport in nearest_airports.iterrows():
            airports_list.append({
                'name': airport['name'],
                'iata': airport['iata'],
                'distance': airport['distance'],
                'lat': airport['lat'],
                'lon': airport['lon']
            })
            
        return airports_list
    except Exception as e:
        print(f"Error finding nearest airports: {e}")
        return []

def find_nearest_airport(latitude, longitude, airports_df):
    """Find the single nearest airport to given coordinates."""
    try:
        airports = find_multiple_nearest_airports(latitude, longitude, airports_df, max_airports=1)
        return airports[0] if airports else None
    except Exception as e:
        print(f"Error finding nearest airport: {e}")
        return None
    
def get_flight_options_with_fallback(destination_lat, destination_lon, airports_df, departure_airport_iata, flight_date=None):
    """Get flight options using SearchAPI with fallback to alternative airports."""
    print("\nStarting enhanced flight search process...")
    print(f"Input coordinates: lat={destination_lat}, lon={destination_lon}")
    
    # Get multiple nearest airports
    nearest_airports = find_multiple_nearest_airports(destination_lat, destination_lon, airports_df)
    
    if not nearest_airports:
        st.warning("No airports found within reasonable distance.")
        return None
    
    # If no specific date is provided, use default (30 days from now)
    if flight_date is None:
        flight_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    
    for airport in nearest_airports:
        print(f"\nTrying airport: {airport['name']} ({airport['iata']}) - {airport['distance']:.2f} km away")
        
        url = "https://www.searchapi.io/api/v1/search"
        params = {
            "engine": "google_flights",
            "flight_type": "one_way",
            "departure_id": departure_airport_iata,
            "arrival_id": airport['iata'],
            "outbound_date": flight_date,
            "api_key": "YrMmJVXJspdPdzPaCfJqj4tq"
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            flights_data = response.json()
            
            if flights_data and 'best_flights' in flights_data and flights_data['best_flights']:
                print(f"Found flights for {airport['iata']}")
                flights_data['airport_info'] = {
                    'name': airport['name'],
                    'iata': airport['iata'],
                    'distance': airport['distance']
                }
                return flights_data
            else:
                print(f"No flights found for {airport['iata']}")
                
        except requests.exceptions.RequestException as e:
            print(f"Error in API request for {airport['iata']}: {str(e)}")
            continue
    
    return None


def get_directions(
    api_key: str,
    o_lat: float,
    o_lon: float,
    d_lat: float,
    d_lon: float,
    mode: str = 'driving'
) -> Optional[Dict[str, Any]]:
    """
    Get directions from Google Maps API using coordinates.
    
    Args:
        api_key (str): Google Maps API key
        o_lat (float): Origin latitude
        o_lon (float): Origin longitude
        d_lat (float): Destination latitude
        d_lon (float): Destination longitude
        mode (str): Transportation mode ('driving' or 'transit')
    
    Returns:
        Optional[Dict[str, Any]]: Directions data if successful, None if failed
    """
    if not all([o_lat, o_lon, d_lat, d_lon]):
        st.error("Missing coordinate information")
        return None

    url = (
        "https://maps.googleapis.com/maps/api/directions/json?"
        f"origin={o_lat},{o_lon}&destination={d_lat},{d_lon}"
        f"&mode={mode}&key={api_key}"
    )
    
    try:
        response = requests.get(url, timeout=10)  # Add timeout
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching directions: {str(e)}")
        return None

def plot_route_on_map(directions_data: Dict[str, Any], mode: str, is_return: bool = False) -> Optional[folium.Map]:
    """
    Create a Folium map with the route plotted.
    
    Args:
        directions_data (Dict[str, Any]): Directions data from Google Maps API
        mode (str): Transportation mode ('driving' or 'transit')
        is_return (bool): Whether this is a return journey (default: False)
    
    Returns:
        Optional[folium.Map]: Folium map object if successful, None if failed
    """
    if not directions_data or 'routes' not in directions_data or not directions_data['routes']:
        st.warning("No route data available for plotting")
        return None
    
    try:
        # Extract route points from directions
        route = directions_data['routes'][0]['overview_polyline']['points']
        coordinates = decode(route)
        
        if not coordinates:
            st.warning("No coordinates found in route data")
            return None
        
        # Create a map centered on the origin
        start_location = coordinates[0]
        m = folium.Map(
            location=start_location,
            zoom_start=12,
            prefer_canvas=True
        )
        
        # Style configuration based on mode
        route_styles = {
            'driving': {'color': 'blue', 'icon': 'car'},
            'transit': {'color': 'green', 'icon': 'bus'}
        }
        style = route_styles.get(mode, route_styles['driving'])
        
        # Add route polyline
        folium.PolyLine(
            coordinates,
            color=style['color'],
            weight=3,
            opacity=0.8,
            tooltip=f"{mode.title()} Route"
        ).add_to(m)
        
        # For return journey, swap the hotel and airport positions
        start_marker = {
            'location': coordinates[0],
            'tooltip': "Hotel" if is_return else "Airport",
            'icon': folium.Icon(
                color="red" if is_return else "green",
                icon="hotel" if is_return else "plane",
                prefix='fa'
            )
        }
        
        end_marker = {
            'location': coordinates[-1],
            'tooltip': "Airport" if is_return else "Hotel",
            'icon': folium.Icon(
                color="green" if is_return else "red",
                icon="plane" if is_return else "hotel",
                prefix='fa'
            )
        }
        
        # Add markers
        folium.Marker(
            start_marker['location'],
            tooltip=start_marker['tooltip'],
            icon=start_marker['icon']
        ).add_to(m)
        
        folium.Marker(
            end_marker['location'],
            tooltip=end_marker['tooltip'],
            icon=end_marker['icon']
        ).add_to(m)
        
        # Add distance and duration popup if available
        if 'legs' in directions_data['routes'][0]:
            leg = directions_data['routes'][0]['legs'][0]
            distance = leg.get('distance', {}).get('text', 'N/A')
            duration = leg.get('duration', {}).get('text', 'N/A')
            
            popup_html = f"""
            <div style='font-size: 12px'>
                <b>Distance:</b> {distance}<br>
                <b>Duration:</b> {duration}
            </div>
            """
            
            folium.Popup(popup_html).add_to(m)
        
        # Fit bounds to show the entire route with padding
        m.fit_bounds([coordinates[0], coordinates[-1]], padding=[30, 30])
        
        return m
        
    except Exception as e:
        st.error(f"Error creating map: {str(e)}")
        return None

def display_flight_options(flights_data):
    """Display flight options using Streamlit components with airline logos and INR prices."""
    if not flights_data or 'best_flights' not in flights_data:
        st.warning("No flight information available.")
        return
    
    st.subheader("Available Flights")
    
    # Display airport information if available
    if 'airport_info' in flights_data:
        airport_info = flights_data['airport_info']
        st.info(f"Showing flights to the Nearest Available Airport - {airport_info['name']} ({airport_info['iata']})")
    
    # USD to INR conversion rate
    USD_TO_INR = 85.5
    
    for best_flight in flights_data['best_flights'][:3]:  # Display top flight option
        total_duration = best_flight.get('total_duration', 'N/A')
        price_usd = best_flight.get('price', 0)
        price_inr = price_usd * USD_TO_INR
        
        # Create expander header with price in both currencies
        expander_header = f"₹{price_inr:,.2f} (${price_usd}) - ⏱️ {total_duration} mins"
        
        with st.expander(expander_header):
            # Display each flight segment in the itinerary
            for i, flight in enumerate(best_flight['flights'], 1):
                # Create columns for airline info and flight details
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    # Display airline logo if available
                    if 'airline_logo' in flight:
                        st.image(flight['airline_logo'], width=70)
                    st.write(f"**{flight.get('airline', 'N/A')}**")
                    st.write(f"Flight {flight.get('flight_number', 'N/A')}")
                
                with col2:
                    # Create sub-columns for departure and arrival
                    dep_col, arr_col = st.columns(2)
                    
                    with dep_col:
                        st.write("**Departure:**")
                        dep = flight['departure_airport']
                        st.write(f"🛫 {dep['name']} ({dep['id']})")
                        st.write(f"📅 {dep['date']}")
                        st.write(f"🕒 {dep['time']}")
                    
                    with arr_col:
                        st.write("**Arrival:**")
                        arr = flight['arrival_airport']
                        st.write(f"🛬 {arr['name']} ({arr['id']})")
                        st.write(f"📅 {arr['date']}")
                        st.write(f"🕒 {arr['time']}")
                
                # Flight details section
                st.write("**Flight Details:**")
                st.write(f"✈️ Aircraft: {flight.get('airplane', 'N/A')}")
                st.write(f"⏱️ Duration: {flight.get('duration', 'N/A')} mins")
                
                # Display any additional flight information from extensions
                if 'detected_extensions' in flight:
                    ext = flight['detected_extensions']
                    if 'seat_type' in ext:
                        st.write(f"💺 Seat: {ext['seat_type']}")
                    if 'legroom_long' in ext:
                        st.write(f"🦵 Legroom: {ext['legroom_long']}")
                    if 'carbon_emission' in ext:
                        st.write(f"🌱 Carbon emission: {ext['carbon_emission']} kg")
                
                # Display layover information
                if i < len(best_flight['flights']) and 'layovers' in best_flight:
                    layover = best_flight['layovers'][i-1]
                    st.markdown("---")
                    st.write(f"🕒 **Layover:** {layover.get('duration', 'N/A')} mins at {layover.get('name', 'N/A')}")
                    st.markdown("---")

import pandas as pd
import requests
from typing import Optional, Tuple, Dict
import logging

def get_airport_coordinates(airport_id: str) -> Optional[Tuple[float, float]]:
    """
    Retrieve latitude and longitude for an airport from airports.csv.
    
    Args:
        airport_id (str): IATA code of the airport
        
    Returns:
        Optional[Tuple[float, float]]: Tuple of (latitude, longitude) if found, None if not found
    """
    try:
        # Assuming airports.csv is stored in a known location
        # airports.csv should have columns: iata_code, latitude, longitude
        airports_df = pd.read_csv('airports.csv')
        
        # Filter for the specific airport
        airport_data = airports_df[airports_df['iata'] == airport_id]
        
        if not airport_data.empty:
            return (
                float(airport_data.iloc[0]['lat']),
                float(airport_data.iloc[0]['lon'])
            )
        else:
            logging.warning(f"Airport {airport_id} not found in database")
            return None
            
    except Exception as e:
        logging.error(f"Error retrieving airport coordinates: {str(e)}")
        return None

def get_hotel_details(location_id: str) -> Optional[Dict]:
    """
    Retrieve hotel details including coordinates from TripAdvisor API.
    
    Args:
        location_id (str): TripAdvisor location ID for the hotel
        
    Returns:
        Optional[Dict]: Dictionary containing hotel details including latitude and longitude,
                       None if request fails
    """
    if not location_id:
        logging.warning("No location ID provided")
        return None
        
    try:
        api_key = "C5104F92E6354A079E0C6E424B3B1F06"  # Should be stored in environment variables
        base_url = "https://api.content.tripadvisor.com/api/v1"
        endpoint = f"/location/{location_id}/details"
        
        params = {
            "key": api_key,
            "language": "en",
            "currency": "USD"
        }
        
        headers = {
            "accept": "application/json"
        }
        
        response = requests.get(
            f"{base_url}{endpoint}",
            params=params,
            headers=headers,
            timeout=10  # Add timeout to prevent hanging
        )
        
        if response.status_code == 200:
            hotel_data = response.json()
            
            # Extract relevant information
            return {
                'latitude': hotel_data.get('latitude'),
                'longitude': hotel_data.get('longitude'),
                'name': hotel_data.get('name'),
                'address': hotel_data.get('address_obj', {}),
                'rating': hotel_data.get('rating'),
                'num_reviews': hotel_data.get('num_reviews')
            }
        else:
            logging.error(f"Failed to fetch hotel details. Status code: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        logging.error(f"Error making API request: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"Error processing hotel details: {str(e)}")
        return None

def display_route_information(flights_data, hotels):
    """Display route information from airport to hotel.
    
    Args:
        flights_data (dict): Dictionary containing flight information including airports
        hotels (list): List of hotel information dictionaries
    """
    if not hotels or len(hotels) == 0 or not flights_data:
        return
    
    # Add custom CSS to control map container height
    st.markdown("""
        <style>
        .stfolium-container {
            height: 420px !important;
            margin-bottom: 1rem;
        }
        iframe {
            height: 420px !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    google_maps_api_key = "AIzaSyA5QKrsVtwQa30vzOgZwo_p1ak5tyzgyE0"
    
    st.divider()
    st.subheader("🗺️ Ground Transportation to Destination")
    
    # Get arrival airport coordinates
    arrival_airport_id = flights_data['airports'][0]['arrival'][0]['airport']['id']
    arrival_coords = get_airport_coordinates(arrival_airport_id)  # Assuming this function exists
    
    if not arrival_coords:
        st.error("Could not find airport coordinates")
        return
    
    arrival_lat, arrival_lon = arrival_coords
    
    # Get hotel coordinates
    destination_lat = hotels[0].get('latitude')
    destination_lon = hotels[0].get('longitude')
    
    if all([arrival_lat, arrival_lon, destination_lat, destination_lon]):
        # Display route information for both driving and transit
        modes = ['driving', 'transit']
        mode_icons = {'driving': '🚗', 'transit': '🚌'}
        
        for mode in modes:
            st.write(f"**{mode_icons[mode]} {mode.title()} Option:**")
            
            directions_data = get_directions(
                google_maps_api_key,
                arrival_lat,
                arrival_lon,
                destination_lat,
                destination_lon,
                mode
            )
            
            if directions_data and 'routes' in directions_data and directions_data['routes']:
                leg = directions_data['routes'][0]['legs'][0]
                st.write(f"📏 Distance: {leg['distance']['text']}")
                st.write(f"⏱️ Duration: {leg['duration']['text']}")
                
                route_map = plot_route_on_map(directions_data, mode)
                if route_map:
                    st_folium(
                        route_map,
                        width=704,
                        height=420,
                        returned_objects=[],
                        use_container_width=False
                    )
            else:
                st.warning(f"No {mode} route available")
    else:
        st.warning("Could not determine coordinates for route mapping")

def display_weather_forecast(forecasts):
    """Display weather forecast using Streamlit components."""
    if not forecasts:
        return
    
    st.divider()
    st.subheader("5-Day Weather Forecast At the Destination")
    cols = st.columns(len(forecasts))
    
    for idx, forecast in enumerate(forecasts):
        with cols[idx]:
            st.write(f"**{forecast['date']}**")
            icon_url = f"http://openweathermap.org/img/wn/{forecast['icon']}@2x.png"
            st.image(icon_url, width=50)
            st.write(f"{forecast['temp']}°C")
            st.write(f"*{forecast['description'].capitalize()}*")


def create_daily_itinerary(destination_details, duration_days):
    """
    Create a day-by-day itinerary from destination details.
    
    Args:
        destination_details (dict): Dictionary containing details for each category
        duration_days (int): Number of days for the trip
    
    Returns:
        list: List of daily itineraries
    """
    # Ensure we have enough places for each day
    required_places = duration_days
    for category in ['hotels', 'attractions', 'restaurants']:
        if category in destination_details:
            while len(destination_details[category]) < required_places:
                # Duplicate last item if we don't have enough places
                if destination_details[category]:
                    destination_details[category].append(destination_details[category][-1])
    
    # Create daily itineraries
    daily_itineraries = []
    
    for day in range(duration_days):
        daily_itinerary = {
            'day': day + 1,
            'hotel': destination_details.get('hotels', [])[day] if destination_details.get('hotels') else None,
            'attraction': destination_details.get('attractions', [])[day] if destination_details.get('attractions') else None,
            'restaurant': destination_details.get('restaurants', [])[day] if destination_details.get('restaurants') else None,
            'geo_info': destination_details.get('geos', [None])[0]  # Use same geo info for all days
        }
        daily_itineraries.append(daily_itinerary)
    
    return daily_itineraries

def get_return_journey_details(hotels, current_coords, airports_df, departure_airport_iata, return_date):
    """
    Get return journey details from the last hotel to nearest airport with available flights.
    
    Args:
        hotels (list): List of hotels from destination_details
        current_coords (dict): Current user location coordinates
        airports_df (DataFrame): DataFrame containing airport information
        departure_airport_iata (str): User's departure airport IATA code
        return_date (str): Date for return flight in YYYY-MM-DD format
    
    Returns:
        dict: Return journey details including route and flights
    """
    if not hotels or len(hotels) == 0:
        return None
        
    # Get last hotel coordinates
    last_hotel = hotels[-1]
    Rhotel_lat = last_hotel['latitude']
    Rhotel_lon = last_hotel['longitude']
    
    # Find nearest airports within 300km
    nearest_airports = find_multiple_nearest_airports(
        Rhotel_lat,
        Rhotel_lon,
        airports_df,
        max_airports=5,
        max_distance=300
    )
    
    if not nearest_airports:
        return None
    
    # Try each airport until we find one with available flights
    for airport in nearest_airports:
        # Get route to airport
        google_maps_api_key = "AIzaSyA5QKrsVtwQa30vzOgZwo_p1ak5tyzgyE0"

        # airport_city = airport['name'].split(',')[0]  # Get city from airport name
        Rhotel_lat = last_hotel['latitude']
        Rhotel_lon = last_hotel['longitude']
        Rairport_lat = airport['lat']  # Access lat from the dictionary
        Rairport_lon = airport['lon']  # Access lon from the dictionary
        
        routes = {
            'driving': get_directions(google_maps_api_key, Rhotel_lat, Rhotel_lon, Rairport_lat, Rairport_lon, 'driving'),
            'transit': get_directions(google_maps_api_key, Rhotel_lat, Rhotel_lon, Rairport_lat, Rairport_lon, 'transit')
        }
        
        # Get return flights with the specific return date
        flights_data = get_flight_options_with_fallback(
            current_coords['latitude'],
            current_coords['longitude'],
            airports_df,
            airport['iata'],
            flight_date=return_date
        )
        
        if flights_data and 'best_flights' in flights_data and flights_data['best_flights']:
            return {
                'airport': airport,
                'routes': routes,
                'flights': flights_data
            }
    
    return None

def display_return_journey(return_journey, ocity):
    """Display return journey information including route map and flights."""
    if not return_journey:
        st.warning("Could not plan return journey.")
        return
        
    st.divider()
    st.subheader("🔄 Return Journey")
    
    # Display route to airport
    st.markdown(f"""
    <h4>🗺️ Route to {return_journey['airport']['name']}</h4>
    """, unsafe_allow_html=True)
    
    # Add custom CSS to control map container height
    st.markdown("""
        <style>
        .stfolium-container {
            height: 420px !important;
            margin-bottom: 1rem;
        }
        iframe {
            height: 420px !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Display routes for both driving and transit
    available_modes = 0
    for mode, route_data in return_journey['routes'].items():
        try:
            if route_data and 'routes' in route_data and route_data['routes']:
                available_modes += 1
                st.write(f"**{mode.title()} Option:**")
                leg = route_data['routes'][0]['legs'][0]
                st.write(f"📏 Distance: {leg['distance']['text']}")
                st.write(f"⏱️ Duration: {leg['duration']['text']}")
                
                route_map = plot_route_on_map(route_data, mode, is_return=True)
                if route_map:
                    st_folium(
                        route_map,
                        width=704,
                        height=420,
                        returned_objects=[],
                        use_container_width=False
                    )
            elif mode == 'transit':
                st.warning("No transit route available")
        except (KeyError, IndexError) as e:
            st.warning(f"Error displaying {mode} route: Data format incorrect or missing")
        except Exception as e:
            st.warning(f"Unexpected error displaying {mode} route: {str(e)}")
    
    if available_modes == 0:
        st.warning("No route options available to the airport.")
    
    # Display return flight options
    st.divider()
    st.subheader(f"✈️ Journey to {ocity}")
    try:
        display_flight_options(return_journey['flights'])
    except Exception as e:
        st.error("Error displaying flight options. Please try again later.")

def display_daily_itineraries(daily_itineraries):
    """
    Display comprehensive day-by-day itinerary in Streamlit with detailed information.
    
    Args:
        daily_itineraries (list): List of daily itinerary dictionaries
    """
    # Define price level mapping
    price_level_map = {
        "$$$$": "Very Expensive",
        "$$$": "Expensive",
        "$$": "Reasonable Stay",
        "$": "Affordable",
    }
    
    st.divider()
    st.subheader("📅 Day-by-Day Itinerary")
    
    for itinerary in daily_itineraries:
        day_num = itinerary['day']
        
        with st.expander(f"Day {day_num}"):
            # Display Hotel Information
            if itinerary['hotel']:
                st.divider()
                st.markdown("### 🏨 Accommodation")
                hotel = itinerary['hotel']
                
                # Display hotel photos
                if hotel['photos'] and len(hotel['photos']) > 0:
                    cols = st.columns(min(3, len(hotel['photos'])))
                    for idx, photo in enumerate(hotel['photos'][:3]):
                        try:
                            photo_url = photo if isinstance(photo, str) else photo.get('url', '')
                            cols[idx].image(photo_url, use_container_width=True)
                        except Exception as e:
                            st.error(f"Error displaying hotel photo: {str(e)}")
                
                st.write(f"**{hotel['name']}**")
                st.write(f"**Description:** {hotel['description']}")
                st.write(f"**Phone:** {hotel['phone']}")
                
                if hotel['address_obj']:
                    address = hotel['address_obj']
                    st.write("**Address:**")
                    st.write(f"{address.get('street1', '')}")
                    st.write(f"{address.get('city', '')}, {address.get('state', '')} {address.get('postalcode', '')}")
                    st.write(f"{address.get('country', '')}")
                
                # Display price level with description
                price_level = hotel['price_level']
                if price_level in price_level_map:
                    st.write(f"**Price Level:** {price_level} - {price_level_map[price_level]}")
                else:
                    st.write(f"**Price Level:** {price_level}")
                
                if hotel['amenities']:
                    st.write("**Amenities:**")
                    st.write(", ".join(hotel['amenities']))
                
                if hotel['reviews']:
                    st.write("**Recent Reviews:**")
                    for review in hotel['reviews'][:3]:
                        if isinstance(review, dict):
                            st.markdown(f"⭐ **{review.get('rating', 'N/A')}/5** - {review.get('text', 'No review text')}")
                        else:
                            st.markdown(f"⭐ {review}")
                
                st.write(f"[View on TripAdvisor]({hotel['web_url']})")
            
            st.divider()
            # Display Attraction Information
            if itinerary['attraction']:
                st.markdown("### 🎯 Activity")
                attraction = itinerary['attraction']
                
                # Display attraction photos
                if attraction['photos'] and len(attraction['photos']) > 0:
                    cols = st.columns(min(3, len(attraction['photos'])))
                    for idx, photo in enumerate(attraction['photos'][:3]):
                        try:
                            photo_url = photo if isinstance(photo, str) else photo.get('url', '')
                            cols[idx].image(photo_url, use_container_width=True)
                        except Exception as e:
                            st.error(f"Error displaying attraction photo: {str(e)}")
                
                st.write(f"**{attraction['name']}**")
                st.write(f"**Description:** {attraction['description']}")
                st.write(f"**Phone:** {attraction['phone']}")
                
                if attraction['address_obj']:
                    address = attraction['address_obj']
                    st.write("**Address:**")
                    st.write(f"{address.get('street1', '')}")
                    st.write(f"{address.get('city', '')}, {address.get('state', '')} {address.get('postalcode', '')}")
                    st.write(f"{address.get('country', '')}")
                
                if attraction.get('attraction_types'):
                    st.write("**Attraction Types:**")
                    st.write(", ".join([t.get('name', '') for t in attraction['attraction_types']]))
                st.write(f"**Rating:** {attraction.get('rating', 'N/A')}")
                # st.write(f"**Ranking:** {attraction.get('ranking', 'N/A')}")
                
                if attraction['reviews']:
                    st.write("**Recent Reviews:**")
                    for review in attraction['reviews'][:3]:
                        if isinstance(review, dict):
                            st.markdown(f"⭐ **{review.get('rating', 'N/A')}/5** - {review.get('text', 'No review text')}")
                        else:
                            st.markdown(f"⭐ {review}")
                
                st.write(f"[View on TripAdvisor]({attraction['web_url']})")
            
            st.divider()
            # Display Restaurant Information
            if itinerary['restaurant']:
                st.markdown("### 🍽️ Dining")
                restaurant = itinerary['restaurant']
                
                # Display restaurant photos
                if restaurant['photos'] and len(restaurant['photos']) > 0:
                    cols = st.columns(min(3, len(restaurant['photos'])))
                    for idx, photo in enumerate(restaurant['photos'][:3]):
                        try:
                            photo_url = photo if isinstance(photo, str) else photo.get('url', '')
                            cols[idx].image(photo_url, use_container_width=True)
                        except Exception as e:
                            st.error(f"Error displaying restaurant photo: {str(e)}")
                
                st.write(f"**{restaurant['name']}**")
                st.write(f"**Description:** {restaurant['description']}")
                st.write(f"**Phone:** {restaurant['phone']}")
                
                if restaurant['address_obj']:
                    address = restaurant['address_obj']
                    st.write("**Address:**")
                    st.write(f"{address.get('street1', '')}")
                    st.write(f"{address.get('city', '')}, {address.get('state', '')} {address.get('postalcode', '')}")
                    st.write(f"{address.get('country', '')}")
                
                if restaurant.get('cuisine'):
                    st.write("**Cuisine:**")
                    st.write(", ".join([c.get('name', '') for c in restaurant['cuisine']]))
                st.write(f"**Price Range:** {restaurant.get('price_range', 'N/A')}")
                
                if restaurant.get('dietary_restrictions'):
                    st.write("**Dietary Options:**")
                    st.write(", ".join([d.get('name', '') for d in restaurant['dietary_restrictions']]))
                
                if restaurant['reviews']:
                    st.write("**Recent Reviews:**")
                    for review in restaurant['reviews'][:3]:
                        if isinstance(review, dict):
                            st.markdown(f"⭐ **{review.get('rating', 'N/A')}/5** - {review.get('text', 'No review text')}")
                        else:
                            st.markdown(f"⭐ {review}")
                
                st.write(f"[View on TripAdvisor]({restaurant['web_url']})")
            
            # # Display Location/Geographic Information once per day
            # if itinerary['geo_info']:
            #     st.markdown("### 📍 Location Information")
            #     geo = itinerary['geo_info']
                
            #     st.write(f"**{geo['name']}**")
            #     st.write(f"**Description:** {geo['description']}")
            #     if geo.get('geo_type'):
            #         st.write(f"**Location Type:** {geo['geo_type']}")
            #     if geo.get('timezone'):
            #         st.write(f"**Timezone:** {geo['timezone']}")
                
            #     if geo['reviews']:
            #         st.write("**Area Reviews:**")
            #         for review in geo['reviews'][:3]:
            #             if isinstance(review, dict):
            #                 st.markdown(f"⭐ **{review.get('rating', 'N/A')}/5** - {review.get('text', 'No review text')}")
            #             else:
            #                 st.markdown(f"⭐ {review}")
                
            #     st.write(f"[View Area on TripAdvisor]({geo['web_url']})")

def get_destination_details(destination, duration_days):
    """
    Modified version to fetch appropriate number of places based on trip duration.
    """
    base_url = "https://api.content.tripadvisor.com/api/v1"
    tripadvisor_api_key = "C5104F92E6354A079E0C6E424B3B1F06"
    weather_api_key = "a73d2e9d5872429030175d780367cf35"
    
    categories = ["hotels", "attractions", "restaurants", "geos"]
    
    try:
        destination_details = {}
        weather_forecast = None
        first_location_coords = None

        for category in categories:
            # Search for locations
            search_url = f"{base_url}/location/search"
            search_params = {
                "key": tripadvisor_api_key,
                "searchQuery": destination,
                "category": category,
                "language": "en"
            }
            
            search_response = requests.get(
                search_url,
                params=search_params,
                headers={"accept": "application/json"}
            )
            search_response.raise_for_status()
            search_data = search_response.json()
            
            # Extract location IDs
            location_ids = [
                item.get("location_id")
                for item in search_data.get("data", [])
            ]
            
            # Determine how many places to fetch based on category and duration
            if category == "geos":
                places_to_fetch = 1  # We only need one geo entry
            else:
                places_to_fetch = min(duration_days, len(location_ids))
            
            category_details = []
            
            # Fetch details for each location
            for location_id in location_ids[:places_to_fetch]:
                details_url = f"{base_url}/location/{location_id}/details"
                details_params = {
                    "key": tripadvisor_api_key,
                    "language": "en",
                    "currency": "USD"
                }
                
                details_response = requests.get(
                    details_url,
                    params=details_params,
                    headers={"accept": "application/json"}
                )
                details_response.raise_for_status()
                location_data = details_response.json()
                
                # Extract coordinates
                latitude = location_data.get("latitude")
                longitude = location_data.get("longitude")
                
                # Store first valid coordinates for weather data
                if first_location_coords is None and latitude and longitude:
                    first_location_coords = (latitude, longitude)
                
                # Fetch photos and reviews
                photos = get_hotel_photos(location_id, tripadvisor_api_key)
                reviews = get_hotel_reviews(location_id, tripadvisor_api_key)
                
                # Compile location information based on category
                location_info = {
                    "name": location_data.get("name", "N/A"),
                    "description": location_data.get("description", "No description available"),
                    "web_url": location_data.get("web_url", "N/A"),
                    "phone": location_data.get("phone", "N/A"),
                    "latitude": latitude,
                    "longitude": longitude,
                    "address_obj": location_data.get("address_obj", {}),
                    "photos": photos,
                    "reviews": reviews
                }
                
                # Add category-specific information
                if category == "hotels":
                    location_info.update({
                        "price_level": location_data.get("price_level", "N/A"),
                        "amenities": location_data.get("amenities", [])[:6]
                    })
                elif category == "restaurants":
                    location_info.update({
                        "cuisine": location_data.get("cuisine", []),
                        "price_range": location_data.get("price_range", "N/A"),
                        "dietary_restrictions": location_data.get("dietary_restrictions", [])
                    })
                elif category == "attractions":
                    location_info.update({
                        "attraction_types": location_data.get("attraction_types", []),
                        "rating": location_data.get("rating", "N/A"),
                        "ranking": location_data.get("ranking", "N/A")
                    })
                elif category == "geos":
                    location_info.update({
                        "geo_type": location_data.get("geo_type", "N/A"),
                        "ancestors": location_data.get("ancestors", []),
                        "timezone": location_data.get("timezone", "N/A")
                    })
                
                category_details.append(location_info)
            
            destination_details[category] = category_details
        
        # Fetch weather data if we have coordinates
        if first_location_coords:
            weather_forecast = get_weather_forecast(
                first_location_coords[0],
                first_location_coords[1],
                weather_api_key
            )
        
        return destination_details, weather_forecast
    
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching destination data: {str(e)}")
        return {}, None

def display_destination_details(destination_details):
    """
    Display the fetched destination details in the Streamlit app.
    
    Args:
        destination_details (dict): Dictionary containing details for each category
    """
    for category, items in destination_details.items():
        if items:
            st.subheader(f"{category.title()}")
            
            for item in items:
                with st.expander(f"{item['name']}"):
                    # Display photos first if available
                    if item['photos'] and len(item['photos']) > 0:
                        # st.write("**Photos:**")
                        # Check the structure of the first photo to determine how to handle it
                        if isinstance(item['photos'][0], str):
                            # If photos are direct URLs
                            cols = st.columns(min(3, len(item['photos'])))
                            for idx, photo_url in enumerate(item['photos'][:3]):
                                try:
                                    cols[idx].image(photo_url, use_container_width=True)
                                except Exception as e:
                                    st.error(f"Error displaying photo: {str(e)}")
                        else:
                            # If photos are objects with URLs
                            cols = st.columns(min(3, len(item['photos'])))
                            for idx, photo in enumerate(item['photos'][:3]):
                                try:
                                    photo_url = photo.get('url') if isinstance(photo, dict) else str(photo)
                                    cols[idx].image(photo_url, use_container_width=True)
                                except Exception as e:
                                    st.error(f"Error displaying photo: {str(e)}")

                    st.write(f"**Description:** {item['description']}")
                    st.write(f"**Phone:** {item['phone']}")
                    
                    # Display address if available
                    if item['address_obj']:
                        address = item['address_obj']
                        st.write("**Address:**")
                        st.write(f"{address.get('street1', '')}")
                        st.write(f"{address.get('city', '')}, {address.get('state', '')} {address.get('postalcode', '')}")
                        st.write(f"{address.get('country', '')}")
                    
                    # Display category-specific information
                    if category == "hotels":
                        st.write(f"**Price Level:** {item['price_level']}")
                        if item['amenities']:
                            st.write("**Amenities:**")
                            st.write(", ".join(item['amenities']))
                    
                    elif category == "restaurants":
                        if item.get('cuisine'):
                            st.write("**Cuisine:**")
                            st.write(", ".join([c.get('name', '') for c in item['cuisine']]))
                        st.write(f"**Price Range:** {item.get('price_range', 'N/A')}")
                        if item.get('dietary_restrictions'):
                            st.write("**Dietary Options:**")
                            st.write(", ".join([d.get('name', '') for d in item['dietary_restrictions']]))
                    
                    elif category == "attractions":
                        if item.get('attraction_types'):
                            st.write("**Attraction Types:**")
                            st.write(", ".join([t.get('name', '') for t in item['attraction_types']]))
                        st.write(f"**Rating:** {item.get('rating', 'N/A')}")
                        st.write(f"**Ranking:** {item.get('ranking', 'N/A')}")
                    
                    elif category == "geos":
                        st.write(f"**Type:** {item.get('geo_type', 'N/A')}")
                        st.write(f"**Timezone:** {item.get('timezone', 'N/A')}")
                    
                    # Display reviews if available
                    if item['reviews']:
                        st.write("**Recent Reviews:**")
                        for review in item['reviews'][:3]:
                            if isinstance(review, dict):
                                st.markdown(f"⭐ **{review.get('rating', 'N/A')}/5** - {review.get('text', 'No review text')}")
                            else:
                                st.markdown(f"⭐ {review}")
                    
                    st.write(f"[View on TripAdvisor]({item['web_url']})")

def get_hotel_photos(location_id, api_key):
    """
    Fetch photos for a specific location from TripAdvisor API.
    
    Args:
        location_id (str): TripAdvisor location ID
        api_key (str): TripAdvisor API key
    
    Returns:
        list: List of photo URLs or photo objects
    """
    try:
        base_url = "https://api.content.tripadvisor.com/api/v1"
        photos_url = f"{base_url}/location/{location_id}/photos"
        photos_params = {
            "key": api_key,
            "language": "en"
        }
        
        response = requests.get(
            photos_url,
            params=photos_params,
            headers={"accept": "application/json"}
        )
        response.raise_for_status()
        
        photos_data = response.json()
        photos = []
        
        # Extract photo URLs from the response
        if isinstance(photos_data, dict) and 'data' in photos_data:
            for photo in photos_data['data'][:3]:  # Limit to 3 photos
                if isinstance(photo, dict):
                    # Extract the largest available image URL
                    images = photo.get('images', {})
                    if images:
                        # Try to get the large image, fall back to original if not available
                        photo_url = (images.get('large', {}) or images.get('original', {})).get('url')
                        if photo_url:
                            photos.append(photo_url)
        
        return photos
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching photos: {str(e)}")
        return []


def get_price_level_description(price_level):
    """Convert price level symbols to descriptive text."""
    price_descriptions = {
        "$$$$": "Very Costly",
        "$$$": "Costly",
        "$$": "Affordable",
        "$": "Great Bargain!!"
    }
    return price_descriptions.get(price_level, price_level)

def parse_travel_input(text):
    if not text:
        return {"error": "Please enter your travel plans."}
    
    try:
        destination = extract_destination(text)
        budget = extract_budget(text)
        duration = extract_duration(text)
        interests = extract_interests(text)
        
        return {
            "destination": destination,
            "budget": budget,
            "duration": duration,
            "interests": interests
        }
    except Exception as e:
        return {"error": f"Error processing input: {str(e)}"}


# Set the Streamlit page configuration
st.set_page_config(
    page_title="Travel Itinerary Generator",
    page_icon="🗺️", 
    # layout="wide",            # For a WIDE website layout         
)

def main():
    st.title("TripTailor - Your Personalised Travel Itinerary Generator and Assistant")
    
    # Load airports data
    try:
        airports_df = pd.read_csv('airports.csv')
        airports_df['lat'] = pd.to_numeric(airports_df['lat'], errors='coerce')
        airports_df['lon'] = pd.to_numeric(airports_df['lon'], errors='coerce')
        airports_df = airports_df.dropna(subset=['lat', 'lon', 'iata'])
    except Exception as e:
        st.error(f"Error loading airports data: {e}")
        return

    st.write("Describe your travel plans in one sentence, and I'll generate a personalized itinerary.")

    user_input = st.text_area(
        "Enter your travel plans:",
        placeholder="e.g., I want to travel to the Maldives with my wife for a romantic vacation with a budget of $10,000 for 3 nights and 4 days."
    )

    if st.button("Generate Itinerary"):
        st.divider()
        if user_input:
            # Parse and validate travel input first
            travel_info = parse_travel_input(user_input)
            if "error" in travel_info:
                st.warning(travel_info["error"])
                return
            elif not travel_info["destination"]:
                st.warning("Could not extract destination. Please include it in your prompt.")
                return
            elif not travel_info["budget"]:
                st.warning("Could not extract budget. Please include it in your prompt.")
                return
            elif not travel_info["duration"]["days"]:
                st.warning("Could not extract duration. Please include it in your prompt.")
                return

            # Display success message and extracted info first
            st.success("Information extracted successfully!")
            st.write("**Extracted Information**:")
            st.write(f"**Destination**: {travel_info['destination']}")
            st.write(f"**Budget**: {travel_info['budget']['currency']} {travel_info['budget']['amount']:,}")
            st.write(f"**Duration**: {travel_info['duration']['nights']} nights and {travel_info['duration']['days']} days")
            if travel_info['duration']['start_date']:
                st.write(f"**Dates**: {travel_info['duration']['start_date']} to {travel_info['duration']['end_date']}")
            st.write(f"**Interests**: {', '.join(travel_info['interests']) if travel_info['interests'] else 'Not specified'}")

            # Then handle location information
            departure_airport_iata = "BOM"  # Default to Mumbai
            user_ip = get_user_ip()
            location_info = {}
            
            if user_ip:
                st.divider()
                location = get_user_location(user_ip)
                if location:
                    location_info['location'] = f"📍 Detected your location: {location['city']}, {location['region']}, {location['country']}"
                    nearest_airport = find_nearest_airport(location['latitude'], location['longitude'], airports_df)
                    if nearest_airport:
                        departure_airport_iata = nearest_airport['iata']
                        location_info['airport'] = f"✈️ Nearest Airport: {nearest_airport['name']} ({departure_airport_iata})"
                    else:
                        location_info['airport'] = "Using Mumbai (BOM) as default departure airport."
                else:
                    location_info['airport'] = "Unable to determine your location. Using Mumbai (BOM) as default departure airport."
            else:
                location_info['airport'] = "Unable to retrieve your IP address. Using Mumbai (BOM) as default departure airport."

            # Display location info last
            st.write(location_info.get('location', ''))
            st.write(location_info.get('airport', ''))

            st.divider()
            # Now show spinner while fetching trip details
            with st.spinner("Generating your personalized travel itinerary..."):
                # Calculate the outbound and return dates
                if travel_info['duration']['start_date']:
                    # If specific dates were provided
                    outbound_date = datetime.strptime(travel_info['duration']['start_date'], "%d/%m/%y").strftime("%Y-%m-%d")
                    return_date = datetime.strptime(travel_info['duration']['end_date'], "%d/%m/%y").strftime("%Y-%m-%d")
                else:
                    # If no specific dates, use default (starting 30 days from now)
                    outbound_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
                    return_date = (datetime.now() + timedelta(days=30 + travel_info['duration']['days'])).strftime("%Y-%m-%d")
                
                # Fetch all required data with duration
                destination_details, weather_forecast = get_destination_details(
                    travel_info['destination'], 
                    travel_info['duration']['days']
                )
                
                # Get coordinates for flight search
                destination_coords = None
                flights_data = None
                if destination_details.get('hotels') and len(destination_details['hotels']) > 0:
                    first_hotel = destination_details['hotels'][0]
                    if first_hotel['latitude'] and first_hotel['longitude']:
                        destination_coords = {
                            'latitude': first_hotel['latitude'],
                            'longitude': first_hotel['longitude']
                        }
                        flights_data = get_flight_options_with_fallback(
                            destination_coords['latitude'],
                            destination_coords['longitude'],
                            airports_df,
                            departure_airport_iata,
                            flight_date=outbound_date
                        )

            # After spinner, display trip information
            st.markdown("<h1 style='text-align: center;'>YOUR TRIP INFORMATION</h1>", unsafe_allow_html=True)
            
            # Display weather information
            if weather_forecast:
                display_weather_forecast(weather_forecast)
                st.divider()
            
            # Display flight options if available
            if flights_data:
                st.subheader(f"✈️ Journey to {travel_info['destination']}")
                display_flight_options(flights_data)
                display_route_information(flights_data, destination_details.get('hotels', []))
            else:
                st.warning("Could not find flight information for the destination.")
            
            # Create and display daily itineraries
            if destination_details:
                daily_itineraries = create_daily_itinerary(
                    destination_details, 
                    travel_info['duration']['days']
                )
                display_daily_itineraries(daily_itineraries)
                
                # Update the return journey section
                if destination_details.get('hotels'):
                    with st.spinner("Planning your return journey..."):
                        user_ip = get_user_ip()
                        if user_ip:
                            location = get_user_location(user_ip)
                            if location:
                                current_coords = {
                                    'latitude': location['latitude'],
                                    'longitude': location['longitude']
                                }
                                
                                # Get and display return journey with the calculated return date
                                return_journey = get_return_journey_details(
                                    destination_details['hotels'],
                                    current_coords,
                                    airports_df,
                                    departure_airport_iata,
                                    return_date=return_date
                                )
                                display_return_journey(return_journey, location['city'])
            else:
                st.warning("No destination information found.")
            
            # Add final divider before PDF button
            st.divider()
            
            # Add the button and trigger the print dialog
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                # Add a custom button with embedded JavaScript
                st.markdown("""
                    <style>
                        .print-button {
                            display: inline-block;
                            padding: 0.8rem 1.5rem;
                            background-color: #007bff;
                            color: white;
                            font-size: 16px;
                            font-weight: bold;
                            border: none;
                            border-radius: 5px;
                            cursor: pointer;
                            text-align: center;
                            transition: background-color 0.3s ease;
                            text-decoration: none;
                        }
                        .print-button:hover {
                            background-color: #0056b3;
                        }
                    </style>
                    <div style="text-align: center;">
                        <button class="print-button" onclick="triggerPrint()">📄 Save Itinerary as PDF</button>
                    </div>
                    <script>
                        function triggerPrint() {
                            window.print(); // Trigger the browser's print dialog
                        }
                    </script>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()