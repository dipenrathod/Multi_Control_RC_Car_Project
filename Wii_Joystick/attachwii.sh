#!/bin/bash
hcitool dev | grep hci >/dev/null
if test $? -eq 0 ; then
    wminput -d -c  /home/pi/wii_rpi/mywminput 00:1E:A9:67:2E:C4 &
else
    echo "Blue-tooth adapter not present!"
    exit 1
fi

ttl=30
alert="/home/pi/complete.oga"
fail="/home/pi/bark.oga"
begin_sound="/home/pi/robot-blip.wav"
end_sound="/home/pi/service-logout.oga"
mac="\([[:xdigit:]]\{2\}:\)\{5\}[[:xdigit:]]" # "00:" * 5 + "00"
device_file="/tmp/wiimote-scan"

function play {
    ogg123 $1 &> /dev/null &
}

function match {
    echo $1 | grep $2
}

function show {
    if [[ -n $DEBUG ]]
    then
        echo $1
    fi
}

# prevent scans from interfering with one another?
killall hcitool && sleep 5

if [[ `hcitool dev | grep hci` ]]
then
    aplay $begin_sound &> /dev/null &
    echo "Bluetooth detected, starting scan with ${ttl}s timeout..."

    timeout $ttl hcitool scan | while read device
    do
        show "found $device"

        if [[ `match "$device" "Nintendo"` ]]
        then
            show "matched Nintendo in $device"

            id=`echo $device | cut -d" " -f1`

            if [[ `match $id $mac` && \
                "$id"!="00:1E:A9:67:2E:C4" ]]
            then
                show "matched MAC in $id"

                echo -n "Detected Wiimote with ID: ${id}..."
                wminput -d -c /home/pi/mywminput $id &
                echo " registered."
                play $alert
            fi
        fi
    done

    play $end_sound
    echo "Scan complete."

    if [[ "$rebootWithoutWiimotes" == "1" && -z `pidof wminput` ]]
    then
        echo "No Wiimotes detected!  Restarting..."
        sudo reboot
    fi
else
    echo "Blue-tooth adapter not present!"
    play $fail
fi
