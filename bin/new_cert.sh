#!/bin/sh

openssl req -nodes -new -x509 -keyout key.pem -out cert.pem -days 365
