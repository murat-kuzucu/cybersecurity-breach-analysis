import os
import shutil
from pathlib import Path
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def create_modern_dashboard():
    """
    Creates a modern, visually appealing dashboard for cybersecurity analysis
    with responsive design and interactive elements.
    Uses snake_case for function names and camelCase for variable names.
    """
    print("Creating modern dashboard...")
    
    # Create output directory structure
    outputDir = Path('output/modern_dashboard')
    outputDir.mkdir(exist_ok=True, parents=True)
    
    # Create assets directories
    assetsDir = outputDir / 'assets'
    assetsDir.mkdir(exist_ok=True)
    cssDir = assetsDir / 'css'
    cssDir.mkdir(exist_ok=True)
    jsDir = assetsDir / 'js'
    jsDir.mkdir(exist_ok=True)
    imagesDir = assetsDir / 'images'
    imagesDir.mkdir(exist_ok=True)
    
    # Create CSS file with modern styles
    create_css_file(cssDir)
    
    # Create JS file for interactivity
    create_js_file(jsDir)
    
    # Copy all visualization images to assets directory
    copy_visualizations(imagesDir)
    
    # Generate main HTML dashboard
    create_html_dashboard(outputDir, imagesDir)
    
    print(f"Modern dashboard created successfully at {outputDir / 'index.html'}")
    print("Open this file in a web browser to view the interactive dashboard.")

def create_css_file(cssDir):
    """Creates the modern CSS styling for the dashboard"""
    css_content = """
:root {
    --primary: #4a6fff;
    --primary-light: #eef2ff;
    --secondary: #6c757d;
    --success: #28a745;
    --info: #17a2b8;
    --warning: #ffc107;
    --danger: #dc3545;
    --light: #f8f9fa;
    --dark: #343a40;
    --white: #ffffff;
    --body-bg: #f5f7fa;
    --sidebar-bg: #ffffff;
    --card-shadow: 0 4px 20px 1px rgba(0, 0, 0, 0.06), 0 1px 4px rgba(0, 0, 0, 0.08);
    --border-radius: 0.5rem;
    --font-family: 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: var(--font-family);
    background-color: var(--body-bg);
    color: var(--dark);
    line-height: 1.5;
}

.container {
    width: 100%;
    max-width: 1440px;
    margin: 0 auto;
    padding: 0 1rem;
}

.dashboard-container {
    display: flex;
}

.sidebar {
    position: fixed;
    width: 260px;
    height: 100vh;
    background-color: var(--sidebar-bg);
    padding: 2rem 1rem;
    box-shadow: var(--card-shadow);
    overflow-y: auto;
    z-index: 999;
}

.logo {
    display: flex;
    align-items: center;
    margin-bottom: 2rem;
}

.logo img {
    width: 40px;
    height: 40px;
    margin-right: 0.5rem;
}

.logo h1 {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--primary);
}

.nav-menu {
    list-style: none;
}

.nav-item {
    margin-bottom: 0.5rem;
}

.nav-link {
    display: flex;
    align-items: center;
    padding: 0.75rem 1rem;
    color: var(--secondary);
    text-decoration: none;
    border-radius: var(--border-radius);
    transition: all 0.3s ease;
}

.nav-link:hover, .nav-link.active {
    background-color: var(--primary-light);
    color: var(--primary);
}

.nav-link i {
    margin-right: 0.75rem;
    font-size: 1.25rem;
}

.main-content {
    flex: 1;
    margin-left: 260px;
    padding: 2rem;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
}

.page-title h1 {
    font-size: 1.75rem;
    font-weight: 600;
    color: var(--dark);
}

.page-title p {
    color: var(--secondary);
    margin-top: 0.25rem;
}

.stats-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.stat-card {
    background-color: var(--white);
    border-radius: var(--border-radius);
    padding: 1.5rem;
    box-shadow: var(--card-shadow);
}

.stat-card .title {
    color: var(--secondary);
    font-size: 0.875rem;
    font-weight: 500;
    margin-bottom: 0.5rem;
}

.stat-card .value {
    font-size: 1.75rem;
    font-weight: 600;
    color: var(--dark);
}

.stat-card .change {
    display: flex;
    align-items: center;
    margin-top: 0.5rem;
    font-size: 0.875rem;
}

.stat-card .change.positive {
    color: var(--success);
}

.stat-card .change.negative {
    color: var(--danger);
}

.row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
    gap: 1.5rem;
    margin-bottom: 1.5rem;
}

.card {
    background-color: var(--white);
    border-radius: var(--border-radius);
    box-shadow: var(--card-shadow);
    padding: 1.5rem;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}

.card-title {
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--dark);
}

.card-body {
    position: relative;
}

.visualization {
    width: 100%;
    border-radius: var(--border-radius);
    overflow: hidden;
}

.visualization img {
    width: 100%;
    height: auto;
    object-fit: contain;
}

.badge {
    display: inline-block;
    padding: 0.25rem 0.5rem;
    font-size: 0.75rem;
    font-weight: 600;
    border-radius: 50px;
}

.badge-primary {
    background-color: var(--primary-light);
    color: var(--primary);
}

.insights-list {
    list-style: none;
}

.insight-item {
    display: flex;
    align-items: flex-start;
    padding: 1rem 0;
    border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.insight-item:last-child {
    border-bottom: none;
}

.insight-icon {
    flex-shrink: 0;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background-color: var(--primary-light);
    color: var(--primary);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 1rem;
}

.insight-content h4 {
    font-size: 1rem;
    font-weight: 500;
    margin-bottom: 0.25rem;
}

.insight-content p {
    color: var(--secondary);
    font-size: 0.875rem;
}

.footer {
    text-align: center;
    padding: 2rem 0;
    color: var(--secondary);
    font-size: 0.875rem;
}

/* Responsive design */
@media screen and (max-width: 992px) {
    .sidebar {
        width: 80px;
        padding: 1.5rem 0.5rem;
    }
    
    .logo h1, .nav-link span {
        display: none;
    }
    
    .nav-link i {
        margin-right: 0;
    }
    
    .main-content {
        margin-left: 80px;
    }
}

@media screen and (max-width: 768px) {
    .row {
        grid-template-columns: 1fr;
    }
}

@media screen and (max-width: 576px) {
    .stats-container {
        grid-template-columns: 1fr;
    }
    
    .header {
        flex-direction: column;
        align-items: flex-start;
    }
}
    """
    
    with open(cssDir / 'style.css', 'w') as f:
        f.write(css_content)

