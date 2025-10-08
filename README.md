# 🥗 Project_AI_Nutrition_Coach  

Ứng dụng **AI Nutrition Coach** giúp phân tích **thành phần dinh dưỡng** và **lượng calories** từ hình ảnh món ăn.  
Project này sử dụng **Flask** để xây dựng web app và **Google GenAI API** để phân tích hình ảnh & văn bản.  

---

## 🚀 Tính năng
- Upload ảnh món ăn để phân tích.  
- Đặt câu hỏi liên quan đến dinh dưỡng (ví dụ: *How many calories are in this food?*).  
- Nhận phản hồi chi tiết từ AI (calories, thành phần, breakdown dinh dưỡng).  
- Giao diện web thân thiện, có CSS tùy chỉnh.  

---

## 📂 Cấu trúc thư mục
```
Project_AI_Nutrition_Coach/
│
├── app.py # Flask 
├── README.md # Tài liệu dự án
│
├── templates/
│ └── index.html # Giao diện web chính
│
├── static/
│ └── style.css # File CSS cho giao diện
│
└── image/
└── Garlic-Herbed-Grilled-Tuna-Steak.png # Ảnh mẫu
```
## ⚙️ Cài đặt & Chạy

### 1️⃣ Clone repo
```bash
git clone https://github.com/SimpleAI04/Project_AI_Nutrition_Coach.git
cd Project_AI_Nutrition_Coach
```
### 2️⃣ Tạo môi trường ảo & cài đặt dependencies
```bash
python -m venv venv
source venv/bin/activate   # trên Linux/Mac
venv\Scripts\activate      # trên Windows
pip install -r requirements.txt
```
### 3️⃣ Cấu hình API key
```bash
GOOGLE_API_KEY=your_api_key_here
```
### 4️⃣ Chạy ứng dụng
```bash
python app.py
```
- Truy cập ứng dụng tại: 👉 http://127.0.0.1:5000

### 🛠️ Công nghệ sử dụng
- Flask – Web framework Python.
- Google GenAI – API AI phân tích hình ảnh & văn bản.
- dotenv – Quản lý biến môi trường.
- Pillow – Xử lý ảnh.
