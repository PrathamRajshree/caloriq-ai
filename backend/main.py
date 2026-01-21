import os
import sys
import io
import tensorflow as tf
import numpy as np
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image



# ==========================
# PATH FIX
# ==========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ML_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "ml"))
sys.path.append(ML_DIR)

from calorie_data import CALORIE_DB

# ==========================
# FASTAPI INIT
# ==========================
app = FastAPI(title="Caloriq Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = os.path.join(ML_DIR, "caloriq_food_model_v2.h5")
DATA_DIR = os.path.join(ML_DIR, "data", "processed", "train")
IMAGE_SIZE = (224, 224)

print("✅ Loading ML model...")
model = tf.keras.models.load_model(MODEL_PATH)
class_names = sorted(os.listdir(DATA_DIR))

# ==========================
# GEMINI MODEL (WORKING)
# ==========================
gemini_model = genai.GenerativeModel("gemini-1.5-flash-002")

# ==========================
# ROOT
# ==========================
@app.get("/")
def root():
    return {"status": "Caloriq backend running ✅"}

# ==========================
# IMAGE PREDICTION
# ==========================
def predict_food(image_bytes, top_k=3):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize(IMAGE_SIZE)

    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    preds = model.predict(img_array)[0]
    top_indices = preds.argsort()[-top_k:][::-1]

    return [(class_names[i], float(preds[i])) for i in top_indices]

# ==========================
# PREDICT API
# ==========================
@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    portion: str = Form(...)
):
    image_bytes = await file.read()
    predictions = predict_food(image_bytes)

    response = []
    for food, confidence in predictions:
        food_data = CALORIE_DB.get(food)
        if food_data and portion in food_data:
            response.append({
                "food": food,
                "confidence": round(confidence, 3),
                "calories": food_data[portion]
            })

    return {"top_predictions": response}

# ==========================
# 💬 GEMINI CHAT API (FIXED)
# ==========================
@app.post("/chat")
async def chat(message: str = Form(...)):
    try:
        import google.generativeai as genai
        import os

        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

        model = genai.GenerativeModel("gemini-1.5-flash-002")

        prompt = f"""
You are Caloriq AI, a nutrition expert.
Answer clearly, practically, and simply.

User question:
{message}
"""
        response = model.generate_content(prompt)

        return {"reply": response.text.strip()}

    except Exception as e:
        print("Gemini error:", e)
        return {
            "reply": "⚠️ AI chat temporarily unavailable."
        }