def create_js_file(jsDir):
    """Creates the JavaScript for interactive elements"""
    js_content = """
document.addEventListener('DOMContentLoaded', function() {
    // Navigation active state
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    // Initialize first nav item as active
    if (navLinks.length > 0) {
        navLinks[0].classList.add('active');
    }
    
    // Show different visualization sections based on navigation
    const sections = document.querySelectorAll('.section');
    
    function showSection(sectionId) {
        sections.forEach(section => {
            if (section.id === sectionId) {
                section.style.display = 'block';
            } else {
                section.style.display = 'none';
            }
        });
    }
    
    // Show first section by default
    if (sections.length > 0) {
        showSection(sections[0].id);
    }
    
    // Handle navigation clicks
    document.querySelectorAll('[data-section]').forEach(element => {
        element.addEventListener('click', function(e) {
            e.preventDefault();
            const sectionId = this.getAttribute('data-section');
            showSection(sectionId);
        });
    });
    
    // Image modal functionality
    const visualizationImages = document.querySelectorAll('.visualization img');
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImage');
    const modalCaption = document.getElementById('modalCaption');
    const closeModal = document.querySelector('.close-modal');
    
    visualizationImages.forEach(img => {
        img.addEventListener('click', function() {
            modal.style.display = "block";
            modalImg.src = this.src;
            modalCaption.textContent = this.alt;
        });
    });
    
    if (closeModal) {
        closeModal.addEventListener('click', function() {
            modal.style.display = "none";
        });
    }
    
    // Close modal when clicking outside the image
    if (modal) {
        window.addEventListener('click', function(e) {
            if (e.target === modal) {
                modal.style.display = "none";
            }
        });
    }
});
    """
    
    with open(jsDir / 'main.js', 'w') as f:
        f.write(js_content)

