FROM python:3.8

WORKDIR  /aap

COPY . ./

RUN pip install -r requirements.txt

ADD kaggle.json  /root/.kaggle/kaggle.json

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]


