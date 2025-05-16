def generate_dashboard_html(outputDir, financialViz, attackViz, vulnerabilityViz, correlationViz, trendViz):
    """
    Generates a clean, analytics-focused HTML dashboard with no branding or dates.
    Uses snake_case for function names and camelCase for variable names.
    
    Args:
        outputDir: Directory where dashboard will be saved
        financialViz: List of financial visualization image filenames
        attackViz: List of attack pattern visualization image filenames
        vulnerabilityViz: List of vulnerability visualization image filenames
        correlationViz: List of correlation visualization image filenames
        trendViz: List of trend visualization image filenames
    """
    # Create CSS file
    cssContent = """
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

:root {
    --primary: #2c3e50;
    --secondary: #34495e;
    --accent: #3498db;
    --light: #ecf0f1;
    --dark: #2c3e50;
    --success: #2ecc71;
    --danger: #e74c3c;
    --warning: #f39c12;
    --info: #3498db;
    --body-bg: #f5f5f5;
    --card-bg: #ffffff;
    --card-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    --border-radius: 8px;
    --spacing-xs: 4px;
    --spacing-sm: 8px;
    --spacing-md: 16px;
    --spacing-lg: 24px;
    --spacing-xl: 32px;
}

body {
    background-color: var(--body-bg);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: var(--dark);
    line-height: 1.6;
}

.container {
    width: 100%;
    max-width: 1440px;
    margin: 0 auto;
    padding: var(--spacing-lg);
}

.dashboard {
    display: flex;
    flex-direction: column;
}

nav {
    background-color: var(--primary);
    border-radius: var(--border-radius);
    margin-bottom: var(--spacing-lg);
    position: sticky;
    top: 0;
    z-index: 100;
}

.nav-container {
    display: flex;
    justify-content: center;
    padding: var(--spacing-md);
}

.nav-list {
    display: flex;
    list-style: none;
    overflow-x: auto;
    white-space: nowrap;
}

.nav-item {
    margin: 0 var(--spacing-md);
}

.nav-link {
    color: var(--light);
    text-decoration: none;
    padding: var(--spacing-md);
    font-weight: 500;
    transition: color 0.3s;
}

.nav-link:hover,
.nav-link.active {
    color: var(--accent);
}

.section {
    margin-bottom: var(--spacing-xl);
    display: none;
}

.section.active {
    display: block;
    animation: fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.section-title {
    font-size: 24px;
    margin-bottom: var(--spacing-lg);
    color: var(--primary);
    border-bottom: 2px solid var(--accent);
    padding-bottom: var(--spacing-sm);
}

.viz-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(600px, 1fr));
    gap: var(--spacing-lg);
    margin-bottom: var(--spacing-xl);
}

.viz-card {
    background-color: var(--card-bg);
    border-radius: var(--border-radius);
    overflow: hidden;
    box-shadow: var(--card-shadow);
    transition: transform 0.3s, box-shadow 0.3s;
}

.viz-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
}

.viz-header {
    padding: var(--spacing-md);
    background-color: var(--light);
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.viz-title {
    font-size: 18px;
    font-weight: 500;
    margin: 0;
}

.viz-body {
    padding: var(--spacing-sm);
}

.viz-img {
    width: 100%;
    height: auto;
    cursor: pointer;
    transition: opacity 0.3s;
}

.viz-img:hover {
    opacity: 0.9;
}

/* Modal for enlarged images */
.modal {
    display: none;
    position: fixed;
    z-index: 1000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.8);
}

.modal-content {
    margin: auto;
    display: block;
    max-width: 90%;
    max-height: 90%;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.close {
    position: absolute;
    top: 15px;
    right: 35px;
    color: #f1f1f1;
    font-size: 40px;
    font-weight: bold;
    transition: 0.3s;
    cursor: pointer;
}

.close:hover {
    color: #bbb;
}

.insights-section {
    background-color: var(--card-bg);
    border-radius: var(--border-radius);
    padding: var(--spacing-lg);
    margin-bottom: var(--spacing-xl);
    box-shadow: var(--card-shadow);
}

.insights-title {
    font-size: 22px;
    margin-bottom: var(--spacing-md);
    color: var(--primary);
}

.insights-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
    gap: var(--spacing-lg);
}

.insight-card {
    background-color: var(--light);
    border-radius: var(--border-radius);
    padding: var(--spacing-md);
    border-left: 4px solid var(--accent);
}

.insight-header {
    font-weight: 600;
    margin-bottom: var(--spacing-sm);
    color: var(--primary);
}

.insight-text {
    color: var(--secondary);
    font-size: 14px;
}

@media (max-width: 768px) {
    .viz-grid {
        grid-template-columns: 1fr;
    }
    
    .insights-grid {
        grid-template-columns: 1fr;
    }
}
"""
    
    with open(outputDir / 'styles.css', 'w') as f:
        f.write(cssContent)
    
    # Create JavaScript file
    jsContent = """
document.addEventListener('DOMContentLoaded', function() {
    // Show default section
    showSection('overview');
    
    // Navigation handling
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all links
            document.querySelectorAll('.nav-link').forEach(l => {
                l.classList.remove('active');
            });
            
            // Add active class to clicked link
            this.classList.add('active');
            
            // Show corresponding section
            const sectionId = this.getAttribute('data-section');
            showSection(sectionId);
        });
    });
    
    // Image modal functionality
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImage');
    const closeBtn = document.getElementsByClassName('close')[0];
    
    document.querySelectorAll('.viz-img').forEach(img => {
        img.addEventListener('click', function() {
            modal.style.display = 'block';
            modalImg.src = this.src;
        });
    });
    
    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });
    
    window.addEventListener('click', function(e) {
        if (e.target == modal) {
            modal.style.display = 'none';
        }
    });
});

function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    
    // Show selected section
    document.getElementById(sectionId).classList.add('active');
}
"""
    
    with open(outputDir / 'main.js', 'w') as f:
        f.write(jsContent)
    
    # Generate HTML content
    htmlContent = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cybersecurity Analysis</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <div class="dashboard">
            <nav>
                <div class="nav-container">
                    <ul class="nav-list">
                        <li class="nav-item">
                            <a href="#" class="nav-link active" data-section="overview">Overview</a>
                        </li>
                        <li class="nav-item">
                            <a href="#" class="nav-link" data-section="financial-impact">Financial</a>
                        </li>
                        <li class="nav-item">
                            <a href="#" class="nav-link" data-section="attack-analysis">Attacks</a>
                        </li>
                        <li class="nav-item">
                            <a href="#" class="nav-link" data-section="vulnerability-analysis">Vulnerabilities</a>
                        </li>
                        <li class="nav-item">
                            <a href="#" class="nav-link" data-section="correlation-analysis">Correlations</a>
                        </li>
                        <li class="nav-item">
                            <a href="#" class="nav-link" data-section="trend-analysis">Trends</a>
                        </li>
                        <li class="nav-item">
                            <a href="#" class="nav-link" data-section="key-insights">Insights</a>
                        </li>
                    </ul>
                </div>
            </nav>
            
            <!-- Overview Section -->
            <section id="overview" class="section active">
                <h2 class="section-title">Analysis Overview</h2>
                
                <div class="viz-grid">
