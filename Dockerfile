FROM python:3.9-alpine
RUN mkdir /app && adduser -SH dns
ADD . /app
WORKDIR /app
USER dns
CMD ["python", "dns.py"]