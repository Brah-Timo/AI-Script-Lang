import torch
import cv2
import numpy as np
from model import SceneUnderstandingModel
import torchvision.transforms as transforms
from PIL import Image

# تحديد الجهاز (GPU إذا كان متاحًا، وإلا CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# تحميل النموذج المدرب
model = SceneUnderstandingModel().to(device)
model.load_state_dict(torch.load("scene_model.pth", map_location=device))
model.eval()

# تحويل الصورة إلى Tensor مع تطبيع القيم
transform = transforms.Compose([
    transforms.Resize((512, 512)),  
    transforms.ToTensor(),  
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def analyze_scene(image_path):
    """تحليل محتوى المشهد باستخدام نموذج الذكاء الاصطناعي."""
    image = Image.open(image_path).convert("RGB")  
    image_tensor = transform(image).unsqueeze(0).to(device)  

    with torch.no_grad():
        scene_info = model(image_tensor)

    return scene_info.cpu().numpy()  # إرجاع تحليل المشهد

# تجربة تحليل المشهد
if __name__ == "__main__":
    scene_data = analyze_scene("scene.jpg")
    print("🔍 تحليل المشهد:")
    print(scene_data)
