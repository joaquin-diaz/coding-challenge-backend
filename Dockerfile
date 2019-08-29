FROM python:3.7
RUN mkdir /code
WORKDIR /code
COPY . /code/
EXPOSE 8000