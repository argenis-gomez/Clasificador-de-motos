import tensorflow as tf
from tensorflow.keras.applications.xception import preprocess_input
from motos_1_clases import clases_dict as values
from motos_2_clases import clases_dict as clases


def load_model(model_path):
    return tf.keras.models.load_model(model_path)


def process_image(image, img_shape):
    img = tf.io.decode_image(image, channels=3)
    img = tf.image.resize(img, img_shape)
    img = preprocess_input(img)
    img = tf.expand_dims(img, axis=0)
    return img


def return_prediction(image, model, img_shape, motos_classes=True):
    image = process_image(image, img_shape)
    result = model(image)

    prediction = tf.argmax(result[0]).numpy()

    if motos_classes:
        return clases[prediction], prediction
    else:
        return values[prediction], prediction
