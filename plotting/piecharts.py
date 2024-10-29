import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import patheffects
import os

def create_pie_charts(csv_paths, output_path):
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    colors = {
        '< 35': '#82A6AD', '35-40': '#A0BABF', '40-45': '#B8D6D1',
        '45-50': '#CEE4CC', '50-55': '#E2F2BF', '55-60': '#F3C683',
        '60-65': '#E87E4D', '65-70': '#CD463E', '70-75': '#A11A4D',
        '75-80': '#75085C', '> 80': '#430A4A'
    }

    def plot_pie(ax, data, labels, title):
        # Generate the pie chart
        wedges, texts, autotexts = ax.pie(
            data,
            labels=labels,
            autopct='%1.0f%%',
            startangle=140,
            colors=[colors.get(label.replace(' dB', ''), '#808080') for label in labels],
            wedgeprops=dict(edgecolor='w'),
            explode=[0.1 if value < 5 else 0 for value in data]
        )

        for text in autotexts:
            text.set_fontsize(10)
            text.set_path_effects([
                patheffects.Stroke(linewidth=2, foreground="white"),
                patheffects.Normal()
            ])

        ax.set_title(title, pad=20)

    fig, axes = plt.subplots(2, 2, figsize=(16, 16))

    titles = ['No Change - Baseline', 'Speed limit set to 10 km/h', 'Changed to footway', 'Changed to no vehicles']

    # Top left: Baseline
    df_baseline = pd.read_csv(csv_paths[0])
    df_baseline['ISOLABEL'] = df_baseline['ISOLABEL'].astype(str) + ' dB'
    df_baseline['area_original'] = (df_baseline['area_original'] / df_baseline['area_original'].sum()) * 100
    df_baseline_grouped = df_baseline.groupby('ISOLABEL').sum().reset_index()
    plot_pie(axes[0, 0], df_baseline_grouped['area_original'], df_baseline_grouped['ISOLABEL'], titles[0])

    # Top right: 10 km/h
    df_10kmh = pd.read_csv(csv_paths[2])
    df_10kmh['ISOLABEL'] = df_10kmh['ISOLABEL'].astype(str) + ' dB'
    df_10kmh['area_after_change'] = (df_10kmh['area_after_change'] / df_10kmh['area_after_change'].sum()) * 100
    df_10kmh_grouped = df_10kmh.groupby('ISOLABEL').sum().reset_index()
    plot_pie(axes[0, 1], df_10kmh_grouped['area_after_change'], df_10kmh_grouped['ISOLABEL'], titles[1])

    # Bottom left: Footway
    df_footway = pd.read_csv(csv_paths[1])
    df_footway['ISOLABEL'] = df_footway['ISOLABEL'].astype(str) + ' dB'
    df_footway['area_after_change'] = (df_footway['area_after_change'] / df_footway['area_after_change'].sum()) * 100
    df_footway_grouped = df_footway.groupby('ISOLABEL').sum().reset_index()
    plot_pie(axes[1, 0], df_footway_grouped['area_after_change'], df_footway_grouped['ISOLABEL'], titles[2])

    # Bottom right: No vehicles
    df_no_vehicles = pd.read_csv(csv_paths[0])
    df_no_vehicles['ISOLABEL'] = df_no_vehicles['ISOLABEL'].astype(str) + ' dB'
    df_no_vehicles['area_after_change'] = (df_no_vehicles['area_after_change'] / df_no_vehicles['area_after_change'].sum()) * 100
    df_no_vehicles_grouped = df_no_vehicles.groupby('ISOLABEL').sum().reset_index()
    plot_pie(axes[1, 1], df_no_vehicles_grouped['area_after_change'], df_no_vehicles_grouped['ISOLABEL'], titles[3])

    fig.suptitle('Area Distribution by Noise Level', fontsize=16, fontweight='bold', y=0.95)

    plt.subplots_adjust(top=0.9)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.show()

output_dir = 'output/area'
csv_paths = [os.path.join(output_dir, file) for file in os.listdir(output_dir) if file.endswith('_area_change.csv')]
output_path = 'figures/piecharts.png'
create_pie_charts(csv_paths, output_path)