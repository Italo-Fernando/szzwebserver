FROM python:3.10-slim-bullseye

WORKDIR /app

RUN apt update && apt upgrade -y --no-install-recommends && \
    apt install -y --no-install-recommends wget libarchive13 libcurl4 libxml2 && \
    apt install -y --no-install-recommends git

RUN wget http://131.123.42.38/lmcrs/v1.0.0/srcml_1.0.0-1_ubuntu20.04.deb && \
    dpkg -i srcml_1.0.0-1_ubuntu20.04.deb

COPY ./requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

COPY ./pyszz_v2 ./pyszz_v2
RUN pip3 install --editable pyszz_v2/

COPY config/ szz_runner.py szz_selector.py ./

CMD [ "python3", "szz_runner.py"]