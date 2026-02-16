# 🏥 HỆ THỐNG HỖ TRỢ CHẨN ĐOÁN Y KHOA

![Python](https://img.shields.io/badge/Python-3.9-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)
![Algorithm](https://img.shields.io/badge/AI-Random_Forest-orange.svg)
![Status](https://img.shields.io/badge/Status-Completed-success.svg)

> **Đồ án 2** - Xây dựng hệ thống dự báo sớm bệnh tiểu đường dựa trên các chỉ số lâm sàng và Machine Learning.

---

## 📖 Giới thiệu

**HỆ THỐNG HỖ TRỢ CHẨN ĐOÁN Y KHOA** là một nền tảng Web Application tích hợp Trí tuệ nhân tạo (AI) nhằm hỗ trợ bác sĩ và người dùng phổ thông trong việc tầm soát sớm nguy cơ mắc bệnh Tiểu đường (Diabetes).

Hệ thống sử dụng thuật toán học máy **Random Forest Classifier**, được huấn luyện trên bộ dữ liệu chuẩn y khoa với hơn 100.000 bản ghi, đảm bảo độ chính xác cao và khả năng xử lý thời gian thực.

### 🎯 Mục tiêu
* Tự động hóa quy trình chẩn đoán sơ bộ.
* Giảm tải áp lực cho đội ngũ y tế.
* Cung cấp giao diện trực quan, dễ sử dụng cho bệnh nhân.

---

## 🚀 Tính năng nổi bật

* **⚡ Chẩn đoán tức thì:** Trả về kết quả phân tích rủi ro chỉ trong < 0.5 giây.
* **📊 Trực quan hóa dữ liệu:** Hiển thị mức độ nguy cơ bằng biểu đồ Doughnut (Chart.js) và các chỉ số phần trăm cụ thể.
* **🛡️ Bảo mật cao:** Dữ liệu bệnh nhân được xử lý cục bộ thông qua Docker Container, không lưu trữ trên Cloud công cộng.
* **📱 Giao diện Responsive:** Tương thích hoàn hảo trên cả máy tính và thiết bị di động.
* **🖨️ Xuất hồ sơ:** Tính năng in phiếu kết quả chẩn đoán trực tiếp từ trình duyệt.

---

## 🛠️ Công nghệ sử dụng

### 1. Artificial Intelligence (AI Core)
* **Ngôn ngữ:** Python 3.9
* **Thư viện:** Scikit-learn, Pandas, NumPy, Joblib.
* **Thuật toán:** Random Forest Classifier (Rừng ngẫu nhiên).
* **Kỹ thuật xử lý:**
    * SMOTE (Synthetic Minority Over-sampling Technique) để cân bằng dữ liệu.
    * StandardScaler để chuẩn hóa dữ liệu đầu vào.

### 2. Backend (API Service)
* **Framework:** Flask (Python Microframework).
* **Server:** Gunicorn (WSGI Server).
* **Port:** 5000 (Internal).

### 3. Frontend (User Interface)
* **Ngôn ngữ:** HTML5, CSS3, JavaScript (ES6).
* **Framework:** Bootstrap 5 (Giao diện), Chart.js (Biểu đồ).
* **Server:** Nginx (Web Server & Reverse Proxy).

### 4. DevOps & Deployment
* **Containerization:** Docker & Docker Compose.
* **Architecture:** Microservices (Tách biệt Frontend và Backend).

---

## ⚙️ Cài đặt và Vận hành

Để chạy hệ thống, bạn cần cài đặt **Docker** và **Docker Desktop** trên máy tính.

### Bước 1: Clone dự án
Tải mã nguồn về máy tính của bạn:
```bash
git clone [https://github.com/username/diabetes-prediction-system.git](https://github.com/username/diabetes-prediction-system.git)
cd diabetes-prediction-system

```

### Bước 2: Khởi chạy với Docker Compose

Mở Terminal tại thư mục gốc của dự án và chạy lệnh:

```bash
docker compose up --build

```

*Lệnh này sẽ tự động tải các thư viện cần thiết, huấn luyện model (nếu chưa có), và khởi động cả 2 container Backend và Frontend.*

### Bước 3: Truy cập hệ thống

Mở trình duyệt web và truy cập địa chỉ:
👉 **http://localhost:8081**

---

## 📂 Cấu trúc dự án

```
DIABETES-PREDICTION-SYSTEM/
├── backend/                # Source code Backend (Python/Flask)
│   ├── model/              # Chứa file model.pkl đã train
│   ├── app.py              # API Endpoint chính
│   ├── train_model.py      # Script huấn luyện AI
│   └── Dockerfile          # Cấu hình Docker cho Backend
│
├── frontend/               # Source code Frontend (HTML/CSS/JS)
│   ├── index.html          # Trang chủ
│   ├── diagnosis.html      # Trang chẩn đoán (Dashboard)
│   ├── models.html         # Trang danh mục mô hình
│   ├── news.html           # Trang tin tức
│   └── Dockerfile          # Cấu hình Docker cho Nginx
│
├── nginx/
│   └── default.conf        # Cấu hình Reverse Proxy cho Nginx
│
├── dataset/                # Thư mục chứa dữ liệu CSV
├── docker-compose.yml      # File cấu hình chạy toàn bộ hệ thống
└── README.md               # Tài liệu hướng dẫn

```

---

## 🧬 Mô tả dữ liệu đầu vào (Input)

Hệ thống yêu cầu 8 chỉ số sinh tồn quan trọng để thực hiện chẩn đoán:

1. **Giới tính (Gender):** Nam/Nữ.
2. **Tuổi (Age):** Tuổi của bệnh nhân.
3. **Cao huyết áp (Hypertension):** Có tiền sử bệnh hay không.
4. **Bệnh tim mạch (Heart Disease):** Có tiền sử bệnh hay không.
5. **Lịch sử hút thuốc (Smoking History):** Chưa bao giờ / Đã cai / Đang hút.
6. **BMI (Body Mass Index):** Chỉ số khối cơ thể.
7. **HbA1c Level:** Chỉ số đường huyết trung bình trong 3 tháng.
8. **Blood Glucose Level:** Chỉ số đường huyết đo lúc đói.

---

## 👨‍💻 Tác giả

**DuyNguyenTech**

* **Vai trò:** Fullstack Developer & AI Engineer.
* **Liên hệ:** [Email của bạn]
* **Đồ án:** Kỹ thuật Phần mềm 2026.

---

*© 2026 MED-AI System. All rights reserved.*