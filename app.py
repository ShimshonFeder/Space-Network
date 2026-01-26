from space_network_lib import SpaceEntity, Packet, SpaceNetwork

# class of sate llite, inherits from SpaceEntity
class Satellite(SpaceEntity):

    def receive_signal(self, packet: Packet):
        print(f"[{self.name}] Received: {packet}")

# Instance for a spce network for transmitting massages
space_net_1 = SpaceNetwork(level=1)

# Two instance of sate llite
sat_1  = Satellite("Sat1", 100)
sat_2  = Satellite("Sat2", 200)

# Create a massage(packet)
msg_1 = Packet("Hello from spaces!", sat_1, sat_2)

# Send message with our space network
space_net_1.send(msg_1)