# Sử dụng đúng phiên bản Python đã ghi trong báo cáo
FROM python:3.10-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy và cài đặt thư viện
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ thư mục backend vào
COPY . .

# Mở cổng giao tiếp
EXPOSE 5000

# Chạy bằng Gunicorn để chịu tải tốt hơn (chuẩn thực tế)
# Lưu ý: Cần thêm gunicorn vào file requirements.txt
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000"]