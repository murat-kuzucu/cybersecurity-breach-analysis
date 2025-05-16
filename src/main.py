import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import os
import sys
from datetime import datetime
try:
    from src.analysis.financial_impact import analyze_financial_impact
    from src.analysis.attack_patterns import analyze_attack_patterns
    from src.analysis.resolution_vulnerability import analyze_resolution_vulnerability
except ImportError:
    print("Error importing analysis modules. Make sure you're running this script from the analysis directory.")
    sys.exit(1)
def create_dashboard():
    print("Creating comprehensive dashboard...")
    outputDir = Path('output')
    if not outputDir.exists():
        print("No output directory found. Please run the analysis modules first.")
        return
    dashboardDir = Path('output/dashboard')
    dashboardDir.mkdir(exist_ok=True)
    keyVisualizations = [
        {'file': 'financial_impact_by_industry.png', 'title': 'Financial Impact by Industry'},
        {'file': 'attack_type_distribution.png', 'title': 'Attack Type Distribution'},
        {'file': 'vulnerability_distribution.png', 'title': 'Security Vulnerability Distribution'},
        {'file': 'resolution_time_by_attack.png', 'title': 'Resolution Time by Attack Type'},
        {'file': 'attack_type_by_industry.png', 'title': 'Attack Types by Industry'},
        {'file': 'resolution_vs_financial_loss.png', 'title': 'Resolution Time vs Financial Loss'}
    ]
    with open(dashboardDir / 'cybersecurity_dashboard.html', 'w') as f:
        f.write()
        for i, viz in enumerate(keyVisualizations):
            if i > 0 and i % 2 == 0:
                f.write('</div>\n<div class="visualization-row">\n')
            f.write(f)
        f.write( + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + )
    with open(dashboardDir / 'index.md', 'w') as f:
        f.write("
        f.write(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("
        f.write("- [View Interactive Dashboard](cybersecurity_dashboard.html)\n\n")
        f.write("
        f.write("- [Financial Impact Analysis](../financial_impact_summary.md)\n")
        f.write("- [Attack Patterns Analysis](../attack_patterns_summary.md)\n")
        f.write("- [Resolution Time & Vulnerability Analysis](../resolution_vulnerability_summary.md)\n\n")
        f.write("
        f.write("
        f.write("- [Financial Impact by Industry](../financial_impact_by_industry.png)\n")
        f.write("- [Financial Impact by Attack Type](../financial_impact_by_attack.png)\n")
        f.write("- [Financial Impact Distribution](../financial_impact_distribution.png)\n")
        f.write("- [Financial Impact Heatmap](../financial_impact_heatmap.png)\n")
        f.write("- [Financial Impact Trends](../financial_impact_trends.png)\n")
        f.write("- [Financial Impact by Vulnerability](../financial_impact_by_vulnerability.png)\n\n")
        f.write("
        f.write("- [Attack Type Distribution](../attack_type_distribution.png)\n")
        f.write("- [Attack Evolution Over Time](../attack_evolution.png)\n")
        f.write("- [Attack Source Distribution](../attack_source_distribution.png)\n")
        f.write("- [Attack Type by Source](../attack_type_by_source.png)\n")
        f.write("- [Attack Type by Industry](../attack_type_by_industry.png)\n")
        f.write("- [Geographic Attack Distribution](../geographic_attack_distribution.png)\n")
        f.write("- [Affected Users by Attack Type](../affected_users_by_attack.png)\n\n")
        f.write("
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
    print("Starting comprehensive cybersecurity breach analysis...")
    outputDir = Path('analysis/output')
    outputDir.mkdir(exist_ok=True, parents=True)
    print("\n=== FINANCIAL IMPACT ANALYSIS ===")
    analyze_financial_impact()
    print("\n=== ATTACK PATTERNS ANALYSIS ===")
    analyze_attack_patterns()
    print("\n=== RESOLUTION & VULNERABILITY ANALYSIS ===")
    analyze_resolution_vulnerability()
    print("\n=== CREATING DASHBOARD ===")
    create_dashboard()
    print("\nComprehensive analysis completed successfully!")
    print(f"All visualizations and reports are available in the {outputDir} directory")
    print(f"Dashboard is available at {outputDir / 'dashboard/cybersecurity_dashboard.html'}")
if __name__ == "__main__":
    generate_comprehensive_analysis()