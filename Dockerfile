FROM python:3-alpine3.15

WORKDIR /app

COPY . /app

RUN apk update && apk add --no-cache gcc musl-dev && apk add libxml2-dev libxslt-dev
RUN apk add --no-cache build-base linux-headers

# git
RUN apk add --no-cache git

# Nmap
RUN apk add --no-cache nmap

# Nmap scripts
RUN apk add --no-cache nmap-scripts

# Clone vulners script for Nmap
RUN mkdir -p /usr/share/nmap/scripts \
    && cd /usr/share/nmap/scripts \
    && git clone https://github.com/vulnersCom/nmap-vulners.git

RUN pip install -r requirements.txt

EXPOSE 5000

CMD gunicorn app:app --bind 0.0.0.0:5000 --timeout 300