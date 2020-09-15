docker run --rm -d \
       --name wiot-psutil \
       -v /home/pi/Code/HomeIoT:/home \
       -w /home \
       dhudsmith/wiot_home:psutil \
       python apps/psutil/main.py --cfg=creds/config.yml

