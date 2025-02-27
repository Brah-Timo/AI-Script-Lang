import torch
import cv2
import numpy as np
import torchvision.transforms as transforms
from model import VideoSummarizationModel

# تحديد الجهاز (CUDA إذا كان متاحًا)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# تحميل نموذج تلخيص الفيديو
model = VideoSummarizationModel().to(device)
model.load_state_dict(torch.load("summary_model.pth", map_location=device))
model.eval()

# تحويل الصورة إلى Tensor
transform = transforms.Compose([
    transforms.ToTensor()
])

def extract_video_features(video_path, sample_rate=10):
    """ استخراج ميزات الفيديو عن طريق أخذ عينات من الإطارات وتحويلها إلى Tensors """
    cap = cv2.VideoCapture(video_path)
    frame_features = []
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # أخذ عينة كل `sample_rate` إطار فقط
        if frame_count % sample_rate == 0:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_tensor = transform(frame_rgb).unsqueeze(0).to(device)  # إضافة البُعد batch
            frame_features.append(frame_tensor)

        frame_count += 1

    cap.release()

    if len(frame_features) == 0:
        raise ValueError("لم يتم استخراج أي ميزات، تحقق من الفيديو!")

    return torch.cat(frame_features, dim=0)  # تجميع الميزات في Tensor واحد

def summarize_video(video_path):
    """ تحليل الفيديو واستخراج اللقطات المهمة """
    video_tensor = extract_video_features(video_path)

    with torch.no_grad():
        summary = model(video_tensor)

    return summary.cpu().numpy()  # إرجاع اللقطات الأساسية

# تلخيص فيديو تلقائيًا
if __name__ == "__main__":
    summary_clips = summarize_video("lecture.mp4")
    print(f"Summary Clips: {summary_clips}")
