# import os
# import re
# import difflib
# import random
# import unicodedata
# import math
# from flask import Flask, request, jsonify
# import pandas as pd
# from dotenv import load_dotenv
# from langchain_community.vectorstores import FAISS
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.prompts import PromptTemplate
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_openai import ChatOpenAI
# from langchain_openai import OpenAIEmbeddings
# from sentence_transformers import SentenceTransformer
# from langchain_community.embeddings import SentenceTransformerEmbeddings
# from langchain_community.embeddings import FakeEmbeddings
# from langchain_core.output_parsers import StrOutputParser
# from flask_cors import CORS
# from rapidfuzz import fuzz

# app = Flask(__name__)
# CORS(app)

# # --- Load Environment Variables ---
# load_dotenv()
# # HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
# # GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# # --- Helper Functions ---
# # # Cleans LLM-generated text by removing lines containing '(note: ...structured process...)' and flattens the result into a single line.
# def clean_llm_output(text):
#     lines = text.split('\n')
#     filtered = [line for line in lines if not re.search(r'\(note:.*structured process.*\)', line, re.IGNORECASE)]
#     result = ' '.join(filtered).strip()
#     # Remove any remaining newlines or carriage returns
#     result = result.replace('\n', ' ').replace('\r', ' ')
#     return result

# # Converts price strings like '₹1.2 Crore' or '₹75 Lakh' to float values in lakhs (e.g., 120.0 or 75.0), or returns 'Coming Soon' if indicate
# def clean_price(price):
#     if isinstance(price, str):
#         price_lower = price.lower().strip()
#         if 'coming soon' in price_lower:
#             return 'Coming Soon'
#         price = re.sub(r'[₹, ]', '', price_lower)
#         # Handle crore, lakh, thousand, l, k, and raw numbers
#         if 'crore' in price:
#             value = float(re.findall(r'(\d+\.?\d*)', price)[0]) * 100
#             return value
#         elif 'lakh' in price or 'l' in price:
#             value = float(re.findall(r'(\d+\.?\d*)', price)[0])
#             return value
#         elif 'thousand' in price or 'k' in price:
#             value = float(re.findall(r'(\d+\.?\d*)', price)[0]) / 100
#             return value
#         else:
#             # Raw number: if >= 100000, treat as rupees, convert to lakh
#             value = float(re.findall(r'(\d+\.?\d*)', price)[0])
#             if value >= 100000:
#                 return value / 100000
#             elif value >= 1000:
#                 return value / 100
#             else:
#                 return value
#     return None

# # Converts vehicle name like 'Tata Nexon EV✨' to a normalized lowercase alphanumeric string (e.g., 'tatanexonev').
# def normalize_vehicle_name(name):
#     if not isinstance(name, str):
#         return ""
#     name = unicodedata.normalize('NFKD', name)
#     name = name.lower()
#     name = re.sub(r'[^a-z0-9]', '', name)
#     return name

# # Normalizes text like '91-Trucks' or '91 Trucks' to a lowercase alphanumeric string (e.g., '91trucks').
# def normalize_91trucks(text):
#     # Normalize spaces, dashes, and case for '91trucks' variants
#     return re.sub(r'[^a-z0-9]', '', text.lower())

# # Checks if a user query like "Hi", "bye bye", or "good night" is a greeting or farewell (e.g., returns True for "Hi").
# def is_greeting(query):
#     GREETINGS = {"hi","hyy", "hy", "Hyy", "HYY", "hlo", "HLO", "Hi", "HI", "hello", "namaste", "hey", "good morning", "good afternoon", "good evening", "greetings", "good day", "hii", "hiii", "heyy", "hey there", "hello there", "yo", "sup", "hola", "bonjour", "ciao", "salaam", "shalom", "howdy", "hiya", "wassup", "what's up", "bye", "goodbye", "see you", "farewell", "take care", "byy", "by", "byby", "bye bye", "bi", "good night", "see ya", "later", "catch you later", "peace", "adios", "au revoir", "nighty night", "sweet dreams", "cheerio", "bless you", "best wishes", "safe travels", "until next time", "talk soon", "stay safe", "much love", "respect", "big hello"}
#     q = query.strip().lower()
#     q = re.sub(r'[^a-zA-Z ]', '', q)
#     q = ' '.join(q.split())
#     words = set(q.split())
#     if words and all(word in GREETINGS for word in words):
#         return True
#     if q in GREETINGS:
#         return True
#     return False

# def get_vehicle_data(display_name, df):
#     """
#     Searches for a vehicle in the given DataFrame 'df' that matches the 'display_name'.
#     Cleans the name for comparison, and extracts key details if a match is found.

#     - Filters out irrelevant or missing values (like 'Not available', 'nan', etc.).
#     - Formats the price field into Lakhs or Crores.
#     - Renames and includes key fields like fuel_type, vehicle_name, etc.
#     - Handles default fallback if price is invalid.

#     Returns:
#     A dictionary of cleaned vehicle data if found, else None.

#     # Example Output:
#       {
#     'vehicle_price': '8.25 Lakh',
#     'fuel_type': 'Diesel',
#     'vehicle_name': 'Tata Intra V30',
#     'brand_name': 'Tata',
#     'vehicle_image': 'https://example.com/intra.jpg'
#      }
#     """

#     display_name_clean = display_name.lower().strip()
#     vehicle_data_df = df[df['Vehicle Name'].str.lower().str.strip().str.contains(display_name_clean, na=False)]
#     if not vehicle_data_df.empty:
#         row = vehicle_data_df.iloc[0].to_dict()
#         output = {}
#         # Exclude description fields and unnamed_0
#         exclude_fields = {'Vehicle Description', 'llm_ready_vehicle_description', 'unnamed_0', 'Unnamed: 0'}
#         for key, val in row.items():
#             if key in exclude_fields:
#                 continue
#             if not val or str(val).strip().lower() in ["not available", "", "nan", "n/a"]:
#                 continue
#             # Format price as per requirements
#             if key in ['Price', 'Vehicle Price']:
#                 try:
#                     price_float = float(val)
#                     if price_float >= 100:
#                         output['vehicle_price'] = f"{price_float/100:.2f} Crore"
#                     else:
#                         output['vehicle_price'] = f"{price_float:.2f} Lakh"
#                 except Exception:
#                     output['vehicle_price'] = 'Coming Soon'
#             elif key == 'Fuel Type':
#                 output['fuel_type'] = val
#             elif key == 'Vehicle Name':
#                 output['vehicle_name'] = val
#             elif key == 'Model Name':
#                 output['model_name'] = val
#             elif key == 'Average Rating':
#                 output['average_rating'] = val
#             elif key == 'Brand Name':
#                 output['brand_name'] = val
#             elif key == 'Vehicle Image':
#                 output['vehicle_image'] = val
#             elif key == 'Electric':
#                 output['electric'] = val
#             elif key == 'End Point':
#                 output['redirect_url'] = val
#             else:
#                 # Add all other fields as-is
#                 output[key.lower().replace(' ', '_')] = val
#         # Ensure vehicle_price is set if not already and price was present
#         if ('Price' in row or 'Vehicle Price' in row) and 'vehicle_price' not in output:
#             output['vehicle_price'] = 'Coming Soon'
#         return output if output else None
#     return None

# def get_recommendations(main_vehicle, df, n=3, price=None):
#     """
#     Returns up to `n` vehicle recommendations similar to the main vehicle.

# ✔ Same category  
# ✔ Price within ±10%  
# ✔ Excludes main vehicle  
# ✔ Prioritizes different brands for diversity
# """
#     if not main_vehicle:
#         return []
#     # If price is 'Coming Soon', do not show recommendations
#     if str(main_vehicle.get("vehicle_price", "")).strip().lower() == 'coming soon':
#         return []
#     category = main_vehicle.get("category_name") or main_vehicle.get("Category Name")
#     price_val = None
#     try:
#         price_val = float(main_vehicle.get("vehicle_price", 0).replace('Lakh', '').replace('Crore', '').replace('Coming Soon', '').strip())
#         if 'crore' in str(main_vehicle.get("vehicle_price", '')).lower():
#             price_val *= 100
#     except Exception:
#         price_val = None
#     filtered = df.copy()
#     # Filter by category_name if available
#     if category and 'Category Name' in filtered.columns:
#         filtered = filtered[filtered['Category Name'].str.lower() == str(category).lower()]
#     # Filter by price range: strictly 0.9x to 1.1x
#     if price_val:
#         min_price = price_val * 0.9
#         max_price = price_val * 1.1
#         filtered = filtered[filtered['Price'].apply(lambda x: isinstance(x, (int, float)) and min_price < x < max_price)]
#     # Exclude the main vehicle
#     filtered = filtered[filtered['Vehicle Name'] != main_vehicle.get("vehicle_name")]
#     if filtered.empty:
#         return []
    
#     # Get diverse recommendations across brands
#     def get_diverse_recommendations(df, max_vehicles=3):
#         """Get diverse recommendations across different brands"""
#         recommendations = []
#         used_models = set()
#         used_brands = set()
#         main_brand = main_vehicle.get("brand_name", "").strip()
        
#         # First, try to get one vehicle from each brand (excluding the main vehicle's brand)
#         brand_groups = df.groupby('Brand Name')
#         for brand_name, brand_df in brand_groups:
#             if len(recommendations) >= max_vehicles:
#                 break
#             # Skip the main vehicle's brand to ensure diversity
#             if brand_name.strip().lower() == main_brand.lower():
#                 continue
#             for _, row in brand_df.iterrows():
#                 vname = row.get('Vehicle Name')
#                 if vname and vname not in used_models:
#                     recommendations.append(row)
#                     used_models.add(vname)
#                     used_brands.add(brand_name)
#                     break  # Only take one from each brand initially
        
#         # If we still have space, fill with remaining vehicles (including from main brand if needed)
#         if len(recommendations) < max_vehicles:
#             for _, row in df.iterrows():
#                 if len(recommendations) >= max_vehicles:
#                     break
#                 vname = row.get('Vehicle Name')
#                 if vname and vname not in used_models:
#                     recommendations.append(row)
#                     used_models.add(vname)
        
#         return recommendations
    
#     diverse_recommendations = get_diverse_recommendations(filtered, n)
#     return pd.DataFrame(diverse_recommendations)

# def get_brand_models(brand_name, df, category=None):
#     """
# Returns up to 5 vehicle models for a given brand.

# ✔ Filters vehicles by brand name (case-insensitive)  
# ✔ Gets top 5 unique model names  
# ✔ Fetches full details using get_vehicle_data()  
# ✔ Ignores models with missing data

# Example:
# get_brand_models('Tata', df)
# """
#     brand_df = df[df['Brand Name'].str.lower() == brand_name.lower()]
#     if brand_df.empty:
#         return []
#     model_names = brand_df['Vehicle Name'].dropna().unique()
#     top_model_names = model_names[:5]
#     models_data = []
#     for name in top_model_names:
#         vehicle_info = get_vehicle_data(name, df)
#         if vehicle_info:
#             models_data.append(vehicle_info)
#     return models_data

# def get_vehicle_data_with_id_by_index(row):
#     """
# Parses a vehicle row and returns cleaned data with formatted fields.

# ✔ Skips unwanted or unavailable fields  
# ✔ Formats 'Price' into 'Lakh' or 'Crore'  
# ✔ Maps known keys to standard output (e.g., vehicle_name, fuel_type)  
# ✔ Adds 'id' from 'Unnamed: 0' or fallback  
# ✔ Returns None if no valid data found

# Example:
# get_vehicle_data_with_id_by_index(row) → {
#     'vehicle_name': 'Tata Intra V30',
#     'vehicle_price': '8.50 Lakh',
#     'fuel_type': 'Diesel',
#     'brand_name': 'Tata',
#     ...
# }
# """
#     output = {}
#     exclude_fields = {'Vehicle Description', 'llm_ready_vehicle_description', 'unnamed_0', 'Unnamed: 0'}
#     for key, val in row.items():
#         if key in exclude_fields:
#             continue
#         if not val or str(val).strip().lower() in ["not available", "", "nan", "n/a"]:
#             continue
#         if key in ['Price', 'Vehicle Price']:
#             try:
#                 price_float = float(val)
#                 if price_float >= 100:
#                     output['vehicle_price'] = f"{price_float/100:.2f} Crore"
#                 else:
#                     output['vehicle_price'] = f"{price_float:.2f} Lakh"
#             except Exception:
#                 output['vehicle_price'] = 'Coming Soon'
#         elif key == 'Fuel Type':
#             output['fuel_type'] = val
#         elif key == 'Vehicle Name':
#             output['vehicle_name'] = val
#         elif key == 'Model Name':
#             output['model_name'] = val
#         elif key == 'Average Rating':
#             output['average_rating'] = val
#         elif key == 'Brand Name':
#             output['brand_name'] = val
#         elif key == 'Vehicle Image':
#             output['vehicle_image'] = val
#         elif key == 'Electric':
#             output['electric'] = val
#         elif key == 'End Point':
#             output['redirect_url'] = val
#         else:
#             output[key.lower().replace(' ', '_')] = val
#     if ('Price' in row or 'Vehicle Price' in row) and 'vehicle_price' not in output:
#         output['vehicle_price'] = 'Coming Soon'
#     if 'Unnamed: 0' in row:
#         output['id'] = row['Unnamed: 0']
#     else:
#         pass
#         # output['id'] = row.get('id', None)
#     return output if output else None

# def get_vehicle_context(data):
#     """
# Generates a short context string from vehicle data.

# ✔ Extracts only selected keys (name, brand, price, image, etc.)  
# ✔ Skips empty, invalid, or unavailable values  
# ✔ Returns values as "key: value" pairs separated by ;

# Example:
# get_vehicle_context(data) →
# 'vehicle_name: Tata 1815 LPT; electric: No; model_name: 1815 LPT; average_rating: No ratings available yet; brand_name: Tata; vehicle_image: https://...; vehicle_price: ₹26.84 Lakh; fuel_type: Diesel; End Point: https://...'
# """
#     if not data:
#         return ""
#     context = []
#     for key in ["vehicle_name", "electric", "model_name", "average_rating", "brand_name", "vehicle_image", "vehicle_price", "fuel_type","End Point"]:
#         val = data.get(key)
#         if val and str(val).strip().lower() not in ["not available", "nan", "n/a", ""]:
#             context.append(f"{key}: {val}")
#     return "; ".join(context)

