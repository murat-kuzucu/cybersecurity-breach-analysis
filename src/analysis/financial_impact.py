import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import os
def analyze_financial_impact():
    print("Starting financial impact analysis...")
    outputDir = Path('analysis/output')
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
    plt.figure(figsize=(12, 8))
    industryImpact = df.groupby('Target Industry Standardized')['Financial Loss (in Million $)'].mean().sort_values(ascending=False)
    ax = sns.barplot(x=industryImpact.index, y=industryImpact.values, palette='viridis')
    plt.title('Average Financial Loss by Industry', fontsize=16, pad=20)
    plt.xlabel('Industry', fontsize=14)
    plt.ylabel('Average Financial Loss (Million $)', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    for i, v in enumerate(industryImpact.values):
        ax.text(i, v + 1, f'{v:.2f}', ha='center', fontsize=10)
    plt.savefig(outputDir / 'financial_impact_by_industry.png', dpi=300, bbox_inches='tight')
    plt.close()
    plt.figure(figsize=(14, 8))
    attackImpact = df.groupby('Attack Type Detailed')['Financial Loss (in Million $)'].mean().sort_values(ascending=False)
    ax = sns.barplot(x=attackImpact.index, y=attackImpact.values, palette='magma')
    plt.title('Average Financial Loss by Attack Type', fontsize=16, pad=20)
    plt.xlabel('Attack Type', fontsize=14)
    plt.ylabel('Average Financial Loss (Million $)', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    for i, v in enumerate(attackImpact.values):
        ax.text(i, v + 1, f'{v:.2f}', ha='center', fontsize=10)
    plt.savefig(outputDir / 'financial_impact_by_attack.png', dpi=300, bbox_inches='tight')
    plt.close()
    plt.figure(figsize=(10, 8))
    sns.violinplot(data=df, x='Target Industry Standardized', y='Financial Loss (in Million $)', palette='muted')
    plt.title('Financial Loss Distribution by Industry', fontsize=16, pad=20)
    plt.xlabel('Industry', fontsize=14)
    plt.ylabel('Financial Loss (Million $)', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(outputDir / 'financial_impact_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    plt.figure(figsize=(16, 10))
    heatmapData = df.pivot_table(
        values='Financial Loss (in Million $)',
        index='Target Industry Standardized',
        columns='Attack Type',
        aggfunc='mean'
    )
    sns.heatmap(heatmapData, annot=True, cmap='YlOrRd', fmt='.2f', linewidths=.5)
    plt.title('Average Financial Loss by Industry and Attack Type (Million $)', fontsize=16, pad=20)
    plt.tight_layout()
    plt.savefig(outputDir / 'financial_impact_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    plt.figure(figsize=(14, 8))
    yearlyImpact = df.groupby(['Year', 'Target Industry Standardized'])['Financial Loss (in Million $)'].mean().reset_index()
    sns.lineplot(data=yearlyImpact, x='Year', y='Financial Loss (in Million $)',
                hue='Target Industry Standardized', marker='o', linewidth=2.5)
    plt.title('Financial Loss Trends by Industry (2015-2024)', fontsize=16, pad=20)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Average Financial Loss (Million $)', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(title='Industry', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(outputDir / 'financial_impact_trends.png', dpi=300, bbox_inches='tight')
    plt.close()
    plt.figure(figsize=(12, 8))
    vulnerabilityImpact = df.groupby('Security Vulnerability Type')['Financial Loss (in Million $)'].mean().sort_values(ascending=False)
    ax = sns.barplot(x=vulnerabilityImpact.index, y=vulnerabilityImpact.values, palette='crest')
    plt.title('Average Financial Loss by Security Vulnerability Type', fontsize=16, pad=20)
    plt.xlabel('Vulnerability Type', fontsize=14)
    plt.ylabel('Average Financial Loss (Million $)', fontsize=14)
    plt.tight_layout()
    for i, v in enumerate(vulnerabilityImpact.values):
        ax.text(i, v + 1, f'{v:.2f}', ha='center', fontsize=10)
    plt.savefig(outputDir / 'financial_impact_by_vulnerability.png', dpi=300, bbox_inches='tight')
    plt.close()
    with open(outputDir / 'financial_impact_summary.md', 'w') as f:
        f.write("
        f.write(f"
        f.write(f"- Total financial loss: ${df['Financial Loss (in Million $)'].sum():.2f} million\n")
        f.write(f"- Average financial loss per incident: ${df['Financial Loss (in Million $)'].mean():.2f} million\n")
        f.write(f"- Maximum financial loss: ${df['Financial Loss (in Million $)'].max():.2f} million\n\n")
        f.write("
        for industry, loss in industryImpact.head(3).items():
            f.write(f"- {industry}: ${loss:.2f} million\n")
        f.write("\n")
        f.write("
        for attack, loss in attackImpact.head(3).items():
            f.write(f"- {attack}: ${loss:.2f} million\n")
        f.write("\n")
        f.write("
        for vuln, loss in vulnerabilityImpact.head(3).items():
            f.write(f"- {vuln}: ${loss:.2f} million\n")
    print("Financial impact analysis completed successfully!")
if __name__ == "__main__":
    analyze_financial_impact()