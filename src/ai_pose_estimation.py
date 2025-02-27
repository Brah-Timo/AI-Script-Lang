import torch
import cv2
import numpy as np
from model import PoseEstimationModel

# تحديد الجهاز (GPU إذا كان متاحًا)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# تحميل النموذج
model = PoseEstimationModel().to(device)
model.load_state_dict(torch.load("pose_model.pth", map_location=device))
model.eval()

def estimate_pose(image_path):
    """تحليل وضعيات الجسد داخل صورة باستخدام نموذج الذكاء الاصطناعي."""
    
    # تحميل الصورة وتحويلها إلى `float32`
    image = cv2.imread(image_path)
    image = cv2.resize(image, (512, 512))
    image = image.astype(np.float32) / 255.0  # تطبيع القيم

    # تحويل الصورة إلى Tensor بالترتيب الصحيح
    image_tensor = torch.tensor(image).permute(2, 0, 1).unsqueeze(0).to(device)

    with torch.no_grad():
        pose_data = model(image_tensor)

    # تحويل المخرجات إلى NumPy
    pose_data = pose_data.squeeze(0).cpu().numpy()

    return pose_data

# تحليل وضعيات الجسد داخل صورة
pose_info = estimate_pose("person.jpg")
print(f"Pose Data: {pose_info}")
