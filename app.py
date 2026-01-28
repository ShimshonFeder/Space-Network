import time
from space_network_lib import *

# class of sate llite, inherits from SpaceEntity
class Satellite(SpaceEntity):

    def receive_signal(self, packet: Packet):
        # Checked if type massage is RelayPacket
        if isinstance(packet, RelayPacket):
            print(f"[{self.name}] Unwrapping and forwarding to {packet.data.receiver}" )
            attempt_transmission(packet.data)
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

def sort_satellites(list_sat: list):
    # Sort satellites by distance from Earth (small to big)
    for i in range(len(list_sat)):
        for j in range(len(list_sat) - 1):
            if list_sat[j].distance_from_earth > list_sat[j + 1].distance_from_earth:
                list_sat[j], list_sat[j + 1] = list_sat[j + 1], list_sat[j]
    return list_sat


def build_relay_packet(path_rev: list[Satellite], packet: Packet):
    # sent from the satellite closest to the receiver
    inner  = Packet(packet.data, path_rev[1], path_rev[0])
    for i in range(1, len(path_rev) - 1):
        inner = RelayPacket(inner, path_rev[i + 1], path_rev[i])

    # Return the fully wrapped packet
    return inner


def smart_send_packet(sat_list: list[Satellite], packet: Packet):
    # Get sorted satellite list
    sort_list = sort_satellites(sat_list)

    sender = packet.sender
    receiver = packet.receiver

    new_path = [receiver]
    if sender.distance_from_earth < receiver.distance_from_earth:

        i = sort_list.index(sender)
        proxy = receiver

        while proxy != sender:
            if sort_list[i].distance_from_earth + 150 >= proxy.distance_from_earth:
                proxy = sort_list[i]
                new_path.append(proxy)
                i = sort_list.index(sender)
            else:
                i += 1
    return build_relay_packet(new_path, packet)


# Instance for a spce network for transmitting massages
space_net_1 = SpaceNetwork(level=6)

# Instance of sate llite
sat_1  = Satellite("Sat1", 20)
sat_2  = Satellite("Sat2", 60)
sat_3  = Satellite("Sat3", 180)
sat_4  = Satellite("Sat4", 250)
sat_5  = Satellite("Sat5", 300)
sat_6  = Satellite("Sat6", 370)
sat_7  = Satellite("Sat7", 450)

# Instance of earth
earth = Earth("Earth", 0)

# Proxy
list_sat = [earth, sat_1, sat_2, sat_3, sat_4, sat_5, sat_6, sat_7]


# Send message with function sending message
# # Catches errors using try/except, prints a warning
# # prevents the program from crashing

p_msg = Packet("hello", earth, sat_7)
packet_send = smart_send_packet(list_sat, p_msg)

try:
    attempt_transmission(packet_send)
except BrokenConnectionError:
    print("Transmission failed!")

# Test sort
