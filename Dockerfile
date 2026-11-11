FROM Python:3
WORKDIR /app
COPY requirements.text
RUN pip install --no-cache-dir -r requirements.text
COPY ..
EXPOSE 8501
CMD ["streamlit", "run", "main.py"]
