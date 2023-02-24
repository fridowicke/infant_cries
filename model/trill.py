import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_addons as tfa

from keras import backend as K
from keras import layers, losses

# def recall_m(y_true, y_pred):
#     true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
#     possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
#     recall = true_positives / (possible_positives+K.epsilon())
#     return recall

# def precision_m(y_true, y_pred):
#     true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
#     predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
#     precision = true_positives / (predicted_positives+K.epsilon())
#     return precision

# def f1_m(y_true, y_pred):
#     precision = precision_m(y_true, y_pred)
#     recall = recall_m(y_true, y_pred)
#     return 2*((precision*recall)/(precision+recall+K.epsilon()))

# ---------------------------

def get_f1(y_true, y_pred): #taken from old keras source code
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    recall = true_positives / (possible_positives + K.epsilon())
    f1_val = 2*(precision*recall)/(precision+recall+K.epsilon())
    return f1_val


def trill(model = 'https://tfhub.dev/google/trillsson5/1'):
  input = layers.Input(shape=(None,))
  m = hub.KerasLayer(model)

  # NOTE: Audio should be floats in [-1, 1], sampled at 16kHz. Model input is of
  # the shape [batch size, time].
  # audio_samples = tf.zeros([3, 64000])

  embeddings = m(input)['embedding']

  x = layers.Flatten()(embeddings)
  x = layers.Dense(1000, activation='relu')(x)
  predictions = layers.Dense(1, activation='sigmoid')(x)

  trill_pretrained = tf.keras.Model(inputs = m.input, outputs = predictions)
  trill_pretrained.compile(optimizer='adam', loss=losses.BinaryCrossentropy(), metrics=[get_f1])
  return trill_pretrained