"""Script to generate Average Delivery Delay vs. Node Density chart for EE597."""
import matplotlib.pyplot as plt

def generate_delay_density_graph():
    node_counts = [20, 30, 40, 50]

    direct_delivery_delay = [86, 66, 110, 87]
    
    binary_sw_delay = [102.40, 59.80, 53.34, 42.66]

    epidemic_delay = [29.90, 23.23, 15.83, 11.85]

    fig, ax = plt.subplots(figsize=(8, 6))

    ax.plot(node_counts, direct_delivery_delay, label='Direct Delivery', 
            linestyle=':', color='#808080', marker='^', linewidth=2.5, markersize=8)

    ax.plot(node_counts, binary_sw_delay, label='Binary Spray and Wait', 
            linestyle='-', color='#0066CC', marker='o', linewidth=3, markersize=8)

    ax.plot(node_counts, epidemic_delay, label='Epidemic', 
            linestyle='--', color='#FF4B4B', marker='s', linewidth=2.5, markersize=8)

    ax.set_title('Average Delivery Delay vs. Node Density', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Number of Nodes in Simulation', fontsize=12, fontweight='bold')
    ax.set_ylabel('Average Delivery Delay (Seconds)', fontsize=12, fontweight='bold')
    
    ax.set_xticks(node_counts)
    ax.set_ylim(0, 140)

    ax.grid(True, linestyle='--', alpha=0.6)
    
    ax.legend(loc='upper right', fontsize=11, framealpha=0.9, edgecolor='black')
    
    plt.tight_layout()

    plt.savefig('delay_vs_density.png', dpi=300)
    print("Graph successfully saved as 'delay_vs_density.png'")
    plt.show()

if __name__ == '__main__':
    generate_delay_density_graph()