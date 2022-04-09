FROM python:3.9-bullseye
WORKDIR /app
ADD requirements.txt .
RUN python -m pip install -r requirements.txt
COPY streamlit.py /app
EXPOSE 8501
ENTRYPOINT [ "streamlit", "run", "--server.headless", "true" ]
CMD ["streamlit.py"]
