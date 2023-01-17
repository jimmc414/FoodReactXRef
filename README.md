# FoodReactXRef
Python prototype for UPC scanning Android and Iphone App that allows the tracking of food consumption via UPC cross referenced with symptoms of food reaction or intolerance and produce report showing correlations

This code prompts a user to enter a UPC code for a food item, and then makes a GET request to the Open Food Facts API to retrieve information about that food item. It then parses the response and checks if the product key exists in the JSON object returned by the API. If it does, it extracts the ingredient list and timestamp from the response, normalizes the ingredient names, removes duplicates, and creates a report containing the product's UPC code, product name, timestamp, and a list of ingredients. The code then asks the user if they want to add the ingredients to a daily food log and if the user enters 'Y', it will add each ingredient and timestamp to a DataFrame. Finally, it displays a report of all ingredients entered for the current day.

To Do:
A potential problem with this code is that it assumes that 'product' key will always be present in the JSON object returned by the API, and it also assumes that all the keys used in the code will be present in the JSON object. This can cause the code to throw an error if the API returns a different JSON object than what is expected. Also, the program does not perform any input validation for UPC code entered by the user.

Rewrite that handles both of the concerns.
