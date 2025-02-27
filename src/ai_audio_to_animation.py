import torch
import librosa
import numpy as np
from model import AudioAnimationModel

# تحديد الجهاز (GPU إذا كان متاحًا)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# تحميل نموذج تحويل الصوت إلى حركة
model = AudioAnimationModel().to(device)
model.load_state_dict(torch.load("audio_anim_model.pth", map_location=device))
model.eval()

def audio_to_animation(audio_path):
    """تحليل الصوت وتحويله إلى رسوم متحركة باستخدام نموذج الذكاء الاصطناعي."""

    # تحميل الصوت ومعاينته
    audio, sr = librosa.load(audio_path, sr=16000)  # إعادة التشكيل إلى 16kHz

    # استخراج ميزات Mel Spectrogram
    mel_spectrogram = librosa.feature.melspectrogram(y=audio, sr=sr, n_mels=128, fmax=8000)
    mel_spectrogram = librosa.power_to_db(mel_spectrogram, ref=np.max)

    # تحويل إلى Tensor وتطبيع القيم
    audio_tensor = torch.tensor(mel_spectrogram, dtype=torch.float32).unsqueeze(0).to(device)

    with torch.no_grad():
        animation_data = model(audio_tensor)

    return animation_data.cpu().numpy()

# تجربة تحويل الصوت إلى رسوم متحركة
animation = audio_to_animation("voice.wav")
print(f"Generated Animation Data: {animation}")
