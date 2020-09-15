docker run --rm -d \
       --name wiot-speedtest \
       -v /home/pi/Code/HomeIoT:/home \
       -w /home \
       dhudsmith/wiot_home:speedtest \
       python apps/speedtest/main.py --cfg=creds/config.yml

