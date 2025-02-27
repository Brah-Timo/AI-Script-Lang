import torch
import numpy as np
from model import MotionPredictionModel

# تحديد الجهاز (CUDA إذا كان متاحًا)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# تحميل نموذج التنبؤ بالحركة
model = MotionPredictionModel().to(device)
model.load_state_dict(torch.load("motion_pred_model.pth", map_location=device))
model.eval()

# وظيفة تطبيع وإعادة تطبيع البيانات
def normalize(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data) + 1e-8)

def denormalize(data, original_min, original_max):
    return data * (original_max - original_min) + original_min

def predict_motion(motion_data):
    """التنبؤ بالحركة القادمة لشخصية 3D"""
    # استخراج القيم الأصلية قبل التطبيع
    original_min, original_max = np.min(motion_data), np.max(motion_data)
    
    # تطبيع البيانات
    motion_data = normalize(motion_data)

    # تحويل البيانات إلى Tensor وإضافة batch dimension
    motion_tensor = torch.tensor(motion_data, dtype=torch.float32).unsqueeze(0).to(device)

    with torch.no_grad():
        predicted_motion = model(motion_tensor)

    # إعادة تطبيع القيم إلى المدى الأصلي
    return denormalize(predicted_motion.cpu().numpy(), original_min, original_max)

# تجربة التنبؤ بالحركة القادمة
if __name__ == "__main__":
    motion_data = np.random.rand(50, 3)  # محاكاة لبيانات الحركة السابقة
    next_moves = predict_motion(motion_data)
    print(f"Predicted Motion: {next_moves}")
