import os
import shutil
from pathlib import Path

def move_unused_files_to_trash():
    """
    Identify and move unused files to the trash-bin directory.
    Uses snake_case for function names as per user rules.
    """
    # Ensure trash-bin directory exists
    trashBinDir = Path('trash-bin')
    trashBinDir.mkdir(exist_ok=True)
    
    # List of files/directories that are no longer needed
    unusedFiles = [
        # Old analysis results that have been replaced by enhanced analysis
        'analysis_results/attack_source_analysis.txt',
        'analysis_results/attack_source_distribution.png',
        'analysis_results/avg_loss_by_industry.png',
        'analysis_results/avg_resolution_by_attack.png',
        'analysis_results/data_summary.txt',
        'analysis_results/financial_analysis.txt',
        'analysis_results/industry_loss_trends.png',
        'analysis_results/loss_by_defense.png',
        'analysis_results/loss_by_vulnerability.png',
        'analysis_results/loss_trend_over_time.png',
        'analysis_results/resolution_analysis.txt',
        'analysis_results/resolution_boxplot.png',
        'analysis_results/resolution_vs_loss.png',
        'analysis_results/source_by_country_heatmap.png',
        'analysis_results/time_by_defense.png',
        'analysis_results/type_by_source_heatmap.png',
        'analysis_results/vulnerability_analysis.txt',
        
        # Redundant files in the analysis directory
        'analysis/improve_defense_mechanism_graph.py',  # Replaced by simple_defense_viz.py
        'analysis/attack_source_distribution.png',      # Output now in enhanced_analysis
        'analysis/attack_type_distribution.png',        # Output now in enhanced_analysis
        'analysis/financial_impact_by_industry.png',    # Output now in enhanced_analysis
        
        # Duplicate analysis folder structure
        'analysis/analysis',                            # Redundant nested directory
        
        # Old dashboard versions replaced by enhanced_analysis
        'analysis/output/dashboard',                    # Older dashboard version
        'analysis/output/modern_dashboard',             # Replaced by enhanced_analysis
        
        # Questions directory (no longer needed for analysis)
        'questions',
        
        # Old or unused scripts
        'create_presentation.py',                       # Not used in the final solution
    ]
    
    # Move each unused file to trash-bin
    filesProcessed = 0
    for filePath in unusedFiles:
        srcPath = Path(filePath)
        
        # Skip if file doesn't exist
        if not srcPath.exists():
            print(f"Skipping non-existent path: {srcPath}")
            continue
        
        # Create destination path
        destPath = trashBinDir / srcPath.name
        
        # Create parent directories in trash-bin if needed
        if destPath.name != srcPath.name:  # For subdirectories preservation
            destPath = trashBinDir / filePath
            destPath.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            # Move file or directory
            if srcPath.is_dir():
                # For directories, copy the structure then remove original
                if destPath.exists():
                    shutil.rmtree(destPath)
                shutil.copytree(srcPath, destPath)
                shutil.rmtree(srcPath)
                print(f"Moved directory: {srcPath} → trash-bin/{destPath.relative_to(trashBinDir)}")
            else:
                # For files, just move them
                shutil.move(srcPath, destPath)
                print(f"Moved file: {srcPath} → trash-bin/{destPath.relative_to(trashBinDir)}")
            
            filesProcessed += 1
        except Exception as e:
            print(f"Error moving {srcPath}: {e}")
    
    print(f"\nCompleted: {filesProcessed} file(s)/director(ies) moved to trash-bin")

if __name__ == "__main__":
    move_unused_files_to_trash()
