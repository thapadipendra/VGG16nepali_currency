# -*- coding: utf-8 -*-
"""vggfrmlecture.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YL8T8o6jjYg2jYuivFBmNJJQ9ip7Z183
"""

import tensorflow as tf
from google.colab import drive 
drive.mount('/content/drive/')
import os
import zipfile
dataset_path = "/content/drive/MyDrive/Colab Notebooks/nepali_notes.zip"
zip_object = zipfile.ZipFile(file=dataset_path, mode="r")
zip_object.extractall("./")
zip_object.close()

from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_dir='/content/nepali_notes/train'
valid_dir='/content/nepali_notes/valid'

 
train_datagen = ImageDataGenerator(
      rescale=1./255,
      rotation_range=90,
      width_shift_range=0.1,
      height_shift_range=0.1,
      shear_range=0.1,
      zoom_range=[0.9, 1.5],
      horizontal_flip=True,
      vertical_flip=True,
      fill_mode='nearest')
test_datagen = ImageDataGenerator(rescale=1./255)


train_generator= train_datagen.flow_from_directory(directory=train_dir,
                                                    target_size=(224, 224),
                                                    batch_size=20,
                                                    shuffle=True,
                                                   class_mode='categorical'
                                                     )

validation_generator  = test_datagen.flow_from_directory(directory=valid_dir,
                                                  target_size=(224, 224),
                                                  batch_size=20,
                                                  shuffle=False)



train_generator.class_indices

from tensorflow.keras.applications import VGG16
conv_base=VGG16(weights='imagenet',include_top=False,input_shape=(224, 224,3))
conv_base.summary()

from tensorflow.keras import models
from tensorflow.keras import layers

model=models.Sequential()
model.add(conv_base)
model.add(layers.Flatten())
model.add(layers.Dense(256,activation='relu'))
model.add(layers.Dense(7,activation='sigmoid'))
model.summary()

# conv_base.trainable=False
from tensorflow.keras import optimizers
model.compile(loss='categorical_crossentropy',optimizer=optimizers.RMSprop(lr=1e-5),metrics=['categorical_accuracy'])

# checkpoint_cb=keras.callbacks.
history = model.fit_generator(generator=train_generator,
                                  epochs=10,
                                  validation_data=validation_generator,
                                  )

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline

pd.DataFrame(history.history).plot(figsize=(8,5))
plt.grid(True)
plt.gca().set_ylim(0,1)
plt.show()

from PIL import Image
import numpy as np
from skimage import transform
def load(filename):
   np_image = Image.open(filename)
   np_image = np.array(np_image).astype('float32')/255
   np_image = transform.resize(np_image, (224, 224, 3))
   np_image = np.expand_dims(np_image, axis=0)
   return np_image

image = load('/content/R5b268b451f54a90d19a816edd52deeba.jpg')
model.predict(image)

model.save('mymodel.h5')

converter = tf.lite.TFLiteConverter.from_saved_model('/content/mymodel')
tflite_model = converter.convert()

with open('model.tflite', 'wb') as f:
  f.write(tflite_model)

loaded = models.load_model('/content/mymodel.h5')

loaded.summary()