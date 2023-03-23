FROM python:3.7-slim

WORKDIR /app_back

COPY backend/foodgram/requirements.txt .

RUN pip install -r requirements.txt

COPY backend/foodgram .

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]