import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from keras.layers.advanced_activations import LeakyReLU

path = '/Users/danzam284/Desktop/mnist.npz'
with np.load(path, allow_pickle=True) as f:
    (x_train, y_train), (x_test, y_test) = (f['x_train'], f['y_train']), (f['x_test'], f['y_test'])

x_train = tf.keras.utils.normalize(x_train, axis=1)
x_test = tf.keras.utils.normalize(x_test, axis=1)

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model.fit(x_train, y_train, epochs=20)

model.save('/Users/danzam284/Desktop/Python Codes/saved/my_model')
