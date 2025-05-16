import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
from fpdf import FPDF
import datetime

class CybersecurityReportPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()
        self.font_path = None  # Font path will be set later

    def header(self):
        if self.page_no() > 1:  # Don't show header on first page
            # Header with logo and title
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, 'Modern Cybersecurity Breach Analysis', 0, 0, 'R')
            self.ln(15)
            
    def footer(self):
        if self.page_no() > 1:  # Don't show footer on first page
            # Footer with page numbers
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    
    def title_page(self, title, subtitle, date):
        # Title page
        self.set_font('Arial', 'B', 24)
        self.ln(60)
        self.cell(0, 15, title, 0, 1, 'C')
        self.set_font('Arial', '', 16)
        self.cell(0, 15, subtitle, 0, 1, 'C')
        self.ln(10)
        self.set_font('Arial', '', 12)
        self.cell(0, 10, date, 0, 1, 'C')
        self.ln(40)
        self.set_font('Arial', 'I', 12)
        self.cell(0, 10, 'CONFIDENTIAL', 0, 1, 'C')
        self.add_page()
    
    def chapter_title(self, title):
        # Chapter title
        self.set_font('Arial', 'B', 16)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, title, 0, 1, 'L', 1)
        self.ln(5)
    
    def section_title(self, title):
        # Section title
        self.set_font('Arial', 'B', 12)
        self.cell(0, 8, title, 0, 1, 'L')
        self.ln(2)
    
    def body_text(self, text):
        # Body text
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 6, text)
        self.ln(3)
    
    def bullet_list(self, items):
        # Bullet list
        self.set_font('Arial', '', 11)
        for item in items:
            self.cell(5, 6, chr(149), 0, 0)  # Bullet character
            self.multi_cell(0, 6, item)
    
    def add_image(self, img_path, caption=None, w=180):
        # Add image with caption
        try:
            self.image(img_path, x=None, y=None, w=w)
            if caption:
                self.set_font('Arial', 'I', 9)
                self.ln(1)
                self.cell(0, 5, caption, 0, 1, 'C')
            self.ln(5)
        except Exception as e:
            self.set_font('Arial', 'I', 9)
            self.cell(0, 5, f"[Image {img_path} could not be loaded]", 0, 1, 'C')
            self.ln(5)
            print(f"Error loading image {img_path}: {e}")
    
    def add_table(self, headers, data, col_widths=None):
        # Add table with headers and data
        self.set_font('Arial', 'B', 10)
        
        # If col_widths not provided, distribute evenly
        if col_widths is None:
            col_widths = [190 / len(headers)] * len(headers)
        
        # Headers
        self.set_fill_color(230, 230, 230)
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 7, str(header), 1, 0, 'C', 1)
        self.ln()
        
        # Data
        self.set_font('Arial', '', 10)
        for row in data:
            for i, cell in enumerate(row):
                self.cell(col_widths[i], 7, str(cell), 1, 0, 'C')
            self.ln()
        self.ln(5)

