# PowerShell script to move remaining unused files to trash-bin
# Create trash-bin directory if it doesn't exist
$trashBin = "trash-bin"
if (-not (Test-Path $trashBin)) {
    New-Item -Path $trashBin -ItemType Directory
}

# List of files/directories that are no longer needed
$unusedFiles = @(
    # Root level Python files that are no longer used 
    # (superseded by the enhanced analysis scripts)
    "create_final_report.py",
    "cybersecurity_analysis.py",
    "excel_reports.py",
    
    # Scripts replaced by enhanced_analysis_generator.py
    "analysis\create_dashboard.py",
    "analysis\modern_dashboard_generator.py",
    
    # Older visualization PNG files directly in the analysis folder
    "analysis\*.png",
    
    # Move the unused script we just created
    "move_unused_files.py",
    
    # Preserve this script but will be moved after execution
    # "final_cleanup.ps1"
)

# Move each file/directory to trash-bin
$processed = 0
foreach ($file in $unusedFiles) {
    # Handle wildcard patterns
    if ($file -match "\*") {
        $items = Get-ChildItem -Path $file
        foreach ($item in $items) {
            $fileName = Split-Path $item.FullName -Leaf
            $destination = Join-Path $trashBin $fileName
            
            # If destination already exists, remove it
            if (Test-Path $destination) {
                Remove-Item $destination -Force
            }
            
            # Move item to trash-bin
            Move-Item -Path $item.FullName -Destination $destination -Force
            Write-Host "Moved: $($item.FullName) -> $destination"
            $processed++
        }
    }
    # Handle specific files/directories
    elseif (Test-Path $file) {
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

# Move this script itself at the end
$selfScript = "final_cleanup.ps1"
$selfDestination = Join-Path $trashBin $selfScript
if (Test-Path $selfDestination) {
    Remove-Item $selfDestination -Force
}

Write-Host "`nCompleted: $processed file(s)/directory(ies) moved to trash-bin"
Write-Host "Now moving this cleanup script to trash-bin as well..."

# This command will execute after script completion
# Copy-Item -Path $selfScript -Destination $selfDestination
# Note: PowerShell can't delete a script while it's running, so we just copy it instead
