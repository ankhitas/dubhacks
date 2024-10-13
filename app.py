import os
import random
from flask import Flask, request, jsonify, render_template
from PIL import Image
import io
import requests
import tensorflow as tf

app = Flask(__name__)

# Load pre-trained model 
#model = tf.keras.models.load_model('saved_model_epoch_0.pt')


# Function to preprocess the uploaded image for the model
'''
def preprocess_image(image):
    img = image.resize((224, 224))  # Adjust size as needed
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = img / 255.0  # Normalize if needed
    img = img.reshape(1, 224, 224, 3)  # Assuming the model needs this input shape
  
'''

# Route for rendering the HTML page
def index():
    return render_template('index.html')

# Route for handling image upload and prediction
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        # Load the image
        image = Image.open(io.BytesIO(file.read()))
        #processed_image = preprocess_image(image)
        #get indices from model
        predicted_indices = [57, 84, 88] #mock indices
        predicted_food_items = [food_items.get(index, "Not found") for index in predicted_indices]
        nutrition_query = ', '.join(predicted_food_items)

        # Fetch nutrition data from calorie ninjas api
        api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
        response = requests.get(api_url + nutrition_query, headers={'X-Api-Key': 'hI9CvNLmdaANByBcVNGUnA==VIApwPMtwczl8ZGP'})
        
        if response.status_code == requests.codes.ok:
            nutrition_data = response.json()  # Get the JSON response
            
            # Format the output in a readable list format
            formatted_nutrition = []
            for item in nutrition_data.get("items", []):
                formatted_nutrition.append({
                    'name': item['name'],
                    'calories': f"{item['calories']} kcal",
                    'serving_size': f"{item['serving_size_g']} g",
                    'fat_total': f"{item['fat_total_g']} g",
                    'fat_saturated': f"{item['fat_saturated_g']} g",
                    'protein': f"{item['protein_g']} g",
                    'sodium': f"{item['sodium_mg']} mg",
                    'potassium': f"{item['potassium_mg']} mg",
                    'cholesterol': f"{item['cholesterol_mg']} mg",
                    'carbohydrates': f"{item['carbohydrates_total_g']} g",
                    'fiber': f"{item['fiber_g']} g",
                    'sugar': f"{item['sugar_g']} g"
                })
                
            return jsonify({'prediction': formatted_nutrition})

        else:
            return jsonify({'error': f"Error fetching nutrition data: {response.status_code} - {response.text}"}), 500

    except Exception as e:
        return jsonify({'error': f'Failed to process image: {str(e)}'}), 400

food_items = {
    1: "candy",
    2: "egg tart",
    3: "french fries",
    4: "chocolate",
    5: "biscuit",
    6: "popcorn",
    7: "pudding",
    8: "ice cream",
    9: "cheese butter",
    10: "cake",
    11: "wine",
    12: "milkshake",
    13: "coffee",
    14: "juice",
    15: "milk",
    16: "tea",
    17: "almond",
    18: "red beans",
    19: "cashew",
    20: "dried cranberries",
    21: "soy",
    22: "walnut",
    23: "peanut",
    24: "egg",
    25: "apple",
    26: "date",
    27: "apricot",
    28: "avocado",
    29: "banana",
    30: "strawberry",
    31: "cherry",
    32: "blueberry",
    33: "raspberry",
    34: "mango",
    35: "olives",
    36: "peach",
    37: "lemon",
    38: "pear",
    39: "fig",
    40: "pineapple",
    41: "grape",
    42: "kiwi",
    43: "melon",
    44: "orange",
    45: "watermelon",
    46: "steak",
    47: "pork",
    48: "chicken duck",
    49: "sausage",
    50: "fried meat",
    51: "lamb",
    52: "sauce",
    53: "crab",
    54: "fish",
    55: "shellfish",
    56: "shrimp",
    57: "soup",
    58: "bread",
    59: "corn",
    60: "hamburg",
    61: "pizza",
    62: "hanamaki baozi",
    63: "wonton dumplings",
    64: "pasta",
    65: "noodles",
    66: "rice",
    67: "pie",
    68: "tofu",
    69: "eggplant",
    70: "potato",
    71: "garlic",
    72: "cauliflower",
    73: "tomato",
    74: "kelp",
    75: "seaweed",
    76: "spring onion",
    77: "rape",
    78: "ginger",
    79: "okra",
    80: "lettuce",
    81: "pumpkin",
    82: "cucumber",
    83: "white radish",
    84: "carrot",
    85: "asparagus",
    86: "bamboo shoots",
    87: "broccoli",
    88: "celery stick",
    89: "cilantro mint",
    90: "snow peas",
    91: "cabbage",
    92: "bean sprouts",
    93: "onion",
    94: "pepper",
    95: "green beans",
    96: "French beans",
    97: "king oyster mushroom",
    98: "shiitake",
    99: "enoki mushroom",
    100: "oyster mushroom",
    101: "white button mushroom",
    102: "salad",
    103: "other ingredients"
}
  
if __name__ == '_main_':
    app.run(debug=True)