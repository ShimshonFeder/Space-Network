import time
from space_network_lib import *

# class of sate llite, inherits from SpaceEntity
class Satellite(SpaceEntity):

    def receive_signal(self, packet: Packet):
        print(f"[{self.name}] Received: {packet}")

# Error: Satellite communication is broken
class BrokenConnectionError(CommsError):
    pass

# Function for sending messages with spaces, even when an error occurs
def attempt_transmission(space_network: SpaceNetwork, packet: Packet):
    while True:
        try:
            space_network.send(packet)
            break
        # Error: Temporary interruption detected
        # waiting two second before retrying
        except TemporalInterferenceError:
            print("Interference, waiting...")
            time.sleep(2)
        # Error: Random error occurred – retrying the operation
        except DataCorruptedError:
            print("Corrupted, retrying...")

        # Error: Satellite communication permanently lost
        except LinkTerminatedError:
            print("Link lost")
            raise BrokenConnectionError

        # Error: Target satellite out of range
        except OutOfRangeError:
            print("Target out of range")
            raise BrokenConnectionError

# Instance for a spce network for transmitting massages
# In level 3 change instance to level 2
space_net_1 = SpaceNetwork(level=3)

# Two instance of sate llite
sat_1  = Satellite("Sat1", 100)
sat_2  = Satellite("Sat2", 200)

# Create a massage(packet)
msg_1 = Packet("Hello from spaces!", sat_1, sat_2)

# Send message with function sending massage
# # Catches errors using try/except, prints a warning
# # prevents the program from crashing
try:
    attempt_transmission(space_net_1, msg_1)
except BrokenConnectionError:
    print("Transmission failed!")