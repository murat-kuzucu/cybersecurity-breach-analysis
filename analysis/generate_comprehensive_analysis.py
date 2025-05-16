import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import os
import sys
from datetime import datetime

# Import individual analysis modules
try:
    from financial_impact_analysis import analyze_financial_impact
    from attack_patterns_analysis import analyze_attack_patterns
    from resolution_vulnerability_analysis import analyze_resolution_vulnerability
except ImportError:
    print("Error importing analysis modules. Make sure you're running this script from the analysis directory.")
    sys.exit(1)

def create_dashboard():
    """Creates a unified dashboard from key visualizations"""
    print("Creating comprehensive dashboard...")
    
    outputDir = Path('output')
    if not outputDir.exists():
        print("No output directory found. Please run the analysis modules first.")
        return
    
    # Create dashboard directory
    dashboardDir = Path('output/dashboard')
    dashboardDir.mkdir(exist_ok=True)
    
    # List of key visualizations for the dashboard (6 most important ones)
    keyVisualizations = [
        {'file': 'financial_impact_by_industry.png', 'title': 'Financial Impact by Industry'},
        {'file': 'attack_type_distribution.png', 'title': 'Attack Type Distribution'},
        {'file': 'vulnerability_distribution.png', 'title': 'Security Vulnerability Distribution'},
        {'file': 'resolution_time_by_attack.png', 'title': 'Resolution Time by Attack Type'},
        {'file': 'attack_type_by_industry.png', 'title': 'Attack Types by Industry'},
        {'file': 'resolution_vs_financial_loss.png', 'title': 'Resolution Time vs Financial Loss'}
    ]
    
    # Create dashboard HTML
    with open(dashboardDir / 'cybersecurity_dashboard.html', 'w') as f:
        f.write("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Cybersecurity Breach Analysis Dashboard</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                }
                .dashboard-container {
                    max-width: 1200px;
                    margin: 0 auto;
                }
                .header {
                    background-color: #1a237e;
                    color: white;
                    padding: 20px;
                    border-radius: 10px 10px 0 0;
                    margin-bottom: 20px;
                }
                .header h1 {
                    margin: 0;
                }
                .visualization-row {
                    display: flex;
                    flex-wrap: wrap;
                    justify-content: space-between;
                    margin-bottom: 20px;
                }
                .visualization-card {
                    background-color: white;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                    margin-bottom: 20px;
                    width: 48%;
                    overflow: hidden;
                }
                .visualization-card h2 {
                    padding: 15px;
                    margin: 0;
                    background-color: #f0f0f0;
                    font-size: 18px;
                    color: #333;
                }
                .visualization-card img {
                    width: 100%;
                    max-height: 400px;
                    object-fit: contain;
                    padding: 10px;
                }
                .footer {
                    text-align: center;
                    margin-top: 30px;
                    padding-top: 15px;
                    border-top: 1px solid #ddd;
                    color: #666;
                }
                .summary {
                    background-color: white;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                    padding: 20px;
                    margin-bottom: 20px;
                }
                .summary h2 {
                    color: #1a237e;
                    margin-top: 0;
                }
            </style>
        </head>
        <body>
            <div class="dashboard-container">
                <div class="header">
                    <h1>Cybersecurity Breach Analysis Dashboard</h1>
                    <p>Comprehensive analysis of global cybersecurity breaches (2015-2024)</p>
                </div>
                
                <div class="summary">
                    <h2>Key Insights</h2>
                    <ul>
                        <li>Financial impact varies significantly by industry, with the highest losses observed in Banking/Finance/FinTech sector</li>
                        <li>Phishing and ransomware remain the most prevalent attack types across all industries</li>
                        <li>There is a strong correlation between incident resolution time and financial loss</li>
                        <li>Social engineering and unpatched software are the leading vulnerability types</li>
                        <li>Advanced defense mechanisms like AI-based detection significantly reduce resolution times</li>
                    </ul>
                </div>
                
                <div class="visualization-row">
        """)
        
        # Add visualizations
        for i, viz in enumerate(keyVisualizations):
            if i > 0 and i % 2 == 0:
                f.write('</div>\n<div class="visualization-row">\n')
            
            f.write(f"""
                    <div class="visualization-card">
                        <h2>{viz['title']}</h2>
                        <img src="../{viz['file']}" alt="{viz['title']}">
                    </div>
            """)
        
        # Close the visualization row and add footer
        f.write("""
                </div>
                
                <div class="footer">
                    <p>Generated on """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
                    <p>For more detailed analysis, refer to the individual analysis reports</p>
                </div>
            </div>
        </body>
        </html>
        """)
    
    # Create an index.md file with links to all reports and visualizations
    with open(dashboardDir / 'index.md', 'w') as f:
        f.write("# Cybersecurity Breach Analysis - Complete Results\n\n")
        f.write(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## Interactive Dashboard\n")
        f.write("- [View Interactive Dashboard](cybersecurity_dashboard.html)\n\n")
        
        f.write("## Summary Reports\n")
        f.write("- [Financial Impact Analysis](../financial_impact_summary.md)\n")
        f.write("- [Attack Patterns Analysis](../attack_patterns_summary.md)\n")
        f.write("- [Resolution Time & Vulnerability Analysis](../resolution_vulnerability_summary.md)\n\n")
        
        f.write("## All Visualizations\n\n")
        f.write("### Financial Impact\n")
        f.write("- [Financial Impact by Industry](../financial_impact_by_industry.png)\n")
        f.write("- [Financial Impact by Attack Type](../financial_impact_by_attack.png)\n")
        f.write("- [Financial Impact Distribution](../financial_impact_distribution.png)\n")
        f.write("- [Financial Impact Heatmap](../financial_impact_heatmap.png)\n")
        f.write("- [Financial Impact Trends](../financial_impact_trends.png)\n")
        f.write("- [Financial Impact by Vulnerability](../financial_impact_by_vulnerability.png)\n\n")
        
        f.write("### Attack Patterns\n")
        f.write("- [Attack Type Distribution](../attack_type_distribution.png)\n")
        f.write("- [Attack Evolution Over Time](../attack_evolution.png)\n")
        f.write("- [Attack Source Distribution](../attack_source_distribution.png)\n")
        f.write("- [Attack Type by Source](../attack_type_by_source.png)\n")
        f.write("- [Attack Type by Industry](../attack_type_by_industry.png)\n")
        f.write("- [Geographic Attack Distribution](../geographic_attack_distribution.png)\n")
        f.write("- [Affected Users by Attack Type](../affected_users_by_attack.png)\n\n")
        
        f.write("### Resolution & Vulnerability\n")
        f.write("- [Resolution Time by Industry](../resolution_time_by_industry.png)\n")
        f.write("- [Resolution Time by Attack Type](../resolution_time_by_attack.png)\n")
        f.write("- [Resolution Time Distribution](../resolution_time_distribution.png)\n")
        f.write("- [Resolution Time by Defense](../resolution_time_by_defense.png)\n")
        f.write("- [Resolution vs Financial Loss](../resolution_vs_financial_loss.png)\n")
        f.write("- [Vulnerability Distribution](../vulnerability_distribution.png)\n")
        f.write("- [Vulnerability by Industry](../vulnerability_by_industry.png)\n")
    
    print(f"Dashboard created successfully at {dashboardDir / 'cybersecurity_dashboard.html'}")
    print(f"Index created successfully at {dashboardDir / 'index.md'}")

def generate_comprehensive_analysis():
    """
    Runs all analysis modules and generates a comprehensive dashboard.
    Uses snake_case for function names and camelCase for variable names.
    """
    print("Starting comprehensive cybersecurity breach analysis...")
    
    # Create output directory
    outputDir = Path('analysis/output')
    outputDir.mkdir(exist_ok=True, parents=True)
    
    # Run financial impact analysis
    print("\n=== FINANCIAL IMPACT ANALYSIS ===")
    analyze_financial_impact()
    
    # Run attack patterns analysis
    print("\n=== ATTACK PATTERNS ANALYSIS ===")
    analyze_attack_patterns()
    
    # Run resolution time and vulnerability analysis
    print("\n=== RESOLUTION & VULNERABILITY ANALYSIS ===")
    analyze_resolution_vulnerability()
    
    # Create comprehensive dashboard
    print("\n=== CREATING DASHBOARD ===")
    create_dashboard()
    
    print("\nComprehensive analysis completed successfully!")
    print(f"All visualizations and reports are available in the {outputDir} directory")
    print(f"Dashboard is available at {outputDir / 'dashboard/cybersecurity_dashboard.html'}")

if __name__ == "__main__":
    generate_comprehensive_analysis()
