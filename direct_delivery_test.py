"""Direct Delivery (Hold and Delivery) vs. Node Density (Interactive Monte Carlo)."""
import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
from pywisim import EventLoop, Node, WirelessNetwork
from mobility import MobilityManager

global_transmission_count = 0

# --- 1. Routing Protocol Definition (Direct Delivery) ---
class direct_delivery(Node):
    def __init__(self, nid, dest_id):
        super().__init__(nid)
        self.buffer = {}                        
        self.dest_id = dest_id  # Needs to know who the ultimate destination is

    def inject(self, mid):
        self.buffer[mid] = True

    def on_receive(self, msg, sender):
        global global_transmission_count
        
        if msg[0] == 'ENCOUNTER':                  
            # Hold and Delivery Logic: ONLY forward if the encountered node is the FINAL destination
            if sender == self.dest_id:
                sender_node = self.net.nodes.get(sender)
                for mid in self.buffer.keys():
                    if mid not in sender_node.buffer:
                        self.unicast(sender, ('DATA', mid)) 
                        global_transmission_count += 1
                        
        elif msg[0] == 'DATA':
            mid = msg[1]
            if mid not in self.buffer:
                self.buffer[mid] = True

# --- 2. Single Simulation Wrapper Function ---
def run_single_simulation(current_seed, run_index, total_nodes):
    global global_transmission_count
    global_transmission_count = 0  
    
    loop = EventLoop()
    net = WirelessNetwork(loop, tx_range=20.0, loss=0.0, tx_time=0.01, verbose=False, seed=current_seed)
    
    DESTINATION_ID = str(total_nodes - 1)
    
    for i in range(total_nodes):
        nid = str(i)
        x_start = net.rng.uniform(0, 100)
        y_start = net.rng.uniform(0, 100)
        # Pass the destination ID so nodes know who to look for
        net.add_node(direct_delivery(nid, dest_id=DESTINATION_ID), x_start, y_start)

    mob = MobilityManager(net, interval=0.1, speed=5.0, bounds=(100, 100), comm_range=20.0, dtn_mode=True)
    mob.start(model='gauss_markov', alpha=0.8)

    SOURCE = '0'
    
    loop.schedule(0.1, net.nodes[SOURCE].inject, 'file.pdf')

    delivery_delay = None
    done = False

    def status():
        nonlocal delivery_delay, done
        if done: return
        
        if 'file.pdf' in net.nodes[DESTINATION_ID].buffer:
            delivery_delay = loop.time
            mob.stop()
            done = True

    for t in np.arange(0.5, 300, 0.5): 
        loop.schedule(float(t), status)

    loop.run(until=300)
    return delivery_delay, global_transmission_count

# --- 3. Interactive Batch Execution ---
if __name__ == '__main__':
    RUNS = 30
    
    print("="*50)
    print("   Direct Delivery (Hold & Delivery) Setup")
    print("="*50)
    
    # Interactive input for Densities (Default: 30)
    d_input = input("Enter node densities to test (comma-separated, e.g., 20,30,40) [Default: 30]: ").strip()
    if d_input:
        try:
            densities_to_test = [int(x.strip()) for x in d_input.split(',')]
        except ValueError:
            print("Invalid input. Using default Density = [30].")
            densities_to_test = [30]
    else:
        densities_to_test = [30]

    print("\n" + "="*50)
    print("=== Starting Unified DTN Experiments ===")
    print(f"Protocol: Direct Delivery (Hold and Delivery Baseline)")
    print(f"Densities to test: {densities_to_test}")
    print(f"Mobility: G")
    print("="*50)

    base_seed = int(time.time())

    for N in densities_to_test:
        print(f"\n[Testing Density: {N} Nodes]")
        delays = []
        overheads = []
        
        for i in range(1, RUNS + 1):
            delay, overhead = run_single_simulation(current_seed=base_seed + i, run_index=i, total_nodes=N)
            overheads.append(overhead)
            if delay is not None:
                delays.append(delay)
                
        avg_overhead = np.mean(overheads)
        if delays:
            avg_delay = np.mean(delays)
            print(f"  -> Delivery Ratio: {len(delays)}/{RUNS} ({len(delays)/RUNS*100:.1f}%)")
            print(f"  -> Average Delay: {avg_delay:.2f} seconds")
            print(f"  -> Average Overhead: {avg_overhead:.2f} transmissions")
        else:
            print(f"  -> Delivery Ratio: 0/{RUNS} (0.0%) - All runs failed within 300s limit.")
            print(f"  -> Average Overhead: {avg_overhead:.2f} transmissions")