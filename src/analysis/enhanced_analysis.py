import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import os
import shutil
from datetime import datetime
def generate_enhanced_analysis():
    print("Generating enhanced analysis visualizations...")
    outputDir = Path('../../output/visualizations')
    dashboardDir = Path('../../output/dashboard')
    outputDir.mkdir(exist_ok=True, parents=True)
    dashboardDir.mkdir(exist_ok=True, parents=True)
    possiblePaths = [
        Path('../../data/cybersecurity_breach_data.csv'),
        Path('data/cybersecurity_breach_data.csv'),
        Path('../data/cybersecurity_breach_data.csv')
    ]
    df = None
    for dataPath in possiblePaths:
        try:
            df = pd.read_csv(dataPath)
            print(f"Loaded data with {len(df)} records from {dataPath}")
            break
        except Exception:
            continue
    if df is None:
        print(f"Error: Could not load data from any of the possible paths")
        return
    generate_financial_analysis(df, outputDir)
    generate_attack_analysis(df, outputDir)
    generate_vulnerability_analysis(df, outputDir)
    generate_correlation_analysis(df, outputDir)
    generate_trend_analysis(df, outputDir)
    create_pure_analysis_dashboard(outputDir, dashboardDir)
    dashboardPath = os.path.join('output', 'dashboard', 'index.html')
    print(f"Enhanced analysis completed. Dashboard available at {dashboardPath}")
