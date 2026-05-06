"""Script to generate Delivery Ratio vs. Number of Copies (L) chart for EE597."""
import matplotlib.pyplot as plt

def generate_delivery_ratio_graph():
    # --- 1. Define X-axis data (Number of Initial Copies L) ---
    L_values = [1, 2, 4, 8, 12, 16]

    # --- 2. Define Y-axis data (Delivery Ratio 0.0 to 1.0) ---
    # IMPORTANT: Replace these mock values with your actual Monte Carlo simulation results!
    # How to calculate Delivery Ratio: (Number of successful deliveries) / (Total simulation runs)
    
    # Epidemic: Always achieves maximum possible delivery (e.g., 97% success rate)
    # It does not depend on L, so it is a flat horizontal line.
    epidemic_ratio = [1, 1, 1, 1, 1, 1]
    
    # Direct Delivery: Lowest success rate. It only uses 1 copy (Source to Destination).
    # It also does not depend on L, so it is a flat horizontal line at the bottom.
    direct_delivery_ratio = [0.6, 0.6, 0.6, 0.6, 0.6, 0.6]
    
    # Binary Spray and Wait: Logarithmic growth approaching Epidemic.
    # When L=1, it acts like Direct Delivery. As L increases, it approaches Epidemic.
    binary_sw_ratio = [0.64, 0.7, 0.87, 0.97, 0.97, 0.97]

    # --- 3. Plotting the Graph ---
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot Epidemic (Baseline 1) - Flat line at the top
    ax.plot(L_values, epidemic_ratio, label='Epidemic (Baseline)', 
            linestyle='--', color='#FF4B4B', marker='s', linewidth=2.5, markersize=8)

    # Plot Binary Spray and Wait (Your Protocol) - Upward curve
    ax.plot(L_values, binary_sw_ratio, label='Binary Spray and Wait', 
            linestyle='-', color='#0066CC', marker='o', linewidth=3, markersize=8)

    # Plot Direct Delivery (Baseline 2) - Flat line at the bottom
    ax.plot(L_values, direct_delivery_ratio, label='Direct Delivery', 
            linestyle=':', color='#808080', marker='^', linewidth=2.5, markersize=8)

    # --- 4. Formatting the chart for an academic report ---
    ax.set_title('Delivery Ratio vs. Number of Copies (L)', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Number of Initial Copies (L)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Delivery Ratio', fontsize=12, fontweight='bold')
    
    # Set axis limits
    ax.set_xlim(0, 17)
    ax.set_ylim(0, 1.1) 
    
    # Set specific ticks for X-axis based on our L values
    ax.set_xticks(L_values)
    
    # Format Y-axis as percentages (0% to 100%)
    vals = ax.get_yticks()
    ax.set_yticklabels(['{:,.0%}'.format(x) for x in vals])

    # Add grid, legend, and layout adjustments
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='lower right', fontsize=11, framealpha=0.9, edgecolor='black')
    
    plt.tight_layout()

    # --- 5. Save and Show ---
    plt.savefig('delivery_ratio_vs_L.png', dpi=300)
    print("Graph successfully saved as 'delivery_ratio_vs_L.png'")
    plt.show()

if __name__ == '__main__':
    generate_delivery_ratio_graph()