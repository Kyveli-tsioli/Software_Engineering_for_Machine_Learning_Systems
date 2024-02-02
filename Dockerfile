FROM ubuntu:jammy
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -yq install python3-pip
COPY model/requirements.txt /model/
RUN pip3 install -r /model/requirements.txt
COPY model/model.py /model/
COPY model/preprocess_data.py /model/
COPY model/train.py /model/
COPY model/trained_model.sav /model/
CMD /model/model.py --input=/data/test.csv --output=/data/aki.csv