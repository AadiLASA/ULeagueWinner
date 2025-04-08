import os
import subprocess
from tensorflow import keras

KERAS_MODEL_PATH = "league_win_predictor.keras"
SAVED_MODEL_DIR = "testing"
TFJS_OUTPUT_DIR = "tfjs_model"

# Load and save as SavedModel
model = keras.models.load_model(KERAS_MODEL_PATH)
model.export(SAVED_MODEL_DIR)  # Just give it a folder path

# Convert to TF.js format
subprocess.run([
    "tensorflowjs_converter",
    "--input_format=tf_saved_model",
    SAVED_MODEL_DIR,
    TFJS_OUTPUT_DIR
])
