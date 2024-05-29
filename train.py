
import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, Input

img_height, img_width = 200, 200 # image dimensions
batch_size = 32 # batch size
epochs = 25 # number of epochs


train = ImageDataGenerator(rescale=1./255, validation_split=0.2) 
validation = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train_generator = train.flow_from_directory(
    'dataset/train',
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='binary',
)


validation_generator = validation.flow_from_directory(
    'dataset/validation',
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='binary',
)

model = Sequential(
    [
        Conv2D(16, (3,3), activation='relu', input_shape=(img_height, img_width, 3)),
        MaxPooling2D(pool_size=(2,2)),
        Conv2D(32, (3,3), activation='relu', ),
        MaxPooling2D(pool_size=(2,2)),
        Conv2D(64, (3,3), activation='relu', ),
        MaxPooling2D(pool_size=(2,2)),
        Conv2D(128, (3,3), activation='relu'),
        MaxPooling2D(pool_size=(2,2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
       Dense(1, activation='sigmoid')  # Change output to 1 node with sigmoid activation
    ]
)

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'],)

model.summary()

print("Training the model...")


history = model.fit(train_generator,
                    steps_per_epoch=train_generator.samples // batch_size,
                    epochs=epochs,
                    validation_data=validation_generator)

model.save('model.keras')

loss, accuracy = model.evaluate(validation_generator)

print(f"Validation Accuracy: {accuracy * 100:.2f}%")