import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from keras.layers.advanced_activations import LeakyReLU

IMGSIZE = 28

path = '/Users/danzam284/Desktop/mnist.npz'
with np.load(path, allow_pickle=True) as f:
    (x_train, y_train), (x_test, y_test) = (f['x_train'], f['y_train']), (f['x_test'], f['y_test'])

x_train = tf.keras.utils.normalize(x_train, axis=1)
x_test = tf.keras.utils.normalize(x_test, axis=1)

x_trainer = np.array(x_train).reshape(-1, IMGSIZE, IMGSIZE, 1)
x_tester = np.array(x_test).reshape(-1, IMGSIZE, IMGSIZE, 1)

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Conv2D(64, (3, 3), input_shape=x_trainer.shape[1:]))
model.add(tf.keras.layers.Activation(tf.nn.relu))
model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
model.add(tf.keras.layers.Conv2D(64, (3, 3)))
model.add(tf.keras.layers.Activation(tf.nn.relu))
model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
model.add(tf.keras.layers.Conv2D(64, (3, 3)))
model.add(tf.keras.layers.Activation(tf.nn.relu))
model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(64))
model.add(tf.keras.layers.Activation(tf.nn.relu))
model.add(tf.keras.layers.Dense(32))
model.add(tf.keras.layers.Activation(tf.nn.relu))
model.add(tf.keras.layers.Dense(10))
model.add(tf.keras.layers.Activation(tf.nn.softmax))

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model.fit(x_trainer, y_train, epochs=5, validation_split=0.3)

model.save('/Users/danzam284/Desktop/Python Codes/saved/my_model')

"""
Potential other model
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))
"""
