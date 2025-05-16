import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import os

def analyze_attack_patterns():
    """
    Analyzes attack patterns in cybersecurity breaches and creates visualizations.
    Uses snake_case for function names and camelCase for variable names.
    """
    print("Starting attack patterns analysis...")
    
    # Create output directory if it doesn't exist
    outputDir = Path('analysis/output')
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
    
    # 1. Attack Type Distribution
    plt.figure(figsize=(12, 8))
    attackCounts = df['Attack Type Detailed'].value_counts()
    explode = [0.1 if i == 0 else 0.05 if i == 1 else 0 for i in range(len(attackCounts))]
    
    # Create pie chart
    plt.pie(attackCounts, labels=attackCounts.index, autopct='%1.1f%%', 
            startangle=90, explode=explode, shadow=True, textprops={'fontsize': 12})
    plt.title('Distribution of Attack Types', fontsize=16, pad=20)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.tight_layout()
    
    # Save the figure
    plt.savefig(outputDir / 'attack_type_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Attack Type Evolution Over Time
    plt.figure(figsize=(14, 10))
    # Group by year and attack type and count
    yearlyAttacks = df.groupby(['Year', 'Attack Type'])['Attack Source'].count().unstack()
    
    # Normalize to percentage
    yearlyAttacksPercent = yearlyAttacks.div(yearlyAttacks.sum(axis=1), axis=0) * 100
    
    # Create stacked area chart
    yearlyAttacksPercent.plot(kind='area', stacked=True, alpha=0.7, figsize=(14, 10), colormap='viridis')
    plt.title('Evolution of Attack Types Over Time (% of Total)', fontsize=16, pad=20)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Percentage of Attacks', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(title='Attack Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    # Save the figure
    plt.savefig(outputDir / 'attack_evolution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Attack Source Distribution
    plt.figure(figsize=(10, 8))
    sourceCounts = df['Attack Source'].value_counts()
    
    # Create bar chart
    ax = sns.barplot(x=sourceCounts.index, y=sourceCounts.values, palette='Set3')
    plt.title('Distribution of Attack Sources', fontsize=16, pad=20)
    plt.xlabel('Attack Source', fontsize=14)
    plt.ylabel('Number of Incidents', fontsize=14)
    plt.tight_layout()
    
    # Add value labels
    for i, v in enumerate(sourceCounts.values):
        ax.text(i, v + 20, str(v), ha='center', fontsize=10)
    
    # Save the figure
    plt.savefig(outputDir / 'attack_source_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. Heatmap of Attack Types by Source
    plt.figure(figsize=(12, 8))
    # Create contingency table
    attackSourceTable = pd.crosstab(df['Attack Type'], df['Attack Source'])
    
    # Create heatmap
    sns.heatmap(attackSourceTable, annot=True, cmap='Blues', fmt='d', linewidths=.5)
    plt.title('Relationship Between Attack Types and Sources', fontsize=16, pad=20)
    plt.tight_layout()
    
    # Save the figure
    plt.savefig(outputDir / 'attack_type_by_source.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 5. Attack Type by Industry
    plt.figure(figsize=(16, 10))
    # Create contingency table
    industryAttackTable = pd.crosstab(df['Target Industry Standardized'], df['Attack Type'])
    
    # Convert to percentages
    industryAttackTablePct = industryAttackTable.div(industryAttackTable.sum(axis=1), axis=0) * 100
    
    # Create heatmap
    sns.heatmap(industryAttackTablePct, annot=True, cmap='YlGnBu', fmt='.1f', linewidths=.5)
    plt.title('Attack Type Distribution by Industry (%)', fontsize=16, pad=20)
    plt.tight_layout()
    
    # Save the figure
    plt.savefig(outputDir / 'attack_type_by_industry.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 6. Geographic Distribution of Attacks 
    plt.figure(figsize=(14, 8))
    countryAttacks = df['Country'].value_counts().head(10)
    
    # Create horizontal bar chart
    ax = sns.barplot(y=countryAttacks.index, x=countryAttacks.values, palette='crest')
    plt.title('Top 10 Countries by Number of Cybersecurity Incidents', fontsize=16, pad=20)
    plt.xlabel('Number of Incidents', fontsize=14)
    plt.ylabel('Country', fontsize=14)
    plt.tight_layout()
    
    # Add value labels
    for i, v in enumerate(countryAttacks.values):
        ax.text(v + 10, i, str(v), va='center', fontsize=10)
    
    # Save the figure
    plt.savefig(outputDir / 'geographic_attack_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 7. Average Number of Affected Users by Attack Type
    plt.figure(figsize=(12, 8))
    usersImpact = df.groupby('Attack Type')['Number of Affected Users'].mean().sort_values(ascending=False)
    
    # Create bar chart
    ax = sns.barplot(x=usersImpact.index, y=usersImpact.values, palette='rocket')
    plt.title('Average Number of Affected Users by Attack Type', fontsize=16, pad=20)
    plt.xlabel('Attack Type', fontsize=14)
    plt.ylabel('Average Number of Affected Users', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Format y-axis with thousands separator
    from matplotlib.ticker import FuncFormatter
    def thousands_formatter(x, pos):
        return f'{int(x):,}'
    ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))
    
    # Add value labels
    for i, v in enumerate(usersImpact.values):
        ax.text(i, v + 20000, f'{int(v):,}', ha='center', fontsize=9, rotation=45)
    
    # Save the figure
    plt.savefig(outputDir / 'affected_users_by_attack.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Generate summary report
    with open(outputDir / 'attack_patterns_summary.md', 'w') as f:
        f.write("# Attack Patterns Analysis Summary\n\n")
        
        f.write("## Most Common Attack Types\n")
        for attack, count in attackCounts.head(3).items():
            f.write(f"- {attack}: {count} incidents ({count/len(df)*100:.1f}%)\n")
        f.write("\n")
        
        f.write("## Most Common Attack Sources\n")
        for source, count in sourceCounts.head(3).items():
            f.write(f"- {source}: {count} incidents ({count/len(df)*100:.1f}%)\n")
        f.write("\n")
        
        f.write("## Most Targeted Countries\n")
        for country, count in countryAttacks.head(3).items():
            f.write(f"- {country}: {count} incidents ({count/len(df)*100:.1f}%)\n")
        f.write("\n")
        
        f.write("## Attack Types with Highest User Impact\n")
        for attack, users in usersImpact.head(3).items():
            f.write(f"- {attack}: {int(users):,} average affected users\n")
    
    print("Attack patterns analysis completed successfully!")

if __name__ == "__main__":
    analyze_attack_patterns()
