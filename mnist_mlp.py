'''Trains a simple deep NN on the MNIST dataset.

Gets to 98.40% test accuracy after 20 epochs
(there is *a lot* of margin for parameter tuning).
2 seconds per epoch on a K520 GPU.
'''

from __future__ import print_function

import tensorflow as tf

import keras
from keras.preprocessing.image import img_to_array
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop
from PIL import Image
import glob
import numpy as np


batch_size = 128
num_classes = 11
epochs = 1

# custom data
image_list = []
for filename in glob.glob('/home/kazimieras/Downloads/notMNIST_small/A/*.png'):
    im=Image.open(filename)
    image_list.append(img_to_array(im))

x_train2 = np.array(image_list)
x_train2 = x_train2[:1000]
x_train2 = x_train2.reshape(1000, 784)


x_test2  = np.array(image_list)
x_test2  = x_test2[1000:1800]
x_test2  = x_test2.reshape(800, 784)

y_test2  = [10] * 800
y_train2 = [10] * 1000


# the data, shuffled and split between train and test sets
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train.astype('float32')
x_train = x_train.reshape(60000, 784)
x_test = x_test.reshape(10000, 784)

x_train = np.concatenate((x_train, x_train2))
x_test  = np.concatenate((x_test,  x_test2))
y_train = np.concatenate((y_train, y_train2))
y_test  = np.concatenate((y_test,  y_test2))




x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255



print(x_train.shape[0], 'train samples')


# convert class vectors to binary class matrices

y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)
y_test2 = keras.utils.to_categorical(y_test2, num_classes)


print(len(x_test), 'test samples')

model = Sequential()
model.add(Dense(512, activation='relu', input_shape=(784,)))
model.add(Dropout(0.2))
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(num_classes, activation='softmax'))

model.summary()

model.compile(loss='categorical_crossentropy',
              optimizer=RMSprop(),
              metrics=['accuracy'])

tbCallBack = keras.callbacks.TensorBoard(log_dir='/tmp/neural-network-initiation', histogram_freq=0, batch_size=batch_size, write_graph=True, write_grads=False, write_images=False, embeddings_freq=0, embeddings_layer_names=None, embeddings_metadata=None)

history = model.fit(x_train, y_train,
                    batch_size=batch_size,
                    epochs=epochs,
                    verbose=1,
                    validation_data=(x_test, y_test),
					callbacks=[tbCallBack])
score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])


#images = np.vstack([[image_list[0]]])
#pred = model.predict_classes(images)
#print("Prediction")
#print(pred)