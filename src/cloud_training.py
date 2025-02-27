import torch
import requests

# عنوان خادم التدريب السحابي
CLOUD_SERVER = "https://ai-cloud-training.com/api/train"
CHECK_STATUS_ENDPOINT = "https://ai-cloud-training.com/api/status"

# مفتاح المصادقة (في حال كان مطلوبًا)
API_KEY = "your_api_key_here"

def train_model_on_cloud(model_path, dataset_path):
    """رفع نموذج وبيانات إلى السحابة لبدء التدريب"""
    headers = {"Authorization": f"Bearer {API_KEY}"}

    try:
        with open(model_path, "rb") as model_file, open(dataset_path, "rb") as dataset_file:
            files = {"model": model_file, "dataset": dataset_file}
            response = requests.post(CLOUD_SERVER, files=files, headers=headers)
        
        # التحقق من نجاح الطلب
        if response.status_code == 200:
            return response.json()  # إرجاع معلومات التدريب (مثل job_id)
        else:
            return {"error": f"Failed to start training: {response.text}"}
    
    except Exception as e:
        return {"error": f"Exception occurred: {str(e)}"}

def check_training_status(job_id):
    """التحقق من حالة التدريب باستخدام job_id"""
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(f"{CHECK_STATUS_ENDPOINT}/{job_id}", headers=headers)

    if response.status_code == 200:
        return response.json()  # إرجاع الحالة الحالية للتدريب
    else:
        return {"error": f"Failed to check status: {response.text}"}

# تجربة تدريب نموذج على السحابة
if __name__ == "__main__":
    training_response = train_model_on_cloud("ai_model.pth", "dataset.zip")

    if "job_id" in training_response:
        job_id = training_response["job_id"]
        print(f"Training started! Job ID: {job_id}")

        # تتبع الحالة بعد فترة قصيرة
        import time
        time.sleep(10)
        status = check_training_status(job_id)
        print(f"Training Status: {status}")
    else:
        print(f"Error: {training_response}")

