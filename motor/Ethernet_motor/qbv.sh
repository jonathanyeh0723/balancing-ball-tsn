#!/bin/bash

INTERFACE_NAME="enp2s0"
$SUDO iptables -t mangle -F

sleep 2
#Port 5000 - Best effort
$SUDO iptables -t mangle -A POSTROUTING -p udp --dport 5000 -j CLASSIFY --set-class 0:5
#Port 5010 - Control
$SUDO iptables -t mangle -A POSTROUTING -p udp --dport 5010 -j CLASSIFY --set-class 0:6
#$SUDO iptables -t mangle -A POSTROUTING -p udp --dport 5010 -j DSCP --set-dscp-class CS6
#Port 4840 - OPCUA UDP
$SUDO iptables -t mangle -A POSTROUTING -p udp --dport 4840 -j CLASSIFY --set-class 0:7

$SUDO tc qdisc del dev $INTERFACE_NAME parent root

tc qdisc add dev $INTERFACE_NAME parent root handle 100 taprio \
num_tc 4 \
map 3 3 3 3 3 1 2 0 3 3 3 3 3 3 3 3 \
queues 1@0 1@1 1@2 1@3 \
sched-entry S 01 50000 \
sched-entry S 02 100000 \
sched-entry S 04 50000 \
sched-entry S 08 50000 \
flags 0x2 \
txtime-delay 0

$SUDO tc qdisc show dev $INTERFACE_NAME
