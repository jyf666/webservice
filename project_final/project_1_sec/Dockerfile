FROM python:3.6.3
MAINTAINER jyf-17126168
ADD . /ram_code2
WORKDIR /ram_code2
RUN pip install -r requirements.txt
EXPOSE 8001
CMD python system_service.py