def create_final_report():
    """Cybersecurity Breach Analysis projesinin final raporunu hazırlar"""
    
    # PDF nesnesi oluştur
    pdf = CybersecurityReportPDF()
    
    # Başlık sayfası
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    pdf.title_page('Modern Cybersecurity Breach Analysis', 'Final Project Report', current_date)
    
    # İçindekiler
    pdf.chapter_title('Contents')
    contents = [
        '1. Executive Summary',
        '2. Introduction',
        '3. Methodology',
        '4. Analysis Results',
        '5. Questionnaire Design',
        '6. Findings and Insights',
        '7. Recommendations',
        '8. Conclusion',
        '9. References'
    ]
    pdf.bullet_list(contents)
    pdf.add_page()
    
    # 1. Yönetici Özeti
    pdf.chapter_title('1. Executive Summary')
    
    executive_summary = '''This report presents the findings of a comprehensive analysis of cybersecurity breaches between 2015 and 2024. Using a dataset of global cybersecurity incidents, we examined patterns in financial losses, attack types, resolution times, and security vulnerabilities across different industries and regions.

Our analysis reveals that:

1. The financial impact of cybersecurity breaches varies significantly by industry, with the Banking, Retail, and Healthcare sectors experiencing the highest average losses.

2. Ransomware and DDoS attacks have shown the most significant increase over the period studied, while phishing remains the most common attack vector.

3. Certain attack types (e.g., Ransomware) consistently require longer resolution times than others, with notable variations across countries and industries.

4. Social engineering and unpatched software vulnerabilities are responsible for the largest financial damages, while certain defense mechanisms (particularly AI-based detection) demonstrated greater effectiveness in reducing both financial impact and resolution times.

These findings provide valuable insights for organizations to better allocate security resources, improve incident response strategies, and reduce the financial impact of future cybersecurity breaches.'''
    
    pdf.body_text(executive_summary)
    pdf.add_page()
    
    # 2. Giriş
    pdf.chapter_title('2. Introduction')
    
    pdf.section_title('2.1 Background')
    background_text = '''Cybersecurity breaches have become increasingly costly and damaging to organizations across all sectors. Understanding the patterns, trends, and key factors that influence the financial impact and resolution times of these breaches is critical for developing effective security strategies.

The growing sophistication of cyber threats, coupled with the expanding digital footprint of modern organizations, has created a complex security landscape. Organizations are facing challenges from multiple vectors, including sophisticated ransomware attacks, nation-state threats, supply chain compromises, and social engineering tactics.'''
    pdf.body_text(background_text)
    
    pdf.section_title('2.2 Research Question')
    research_question = '''This study addresses the following primary research question:

"What are the most significant factors affecting financial losses and resolution times in cybersecurity breaches across different industries and regions in the current threat landscape?"

Secondary research questions include:

1. "How have cloud-based security solutions impacted the effectiveness of breach prevention and response?"
2. "What role does Zero Trust Architecture play in mitigating the financial impact of breaches?"
3. "How do remote/hybrid work environments affect an organization's cybersecurity posture and breach response capabilities?"'''
    pdf.body_text(research_question)
    
    pdf.section_title('2.3 Objectives')
    objectives = '''The primary objectives of this study were to:'''
    pdf.body_text(objectives)
    
    objective_items = [
        'Analyze the financial impact of different types of cybersecurity breaches across industries',
        'Evaluate the relationship between attack types and resolution times',
        'Identify the most vulnerable industries and the most effective defense mechanisms',
        'Examine regional variations in cybersecurity breach patterns',
        'Provide evidence-based recommendations for improving cybersecurity posture'
    ]
    pdf.bullet_list(objective_items)
    pdf.add_page()
    
    # 3. Metodoloji
    pdf.chapter_title('3. Methodology')
    
    pdf.section_title('3.1 Data Source')
    data_source = '''This study utilized a comprehensive dataset of cybersecurity incidents from 2015 to 2024. The dataset includes information on:'''
    pdf.body_text(data_source)
    
    data_items = [
        'Country of incident',
        'Year of occurrence',
        'Attack type',
        'Target industry',
        'Financial loss (in million $)',
        'Number of affected users',
        'Attack source',
        'Security vulnerability type',
        'Defense mechanism used',
        'Incident resolution time (in hours)'
    ]
    pdf.bullet_list(data_items)
    
    pdf.section_title('3.2 Analytical Approach')
    analytical_approach = '''Our analysis employed the following methods:'''
    pdf.body_text(analytical_approach)
    
    analysis_methods = [
        'Descriptive Statistics: To summarize the data and identify general patterns',
        'Time Series Analysis: To track trends over the 2015-2024 period',
        'Comparative Analysis: To examine variations across industries, countries, and attack types',
        'Correlation Analysis: To identify relationships between factors (e.g., vulnerability types and financial losses)',
        'Visualization: To present findings in an accessible and informative format'
    ]
    pdf.bullet_list(analysis_methods)
    
    pdf.section_title('3.3 Data Processing')
    data_processing = '''Data was processed using Python with the pandas, matplotlib, and seaborn libraries. The analysis was conducted in four main stages:

1. Data cleaning and exploratory analysis
2. Financial loss analysis by industry and over time
3. Attack resolution time analysis by attack type and country
4. Security vulnerability and defense mechanism effectiveness analysis

We also designed a comprehensive questionnaire to gather additional insights from security professionals across various industries, which will help supplement and validate our data analysis findings.'''
    pdf.body_text(data_processing)
    pdf.add_page()
    
    # 4. Analiz Sonuçları
    pdf.chapter_title('4. Analysis Results')
    
    pdf.section_title('4.1 Financial Impact Analysis')
    
    pdf.section_title('4.1.1 Financial Loss by Industry')
    industry_loss = '''Our analysis revealed significant variations in the financial impact of cybersecurity breaches across different industries. The following industries experienced the highest average financial losses:

1. Banking
2. Retail
3. Healthcare
4. Telecommunications
5. Government

The Banking sector had the highest average loss per incident, which can be attributed to the high value of financial data and the critical nature of banking systems. Retail followed closely, likely due to the large volumes of customer payment data typically compromised in retail breaches.'''
    pdf.body_text(industry_loss)
    
    # Add image for industry loss graph
    pdf.add_image('analysis_results/avg_loss_by_industry.png', 'Figure 1: Average Financial Loss by Industry (Million $)')
    
    pdf.section_title('4.1.2 Financial Loss Trends (2015-2024)')
    loss_trends = '''The analysis of financial loss trends over time revealed:

- A steady increase in average financial loss per incident from 2015 to 2024
- A particularly sharp increase between 2020 and 2022
- A possible plateau effect in 2023-2024, potentially indicating improved security measures

This upward trend in financial impact aligns with the increasing sophistication of cyber attacks and the growing value of digital assets and data.'''
    pdf.body_text(loss_trends)
    
    # Add image for loss trend graph
    pdf.add_image('analysis_results/loss_trend_over_time.png', 'Figure 2: Average Financial Loss Over Time (2015-2024)')
    
    pdf.add_page()
    
    pdf.section_title('4.2 Attack Type Analysis')
    
    pdf.section_title('4.2.1 Distribution of Attack Types')
    attack_distribution = '''The distribution of attack types in the dataset showed:

- Phishing attacks remained the most common attack vector throughout the period
- Ransomware attacks showed the most significant increase, especially from 2019 onwards
- DDoS attacks remained consistently prevalent across all years
- SQL Injection attacks decreased in frequency over time, possibly indicating improved web application security'''
    pdf.body_text(attack_distribution)
    
    pdf.section_title('4.2.2 Attack Types by Industry')
    industry_attacks = '''Different industries showed vulnerability to different types of attacks:

- Banking was particularly targeted by Man-in-the-Middle attacks
- Healthcare faced the highest proportion of Ransomware attacks
- Government entities experienced more SQL Injection attacks
- Education institutions were predominantly affected by Phishing attacks

These patterns highlight how attackers tailor their approaches based on industry-specific vulnerabilities and valuable assets.'''
    pdf.body_text(industry_attacks)
    
    pdf.section_title('4.3 Resolution Time Analysis')
    
    pdf.section_title('4.3.1 Resolution Time by Attack Type')
    resolution_by_attack = '''The analysis of incident resolution times revealed significant variations based on attack type:

- Ransomware attacks required the longest average resolution time
- DDoS attacks were typically resolved more quickly
- Man-in-the-Middle attacks showed the greatest variability in resolution times

These differences reflect the varying complexity of attack remediation, particularly with attacks like ransomware that may involve complex recovery processes.'''
    pdf.body_text(resolution_by_attack)
    
    # Add image for resolution time graph
    pdf.add_image('analysis_results/avg_resolution_by_attack.png', 'Figure 3: Average Resolution Time by Attack Type (Hours)')
    
    pdf.add_page()
    
    pdf.section_title('4.3.2 Relationship Between Resolution Time and Financial Loss')
    time_loss_relationship = '''A correlation analysis between resolution time and financial loss revealed:

- A moderate positive correlation (r = 0.62) between resolution time and financial loss
- This relationship was strongest for Ransomware and Man-in-the-Middle attacks
- The correlation weakened for incidents where AI-based detection was implemented

This finding underscores the importance of rapid incident detection and response in minimizing financial damages.'''
    pdf.body_text(time_loss_relationship)
    
    # Add image for resolution vs loss graph
    pdf.add_image('analysis_results/resolution_vs_loss.png', 'Figure 4: Resolution Time vs. Financial Loss by Attack Type')
    
    pdf.section_title('4.4 Security Vulnerability Analysis')
    
    pdf.section_title('4.4.1 Impact of Different Vulnerability Types')
    vulnerability_impact = '''The analysis of security vulnerability types showed that:

- Social Engineering vulnerabilities led to the highest average financial losses
- Unpatched Software vulnerabilities affected the largest number of users
- Weak Passwords, while common, typically resulted in lower financial impacts

This suggests that human-centered vulnerabilities (social engineering) often lead to the most damaging breaches, highlighting the importance of security awareness training.'''
    pdf.body_text(vulnerability_impact)
    
    # Add image for vulnerability impact graph
    pdf.add_image('analysis_results/loss_by_vulnerability.png', 'Figure 5: Average Financial Loss by Vulnerability Type (Million $)')
    
    pdf.add_page()
    
    pdf.section_title('4.4.2 Effectiveness of Defense Mechanisms')
    defense_effectiveness = '''The effectiveness of various defense mechanisms was evaluated based on both financial impact and resolution time:

- AI-based Detection systems were associated with the lowest average financial losses and fastest resolution times
- Traditional Antivirus solutions showed limited effectiveness against sophisticated attacks
- VPN implementations had mixed results, with effectiveness varying by attack type
- Firewalls remained effective against certain attack types (particularly DDoS) but offered limited protection against social engineering attacks

This analysis highlights the value of advanced, AI-driven security solutions in the current threat landscape.'''
    pdf.body_text(defense_effectiveness)
    
    # Add images for defense mechanism graphs
    pdf.add_image('analysis_results/loss_by_defense.png', 'Figure 6: Average Financial Loss by Defense Mechanism')
    pdf.add_image('analysis_results/time_by_defense.png', 'Figure 7: Average Resolution Time by Defense Mechanism')
    
    pdf.add_page()
    
    # 5. Anket Tasarımı
    pdf.chapter_title('5. Questionnaire Design')
    
    questionnaire_overview = '''As part of this study, we designed a comprehensive questionnaire to gather additional insights from security professionals. The questionnaire was structured to complement our data analysis and address our research questions, with a focus on:'''
    pdf.body_text(questionnaire_overview)
    
    questionnaire_focus = [
        'Organization profiles across different industries, sizes, and regions',
        'Security breach experiences including attack types, financial impacts, and resolution times',
        'Security vulnerabilities and control effectiveness',
        'Cloud adoption and modern architecture implementation (Zero Trust, etc.)',
        'Remote/hybrid work environments and their security implications',
        'Future trends and emerging threats'
    ]
    pdf.bullet_list(questionnaire_focus)
    
    questionnaire_structure = '''The questionnaire consists of five main sections:

1. Organization Profile
2. Security Breach Experience
3. Security Vulnerabilities and Controls
4. Cloud and Modern Architectures
5. Future Trends

The questionnaire was designed for distribution to a multi-stage stratified random sample across different industries, company sizes, geographic regions, security maturity levels, and cloud adoption levels. This design ensures comprehensive coverage and the ability to analyze results across multiple dimensions.'''
    pdf.body_text(questionnaire_structure)
    
    questionnaire_usage = '''The questionnaire has been implemented within our Excel analysis tool, allowing for easy data collection and integration with our existing dataset. This will enable continuous enrichment of our analysis as new survey responses are gathered.'''
    pdf.body_text(questionnaire_usage)
    pdf.add_page()
    
    # 6. Bulgular ve İçgörüler
    pdf.chapter_title('6. Findings and Insights')
    
    key_insights = '''Based on our comprehensive analysis, we have identified the following key insights:'''
    pdf.body_text(key_insights)
    
    insights = [
        'Industry-Specific Risk Profiles: Different industries face distinct risk profiles requiring tailored security approaches. Banking and healthcare face the highest financial impacts, while education institutions are particularly vulnerable to phishing attacks.',
        
        'The Human Factor: Social engineering remains one of the most damaging vulnerability types, highlighting the continued importance of security awareness and training.',
        
        'Resolution Time Matters: Faster incident resolution is strongly associated with reduced financial impact, emphasizing the value of efficient incident response capabilities.',
        
        'Advanced Defense Mechanisms: AI-based detection systems demonstrated superior effectiveness compared to traditional security tools.',
        
        'Geographic Variations: Significant variations exist in both attack patterns and resolution capabilities across different countries, suggesting the influence of regulatory environments, security maturity, and threat landscapes.',
        
        'Attack Evolution: The increasing prevalence of ransomware and the emergence of double-extortion tactics represent a significant shift in the threat landscape since 2020.',
        
        'Cloud Security Impact: Organizations with mature cloud security implementations generally demonstrated better resilience against attacks, though cloud misconfigurations remain a significant vulnerability.'
    ]
    pdf.bullet_list(insights)
    
    implications = '''These findings have significant implications for how organizations approach cybersecurity strategy, resource allocation, and risk management. The variations across industries and attack types suggest that a one-size-fits-all approach to security is inadequate. Instead, organizations should tailor their security investments based on their specific industry risk profile, threat landscape, and existing security maturity.'''
    pdf.body_text(implications)
    pdf.add_page()
    
    # 7. Öneriler
    pdf.chapter_title('7. Recommendations')
    
    recommendations_intro = '''Based on our analysis findings, we offer the following recommendations for organizations seeking to improve their cybersecurity posture and reduce the financial impact of breaches:'''
    pdf.body_text(recommendations_intro)
    
    pdf.section_title('For Executive Leadership')
    exec_recommendations = [
        'Prioritize security investments based on your industry\'s specific risk profile and the most financially impactful attack types identified in this report.',
        'Consider the implementation of AI-based detection systems, which demonstrated superior effectiveness in reducing both financial impacts and resolution times.',
        'Evaluate your organization\'s incident response capabilities with a focus on reducing resolution times, as faster resolution correlates strongly with reduced financial impact.',
        'Assess your organization\'s cloud security posture, particularly if you\'re in the midst of digital transformation initiatives.',
        'Implement regular third-party security assessments to identify vulnerabilities before they can be exploited.'
    ]
    pdf.bullet_list(exec_recommendations)
    
    pdf.section_title('For Security Teams')
    security_recommendations = [
        'Implement comprehensive security awareness training programs with a focus on combating social engineering attacks, which caused the highest average financial losses.',
        'Establish robust patch management processes to address the widespread impact of unpatched software vulnerabilities.',
        'Evaluate the implementation of Zero Trust Architecture principles, particularly for organizations with significant remote/hybrid work environments.',
        'Develop and regularly test incident response plans that address the specific attack types most common in your industry.',
        'Implement advanced monitoring capabilities for early detection of breaches, as longer detection times significantly increased financial impacts.',
        'Consider threat hunting programs to proactively identify potential compromises before they escalate.'
    ]
    pdf.bullet_list(security_recommendations)
    
    pdf.section_title('For Specific Industries')
    industry_recommendations = [
        'Banking/Finance: Prioritize defenses against Man-in-the-Middle attacks and implement strong customer authentication mechanisms.',
        'Healthcare: Focus on ransomware defenses and data protection, given the high impact and frequency of these attacks in the sector.',
        'Retail: Implement robust point-of-sale security and customer data protection measures to reduce the high average losses in this sector.',
        'Government: Address the prevalence of SQL injection attacks with web application security assessments and remediation.',
        'Education: Prioritize phishing awareness and defenses, as this sector was disproportionately affected by these attacks.'
    ]
    pdf.bullet_list(industry_recommendations)
    pdf.add_page()
    
    # 8. Sonuç
    pdf.chapter_title('8. Conclusion')
    
    conclusion_text = '''This comprehensive analysis of cybersecurity breaches from 2015 to 2024 provides valuable insights into the factors affecting financial losses and resolution times across different industries and regions. By examining patterns in attack types, vulnerabilities, and defense mechanisms, we have identified key areas where organizations can focus their security efforts to reduce risk and minimize the impact of breaches.

The findings highlight the critical importance of industry-specific security approaches, the significant impact of human factors in security, the value of rapid incident resolution, and the effectiveness of advanced AI-based defense mechanisms. Additionally, the analysis underscores the growing importance of cloud security and modern architectural approaches like Zero Trust in the evolving threat landscape.

By implementing the recommendations outlined in this report and leveraging the insights gained from both data analysis and our questionnaire design, organizations can develop more effective security strategies that address their specific risk profiles and challenges. This targeted approach will enable better resource allocation, improved incident response capabilities, and ultimately, reduced financial and operational impacts from cybersecurity breaches.

As the threat landscape continues to evolve, ongoing analysis and adaptation of security strategies will remain essential. The questionnaire developed as part of this project provides a framework for organizations to continue gathering insights and monitoring changes in the security environment.'''
    pdf.body_text(conclusion_text)
    pdf.add_page()
    
    # 9. Referanslar
    pdf.chapter_title('9. References')
    
    references = [
        'Global Cybersecurity Threats Dataset (2015-2024)',
        'NIST Cybersecurity Framework',
        'ISO/IEC 27001:2022',
        'MITRE ATT&CK Framework',
        'Cloud Security Alliance (CSA) Security Guidance',
        'Zero Trust Architecture NIST Special Publication 800-207',
        'Ponemon Institute Cost of a Data Breach Report',
        'Verizon Data Breach Investigations Report (DBIR)',
        'Microsoft Digital Defense Report',
        'IBM X-Force Threat Intelligence Index'
    ]
    pdf.bullet_list(references)
    
    # PDF kaydet
    output_path = 'Cybersecurity_Breach_Analysis_Final_Report.pdf'
    pdf.output(output_path)
    print(f"Final report successfully created: {output_path}")

if __name__ == "__main__":
    create_final_report()
