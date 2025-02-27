import torch
import cv2
import numpy as np
from model import FaceRelightingModel

# تحديد الجهاز (GPU إذا كان متاحًا)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# تحميل النموذج
model = FaceRelightingModel().to(device)
model.load_state_dict(torch.load("relighting_model.pth", map_location=device))
model.eval()

def relight_face(image_path, output_path="relit_face.jpg"):
    """تحسين إضاءة الوجه داخل صورة باستخدام نموذج الذكاء الاصطناعي."""
    
    # تحميل الصورة وتحويلها إلى `float32`
    image = cv2.imread(image_path)
    image = cv2.resize(image, (512, 512))
    image = image.astype(np.float32) / 255.0  # تطبيع القيم

    # تحويل الصورة إلى Tensor بالترتيب الصحيح
    image_tensor = torch.tensor(image).permute(2, 0, 1).unsqueeze(0).to(device)

    with torch.no_grad():
        relit_face = model(image_tensor)

    # تحويل الإطار مرة أخرى إلى `uint8`
    relit_face = relit_face.squeeze(0).permute(1, 2, 0).cpu().numpy()
    relit_face = np.clip(relit_face * 255, 0, 255).astype(np.uint8)

    # حفظ الصورة الجديدة
    cv2.imwrite(output_path, relit_face)

# تحسين إضاءة الوجه داخل صورة
relight_face("face.jpg")
