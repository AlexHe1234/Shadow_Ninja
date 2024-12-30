FROM jess/chrome:latest

USER root

RUN mkdir -p /var/lib/apt/lists/partial && chmod -R 777 /var/lib/apt/lists/

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    vim \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python

RUN python --version && pip --version

WORKDIR /app

WORKDIR /app

COPY . /app
RUN chmod -R 777 /app

RUN pip install -r requirements.txt

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
    ttf-wqy-zenhei \
    ttf-wqy-microhei \
    fonts-arphic-ukai \
    fonts-arphic-uming \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


RUN useradd -m chromeuser
USER chromeuser

CMD ["python", "app.py"]
