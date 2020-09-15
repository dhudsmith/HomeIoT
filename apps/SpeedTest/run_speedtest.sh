docker run --rm -i -t \
       --name rpi-speedtest \
       -v /home/pi/Code/SpeedMonitor/source:/home \
       -w /home \
       dhudsmith/wiot_speedtest:rpi \
       python checkspeed.py --cfg=config.yml