"""
    
    # Add one visualization from each category to the overview
    overviewViz = []
    if financialViz: overviewViz.append(financialViz[0])
    if attackViz: overviewViz.append(attackViz[0])
    if vulnerabilityViz: overviewViz.append(vulnerabilityViz[0])
    if correlationViz: overviewViz.append(correlationViz[0])
    
    for viz in overviewViz:
        title = ' '.join(word.capitalize() for word in viz.replace('.png', '').split('_'))
        htmlContent += f"""
                    <div class="viz-card">
                        <div class="viz-header">
                            <h3 class="viz-title">{title}</h3>
                        </div>
                        <div class="viz-body">
                            <img src="{viz}" alt="{title}" class="viz-img">
                        </div>
                    </div>
        """
    
    htmlContent += """
                </div>
            </section>
            
            <!-- Financial Impact Section -->
            <section id="financial-impact" class="section">
                <h2 class="section-title">Financial Impact Analysis</h2>
                
                <div class="viz-grid">
    """
    
    for viz in financialViz:
        title = ' '.join(word.capitalize() for word in viz.replace('.png', '').split('_'))
        htmlContent += f"""
                    <div class="viz-card">
                        <div class="viz-header">
                            <h3 class="viz-title">{title}</h3>
                        </div>
                        <div class="viz-body">
                            <img src="{viz}" alt="{title}" class="viz-img">
                        </div>
                    </div>
        """
    
    htmlContent += """
                </div>
            </section>
            
            <!-- Attack Analysis Section -->
            <section id="attack-analysis" class="section">
                <h2 class="section-title">Attack Pattern Analysis</h2>
                
                <div class="viz-grid">
    """
    
    for viz in attackViz:
        title = ' '.join(word.capitalize() for word in viz.replace('.png', '').split('_'))
        htmlContent += f"""
                    <div class="viz-card">
                        <div class="viz-header">
                            <h3 class="viz-title">{title}</h3>
                        </div>
                        <div class="viz-body">
                            <img src="{viz}" alt="{title}" class="viz-img">
                        </div>
                    </div>
        """
    
    htmlContent += """
                </div>
            </section>
            
            <!-- Vulnerability Analysis Section -->
            <section id="vulnerability-analysis" class="section">
                <h2 class="section-title">Vulnerability & Resolution Analysis</h2>
                
                <div class="viz-grid">
    """
    
    for viz in vulnerabilityViz:
        title = ' '.join(word.capitalize() for word in viz.replace('.png', '').split('_'))
        htmlContent += f"""
                    <div class="viz-card">
                        <div class="viz-header">
                            <h3 class="viz-title">{title}</h3>
                        </div>
                        <div class="viz-body">
                            <img src="{viz}" alt="{title}" class="viz-img">
                        </div>
                    </div>
        """
    
    htmlContent += """
                </div>
            </section>
            
            <!-- Correlation Analysis Section -->
            <section id="correlation-analysis" class="section">
                <h2 class="section-title">Correlation Analysis</h2>
                
                <div class="viz-grid">
    """
    
    for viz in correlationViz:
        title = ' '.join(word.capitalize() for word in viz.replace('.png', '').split('_'))
        htmlContent += f"""
                    <div class="viz-card">
                        <div class="viz-header">
                            <h3 class="viz-title">{title}</h3>
                        </div>
                        <div class="viz-body">
                            <img src="{viz}" alt="{title}" class="viz-img">
                        </div>
                    </div>
        """
    
    htmlContent += """
                </div>
            </section>
            
            <!-- Trend Analysis Section -->
            <section id="trend-analysis" class="section">
                <h2 class="section-title">Trend Analysis</h2>
                
                <div class="viz-grid">
    """
    
    for viz in trendViz:
        title = ' '.join(word.capitalize() for word in viz.replace('.png', '').split('_'))
        htmlContent += f"""
                    <div class="viz-card">
                        <div class="viz-header">
                            <h3 class="viz-title">{title}</h3>
                        </div>
                        <div class="viz-body">
                            <img src="{viz}" alt="{title}" class="viz-img">
                        </div>
                    </div>
        """
    
    htmlContent += """
                </div>
            </section>
            
            <!-- Key Insights Section -->
            <section id="key-insights" class="section">
                <h2 class="section-title">Key Insights & Findings</h2>
                
                <div class="insights-section">
                    <h3 class="insights-title">Critical Findings</h3>
                    
                    <div class="insights-grid">
                        <div class="insight-card">
                            <div class="insight-header">Financial Impact by Industry</div>
                            <div class="insight-text">Banking/Finance sector experiences the highest average financial losses from cybersecurity breaches, followed by Healthcare and Government sectors, suggesting these industries require more robust security measures.</div>
                        </div>
                        
                        <div class="insight-card">
                            <div class="insight-header">Attack Type Distribution</div>
                            <div class="insight-text">Phishing and ransomware attacks are the most prevalent and financially damaging attack types across all industries, highlighting the need for improved user training and robust backup systems.</div>
                        </div>
                        
                        <div class="insight-card">
                            <div class="insight-header">Security Vulnerability Patterns</div>
                            <div class="insight-text">Social engineering and unpatched software vulnerabilities account for the majority of successful breaches, indicating organizations should prioritize regular patching cycles and security awareness training.</div>
                        </div>
                        
                        <div class="insight-card">
                            <div class="insight-header">Resolution Time Correlation</div>
                            <div class="insight-text">Strong positive correlation exists between incident resolution time and financial impact - each additional hour of resolution time is associated with increased financial losses, emphasizing the importance of rapid incident response.</div>
                        </div>
                        
                        <div class="insight-card">
                            <div class="insight-header">Defense Mechanism Effectiveness</div>
                            <div class="insight-text">AI-based detection systems demonstrate significantly better performance in reducing both resolution times and financial impacts compared to traditional security systems.</div>
                        </div>
                        
                        <div class="insight-card">
                            <div class="insight-header">Attack Source Analysis</div>
                            <div class="insight-text">Nation-state actors are responsible for the most sophisticated and financially damaging attacks, particularly targeting critical infrastructure and government institutions.</div>
                        </div>
                        
                        <div class="insight-card">
                            <div class="insight-header">Temporal Patterns</div>
                            <div class="insight-text">Ransomware attacks show a significant increasing trend over the analyzed period, while SQL injection attacks are decreasing, suggesting evolving attack priorities among threat actors.</div>
                        </div>
                        
                        <div class="insight-card">
                            <div class="insight-header">Geographic Insights</div>
                            <div class="insight-text">Organizations in certain regions face disproportionately higher attack frequencies, potentially due to geopolitical factors or variations in security infrastructure maturity.</div>
                        </div>
                    </div>
                </div>
            </section>
            
            <!-- Image Modal -->
            <div id="imageModal" class="modal">
                <span class="close">&times;</span>
                <img class="modal-content" id="modalImage">
            </div>
        </div>
    </div>
    
    <script src="main.js"></script>
</body>
</html>
"""
    
    with open(outputDir / 'index.html', 'w') as f:
        f.write(htmlContent)
