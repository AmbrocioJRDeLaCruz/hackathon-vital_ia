# Stage 1
FROM python:3.9-slim AS builder

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install  -r requirements.txt

# Stage 2
FROM python:3.9-slim

WORKDIR /app

COPY . /app

COPY --from=builder /install /usr/local

EXPOSE ${STREAMLIT_PORT}

CMD ["python", "start_streamlit.py"]