# # Add a set of competitor keywords
# COMPETITOR_KEYWORDS = [
#     'truck junction', 'trucksdekho', 'trucks dekho', 'trucksbazi', 'trucks bazi', 'trucksbazar', 'trucks bazar',
#     'busesdekho', 'buses dekho', 'busesbazar', 'buses bazar', 'busesbazi', 'buses bazi',
#     'carjunction', 'car junction', 'carbazaar', 'car bazaar', 'carbazar', 'car bazar',
#     'bikejunction', 'bike junction', 'bikebazaar', 'bike bazaar', 'bikebazar', 'bike bazar',
#     'tractorjunction', 'tractor junction', 'tractor bazaar', 'tractor bazar', 'tractorjunction',
#     'auto junction', 'auto bazaar', 'auto bazar', 'autojunction',
#     'spinny', 'spinny', 'spinny.com', 'spinny cars', 'spinnycars',
#     'cars24', 'cars 24', 'cars24.com', 'cars24 cars', 'cars24cars',
# ]

# def contains_competitor(text):
#     # Returns True if input text closely matches any competitor keyword (partial match > 85), else False.
#     t = text.lower()
#     for kw in COMPETITOR_KEYWORDS:
#         if fuzz.partial_ratio(kw, t) > 85:
#             return True
#     return False

# def normalize_text(text):
#     # Converts text to lowercase and removes all non-alphanumeric characters.
#     return re.sub(r'[^a-z0-9]', '', str(text).lower())

# def extract_price_filter_improved(prompt_lower):
#     """
#     Improved price filter extraction that handles all variations:
#     - "need tata trucks under 15 lakhs" ✓
#     - "need a truck under price of 15 lakhs" ✓
#     - "trucks under 10 lakh" ✓
#     - "best tata trucks under the 10 lakh" ✓
#     - "vehicles below 20 lakh" ✓
#     - "trucks between 5 and 15 lakh" ✓
#     - "show me trucks under 15 lakh" ✓
#     - "find vehicles below 20 lakh" ✓
#     - "get tata trucks under 10 lakh" ✓
#     - "recommend vehicles under 25 lakh" ✓
#     - "trucks under ₹15 lakh" ✓
#     - "vehicles below 15L" ✓
#     - "trucks under 1.5 crore" ✓
#     - "trucks under 200000" ✓
#     - "trucks under 2l" ✓
#     - "trucks under 2000 thousand" ✓
#     """
#     price_patterns = [
#         r'(under|below|less than|within|over|above|more than)\s*₹?\s*([\d\.]+)\s*(lakhs?|crores?|l|thousand|k)?',
#         r'(under|below|less than|within|over|above|more than)\s+(?:price\s+(?:of\s+)?)?₹?\s*([\d\.]+)\s*(lakhs?|crores?|l|thousand|k)?',
#         r'(under|below|less than|within|over|above|more than)\s+(?:the\s+)?₹?\s*([\d\.]+)\s*(lakhs?|crores?|l|thousand|k)?',
#         r'between\s*₹?\s*([\d\.]+)\s*(lakhs?|crores?|l|thousand|k)?\s*(?:and|to)\s*₹?\s*([\d\.]+)\s*(lakhs?|crores?|l|thousand|k)?',
#         r'best\s+(?:under|below|less than)\s+(?:the\s+)?₹?\s*([\d\.]+)\s*(lakhs?|crores?|l|thousand|k)?',
#         r'₹?\s*([\d\.]+)\s*(lakhs?|crores?|l|thousand|k)\s+(?:and\s+)?(?:under|below|less than)',
#         r'(?:need\s+)?(?:a|the)\s+\w+\s+(under|below|less than|within|over|above|more than)\s+(?:price\s+(?:of\s+)?)?(?:the\s+)?₹?\s*([\d\.]+)\s*(lakhs?|crores?|l|thousand|k)?',
#         r'(?:show\s+me|find|recommend|search\s+for)\s+\w+\s+(under|below|less than|within|over|above|more than)\s+(?:price\s+(?:of\s+)?)?(?:the\s+)?₹?\s*([\d\.]+)\s*(lakhs?|crores?|l|thousand|k)?',
#         r'(under|below|less than|within|over|above|more than)\s*₹?\s*([\d\.]+)\s*l',
#         r'(under|below|less than|within|over|above|more than)\s*₹\s*([\d\.]+)\s*(lakhs?|crores?|l|thousand|k)?',
#         r'(?:any|some|all)\s+\w+\s+(under|below|less than|within|over|above|more than)\s+(?:price\s+(?:of\s+)?)?(?:the\s+)?₹?\s*([\d\.]+)\s*(lakhs?|crores?|l|thousand|k)?',
#         r'(under|below|less than|within|over|above|more than)\s+price\s+₹?\s*([\d\.]+)\s*(lakhs?|crores?|l|thousand|k)?',
#     ]
#     def to_lakh(value, unit):
#         if unit in ['crore']:
#             return float(value) * 100
#         elif unit in ['lakh', 'l']:
#             return float(value)
#         elif unit in ['thousand', 'k']:
#             return float(value) / 100
#         else:
#             # If value is large, treat as rupees
#             value = float(value)
#             if value >= 100000:
#                 return value / 100000
#             elif value >= 1000:
#                 return value / 100
#             else:
#                 return value
#     for pattern in price_patterns:
#         match = re.search(pattern, prompt_lower, re.IGNORECASE)
#         if match:
#             if 'between' in pattern:
#                 price1 = to_lakh(match.group(1), (match.group(2) or '').lower())
#                 price2 = to_lakh(match.group(3), (match.group(4) or '').lower())
#                 return ('between', price1, price2)
#             else:
#                 condition = match.group(1).lower()
#                 price = to_lakh(match.group(2), (match.group(3) or '').lower())
#                 return (condition, price, 'lakh')
#     return None

# def apply_price_filter_improved(df, price_filter):
#     """
#     Apply price filter to dataframe with proper handling of price formats
#     """
#     if not price_filter or 'Price' not in df.columns:
#         return df
    
#     # Create a copy to avoid modifying original
#     df_filtered = df.copy()
    
#     # Convert Price column to numeric, handling various formats
#     def extract_numeric_price(price_val):
#         if pd.isna(price_val) or price_val is None:
#             return None
        
#         price_str = str(price_val).lower().strip()
        
#         # Handle "Coming Soon" or empty values
#         if 'coming soon' in price_str or price_str in ['', 'nan', 'n/a']:
#             return None
        
#         # Remove currency symbols and commas
#         price_str = re.sub(r'[₹,]', '', price_str)
        
#         # Extract numeric value and unit
#         if 'crore' in price_str:
#             match = re.search(r'(\d+\.?\d*)', price_str)
#             if match:
#                 return float(match.group(1)) * 100  # Convert to lakhs
#         elif 'lakh' in price_str:
#             match = re.search(r'(\d+\.?\d*)', price_str)
#             if match:
#                 return float(match.group(1))
#         else:
#             # Try to extract just the number
#             match = re.search(r'(\d+\.?\d*)', price_str)
#             if match:
#                 return float(match.group(1))
        
#         return None
    
#     # Apply price conversion
#     df_filtered['Price_Numeric'] = df_filtered['Price'].apply(extract_numeric_price)
    
#     # Remove rows with invalid prices
#     df_filtered = df_filtered[df_filtered['Price_Numeric'].notna()]
    
#     if df_filtered.empty:
#         return df_filtered
    
#     # Apply the price filter
#     condition, price1, unit1 = price_filter
    
#     if condition in ['under', 'below', 'less than', 'within']:
#         df_filtered = df_filtered[df_filtered['Price_Numeric'] < price1]
#         # Sort by price in descending order to show higher prices first
#         df_filtered = df_filtered.sort_values(by='Price_Numeric', ascending=False)
#     elif condition in ['over', 'above', 'more than']:
#         df_filtered = df_filtered[df_filtered['Price_Numeric'] > price1]
#         # Sort by price in ascending order to show lower prices first
#         df_filtered = df_filtered.sort_values(by='Price_Numeric', ascending=True)
#     elif condition == 'between':
#         price2 = unit1  # In between pattern, unit1 contains price2
#         min_price, max_price = sorted([price1, price2])
#         df_filtered = df_filtered[(df_filtered['Price_Numeric'] >= min_price) & (df_filtered['Price_Numeric'] <= max_price)]
#         # Sort by price in descending order
#         df_filtered = df_filtered.sort_values(by='Price_Numeric', ascending=False)
    
#     return df_filtered

# def is_theory_query(prompt):
#     # theory_patterns = [
#     #     r"what is", r"explain", r"meaning of", r"define", r"difference between", r"how does", r"how do", r"why", r"purpose of", r"concept of", r"benefit of", r"advantage of", r"disadvantage of", r"faq", r"question", r"explanation", r"describe", r"how are you", r"who are you", r"about you", r"about 91trucks",
#     #     r"founder", r"founders", r"who founded", r"who created", r"who started", r"history", r"background", r"information", r"tell me about", r"what can you", r"how can you", r"what do you", r"help me", r"assist", r"guide", r"advice", r"recommendation", r"suggestion",
#     #     r"what are", r"what does", r"what should", r"what would", r"what could", r"how to", r"how should", r"how would", r"how could", r"when to", r"where to", r"which is", r"which are", r"can you", r"could you", r"would you", r"should you",
#     #     r"company", r"business", r"service", r"platform", r"website", r"online", r"digital", r"technology", r"innovation", r"industry", r"market", r"sector", r"field", r"domain", r"area",r"is", r"specialty", r"expertise"
#     # ]
#     theory_patterns = [
#     # Basic Definitions & Explanations
#     r"\bwhat is\b", r"\bwhat are\b", r"\bwhat does\b", r"\bmeaning of\b", r"\bdefine\b", r"\bdefinition of\b", r"\bexplain\b", r"\bexplanation\b", r"\bdescribe\b", r"\bfaq\b", r"\bquestion\b",

#     # Purpose, Concept, Reason
#     r"\bwhy\b", r"\bpurpose of\b", r"\bconcept of\b",

#     # Comparisons
#     r"\bdifference between\b", r"\bhow is\b", r"\bwhich is\b", r"\bwhich are\b", r"\bvs\b",

#     # Advantages / Disadvantages / Benefits
#     r"\badvantage of\b", r"\bdisadvantage of\b", r"\bbenefit of\b", r"\bpros and cons\b",

#     # Functional & How-To
#     r"\bhow to\b", r"\bhow does\b", r"\bhow do\b", r"\bhow can\b", r"\bhow should\b", r"\bhow would\b", r"\bhow could\b",

#     # Actionable Guidance
#     r"\bhelp me\b", r"\bassist\b", r"\bguide\b", r"\badvice\b", r"\brecommendation\b", r"\bsuggestion\b", r"\btips for\b",

#     # Capability Questions
#     r"\bwhat can you\b", r"\bhow can you\b", r"\bwhat do you\b", r"\bcan you\b", r"\bcould you\b", r"\bwould you\b", r"\bshould you\b",r"\What\b",r"\who\b",r"\What is\b",r"\where\b",r"\where is\b"

#     # Questions Starting with "When", "Where", "Which"
#     r"\bwhen to\b", r"\bwhere to\b", r"\bwhich is\b", r"\bwhich are\b", r"\bwhere can\b", r"\bwhen can\b",r"\which\b", r"\bwhich can\b",

#     # Personal/Identity Queries (for bot or company)
#     r"\bwho are you\b", r"\bhow are you\b", r"\babout you\b", r"\babout 91trucks\b", r"\btell me about\b", r"\bwhat do you do\b", r"\bwho made you\b", r"\babout the 91trucks\b", r"\babout the 91 trucks\b",

#     # Company Info Queries
#     r"\bcompany\b", r"\bbusiness\b", r"\bplatform\b", r"\bwebsite\b", r"\bonline\b", r"\bdigital\b", r"\btechnology\b", r"\binnovation\b", r"\bindustry\b", r"\bmarket\b", r"\bsector\b", r"\bfield\b", r"\bdomain\b", r"\barea\b", r"\bspecialty\b", r"\bexpertise\b",

#     # Founders & History
#     r"\bfounder\b", r"\bfounders\b", r"\bwho founded\b", r"\bwho created\b", r"\bwho started\b", r"\bhistory\b", r"\bbackground\b", r"\binformation\b",

#     # Miscellaneous / Edge Cases
#     r"\bcan u\b", r"\bcould u\b", r"\bpls explain\b", r"\bi want to know\b", r"\bi would like to know\b", r"\bneed help with\b", r"\bis\b", r"\bare\b",r"\bcan I\b",r"\bcan\b",
# ]

#     prompt_lower = prompt.lower()
#     return any(re.search(pattern, prompt_lower) for pattern in theory_patterns)

# def process_query(prompt, df_main, brand_names, display_names, qa_chain=None):
#     prompt_lower = prompt.strip().lower()
#     normalized_prompt = normalize_vehicle_name(prompt)
#     normalized_display_names = {normalize_vehicle_name(name): name for name in display_names}

#     # Ensure display_names is a list for indexing
#     if isinstance(display_names, set):
#         display_names = list(display_names)

#     # --- EARLY: Greetings (FIRST PRIORITY) ---
#     if is_greeting(prompt):
#         goodbye_words = {"bye", "goodbye", "see you", "farewell", "take care","byy","by","byby","bye bye","take care","bi","good night","see ya", "later", "catch you later", "take care", "peace", "adios", "au revoir", "good night", "nighty night", "sweet dreams", "cheerio", "bless you", "best wishes", "safe travels", "until next time", "talk soon", "stay safe", "much love", "respect", "big hello","byy","by","byby","bye bye","take care","bi"}
#         prompt_clean = prompt.strip().lower()
#         if any(word in prompt_clean for word in goodbye_words):
#             goodbye_responses = [
#                 "Sad to see you go! If you need commercial vehicle info again, 91 Trucks will be here for you.",
#                 "Goodbye! Have a wonderful day ahead — from all of us at 91 Trucks.",
#                 "Take care! Come back anytime to 91 Trucks for trusted commercial vehicle advice.",
#                 "Farewell! Wishing you safe and successful journeys with your commercial vehicles — 91 Trucks is always ready to help.",
#                 "See you soon! Hope 91 Trucks was helpful in your commercial vehicle search."
#             ]
#             bye_msg = random.choice(goodbye_responses)
#             return {"status": "success", "response": bye_msg}
#         return {"status": "success", "response": "Hello from 91Trucks! How can I assist you today? To explore or purchase a commercial vehicle, visit 91trucks.com – India's #1 platform for commercial vehicles."}

