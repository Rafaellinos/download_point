FROM ubuntu:18.04

WORKDIR /usr/src/flask_app

RUN apt-get update \
        && apt-get install -y --no-install-recommends \
            sqlite3 \
            python3-pip \
            python3-wheel \
            python3-setuptools

COPY ./application/requirements.txt ./

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["/bin/bash"]