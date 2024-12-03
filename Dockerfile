# Stage 1: Build the application
FROM python:3.9-slim as builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Stage 2: Create the final image
FROM python:3.9-slim

WORKDIR /app

COPY --from=builder /app /app

EXPOSE 5001

CMD ["python", "app.py"]