#     # --- EARLY: Competitor keyword detection ---
#     if contains_competitor(prompt):
#         return {"status": "success", "response": "I am a 91Trucks assistant and can only answer questions about 91Trucks and vehicles listed on 91trucks.com."}

#     # --- EARLY: Brand existence check ---
#     # Check if the query is a single brand name that doesn't exist in our dataset
#     # Only check for single brand names, not brand + vehicle combinations
#     available_brands = df_main['Brand Name'].dropna().unique()
#     normalized_available_brands = [normalize_brand_name(brand) for brand in available_brands]
#     normalized_prompt_brand = normalize_brand_name(prompt)
    
#     # Only check for single brand names (not brand + vehicle combinations)
#     # If the prompt contains spaces, it's likely a brand + vehicle combination, so skip this check
#     if normalized_prompt_brand and ' ' not in prompt.strip():
#         # Check if it's a close match to any available brand
#         close_matches = difflib.get_close_matches(normalized_prompt_brand, normalized_available_brands, n=1, cutoff=0.8)
#         if not close_matches:
#             pass  # Do not return, let LLM handle

#     if is_greeting(prompt):
#         goodbye_words = {"bye", "goodbye", "see you", "farewell", "take care","byy","by","byby","bye bye","take care","bi"}
#         prompt_clean = prompt.strip().lower()
#         if any(word in prompt_clean for word in goodbye_words):
#             goodbye_responses = [
#                 "Sad to see you go! If you need commercial vehicle info again, 91 Trucks will be here for you.",
#                 "Goodbye! Have a wonderful day ahead — from all of us at 91 Trucks.",
#                 "Take care! Come back anytime to 91 Trucks for trusted commercial vehicle advice.",
#                 "Farewell! Wishing you safe and successful journeys with your commercial vehicles — 91 Trucks is always ready to help.",
#                 "See you soon! Hope 91 Trucks was helpful in your commercial vehicle search."
#             ]
#             bye_msg = random.choice(goodbye_responses)
#             return {"status": "success", "response": bye_msg}
#         return {"status": "success", "response": "Hello from 91Trucks! How can we assist you today? To explore or purchase a commercial vehicle, visit 91trucks.com – India's #1 platform for commercial vehicles."}

#     # Handle visual/image-related queries politely
#     visual_keywords = [
#         'image', 'photo','image', 'display image'
#     ]
#     if any(word in prompt_lower for word in visual_keywords):
#         return {
#             "status": "success",
#             "response": (
#                 "I can't show images directly, but I can provide descriptions, specs, or guide you to the official 91Trucks or manufacturer websites for visuals."
#             )
#         }

#     # --- EARLY: "Need" and action verb queries with price filters ---
#     action_verbs = ['need', 'show', 'find', 'recommend', 'search']
#     has_action_verb = any(prompt_lower.startswith(verb) for verb in action_verbs)
    
#     if has_action_verb and extract_price_filter_improved(prompt_lower):
#         # Handle queries like "need tata trucks under 15 lakhs", "need a truck under price of 15 lakhs"
#         price_filter = extract_price_filter_improved(prompt_lower)
        
#         # Extract brand and category from the query
#         brand_match = None
#         category_match = None
        
#         # Check for brand names
#         for brand in brand_names:
#             if brand.lower() in prompt_lower:
#                 brand_match = brand
#                 break
        
#         # Check for category keywords
#         category_keywords = ['truck', 'trucks', 'bus', 'buses', 'auto', 'rickshaw', 'tractor', 'trailer', 'vehicle', 'vehicles']
#         for keyword in category_keywords:
#             if keyword in prompt_lower:
#                 category_match = keyword
#                 break
        
#         # Apply filters
#         df_filtered = df_main.copy()
        
#         # Apply brand filter
#         if brand_match:
#             df_filtered = df_filtered[df_filtered['Brand Name'].str.lower().str.contains(brand_match.lower())]
        
#         # Apply category filter
#         if category_match and 'Category Name' in df_filtered.columns:
#             category_mapping = {
#                 'truck': 'Truck', 'trucks': 'Truck',
#                 'bus': 'Bus', 'buses': 'Bus',
#                 'auto': 'Auto Rickshaws', 'rickshaw': 'Auto Rickshaws',
#                 'tractor': 'Tractor', 'trailer': 'Trailer',
#                 'vehicle': None, 'vehicles': None  # Don't filter by category for general vehicle queries
#             }
#             target_category = category_mapping.get(category_match.lower(), category_match)
#             if target_category:  # Only apply category filter if we have a specific category
#                 df_filtered = df_filtered[df_filtered['Category Name'].str.lower() == target_category.lower()]
        
#         # Apply price filter
#         if price_filter:
#             df_filtered = apply_price_filter_improved(df_filtered, price_filter)
        
#         # Get top vehicles by rating if available
#         if 'Rating' in df_filtered.columns:
#             df_filtered = df_filtered.sort_values(by='Rating', ascending=False)
        
#         # Return top 5 vehicles
#         selected_vehicles= []
#         used_models = set()
#         for _, row in df_filtered.iterrows():
#             if len(selected_vehicles) >= 10:
#                 break
#             vehicle_data = get_vehicle_data_with_id_by_index(row)
#             if vehicle_data and vehicle_data.get('vehicle_name') not in used_models:
                
#                 selected_vehicles.append(vehicle_data)
#                 used_models.add(vehicle_data.get('vehicle_name'))
        
#         if selected_vehicles:
#             return {"status": "success", "response": {"possible_matches": selected_vehicles}}
#         else:
#             return {"status": "success", "response": "I couldn't find any vehicles matching your criteria. Please try adjusting your search parameters."}

#     # --- EARLY: Theoretical/Informational queries ---
#     if is_theory_query(prompt) and qa_chain:
#         try:
#             retriever = vector_store.as_retriever()
#             docs = retriever.get_relevant_documents(prompt)
#             context = "\n".join([doc.page_content for doc in docs]) if docs else ""
#             result = qa_chain.invoke({"question": prompt, "context": context})
#             if isinstance(result, dict):
#                 answer = result.get("result") or "Sorry, I couldn't find an answer to that."
#             else:
#                 answer = result or "Sorry, I couldn't find an answer to that."
#             answer = clean_llm_output(answer)
#         except Exception as e:
#             answer = "I'm currently experiencing technical difficulties. Please try again in a few moments or ask about specific vehicles in our database."
#         answer = remove_duplicate_website_links(answer)
#         answer = strip_markdown(answer)
#         # Enhance the response with vehicle details instead of links
#         answer = enhance_llm_response_with_vehicle_details(answer, df_main, display_names)
#         # Try to attach a vehicle card if the text clearly points to a single vehicle
#         vehicle_card = find_vehicle_from_text(f"{prompt} \n {answer}", display_names, df_main)
#         if vehicle_card:
#             return {"status": "success", "response": answer, "vehicle": vehicle_card}
#         # Attach vehicle card when detectable
#         vehicle_card = find_vehicle_from_text(f"{prompt} \n {answer}", display_names, df_main)
#         if vehicle_card:
#             return {"status": "success", "response": answer, "vehicle": vehicle_card}
#         vehicle_card = find_vehicle_from_text(f"{prompt} \n {answer}", display_names, df_main)
#         if vehicle_card:
#             return {"status": "success", "response": answer, "vehicle": vehicle_card}
#         vehicle_card = find_vehicle_from_text(f"{prompt} \n {answer}", display_names, df_main)
#         if vehicle_card:
#             return {"status": "success", "response": answer, "vehicle": vehicle_card}
#         return {"status": "success", "response": answer}

#     # --- EARLY: Comparison queries ---
#     if (" vs " in prompt_lower or " versus " in prompt_lower or "compare" in prompt_lower) and qa_chain:
#         match = re.split(r'\s+and\s+|\s+with\s+|\s+versus\s+|\s+vs\s+|\s+compare\s+', prompt_lower)
#         if len(match) == 2:
#             v1_name = match[0].strip()
#             v2_name = match[1].strip()
#             v1_best = difflib.get_close_matches(v1_name, [name.lower() for name in display_names], n=1)
#             v2_best = difflib.get_close_matches(v2_name, [name.lower() for name in display_names], n=1)
#             v1_data = get_vehicle_data(v1_best[0], df_main) if v1_best else None
#             v2_data = get_vehicle_data(v2_best[0], df_main) if v2_best else None
#             if v1_data and v2_data:
#                 # Special case: Tata Intra V30 vs Mahindra Zeo (any order)
#                 names = {v1_data.get('vehicle_name', '').lower(), v2_data.get('vehicle_name', '').lower()}
#                 if names == {'tata intra v30', 'mahindra zeo'}:
#                     summary = (
#                         "The Tata Intra V30 is a diesel-powered vehicle, while the Mahindra Zeo is an electric vehicle.  "
#                         "The Mahindra Zeo has a higher average rating (4.6) compared to the Tata Intra V30 (3.3). * The Tata Intra V30 is priced slightly higher than the Mahindra Zeo.  "
#                         "Recommendation: If you're looking for an eco-friendly option with lower operating costs, the Mahindra Zeo might be a better fit. However, if you prefer a diesel-powered vehicle, the Tata Intra V30 could be a suitable choice."
#                     )
#                     return {
#                         "status": "success",
#                         "response": {
#                             "vehicles": [v1_data, v2_data],
#                             "summary": summary
#                         }
#                     }
#                 # Default: LLM-generated summary
#                 context = f"Vehicle 1: {get_vehicle_context(v1_data)}\nVehicle 2: {get_vehicle_context(v2_data)}"
#                 result = qa_chain.invoke({"question": prompt, "context": context})
#                 summary = clean_llm_output(result.get("result") if isinstance(result, dict) else result)
#                 summary = remove_duplicate_website_links(summary)
#                 summary = strip_markdown(summary)
#                 # Enhance the response with vehicle details instead of links
#                 summary = enhance_llm_response_with_vehicle_details(summary, df_main, display_names)
#                 # Extract recommended vehicle name from summary
#                 recommended_vehicle = None
#                 vehicles_list = [v1_data, v2_data]
#                 # Try to find a vehicle name after 'choose' or 'recommendation:'
#                 match = re.search(r'(choose|recommendation:|recommend)\s+([a-zA-Z0-9\- ]+)', summary, re.IGNORECASE)
#                 if match:
#                     rec_name = match.group(2).strip().lower()
#                     for v in vehicles_list:
#                         if rec_name in v.get('vehicle_name', '').lower() or rec_name in v.get('model_name', '').lower():
#                             recommended_vehicle = v
#                             break
#                 # Fallback: if not found, try fuzzy match with vehicle names
#                 if not recommended_vehicle:
#                     for v in vehicles_list:
#                         if v.get('vehicle_name', '').lower() in summary.lower() or v.get('model_name', '').lower() in summary.lower():
#                             recommended_vehicle = v
#                             break
#                 # Detect if this is a comparison query
#                 if re.search(r"\bcompare\b|\bvs\b|\bversus\b|\bwith\b|\band\b", prompt_lower, re.IGNORECASE):
#                     return {
#                     "status": "success",
#                     "response": {
#                             "summary": summary,
#                             "vehicles": vehicles_list
#                         }
#                     }
#                 else:
#                     return {
#                         "status": "success",
#                         "response": {
#                             "summary": summary,
#                             "vehicle": recommended_vehicle
#                     }
#                 }
#             else:
#                 return {
#                     "status": "error",
#                     "response": "Please provide the full names of both vehicles for comparison using , eg-'Tata Intra V30 vs Mahindra Jeeto' or 'Tata Intra V30 with Mahindra Jeeto' or' Tata Intra V30 and Mahindra Jeeto.'"
#                 }
#         else:
#             return {
#                 "status": "error",
#                 "response": "Please provide the full names of both vehicles for comparison using , eg-'Tata Intra V30 vs Mahindra Jeeto' or 'Tata Intra V30 with Mahindra Jeeto' or' Tata Intra V30 and Mahindra Jeeto.'"
#             }

#     def get_top_matches_and_nearest(df, price_col, direction, threshold, n=4, exclude_names=None, between_range=None):
#         # direction: 'under', 'over', or 'between'
#         exclude_names = exclude_names or []
#         df = df[~df['Vehicle Name'].isin(exclude_names)]
#         df[price_col] = pd.to_numeric(df[price_col], errors='coerce')
#         matches = pd.DataFrame()
#         nearest = pd.DataFrame()
#         if direction == 'under':
#             matches = df[df[price_col] < threshold].sort_values(by=price_col, ascending=False).head(n)
#             if len(matches) < n:
#                 # Fill with next closest vehicles below threshold, not including threshold or above
#                 remaining_needed = n - len(matches)
#                 # Exclude already matched vehicles
#                 below = df[(df[price_col] < threshold) & (~df['Vehicle Name'].isin(matches['Vehicle Name']))]
#                 below = below.sort_values(by=price_col, ascending=False).head(remaining_needed)
#                 matches = pd.concat([matches, below]).drop_duplicates(subset=['Vehicle Name']).head(n)
#         elif direction == 'over':
#             matches = df[df[price_col] > threshold].sort_values(by=price_col).head(n)
#             if len(matches) < n:
#                 nearest = df[(df[price_col] > threshold) & (~df['Vehicle Name'].isin(matches['Vehicle Name']))]
#                 nearest = nearest.sort_values(by=price_col).head(n - len(matches))
#                 matches = pd.concat([matches, nearest]).drop_duplicates(subset=['Vehicle Name']).head(n)
#         elif direction == 'between' and between_range:
#             min_p, max_p = between_range
#             matches = df[(df[price_col] > min_p) & (df[price_col] < max_p)].sort_values(by=price_col).head(n)
#             if len(matches) < n:
#                 # Try to fill with nearest inside, then outside
#                 inside = df[(df[price_col] > min_p) & (df[price_col] < max_p) & (~df['Vehicle Name'].isin(matches['Vehicle Name']))]
#                 inside = inside.sort_values(by=price_col).head(n - len(matches))
#                 matches = pd.concat([matches, inside]).head(n)
#                 if len(matches) < n:
#                     outside = df[(df[price_col] <= min_p) | (df[price_col] >= max_p)]
#                     outside['dist'] = outside[price_col].apply(lambda x: min(abs(x - min_p), abs(x - max_p)) if pd.notnull(x) else float('inf'))
#                     outside = outside.sort_values(by='dist').head(n - len(matches))
#                     matches = pd.concat([matches, outside]).head(n)
#         all_matches = matches.drop_duplicates(subset=['Vehicle Name']).head(n)
#         return [get_vehicle_data_with_id_by_index(row) for _, row in all_matches.iterrows() if get_vehicle_data_with_id_by_index(row)]

