from flask import current_app
import tensorflow as tf

def get_model() -> tf.keras.Model:
    """
    Load the machine learning model from the path specified in the Flask app's config.

    Returns:
        tf.keras.Model: The TensorFlow Keras model that was loaded from the specified path.
    """
    config = current_app.config
    model = tf.keras.models.load_model(config['MODEL_PATH'])

    return model
