import torch
import librosa
import numpy as np
from model import VoiceToAnimationModel  # نموذج ذكاء اصطناعي لتحليل الصوت وتحويله إلى حركة

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = VoiceToAnimationModel().to(device)
model.load_state_dict(torch.load("voice_to_anim.pth", map_location=device))
model.eval()

def generate_animation(audio_path):
    audio, sr = librosa.load(audio_path, sr=16000)
    audio_features = np.expand_dims(audio, axis=0)
    audio_tensor = torch.tensor(audio_features, dtype=torch.float32).to(device)

    with torch.no_grad():
        animation_data = model(audio_tensor)

    return animation_data.cpu().numpy()  # بيانات التحريك

# تجربة توليد الحركة من ملف صوتي
animation = generate_animation("voice_input.wav")
print(animation)  # إخراج بيانات التحريك