#     # --- CARD LOGIC: 1. Brand-only, 2. Brand+Category, 3. Card-phrase, 4. Vehicle/model name ---
#     brands = set(df_main['Brand Name'].str.lower().unique())
#     categories = set(df_main['Category Name'].str.lower().unique()) if 'Category Name' in df_main.columns else set()
#     vehicle_names = [normalize_vehicle_name_unique(name) for name in display_names]
#     # More precise brand detection - avoid partial matches like "ele" from "electric"
#     prompt_brand_match = None
#     for b in brands:
#         # Check for word boundaries to avoid partial matches
#         if re.search(rf'\b{re.escape(b)}\b', prompt_lower):
#             prompt_brand_match = b
#             break
#     # Enhanced category detection with mapping
#     category_mapping = {
#         'truck': 'Truck',
#         'trucks': 'Truck',
#         'bus': 'Bus', 
#         'buses': 'Bus',
#         'auto': 'Auto Rickshaws',
#         'auto rickshaw': 'Auto Rickshaws',
#         'auto rickshaws': 'Auto Rickshaws',
#         'auto rickshaw 3 wheelers': 'Auto Rickshaws',
#         'auto rickshaw 3 wheeler': 'Auto Rickshaws',
#         '3 wheelers': 'Auto Rickshaws',
#         '3 wheeler': 'Auto Rickshaws',
#         'three wheelers':'Auto Rickshaws',
#         'three wheeler':'Auto Rickshaws',
#         'rickshaw': 'Auto Rickshaws',
#         'rickshaws': 'Auto Rickshaws',
#         'tractor': 'Tractor',
#         'tractors': 'Tractor',
#         'trailer': 'Trailer',
#         'trailers': 'Trailer',
#         'cargo': 'Cargo',
#         'cargo van': 'Cargo Van',
#         'cargo vans': 'Cargo Van',
#         'pickup': 'Pickup',
#         'pickups': 'Pickup',
#         'mini truck': 'Mini Truck',
#         'mini trucks': 'Mini Truck',
#         'minitruck': 'Mini Truck',
#         'minitrucks': 'Mini Truck'
#     }
    
#     # Check for category matches in the prompt
#     prompt_category_match = None
#     for category_term, mapped_category in category_mapping.items():
#         if category_term in prompt_lower:
#             prompt_category_match = mapped_category
#             break
#     card_phrases = [
#     "show me trucks", "show me buses", "show me vehicles",
#     "get me trucks", "get me buses", "get me vehicles", 
#     "display trucks", "display buses", "display vehicles",
#     "list trucks", "list buses", "list vehicles",
#     "variants", "variant", "models", "model","how many variants",
#     "how many models", "how many variants of", "how many models of",
#     "show variants", "show models", "show me variants", "show me models",
#     "get variants", "get models", "get me variants", "get me models",
#     "display variants", "display models", "display variants of", "display models of",
#     "list variants", "list models", "list variants of", "list models of",
#     "variants of", "models of"

    
# ]
    
    
#     # Multi-category logic for brand + general vehicle terms
#     def get_mixed_category_vehicles_for_brand(brand_name, fuel_filter=None, max_vehicles=5, price_filter=None):
#         """Get diverse vehicles from a brand across different categories"""
#         df_filtered = df_main[df_main['Brand Name'].str.lower().str.contains(brand_name.lower())]
        
#         # Apply fuel type filter if specified
#         if fuel_filter:
#             if fuel_filter.lower() == 'electric':
#                 if 'Electric' in df_filtered.columns:
#                     df_filtered = df_filtered[df_filtered['Electric'].str.lower() == 'yes']
#                 if 'Fuel Type' in df_filtered.columns:
#                     df_filtered = df_filtered[df_filtered['Fuel Type'].str.lower().str.contains('electric', na=False)]
#             elif fuel_filter.lower() == 'diesel':
#                 if 'Fuel Type' in df_filtered.columns:
#                     df_filtered = df_filtered[df_filtered['Fuel Type'].str.lower().str.contains('diesel', na=False)]
#             elif fuel_filter.lower() == 'cng':
#                 if 'Fuel Type' in df_filtered.columns:
#                     df_filtered = df_filtered[df_filtered['Fuel Type'].str.lower().str.contains('cng', na=False)]
#             elif fuel_filter.lower() == 'petrol':
#                 if 'Fuel Type' in df_filtered.columns:
#                     df_filtered = df_filtered[df_filtered['Fuel Type'].str.lower().str.contains('petrol', na=False)]
        
#         # Apply category filter if specified (e.g., "trucks", "buses")
#         # This will be passed from the calling function based on the prompt
#         if 'truck' in prompt_lower or 'trucks' in prompt_lower:
#             if 'Category Name' in df_filtered.columns:
#                 df_filtered = df_filtered[df_filtered['Category Name'].str.lower() == 'truck']
#         elif 'bus' in prompt_lower or 'buses' in prompt_lower:
#             if 'Category Name' in df_filtered.columns:
#                 df_filtered = df_filtered[df_filtered['Category Name'].str.lower() == 'bus']
#         elif 'auto' in prompt_lower or 'rickshaw' in prompt_lower:
#             if 'Category Name' in df_filtered.columns:
#                 df_filtered = df_filtered[df_filtered['Category Name'].str.lower() == 'auto rickshaws']
        
#         # Apply price filter if specified using improved function
#         if price_filter:
#             df_filtered = apply_price_filter_improved(df_filtered, price_filter)
        
#         # Check if we have any vehicles after all filters
#         if df_filtered.empty:
#             return []
        
#         # Additional check: if we have no vehicles after fuel and category filtering, return empty
#         if len(df_filtered) == 0:
#             return []
        
#         # Group by category and get diverse selection
#         category_groups = {}
#         if 'Category Name' in df_filtered.columns:
#             for category in df_filtered['Category Name'].unique():
#                 if pd.notna(category):
#                     category_groups[category] = df_filtered[df_filtered['Category Name'] == category]
        
#         # Distribute vehicles across categories
#         selected_vehicles = []
#         used_models = set()
        
#         # Calculate how many from each category (aim for diversity)
#         total_categories = len(category_groups)
#         if total_categories == 0:
#             # No category info, just take first 5 (sorted by price in descending order)
#             for _, row in df_filtered.iterrows():
#                 if len(selected_vehicles) >= max_vehicles:
#                     break
#                 vehicle_data = get_vehicle_data_with_id_by_index(row)
#                 if vehicle_data and vehicle_data.get('vehicle_name') not in used_models and vehicle_data.get('vehicle_price', '').strip().lower() != 'coming soon':
#                     selected_vehicles.append(vehicle_data)
#                     used_models.add(vehicle_data.get('vehicle_name'))
#         else:
#             # Distribute across categories
#             vehicles_per_category = max(1, max_vehicles // total_categories)
#             remaining_vehicles = max_vehicles % total_categories
            
#             for category, category_df in category_groups.items():
#                 category_count = vehicles_per_category + (1 if remaining_vehicles > 0 else 0)
#                 remaining_vehicles -= 1
                
#                 for _, row in category_df.iterrows():
#                     if len(selected_vehicles) >= max_vehicles:
#                         break
#                     vehicle_data = get_vehicle_data_with_id_by_index(row)
#                     if vehicle_data and vehicle_data.get('vehicle_name') not in used_models and vehicle_data.get('vehicle_price', '').strip().lower() != 'coming soon':
#                         selected_vehicles.append(vehicle_data)
#                         used_models.add(vehicle_data.get('vehicle_name'))
#                         if len([v for v in selected_vehicles if v.get('category_name') == category]) >= category_count:
#                             break
        
#         # Sort selected vehicles by price in descending order to show higher prices first
#         selected_vehicles.sort(key=lambda x: float(x.get('vehicle_price', '0').replace('Lakh', '').replace('Crore', '').replace('Coming Soon', '0')), reverse=True)
        
#         # Ensure we only return vehicles that actually match the criteria
#         final_vehicles = selected_vehicles[:max_vehicles]
        
#         # Double-check that all vehicles are from the requested brand
#         if brand_name:
#             final_vehicles = [v for v in final_vehicles if v.get('brand_name', '').lower() == brand_name.lower()]
        
#         return final_vehicles
    
#     # 1. Brand + General Vehicle Terms (Multi-category logic)
#     brand_vehicle_patterns = [
#         r'(\w+)\s+(electric\s+)?vehicles?',
#         r'(\w+)\s+(diesel\s+)?vehicles?',
#         r'(\w+)\s+(cng\s+)?vehicles?',
#         r'(\w+)\s+(petrol\s+)?vehicles?',
#         r'(\w+)\s+evs?',
#         r'(\w+)\s+electric\s+cars?',
#         r'(\w+)\s+diesel\s+trucks?',
#         r'(\w+)\s+cng\s+buses?',
#         r'(\w+)\s+petrol\s+trucks?',  # Specific pattern for "eicher petrol trucks"
#         r'(\w+)\s+diesel\s+trucks?',
#         r'(\w+)\s+electric\s+trucks?',
#         r'(\w+)\s+cng\s+trucks?'
#     ]
    
#     for pattern in brand_vehicle_patterns:
#         match = re.search(pattern, prompt_lower)
#         if match:
#             brand_name = match.group(1)
#             fuel_type = None
#             if 'electric' in prompt_lower or 'ev' in prompt_lower:
#                 fuel_type = 'electric'
#             elif 'diesel' in prompt_lower:
#                 fuel_type = 'diesel'
#             elif 'cng' in prompt_lower:
#                 fuel_type = 'cng'
#             elif 'petrol' in prompt_lower:
#                 fuel_type = 'petrol'
            
#             # Extract price filter if present using improved function
#             price_filter = extract_price_filter_improved(prompt_lower)
            
#             # Check if brand exists in our data
#             if brand_name.lower() in brands:
#                 mixed_vehicles = get_mixed_category_vehicles_for_brand(brand_name, fuel_type, 5, price_filter)
#                 if mixed_vehicles:
#                     # Ensure all vehicles are from the requested brand
#                     filtered_vehicles = [v for v in mixed_vehicles if v.get('brand_name', '').lower() == brand_name.lower()]
#                     if filtered_vehicles:
#                         return {"status": "success", "response": {"possible_matches": filtered_vehicles}}
#                     else:
#                         return {"status": "success", "response": f"No {fuel_type} vehicles found for {brand_name} in our database."}
#                 else:
#                     return {"status": "success", "response": f"No {fuel_type} vehicles found for {brand_name} in our database."}
    
#     # 2. Brand-only (existing logic) - only if the entire prompt is exactly a brand name
#     if prompt.strip().lower() in brands:
#         n_cards = 5
#         df_filtered = df_main[df_main['Brand Name'].str.lower().str.contains(prompt_brand_match)]
#         if 'Rating' in df_filtered.columns:
#             df_filtered = df_filtered.sort_values(by='Rating', ascending=False)
#         # Prevent duplicate models
#         matches = []
#         used_models = set()
#         for _, row in df_filtered.iterrows():
#             if len(matches) >= n_cards:
#                 break
#             vehicle_data = get_vehicle_data_with_id_by_index(row)
#             if vehicle_data:
#                 model_name = vehicle_data.get('vehicle_name', '').strip()
#                 if model_name and model_name not in used_models:
#                     matches.append(vehicle_data)
#                     used_models.add(model_name)
#         matches = [v for v in matches if v]
#         if matches:
#             return {"status": "success", "response": {"possible_matches": matches}}
#         return {"status": "success", "response": "There are no vehicles in the Knowledgebase matching your criteria."}
#     # 2. Fuel-only queries (without brand) - NEW HANDLER
#     if not prompt_brand_match and prompt_category_match and any(fuel in prompt_lower for fuel in ['electric', 'diesel', 'cng', 'petrol']):
#         # Handle queries like "electric buses", "diesel trucks", "cng rickshaws"
#         n_cards = 5
#         df_filtered = df_main.copy()
        
#         # Apply category filter
#         if 'Category Name' in df_filtered.columns:
#             # Map user input to exact category names
#             category_mapping = {
#                 'truck': 'Truck',
#                 'trucks': 'Truck',
#                 'bus': 'Bus', 
#                 'buses': 'Bus',
#                 'auto': 'Auto Rickshaws',
#                 'auto rickshaw': 'Auto Rickshaws',
#                 'auto rickshaws': 'Auto Rickshaws',
#                 'rickshaw': 'Auto Rickshaws',
#                 'rickshaws': 'Auto Rickshaws',
#                 'tractor': 'Tractor',
#                 'tractors': 'Tractor',
#                 'trailer': 'Trailer',
#                 'trailers': 'Trailer',
#                 'cargo': 'Cargo',
#                 'cargo van': 'Cargo Van',
#                 'cargo vans': 'Cargo Van',
#                 'pickup': 'Pickup',
#                 'pickups': 'Pickup',
#                 'mini truck': 'Mini Truck',
#                 'mini trucks': 'Mini Truck',
#                 'minitruck': 'Mini Truck',
#                 'minitrucks': 'Mini Truck'
#             }
            
#             # Get the exact category name to match
#             target_category = category_mapping.get(prompt_category_match.lower(), prompt_category_match)
            
#             # Apply category filter
#             df_filtered = df_filtered[df_filtered['Category Name'].str.lower() == target_category.lower()]
            
#             if len(df_filtered) == 0:
#                 return {"status": "success", "response": f"No {prompt_category_match} found in the Knowledgebase."}
        
#         # Apply fuel type filter
#         fuel_filter = None
#         if 'electric' in prompt_lower or 'ev' in prompt_lower:
#             fuel_filter = 'electric'
#         elif 'diesel' in prompt_lower:
#             fuel_filter = 'diesel'
#         elif 'cng' in prompt_lower:
#             fuel_filter = 'cng'
#         elif 'petrol' in prompt_lower:
#             fuel_filter = 'petrol'
        
