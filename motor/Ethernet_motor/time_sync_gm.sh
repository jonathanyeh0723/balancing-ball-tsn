killall -9 phc2sys
killall -9 ptp4l
INF=enp2s0
taskset -c 1 ptp4l -i $INF -A -2 -m -f gPTP.cfg
taskset -c 1 phc2sys -s CLOCK_REALTIME -c $INF -O 0 -w -m -f gPTP.cfg
