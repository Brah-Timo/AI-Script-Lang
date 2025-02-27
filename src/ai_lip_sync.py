import torch
import librosa
import numpy as np
import json
from model import LipSyncModel  # نموذج الذكاء الاصطناعي لمزامنة الشفاه

# تحديد الجهاز (GPU إذا كان متاحًا)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# تحميل النموذج المدرب
model = LipSyncModel().to(device)
model.load_state_dict(torch.load("lip_sync_model.pth", map_location=device))
model.eval()

def sync_lips(audio_path, text, n_mfcc=13):
    """
    مزامنة الشفاه مع الصوت باستخدام ميزات MFCC.
    """
    # تحميل الصوت وتحويله إلى تردد 16kHz
    audio, sr = librosa.load(audio_path, sr=16000)

    # استخراج ميزات MFCC من الصوت
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc)
    audio_tensor = torch.tensor(mfcc.T, dtype=torch.float32).unsqueeze(0).to(device)

    # تنفيذ التنبؤ بدون حساب المشتقات
    with torch.no_grad():
        lip_movements = model(audio_tensor)

    # تحويل بيانات تحريك الشفاه إلى مصفوفة NumPy
    lip_sync_data = lip_movements.cpu().numpy()

    # حفظ البيانات في ملف JSON
    output_data = {
        "text": text,
        "lip_sync_frames": lip_sync_data.tolist()
    }
    with open("lip_sync_data.json", "w") as f:
        json.dump(output_data, f, indent=4)

    return lip_sync_data

# ✅ تجربة مزامنة الشفاه مع الصوت
if __name__ == "__main__":
    lip_sync_result = sync_lips("dialogue.wav", "Hello! How are you?")
    print(f"✅ تم استخراج {len(lip_sync_result)} إطارًا لمزامنة الشفاه!")
