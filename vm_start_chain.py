"""EE 250L Lab 04 Starter Code
Run vm_sub.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt
import time

"""This function (or "callback") will be executed when this client receives 
a connection acknowledgement packet response from the server. """
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    #replace user with your USC username in all subscriptions
    client.subscribe("rsabino/pong")
    
    #Add the custom callbacks by indicating the topic and the name of the callback handle
    client.message_callback_add("rsabino/pong", on_message_from_pong)


"""This object (functions are objects!) serves as the default callback for 
messages received when another node publishes a message this client is 
subscribed to. By "default,"" we mean that this callback is called if a custom 
callback has not been registered using paho-mqtt's message_callback_add()."""
def on_message(client, userdata, msg):
    print("Default callback - topic: " + msg.topic + "   msg: " + str(msg.payload, "utf-8"))

#Custom message callback.
def on_message_from_pong(client, userdata, message):
   firstMessageFlag = True
   print("Custom callback  - pong: "+message.payload.decode())
   i = int(message.payload.decode())
   print(i)
   i+=1
   client.publish("rsabino/ping", f"{i}")
   print("Publishing ping")
   time.sleep(1)


if __name__ == '__main__':
    firstMessageFlag = False;
    initial = 0
    #create a client object
    client = mqtt.Client()
    
    #attach the on_connect() callback function defined above to the mqtt client
    client.on_connect = on_connect
    client.on_message = on_message
    """Connect using the following hostname, port, and keepalive interval (in 
    seconds). We added "host=", "port=", and "keepalive=" for illustrative 
    purposes. You can omit this in python. For example:
    
    `client.connect("eclipse.usc.edu", 11000, 60)` 
    
    The keepalive interval indicates when to send keepalive packets to the 
    server in the event no messages have been published from or sent to this 
    client. If the connection request is successful, the callback attached to
    `client.on_connect` will be called."""

    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)

    """ask paho-mqtt to spawn a separate thread to handle
    incoming and outgoing mqtt messages."""
    client.loop_start()
    time.sleep(1)

    while (firstMessageFlag == False):
        #replace user with your USC username in all subscriptions
        client.publish("rsabino/ping", f"{initial}")
        print("Publishing ping")
        time.sleep(4)


        
