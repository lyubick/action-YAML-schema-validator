FROM python:3.11-slim

WORKDIR /

ADD requirements.txt /
ADD validator.py /

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "/validator.py"]
