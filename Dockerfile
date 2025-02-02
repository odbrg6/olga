FROM python:3.9-slim
RUN apt update && apt install -y \
    git p7zip-full gcc g++ make libffi-dev libssl-dev \
    python3-dev libxml2-dev libxslt-dev zlib1g-dev libjpeg-dev \
    curl ffmpeg wget chromium chromium-driver
ENV PATH="/usr/lib/chromium/:$PATH"
RUN git clone https://github.com/odbrg6/olga.git /root/sbb_b
WORKDIR /root/sbb_b
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt
ENV PATH="/root/sbb_b/bin:$PATH"
CMD ["python3", "-m", "sbb_b"]
