import time
import zmq
import random
import thread
import logging
#
# This is the server
def server():
    port = "5560"
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.connect("tcp://localhost:%s" % port)
    server_id = random.randrange(1,10005)
    while True:
        try:
            time.sleep(1)
            socket.send("World from server %s" % server_id)
        except:
            message = socket.recv()
            print "Received request: {}".format(message)

## This is the client here.
def client():
    port = "5559"
    context = zmq.Context()
    print "Connecting to server..."
    socket = context.socket(zmq.REQ)
    socket.connect ("tcp://localhost:%s" % port)
    client_id = random.randrange(1,10005)
    #  Do 10 requests, waiting each time for a response
    for request in range (1,10):
        try:
            print "Sending request from client {} ... ".format(request)
            #print "here is the break "
            socket.send ("Hello from client %s" % client_id)
        except:
            message = socket.recv()
            print "Received reply {} , {}".format(request,message)

def queue():
    try:
        context = zmq.Context(1)
        # Socket facing clients
        frontend = context.socket(zmq.XREP)
        frontend.bind("tcp://*:5559")
        # Socket facing services
        backend = context.socket(zmq.XREQ)
        backend.bind("tcp://*:5560")
        zmq.device(zmq.QUEUE, frontend, backend)
    except Exception, e:
        print e
        print "bringing down zmq device"
    finally:
        pass
        frontend.close()
        backend.close()
        context.term()

def start_zmq():
    try:
        thread.start_new_thread(client, ( ) )
        thread.start_new_thread(server,( ))
    except Exception,e:
        print "There is an error is thread execution {}".format(e)
        logging.error(e)
    while True:
        pass

thread.start_new_thread(queue, ( ) )

start_zmq()