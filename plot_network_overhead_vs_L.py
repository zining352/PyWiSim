"""Script to generate Network Overhead vs. Number of Copies (L) chart for EE597."""
import matplotlib.pyplot as plt

def generate_overhead_graph():
    L_values = [1, 2, 4, 8, 12, 16]
    epidemic_overhead = [16.77, 16.77, 16.77, 16.77, 16.77, 16.77]

    binary_sw_overhead = [0.63, 1.70, 3.77, 6.93, 8.67, 8.83]

    fig, ax = plt.subplots(figsize=(8, 6))

    ax.plot(L_values, epidemic_overhead, label='Epidemic (Massive Overhead)', 
            linestyle='--', color='#FF4B4B', marker='s', linewidth=2.5, markersize=8)

    ax.plot(L_values, binary_sw_overhead, label='Binary Spray and Wait (Bounded)', 
            linestyle='-', color='#0066CC', marker='o', linewidth=3, markersize=8)

    ax.set_title('Network Overhead vs. Number of Copies (L)', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Number of Initial Copies (L)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Total Transmissions (Network Overhead)', fontsize=12, fontweight='bold')
    
    ax.set_xlim(0, 17)
    ax.set_ylim(0, 18) 
    
    ax.set_xticks(L_values)

    ax.grid(True, linestyle='--', alpha=0.6)
    
    ax.legend(loc='lower right', fontsize=11, framealpha=0.9, edgecolor='black')
    
    plt.tight_layout()

    plt.savefig('network_overhead_vs_L.png', dpi=300)
    print("Graph successfully saved as 'network_overhead_vs_L.png'")
    plt.show()

if __name__ == '__main__':
    generate_overhead_graph()