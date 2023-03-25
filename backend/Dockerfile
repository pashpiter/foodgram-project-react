FROM python:3.7-slim

WORKDIR /app_back

COPY backend/requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]