def generate_financial_analysis(df, outputDir):
    print("Generating financial impact analysis...")
    sns.set_style("whitegrid")
    plt.rcParams['font.family'] = 'sans-serif'
    plt.figure(figsize=(12, 8))
    industryImpact = df.groupby('Target Industry Standardized')['Financial Loss (in Million $)'].mean().sort_values()
    sns.barplot(y=industryImpact.index, x=industryImpact.values, hue=industryImpact.index, palette='viridis', legend=False)
    plt.title('Average Financial Loss by Industry', fontsize=16)
    plt.xlabel('Average Financial Loss (Million $)', fontsize=14)
    plt.ylabel('Industry', fontsize=14)
    plt.tight_layout()
    plt.savefig(outputDir / 'financial_impact_by_industry.png', dpi=300, bbox_inches='tight')
    plt.close()
    plt.figure(figsize=(14, 8))
    sns.boxplot(data=df, x='Target Industry Standardized', y='Financial Loss (in Million $)',
              hue='Target Industry Standardized', palette='muted', legend=False)
    plt.title('Financial Loss Distribution by Industry', fontsize=16)
    plt.xlabel('Industry', fontsize=14)
    plt.ylabel('Financial Loss (Million $)', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(outputDir / 'financial_loss_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    plt.figure(figsize=(16, 10))
    heatmapData = df.pivot_table(
        values='Financial Loss (in Million $)',
        index='Target Industry Standardized',
        columns='Attack Type',
        aggfunc='mean'
    )
    sns.heatmap(heatmapData, annot=True, cmap='YlOrRd', fmt='.2f', linewidths=.5)
    plt.title('Average Financial Loss by Industry and Attack Type (Million $)', fontsize=16)
    plt.tight_layout()
    plt.savefig(outputDir / 'financial_impact_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    plt.figure(figsize=(12, 8))
    sns.scatterplot(
        data=df,
        x='Number of Affected Users',
        y='Financial Loss (in Million $)',
        hue='Attack Type',
        size='Incident Resolution Time (in Hours)',
        sizes=(20, 200),
        alpha=0.7
    )
    plt.title('Financial Loss vs. Number of Affected Users', fontsize=16)
    plt.xlabel('Number of Affected Users', fontsize=14)
    plt.ylabel('Financial Loss (Million $)', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(outputDir / 'financial_loss_vs_users.png', dpi=300, bbox_inches='tight')
    plt.close()
def generate_attack_analysis(df, outputDir):
    print("Generating attack pattern analysis...")
    sns.set_style("whitegrid")
    plt.rcParams['font.family'] = 'sans-serif'
    plt.figure(figsize=(12, 10))
    attackCounts = df['Attack Type'].value_counts()
    explode = [0.1 if i == 0 else 0.05 if i == 1 else 0 for i in range(len(attackCounts))]
    plt.pie(attackCounts, labels=attackCounts.index, autopct='%1.1f%%',
            startangle=90, explode=explode, shadow=True, textprops={'fontsize': 12})
    plt.title('Distribution of Attack Types', fontsize=16)
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig(outputDir / 'attack_type_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    plt.figure(figsize=(14, 10))
    attackSourceCross = pd.crosstab(df['Attack Type'], df['Attack Source'])
    attackSourcePct = attackSourceCross.div(attackSourceCross.sum(axis=1), axis=0) * 100
    attackSourcePct.plot(kind='bar', stacked=True, figsize=(14, 8), colormap='tab20')
    plt.title('Attack Sources by Attack Type (%)', fontsize=16)
    plt.xlabel('Attack Type', fontsize=14)
    plt.ylabel('Percentage', fontsize=14)
    plt.legend(title='Attack Source', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(outputDir / 'attack_source_by_type.png', dpi=300, bbox_inches='tight')
    plt.close()
    plt.figure(figsize=(16, 10))
    industryAttackTable = pd.crosstab(df['Target Industry Standardized'], df['Attack Type'])
    industryAttackTablePct = industryAttackTable.div(industryAttackTable.sum(axis=1), axis=0) * 100
    sns.heatmap(industryAttackTablePct, annot=True, cmap='YlGnBu', fmt='.1f', linewidths=.5)
    plt.title('Attack Type Distribution by Industry (%)', fontsize=16)
    plt.tight_layout()
    plt.savefig(outputDir / 'attack_type_by_industry.png', dpi=300, bbox_inches='tight')
    plt.close()
    plt.figure(figsize=(14, 10))
    countryAttacks = df['Country'].value_counts()
    sns.barplot(y=countryAttacks.index[:10], x=countryAttacks.values[:10],
              hue=countryAttacks.index[:10], palette='crest', legend=False)
    plt.title('Top 10 Countries by Number of Cybersecurity Incidents', fontsize=16)
    plt.xlabel('Number of Incidents', fontsize=14)
    plt.ylabel('Country', fontsize=14)
    plt.tight_layout()
    plt.savefig(outputDir / 'geographic_attack_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
def generate_vulnerability_analysis(df, outputDir):
    print("Generating vulnerability and resolution time analysis...")
    sns.set_style("whitegrid")
    plt.rcParams['font.family'] = 'sans-serif'
    plt.figure(figsize=(16, 10))
    resTimeByIndVuln = df.groupby(['Target Industry Standardized', 'Security Vulnerability Type'])['Incident Resolution Time (in Hours)'].mean().reset_index()
    g = sns.catplot(
        data=resTimeByIndVuln,
        kind="bar",
        x="Target Industry Standardized",
        y="Incident Resolution Time (in Hours)",
        hue="Security Vulnerability Type",
        palette="dark",
        alpha=.6,
        height=8,
        aspect=2
    )
    g.set_xticklabels(rotation=45, ha="right")
    g.fig.suptitle('Average Resolution Time by Industry and Vulnerability Type', fontsize=16, y=1.02)
    g.set_axis_labels("Industry", "Resolution Time (Hours)")
    plt.savefig(outputDir / 'resolution_by_industry_vulnerability.png', dpi=300, bbox_inches='tight')
    plt.close()
    plt.figure(figsize=(12, 8))
    vulnCounts = df['Security Vulnerability Type'].value_counts()
    plt.pie(vulnCounts, labels=vulnCounts.index, autopct='%1.1f%%',
            startangle=90, wedgeprops=dict(width=0.5), textprops={'fontsize': 12})
    plt.title('Distribution of Security Vulnerabilities', fontsize=16)
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig(outputDir / 'vulnerability_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    plt.figure(figsize=(12, 8))
    vulnGroup = df.groupby('Security Vulnerability Type').agg({
        'Incident Resolution Time (in Hours)': 'mean',
        'Financial Loss (in Million $)': 'mean',
        'Number of Affected Users': 'mean'
    }).reset_index()
    sns.scatterplot(
        data=vulnGroup,
        x='Incident Resolution Time (in Hours)',
        y='Financial Loss (in Million $)',
        size='Number of Affected Users',
        hue='Security Vulnerability Type',
        sizes=(100, 2000),
        alpha=0.7
    )
    plt.title('Resolution Time vs. Financial Loss by Vulnerability Type', fontsize=16)
    plt.xlabel('Average Resolution Time (Hours)', fontsize=14)
    plt.ylabel('Average Financial Loss (Million $)', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(outputDir / 'resolution_vs_loss_by_vulnerability.png', dpi=300, bbox_inches='tight')
    plt.close()
    plt.figure(figsize=(14, 8))
    sns.violinplot(data=df, x='Defense Mechanism Used', y='Incident Resolution Time (in Hours)',
                  hue='Defense Mechanism Used', palette='muted', legend=False)
    plt.title('Resolution Time Distribution by Defense Mechanism', fontsize=16)
    plt.xlabel('Defense Mechanism', fontsize=14)
    plt.ylabel('Resolution Time (Hours)', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(outputDir / 'defense_mechanism_effectiveness.png', dpi=300, bbox_inches='tight')
    plt.close()
def generate_correlation_analysis(df, outputDir):
    print("Generating correlation analysis...")
    sns.set_style("whitegrid")
    plt.rcParams['font.family'] = 'sans-serif'
    plt.figure(figsize=(12, 10))
    numericColumns = df.select_dtypes(include=[np.number]).columns
    corr = df[numericColumns].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
                square=True, linewidths=.5, annot=True, fmt='.2f')
    plt.title('Correlation Matrix of Numeric Variables', fontsize=16)
    plt.tight_layout()
    plt.savefig(outputDir / 'correlation_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()
    plt.figure(figsize=(12, 8))
    plt.hexbin(df['Incident Resolution Time (in Hours)'],
               df['Financial Loss (in Million $)'],
               gridsize=30, cmap='viridis', mincnt=1)
    plt.colorbar(label='Count')
    plt.title('Resolution Time vs. Financial Loss', fontsize=16)
    plt.xlabel('Resolution Time (Hours)', fontsize=14)
    plt.ylabel('Financial Loss (Million $)', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(outputDir / 'resolution_vs_loss_hexbin.png', dpi=300, bbox_inches='tight')
    plt.close()
    plt.figure(figsize=(16, 12))
    g = sns.FacetGrid(df, col="Attack Source", row="Security Vulnerability Type",
                    height=5, aspect=1.2, sharey=False)
    g.map_dataframe(sns.histplot, x="Financial Loss (in Million $)", bins=20, kde=True)
    g.set_axis_labels("Financial Loss (Million $)", "Count")
    g.set_titles(col_template="{col_name}", row_template="{row_name}")
    g.fig.suptitle('Financial Loss Distribution by Attack Source and Vulnerability Type',
                 fontsize=16, y=1.02)
    g.tight_layout()
    plt.savefig(outputDir / 'loss_by_source_vulnerability.png', dpi=300, bbox_inches='tight')
    plt.close()
    plt.figure(figsize=(12, 8))
    sns.scatterplot(
        data=df,
        x='Number of Affected Users',
        y='Incident Resolution Time (in Hours)',
        hue='Attack Type',
        style='Attack Source',
        alpha=0.7
    )
    plt.title('Affected Users vs. Resolution Time by Attack Type', fontsize=16)
    plt.xlabel('Number of Affected Users', fontsize=14)
    plt.ylabel('Resolution Time (Hours)', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(outputDir / 'users_vs_resolution.png', dpi=300, bbox_inches='tight')
    plt.close()
def generate_trend_analysis(df, outputDir):
    print("Generating trend analysis...")
    sns.set_style("whitegrid")
    plt.rcParams['font.family'] = 'sans-serif'
    plt.figure(figsize=(14, 8))
    yearlyAttacks = df.groupby(['Year', 'Attack Type']).size().unstack()
    yearlyAttacks.plot(marker='o', linewidth=2.5)
    plt.title('Evolution of Attack Types Over Time', fontsize=16)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Number of Incidents', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(title='Attack Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(outputDir / 'attack_evolution.png', dpi=300, bbox_inches='tight')
    plt.close()
    plt.figure(figsize=(14, 8))
    yearlyLossByIndustry = df.groupby(['Year', 'Target Industry Standardized'])['Financial Loss (in Million $)'].mean().reset_index()
    sns.lineplot(
        data=yearlyLossByIndustry,
        x='Year',
        y='Financial Loss (in Million $)',
        hue='Target Industry Standardized',
        marker='o',
        linewidth=2.5
    )
    plt.title('Financial Loss Trends by Industry', fontsize=16)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Average Financial Loss (Million $)', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(title='Industry', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(outputDir / 'financial_loss_trends.png', dpi=300, bbox_inches='tight')
    plt.close()
    plt.figure(figsize=(14, 8))
    yearlyResolutionByAttack = df.groupby(['Year', 'Attack Type'])['Incident Resolution Time (in Hours)'].mean().reset_index()
    sns.lineplot(
        data=yearlyResolutionByAttack,
        x='Year',
        y='Incident Resolution Time (in Hours)',
        hue='Attack Type',
        marker='o',
        linewidth=2.5
    )
    plt.title('Resolution Time Trends by Attack Type', fontsize=16)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Average Resolution Time (Hours)', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(title='Attack Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(outputDir / 'resolution_time_trends.png', dpi=300, bbox_inches='tight')
    plt.close()
    plt.figure(figsize=(14, 8))
    yearlyVulnerabilities = df.groupby(['Year', 'Security Vulnerability Type']).size().unstack()
    yearlyVulnerabilities.plot(marker='o', linewidth=2.5)
    plt.title('Vulnerability Exploitation Trends', fontsize=16)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Number of Incidents', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(title='Vulnerability Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(outputDir / 'vulnerability_trends.png', dpi=300, bbox_inches='tight')
    plt.close()
def create_pure_analysis_dashboard(vizDir, dashboardDir):
    from src.dashboard.html_generator import generate_dashboard_html
    visualizationFiles = [f for f in os.listdir(vizDir) if f.endswith('.png')]
    financialViz = [f for f in visualizationFiles if 'financial' in f.lower() or 'loss' in f.lower()]
    attackViz = [f for f in visualizationFiles if 'attack' in f.lower() or 'geographic' in f.lower()]
    vulnerabilityViz = [f for f in visualizationFiles if 'vulnerability' in f.lower() or 'resolution' in f.lower() or 'defense' in f.lower()]
    correlationViz = [f for f in visualizationFiles if 'correlation' in f.lower() or 'vs' in f.lower()]
    trendViz = [f for f in visualizationFiles if 'trend' in f.lower() or 'evolution' in f.lower() or 'over_time' in f.lower()]
    generate_dashboard_html(vizDir, dashboardDir, financialViz, attackViz, vulnerabilityViz, correlationViz, trendViz)
    print(f"Analytics dashboard created at {dashboardDir}/index.html")
if __name__ == "__main__":
    generate_enhanced_analysis()