from space_network_lib import SpaceEntity, Packet, SpaceNetwork


class Satellite(SpaceEntity):

    def receive_signal(self, packet: Packet):
        print(f"[{self.name}] Received: {packet}")

# Instance for a spce network for transmitting massages
space_net_1 = SpaceNetwork(level=1)

# Two instance of sate llite
sat_1  = Satellite("Sat1", 100)
sat_2  = Satellite("Sat2", 200)