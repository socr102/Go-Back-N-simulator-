class Packet:
    """Represent a packet of data.
    Note - DO NOT REMOVE or CHANGE the data attribute!
    The simulation assumes this is present!"""

    def __init__(self, binary_data,seq):
        # Add which ever attributes you think you might need
        # to have a functional packet.
        # TIPS: Add a __str__ method to print a packet-object nicely! :)
        self.data = binary_data
        self.seq = seq
        self.status = ""

    def __str__(self):
        return str(self.data.decode())
