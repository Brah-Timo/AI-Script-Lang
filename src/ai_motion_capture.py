import mediapipe as mp
import cv2
import json

# تحميل نموذج Mediapipe للكشف عن الحركة
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

def capture_motion(video_path):
    """
    يلتقط بيانات الحركة من فيديو أو كاميرا ويب باستخدام Mediapipe.
    """
    cap = cv2.VideoCapture(video_path)
    motion_data = []

    # التحقق من فتح الملف بنجاح
    if not cap.isOpened():
        print("❌ فشل في فتح الفيديو!")
        return None

    frame_count = 0
    fps = cap.get(cv2.CAP_PROP_FPS)  # الحصول على معدل الإطارات

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # تحويل الصورة إلى RGB لمعالجة Mediapipe
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)

        # استخراج نقاط الحركة إذا تم اكتشافها
        frame_data = {"frame": frame_count, "fps": fps, "landmarks": None}
        if results.pose_landmarks:
            frame_data["landmarks"] = [
                {"x": lm.x, "y": lm.y, "z": lm.z} for lm in results.pose_landmarks.landmark
            ]

        motion_data.append(frame_data)
        frame_count += 1

        # عرض الفيديو أثناء المعالجة (اختياري)
        cv2.imshow("Motion Capture", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()  # إغلاق نافذة العرض

    # حفظ بيانات الحركة إلى ملف JSON
    with open("motion_data.json", "w") as f:
        json.dump(motion_data, f, indent=4)

    return motion_data

# ✅ تجربة التقاط الحركة
if __name__ == "__main__":
    video_source = "person_running.mp4"  # يمكن استبداله بـ 0 لاستخدام كاميرا الويب
    motion = capture_motion(video_source)

    if motion:
        print(f"✅ تم استخراج {len(motion)} إطارًا بنجاح!")
    else:
        print("❌ لم يتم التقاط أي حركة.")
