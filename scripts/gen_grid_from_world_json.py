import matplotlib.pyplot as plt
import json
import numpy as np

# Define colors and styles based on location type
TERRAIN_TYPES = {
    "forest edge": "#228B22",  # Green
    "glade": "#ADFF2F",  # Light green
    "grove": "#7FFF00",  # Medium green
    "dense forest": "#006400",  # Dark green
    "dense underbrush": "#556B2F",  # Olive green
    "meadow edge": "#FFD700",  # Yellow
    "rugged forest": "#8B4513",  # Brown
    "field approach": "#F4A460",  # Sandy brown
}


def load_json_from_file(file_path):
    """Load JSON data from a file."""
    with open(file_path, 'r') as f:
        return json.load(f)


def plot_locations(json_data):
    """Plot the locations from the JSON data on a game-style map."""
    locations = json_data['locations']

    fig, ax = plt.subplots(figsize=(12, 12))

    # Create a list to track the plotted points and corresponding names
    plotted_points = []

    # Define size scaling factor for locations
    scaling_factor = 300

    # Create a background grid with texture-like appearance
    x_vals = np.arange(-3, 4, 1)
    y_vals = np.arange(-3, 4, 1)
    ax.set_xticks(x_vals)
    ax.set_yticks(y_vals)
    ax.set_xlim([-3, 3])
    ax.set_ylim([-3, 3])
    ax.grid(True, color='gray', linestyle='--', alpha=0.5)  # Light grid for terrain

    # Plot each location with a terrain style
    for location in locations:
        coords = location['coords']
        name = location['name']
        location_type = location.get("type", "forest edge").split(":")[-1].strip()

        x, y = coords['x'], coords['y']
        terrain_color = TERRAIN_TYPES.get(location_type, "#D3D3D3")  # Default gray if type not found

        # Plot the terrain as a background color
        ax.fill_between([x - 0.5, x + 0.5], y - 0.5, y + 0.5, color=terrain_color, alpha=0.5)

        # Plot the location marker with a different color
        ax.scatter(x, y, color='black', s=scaling_factor, marker='o', edgecolor='black')

        # Track the plotted points for labeling
        plotted_points.append((x, y, name))

    # Label each location with its name
    for x, y, name in plotted_points:
        ax.annotate(
            name, (x, y),
            textcoords="offset points",  # Positioning relative to the point
            xytext=(0, 10),  # Offset the text a bit from the point
            ha='center', fontsize=8,
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none')  # Add a white background to the text
        )

    # Set a more game-like title
    ax.set_title('Game Map of Generated Locations', fontsize=16, weight='bold')

    # Save the plot to a file instead of displaying it
    plt.savefig("game_map_output.png", dpi=300)  # High resolution for a nicer output


def main():
    # Ask user to input a file path or JSON string
    file_or_input = input("Enter the path to the JSON file or input JSON text directly: ")

    try:
        # Check if the input is a file path
        if file_or_input.endswith('.json'):
            json_data = load_json_from_file(file_or_input)
        else:
            # Assume the input is a JSON string and parse it
            json_data = json.loads(file_or_input)

        # Plot the locations from the JSON data
        plot_locations(json_data)

    except Exception as e:
        print(f"Error processing the input: {str(e)}")


if __name__ == '__main__':
    main()
