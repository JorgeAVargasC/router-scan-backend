FROM python:3-alpine3.15

WORKDIR /app

COPY . /app

RUN apk update && apk add --no-cache gcc musl-dev && apk add libxml2-dev libxslt-dev
RUN apk add --no-cache build-base linux-headers
RUN apk add --no-cache nmap
RUN pip install -r requirements.txt

EXPOSE 5000

CMD gunicorn app:app --bind 0.0.0.0:5000