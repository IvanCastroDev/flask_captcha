import tensorflow as tf
import cv2
from PIL import Image
import os
def encode_single_sample(img_path):
    img_width = 220
    img_height = 40

    # 1. Read image
    img = tf.io.read_file(img_path)
    # 2. Decode and convert to grayscale
    img = tf.io.decode_png(img, channels=1)
    # 3. Convert to float32 in [0, 1] range
    img = tf.image.convert_image_dtype(img, tf.float32)
    # 4. Resize to the desired size
    img = tf.image.resize(img, [img_height, img_width])
    # 5. Transpose the image because we want the time
    # dimension to correspond to the width of the image.
    img = tf.transpose(img, perm=[1, 0, 2])
    # 7. Return a dict as our model is expecting two inputs
    return {"image": img}

def processImage(img_path):
    with Image.open(img_path) as img:
        path = f"./captchas/{img_path.split('/')[2].replace('.', '')}.jpg"
        img = img.convert('L')
        img = img.point(lambda x: 0 if x < 225 else 255, '1')
        img = img.point(lambda x: 0 if x >= 230 else 255)
        img.save(path)
        img = cv2.imread(path)
        img = cv2.bitwise_not(img)
        cv2.imwrite(path, img)

        os.remove(img_path)

        return path