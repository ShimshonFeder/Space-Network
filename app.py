import time
from space_network_lib import *

# class of sate llite, inherits from SpaceEntity
class Satellite(SpaceEntity):

    def receive_signal(self, packet: Packet):
        # Checked if type massage is RelayPacket
        if isinstance(packet, RelayPacket):
            inner_packet = packet.data
            print(f"Unwrapping and forwarding to {inner_packet.receiver}" )
            attempt_transmission(inner_packet)
        else:
            print(f"Final destination reached: {packet.data}" )

# class of earth, inherits from SpaceEntity
class Earth(SpaceEntity):
    def receive_signal(self, packet: Packet):
        pass

# Error: Satellite communication is broken
class BrokenConnectionError(CommsError):
    pass

# Packet class using a relay satellite (proxy) for message transmission
class RelayPacket(Packet):
    def __init__(self, paket_to_relay, sender, proxy):
        super().__init__(paket_to_relay, sender, proxy)

    def __repr__(self):
        return f"RelayPacket (Relaying [{self.data}] to {self.receiver} from {self.sender})"

# Function for sending messages with spaces, even when an error occurs
def attempt_transmission(packet: Packet):
    while True:
        try:
            space_net_1.send(packet)
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

# Instance of sate llite
sat_1  = Satellite("Sat1", 100)
sat_2  = Satellite("Sat2", 200)
sat_3  = Satellite("Sat3", 300)
sat_4  = Satellite("Sat4", 400)

# Instance of earth
earth = Earth("Earth", 0)

# Create a massage(packet), and proxy to send from earth
p_final = Packet("Hello from Earth!", sat_1, sat_2)
p_earth_to_sat1 = RelayPacket(p_final, earth, sat_1)

# Send message with function sending message
# # Catches errors using try/except, prints a warning
# # prevents the program from crashing
try:
    attempt_transmission(p_earth_to_sat1)
except BrokenConnectionError:
    print("Transmission failed!")