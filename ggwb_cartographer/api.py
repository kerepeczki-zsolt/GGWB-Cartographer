from flask import Flask, request, jsonify
import base64
import io
import time

import numpy as np
from PIL import Image

from ggwb_cartographer.features import GeometricFeatureExtractor
from ggwb_cartographer.models import build_resnet50_classifier, ensemble_predict


app = Flask(__name__)

# TODO: ide később betöltjük a valódi, betanított modelleket
feature_extractor = GeometricFeatureExtractor()
# ideiglenes: egyetlen frissen létrehozott modell, hogy a kód fusson
ensemble_models = [build_resnet50_classifier()]

# 27 osztály helykitöltő nevei – később cseréljük a végleges Gravity Spy / saját label listára
CLASSES = [
    "CHIRP",
    "POWER_LINE",
    "BLIP",
    "SCATTERED_LIGHT",
    "NO_GLITCH",
    "CLASS_6",
    "CLASS_7",
    "CLASS_8",
    "CLASS_9",
    "CLASS_10",
    "CLASS_11",
    "CLASS_12",
    "CLASS_13",
    "CLASS_14",
    "CLASS_15",
    "CLASS_16",
    "CLASS_17",
    "CLASS_18",
    "CLASS_19",
    "CLASS_20",
    "CLASS_21",
    "CLASS_22",
    "CLASS_23",
    "CLASS_24",
    "CLASS_25",
    "CLASS_26",
    "CLASS_27",
]


def preprocess_spectrogram(image: Image.Image):
    """
    Alap előfeldolgozás: RGB-re konvertálás, 224x224-re méretezés, [0,1] normálás.
    A végleges rendszerben ezt a LIGO/Gravity Spy pipeline-hoz igazítjuk.
    """
    image = image.convert("RGB")
    image = image.resize((224, 224))
    arr = np.array(image).astype("float32") / 255.0
    return arr


@app.route("/classify", methods=["POST"])
def classify_spectrogram():
    start_time = time.time()

    try:
        data = request.json
        img_data = base64.b64decode(data["spectrogram_data"])
        image = Image.open(io.BytesIO(img_data))

        spectrogram = preprocess_spectrogram(image)

        # Ha a feature-extractor 2D mátrixot vár, itt igazítjuk
        features = feature_extractor.extract_all_features(spectrogram)

        # Ensemble előrejelzés (jelenleg dummy, később betöltött modellekkel)
        # features [92] -> [1, 92] batch dimenzió
        pred = ensemble_predict(ensemble_models, features[None, :])

        predicted_index = int(np.argmax(pred))
        predicted_label = (
            CLASSES[predicted_index] if 0 <= predicted_index < len(CLASSES) else predicted_index
        )

        return jsonify(
            {
                "classification": predicted_label,
                "confidence": float(np.max(pred)),
                "processing_time": time.time() - start_time,
                "all_probabilities": pred.tolist(),
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
