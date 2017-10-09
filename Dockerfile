
FROM alpine:3.1

WORKDIR /root

# Install and Update
RUN apk add --update bash python py-pip

# Install app dependencies
RUN pip2 install ccxt --src /usr/local/src

# Bundle app source
COPY arbitrage.sh /root
COPY database.py /root
COPY get_price_info.py /root
