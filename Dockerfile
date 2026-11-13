FROM python:3
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
#sem o serve.port e serve.adress nao abre no navegador...
CMD ["python", "-m", "streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
