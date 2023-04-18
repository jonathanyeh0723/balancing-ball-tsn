IF_1=enp4s0
IF_2=enp2s0
IF_3=eno1
tc qdisc show dev $IF_1
ip link add link $IF_1 name $IF_1.8 type vlan id 8 egress-qos-map 5:5 6:6 7:7
ip link add link $IF_2 name $IF_2.8 type vlan id 8 egress-qos-map 5:5 6:6 7:7
ifconfig $IF_2 0.0.0.0 
ifconfig $IF_2.8 0.0.0.0 
ifconfig $IF_1 0.0.0.0 
ifconfig $IF_1.8 0.0.0.0  
ip link add name br0 type bridge
ip link set dev br0 up
ip link set dev $IF_2.8 master br0
ip link set dev $IF_2 master br0
ip link set dev $IF_1 master br0
ip link set dev $IF_3 master br0
ifconfig br0 192.168.137.1

iptables -A FORWARD -j ACCEPT
