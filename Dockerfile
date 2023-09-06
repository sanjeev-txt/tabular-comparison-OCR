FROM python:3.8
WORKDIR /practicedoker
COPY . $WORKDIR
RUN pip install -r requirements.txt
