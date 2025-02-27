import torch
import cv2
import numpy as np
from model import DeepfakeModel

# تحديد الجهاز (GPU إذا كان متاحًا)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# تحميل نموذج التزييف العميق
model = DeepfakeModel().to(device)
model.load_state_dict(torch.load("deepfake_model.pth", map_location=device))
model.eval()

def preprocess_image(image_path):
    """تحميل الصورة وتحضيرها للنموذج."""
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # تحويل إلى RGB
    image = cv2.resize(image, (512, 512))
    image = image.astype(np.float32) / 255.0  # تطبيع القيم إلى [0, 1]
    image = torch.tensor(image).permute(2, 0, 1).unsqueeze(0).to(device)  # (C, H, W) مع Batch
    return image

def swap_face(source_image, target_image):
    """استبدال الوجه من صورة المصدر إلى الوجه في الصورة الهدف."""
    src_tensor = preprocess_image(source_image)
    tgt_tensor = preprocess_image(target_image)

    with torch.no_grad():
        swapped_face = model(src_tensor, tgt_tensor)

    swapped_face = swapped_face.squeeze(0).permute(1, 2, 0).cpu().numpy()  # (H, W, C)
    swapped_face = (swapped_face * 255).astype(np.uint8)  # إعادة القيم إلى [0, 255]

    return swapped_face

# تجربة استبدال الوجه
new_face = swap_face("actor.jpg", "celebrity.jpg")
cv2.imwrite("deepfake_output.jpg", cv2.cvtColor(new_face, cv2.COLOR_RGB2BGR))  # إعادة الصورة إلى BGR للحفظ
