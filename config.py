"""Main config file used to control key aspects of a particular simulation run.
"""
# Tips: Make it work for one thing at a time:
# - Start with dropped packets only
# - Then corrupted packets only
# - Then delayed packets only

# Keep the number of packets low in the beginning

# Number of packets per simulation
PACKET_NUM = 10
#the Number of packet in each frame
PACKET_FRAME = 4

# The size of each packet in bytes.
# The data in each packet will be uppercase ASCII letters only!
PACKET_SIZE = 4

# The seed ensures a new run is identical to the last
RANDOM_SEED = 84737869  # I love you! :)
# If you don't want an identical run, set this to True
RANDOM_RUN = False

# The chance that each packet is dropped
DROP_CHANCE = 0.0
# The chance that the data in a packet is changed
CORRUPT_CHANCE = 0.0

# The chance that the packet is delayed
DELAY_CHANCE = 0.0

while 1:
	key = input("Please enter 'z' to test DROPPING\nPlease enter 'x' to test COURRUPTING\nPlease enter 'c' to test DELAYING\n")
	if key=='z':
		print("Please input (0.0~1.0)\n")
		DROP_CHANCE = float(input())
		if 0.0<=DROP_CHANCE<1.0:
			break
	if key=='x':
		print("Please input (0.0~1.0)\n")
		CORRUPT_CHANCE = float(input())
		if 0.0<=CORRUPT_CHANCE<1.0:
			break
	if key=='c':
		print("Please input (0.0~1.0)\n")
		DELAY_CHANCE= float(input())
		if 0.0<=DELAY_CHANCE<1.0:
			break


# Delay in seconds
DELAY_AMOUNT = 3
