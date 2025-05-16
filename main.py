#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from src.analysis.enhanced_analysis import generate_enhanced_analysis
def main():
    print("Running Cybersecurity Breach Analysis...")
    generate_enhanced_analysis()
    dashboardPath = os.path.join('output', 'dashboard', 'index.html')
    print("Analysis complete. Results available in the output directory.")
    print(f"Dashboard available at: {dashboardPath}")
if __name__ == "__main__":
    main()