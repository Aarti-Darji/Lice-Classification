# -*- coding: utf-8 -*-
"""Lice Classification

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ns82rnie5eUUwUGfygsgi_OV9t-3RgBr
"""

from google.colab import drive
drive.mount('/content/drive')

#Import the libraries
import zipfile
import os

zip_ref = zipfile.ZipFile('/content/drive/MyDrive/LICE_UTA2.zip', 'r') #Opens the zip file in read mode
zip_ref.extractall('/tmp') #Extracts the files into the /tmp folder
zip_ref.close()

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

sp1 = Image.open('/tmp/LICE_UTA/sp1/GBIF.1826285118.Camp.F.V.jpg')

print(sp1.format)
print(sp1.size)
print(sp1.mode)
# show the image
sp1.show()

dir_path = "/tmp/LICE_UTA"

# Get a list of all subdirectories within the directory path
class_labels = os.listdir(dir_path)

# Initialize a list to store the counts
counts = []

# Loop through each subdirectory and count the number of image files
for class_label in class_labels:
    class_dir = os.path.join(dir_path, class_label)
    count = len(os.listdir(class_dir))
    counts.append(count)

# Plot the counts as a bar graph
plt.bar(class_labels, counts)
plt.title("Number of Images in Each Class")
plt.xlabel("Class Label")
plt.ylabel("Count")
plt.show()

import os
import random
import shutil

# Set the path to the directory containing the images
path = "/tmp/LICE_UTA"

# Set the ratio of images to use for testing and validation
test_ratio = 0.1
val_ratio = 0.2

# Get the list of subdirectories
subdirs = [x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x)) and x not in ['train', 'test', 'val']]

# Create the train, test, and validation directories if they do not exist
train_dir = os.path.join(path, 'train')
if not os.path.exists(train_dir):
    os.mkdir(train_dir)

test_dir = os.path.join(path, 'test')
if not os.path.exists(test_dir):
    os.mkdir(test_dir)

val_dir = os.path.join(path, 'val')
if not os.path.exists(val_dir):
    os.mkdir(val_dir)

# Loop through each subdirectory
for subdir in subdirs:
    # Get the path to the subdirectory
    subdir_path = os.path.join(path, subdir)

    # Create the subdirectories in train, test, and validation directories if they don't exist
    train_subdir = os.path.join(train_dir, subdir)
    if not os.path.exists(train_subdir):
        os.makedirs(train_subdir)

    test_subdir = os.path.join(test_dir, subdir)
    if not os.path.exists(test_subdir):
        os.makedirs(test_subdir)

    val_subdir = os.path.join(val_dir, subdir)
    if not os.path.exists(val_subdir):
        os.makedirs(val_subdir)

    # Loop through each image file in the subdirectory
    for filename in os.listdir(subdir_path):
        if filename.endswith(".jpg"):
            # Decide whether to move this file to the train, test, or validation directory
            rand = random.random()
            if rand < test_ratio:
                dest = os.path.join(test_subdir, filename)
            elif rand < test_ratio + val_ratio:
                dest = os.path.join(val_subdir, filename)
            else:
                dest = os.path.join(train_subdir, filename)

            # Move the file to the appropriate directory
            shutil.move(os.path.join(subdir_path, filename), dest)

from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Set the batch size and image size
batch_size = 32
img_size = (224, 224)

# Define the paths to the train and validation data
train_dir = '/tmp/LICE_UTA/train'
val_dir = '/tmp/LICE_UTA/val'
test_dir = '/tmp/LICE_UTA/test'

# Create ImageDataGenerator for the train and validation data
train_datagen = ImageDataGenerator(
    rotation_range=30,
    zoom_range=0.2,
    width_shift_range=0.3,
    height_shift_range=0.3,
    horizontal_flip=True,
    vertical_flip=False,
    brightness_range=[0.5, 1.5],
    channel_shift_range=0.4
)

