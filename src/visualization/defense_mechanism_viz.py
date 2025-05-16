import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
def create_defense_mechanism_visualizations():
    print("Generating improved defense mechanism visualizations...")
    outputDir = Path('output/enhanced_analysis')
    outputDir.mkdir(exist_ok=True, parents=True)
    dataPath = Path('../Enhanced_Cybersecurity_Data.csv')
    try:
        df = pd.read_csv(dataPath)
        print(f"Loaded data with {len(df)} records")
    except Exception as e:
        print(f"Error loading data: {e}")
        return
    sns.set_style("whitegrid")
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.figure(figsize=(12, 7))
    defenseData = df.groupby('Defense Mechanism Used')['Incident Resolution Time (in Hours)'].mean().sort_values()
    barColors = sns.color_palette("viridis", len(defenseData))
    bars = plt.bar(
        defenseData.index,
        defenseData.values,
        color=barColors,
        width=0.6,
        edgecolor='black',
        linewidth=1
    )
    plt.title('Average Resolution Time by Defense Mechanism', fontsize=16, fontweight='bold')
    plt.xlabel('Defense Mechanism', fontsize=14)
    plt.ylabel('Average Resolution Time (Hours)', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width()/2.,
            height + 1,
            f'{height:.1f}h',
            ha='center',
            va='bottom',
            fontsize=12,
            fontweight='bold'
        )
    plt.tight_layout()
    plt.savefig(outputDir / 'defense_mechanism_resolution_time.png', dpi=300, bbox_inches='tight')
    plt.close()
    plt.figure(figsize=(12, 7))
    defenseFinancialData = df.groupby('Defense Mechanism Used')['Financial Loss (in Million $)'].mean().sort_values()
    barColors = sns.color_palette("magma", len(defenseFinancialData))
    bars = plt.bar(
        defenseFinancialData.index,
        defenseFinancialData.values,
        color=barColors,
        width=0.6,
        edgecolor='black',
        linewidth=1
    )
    plt.title('Average Financial Loss by Defense Mechanism', fontsize=16, fontweight='bold')
    plt.xlabel('Defense Mechanism', fontsize=14)
    plt.ylabel('Average Financial Loss (Million $)', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width()/2.,
            height + 1,
            f'${height:.1f}M',
            ha='center',
            va='bottom',
            fontsize=12,
            fontweight='bold'
        )
    plt.tight_layout()
    plt.savefig(outputDir / 'defense_mechanism_financial_loss.png', dpi=300, bbox_inches='tight')
    plt.close()
    plt.figure(figsize=(12, 7))
    defenseStats = df.groupby('Defense Mechanism Used').agg({
        'Incident Resolution Time (in Hours)': 'mean',
        'Financial Loss (in Million $)': 'mean'
    }).reset_index()
    maxResolutionTime = defenseStats['Incident Resolution Time (in Hours)'].max()
    maxFinancialLoss = defenseStats['Financial Loss (in Million $)'].max()
    defenseStats['NormalizedTime'] = 1 - (defenseStats['Incident Resolution Time (in Hours)'] / maxResolutionTime)
    defenseStats['NormalizedLoss'] = 1 - (defenseStats['Financial Loss (in Million $)'] / maxFinancialLoss)
    defenseStats['EffectivenessScore'] = (defenseStats['NormalizedTime'] * 0.5 +
                                         defenseStats['NormalizedLoss'] * 0.5) * 100
    defenseStats = defenseStats.sort_values('EffectivenessScore', ascending=False)
    scoreColors = plt.cm.RdYlGn(defenseStats['EffectivenessScore']/100)
    bars = plt.barh(
        defenseStats['Defense Mechanism Used'],
        defenseStats['EffectivenessScore'],
        color=scoreColors,
        edgecolor='black',
        linewidth=1,
        height=0.6
    )
    plt.title('Defense Mechanism Effectiveness Ranking', fontsize=16, fontweight='bold')
    plt.xlabel('Effectiveness Score (0-100)', fontsize=14)
    plt.xlim(0, 100)
    plt.grid(axis='x', alpha=0.3)
    for i, bar in enumerate(bars):
        width = bar.get_width()
        plt.text(
            width + 1,
            bar.get_y() + bar.get_height()/2,
            f'{width:.1f}',
            va='center',
            fontsize=12,
            fontweight='bold'
        )
    plt.figtext(
        0.5,
        0.01,
        "Higher score = Better defense mechanism (based on resolution time and financial loss)",
        ha='center',
        fontsize=12,
        style='italic'
    )
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    plt.savefig(outputDir / 'defense_mechanism_ranking.png', dpi=300, bbox_inches='tight')
    plt.close()
    plt.figure(figsize=(14, 8))
    pivotData = pd.pivot_table(
        data=df,
        values='Incident Resolution Time (in Hours)',
        index='Defense Mechanism Used',
        columns='Attack Type',
        aggfunc='mean'
    )
    ax = sns.heatmap(
        pivotData,
        annot=True,
        fmt='.1f',
        cmap='YlGnBu_r',
        linewidths=0.5,
        cbar_kws={'label': 'Resolution Time (Hours)'}
    )
    plt.title('Defense Mechanism Effectiveness Against Different Attack Types', fontsize=16, fontweight='bold')
    plt.ylabel('Defense Mechanism', fontsize=14)
    plt.xlabel('Attack Type', fontsize=14)
    plt.tight_layout()
    plt.savefig(outputDir / 'defense_vs_attack_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Improved defense mechanism visualizations created successfully!")
if __name__ == "__main__":
    create_defense_mechanism_visualizations()