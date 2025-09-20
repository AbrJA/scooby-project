FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#ENV FILE_IMAGES=https://drive.google.com/uc?id=16VNhbfSuaujdFOc_Le03fUMkE3PxBwg4
#ENV MODEL_NAME=unum-cloud/uform3-image-text-english-small

COPY main.py .

CMD ["python", "main.py"]
