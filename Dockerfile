FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /webapp
WORKDIR /webapp
ADD requirements.txt /webapp/
RUN pip install --upgrade pip && pip install -r requirements.txt
ADD . /webapp/
