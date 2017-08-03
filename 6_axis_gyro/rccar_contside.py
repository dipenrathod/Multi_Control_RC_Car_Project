import socket
import time
import sys
import re
#sys.path.append("./acgy.py")
import accgyro

s = None
pipe = None

RESEND_TIME = 0.1 # sec

def main():
    if len(sys.argv) > 1:
        host = ipcheck(sys.argv[1])
    else:
        host = '127.0.0.1'

    port = 10000

    floatYaw = 0.0
    floatPitch = 0.0
    floatRoll = 0.0

    global s
    global pipe

    while True:
        try:
            print 'Try Socket Open'
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            s.connect((host,port))
            print 'connection End'
            sys.stdout.write('%')
        except socket.error:
            print 'socket connection error'
            s.close()
            time.sleep(2)
            continue

        #finally:
        #    # Clean up the connection
        #    s.close()

        acgy = accgyro.ACCGYRO()

        timeCnt = 0
        while True:
            acgy.runFloatYPR()
            floatYaw = acgy.getFloatYaw()
            if (floatYaw==None):
                continue
            floatPitch = acgy.getFloatPitch()
            floatRoll = acgy.getFloatRoll()

            if ( timeCnt == (RESEND_TIME*400)):
                print str( floatYaw ) + ' /  ' + str( floatPitch ) + ' / ' + str( floatRoll )

                rtc = data_send(floatYaw, floatPitch, floatRoll)

                if rtc < 0:
                    break

                timeCnt = 0
            timeCnt = timeCnt + 1

def data_send(dataYaw, dataPitch, dataRoll):
    strPitch = "%6.3f" % dataPitch
    strRoll = "%6.3f" % dataRoll
    send_data = 'fb:' + strPitch + ';lr:' + strRoll
    length = "%04d" % len(send_data)
    send_data = 'rcpi' + length + send_data
    # Data Sample : "rcpi0020fb:-75.114;lr: 1.094"
    print (send_data)
    try:
        rtc = s.send(send_data)
        return rtc
    except socket.error:
        print 'send error'
        s.close()
        time.sleep(1)
        return (-1)

def ipcheck(ip):
    ippattern_str = '(([1-2]?[\d]{0,2}\.){1,3}([1-2]?[\d]{0,2})|any)'

    ippattern = re.compile(ippattern_str)
    # ippattern is now used to call match, passing only the ip string
    matchip = ippattern.match(ip)
    if matchip:
        print "ip match: %s" % matchip.group()
        return matchip.group()

if __name__ == "__main__":
    main()