#         if fuel_filter:
#             if fuel_filter == 'electric':
#                 # Create a mask for electric vehicles
#                 electric_mask = pd.Series([False] * len(df_filtered), index=df_filtered.index)
                
#                 # Check Electric column
#                 if 'Electric' in df_filtered.columns:
#                     electric_mask |= df_filtered['Electric'].str.lower().str.contains('yes|true|1', na=False)
                
#                 # Check Fuel Type column
#                 if 'Fuel Type' in df_filtered.columns:
#                     electric_mask |= df_filtered['Fuel Type'].str.lower().str.contains('electric', na=False)
                
#                 # Check Vehicle Name for electric keywords
#                 if 'Vehicle Name' in df_filtered.columns:
#                     electric_mask |= df_filtered['Vehicle Name'].str.lower().str.contains('electric|e-|ev', na=False)
                
#                 # Apply the electric filter
#                 df_filtered = df_filtered[electric_mask]
            
#             elif fuel_filter == 'diesel':
#                 if 'Fuel Type' in df_filtered.columns:
#                     df_filtered = df_filtered[df_filtered['Fuel Type'].str.lower().str.contains('diesel', na=False)]
            
#             elif fuel_filter == 'cng':
#                 if 'Fuel Type' in df_filtered.columns:
#                     df_filtered = df_filtered[df_filtered['Fuel Type'].str.lower().str.contains('cng', na=False)]
            
#             elif fuel_filter == 'petrol':
#                 if 'Fuel Type' in df_filtered.columns:
#                     df_filtered = df_filtered[df_filtered['Fuel Type'].str.lower().str.contains('petrol', na=False)]
        
#         # Apply price filter if present
#         price_filter = extract_price_filter_improved(prompt_lower)
#         if price_filter:
#             df_filtered = apply_price_filter_improved(df_filtered, price_filter)
        
#         # Sort by rating if available
#         if 'Rating' in df_filtered.columns:
#             df_filtered = df_filtered.sort_values(by='Rating', ascending=False)

#         # Check if we have any vehicles after all filters
#         if len(df_filtered) == 0:
#             return {"status": "success", "response": f"No {prompt_category_match} with {fuel_filter} fuel type found in the Knowledgebase."}
        
#         # Get diverse vehicles across brands
#         def get_diverse_vehicles(df, max_vehicles=5):
#             """Get diverse vehicles across different brands"""
#             matches = []
#             used_models = set()
#             used_brands = set()
            
#             # First, try to get one vehicle from each brand
#             brand_groups = df.groupby('Brand Name')
#             for brand_name, brand_df in brand_groups:
#                 if len(matches) >= max_vehicles:
#                     break
#                 for _, row in brand_df.iterrows():
#                     vehicle_data = get_vehicle_data_with_id_by_index(row)
#                     if (vehicle_data and 
#                         vehicle_data.get('vehicle_price', '').strip().lower() != 'coming soon' and
#                         vehicle_data.get('vehicle_name', '').strip() not in used_models):
                        
#                         matches.append(vehicle_data)
#                         used_models.add(vehicle_data.get('vehicle_name', '').strip())
#                         used_brands.add(brand_name)
#                         break  # Only take one from each brand initially
            
#             # If we still have space, fill with remaining vehicles
#             if len(matches) < max_vehicles:
#                 for _, row in df.iterrows():
#                     if len(matches) >= max_vehicles:
#                         break
#                     vehicle_data = get_vehicle_data_with_id_by_index(row)
#                     if (vehicle_data and 
#                         vehicle_data.get('vehicle_price', '').strip().lower() != 'coming soon' and
#                         vehicle_data.get('vehicle_name', '').strip() not in used_models):
                        
#                         matches.append(vehicle_data)
#                         used_models.add(vehicle_data.get('vehicle_name', '').strip())
#                         used_brands.add(brand_name)
#                         break  # Only take one from each brand initially
            
#             return matches
        
        
#         matches = get_diverse_vehicles(df_filtered, n_cards)
#         matches = [v for v in matches if v]
#         if matches:
#             return {"status": "success", "response": {"possible_matches": matches}}
#         return {"status": "success", "response": "I apologize, but I couldn't find any vehicles matching your criteria in our database. Please check the vehicles listed on 91Trucks for accurate information about available commercial vehicles."}

#     # 3. Brand+Category
#     if prompt_brand_match and prompt_category_match:
#         n_cards = 5
#         df_filtered = df_main[df_main['Brand Name'].str.lower().str.contains(prompt_brand_match)]
#         brand_df_all = df_filtered.copy()
        
#         # Remove "Coming Soon" vehicles from both DataFrames - they should never be displayed
#         if 'Vehicle Price' in df_filtered.columns:
#             # More robust filtering for "Coming Soon" vehicles
#             coming_soon_mask = df_filtered['Vehicle Price'].str.lower().str.contains('coming soon', na=False)
#             df_filtered = df_filtered[~coming_soon_mask]
#             brand_df_all = brand_df_all[~coming_soon_mask]
#         if 'Category Name' in df_filtered.columns:
#             category_mapping = {
#                 'truck': 'Truck', 'trucks': 'Truck',
#                 'bus': 'Bus', 'buses': 'Bus',
#                 'auto': 'Auto Rickshaws', 'auto rickshaw': 'Auto Rickshaws', 'auto rickshaws': 'Auto Rickshaws',
#                 'rickshaw': 'Auto Rickshaws', 'rickshaws': 'Auto Rickshaws',
#                 'tractor': 'Tractor', 'tractors': 'Tractor',
#                 'trailer': 'Trailer', 'trailers': 'Trailer',
#                 'cargo': 'Cargo', 'cargo van': 'Cargo Van', 'cargo vans': 'Cargo Van',
#                 'pickup': 'Pickup', 'pickups': 'Pickup',
#                 'mini truck': 'Mini Truck', 'mini trucks': 'Mini Truck', 'minitruck': 'Mini Truck', 'minitrucks': 'Mini Truck'
#             }
#             target_category = category_mapping.get(prompt_category_match.lower(), prompt_category_match)
#             df_exact = df_filtered[df_filtered['Category Name'].str.lower() == target_category.lower()]
#             df_filtered = df_exact
#             if len(df_filtered) == 0:
#                 return {"status": "success", "response": f"No {prompt_category_match} found in the Knowledgebase."}
#         # Sort by Rating if present

#         price_filter = extract_price_filter_improved(prompt_lower)
#         if price_filter:
#             df_filtered = apply_price_filter_improved(df_filtered, price_filter)
#         # --- Attribute filters: combine with brand/category if present ---
#         if 'electric' in prompt_lower:
            
#             # Create a mask for electric vehicles
#             electric_mask = pd.Series([False] * len(df_filtered), index=df_filtered.index)
            
#             # Check Electric column
#             if 'Electric' in df_filtered.columns:
#                 electric_mask |= df_filtered['Electric'].str.lower().str.contains('yes|true|1', na=False)
            
#             # Check Fuel Type column
#             if 'Fuel Type' in df_filtered.columns:
#                 electric_mask |= df_filtered['Fuel Type'].str.lower().str.contains('electric', na=False)
            
#             # Check Vehicle Name for electric keywords
#             if 'Vehicle Name' in df_filtered.columns:
#                 electric_mask |= df_filtered['Vehicle Name'].str.lower().str.contains('electric|e-|ev', na=False)
            
#             # Apply the electric filter
#             df_filtered = df_filtered[electric_mask]
#         if 'high payload' in prompt_lower or 'maximum payload' in prompt_lower or 'max payload' in prompt_lower:
#             if 'Payload' in df_filtered.columns:
#                 df_filtered['Payload'] = pd.to_numeric(df_filtered['Payload'], errors='coerce')
#                 df_filtered = df_filtered[df_filtered['Payload'].notna()]
#                 df_filtered = df_filtered.sort_values(by='Payload', ascending=False)
#         if 'high mileage' in prompt_lower or 'maximum mileage' in prompt_lower or 'max mileage' in prompt_lower or 'best mileage' in prompt_lower:
#             if 'Mileage' in df_filtered.columns:
#                 df_filtered['Mileage'] = pd.to_numeric(df_filtered['Mileage'], errors='coerce')
#                 df_filtered = df_filtered[df_filtered['Mileage'].notna()]
#                 df_filtered = df_filtered.sort_values(by='Mileage', ascending=False)

        
#         # --- CNG filter logic ---
#         if 'cng' in prompt_lower:
            
#             # Create a mask for CNG vehicles
#             cng_mask = pd.Series([False] * len(df_filtered), index=df_filtered.index)
            
#             # Check Fuel Type column for CNG
#             if 'Fuel Type' in df_filtered.columns:
#                 cng_mask |= df_filtered['Fuel Type'].str.lower().str.contains('cng', na=False)

#             # Check Vehicle Name for CNG keywords
#             if 'Vehicle Name' in df_filtered.columns:
#                 cng_mask |= df_filtered['Vehicle Name'].str.lower().str.contains('cng', na=False)
            
#             # Apply the CNG filter
#             df_filtered = df_filtered[cng_mask]
        
#         # --- Petrol filter logic ---
#         if 'petrol' in prompt_lower:
            
#             # Create a mask for Petrol vehicles
#             petrol_mask = pd.Series([False] * len(df_filtered), index=df_filtered.index)
            
#             # Check Fuel Type column for Petrol
#             if 'Fuel Type' in df_filtered.columns:
#                 petrol_mask |= df_filtered['Fuel Type'].str.lower().str.contains('petrol', na=False)

#             # Check Vehicle Name for Petrol keywords
#             if 'Vehicle Name' in df_filtered.columns:
#                 petrol_mask |= df_filtered['Vehicle Name'].str.lower().str.contains('petrol', na=False)
            
#             # Apply the Petrol filter
#             df_filtered = df_filtered[petrol_mask]
        
#         # --- Diesel filter logic ---
#         if 'diesel' in prompt_lower:
            
#             # Create a mask for Diesel vehicles
#             diesel_mask = pd.Series([False] * len(df_filtered), index=df_filtered.index)
            
#             # Check Fuel Type column for Diesel
#             if 'Fuel Type' in df_filtered.columns:
#                 diesel_mask |= df_filtered['Fuel Type'].str.lower().str.contains('diesel', na=False)
#             # Check Vehicle Name for Diesel keywords
#             if 'Vehicle Name' in df_filtered.columns:
#                 diesel_mask |= df_filtered['Vehicle Name'].str.lower().str.contains('diesel', na=False)
            
#             # Apply the Diesel filter
#             df_filtered = df_filtered[diesel_mask]
#         if 'Rating' in df_filtered.columns:
#             df_filtered = df_filtered.sort_values(by='Rating', ascending=False)
#         # Build up to 5 vehicles
#         matches = []
#         used_models = set()
#         for _, row in df_filtered.iterrows():
#             if len(matches) >= n_cards:
#                 break
#             vehicle_data = get_vehicle_data_with_id_by_index(row)
#             if vehicle_data and vehicle_data.get('vehicle_name', '').strip() not in used_models:
#                 matches.append(vehicle_data)
#                 used_models.add(vehicle_data.get('vehicle_name', '').strip())
#         # Don't backfill - only show vehicles that match the criteria
#         # This ensures we don't show non-matching vehicles just to reach 5
#         matches = [v for v in matches if v]
#         if matches:
#             return {"status": "success", "response": {"possible_matches": matches}}
#     # 4. Card-phrase queries OR Category+Price queries (should always show cards)
#     has_card_phrase = any(phrase in prompt_lower for phrase in card_phrases)
#     has_category_and_price = prompt_category_match and any(word in prompt_lower for word in ['under', 'below', 'less than', 'within', 'over', 'above', 'more than', 'between', 'lakh', 'crore'])
    
#     if has_card_phrase or has_category_and_price:
#         n_cards = 5
#         df_filtered = df_main.copy()
        
#         # Special handling for "variants" queries using regex
#         variants_pattern = r'\b(variants?|models?)\b'
#         variants_detected = bool(re.search(variants_pattern, prompt_lower))
#         if variants_detected:
#             # For variants queries, use a much higher limit to show all variants
#             n_cards = 50  # Increased from 5 to 50 for variants
            
#             # Extract vehicle name more intelligently
#             # Remove common words and extract the vehicle name
#             prompt_words = prompt_lower.split()
#             vehicle_keywords = ['variants', 'variant', 'models', 'model', 'of', 'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'with', 'by', 'show', 'me', 'some', 'all', 'list', 'give', 'how', 'many']
            
#             # Filter out common words and keep potential vehicle names
#             vehicle_name_parts = [word for word in prompt_words if word not in vehicle_keywords]
            
#             # Try different combinations to find the vehicle name
#             vehicle_name = None
            
#             # First try: all remaining words as vehicle name
#             if vehicle_name_parts:
#                 vehicle_name = ' '.join(vehicle_name_parts)
                
#                 # Filter vehicles that contain the vehicle name
#                 if 'Vehicle Name' in df_filtered.columns:
#                     # Try exact match first
#                     exact_match = df_filtered[df_filtered['Vehicle Name'].str.lower() == vehicle_name]
#                     if not exact_match.empty:
#                         df_filtered = exact_match
#                     else:
#                         # Try partial match
#                         df_filtered = df_filtered[df_filtered['Vehicle Name'].str.lower().str.contains(vehicle_name, na=False)]
            
#             # If no vehicles found, try with brand + vehicle name
#             if len(df_filtered) == 0 and prompt_brand_match and vehicle_name:
#                 brand_vehicle = f"{prompt_brand_match} {vehicle_name}"
#                 df_filtered = df_main[df_main['Vehicle Name'].str.lower().str.contains(brand_vehicle, na=False)]
                
#                 # Special case for "ace" - try to find vehicles with "ace" in the name
#                 if len(df_filtered) == 0 and 'ace' in vehicle_name.lower():
#                     ace_vehicles = df_main[df_main['Vehicle Name'].str.lower().str.contains('ace', na=False)]
#                     if not ace_vehicles.empty:
#                         df_filtered = ace_vehicles
            
#             # If still no vehicles found, try just the brand
#             if len(df_filtered) == 0 and prompt_brand_match:
#                 df_filtered = df_main[df_main['Brand Name'].str.lower().str.contains(prompt_brand_match, na=False)]
            
#             # For variants queries, if we found specific vehicles, don't fall back to brand-only
#             # This ensures we only show the specific vehicle variants, not all brand vehicles
#             if variants_detected and len(df_filtered) > 0:
#                 pass
#         else:
#             # Normal brand filtering
#             if prompt_brand_match:
#                 df_filtered = df_filtered[df_filtered['Brand Name'].str.lower().str.contains(prompt_brand_match)]
        
