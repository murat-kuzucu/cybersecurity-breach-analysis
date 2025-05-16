# PowerShell script to move unused files to trash-bin
# Create trash-bin directory if it doesn't exist
$trashBin = "trash-bin"
if (-not (Test-Path $trashBin)) {
    New-Item -Path $trashBin -ItemType Directory
}

# List of files/directories that are no longer needed
$unusedFiles = @(
    # Old analysis results that have been replaced by enhanced analysis
    "analysis_results",
    
    # Redundant files in the analysis directory
    "analysis\improve_defense_mechanism_graph.py",  # Replaced by simple_defense_viz.py
    "analysis\attack_source_distribution.png",      # Output now in enhanced_analysis
    "analysis\attack_type_distribution.png",        # Output now in enhanced_analysis
    "analysis\financial_impact_by_industry.png",    # Output now in enhanced_analysis
    
    # Duplicate analysis folder structure
    "analysis\analysis",                            # Redundant nested directory
    
    # Old dashboard versions replaced by enhanced_analysis
    "analysis\output\dashboard",                    # Older dashboard version
    "analysis\output\modern_dashboard",             # Replaced by enhanced_analysis
    
    # Questions directory (no longer needed for analysis)
    "questions",
    
    # Old or unused scripts
    "create_presentation.py"                       # Not used in the final solution
)

# Move each file/directory to trash-bin
$processed = 0
foreach ($file in $unusedFiles) {
    if (Test-Path $file) {
        $fileName = Split-Path $file -Leaf
        $destination = Join-Path $trashBin $fileName
        
        # If destination already exists, remove it
        if (Test-Path $destination) {
            if ((Get-Item $destination) -is [System.IO.DirectoryInfo]) {
                Remove-Item $destination -Force -Recurse
            } else {
                Remove-Item $destination -Force
            }
        }
        
        # Move item to trash-bin
        if ((Get-Item $file) -is [System.IO.DirectoryInfo]) {
            # For directories, copy then remove
            Copy-Item -Path $file -Destination $destination -Recurse
            Remove-Item -Path $file -Force -Recurse
        } else {
            # For files
            Move-Item -Path $file -Destination $destination -Force
        }
        
        Write-Host "Moved: $file -> $destination"
        $processed++
    } else {
        Write-Host "Skipping non-existent path: $file"
    }
}

Write-Host "`nCompleted: $processed file(s)/directory(ies) moved to trash-bin"
