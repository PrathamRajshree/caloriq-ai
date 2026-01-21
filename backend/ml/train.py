import os
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

# ==============================
# CONFIGURATION
# ==============================
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 16
INITIAL_EPOCHS = 5          # already trained, keep for structure
FINE_TUNE_EPOCHS = 10       # NEW
DATA_DIR = "data/processed"

BASE_MODEL_NAME = "caloriq_food_model.h5"
FINE_TUNED_MODEL_NAME = "caloriq_food_model_v2.h5"

# ==============================
# DATA GENERATORS
# ==============================
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.15,
    horizontal_flip=True
)

val_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    os.path.join(DATA_DIR, "train"),
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical"
)

val_generator = val_datagen.flow_from_directory(
    os.path.join(DATA_DIR, "val"),
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical"
)

NUM_CLASSES = train_generator.num_classes
print("Number of classes:", NUM_CLASSES)

# ==============================
# LOAD BASE MODEL
# ==============================
base_model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=(224, 224, 3)
)

# Freeze all layers initially
base_model.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(256, activation="relu")(x)
x = Dropout(0.4)(x)
outputs = Dense(NUM_CLASSES, activation="softmax")(x)

model = Model(inputs=base_model.input, outputs=outputs)

# ==============================
# COMPILE (INITIAL)
# ==============================
model.compile(
    optimizer=Adam(learning_rate=1e-4),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# ==============================
# INITIAL TRAINING (SHORT)
# ==============================
print("🚀 Initial training...")
model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=INITIAL_EPOCHS
)

model.save(BASE_MODEL_NAME)
print(f"✅ Base model saved as {BASE_MODEL_NAME}")

# ==============================
# FINE-TUNING
# ==============================
print("🔧 Fine-tuning last CNN layers...")

base_model.trainable = True

# Freeze bottom layers, unfreeze top layers
for layer in base_model.layers[:-30]:
    layer.trainable = False

model.compile(
    optimizer=Adam(learning_rate=1e-5),  # VERY IMPORTANT
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=FINE_TUNE_EPOCHS
)

# ==============================
# SAVE FINAL MODEL
# ==============================
model.save(FINE_TUNED_MODEL_NAME)
print(f"🔥 Fine-tuned model saved as {FINE_TUNED_MODEL_NAME}")
