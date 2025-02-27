import torch
import cv2
import numpy as np
from model import VideoDenoisingModel

# ضبط الجهاز ليعمل على GPU إذا كان متاحًا
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# تحميل النموذج
model = VideoDenoisingModel().to(device)
model.load_state_dict(torch.load("denoising_model.pth", map_location=device))
model.eval()

def denoise_video(video_path, output_path):
    """إزالة الضوضاء من الفيديو باستخدام نموذج الذكاء الاصطناعي."""
    
    cap = cv2.VideoCapture(video_path)
    
    # استرجاع معلومات الفيديو الأصلي
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # تحويل الصورة إلى `float32` وتطبيع القيم
        frame = frame.astype(np.float32) / 255.0
        frame_tensor = torch.tensor(frame).permute(2, 0, 1).unsqueeze(0).to(device)  # تغيير ترتيب الأبعاد

        with torch.no_grad():
            denoised_frame = model(frame_tensor)

        # تحويل الإطار مرة أخرى إلى `uint8`
        denoised_frame = denoised_frame.squeeze(0).permute(1, 2, 0).cpu().numpy()
        denoised_frame = np.clip(denoised_frame * 255, 0, 255).astype(np.uint8)

        out.write(denoised_frame)

    # إغلاق ملفات الفيديو
    cap.release()
    out.release()

# تجربة إزالة الضوضاء من فيديو
denoise_video("noisy_video.mp4", "clean_video.mp4")
