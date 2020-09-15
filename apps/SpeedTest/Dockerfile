FROM python:3.8-alpine3.11

# Add the required dependencies to install psutil that are missing from alpine
# See: https://github.com/giampaolo/psutil/issues/872#issuecomment-272248943
RUN apk add gcc linux-headers libc-dev

# Install dependencies
RUN pip install wiotp-sdk==0.10.0 speedtest-cli==2.1.2
