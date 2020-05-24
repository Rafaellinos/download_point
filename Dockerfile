FROM ubuntu:18.04

WORKDIR /usr/src/flask_app

RUN apt update \
        && apt install -y --no-install-recommends \
            python3-pip

COPY ./application ./

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["/bin/bash"]