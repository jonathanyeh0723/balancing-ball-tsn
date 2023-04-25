#!/bin/bash

sudo killall -9 pubsub_TSN_loopback
sudo killall -9 pubsub_TSN_loopback_single_thread
sleep 1
sudo taskset -c 1,2,3 /root/motor/open62541/pubsub_TSN_loopback_single_thread -interface 192.168.137.1 -enableBlockingSocket -pubUri opc.udp://192.168.137.2:4840 -cycleTimeInMsec 0.25

