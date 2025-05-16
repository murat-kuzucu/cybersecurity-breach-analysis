#!/usr/bin/env python3
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
def load_data(filename='../../data/cybersecurity_breach_data.csv'):
    try:
        df = pd.read_csv(filename)
        print(f"Loaded data with {len(df)} records")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None
def save_visualization(fig, filename, outputDir='../../output/visualizations'):
    Path(outputDir).mkdir(exist_ok=True, parents=True)
    outputPath = os.path.join(outputDir, filename)
    plt.savefig(outputPath, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved visualization: {outputPath}")
def setup_visualization_style():
    sns.set_style("whitegrid")
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.labelsize'] = 12