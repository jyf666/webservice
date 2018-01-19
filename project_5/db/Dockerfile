FROM python:3.6.3
MAINTAINER jyf-17126168
ADD . /sqlite
WORKDIR /sqlite
RUN pip install -r requirements.txt
EXPOSE 3000
CMD python SQLite_server.py