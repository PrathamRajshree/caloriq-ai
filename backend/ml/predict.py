import tensorflow as tf
import numpy as np
import os
from tensorflow.keras.preprocessing import image

# ==========================
# CONFIG
# ==========================
MODEL_PATH = "caloriq_food_model_v2.h5"
IMAGE_SIZE = (224, 224)
DATA_DIR = "data/processed/train"

# ==========================
# CALORIE DATABASE
# ==========================
CALORIE_DB = {
    "poha": {
        "small": 180,
        "medium": 250,
        "large": 330
    },
    "biryani": {
        "small": 290,
        "medium": 420,
        "large": 550
    },
    "chapati": {
        "small": 120,
        "medium": 180,
        "large": 240
    },
    "paneer_butter_masala": {
        "small": 280,
        "medium": 380,
        "large": 520
    }
}

# ==========================
# LOAD MODEL
# ==========================
model = tf.keras.models.load_model(MODEL_PATH)

# Load class names in correct order
class_names = sorted(os.listdir(DATA_DIR))

# ==========================
# PREDICT FUNCTION
# ==========================
def predict_food(img_path):
    img = image.load_img(img_path, target_size=IMAGE_SIZE)
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)
    confidence = float(np.max(predictions))
    class_index = int(np.argmax(predictions))

    return class_names[class_index], confidence


# ==========================
# CALORIE FUNCTION
# ==========================
def get_calories(food, portion):
    if food in CALORIE_DB:
        return CALORIE_DB[food].get(portion)
    return None


# ==========================
# TEST RUN
# ==========================
if __name__ == "__main__":
    test_image = "test.jpg"     # add any food image here
    portion = "medium"          # small | medium | large

    food, confidence = predict_food(test_image)
    calories = get_calories(food, portion)

    print("\n🍽️ CALORIQ RESULT")
    print("-------------------")
    print(f"Predicted Food : {food}")
    print(f"Confidence     : {confidence * 100:.2f}%")
    print(f"Portion Size   : {portion}")

    if calories:
        print(f"Calories       : {calories} kcal")
    else:
        print("Calories       : Not available")
