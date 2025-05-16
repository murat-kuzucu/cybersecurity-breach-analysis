import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Set style
plt.style.use('ggplot')
sns.set_palette("Set2")

# Load the dataset
filePath = Path('dataset-onExcel.xlsx')
dataFrame = pd.read_excel(filePath)

# Create output directory if it doesn't exist
outputDir = Path('analysis_results')
outputDir.mkdir(exist_ok=True)

# Basic statistics and data cleaning
def clean_and_explore_data(df):
    """Clean data and print basic statistics"""
    # Make a copy to avoid modifying original
    dataCopy = df.copy()
    
    # Check for missing values
    missingValues = dataCopy.isnull().sum()
    
    # Basic statistics
    numericStats = dataCopy.describe()
    
    # Count of attacks by type
    attackCounts = dataCopy['Attack Type'].value_counts()
    
    # Count of attacks by year
    yearCounts = dataCopy['Year'].value_counts().sort_index()
    
    # Save results
    with open(outputDir / 'data_summary.txt', 'w') as f:
        f.write("=== CYBERSECURITY BREACH DATA ANALYSIS ===\n\n")
        f.write(f"Total records: {len(dataCopy)}\n")
        f.write(f"Date range: {dataCopy['Year'].min()} - {dataCopy['Year'].max()}\n")
        f.write(f"Countries included: {', '.join(sorted(dataCopy['Country'].unique()))}\n\n")
        
        f.write("=== MISSING VALUES ===\n")
        f.write(missingValues.to_string())
        f.write("\n\n=== NUMERIC STATISTICS ===\n")
        f.write(numericStats.to_string())
        
        f.write("\n\n=== ATTACK TYPE DISTRIBUTION ===\n")
        f.write(attackCounts.to_string())
        
        f.write("\n\n=== YEARLY ATTACK DISTRIBUTION ===\n")
        f.write(yearCounts.to_string())
    
    return dataCopy

# Analysis 1: Financial losses by industry over time
def analyze_financial_losses(df):
    """Analyze financial losses by industry and over time"""
    # Average financial loss by industry
    industryLoss = df.groupby('Target Industry')['Financial Loss (in Million $)'].agg(['mean', 'sum']).sort_values('sum', ascending=False)
    
    # Financial loss trend over time
    yearlyLoss = df.groupby('Year')['Financial Loss (in Million $)'].mean()
    
    # Financial loss by industry over time (for top 5 industries)
    topIndustries = industryLoss.nlargest(5, 'sum').index
    industryTimeTrend = df[df['Target Industry'].isin(topIndustries)].groupby(['Year', 'Target Industry'])['Financial Loss (in Million $)'].mean().unstack()
    
    # Plot average financial loss by industry
    plt.figure(figsize=(12, 6))
    industryLoss['mean'].sort_values().plot(kind='barh', color='crimson')
    plt.title('Average Financial Loss by Industry (Million $)', fontsize=14)
    plt.xlabel('Average Loss (Million $)')
    plt.tight_layout()
    plt.savefig(outputDir / 'avg_loss_by_industry.png', dpi=300)
    
    # Plot financial loss trend over time
    plt.figure(figsize=(12, 6))
    yearlyLoss.plot(marker='o', linestyle='-', linewidth=2, color='darkblue')
    plt.title('Average Financial Loss Over Time', fontsize=14)
    plt.xlabel('Year')
    plt.ylabel('Average Loss (Million $)')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(outputDir / 'loss_trend_over_time.png', dpi=300)
    
    # Plot industry trends over time
    plt.figure(figsize=(14, 7))
    industryTimeTrend.plot(marker='o')
    plt.title('Financial Loss Trends by Top Industries', fontsize=14)
    plt.xlabel('Year')
    plt.ylabel('Average Loss (Million $)')
    plt.grid(True)
    plt.legend(title='Industry')
    plt.tight_layout()
    plt.savefig(outputDir / 'industry_loss_trends.png', dpi=300)
    
    # Save results
    with open(outputDir / 'financial_analysis.txt', 'w') as f:
        f.write("=== FINANCIAL LOSS ANALYSIS ===\n\n")
        f.write("Financial Loss by Industry:\n")
        f.write(industryLoss.to_string())
        f.write("\n\nFinancial Loss Trend Over Time:\n")
        f.write(yearlyLoss.to_string())

