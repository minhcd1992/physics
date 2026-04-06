import google.generativeai as genai

# THAY API KEY CỦA BẠN VÀO GIỮA 2 DẤU NGOẶC KÉP DƯỚI ĐÂY
API_KEY = "AIzaSy..." 

genai.configure(api_key=API_KEY)

print("Đang truy vấn danh sách model từ Google...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
    print("Hoàn tất!")
except Exception as e:
    print(f"Lỗi truy vấn: {e}")
