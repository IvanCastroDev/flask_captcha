import tensorflow as tf
from tensorflow import keras
from keras import layers
from matplotlib import pyplot as plt
import numpy as np
from images import encode_single_sample

characters = ['2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'P', 'Q', 'R', 'S', 'T', 'V', 'X', 'Y', 'a', 'b', 'c', 'd', 'e', 'f', 'h', 'j', 'k', 'm', 'n', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y']

model_path = "./model/captcha.H5"
model = tf.keras.models.load_model(model_path, compile=False)

def predictText(filename):
    aux = tf.data.Dataset.from_tensor_slices(([filename]))
    aux = (
        aux.map(encode_single_sample, num_parallel_calls=tf.data.AUTOTUNE)
        .batch(1)
        .prefetch(buffer_size=tf.data.AUTOTUNE)
    )

    def decode_batch_predictions(pred):
        # Mapping characters to integers
        char_to_num = layers.StringLookup(vocabulary=list(characters), mask_token=None)

        # Mapping integers back to original characters
        num_to_char = layers.StringLookup(
            vocabulary=char_to_num.get_vocabulary(), mask_token=None, invert=True
        )
        input_len = np.ones(pred.shape[0]) * pred.shape[1]
        # Use greedy search. For complex tasks, you can use beam search
        results = keras.backend.ctc_decode(pred, input_length=input_len, greedy=True)[0][0][
            :, :7
        ]
        # Iterate over the results and get back the text
        output_text = []
        for res in results:
            res = tf.strings.reduce_join(num_to_char(res)).numpy().decode("utf-8")
            output_text.append(res)
        return output_text


    for image in aux.take(1):
        batch_images = image['image']
        predict = model.predict(batch_images)
        pred_texts = decode_batch_predictions(predict)


        # Debug
        """ _, ax = plt.subplots(1, 1, figsize=(10, 5))
        
        img = (batch_images[0, :, :, 0] * 255).numpy().astype(np.uint8)
        img = img.T
        title = f"Prediction: {pred_texts[0]}"
        ax.imshow(img, cmap="gray")
        ax.set_title(title)
        ax.axis("off")

    plt.show() """
    return pred_texts[0]