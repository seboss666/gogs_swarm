FROM frolvlad/alpine-python3

WORKDIR /usr/src/app
RUN apk update
RUN apk add docker
RUN pip install --no-cache-dir ovh

COPY . .

CMD [ "python", "./update_gogs_dns.py" ]
