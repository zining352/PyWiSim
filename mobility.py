"""Mobility models for pywisim nodes."""
import math

class MobilityManager:
    # Added comm_range and dtn_mode parameters with safe default values
    def __init__(self, net, interval=1.0, speed=0.5, bounds=(10, 10), comm_range=2.0, dtn_mode=False):
        self.net, self.interval, self.speed = net, interval, speed
        self.bx, self.by = bounds
        self.targets = {}                          # waypoint targets {nid: (tx,ty)}
        
        self.dtn_mode = dtn_mode                   # Save the mode state
        self.comm_range = comm_range               # Communication radius
        self.active_links = set()                  # Record actively contacting nodes to prevent duplicate triggers

    def start(self, model='waypoint', alpha=0.8):
        self.model, self.running = model, True
        self.alpha = alpha                         # Gauss-Markov memory factor
        
        # Initialize velocity vectors for each node if using the GM model
        if self.model == 'gauss_markov':
            self.velocities = {}
            for nid in self.net.nodes:
                ang = self.net.rng.uniform(0, 2*math.pi)
                self.velocities[nid] = (self.speed * math.cos(ang), self.speed * math.sin(ang))
                
        self._step()

    def stop(self): self.running = False

    def _step(self):
        if not self.running: return
        ds = self.speed * self.interval            # distance per step
        rng = self.net.rng                         # reuse network's seeded RNG
        
        # --- 1. Coordinate Update Phase ---
        for nid in self.net.nodes:
            x, y = self.net.pos[nid]
            if self.model == 'waypoint':
                t = self.targets.get(nid)
                if not t or math.hypot(t[0]-x, t[1]-y) < ds:
                    t = (rng.uniform(0, self.bx), rng.uniform(0, self.by))
                    self.targets[nid] = t
                ang = math.atan2(t[1]-y, t[0]-x)
                x, y = x + ds*math.cos(ang), y + ds*math.sin(ang)
                
            elif self.model == 'walk':
                ang = rng.uniform(0, 2*math.pi)
                x, y = x + ds*math.cos(ang), y + ds*math.sin(ang)
                
            elif self.model == 'gauss_markov':
                # Gauss-Markov discrete velocity update formula
                vx, vy = self.velocities[nid]
                
                # Introduce Gaussian random noise (mean 0, standard deviation 0.5 * base speed)
                noise_x = rng.gauss(0, self.speed * 0.5)
                noise_y = rng.gauss(0, self.speed * 0.5)
                
                # Core formula: v_t = alpha * v_{t-1} + sqrt(1 - alpha^2) * noise
                alpha = self.alpha
                vx = alpha * vx + math.sqrt(1 - alpha**2) * noise_x
                vy = alpha * vy + math.sqrt(1 - alpha**2) * noise_y
                
                # Limit maximum speed to prevent velocity divergence
                v_mag = math.hypot(vx, vy)
                max_speed = self.speed * 1.5
                if v_mag > max_speed:
                    vx, vy = (vx / v_mag) * max_speed, (vy / v_mag) * max_speed
                
                self.velocities[nid] = (vx, vy)
                x, y = x + vx * self.interval, y + vy * self.interval

            # Boundary collision detection (introduced simple mirror bounce logic)
            if x < 0 or x > self.bx:
                x = max(0, min(self.bx, x))
                if self.model == 'gauss_markov': 
                    self.velocities[nid] = (-self.velocities[nid][0], self.velocities[nid][1])
            if y < 0 or y > self.by:
                y = max(0, min(self.by, y))
                if self.model == 'gauss_markov': 
                    self.velocities[nid] = (self.velocities[nid][0], -self.velocities[nid][1])

            self.net.pos[nid] = (x, y)
            
        # --- 2. Physical Encounter Detection Phase (executed only when dtn_mode is True) ---
        if self.dtn_mode:
            nids = list(self.net.nodes.keys())
            for i in range(len(nids)):
                for j in range(i+1, len(nids)):
                    n1, n2 = nids[i], nids[j]
                    
                    # Extract coordinates and calculate Euclidean distance
                    x1, y1 = self.net.pos[n1]
                    x2, y2 = self.net.pos[n2]
                    dist = math.hypot(x1 - x2, y1 - y2)
                    
                    link = frozenset([n1, n2])
                    
                    if dist <= self.comm_range:
                        if link not in self.active_links:
                            self.active_links.add(link)
                            # Trigger the ENCOUNTER event required by DTN routing protocols
                            self.net.nodes[n1].on_receive(('ENCOUNTER', n2), n2)
                            self.net.nodes[n2].on_receive(('ENCOUNTER', n1), n1)
                    else:
                        if link in self.active_links:
                            self.active_links.remove(link)

        self.net.loop.schedule(self.interval, self._step)