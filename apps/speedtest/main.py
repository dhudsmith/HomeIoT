#!/usr/bin/env python

# *****************************************************************************
# Copyright (c) 2014, 2019 IBM Corporation and other Contributors.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v1.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v10.html
# *****************************************************************************

import argparse
import time
import sys
import platform
import json
import signal
from uuid import getnode as get_mac
import wiotp.sdk.device
import speedtest

def interruptHandler(signal, frame):
    client.disconnect()
    sys.exit(0)

def commandProcessor(cmd):
    global interval
    print("Command received: %s" % cmd.data)
    if cmd.commandId == "setInterval":
        if "interval" not in cmd.data:
            print("Error - command is missing required information: 'interval'")
        else:
            try:
                interval = int(cmd.data["interval"])
            except ValueError:
                print("Error - interval not an integer: ", cmd.data["interval"])
    elif cmd.commandId == "print":
        if "message" not in cmd.data:
            print("Error - command is missing required information: 'message'")
        else:
            print(cmd.data["message"])

if __name__ == "__main__":
    signal.signal(signal.SIGINT, interruptHandler)

    # Seconds to sleep between readings
    interval = 900

    # Initialize the properties we need
    parser = argparse.ArgumentParser(
        description="Utility for periodically checking internet speed",
        epilog="If neither the quickstart or cfg parameter is provided the device will attempt to parse the configuration from environment variables.",
    )
    parser.add_argument(
        "-n", "--name", required=False, default=platform.node(), help="Defaults to platform.node() if not set"
    )
    parser.add_argument("-q", "--quickstart", required=False, action="store_true", help="Connect device to quickstart?")
    parser.add_argument(
        "-c",
        "--cfg",
        required=False,
        default=None,
        help="Location of device configuration file (ignored if quickstart mode is enabled)",
    )
    parser.add_argument("-v", "--verbose", required=False, action="store_true", help="Enable verbose log messages?")
    args, unknown = parser.parse_known_args()

    client = None
    try:
        if args.quickstart:
            options = {
                "identity": {
                    "orgId": "quickstart",
                    "typeId": "sample-iotpsutil",
                    "deviceId": str(hex(int(get_mac())))[2:],
                }
            }
        elif args.cfg is not None:
            options = wiotp.sdk.device.parseConfigFile(args.cfg)
        else:
            options = wiotp.sdk.device.parseEnvVars()

        client = wiotp.sdk.device.DeviceClient(options)
        client.commandCallback = commandProcessor
        client.connect()
    except Exception as e:
        print(str(e))
        sys.exit(1)

    if args.quickstart:
        print(
            "Welcome to IBM Watson IoT Platform Quickstart, view a vizualization of live data from this device at the URL below:"
        )
        print(
            "https://quickstart.internetofthings.ibmcloud.com/#/device/%s/sensor/" % (options["identity"]["deviceId"])
        )

    print("(Press Ctrl+C to disconnect)")

    # servers for speedtest
    servers=[]
    threads = None
    s = speedtest.Speedtest()

    while True:
        time.sleep(interval)

        s.get_servers(servers)
        s.get_best_server()
        s.download(threads=threads)
        s.upload(threads=threads)
        s.results.share()

        results_dict = s.results.dict()

        if args.verbose:
            print("Datapoint = " + json.dumps(results_dict))

        client.publishEvent("speedtest", "json", results_dict)

        # Update timestamp and data ready for next loop
        