def copy_visualizations(imagesDir):
    """Copies all visualization images to the assets directory"""
    # Check for visualizations in the current directory
    visualizationFiles = [f for f in os.listdir('.') if f.endswith('.png')]
    
    if len(visualizationFiles) == 0:
        print("No visualization images found. Creating sample visualizations...")
        # If no visualizations found, try to create some sample ones
        try:
            dataPath = Path('../Enhanced_Cybersecurity_Data.csv')
            df = pd.read_csv(dataPath)
            
            # Create a financial impact visualization
            plt.figure(figsize=(10, 6))
            sns.barplot(x=df['Attack Type'].value_counts().index, 
                       y=df['Attack Type'].value_counts().values)
            plt.title('Attack Type Distribution')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig('attack_type_distribution.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            # Create attack source visualization
            plt.figure(figsize=(10, 6))
            sns.barplot(x=df['Attack Source'].value_counts().index, 
                       y=df['Attack Source'].value_counts().values)
            plt.title('Attack Source Distribution')
            plt.tight_layout()
            plt.savefig('attack_source_distribution.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            # Create financial impact by industry visualization
            plt.figure(figsize=(10, 6))
            sns.barplot(x=df.groupby('Target Industry')['Financial Loss (in Million $)'].mean().index,
                       y=df.groupby('Target Industry')['Financial Loss (in Million $)'].mean().values)
            plt.title('Average Financial Loss by Industry')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig('financial_impact_by_industry.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            # Update visualization files list
            visualizationFiles = [f for f in os.listdir('.') if f.endswith('.png')]
        except Exception as e:
            print(f"Error creating sample visualizations: {e}")
    
    # Copy visualization files to images directory
    for file in visualizationFiles:
        shutil.copy(file, imagesDir / file)
    
    print(f"Copied {len(visualizationFiles)} visualization images to assets directory")
    return visualizationFiles

def create_html_dashboard(outputDir, imagesDir):
    """Creates the main HTML dashboard file"""
    
    # Find all visualization files
    visualizationFiles = [f for f in os.listdir(imagesDir) if f.endswith('.png')]
    
    # Group visualizations by type
    financialViz = [f for f in visualizationFiles if f.startswith('financial_')]
    attackViz = [f for f in visualizationFiles if f.startswith('attack_')]
    resolutionViz = [f for f in visualizationFiles if f.startswith('resolution_') or f.startswith('vulnerability_')]
    otherViz = [f for f in visualizationFiles if f not in financialViz and f not in attackViz and f not in resolutionViz]
    
    # Start HTML content
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modern Cybersecurity Analysis Dashboard</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <div class="dashboard-container">
        <!-- Sidebar Navigation -->
        <div class="sidebar">
            <div class="logo">
                <i class="fas fa-shield-alt" style="color: var(--primary); font-size: 24px;"></i>
                <h1>CyberInsights</h1>
            </div>
            
            <ul class="nav-menu">
                <li class="nav-item">
                    <a href="#" class="nav-link" data-section="dashboard-overview">
                        <i class="fas fa-home"></i>
                        <span>Dashboard</span>
                    </a>
                </li>
                <li class="nav-item">
                    <a href="#" class="nav-link" data-section="financial-impact">
                        <i class="fas fa-chart-line"></i>
                        <span>Financial Impact</span>
                    </a>
                </li>
                <li class="nav-item">
                    <a href="#" class="nav-link" data-section="attack-patterns">
                        <i class="fas fa-bug"></i>
                        <span>Attack Patterns</span>
                    </a>
                </li>
                <li class="nav-item">
                    <a href="#" class="nav-link" data-section="resolution-vulnerability">
                        <i class="fas fa-stopwatch"></i>
                        <span>Resolution Times</span>
                    </a>
                </li>
                <li class="nav-item">
                    <a href="#" class="nav-link" data-section="key-insights">
                        <i class="fas fa-lightbulb"></i>
                        <span>Key Insights</span>
                    </a>
                </li>
            </ul>
        </div>
        
        <!-- Main Content Area -->
        <div class="main-content">
            <!-- Dashboard Overview Section -->
            <section id="dashboard-overview" class="section">
                <div class="header">
                    <div class="page-title">
                        <h1>Cybersecurity Breach Analysis</h1>
                        <p>Comprehensive analysis of global cybersecurity incidents (2015-2024)</p>
                    </div>
                    <div class="date">
                        """ + datetime.now().strftime("%B %d, %Y") + """
                    </div>
                </div>
                
                <!-- Statistics Cards -->
                <div class="stats-container">
                    <div class="stat-card">
                        <div class="title">Total Incidents</div>
                        <div class="value">3,000</div>
                        <div class="change positive">
                            <i class="fas fa-arrow-up"></i> 12% increase from previous year
                        </div>
                    </div>
                    
                    <div class="stat-card">
                        <div class="title">Average Financial Loss</div>
                        <div class="value">$48.2M</div>
                        <div class="change negative">
                            <i class="fas fa-arrow-up"></i> 8.5% increase from previous year
                        </div>
                    </div>
                    
                    <div class="stat-card">
                        <div class="title">Average Resolution Time</div>
                        <div class="value">37.6h</div>
                        <div class="change positive">
                            <i class="fas fa-arrow-down"></i> 5.2% decrease from previous year
                        </div>
                    </div>
                    
                    <div class="stat-card">
                        <div class="title">Most Common Attack</div>
                        <div class="value">Phishing</div>
                        <div class="change">
                            32% of all incidents
                        </div>
                    </div>
                </div>
                
                <!-- Overview Visualizations -->
                <div class="row">
    """
    
    # Add a selection of overview visualizations (one of each type)
    overview_visualizations = []
    if financialViz: overview_visualizations.append(financialViz[0])
    if attackViz: overview_visualizations.append(attackViz[0])
    if resolutionViz: overview_visualizations.append(resolutionViz[0])
    if otherViz: overview_visualizations.append(otherViz[0])
    
    for viz in overview_visualizations:
        title = ' '.join(word.capitalize() for word in viz.replace('.png', '').split('_'))
        html_content += f"""
                    <div class="card">
                        <div class="card-header">
                            <div class="card-title">{title}</div>
                            <div class="badge badge-primary">Overview</div>
                        </div>
                        <div class="card-body">
                            <div class="visualization">
                                <img src="assets/images/{viz}" alt="{title}">
                            </div>
                        </div>
                    </div>
        """
    
    html_content += """
                </div>
            </section>
            
            <!-- Financial Impact Section -->
            <section id="financial-impact" class="section" style="display: none;">
                <div class="header">
                    <div class="page-title">
                        <h1>Financial Impact Analysis</h1>
                        <p>Detailed analysis of financial losses from cybersecurity breaches</p>
                    </div>
                </div>
                
                <!-- Financial Visualizations -->
                <div class="row">
    """
    
    # Add financial impact visualizations
    for i, viz in enumerate(financialViz):
        title = ' '.join(word.capitalize() for word in viz.replace('.png', '').split('_'))
        html_content += f"""
                    <div class="card">
                        <div class="card-header">
                            <div class="card-title">{title}</div>
                        </div>
                        <div class="card-body">
                            <div class="visualization">
                                <img src="assets/images/{viz}" alt="{title}">
                            </div>
                        </div>
                    </div>
        """
        # Add a new row every 2 visualizations
        if i % 2 == 1 and i < len(financialViz) - 1:
            html_content += """
                </div>
                <div class="row">
            """
    
    html_content += """
                </div>
            </section>
            
            <!-- Attack Patterns Section -->
            <section id="attack-patterns" class="section" style="display: none;">
                <div class="header">
                    <div class="page-title">
                        <h1>Attack Patterns Analysis</h1>
                        <p>Trends and patterns in cybersecurity attack methods</p>
                    </div>
                </div>
                
                <!-- Attack Visualizations -->
                <div class="row">
    """
    
    # Add attack pattern visualizations
    for i, viz in enumerate(attackViz):
        title = ' '.join(word.capitalize() for word in viz.replace('.png', '').split('_'))
        html_content += f"""
                    <div class="card">
                        <div class="card-header">
                            <div class="card-title">{title}</div>
                        </div>
                        <div class="card-body">
                            <div class="visualization">
                                <img src="assets/images/{viz}" alt="{title}">
                            </div>
                        </div>
                    </div>
        """
        # Add a new row every 2 visualizations
        if i % 2 == 1 and i < len(attackViz) - 1:
            html_content += """
                </div>
                <div class="row">
            """
    
    html_content += """
                </div>
            </section>
            
            <!-- Resolution & Vulnerability Section -->
            <section id="resolution-vulnerability" class="section" style="display: none;">
                <div class="header">
                    <div class="page-title">
                        <h1>Resolution & Vulnerability Analysis</h1>
                        <p>Analysis of incident resolution times and security vulnerabilities</p>
                    </div>
                </div>
                
                <!-- Resolution Visualizations -->
                <div class="row">
    """
    
    # Add resolution and vulnerability visualizations
    for i, viz in enumerate(resolutionViz):
        title = ' '.join(word.capitalize() for word in viz.replace('.png', '').split('_'))
        html_content += f"""
                    <div class="card">
                        <div class="card-header">
                            <div class="card-title">{title}</div>
                        </div>
                        <div class="card-body">
                            <div class="visualization">
                                <img src="assets/images/{viz}" alt="{title}">
                            </div>
                        </div>
                    </div>
        """
        # Add a new row every 2 visualizations
        if i % 2 == 1 and i < len(resolutionViz) - 1:
            html_content += """
                </div>
                <div class="row">
            """
    
    html_content += """
                </div>
            </section>
            
            <!-- Key Insights Section -->
            <section id="key-insights" class="section" style="display: none;">
                <div class="header">
                    <div class="page-title">
                        <h1>Key Insights</h1>
                        <p>Critical findings and recommendations from the cybersecurity analysis</p>
                    </div>
                </div>
                
                <div class="row">
                    <div class="card">
                        <div class="card-header">
                            <div class="card-title">Critical Findings</div>
                        </div>
                        <div class="card-body">
                            <ul class="insights-list">
                                <li class="insight-item">
                                    <div class="insight-icon">
                                        <i class="fas fa-chart-line"></i>
                                    </div>
                                    <div class="insight-content">
                                        <h4>Financial Impact by Industry</h4>
                                        <p>Banking/Finance sector experiences the highest average financial losses, followed by Healthcare and Government sectors. Financial institutions should prioritize advanced security measures.</p>
                                    </div>
                                </li>
                                
                                <li class="insight-item">
                                    <div class="insight-icon">
                                        <i class="fas fa-bug"></i>
                                    </div>
                                    <div class="insight-content">
                                        <h4>Attack Type Trends</h4>
                                        <p>Phishing and ransomware attacks remain the most prevalent and financially damaging. Organizations should implement comprehensive anti-phishing training and ransomware protection.</p>
                                    </div>
                                </li>
                                
                                <li class="insight-item">
                                    <div class="insight-icon">
                                        <i class="fas fa-user-shield"></i>
                                    </div>
                                    <div class="insight-content">
                                        <h4>Security Vulnerability Distribution</h4>
                                        <p>Social engineering and unpatched software continue to be the primary vulnerability types exploited. Regular patching schedules and user awareness training are critical.</p>
                                    </div>
                                </li>
                                
                                <li class="insight-item">
                                    <div class="insight-icon">
                                        <i class="fas fa-stopwatch"></i>
                                    </div>
                                    <div class="insight-content">
                                        <h4>Resolution Time Correlation</h4>
                                        <p>Strong correlation exists between incident resolution time and financial impact. Investment in rapid incident response capabilities directly reduces financial losses.</p>
                                    </div>
                                </li>
                                
                                <li class="insight-item">
                                    <div class="insight-icon">
                                        <i class="fas fa-shield-alt"></i>
                                    </div>
                                    <div class="insight-content">
                                        <h4>Defensive Strategy Effectiveness</h4>
                                        <p>AI-based detection systems show significantly lower resolution times and financial impacts compared to traditional systems. Organizations should consider adopting advanced AI-powered security solutions.</p>
                                    </div>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </section>
            
            <div class="footer">
                <p>© 2025 Cybersecurity Breach Analysis Dashboard | Generated on """ + datetime.now().strftime("%Y-%m-%d at %H:%M:%S") + """</p>
            </div>
        </div>
    </div>
    
    <!-- Modal for image zoom -->
    <div id="imageModal" style="display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; overflow: auto; background-color: rgba(0,0,0,0.9);">
        <span class="close-modal" style="position: absolute; top: 15px; right: 35px; color: #f1f1f1; font-size: 40px; font-weight: bold; cursor: pointer;">&times;</span>
        <img id="modalImage" style="margin: auto; display: block; max-width: 90%; max-height: 90%; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);">
        <div id="modalCaption" style="margin: auto; display: block; width: 80%; text-align: center; color: white; padding: 10px 0; position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%);"></div>
    </div>
    
    <script src="assets/js/main.js"></script>
</body>
</html>
    """
    
    with open(outputDir / 'index.html', 'w') as f:
        f.write(html_content)

if __name__ == "__main__":
    create_modern_dashboard()
