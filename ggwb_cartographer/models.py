import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models


def build_resnet50_classifier():
    base_model = tf.keras.applications.ResNet50(
        weights="imagenet",
        include_top=False,
        input_shape=(224, 224, 3),
    )

    model = models.Sequential(
        [
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.Dense(1024, activation="relu"),
            layers.Dropout(0.5),
            layers.Dense(512, activation="relu"),
            layers.Dropout(0.5),
            layers.Dense(256, activation="relu"),
            layers.Dense(27, activation="softmax"),  # 27 classes
        ]
    )

    return model


def ensemble_predict(models_list, X):
    predictions = []
    weights = [0.25, 0.22, 0.20, 0.18, 0.15]  # Based on validation F1

    for i, model in enumerate(models_list):
        pred = model.predict(X)
        predictions.append(weights[i] * pred)

    return np.sum(predictions, axis=0)
