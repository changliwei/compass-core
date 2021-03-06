#!/bin/bash -x
# create a bridge named 'installation' so that compass and pxeboot vm are in the
# same l2 network.
brctl show |grep installation > /dev/null
if [[ $? -eq 0 ]] ; then
    echo "bridge already exists"
else
    brctl addbr installation
    brctl addif installation eth1
    ifconfig eth1 up
    dhclient -r eth1
    dhclient -r installation
    dhclient installation
fi
source compass-core/install/install.conf.template
/bin/bash -x compass-core/install/install.sh
sleep 5
