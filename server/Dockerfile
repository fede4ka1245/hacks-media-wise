# Use a base Python image
FROM python:3.11
WORKDIR /app
ARG BACKEND_URL

COPY . .
RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "main.py" ]