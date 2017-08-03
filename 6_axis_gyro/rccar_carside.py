import socket
import sys
import re
import RPi.GPIO as gpio
import time

LOCALHOST = '127.0.0.1'
PORT = 10000
TIME_OUT = 100

#Motor 1 GPIO Pin
IC1A = 4
IC1B = 17

#Motor 2 GPIO Pin
IC2A = 27
IC2B = 22

#RuntimeWarning: This channel is already in use, continuing anyway.  Use GPIO.setwarnings(False) to disable warnings.
#gpio.setwarnings(False)

gpio.cleanup()

gpio.setmode(gpio.BCM)

#Motor Pin Setup
gpio.setup(IC1A, gpio.OUT)
gpio.setup(IC1B, gpio.OUT)
gpio.setup(IC2A, gpio.OUT)
gpio.setup(IC2B, gpio.OUT)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def main():
    HOST = LOCALHOST
    # Bind the socket to the port
    if len(sys.argv) > 1:
        HOST = ipcheck(sys.argv[1])
    server_address = (HOST, PORT)
    print >>sys.stderr, 'starting up on %s port %s' % server_address
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    while True:
        # Wait for a connection
        print >>sys.stderr, 'waiting for a connection'
        connection, client_address = sock.accept()

        # Timeout
        connection.settimeout(TIME_OUT)

        try:
            print >>sys.stderr, 'connection from', client_address

            # Receive the data in small chunks and retransmit it
            while True:
                try:
                    data = connection.recv(8)
                    print >>sys.stderr, 'head received "%s"' % data
                except socket.error:
                    print 'Data Receive Error'
                    connection.close()
                    time.sleep(2)
                    break

                if not data.lower().startswith("rcpi"):
                    # Clean up the connection
                    connection.close()
                    continue
                rcvLength = int(data.replace("rcpi",""))

                if rcvLength > 0:
                    data = connection.recv(rcvLength)

                    if data:
                        pdata = parsing_data(data)
                        #print 'Go %s' % pdata

                else:
                    print >>sys.stderr, 'no more data from', client_address
                    break

        except socket.timeout:
            print 'timeout error : "%d" secs' % TIME_OUT
            connection.close()

        finally:
            # Clean up the connection
            connection.close()

def parsing_data(data) :
    data = data.lower()
    #print 'receive data : %s' % data

    splitCode = data.split(';')

    for i in range(len(splitCode)):
        splitValue = splitCode[i].split(':')

        try:
            #print >>sys.stderr, 'Receive Key : "%s"' % arrStr[i]

            strCode = splitValue[0]
            strValue = splitValue[1]

            if ( strCode == 'fb' ):
                print 'Move Forward/Backward %s speed' % strValue
            elif ( strCode == 'lr' ):
                print 'Trun Left/Right %s speed' % strValue
            else:
                print 'unknown commend'
                return 'u'

            run_motor(strCode, float(strValue))

        except ValueError:
            return 'a'

def run_motor(rcvCode, rcvValue):
    if ( rcvCode == 'lr' ):
        if rcvValue < -10:
            print 'GPIO Turn Right %f' % rcvValue
            gpio.output(IC1A, gpio.LOW)
            gpio.output(IC1B, gpio.HIGH)
        elif rcvValue > 10:
            print 'GPIO Turn Left %f' % rcvValue
            gpio.output(IC1A, gpio.HIGH)
            gpio.output(IC1B, gpio.LOW)
        else:
            print 'GPIO Front Wheel Zero'
            gpio.output(IC1A, gpio.LOW)
            gpio.output(IC1B, gpio.LOW)
    elif ( rcvCode == 'fb' ):
        if rcvValue > 10:
            print 'GPIO Forward %f' % rcvValue
            gpio.output(IC2A, gpio.LOW)
            gpio.output(IC2B, gpio.HIGH)
        elif rcvValue < -10:
            print 'GPIO Backward %f' % rcvValue
            gpio.output(IC2A, gpio.HIGH)
            gpio.output(IC2B, gpio.LOW)
        else:
            print 'GPIO Stop Back Wheel'
            gpio.output(IC2A, gpio.LOW)
            gpio.output(IC2B, gpio.LOW)

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



