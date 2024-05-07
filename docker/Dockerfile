FROM ubuntu:23.10

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /setup

COPY scripts/1_prerequs.sh 1_prerequs.sh
RUN chmod +x 1_prerequs.sh
RUN ./1_prerequs.sh

COPY scripts/install_opencilk.sh install_opencilk.sh
RUN chmod +x install_opencilk.sh
RUN ./install_opencilk.sh

WORKDIR /

ENV DEBIAN_FRONTEND=
