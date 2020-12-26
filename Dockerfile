FROM python:3.8.5

EXPOSE 5000

WORKDIR /app
COPY . /app

RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com/pypi/simple -r requirements.txt

CMD ["python", "app.py"]