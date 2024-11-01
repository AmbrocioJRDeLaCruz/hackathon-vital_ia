# Stage 1
FROM python:3.9-slim AS builder

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install  -r requirements.txt

# Stage 2
FROM python:3.9-slim

WORKDIR /app

COPY . /app

ENV ACCEPT_EULA=Y
RUN apt-get update -y && apt-get update \
  && apt-get install -y --no-install-recommends curl gcc g++ gnupg unixodbc-dev

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
  && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
  && apt-get update \
  && apt-get install -y --no-install-recommends --allow-unauthenticated msodbcsql17 mssql-tools \
  && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile \
  && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc

COPY --from=builder /install /usr/local

EXPOSE ${FLASK_PORT}

ENV FLASK_APP=app.py

CMD ["python", "app.py"]