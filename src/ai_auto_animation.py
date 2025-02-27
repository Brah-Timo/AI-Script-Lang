import torch
import librosa
import numpy as np
from model import VoiceToAnimationModel  # استيراد نموذج الذكاء الاصطناعي

# تحديد الجهاز (CUDA إذا كان متاحًا، وإلا استخدام CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# تحميل النموذج المدرب
model = VoiceToAnimationModel().to(device)
model.load_state_dict(torch.load("voice_to_anim.pth", map_location=device))
model.eval()

def extract_features(audio_path):
    """
    استخراج الميزات الصوتية من الملف الصوتي
    """
    try:
        audio, sr = librosa.load(audio_path, sr=16000)  # تحميل الصوت بمعدل عينة ثابت
        mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)  # استخراج ميزات MFCC
        mfccs = np.mean(mfccs, axis=1)  # حساب المتوسط لكل ميزة
        mfccs = np.expand_dims(mfccs, axis=0)  # إضافة بُعد إضافي للـ batch
        mfccs = torch.tensor(mfccs, dtype=torch.float32).to(device)  # تحويل إلى Tensor
        
        return mfccs
    
    except Exception as e:
        print(f"❌ خطأ أثناء معالجة الملف الصوتي: {e}")
        return None

def generate_animation(audio_path):
    """
    توليد حركة بناءً على الصوت المدخل
    """
    audio_tensor = extract_features(audio_path)
    
    if audio_tensor is None:
        return None  # في حالة حدوث خطأ أثناء المعالجة

    with torch.no_grad():
        animation_data = model(audio_tensor)  # تشغيل النموذج على البيانات الصوتية

    return animation_data.cpu().numpy()  # إرجاع بيانات التحريك كـ NumPy array

# ✅ تجربة تحويل ملف صوتي إلى حركة
if __name__ == "__main__":
    animation = generate_animation("voice_input.wav")
    if animation is not None:
        print("✅ تم إنشاء بيانات التحريك بنجاح!")
        print(animation)  # إخراج بيانات التحريك
    else:
        print("❌ فشل إنشاء التحريك.")
