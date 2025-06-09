# 1. استفاده از image پایه پایتون
FROM python:3.11-slim

# 2. تنظیم working directory
WORKDIR /app

# 3. کپی کردن فایل requirements و نصب
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. کپی کردن کل پروژه داخل کانتینر
COPY . .

# 5. اجرای collectstatic (اختیاری، اگه static داری)
RUN python manage.py collectstatic --noinput || true

# 6. فرمان پیش‌فرض برای اجرای سرور
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