# Analysis 2: Attack types and resolution times
def analyze_attack_resolution(df):
    """Analyze relationship between attack types and resolution times"""
    # Average resolution time by attack type
    attackResolution = df.groupby('Attack Type')['Incident Resolution Time (in Hours)'].agg(['mean', 'median', 'count']).sort_values('mean', ascending=False)
    
    # Resolution time by country
    countryResolution = df.groupby('Country')['Incident Resolution Time (in Hours)'].mean().sort_values(ascending=False)
    
    # Resolution time vs. financial loss
    plt.figure(figsize=(10, 8))
    sns.scatterplot(data=df, x='Incident Resolution Time (in Hours)', y='Financial Loss (in Million $)', 
                   hue='Attack Type', size='Number of Affected Users', sizes=(20, 500), alpha=0.7)
    plt.title('Resolution Time vs. Financial Loss by Attack Type', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(outputDir / 'resolution_vs_loss.png', dpi=300)
    
    # Average resolution time by attack type
    plt.figure(figsize=(12, 6))
    attackResolution['mean'].sort_values().plot(kind='barh', color='teal')
    plt.title('Average Resolution Time by Attack Type (Hours)', fontsize=14)
    plt.xlabel('Hours')
    plt.tight_layout()
    plt.savefig(outputDir / 'avg_resolution_by_attack.png', dpi=300)
    
    # Resolution time distribution
    plt.figure(figsize=(14, 6))
    sns.boxplot(data=df, x='Attack Type', y='Incident Resolution Time (in Hours)')
    plt.title('Resolution Time Distribution by Attack Type', fontsize=14)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(outputDir / 'resolution_boxplot.png', dpi=300)
    
    # Save results
    with open(outputDir / 'resolution_analysis.txt', 'w') as f:
        f.write("=== INCIDENT RESOLUTION ANALYSIS ===\n\n")
        f.write("Resolution Time by Attack Type:\n")
        f.write(attackResolution.to_string())
        f.write("\n\nResolution Time by Country:\n")
        f.write(countryResolution.to_string())

# Analysis 3: Security vulnerabilities and financial impact
def analyze_vulnerabilities(df):
    """Analyze security vulnerabilities and their financial impact"""
    # Financial loss by vulnerability type
    vulnLoss = df.groupby('Security Vulnerability Type')['Financial Loss (in Million $)'].agg(['mean', 'sum', 'count']).sort_values('sum', ascending=False)
    
    # Users affected by vulnerability type
    vulnUsers = df.groupby('Security Vulnerability Type')['Number of Affected Users'].agg(['mean', 'sum']).sort_values('sum', ascending=False)
    
    # Effectiveness of defense mechanisms
    defenseLoss = df.groupby('Defense Mechanism Used')['Financial Loss (in Million $)'].mean().sort_values()
    defenseTime = df.groupby('Defense Mechanism Used')['Incident Resolution Time (in Hours)'].mean().sort_values()
    
    # Plot financial loss by vulnerability
    plt.figure(figsize=(12, 6))
    vulnLoss['mean'].sort_values().plot(kind='barh', color='darkred')
    plt.title('Average Financial Loss by Vulnerability Type (Million $)', fontsize=14)
    plt.xlabel('Average Loss (Million $)')
    plt.tight_layout()
    plt.savefig(outputDir / 'loss_by_vulnerability.png', dpi=300)
    
    # Plot defense mechanism effectiveness
    plt.figure(figsize=(12, 6))
    ax = defenseLoss.plot(kind='bar', color='darkgreen', alpha=0.7)
    plt.title('Average Financial Loss by Defense Mechanism', fontsize=14)
    plt.xticks(rotation=45)
    plt.ylabel('Average Loss (Million $)')
    plt.tight_layout()
    plt.savefig(outputDir / 'loss_by_defense.png', dpi=300)
    
    # Plot resolution time by defense
    plt.figure(figsize=(12, 6))
    defenseTime.plot(kind='bar', color='navy', alpha=0.7)
    plt.title('Average Resolution Time by Defense Mechanism', fontsize=14)
    plt.xticks(rotation=45)
    plt.ylabel('Hours')
    plt.tight_layout()
    plt.savefig(outputDir / 'time_by_defense.png', dpi=300)
    
    # Save results
    with open(outputDir / 'vulnerability_analysis.txt', 'w') as f:
        f.write("=== SECURITY VULNERABILITY ANALYSIS ===\n\n")
        f.write("Financial Loss by Vulnerability Type:\n")
        f.write(vulnLoss.to_string())
        f.write("\n\nUsers Affected by Vulnerability Type:\n")
        f.write(vulnUsers.to_string())
        f.write("\n\nDefense Mechanism Effectiveness (Avg Loss):\n")
        f.write(defenseLoss.to_string())
        f.write("\n\nDefense Mechanism Effectiveness (Avg Resolution Time):\n")
        f.write(defenseTime.to_string())

# Analysis 4: Attack sources and patterns
def analyze_attack_sources(df):
    """Analyze attack sources and patterns"""
    # Attack source distribution
    sourceCounts = df['Attack Source'].value_counts()
    
    # Attack source by country
    sourceByCountry = pd.crosstab(df['Country'], df['Attack Source'])
    
    # Attack type by source
    typeBySource = pd.crosstab(df['Attack Source'], df['Attack Type'])
    
    # Plot attack source distribution
    plt.figure(figsize=(10, 6))
    sourceCounts.plot(kind='pie', autopct='%1.1f%%', colors=sns.color_palette("Set3"), startangle=90)
    plt.title('Distribution of Attack Sources', fontsize=14)
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig(outputDir / 'attack_source_distribution.png', dpi=300)
    
    # Plot heatmap of attack source by country
    plt.figure(figsize=(12, 8))
    sns.heatmap(sourceByCountry, annot=True, fmt='d', cmap='YlGnBu')
    plt.title('Attack Sources by Country', fontsize=14)
    plt.tight_layout()
    plt.savefig(outputDir / 'source_by_country_heatmap.png', dpi=300)
    
    # Plot attack type by source
    plt.figure(figsize=(14, 10))
    sns.heatmap(typeBySource, annot=True, fmt='d', cmap='coolwarm')
    plt.title('Attack Types by Source', fontsize=14)
    plt.tight_layout()
    plt.savefig(outputDir / 'type_by_source_heatmap.png', dpi=300)
    
    # Save results
    with open(outputDir / 'attack_source_analysis.txt', 'w') as f:
        f.write("=== ATTACK SOURCE ANALYSIS ===\n\n")
        f.write("Attack Source Distribution:\n")
        f.write(sourceCounts.to_string())
        f.write("\n\nAttack Source by Country:\n")
        f.write(sourceByCountry.to_string())
        f.write("\n\nAttack Type by Source:\n")
        f.write(typeBySource.to_string())

# Run all analyses
def run_all_analyses():
    print("Starting cybersecurity breach data analysis...")
    
    # Clean and explore data
    cleanedData = clean_and_explore_data(dataFrame)
    print("Data cleaning and exploration completed.")
    
    # Run analyses
    analyze_financial_losses(cleanedData)
    print("Financial loss analysis completed.")
    
    analyze_attack_resolution(cleanedData)
    print("Attack resolution analysis completed.")
    
    analyze_vulnerabilities(cleanedData)
    print("Vulnerability analysis completed.")
    
    analyze_attack_sources(cleanedData)
    print("Attack source analysis completed.")
    
    print("All analyses completed successfully!")
    print(f"Results saved to {outputDir} directory.")

if __name__ == "__main__":
    run_all_analyses()
