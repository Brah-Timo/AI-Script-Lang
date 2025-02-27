import torch
import cv2
import numpy as np
import torchvision.transforms as transforms
from model import ObjectDetection3DModel

# تحديد الجهاز (CUDA إذا كان متاحًا)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# تحميل نموذج اكتشاف الأجسام ثلاثية الأبعاد
model = ObjectDetection3DModel().to(device)
model.load_state_dict(torch.load("3d_object_model.pth", map_location=device))
model.eval()

# تحويل الصورة إلى Tensor
transform = transforms.Compose([
    transforms.ToTensor()
])

def detect_3d_objects(video_path, frame_size=(512, 512)):
    """ اكتشاف الأجسام ثلاثية الأبعاد داخل فيديو """
    cap = cv2.VideoCapture(video_path)
    objects_detected = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # معالجة الإطار وضبط الحجم
        frame_resized = cv2.resize(frame, frame_size)
        frame_tensor = transform(frame_resized).unsqueeze(0).to(device)  # إضافة بُعد batch

        with torch.no_grad():
            detected_objects = model(frame_tensor)

        objects_detected.append(detected_objects.cpu().numpy())

    cap.release()
    return objects_detected

# تجربة اكتشاف الأجسام ثلاثية الأبعاد داخل فيديو
if __name__ == "__main__":
    detected_objects = detect_3d_objects("drone_view.mp4")
    print(f"Detected 3D Objects: {detected_objects}")