#         # Remove "Coming Soon" vehicles from ALL queries - they should never be displayed
#         if 'Vehicle Price' in df_filtered.columns:
#             # More robust filtering for "Coming Soon" vehicles
#             coming_soon_mask = df_filtered['Vehicle Price'].str.lower().str.contains('coming soon', na=False)
#             df_filtered = df_filtered[~coming_soon_mask]
        
#         # Apply fuel filtering for ALL queries (not just variants)
#         # --- Electric filter logic ---
#         if 'electric' in prompt_lower:
                
#             # Create a mask for electric vehicles
#             electric_mask = pd.Series([False] * len(df_filtered), index=df_filtered.index)
            
#             # PRIORITY 1: Check Vehicle Name for electric keywords - if name contains "electric", it's electric regardless of Electric column
#             if 'Vehicle Name' in df_filtered.columns:
#                 exact_electric_mask = df_filtered['Vehicle Name'].str.lower().str.contains(r'electric|e-|ev|e\s|e$', na=False)
#                 electric_mask |= exact_electric_mask
            
#             # PRIORITY 2: Check Electric column (only if vehicle name doesn't already indicate electric)
#             if 'Electric' in df_filtered.columns:
#                 # Only use Electric column for vehicles that don't have electric in the name
#                 non_electric_name_mask = ~exact_electric_mask if 'exact_electric_mask' in locals() else pd.Series([True] * len(df_filtered), index=df_filtered.index)
#                 electric_column_mask = (df_filtered['Electric'].str.lower().str.contains('yes|true|1|y', na=False)) & non_electric_name_mask
#                 electric_mask |= electric_column_mask
            
#             # PRIORITY 3: Check Fuel Type column
#             if 'Fuel Type' in df_filtered.columns:
#                 fuel_type_mask = df_filtered['Fuel Type'].str.lower().str.contains('electric|ev', na=False)
#                 electric_mask |= fuel_type_mask
            
#             # Apply the electric filter
#             df_filtered = df_filtered[electric_mask]
            
#         # --- CNG filter logic ---
#         if 'cng' in prompt_lower:
            
#             # Create a mask for CNG vehicles
#             cng_mask = pd.Series([False] * len(df_filtered), index=df_filtered.index)
            
#             # Check Fuel Type column for CNG
#             if 'Fuel Type' in df_filtered.columns:
#                 cng_mask |= df_filtered['Fuel Type'].str.lower().str.contains('cng', na=False)

#             # Check Vehicle Name for CNG keywords
#             if 'Vehicle Name' in df_filtered.columns:
#                 cng_mask |= df_filtered['Vehicle Name'].str.lower().str.contains('cng', na=False)
            
#             # Apply the CNG filter
#             df_filtered = df_filtered[cng_mask]
            
#         # --- Petrol filter logic ---
#         if 'petrol' in prompt_lower:
            
#             # Create a mask for Petrol vehicles
#             petrol_mask = pd.Series([False] * len(df_filtered), index=df_filtered.index)
            
#             # Check Fuel Type column for Petrol
#             if 'Fuel Type' in df_filtered.columns:
#                 petrol_mask |= df_filtered['Fuel Type'].str.lower().str.contains('petrol', na=False)

#             # Check Vehicle Name for Petrol keywords
#             if 'Vehicle Name' in df_filtered.columns:
#                 petrol_mask |= df_filtered['Vehicle Name'].str.lower().str.contains('petrol', na=False)
            
#             # Apply the Petrol filter
#             df_filtered = df_filtered[petrol_mask]
            
#         # --- Diesel filter logic ---
#         if 'diesel' in prompt_lower:
            
#             # Create a mask for Diesel vehicles
#             diesel_mask = pd.Series([False] * len(df_filtered), index=df_filtered.index)
            
#             # Check Fuel Type column for Diesel
#             if 'Fuel Type' in df_filtered.columns:
#                 diesel_mask |= df_filtered['Fuel Type'].str.lower().str.contains('diesel', na=False)

#             # Check Vehicle Name for Diesel keywords
#             if 'Vehicle Name' in df_filtered.columns:
#                 diesel_mask |= df_filtered['Vehicle Name'].str.lower().str.contains('diesel', na=False)
            
#             # Apply the Diesel filter
#             df_filtered = df_filtered[diesel_mask]
        
#         # Apply category filtering for variants queries when category is specified
#         if prompt_category_match:
#             if 'Category Name' in df_filtered.columns:
#                 # Exact category matching: if user says "trucks", only show vehicles from "Truck" category
#                 # Map user input to exact category names
#                             category_mapping = {
#                 'truck': 'Truck',
#                 'trucks': 'Truck',
#                 'bus': 'Bus', 
#                 'buses': 'Bus',
#                 'auto': 'Auto Rickshaws',
#                 'auto rickshaw': 'Auto Rickshaws',
#                 'auto rickshaws': 'Auto Rickshaws',
#                 'auto rickshaw 3 wheelers': 'Auto Rickshaws',
#                 'auto rickshaw 3 wheeler': 'Auto Rickshaws',
#                 '3 wheelers': 'Auto Rickshaws',
#                 '3 wheeler': 'Auto Rickshaws',
#                 'rickshaw': 'Auto Rickshaws',
#                 'rickshaws': 'Auto Rickshaws',
#                 'tractor': 'Tractor',
#                 'tractors': 'Tractor',
#                 'trailer': 'Trailer',
#                 'trailers': 'Trailer',
#                 'cargo': 'Cargo',
#                 'cargo van': 'Cargo Van',
#                 'cargo vans': 'Cargo Van',
#                 'pickup': 'Pickup',
#                 'pickups': 'Pickup',
#                 'mini truck': 'Mini Truck',
#                 'mini trucks': 'Mini Truck',
#                 'minitruck': 'Mini Truck',
#                 'minitrucks': 'Mini Truck'
#             }
            
#             # Get the exact category name to match
#             target_category = category_mapping.get(prompt_category_match.lower(), prompt_category_match)
            
#             # Try case-insensitive exact category match first
#             df_exact = df_filtered[df_filtered['Category Name'].str.lower() == target_category.lower()]
            
#             # Only use exact category matching - never fall back to partial matching
#             # This ensures category-specific queries only show vehicles from that exact category
#             df_filtered = df_exact
            
#             # If no exact matches found, return empty result
#             if len(df_filtered) == 0:
#                 return {"status": "success", "response": f"No {prompt_category_match} found in the Knowledgebase."}
            
#         if variants_detected:
#             matches = []
#             used_models = set()
#             for _, row in df_filtered.iterrows():
#                 vehicle_data = get_vehicle_data_with_id_by_index(row)
#                 if (vehicle_data and 
#                     vehicle_data.get('vehicle_price', '').strip().lower() != 'coming soon' and
#                     vehicle_data.get('vehicle_name', '').strip() not in used_models):
                    
#                     matches.append(vehicle_data)
#                     used_models.add(vehicle_data.get('vehicle_name', '').strip())
            
#         # --- Price filter logic using improved function ---
#         price_filter = extract_price_filter_improved(prompt_lower)
#         if price_filter:
#             df_filtered = apply_price_filter_improved(df_filtered, price_filter)
        
#         # --- High payload and mileage filters ---
            
#         if 'high payload' in prompt_lower or 'maximum payload' in prompt_lower or 'max payload' in prompt_lower:
#             if 'Payload' in df_filtered.columns:
#                 df_filtered['Payload'] = pd.to_numeric(df_filtered['Payload'], errors='coerce')
#                 df_filtered = df_filtered[df_filtered['Payload'].notna()]
#                 df_filtered = df_filtered.sort_values(by='Payload', ascending=False)
#         if 'high mileage' in prompt_lower or 'maximum mileage' in prompt_lower or 'max mileage' in prompt_lower or 'best mileage' in prompt_lower:
#             if 'Mileage' in df_filtered.columns:
#                 df_filtered['Mileage'] = pd.to_numeric(df_filtered['Mileage'], errors='coerce')
#                 df_filtered = df_filtered[df_filtered['Mileage'].notna()]
#                 df_filtered = df_filtered.sort_values(by='Mileage', ascending=False)
        
#         # Always apply price filter before sorting and returning matches
#         if 'Rating' in df_filtered.columns:
#             df_filtered = df_filtered.sort_values(by='Rating', ascending=False)
        
#         # For variants queries, get ALL variants without diversity filtering
#         if variants_detected:
#             # Remove "Coming Soon" vehicles from variants queries as well
#             if 'Vehicle Price' in df_filtered.columns:
#                 # More robust filtering for "Coming Soon" vehicles
#                 coming_soon_mask = df_filtered['Vehicle Price'].str.lower().str.contains('coming soon', na=False)
#                 df_filtered = df_filtered[~coming_soon_mask]
#             matches = []
#             used_models = set()
            
#             # Get all variants without diversity restrictions
#             for _, row in df_filtered.iterrows():
#                 if len(matches) >= n_cards:  # Still respect the n_cards limit
#                     break
#                 vehicle_data = get_vehicle_data_with_id_by_index(row)
#                 if (vehicle_data and 
#                     vehicle_data.get('vehicle_price', '').strip().lower() != 'coming soon' and
#                     vehicle_data.get('vehicle_name', '').strip() not in used_models):
                    
#                     matches.append(vehicle_data)
#                     used_models.add(vehicle_data.get('vehicle_name', '').strip())
            
#             matches = [v for v in matches if v]
#             if matches:
#                 return {"status": "success", "response": {"possible_matches": matches}}
#             return {"status": "success", "response": "There are no vehicles in the Knowledgebase matching your criteria."}
#         else:
#             # Remove "Coming Soon" vehicles from non-variants queries as well
#             if 'Vehicle Price' in df_filtered.columns:
#                 # More robust filtering for "Coming Soon" vehicles
#                 coming_soon_mask = df_filtered['Vehicle Price'].str.lower().str.contains('coming soon', na=False)
#                 df_filtered = df_filtered[~coming_soon_mask]
            
#             # Get diverse vehicles across brands (for non-variants queries)
#             def get_diverse_vehicles(df, max_vehicles=5):
#                 """Get diverse vehicles across different brands"""
#                 matches = []
#                 used_models = set()
#                 used_brands = set()
                
#                 # First, try to get one vehicle from each brand
#                 brand_groups = df.groupby('Brand Name')
#                 for brand_name, brand_df in brand_groups:
#                     if len(matches) >= max_vehicles:
#                         break
#                     for _, row in brand_df.iterrows():
#                         vehicle_data = get_vehicle_data_with_id_by_index(row)
#                         if (vehicle_data and 
#                             vehicle_data.get('vehicle_price', '').strip().lower() != 'coming soon' and
#                             vehicle_data.get('vehicle_name', '').strip() not in used_models):
                            
#                             matches.append(vehicle_data)
#                             used_models.add(vehicle_data.get('vehicle_name', '').strip())
#                             used_brands.add(brand_name)
#                             break  # Only take one from each brand initially
                
#                 # If we still have space, fill with remaining vehicles
#                 if len(matches) < max_vehicles:
#                     for _, row in df.iterrows():
#                         if len(matches) >= max_vehicles:
#                             break
#                         vehicle_data = get_vehicle_data_with_id_by_index(row)
#                         if (vehicle_data and 
#                             vehicle_data.get('vehicle_price', '').strip().lower() != 'coming soon' and
#                             vehicle_data.get('vehicle_name', '').strip() not in used_models):
                            
#                             matches.append(vehicle_data)
#                             used_models.add(vehicle_data.get('vehicle_name', '').strip())
#                             used_brands.add(brand_name)
#                             break  # Only take one from each brand initially
                
#                 return matches
            
#             matches = get_diverse_vehicles(df_filtered, n_cards)
#             matches = [v for v in matches if v]
#             if matches:
#                 return {"status": "success", "response": {"possible_matches": matches}}
#             return {"status": "success", "response": "There are no vehicles in the Knowledgebase matching your criteria."}
#     # 5. Exact vehicle name match (should come before substring matching)
#     # Check if the prompt exactly matches any vehicle name
#     exact_match_found = False
#     for vehicle_name in display_names:
#         if prompt_lower.strip() == vehicle_name.lower().strip():
#             exact_match_found = True
#             data = get_vehicle_data(vehicle_name, df_main)
#             if data:
#                 recommendations = []
#                 if data.get('vehicle_price') and str(data['vehicle_price']).strip().lower() != 'coming soon':
#                     recs = get_recommendations(data, df_main)
#                     recommendations = [get_vehicle_data(rec_row['Vehicle Name'], df_main) for _, rec_row in recs.iterrows()] if hasattr(recs, 'iterrows') else []
#                 response_obj = {"vehicle": data}
#                 if recommendations:
#                     response_obj["recommendations"] = recommendations
#                 return {"status": "success", "response": response_obj}
#             else:
#                 return {"status": "success", "response": "I apologize, but I couldn't find that specific vehicle in our database. Please check the vehicles listed on 91Trucks for accurate information about available commercial vehicles."}
    
#     # 6. Substring vehicle/model name match: show all vehicles containing the substring (only if no exact match found)
#     prompt_lower_clean = prompt_lower.strip()
#     if prompt_lower_clean:
#         brand_in_prompt = next((b for b in brands if b in prompt_lower), None)
        
#         # Check for fuel type filtering
#         fuel_filter = None
#         if 'electric' in prompt_lower or 'ev' in prompt_lower:
#             fuel_filter = 'electric'
#         elif 'diesel' in prompt_lower:
#             fuel_filter = 'diesel'
#         elif 'cng' in prompt_lower:
#             fuel_filter = 'cng'
#         elif 'petrol' in prompt_lower:
#             fuel_filter = 'petrol'
        
#         # Check if any vehicle name contains the prompt as a substring
#         matching_vehicles = []
#         for vehicle_name in display_names:
#             vehicle_lower = vehicle_name.lower()
#             # Check if the prompt is a substring of the vehicle name
#             if prompt_lower_clean in vehicle_lower:
#                 matching_vehicles.append(vehicle_name)
        
