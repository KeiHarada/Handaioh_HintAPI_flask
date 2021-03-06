FROM ubuntu:latest

RUN apt-get update
RUN apt-get install python3 python3-pip -y
RUN pip3 install flask
RUN pip3 install neo4jrestclient
RUN pip3 install -U flask-cors

RUN mkdir /app
WORKDIR /app
EXPOSE 8080
COPY docker-entrypoint.sh /
RUN chmod 755 /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]