val_datagen = ImageDataGenerator(
    rotation_range=30,
    zoom_range=0.2,
    width_shift_range=0.3,
    height_shift_range=0.3,
    horizontal_flip=True,
    vertical_flip=False,
    brightness_range=[0.5, 1.5],
    channel_shift_range=0.4
)
test_datagen = ImageDataGenerator(
    rotation_range=30,
    zoom_range=0.2,
    width_shift_range=0.3,
    height_shift_range=0.3,
    horizontal_flip=True,
    vertical_flip=False,
    brightness_range=[0.5, 1.5],
    channel_shift_range=0.4
)
# Load the training and validation data using the ImageDataGenerator
train_ds = train_datagen.flow_from_directory(
    train_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode='categorical'
)

val_ds = val_datagen.flow_from_directory(
    val_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode='categorical'
)

test_ds = test_datagen.flow_from_directory(
    test_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode='categorical'
)

# Get a batch of images from the generator
images, labels = train_ds.next()

# Plot the images
fig, axs = plt.subplots(4, 4, figsize=(10, 10))
axs = axs.flatten()

for img, ax in zip(images, axs):
    ax.imshow(img.astype('uint8'))
    ax.axis('off')

plt.tight_layout()
plt.show()

from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array

img = load_img('/tmp/LICE_UTA/val/sp1/RP.AI.015884.Camp.F.V.jpg')
img = img.resize((224, 224))

img_array = img_to_array(img)

img_array = np.expand_dims(img_array, axis=0)
augmented_images = train_datagen.flow(img_array)

# Plot the augmented images
fig, axs = plt.subplots(1, 5, figsize=(15, 5))
for i in range(5):
    axs[i].imshow(augmented_images.next()[0].astype('uint8'))
plt.show()

resnet = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Freeze the weights of the ResNet50 model
for layer in resnet.layers:
    layer.trainable = False

# Add a new output layer to the ResNet50 model
x = resnet.output
x = GlobalAveragePooling2D()(x)
x = Dense(256, activation='relu')(x)
predictions = Dense(train_ds.num_classes, activation='softmax')(x)

model = Model(inputs=resnet.input, outputs=predictions)

# Compile the model with Adam optimizer and categorical cross-entropy loss
model.compile(optimizer=Adam(lr=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model with the augmented dataset
history = model.fit(train_ds, epochs=10, validation_data=val_ds)

test_loss, test_acc = model.evaluate(test_ds)
print("Test loss:", test_loss)
print("Test accuracy:", test_acc)

# Plot the training and validation accuracy and loss
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(1, len(acc) + 1)

plt.plot(epochs, acc, 'b', label='Training acc')
plt.plot(epochs, val_acc, 'r', label='Validation acc')
plt.title('Training and validation accuracy')
plt.legend()

plt.figure()

plt.plot(epochs, loss, 'b', label='Training loss')
plt.plot(epochs, val_loss, 'r', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()

plt.show()

from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.models import Model

# Load the pre-trained VGG-16 model without the top layer
base_model = VGG16(include_top=False, input_shape=(224, 224, 3))

# Freeze the pre-trained layers so they are not trainable
for layer in base_model.layers:
    layer.trainable = False

# Add new trainable layers on top of the frozen layers for classification
x = base_model.output
x = Flatten()(x)
x = Dense(256, activation='relu')(x)
x = Dropout(0.5)(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.5)(x)
predictions = Dense(8, activation='softmax')(x)

# Define the new model
model = Model(inputs=base_model.input, outputs=predictions)

# Compile the model with appropriate optimizer, loss function, and metrics
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

history = model.fit(train_ds, epochs=10, validation_data=val_ds)

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(1, len(acc) + 1)

plt.plot(epochs, acc, 'b', label='Training acc')
plt.plot(epochs, val_acc, 'r', label='Validation acc')
plt.title('Training and validation accuracy')
plt.legend()

plt.figure()

plt.plot(epochs, loss, 'b', label='Training loss')
plt.plot(epochs, val_loss, 'r', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()

plt.show()

test_loss, test_acc = model.evaluate(test_ds)
print("Test Loss:", test_loss)
print("Test Accuracy:", test_acc)

