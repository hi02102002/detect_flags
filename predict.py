from ultralytics import YOLO


model = YOLO("runs/detect/train14/weights/best.pt")

results = model.predict('./image_1.png', save=True)

