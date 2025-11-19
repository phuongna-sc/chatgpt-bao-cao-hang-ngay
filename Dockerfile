# Base image chính thức của Python
FROM python:3.12-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy mã nguồn và file dependency
COPY . .

# Cài đặt các gói cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Cài đặt Functions Framework (nếu chưa có trong requirements.txt)
RUN pip install functions-framework

# Đặt biến môi trường PORT (Cloud Run yêu cầu cổng 8080)
ENV PORT=8080

# Chạy ứng dụng Flask qua Functions Framework
CMD ["functions-framework", "--target=app", "--port=8080"]
