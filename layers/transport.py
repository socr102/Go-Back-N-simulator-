from copy import copy
from threading import Timer

from packet import Packet

from config import PACKET_FRAME
class TransportLayer:
    """The transport layer receives chunks of data from the application layer
    and must make sure it arrives on the other side unchanged and in order.
    """

    def __init__(self):
        self.timer = None
        self.timeout = 0.4  # Seconds

        self.seq = 1
        self.start = 1
        self.status = ["ACK"]

    def with_logger(self, logger):
        self.logger = logger
        return self

    def register_above(self, layer):
        self.application_layer = layer

    def register_below(self, layer):
        self.network_layer = layer

    def from_app(self, binary_data):
        packet = Packet(binary_data,self.seq)
        # Implement me!
        if self.status[self.seq-1] == "ACK":
            if self.seq-self.start > PACKET_FRAME-1:
                self.start = self.start + PACKET_FRAME

            if self.seq-self.start < PACKET_FRAME:

                state = self.network_layer.send(packet)
                packet.seq = self.seq
                self.seq += 1

                if state=="drop":

                    self.application_layer.payload.pos -= self.application_layer.payload.chunk_size*(self.seq-self.start)
                    self.status = self.status[0:self.start]
                    self.seq = self.start
                    print("Resending....")
                    self.application_layer.send_next_packet()


                elif state == "delay":

                    self.timer = self.network_layer.timer_object
                    self.application_layer.payload.pos -= self.application_layer.payload.chunk_size*(self.seq-self.start)
                    self.status = self.status[0:self.start]
                    self.seq  = self.start
                    print("Resending....")
                    self.reset_timer(self.application_layer.send_next_packet)

                else:
                    if self.application_layer.payload.remaining_bytes==0:
                        exit()
                    self.status.append("ACK")
                
            else:

                print("waiting........")
                self.application_layer.payload.pos -= self.application_layer.payload.chunk_size
                self.application_layer.send_next_packet()

    def from_network(self, packet):
        # Implement me!
        flag = True
        for data in packet.data:

            if data < 65 or data > 90:

                flag = False
                break

        if flag == True:
            print("packet",packet.seq,packet.data)

            self.application_layer.receive_from_transport(packet.data)

        else:


            self.network_layer.recipient.transport_layer.application_layer.payload.pos -= self.network_layer.recipient.transport_layer.application_layer.payload.chunk_size*(self.network_layer.recipient.transport_layer.seq-self.network_layer.recipient.transport_layer.start+1)

            self.network_layer.recipient.transport_layer.seq = self.network_layer.recipient.transport_layer.start

            self.network_layer.recipient.transport_layer.application_layer.send_next_packet()
            self.network_layer.recipient.transport_layer.seq -=1
            
            
            

    def reset_timer(self, callback, *args):
        # This is a safety-wrapper around the Timer-objects, which are
        # separate threads. If we have a timer-object already,
        # stop it before making a new one so we don't flood
        # the system with threads!
        if self.timer:
            if self.timer.is_alive():
                self.timer.cancel()
        # callback(a function) is called with *args as arguments
        # after self.timeout seconds.
        self.timer = Timer(self.timeout, callback, *args)
        self.timer.start()
