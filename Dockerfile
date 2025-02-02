# استخدم Python كأساس
FROM python:3.9-slim

# تثبيت المتطلبات الأساسية
RUN apt update && apt install -y git p7zip-full

# استنساخ المستودع من GitHub
RUN git clone https://github.com/odbrg6/olga.git /root/sbb_b

# تعيين المجلد الافتراضي
WORKDIR /root/sbb_b

# تثبيت المتطلبات
RUN pip3 install --no-cache-dir -r requirements.txt

# ضبط مسار البيئة
ENV PATH="/root/sbb_b/bin:$PATH"

# تشغيل البوت
CMD ["python3", "-m", "sbb_b"]
