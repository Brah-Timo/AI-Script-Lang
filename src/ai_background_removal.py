import torch
import cv2
import numpy as np
import torchvision.transforms as transforms
from PIL import Image
from model import BackgroundRemovalModel  # نموذج الذكاء الاصطناعي لإزالة الخلفية

# تحديد الجهاز (GPU إذا كان متاحًا)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# تحميل النموذج المدرب
model = BackgroundRemovalModel().to(device)
model.load_state_dict(torch.load("bg_removal.pth", map_location=device))
model.eval()

# تحويل الصورة إلى تنسيق مناسب
transform = transforms.Compose([
    transforms.ToTensor(),    # تحويل الصورة إلى Tensor
    transforms.Resize((512, 512)),  # ضبط الحجم
])

def remove_background(image_path, output_path="output.png"):
    """
    إزالة الخلفية من صورة وإرجاع صورة شفافة.
    """
    # تحميل الصورة وتحويلها إلى RGB
    image = Image.open(image_path).convert("RGB")
    image_tensor = transform(image).unsqueeze(0).to(device)

    # تنفيذ التنبؤ بدون حساب المشتقات
    with torch.no_grad():
        mask = model(image_tensor)

    # تحويل القناع إلى قيم بين 0 و 1
    mask = torch.sigmoid(mask).squeeze().cpu().numpy()

    # تحويل الصورة الأصلية إلى مصفوفة NumPy
    image_np = np.array(image.resize((512, 512)))

    # تطبيق القناع على الصورة الأصلية
    foreground = image_np * mask[:, :, None]

    # إضافة قناة ألفا لجعل الخلفية شفافة
    transparent_result = np.dstack((foreground, (mask * 255).astype(np.uint8)))

    # حفظ الصورة بتنسيق PNG مع شفافية
    output_image = Image.fromarray(transparent_result.astype(np.uint8))
    output_image.save(output_path)

    return output_path

# ✅ تجربة إزالة الخلفية من صورة
if __name__ == "__main__":
    result_path = remove_background("portrait.jpg")
    print(f"✅ تمت إزالة الخلفية بنجاح! الصورة المحفوظة: {result_path}")
