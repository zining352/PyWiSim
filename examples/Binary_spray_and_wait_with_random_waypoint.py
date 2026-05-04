"""Binary spray and wait with Random Waypoint Mobility (Monte Carlo Simulation)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import numpy as np
from pywisim import EventLoop, Node, WirelessNetwork
from mobility import MobilityManager

# --- 1. Routing Protocol Definition ---
class binary_spray_and_wait(Node):
    def __init__(self, nid, L):
        super().__init__(nid)
        self.buffer = {}                        
        self.L = L

    def inject(self, mid):
        self.buffer[mid] = self.L

    def on_receive(self, msg, sender):
        sender_node = self.net.nodes.get(sender)
        if msg[0] == 'ENCOUNTER':                  
            for mid, quota in self.buffer.items():
                if quota > 1 and mid not in sender_node.buffer:
                    half_quota = quota // 2
                    self.buffer[mid] -= half_quota
                    # Call the underlying API to perform actual data transmission
                    self.unicast(sender, ('DATA', mid, half_quota)) 
        elif msg[0] == 'DATA':
            mid, received_quota = msg[1], msg[2]
            if mid not in self.buffer:
                self.buffer[mid] = received_quota

# --- 2. Single Simulation Wrapper Function ---
def run_single_simulation(current_seed, run_index):
    loop = EventLoop()
    
    net = WirelessNetwork(loop, tx_range=20.0, loss=0.0, tx_time=0.01, verbose=False, seed=current_seed)
    
    # Randomly assign initial coordinates for 8 nodes on a 100x100 map
    for nid in 'ABCDEFGH':
        x_start = net.rng.uniform(0, 100)
        y_start = net.rng.uniform(0, 100)
        net.add_node(binary_spray_and_wait(nid, L=4), x_start, y_start)

    # Initialize and start MobilityManager, dtn_mode=True must be enabled
    mob = MobilityManager(net, interval=0.1, speed=5.0, bounds=(100, 100), comm_range=20.0, dtn_mode=True)
    mob.start(model='waypoint', alpha=0.8)

    DESTINATION = 'H'
    
    # Source node A generates the file at t=0.1, aiming to deliver it to H
    loop.schedule(0.1, net.nodes['A'].inject, 'file.pdf')

    delivery_delay = None
    done = False

    def status():
        nonlocal delivery_delay, done
        if done: return
        
        # Check if the destination node has received the file
        if 'file.pdf' in net.nodes[DESTINATION].buffer:
            delivery_delay = loop.time
            mob.stop()
            done = True
            print(f"  [Run {run_index:02d}] Success! Delivery Delay: {delivery_delay:.1f} s")

    # Silently check status every 0.5 seconds, no more messy waiting printouts
    for t in np.arange(0.5, 300, 0.5): 
        loop.schedule(float(t), status)

    # Assuming maximum tolerable delay is 300 seconds; timeout counts as failure
    loop.run(until=300)
    
    if not done:
         print(f"  [Run {run_index:02d}] Failed: Destination unreachable within 300s limit.")
         
    return delivery_delay

# --- 3. Monte Carlo Batch Execution ---
if __name__ == '__main__':
    RUNS = 30
    delays = []

    print(f"\n=== Starting {RUNS} Independent Monte Carlo Simulations ===")
    print(f"Protocol: Binary Spray and Wait (L=4)")
    print(f"Mobility Model: Gauss-Markov (alpha=0.8, speed=5.0m/s)")
    print(f"Communication Radius: 20.0m\n")

    for i in range(1, RUNS + 1):
        # Pass the random seed to ensure completely different flight paths and spawn points per run
        delay = run_single_simulation(current_seed=i + 1000, run_index=i)
        if delay is not None:
            delays.append(delay)

    # Output statistical analysis results
    print("\n" + "="*30)
    print("=== Final Statistics ===")
    print("="*30)
    print(f"Success Rate: {len(delays)} / {RUNS}")
    
    if delays:
        avg_delay = np.mean(delays)
        std_delay = np.std(delays)
        print(f"Mean Delay: {avg_delay:.2f} seconds")
        print(f"Standard Deviation: {std_delay:.2f} seconds")
        
        # Calculate 95% Confidence Interval (approx 1.96 * standard error)
        se = std_delay / np.sqrt(len(delays))
        margin_of_error = 1.96 * se
        print(f"95% Confidence Interval: [{avg_delay - margin_of_error:.2f}, {avg_delay + margin_of_error:.2f}] seconds")
    print("="*30 + "\n")