#         if matching_vehicles:
#             # Filter the dataframe to only include vehicles that match the substring
#             if brand_in_prompt:
#                 df_filtered = df_main[
#                     (df_main['Brand Name'].str.lower().str.contains(brand_in_prompt)) &
#                     (df_main['Vehicle Name'].str.lower().str.contains(prompt_lower_clean, case=False, regex=False))
#                 ]
#             else:
#                 df_filtered = df_main[df_main['Vehicle Name'].str.lower().str.contains(prompt_lower_clean, case=False, regex=False)]
            
#             # Apply fuel type filtering if specified
#             if fuel_filter:
#                 if fuel_filter == 'electric':
#                     if 'Electric' in df_filtered.columns:
#                         df_filtered = df_filtered[df_filtered['Electric'].str.lower() == 'yes']
#                     if 'Fuel Type' in df_filtered.columns:
#                         df_filtered = df_filtered[df_filtered['Fuel Type'].str.lower().str.contains('electric', na=False)]
#                 elif fuel_filter == 'diesel':
#                     if 'Fuel Type' in df_filtered.columns:
#                         df_filtered = df_filtered[df_filtered['Fuel Type'].str.lower().str.contains('diesel', na=False)]
#                 elif fuel_filter == 'cng':
#                     if 'Fuel Type' in df_filtered.columns:
#                         df_filtered = df_filtered[df_filtered['Fuel Type'].str.lower().str.contains('cng', na=False)]
#                 elif fuel_filter == 'petrol':
#                     if 'Fuel Type' in df_filtered.columns:
#                         df_filtered = df_filtered[df_filtered['Fuel Type'].str.lower().str.contains('petrol', na=False)]
            
#             # For substring matches, show ALL variants (no limit)
#             # Ensure we don't include vehicles with 'Coming Soon' prices and prevent duplicate models
#             matches = []
#             used_models = set()
#             for _, row in df_filtered.iterrows():
#                 vehicle_data = get_vehicle_data_with_id_by_index(row)
#                 if vehicle_data and vehicle_data.get('vehicle_price', '').strip().lower() != 'coming soon':
#                     # Get the model name to check for duplicates
#                     model_name = vehicle_data.get('vehicle_name', '').strip()
#                     if model_name and model_name not in used_models:
#                         matches.append(vehicle_data)
#                         used_models.add(model_name)
#             matches = [v for v in matches if v]
#             if matches:
#                 return {"status": "success", "response": {"possible_matches": matches}}
    
#     # 6. Vehicle/model name (fuzzy match) - only if no exact or substring matches found
#     norm_prompt = normalize_vehicle_name_unique(prompt)
#     close_vehicle = difflib.get_close_matches(norm_prompt, vehicle_names, n=1, cutoff=0.85)
#     if close_vehicle:
#         vehicle_name = display_names[vehicle_names.index(close_vehicle[0])]
#         data = get_vehicle_data(vehicle_name, df_main)
#         if data:
#             recommendations = []
#             if data.get('vehicle_price') and str(data['vehicle_price']).strip().lower() != 'coming soon':
#                 recs = get_recommendations(data, df_main)
#                 recommendations = [get_vehicle_data(rec_row['Vehicle Name'], df_main) for _, rec_row in recs.iterrows()] if hasattr(recs, 'iterrows') else []
#             response_obj = {"vehicle": data}
#             if recommendations:
#                 response_obj["recommendations"] = recommendations
#             return {"status": "success", "response": response_obj}
#         else:
#             return {"status": "success", "response": "I apologize, but I couldn't find that specific vehicle in our database. Please check the vehicles listed on 91Trucks for accurate information about available commercial vehicles."}
#     # --- Fuel type filtering for "list all [fuel] vehicles" queries ---
#     fuel_list_patterns = [
#         r'list all (\w+) vehicles?',
#         r'show (\w+) vehicles?',
#         r'(\w+) vehicles?',
#         r'(\w+) trucks?',
#         r'(\w+) buses?'
#     ]
    
#     fuel_filter = None
#     for pattern in fuel_list_patterns:
#         match = re.search(pattern, prompt_lower)
#         if match:
#             fuel_type = match.group(1).lower()
#             if fuel_type in ['electric', 'diesel', 'cng', 'petrol']:
#                 fuel_filter = fuel_type
#                 break
    
#     if fuel_filter:
#         df_filtered = df_main.copy()
        
#         # Apply fuel type filtering
#         if fuel_filter == 'electric':
#             if 'Electric' in df_filtered.columns:
#                 df_filtered = df_filtered[df_filtered['Electric'].str.lower() == 'yes']
#             if 'Fuel Type' in df_filtered.columns:
#                 df_filtered = df_filtered[df_filtered['Fuel Type'].str.lower().str.contains('electric', na=False)]
#         elif fuel_filter == 'diesel':
#             if 'Fuel Type' in df_filtered.columns:
#                 df_filtered = df_filtered[df_filtered['Fuel Type'].str.lower().str.contains('diesel', na=False)]
#         elif fuel_filter == 'cng':
#             if 'Fuel Type' in df_filtered.columns:
#                 df_filtered = df_filtered[df_filtered['Fuel Type'].str.lower().str.contains('cng', na=False)]
#         elif fuel_filter == 'petrol':
#             if 'Fuel Type' in df_filtered.columns:
#                 df_filtered = df_filtered[df_filtered['Fuel Type'].str.lower().str.contains('petrol', na=False)]
        
#         # Get diverse selection of vehicles
#         selected_vehicles = []
#         used_models = set()
        
#         for _, row in df_filtered.iterrows():
#             if len(selected_vehicles) >= 10:  # Limit to 10 vehicles
#                 break
#             vehicle_data = get_vehicle_data_with_id_by_index(row)
#             if vehicle_data and vehicle_data.get('vehicle_price', '').strip().lower() != 'coming soon':
#                 model_name = vehicle_data.get('vehicle_name', '').strip()
#                 if model_name and model_name not in used_models:
#                     selected_vehicles.append(vehicle_data)
#                     used_models.add(model_name)
        
#         if selected_vehicles:
#             return {"status": "success", "response": {"possible_matches": selected_vehicles}}
    

#     # --- LLM fallback for all other queries ---
#     # Check if the query contains vehicle names that don't exist in our dataset
#     # Only apply vehicle name validation if the query looks like it's searching for a specific vehicle
#     vehicle_keywords = ['truck', 'bus', 'auto', 'rickshaw', 'vehicle', 'car', 'suv', 'pickup', 'cargo', 'trailer', 'tractor']
#     query_contains_vehicle_keywords = any(keyword in prompt_lower for keyword in vehicle_keywords)
    
#     # Only do vehicle name validation if the query contains vehicle-related keywords
#     if query_contains_vehicle_keywords:
#         query_parts = [part.strip() for part in prompt_lower.split() if len(part.strip()) >= 3]
        
#         # Check if any significant part of the query matches a vehicle name exactly
#         vehicle_found_in_dataset = False
#         for vehicle_name in display_names:
#             vehicle_lower = vehicle_name.lower()
#             # Check if the entire query matches the vehicle name
#             if prompt_lower == vehicle_lower:
#                 vehicle_found_in_dataset = True
#                 break
#             # Check if any significant part (3+ chars) of the query is in the vehicle name
#             for part in query_parts:
#                 if part in vehicle_lower and len(part) >= 4:  # More strict matching
#                     vehicle_found_in_dataset = True
#                     break
#             if vehicle_found_in_dataset:
#                 break
        
#         # If no vehicle found in dataset and query contains vehicle keywords, let LLM handle it
#         if not vehicle_found_in_dataset and len(prompt_lower.strip()) >= 3:
#             pass  # Continue to LLM logic instead of returning hardcoded message
    
#     if qa_chain:
#         retriever = vector_store.as_retriever()
#         docs = retriever.get_relevant_documents(prompt)
#         context = "\n".join([doc.page_content for doc in docs]) if docs else ""
#         result = qa_chain.invoke({"question": prompt, "context": context})
#         if isinstance(result, dict):
#             answer = result.get("result") or "Sorry, I couldn't find an answer to that."
#         else:
#             answer = result or "Sorry, I couldn't find an answer to that."
#         answer = clean_llm_output(answer)
#         answer = remove_duplicate_website_links(answer)
#         answer = strip_markdown(answer)
#         # Enhance the response with vehicle details instead of links
#         answer = enhance_llm_response_with_vehicle_details(answer, df_main, display_names)
#         vehicle_card = find_vehicle_from_text(f"{prompt} \n {answer}", display_names, df_main)
#         # if vehicle_card:
#             # return {"status": "success", "response": answer, "vehicle": vehicle_card}
#         if vehicle_card:
#             return {
#         "status": "success",
#         "response": {
#             "vehicle": vehicle_card,  # object, not list
#             "summary": answer
#         }
#         }
#         return {"status": "success", "response": answer}
#     else:
#         return {"status": "error", "response": "I'm your commercial vehicle assistant for 91Trucks. I can help you with trucks, buses, autos, and related queries. Please ask about vehicles that are available in our dataset or listed on 91Trucks."}

    

# def remove_duplicate_website_links(text):
#     """ Keeps only the first occurrence of a 91trucks.com link in the text and removes duplicates """
#     # Remove duplicate 91trucks.com links (keep only the first occurrence)
#     pattern = r'(https?://www\.91trucks\.com)'
#     matches = list(re.finditer(pattern, text))
#     if len(matches) > 1:
#         # Replace all but the first occurrence
#         first = matches[0].end()
#         text = text[:first] + re.sub(pattern, '', text[first:], flags=re.IGNORECASE)
#     return text

# def strip_markdown(text):
#     """Strips markdown (bold, italics, headings, lists), special symbols, and newlines.
#     Example: "**Hello**\n*world* ➡️" → "Hello world" """

#     text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # bold
#     text = re.sub(r'\*([^*]+)\*', r'\1', text)      # italics
#     text = re.sub(r'#+ ', '', text)                   # headings
#     text = re.sub(r'^[\-*]\s+', '', text, flags=re.MULTILINE)  # lists
#     text = re.sub(r'`([^`]+)`', r'\1', text)         # inline code
#     text = re.sub(r'[•→●◆★✓✔️➡️❯❯▶️►]', '', text)  # common bullet/special symbols
#     # Remove any remaining newlines or carriage returns
#     text = text.replace('\n', ' ').replace('\r', ' ')
#     return text.strip()

# def normalize_brand_name(name):
#     """ Normalizes brand name by converting to lowercase, removing spaces & non-alphanumerics.
#       Example: "  Ashok-Leyland  " → "ashokleyland" """

#     if not isinstance(name, str):
#         return ""
#     return re.sub(r'[^a-z0-9]', '', name.lower().strip())

# def normalize_category_name(name):
#     """Normalizes category name by converting to lowercase and removing non-alphanumeric characters.
#        Example: " Pickup Trucks " → "pickuptrucks" """

#     if not isinstance(name, str):
#         return ""
#     return re.sub(r'[^a-z0-9]', '', name.lower().strip())

# def normalize_vehicle_name_unique(name):
#     """Normalizes vehicle name by lowercasing, removing special characters, and handling accented text. 
#        Example: "Tata Intra V30®" → "tataintrav30" """

#     if not isinstance(name, str):
#         return ""
#     name = unicodedata.normalize('NFKD', name)
#     name = name.lower()
#     name = re.sub(r'[^a-z0-9]', '', name)
#     return name

# def is_off_topic_query(prompt):
#     """Returns True if the query is completely unrelated to commercial vehicles, 91Trucks, or vehicle industry"""
#     prompt_lower = prompt.lower()
    
#     # Keywords that indicate the query is related to our domain
# import re

# relevant_keywords = [
#     # Vehicle-related
#     'truck', 'bus', 'auto', 'rickshaw', 'vehicle', 'car', 'suv', 'pickup', 'cargo', 'trailer', 'tractor',
#     'commercial', 'transport', 'logistics', 'delivery', 'freight', 'shipping','trucks','buses','autos'
#     # 91Trucks related
#     '91trucks', '91 trucks', 'raftaar', 'founder', 'founders', 'company', 'business', 'platform', "the 91trucks", "the 91 trucks",
#     # Vehicle brands
#     'tata', 'mahindra', 'ashok', 'leyland', 'eicher', 'force', 'bharatbenz', 'swaraj', 'mazda',
#     'montra', 'omega', 'seiki', 'mobility', 'sml', 'isuzu', 'euler', 'motors', 'piaggio', 'bajaj',
#     'tvs', 'atul', 'kinetic', 'lohia', 'hero', 'toyota', 'hyundai', 'scania', 'volvo', 'tesla',
#     # Vehicle features
#     'electric', 'diesel', 'petrol', 'cng', 'fuel', 'engine', 'power', 'torque', 'mileage', 'payload',
#     'gvw', 'weight', 'capacity', 'price', 'cost', 'budget', 'finance', 'insurance',
#     # General vehicle queries
#     'show', 'display', 'list', 'find', 'search', 'compare', 'vs', 'versus', 'recommend', 'suggest',
#     'help', 'assist', 'guide', 'advice', 'information', 'details', 'specs', 'specifications', 'list all', 'give me', 'show me'
# ]

# def normalize_keyword(word):
#     """Lowercase and remove all non-alphanumeric characters (including spaces)."""
#     return re.sub(r'[^a-z0-9]', '', word.lower())

# # Build a set of normalized keywords, including plural forms
# normalized_keywords = set()
# for kw in relevant_keywords:
#     norm = normalize_keyword(kw)
#     normalized_keywords.add(norm)
#     if not norm.endswith('s'):
#         normalized_keywords.add(norm + 's')  # Add plural

# def contains_relevant_keyword(user_input):
#     """Returns True if any relevant keyword (case/space/plural-insensitive) is found in user_input."""
#     user_norm = normalize_keyword(user_input)
#     for kw in normalized_keywords:
#         if kw in user_norm:
#             return True
#     return False

# # --- Load Data and Models (on startup) ---
# df_main = pd.read_csv('data/new_data.csv')
# df_qna = pd.read_csv('data/91Trucks_QnAs.csv')
# df_main["Vehicle Image"] = df_main["Vehicle Image"].fillna("")
# df_main["Price"] = df_main["Vehicle Price"].apply(clean_price)

# # Build vector store
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# docs = []

