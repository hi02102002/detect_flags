import cv2
import numpy as np
from tensorflow.keras.models import load_model
import base64
import os

def get_image_file_type(image_path):
    _, file_extension = os.path.splitext(image_path)
    return file_extension.lower() 

def preprocess_image(image_path):
    img = cv2.imread(image_path)

    if img is None:
       return None
   
    img = cv2.resize(img, (200, 200)) 

    img = np.array(img) / 255.0

    img = np.expand_dims(img, axis=0)
   

    return img

def detect_flag(image_path):

    model = load_model('model.keras')
    class_names = ['VietNam', 'USA']

    img = preprocess_image(image_path)

    if img is None:
       return None


    predictions = model.predict(img)[0]

    detected_flags = []

    if(predictions is None):
        return None

    for i, score in enumerate(predictions):
        if score > 0.5:
            class_label = class_names[i]

            detected_flags.append({
                'class_label': class_label,
                'score': float(score)
            })

    for flag in detected_flags:
        label = flag['class_label']
        score = flag['score']

        cv2.rectangle(img, (0,0), (200,200), (0,255,0), 2)
        cv2.putText(img, f'{label} ({score:.2f})', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    

    print(detected_flags)


    file_extension = get_image_file_type(image_path)
    _, buffer = cv2.imencode(file_extension, img)
    img_base64 = base64.b64encode(buffer).decode()

    return img_base64


   

