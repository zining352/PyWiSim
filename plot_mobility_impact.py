"""Script to generate Mobility Model Impact (RWP vs. GM) chart for EE597."""
import matplotlib.pyplot as plt
import numpy as np

def generate_mobility_impact_graph():
    # --- 1. Define X-axis Categories (The Two Main Groups) ---
    labels = ['Random Waypoint (RWP)', 'Gauss-Markov (GM)']

    # --- 2. Input your Delivery Delay Data (Seconds) ---
    # IMPORTANT: Replace rwp_delays with the actual data you run!
    # Because of the "Center-Clustering Effect", RWP delays will be falsely lower.
    rwp_delays = [10.07, 8, 7.83, 6.83] 
    
    gm_delays = [102.40, 59.80, 53.34, 42.66]

    # Reorganize data so each density is a separate bar within the two main groups
    # Index 0 is RWP, Index 1 is GM
    density_20 = [rwp_delays[0], gm_delays[0]]
    density_30 = [rwp_delays[1], gm_delays[1]]
    density_40 = [rwp_delays[2], gm_delays[2]]
    density_50 = [rwp_delays[3], gm_delays[3]]

    # --- 3. Set up the Bar Chart Layout ---
    x = np.arange(len(labels))  # The label locations [0, 1]
    width = 0.15                # The width of each bar

    fig, ax = plt.subplots(figsize=(9, 6))

    # Plot the 4 bars for each Mobility Model group
    ax.bar(x - 1.5 * width, density_20, width, label='Density: 20 Nodes', color='#AED6F1', edgecolor='black')
    ax.bar(x - 0.5 * width, density_30, width, label='Density: 30 Nodes', color='#5DADE2', edgecolor='black')
    ax.bar(x + 0.5 * width, density_40, width, label='Density: 40 Nodes', color='#2874A6', edgecolor='black')
    ax.bar(x + 1.5 * width, density_50, width, label='Density: 50 Nodes', color='#154360', edgecolor='black')

    # --- 4. Formatting for Academic Standard ---
    ax.set_title('Graph 4: Mobility Model Impact (RWP vs. GM)\nAverage Delay for Spray & Wait (L=8)', 
                 fontsize=14, fontweight='bold', pad=15)
    ax.set_ylabel('Average Delivery Delay (Seconds)', fontsize=12, fontweight='bold')
    
    # Configure X-axis to show the two distinct mobility models
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=13, fontweight='bold')

    # Add grid lines behind the bars for better readability
    ax.set_axisbelow(True)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Add legend
    ax.legend(title='Network Scale', fontsize=11, title_fontsize=12, framealpha=0.9, edgecolor='black')

    plt.tight_layout()

    # --- 5. Save and Display ---
    plt.savefig('mobility_model_impact.png', dpi=300)
    print("Graph successfully saved as 'mobility_model_impact.png'")
    plt.show()

if __name__ == '__main__':
    generate_mobility_impact_graph()