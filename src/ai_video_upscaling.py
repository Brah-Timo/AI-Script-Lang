import torch
import cv2
import numpy as np
from model import VideoSuperResolutionModel
import torchvision.transforms as transforms
from PIL import Image

# تحديد الجهاز (GPU إذا كان متاحًا، وإلا CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# تحميل نموذج تحسين الفيديو
model = VideoSuperResolutionModel().to(device)
model.load_state_dict(torch.load("super_res_model.pth", map_location=device))
model.eval()

# تحويل الصورة إلى Tensor
transform = transforms.Compose([
    transforms.ToTensor()
])

# إعادة تحويل الـ Tensor إلى صورة
to_pil = transforms.ToPILImage()

def upscale_video(video_path, output_path):
    """تحسين جودة فيديو منخفض الدقة باستخدام الذكاء الاصطناعي."""
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # تحديث حجم الفيديو المحسن إلى 2x الحجم الأصلي
    upscale_width, upscale_height = width * 2, height * 2
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (upscale_width, upscale_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # تحويل الإطار إلى PIL ثم إلى Tensor
        frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        frame_tensor = transform(frame_pil).unsqueeze(0).to(device)

        # تطبيق النموذج
        with torch.no_grad():
            upscaled_frame = model(frame_tensor)

        # تحويل Tensor إلى صورة ثم إلى NumPy
        upscaled_frame = to_pil(upscaled_frame.squeeze(0))
        upscaled_frame = np.array(upscaled_frame)
        upscaled_frame = cv2.cvtColor(upscaled_frame, cv2.COLOR_RGB2BGR)

        out.write(upscaled_frame)

    cap.release()
    out.release()

# تحسين فيديو منخفض الدقة
if __name__ == "__main__":
    upscale_video("low_res_video.mp4", "high_res_video.mp4")
