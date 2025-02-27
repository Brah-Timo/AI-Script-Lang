import torch
import cv2
import numpy as np
from model import EmotionRecognitionModel
import torch.nn.functional as F  # لإجراء عمليات softmax

# تحديد الجهاز (CUDA إذا كان متاحًا، وإلا استخدام CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# تحميل النموذج المدرب
model = EmotionRecognitionModel().to(device)
model.load_state_dict(torch.load("emotion_model.pth", map_location=device))
model.eval()

# قائمة التصنيفات العاطفية (افتراضية، تحتاج إلى ضبطها بناءً على النموذج)
EMOTION_LABELS = ["Angry", "Disgust", "Fear", "Happy", "Neutral", "Sad", "Surprise"]

def preprocess_image(image_path):
    """
    تحميل الصورة وتحويلها إلى تنسيق مناسب للنموذج.
    """
    try:
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)  # تحميل الصورة بالألوان
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # تحويلها إلى تدرج رمادي
        image = cv2.resize(image, (48, 48))  # تغيير الحجم إلى المدخل المطلوب للنموذج
        image = image / 255.0  # تطبيع البيانات بين 0 و 1
        image = np.expand_dims(image, axis=0)  # إضافة بُعد للقنوات
        image = np.expand_dims(image, axis=0)  # إضافة بُعد إضافي للـ batch
        image_tensor = torch.tensor(image, dtype=torch.float32).to(device)  # تحويل إلى Tensor
        
        return image_tensor
    
    except Exception as e:
        print(f"❌ خطأ أثناء معالجة الصورة: {e}")
        return None

def detect_emotion(image_path):
    """
    تحليل المشاعر من صورة وجه.
    """
    image_tensor = preprocess_image(image_path)
    
    if image_tensor is None:
        return None  # في حالة حدوث خطأ أثناء المعالجة

    with torch.no_grad():
        emotion_logits = model(image_tensor)  # تشغيل النموذج
        probabilities = F.softmax(emotion_logits, dim=1)  # حساب الاحتمالات
        predicted_label = torch.argmax(probabilities).item()  # الحصول على التصنيف

    return EMOTION_LABELS[predicted_label]  # إرجاع اسم المشاعر

# ✅ تجربة تحليل المشاعر
if __name__ == "__main__":
    emotion = detect_emotion("face.jpg")
    if emotion:
        print(f"✅ Detected Emotion: {emotion}")
    else:
        print("❌ فشل تحليل المشاعر.")
