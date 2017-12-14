FROM frolvlad/alpine-python3

WORKDIR /usr/src/app
#RUN apk add -U --no-cache docker &&\
#	pip install --no-cache-dir ovh
RUN pip install --no-cache-dir ovh docker
COPY . .

CMD [ "python", "./update_gogs_dns.py" ]