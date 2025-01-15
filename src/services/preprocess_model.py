import numpy as np
from PIL import Image

def preprocess_image(image: Image) -> np.ndarray:
    """
    Preprocesses an input image for model input.
    
    This function resizes the image, converts it to a NumPy array, 
    adds an extra dimension to match the model's expected input shape, 
    and normalizes the pixel values to the range [0, 1].

    Args:
        image (PIL.Image.Image): The input image to be preprocessed.

    Returns:
        np.ndarray: The preprocessed image as a NumPy array with shape (1, 224, 224, 3).
    """
    
    img = image.resize((224, 224))
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    
    return img_array
