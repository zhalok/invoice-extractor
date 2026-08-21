FROM python:3.11-slim
WORKDIR /app
COPY accounting_api.py .
EXPOSE 8080
CMD ["python3", "accounting_api.py"]
