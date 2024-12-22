#syntax=docker/dockerfile:1
FROM alpine:3.18

RUN apk add --update --no-cache gcc \
    g++ \
    make \
    libevent libevent-dev \
    zlib zlib-dev \
    openssl openssl-dev \
    wget

RUN mkdir /build

WORKDIR /build

RUN wget -O tor.tar.gz https://dist.torproject.org/tor-0.4.8.3-rc.tar.gz && \
    tar xzf tor.tar.gz 

WORKDIR /build/tor-0.4.8.3-rc

RUN ./configure && make install

WORKDIR /

COPY ./config.conf /usr/local/etc/tor/torrc

ENTRYPOINT ["tor"]
