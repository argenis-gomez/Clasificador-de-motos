import tensorflow as tf
from tensorflow.keras.applications import Xception
from tensorflow.keras import layers
from tensorflow.keras.regularizers import l2


def build(num_classes, dropout_rate, factor_regularizer, img_shape):
    base_model = Xception(include_top=False, input_shape=img_shape+(3,))

    for layer in base_model.layers[:-46]:
        layer.trainable = False
    for layer in base_model.layers[-46:]:
        layer.trainable = True

    model = tf.keras.Sequential(
        [
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.Dropout(dropout_rate),
            layers.Dense(num_classes,
                         activation="softmax",
                         kernel_regularizer=l2(factor_regularizer*dropout_rate))
        ]
    )
    return model