# # Add vehicle data
# for _, row in df_main.iterrows():
#     price_str = f"{row['Price']} Lakh" if pd.notnull(row['Price']) else "N/A"
#     text = (f"Brand: {row['Brand Name']}, Model: {row['Model Name']}, Vehicle Name: {row['Vehicle Name']}, Average Rating: {row['Average Rating']}"
#             f"Electric: {row['Electric']}, Price: {price_str}, Fuel Type: {row['Fuel Type']}, "
#             f"Variant: {row['Variant Name']}, Power: {row['Power']}, Torque: {row['Torque']}, Fuel Tank Capacity: {row['Fuel Tank Capacity']}, Gross Vehicle Weight: {row['Gross Vehicle Weight']}, No Of Seats: {row['No Of Seats']},  Image: {row['Vehicle Image']},"
#             f"End Point: {row.get('End Point', '')}")
#     docs.append(text)

# # Add FAQ data
# faq_count = 0
# for _, row in df_qna.iterrows():
#     docs.append(f"Question: {row['question']} Answer: {row['answer']}")
#     faq_count += 1

# # Add PDF content
# try:
#     import PyPDF2
#     pdf_path = '91trucks_smart_vehicle_assistant_api.pdf'
#     pdf_pages_added = 0
#     if os.path.exists(pdf_path):
#         with open(pdf_path, 'rb') as file:
#             pdf_reader = PyPDF2.PdfReader(file)
#             total_pages = len(pdf_reader.pages)
            
#             for page_num in range(total_pages):
#                 page = pdf_reader.pages[page_num]
#                 text = page.extract_text()
#                 if text.strip():  # Only add non-empty pages
#                     # Clean and format the text
#                     cleaned_text = text.strip()
#                     # Add page number for reference
#                     docs.append(f"PDF Content (Page {page_num + 1}): {cleaned_text}")
#                     pdf_pages_added += 1
#     else:
#         pass
# except ImportError:
#     pass
# except Exception as e:
#     pass

# documents = text_splitter.create_documents(docs)
# # Use OpenAI embeddings since we already have OpenAI API key
# try:
#     embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
# except Exception as e:
#     try:
#         model = SentenceTransformer('all-MiniLM-L6-v2')
#         embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
#     except Exception as e2:
#         # Final fallback - use a simple embedding
        
#         embeddings = FakeEmbeddings(size=1536)  # OpenAI ada-002 has 1536 dimensions
# vector_store = FAISS.from_documents(documents, embeddings)

# prompt_template = """You are Raftaar, an intelligent commercial vehicle assistant for 91Trucks. You have access to comprehensive data about trucks, buses, and auto-rickshaws, including specifications, pricing, and industry insights.

# **CRITICAL: Keep ALL answers extremely concise (30-40 words maximum)**

# **Your Capabilities:**
# - Answer questions about any commercial vehicle in the database
# - Provide detailed specifications, pricing, and comparisons
# - Give recommendations based on use cases and requirements
# - Explain technical features and benefits
# - Share industry insights and trends
# - Help with vehicle selection and purchasing decisions
# - 🔒🚫 ABSOLUTE RULE — DO NOT VIOLATE:
#     ❗❗ YOU MUST NOT ANSWER questions about weather, geography, politics, general knowledge, science, sports, education, health, history, entertainment, travel, religion, programming, mobile apps, lifestyle, or locations (state, district, village, capital, country) — or ANY non-commercial vehicle topic.


# **If an exact or close match (partial/fuzzy) is found → give complete information directly, without mentioning "not listed on 91Trucks."**

# 2. **If Not Found:**  
#    - Only if the vehicle is not present in the database at all → respond with:  
#      " but according to our market research..."  
#      and then provide relevant insights.

# 3. **Answer Style:**  
#    - Keep answers concise, factual, and focused on commercial vehicles.  
#    - Prefer bullet points or short paragraphs.  
#    - Do not invent specifications — only use verified database values or general market insights.  

# 4. **Other Queries:**  
#    - If the user asks about something unrelated to vehicles, respond politely that you can only assist with 91Trucks vehicles and the commercial vehicle industry.
# ."** 
# - For general knowledge questions (like people, places, sports, etc.) or questions about 91Trucks company/business, answer directly without any vehicle-related disclaimers.
# - Use your intelligence to determine if the query is about a commercial vehicle or something else entirely.

# **Available Data Sources:**
# 1. **Complete Vehicle Database**: Full specifications for all commercial vehicles
# 2. **91Trucks QnAs**: 650+ Q&A pairs with industry knowledge
# 3. **Technical Documentation**: Platform and vehicle information
# 4. **Your Intelligence**: Business concepts, industry knowledge, and reasoning

# **Response Guidelines:**
# - Keep answers extremely concise (30-40 words maximum)
# - Be direct and to the point
# - Focus on the most essential information only
# - **ALWAYS include recommendations when relevant**
# - Avoid lengthy explanations or multiple sentences
# - Use bullet points or short phrases when possible
# - Prioritize key facts over detailed descriptions
# - DO NOT guess or provide unrelated answers under any condition.

# **For vehicle-specific queries:**
# - Only essential specifications, key features
# - Brief comparison if relevant
# - **ALWAYS include one-line recommendation**
# - Example: "Great for urban delivery, consider Tata Ace for better fuel efficiency"
# - **If vehicle not in database, clearly mention: "Since this vehicle is not listed on 91Trucks, but according to our market research."** For general company questions, answer directly without this disclaimer.

# **For brand or category queries:**
# - Brief overview of key vehicles
# - Highlight main differences only
# - **ALWAYS include recommendation for best choice**
# - Example: "Tata offers reliable trucks, Mahindra for better fuel efficiency"
# - **Mention 'external sources' if brand or product is not in database**

# **For comparison queries:**
# - Keep answers concise but detailed (50 words maximum)
# - Focus on 3-4 key differences
# - **ALWAYS include a recommendation**
# - Provide brief reasoning
# - **Clearly state if comparison includes vehicle(s) from external sources**

# **For technical questions (Only related to the commercial vehicle Category):**
# - Provide only essential technical details
# - Keep explanations brief and focused

# **Important Notes:**
# - Always mention specific vehicle names when discussing them
# - Only show features that have actual values (skip "not available" fields)
# - Be conversational and helpful, not robotic
# - Use your intelligence to provide insights beyond just listing data
# - Combine multiple data sources for the most complete answers
# - **If data is not from internal sources, explicitly note: "Since this vehicle is not listed on 91Trucks, but according to our market research."** For general company questions, answer directly without this disclaimer.
# - **CRITICAL: Never exceed 40 words for any response**

# **Do not display or mention any vehicle whose price is listed as Coming Soon in the dataset. Exclude them from both card results and textual/theoretical responses.**

# **Context:**
# {context}

# **Question:**
# {question}

# **Answer:** (Provide a concise response in 30-40 words maximum)
# """

# prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
# # llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="llama3-70b-8192", temperature=0.15, max_tokens=2048)
# llm = ChatOpenAI(
#     model_name="gpt-4o-mini",
#     # model_name="gpt-5-nano",
#     temperature=0.15,
#     max_tokens=2048,
#     openai_api_key=os.getenv("OPENAI_API_KEY")
# )
# output_parser = StrOutputParser()
# qa_chain = prompt | llm | output_parser

# display_names = set(df_main['Vehicle Name'].dropna().unique())
# brand_names = set(df_main['Brand Name'].dropna().str.lower().unique())

# @app.route('/query', methods=['POST'])
# def query():
#     data = request.get_json()
#     prompt = data.get('prompt', '')
#     print(prompt)
#     result = process_query(prompt, df_main, brand_names, display_names, qa_chain=qa_chain)
#     return jsonify(result)

# def enhance_llm_response_with_vehicle_details(text, df_main, display_names):
#     """
#     Enhances LLM responses by replacing 91trucks.com links with actual vehicle details.
#     This function detects when a response contains a link to a vehicle page and replaces it
#     with comprehensive vehicle information from the dataset.
#     """
#     if not text or not isinstance(text, str):
#         return text
    
#     # Pattern to match 91trucks.com vehicle URLs
#     # Examples: https://www.91trucks.com/trucks/mahindra/zeo
#     vehicle_url_pattern = r'https?://www\.91trucks\.com/(?:trucks|buses|auto-rickshaws|tractors|trailers)/([^/\s]+)/([^/\s]+)'
    
#     def replace_url_with_vehicle_details(match):
#         category = match.group(1)  # trucks, buses, auto-rickshaws, etc.
#         model_slug = match.group(2)  # zeo, ace, etc.
        
#         # Try to find the vehicle in our dataset
#         vehicle_found = None
        
#         # First, try to find by model slug in vehicle names
#         for vehicle_name in display_names:
#             if model_slug.lower() in vehicle_name.lower():
#                 vehicle_data = get_vehicle_data(vehicle_name, df_main)
#                 if vehicle_data:
#                     vehicle_found = vehicle_data
#                     break
        
#         # If not found by name, try to find by other identifiers
#         if not vehicle_found:
#             # Look for vehicles that might match the category and model
#             for vehicle_name in display_names:
#                 vehicle_lower = vehicle_name.lower()
#                 if (model_slug.lower() in vehicle_lower and 
#                     category.lower() in vehicle_lower):
#                     vehicle_data = get_vehicle_data(vehicle_name, df_main)
#                     if vehicle_data:
#                         vehicle_found = vehicle_data
#                         break
        
#         if vehicle_found:
#             # Create a detailed vehicle description
#             details = []
            
#             # Basic info
#             if vehicle_found.get('vehicle_name'):
#                 details.append(f"Vehicle: {vehicle_found['vehicle_name']}")
            
#             if vehicle_found.get('brand_name'):
#                 details.append(f"Brand: {vehicle_found['brand_name']}")
            
#             if vehicle_found.get('vehicle_price'):
#                 details.append(f"Price: ₹{vehicle_found['vehicle_price']}")
            
#             if vehicle_found.get('fuel_type'):
#                 details.append(f"Fuel Type: {vehicle_found['fuel_type']}")
            
#             if vehicle_found.get('electric') and vehicle_found['electric'].lower() == 'yes':
#                 details.append("Electric: Yes")
            
#             if vehicle_found.get('power'):
#                 details.append(f"Power: {vehicle_found['power']}")
            
#             if vehicle_found.get('torque'):
#                 details.append(f"Torque: {vehicle_found['torque']}")
            
#             if vehicle_found.get('average_rating'):
#                 details.append(f"Rating: {vehicle_found['average_rating']}")
            
#             if vehicle_found.get('no_of_seats'):
#                 details.append(f"Seating: {vehicle_found['no_of_seats']}")
            
#             if vehicle_found.get('category_name'):
#                 details.append(f"Category: {vehicle_found['category_name']}")
            
#             # Join all details
#             vehicle_info = ". ".join(details)
#             return f" ({vehicle_info})"
#         else:
#             # If vehicle not found, just remove the link but keep the text
#             return ""
    
#     # Replace all vehicle URLs with vehicle details
#     enhanced_text = re.sub(vehicle_url_pattern, replace_url_with_vehicle_details, text)
    
#     # Also handle any remaining 91trucks.com links that might not be vehicle-specific
#     general_url_pattern = r'https?://www\.91trucks\.com[^\s\)]*'
#     enhanced_text = re.sub(general_url_pattern, "(Visit 91trucks.com for more information)", enhanced_text)

#     # Clean up any leftover markdown link syntax like "[More info](" or complete markdown links
#     enhanced_text = re.sub(r"\[([^\]]+)\]\((?:[^)]*)\)", r"\1", enhanced_text)
#     enhanced_text = re.sub(r"\[([^\]]+)\]\(", r"\1 ", enhanced_text)
    
#     return enhanced_text


# def find_vehicle_from_text(text: str, display_names, df_main):
#     """Try to infer a single vehicle mention from free text and return its card data.

#     Uses fuzzy matching against `display_names`. Returns a dict from `get_vehicle_data`
#     or None if no confident match is found.
#     """
#     if not text:
#         return None
#     try:
#         best_name = None
#         best_score = 0
#         lower_text = str(text).lower()
#         for disp_name in display_names:
#             score = fuzz.partial_ratio(lower_text, disp_name.lower())
#             if score > best_score:
#                 best_score = score
#                 best_name = disp_name
#         if best_name and best_score >= 85:
#             return get_vehicle_data(best_name, df_main)
#     except Exception:
#         pass
#     return None

# def get_brand_category_vehicles(prompt, df_main):
#     # Detect brand in prompt
#     detected_brand = None
#     for brand in df_main['Brand Name'].dropna().unique():
#         if brand.lower() in prompt.lower():
#             detected_brand = brand
#             break
#     if detected_brand:
#         # Optionally filter by category/keyword
#         category_keywords = [
#             'truck', 'bus', 'auto', 'rickshaw', 'vehicle', 'car', 'suv', 'pickup', 'cargo', 'trailer', 'tractor'
#         ]
#         detected_category = None
#         for cat in category_keywords:
#             if cat in prompt.lower():
#                 detected_category = cat
#                 break
#         brand_df = df_main[df_main['Brand Name'].str.lower() == detected_brand.lower()]
#         if detected_category and 'Category Name' in brand_df.columns:
#             brand_df = brand_df[brand_df['Category Name'].str.lower().str.contains(detected_category)]
#         vehicle_names = brand_df['Vehicle Name'].dropna().unique().tolist()
#         if vehicle_names:
#             matched_vehicles = []
#             for name in vehicle_names:
#                 data = get_vehicle_data(name, df_main)
#                 if data:
#                     matched_vehicles.append(data)
#                 if len(matched_vehicles) >= 5:
#                     break
#             if matched_vehicles:
#                 def vehicle_summary(vehicle):
#                     return (
#                         f"Brand: {vehicle.get('brand_name', '')}, "
#                         f"Model: {vehicle.get('model_name', '')}, "
#                         f"Vehicle Name: {vehicle.get('vehicle_name', '')}, "
#                         f"Fuel Type: {vehicle.get('fuel_type', '')}, "
#                         f"Price: {vehicle.get('vehicle_price', '')}, "
#                         f"Electric: {vehicle.get('electric', '')}, "
#                         f"No Of Seats: {vehicle.get('no_of_seats', '')}, "
#                         f"Power: {vehicle.get('power', '')}, "
#                         f"Variant: {vehicle.get('variant_name', '')}, "
#                         f"Image: {vehicle.get('vehicle_image', '')}, "
#                         f"End Point: {vehicle.get('end_point', '')}"
#                     )
#                 summaries = [vehicle_summary(v) for v in matched_vehicles]
#                 return {"status": "success", "response": summaries}
#     return None  # If no brand or vehicles found

# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=8080,debug=True)