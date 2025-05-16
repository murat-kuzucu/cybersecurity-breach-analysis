import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import os

def improve_defense_mechanism_visualization():
    """
    Creates an improved and more understandable visualization for defense mechanism effectiveness.
    Uses snake_case for function names and camelCase for variable names.
    """
    print("Generating improved defense mechanism effectiveness visualization...")
    
    # Create output directory
    outputDir = Path('output/enhanced_analysis')
    outputDir.mkdir(exist_ok=True, parents=True)
    
    # Load the enhanced data
    dataPath = Path('../Enhanced_Cybersecurity_Data.csv')
    try:
        df = pd.read_csv(dataPath)
        print(f"Loaded data with {len(df)} records")
    except Exception as e:
        print(f"Error loading data: {e}")
        return
    
    # Set the style for all visualizations
    sns.set_style("whitegrid")
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = 'Arial'
    
    # 1. Defense Mechanism Effectiveness - Bar Chart (Mean and Error bars)
    plt.figure(figsize=(14, 8))
    
    # Calculate mean and standard error for each defense mechanism
    defenseSummary = df.groupby('Defense Mechanism Used').agg({
        'Incident Resolution Time (in Hours)': ['mean', 'sem'],
        'Financial Loss (in Million $)': ['mean', 'sem']
    }).reset_index()
    
    # Sort by mean resolution time
    defenseSummary = defenseSummary.sort_values(('Incident Resolution Time (in Hours)', 'mean'))
    
    # Create bar chart with error bars for resolution time
    plt.subplot(1, 2, 1)
    
    # Define custom color palette with distinct colors
    colorPalette = sns.color_palette("viridis", len(defenseSummary))
    
    # Create bars
    bars = plt.bar(
        defenseSummary['Defense Mechanism Used'], 
        defenseSummary[('Incident Resolution Time (in Hours)', 'mean')],
        yerr=defenseSummary[('Incident Resolution Time (in Hours)', 'sem')],
        capsize=5,
        color=colorPalette,
        width=0.6,
        edgecolor='black',
        linewidth=1
    )
    
    plt.title('Average Resolution Time by Defense Mechanism', fontsize=14, fontweight='bold')
    plt.xlabel('Defense Mechanism', fontsize=12)
    plt.ylabel('Resolution Time (Hours)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    
    # Add value labels on top of bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width()/2.,
            height + 1,
            f'{height:.1f}h',
            ha='center',
            va='bottom',
            fontsize=10,
            fontweight='bold'
        )
    
    # Create bar chart with error bars for financial loss
    plt.subplot(1, 2, 2)
    
    # Sort by mean financial loss
    defenseSummary = defenseSummary.sort_values(('Financial Loss (in Million $)', 'mean'))
    
    # Create bars
    bars = plt.bar(
        defenseSummary['Defense Mechanism Used'], 
        defenseSummary[('Financial Loss (in Million $)', 'mean')],
        yerr=defenseSummary[('Financial Loss (in Million $)', 'sem')],
        capsize=5,
        color=colorPalette,
        width=0.6,
        edgecolor='black',
        linewidth=1
    )
    
    plt.title('Average Financial Loss by Defense Mechanism', fontsize=14, fontweight='bold')
    plt.xlabel('Defense Mechanism', fontsize=12)
    plt.ylabel('Financial Loss (Million $)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    
    # Add value labels on top of bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width()/2.,
            height + 1,
            f'${height:.1f}M',
            ha='center',
            va='bottom',
            fontsize=10,
            fontweight='bold'
        )
    
    plt.tight_layout(pad=3.0)
    plt.savefig(outputDir / 'defense_mechanism_effectiveness.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Defense Mechanism Effectiveness - Combined Visualization
    plt.figure(figsize=(14, 10))
    
    # Create a pivot table for average resolution time by defense mechanism and attack type
    defenseAttackPivot = pd.pivot_table(
        data=df,
        values='Incident Resolution Time (in Hours)',
        index='Defense Mechanism Used',
        columns='Attack Type',
        aggfunc='mean'
    )
    
    # Plot heatmap
    plt.subplot(2, 1, 1)
    sns.heatmap(
        defenseAttackPivot,
        annot=True,
        fmt='.1f',
        cmap='YlGnBu',
        linewidths=0.5,
        cbar_kws={'label': 'Resolution Time (Hours)'}
    )
    plt.title('Defense Mechanism Effectiveness Against Different Attack Types', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    # Create scatter plot showing resolution time vs financial loss by defense mechanism
    plt.subplot(2, 1, 2)
    
    # Group by defense mechanism
    defenseGrouped = df.groupby('Defense Mechanism Used').agg({
        'Incident Resolution Time (in Hours)': 'mean',
        'Financial Loss (in Million $)': 'mean',
        'Number of Affected Users': 'mean'
    }).reset_index()
    
    # Normalize for bubble size (number of affected users)
    maxUsers = defenseGrouped['Number of Affected Users'].max()
    defenseGrouped['BubbleSize'] = (defenseGrouped['Number of Affected Users'] / maxUsers) * 1000
    
    # Create scatter plot with varying bubble sizes
    scatter = plt.scatter(
        defenseGrouped['Incident Resolution Time (in Hours)'],
        defenseGrouped['Financial Loss (in Million $)'],
        s=defenseGrouped['BubbleSize'],
        c=range(len(defenseGrouped)),
        cmap='viridis',
        alpha=0.7,
        edgecolors='black'
    )
    
    # Add labels for each point
    for i, row in defenseGrouped.iterrows():
        plt.annotate(
            row['Defense Mechanism Used'],
            (row['Incident Resolution Time (in Hours)'], row['Financial Loss (in Million $)']),
            xytext=(7, 0),
            textcoords='offset points',
            fontsize=10,
            fontweight='bold'
        )
    
    plt.title('Defense Mechanism: Resolution Time vs. Financial Loss', fontsize=14, fontweight='bold')
    plt.xlabel('Average Resolution Time (Hours)', fontsize=12)
    plt.ylabel('Average Financial Loss (Million $)', fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Add a horizontal line for average financial loss
    plt.axhline(y=df['Financial Loss (in Million $)'].mean(), color='red', linestyle='--', alpha=0.7)
    plt.text(
        df['Incident Resolution Time (in Hours)'].min(), 
        df['Financial Loss (in Million $)'].mean() + 2,
        f'Average Loss: ${df["Financial Loss (in Million $)"].mean():.2f}M',
        color='red',
        fontweight='bold'
    )
    
    # Add a vertical line for average resolution time
    plt.axvline(x=df['Incident Resolution Time (in Hours)'].mean(), color='blue', linestyle='--', alpha=0.7)
    plt.text(
        df['Incident Resolution Time (in Hours)'].mean() + 2, 
        df['Financial Loss (in Million $)'].min(),
        f'Average Time: {df["Incident Resolution Time (in Hours)"].mean():.1f}h',
        color='blue',
        fontweight='bold',
        rotation=90
    )
    
    plt.tight_layout(pad=3.0)
    plt.savefig(outputDir / 'defense_mechanism_effectiveness_detailed.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Defense Mechanism Ranking Visualization
    # Create a scoring system (lower is better):
    # Score = (Normalized Resolution Time * 0.5) + (Normalized Financial Loss * 0.5)
    
    defenseScoring = defenseGrouped.copy()
    
    # Normalize values between 0 and 1 (min-max scaling)
    defenseScoring['NormalizedTime'] = (defenseScoring['Incident Resolution Time (in Hours)'] - defenseScoring['Incident Resolution Time (in Hours)'].min()) / (defenseScoring['Incident Resolution Time (in Hours)'].max() - defenseScoring['Incident Resolution Time (in Hours)'].min())
    defenseScoring['NormalizedLoss'] = (defenseScoring['Financial Loss (in Million $)'] - defenseScoring['Financial Loss (in Million $)'].min()) / (defenseScoring['Financial Loss (in Million $)'].max() - defenseScoring['Financial Loss (in Million $)'].min())
    
    # Calculate combined score
    defenseScoring['EffectivenessScore'] = 1 - ((defenseScoring['NormalizedTime'] * 0.5) + (defenseScoring['NormalizedLoss'] * 0.5))
    
    # Sort by effectiveness score
    defenseScoring = defenseScoring.sort_values('EffectivenessScore', ascending=False)
    
    # Create horizontal bar chart
    plt.figure(figsize=(12, 8))
    
    # Define color gradient based on score
    scoreColors = plt.cm.RdYlGn(defenseScoring['EffectivenessScore'])
    
    # Create horizontal bars
    bars = plt.barh(
        defenseScoring['Defense Mechanism Used'],
        defenseScoring['EffectivenessScore'] * 100,  # Convert to percentage
        color=scoreColors,
        edgecolor='black',
        linewidth=1,
        height=0.6
    )
    
    plt.title('Defense Mechanism Effectiveness Ranking', fontsize=16, fontweight='bold')
    plt.xlabel('Effectiveness Score (0-100)', fontsize=14)
    plt.xlim(0, 100)
    plt.grid(axis='x', alpha=0.3)
    
    # Add value labels to the right of bars
    for i, bar in enumerate(bars):
        width = bar.get_width()
        plt.text(
            width + 1,
            bar.get_y() + bar.get_height()/2,
            f'{width:.1f}%',
            va='center',
            fontsize=10,
            fontweight='bold'
        )
    
    # Add explanatory note
    plt.figtext(
        0.5, 
        0.01, 
        "Effectiveness score based on resolution time and financial loss (higher is better)",
        ha='center',
        fontsize=10,
        style='italic'
    )
    
    plt.tight_layout(pad=1.5)
    plt.savefig(outputDir / 'defense_mechanism_ranking.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Improved defense mechanism visualizations created successfully!")

if __name__ == "__main__":
    improve_defense_mechanism_visualization()
