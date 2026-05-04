"""binary spray and wait over an intermittently connected mobile network (DTN)."""
import sys; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pywisim import EventLoop, Node, WirelessNetwork
from encounter import EncounterManager

class source_spray_and_wait(Node):
    def __init__(self, nid, L):
        super().__init__(nid)
        self.buffer = {}                        # message IDs this node carries
        self.L = L

    def inject(self, mid):
        self.buffer[mid] = self.L
        self.net.log(f"{self.nid}: originated '{mid}'")

    def on_receive(self, msg, sender):
        sender_node = self.net.nodes.get(sender)
        if msg[0] == 'ENCOUNTER':                  # encounter triggers exchange
            for mid, quota in self.buffer.items():
                if quota > 1 and mid not in sender_node.buffer:
                    half_quota = quota // 2
                    self.buffer[mid] -= half_quota
                    self.unicast(sender, ('DATA', mid, half_quota)) # standard pywisim send
        elif msg[0] == 'DATA':
            mid, received_quota = msg[1], msg[2]
            if mid not in self.buffer:
                self.buffer[mid] = received_quota

# --- setup: 8 nodes, lossless encounters ---
loop = EventLoop()
net = WirelessNetwork(loop, loss=0.0, tx_time=0.01, verbose=True, seed=42)
for nid in 'ABCDEFGH':
    net.add_node(source_spray_and_wait(nid, L=8), 0, 0)

enc = EncounterManager(net, rate=1.5, duration=1.0)

# A originates a file at t=0.1
loop.schedule(0.1, net.nodes['A'].inject, 'file.pdf')
enc.start()

# periodic status checks; stop once all nodes have the file
done = False
def status():
    global done
    if done: return
    have = sorted(n for n in net.nodes if net.nodes[n].buffer)
    print(f"\n  Status (t={loop.time:.1f}): {len(have)}/{len(net.nodes)} nodes have file: {have}\n")
    if len(have) == len(net.nodes):
        enc.stop(); done = True

for t in range(2, 60, 2):
    loop.schedule(float(t), status)

loop.run(until=60)
