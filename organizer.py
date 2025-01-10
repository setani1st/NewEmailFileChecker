import os
from NeuralNetwork.predict import predict_image

def classify_file(file_path):
    # Call the pre-trained model
    result = predict_image(file_path)
    return result  # e.g., "Passport", "ID", etc.
