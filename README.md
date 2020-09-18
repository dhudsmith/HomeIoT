# HomeIoT
Having fun with Raspberry Pis and Watson IoT at home

The `apps/` folder contains different sample python applications for home monitoring tools. Each app has the following: 
* `Dockerfile`: the dockerfile used to build the docker app runtime
* `build_docker.sh`: a convenience script for building the docker image
* `main.py`: the main script that performs the monitoring service and logs results with Watson IoT
* `start.sh`/`stop.sh`: convenience scripts for starting and stopping the application

At the top level, `start_all.sh` and `stop_all.sh` are conveince scripts which call the start or stop scripts for each app. 

The `creds/` folder contains the credentials needed to run the applications. 
Add your own credentials files named by removing the `_template` suffix from the examples listed. 
