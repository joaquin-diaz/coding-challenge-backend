FROM python:3.7
RUN mkdir /code
WORKDIR /code
COPY . /code/
CMD python ./app/dev_server.py
