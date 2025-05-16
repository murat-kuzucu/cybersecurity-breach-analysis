from pathlib import Path
import os
def generate_dashboard_html(vizDir, dashboardDir, financialViz, attackViz, vulnerabilityViz, correlationViz, trendViz):
    cssContent =
    with open(Path(dashboardDir) / 'styles.css', 'w') as f:
        f.write(cssContent)
    jsContent =
    with open(Path(dashboardDir) / 'main.js', 'w') as f:
        f.write(jsContent)
    htmlContent =
    overviewViz = []
    if financialViz: overviewViz.append(financialViz[0])
    if attackViz: overviewViz.append(attackViz[0])
    if vulnerabilityViz: overviewViz.append(vulnerabilityViz[0])
    if correlationViz: overviewViz.append(correlationViz[0])
    for viz in overviewViz:
        title = ' '.join(word.capitalize() for word in viz.replace('.png', '').split('_'))
        htmlContent += f
    htmlContent +=
    for viz in financialViz:
        title = ' '.join(word.capitalize() for word in viz.replace('.png', '').split('_'))
        htmlContent += f
    htmlContent +=
    for viz in attackViz:
        title = ' '.join(word.capitalize() for word in viz.replace('.png', '').split('_'))
        htmlContent += f
    htmlContent +=
    for viz in vulnerabilityViz:
        title = ' '.join(word.capitalize() for word in viz.replace('.png', '').split('_'))
        htmlContent += f
    htmlContent +=
    for viz in correlationViz:
        title = ' '.join(word.capitalize() for word in viz.replace('.png', '').split('_'))
        htmlContent += f
    htmlContent +=
    for viz in trendViz:
        title = ' '.join(word.capitalize() for word in viz.replace('.png', '').split('_'))
        htmlContent += f
    htmlContent +=
    with open(Path(dashboardDir) / 'index.html', 'w') as f:
        f.write(htmlContent)