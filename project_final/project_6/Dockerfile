FROM python:3.6.3
MAINTAINER jyf-17126168
ADD /web_code /web_code
WORKDIR /web_code
RUN pip install -r requirements.txt
EXPOSE 8002
CMD python web.py