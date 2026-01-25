from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Model

def build_resnet50_classifier(num_classes=27, trainable_layers="top"):
    """
    ResNet-50 alapú osztályozó Gravity Spy / 27 glitch osztályra.
    Implementáció: doku 5.2.5 (kis módosítással a trainable_layers szerint).
    """
    base_model = ResNet50(weights="imagenet", include_top=False, input_shape=(224, 224, 3))

    if trainable_layers == "none":
        base_model.trainable = False
    elif trainable_layers == "top":
        for layer in base_model.layers[:-30]:
            layer.trainable = False
    else:
        base_model.trainable = True

    x = GlobalAveragePooling2D()(base_model.output)
    x = Dense(1024, activation="relu")(x)
    x = Dropout(0.5)(x)
    x = Dense(512, activation="relu")(x)
    x = Dropout(0.5)(x)
    x = Dense(256, activation="relu")(x)
    predictions = Dense(num_classes, activation="softmax")(x)

    model = Model(inputs=base_model.input, outputs=predictions)
    return model
