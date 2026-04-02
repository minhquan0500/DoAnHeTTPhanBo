# Sử dụng môi trường Python siêu nhẹ
FROM python:3.9-slim

# Tạo thư mục làm việc bên trong container
WORKDIR /app

# Copy file requirements.txt vào trước để cài thư viện
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code vào trong container
COPY main.py .

# Cài đặt biến môi trường mặc định (có thể ghi đè sau)
ENV SERVER_NAME=backend-docker

# Lệnh khởi chạy server khi container bật lên
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]