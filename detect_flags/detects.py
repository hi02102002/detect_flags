import base64
import os
import asyncio
from ultralytics import YOLO
import subprocess
from moviepy.editor import VideoFileClip

def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read())
        base64_string = encoded_string.decode('utf-8')
        return f'data:image/{get_file_type(image_path)};base64,{base64_string}'

def video_to_base64(video_path):
    with open(video_path, "rb") as video_file:
        encoded_string = base64.b64encode(video_file.read())
        base64_string = encoded_string.decode('utf-8')
        return f'data:video/{get_file_type(video_path)};base64,{base64_string}'

def get_file_type(file_path):
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower().strip('.')

async def detect_objects(file_path):
    file_type = get_file_type(file_path)
    
    if file_type not in ['jpg', 'jpeg', 'png', 'mp4', 'avi', 'mov','webp']:
        raise ValueError('Invalid file type. Supported file types are jpg, jpeg, png, mp4, avi, mov')
    
    model = YOLO("E:/detect_flags/runs/detect/train14/weights/best.pt")

    if file_type in ['jpg', 'jpeg', 'png']:
        results = await asyncio.to_thread(model.predict, file_path, save=True, conf=0.5 )

        print(results)

        img_path = results[0].save_dir + '\\' + results[0].path.replace('E:\\detect_flags\\media\\', '') 

        print(img_path)

        return image_to_base64(img_path)
    
    if file_type in ['mp4', 'avi', 'mov']:
        results = await asyncio.to_thread(model.predict, file_path, save=True, conf=0.5, )


        file_name = os.path.basename(file_path)

        input_path = results[0].save_dir + '\\' + file_name.replace('mp4', 'avi')

        output_path = results[0].save_dir + '\\' + file_name

        clip = VideoFileClip(input_path)

        clip.write_videofile(output_path, codec='libx264')

        return video_to_base64(output_path)
