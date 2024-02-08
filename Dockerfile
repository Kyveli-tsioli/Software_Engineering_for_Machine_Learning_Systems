FROM ubuntu:jammy
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -yq install python3-pip
COPY model/requirements.txt /model/
RUN pip3 install -r /model/requirements.txt

COPY model/model.py /model/
COPY model/preprocess_data.py /model/
COPY model/train.py /model/
COPY model/trained_model.sav /model/

COPY client.py /simulator/
COPY simulator.py /simulator/
COPY simulator_test.py /simulator/

WORKDIR /simulator
# RUN ./simulator_test.py
COPY messages.mllp /data/
EXPOSE 8440
EXPOSE 8441
# CMD /simulator/simulator.py --messages=/data/messages.mllp
# ENV MLLP_ADDRESS="0.0.0.0:8440"
# ENV PAGER_ADDRESS="0.0.0.0:8441"
CMD chmod +x /simulator/client.py
# access port that they sent over
# CMD /model/model.py --input=/data/test.csv --output=/data/aki.csv