import requests
import json
import datetime
import pandas as pd
from difflib import get_close_matches

# Create the DataFrame to store ingredients and timestamps
ingredients_df = pd.DataFrame(columns=['ingredient', 'timestamp'])

# Prompt the user for the UPC code of the food item they want to look up
upc = input("Enter the UPC code of the food item you want to look up: ")

# Make a GET request to the Open Food Facts API
response = requests.get(f'https://world.openfoodfacts.org/api/v0/product/{upc}.json')

# Parse the JSON response
data = json.loads(response.text)

# Check if the product key exists in the JSON object
if 'product' not in data:
    print(f"Invalid UPC code {upc}.")
    exit()

# Extract the ingredient list and timestamp from the response
ingredient_list = data.get('product', {}).get('ingredients', [])
timestamp = datetime.datetime.fromtimestamp(int(data['product']['last_modified_t'])).strftime('%H:%M %d-%m-%Y')

# Normalize ingredient names
norm_ingredient_list = []
for ingredient in ingredient_list:
    text = ingredient.get('text', '')
    matches = get_close_matches(text, ingredient_list, n=1, cutoff=0.8)
    if matches:
        norm_text = matches[0]
        norm_ingredient_list.append(norm_text)
    else:
        norm_ingredient_list.append(text)

# Remove duplicates
norm_ingredient_list = list(set(norm_ingredient_list))

# Create the report
report = "\n"
report += "Ingredient Report\n"
report += "UPC: " + upc + "\n"
report += "Product Name: " + data['product']['product_name'] + "\n"
report += "Timestamp: " + timestamp + "\n"


# Iterate through the ingredient list and add each ingredient to the report
for ingredient in norm_ingredient_list:
    report += "Ingredient: " + ingredient + "\n"
    report += "---\n"

#Print the report
print(report)

#Ask the user if they want to add the ingredients to the daily food log
add_to_log = input("Add these ingredients to daily food log? (Y/N) ")

#If the user enters Y, add each ingredient and timestamp to the DataFrame
if add_to_log.upper() == 'Y':
    for ingredient in norm_ingredient_list:
        ingredients_df = pd.concat([ingredients_df, pd.DataFrame({'ingredient': ingredient, 'timestamp': timestamp}, index=[0])], ignore_index=True)

#Display a report of all ingredients entered for the current day
ingredient_count = ingredients_df[ingredients_df['timestamp'] == timestamp].groupby('ingredient').size().reset_index(name='count')

if ingredient_count.shape[0]>0:
    print("Daily Food Log for " + timestamp + "\n")
    print(ingredient_count)
else:
    print("No ingredients have been added to the Daily Food Log for " + timestamp)
