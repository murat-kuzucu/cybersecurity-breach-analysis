from fpdf import FPDF
import os
from datetime import datetime

class PDF(FPDF):
    def header(self):
        # Set header with title
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'CYBERSECURITY BREACH ANALYSIS QUESTIONNAIRE', 0, 1, 'C')
        self.ln(5)
        
    def footer(self):
        # Set footer with page number
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
        
    def create_section(self, title):
        # Create a section with title
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 8, title, 1, 1, 'L', True)
        self.ln(4)
        
    def create_question(self, question_text):
        # Create a question
        self.set_font('Arial', 'B', 10)
        self.multi_cell(0, 6, question_text)
        self.ln(1)
        
    def create_options(self, options, per_row=2):
        # Create multiple choice options
        self.set_font('Arial', '', 10)
        width = 190 / per_row
        
        for i, option in enumerate(options):
            option_text = "[ ] " + option
            self.cell(width, 6, option_text, 0, 0)
            if (i + 1) % per_row == 0:
                self.ln(8)
                
        # If the last row is incomplete, add a line break
        if len(options) % per_row != 0:
            self.ln(8)
        self.ln(2)
    
    def create_text_field(self, lines=5):
        # Create a multi-line text field
        self.set_font('Arial', '', 10)
        for i in range(lines):
            self.cell(0, 7, "_" * 90, 0, 1)
        self.ln(3)

def generate_cybersecurity_questionnaire():
    # Initialize PDF
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Cover page
    pdf.set_font('Arial', 'B', 24)
    pdf.ln(40)
    pdf.cell(0, 10, "CYBERSECURITY BREACH", 0, 1, 'C')
    pdf.cell(0, 10, "ANALYSIS QUESTIONNAIRE", 0, 1, 'C')
    
    pdf.ln(20)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, "For Comprehensive Data Collection and Analysis", 0, 1, 'C')
    
    # Öğrenci bilgileri
    pdf.ln(30)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, "Student: 190444041 Murat KUZUCU", 0, 1, 'C')
    pdf.cell(0, 10, "Course: CENG 418", 0, 1, 'C')
    
    pdf.ln(20)
    pdf.set_font('Arial', 'I', 10)
    current_date = datetime.now().strftime("%B %d, %Y")
    pdf.cell(0, 10, f"Created: {current_date}", 0, 1, 'C')
    
    # Page 1: Basic Information
    pdf.add_page()
    pdf.create_section("1. BASIC INFORMATION")
    
    pdf.create_question("1.1. Organization/Company Name:")
    pdf.create_text_field(1)
    
    pdf.create_question("1.2. Country:")
    pdf.create_text_field(1)
    
    pdf.create_question("1.3. Year of Breach:")
    pdf.create_text_field(1)
    
    pdf.create_question("1.4. Industry Sector:")
    industry_sectors = [
        "Finance", "Healthcare", "Retail", "Technology", 
        "Manufacturing", "Education", "Government", "Energy",
        "Telecommunications", "Other"
    ]
    pdf.create_options(industry_sectors, 3)
    
    pdf.create_question("1.5. Organization Size:")
    org_sizes = [
        "Small (<50 employees)", 
        "Medium (50-250 employees)", 
        "Large (251-1000 employees)", 
        "Enterprise (>1000 employees)"
    ]
    pdf.create_options(org_sizes, 2)
    
    # Page 2: Attack Details
    pdf.add_page()
    pdf.create_section("2. ATTACK DETAILS")
    
    pdf.create_question("2.1. Attack Type (Select all that apply):")
    attack_types = [
        "Ransomware", "DDoS", "Phishing", "SQL Injection", 
        "Man-in-the-Middle", "Malware", "Password Attack", 
        "Cross-site Scripting", "Zero-day Exploit", "Insider Threat", 
        "Business Email Compromise", "Other"
    ]
    pdf.create_options(attack_types, 2)
    
    pdf.create_question("2.2. Attack Source:")
    attack_sources = [
        "State-Sponsored Actors", "Hacktivists", "Organized Crime", 
        "Independent Hackers", "Insider Threat", "Unknown", "Other"
    ]
    pdf.create_options(attack_sources, 2)
    
    pdf.create_question("2.3. Security Vulnerability Type:")
    vulnerabilities = [
        "Software Vulnerability", "Hardware Vulnerability", 
        "Configuration Error", "Social Engineering", 
        "Outdated Systems", "Weak Authentication", 
        "Lack of Encryption", "Missing Patches", "Other"
    ]
    pdf.create_options(vulnerabilities, 2)
    
    # Page 3: Impact Analysis
    pdf.add_page()
    pdf.create_section("3. IMPACT ANALYSIS")
    
    pdf.create_question("3.1. Financial Loss (in Million $):")
    financial_loss = ["<1", "1-5", "5-10", "10-50", "50-100", ">100", "Unknown"]
    pdf.create_options(financial_loss, 4)
    
    pdf.create_question("3.2. Number of Affected Users:")
    affected_users = [
        "<1,000", "1,000-10,000", "10,000-100,000", 
        "100,000-1,000,000", ">1,000,000", "Unknown"
    ]
    pdf.create_options(affected_users, 3)
    
    pdf.create_question("3.3. Financial Impact Category:")
    impact_category = ["Low", "Medium", "High", "Critical", "Not Applicable"]
    pdf.create_options(impact_category, 3)
    
    pdf.create_question("3.4. Type of Data Compromised (Select all that apply):")
    data_types = [
        "Personal Information (PII)", "Payment Card Information", 
        "Health Information", "Intellectual Property", 
        "Authentication Credentials", "Confidential Information",
        "Email Content", "Customer Records", "Other"
    ]
    pdf.create_options(data_types, 2)
    
    # Page 4: Response and Resolution
    pdf.add_page()
    pdf.create_section("4. INCIDENT RESPONSE AND RESOLUTION")
    
    pdf.create_question("4.1. Defense Mechanism Used:")
    defense_mechanisms = [
        "AI-Based Threat Detection", "Firewall", "DDoS Protection", 
        "Access Control", "Data Encryption", "EDR Solution", 
        "SIEM System", "Multi-factor Authentication",
        "Intrusion Prevention", "Endpoint Protection", "Other"
    ]
    pdf.create_options(defense_mechanisms, 2)
    
    pdf.create_question("4.2. Incident Resolution Time (Hours):")
    resolution_time = ["<24", "24-48", "48-72", "72-168", ">168", "Ongoing"]
    pdf.create_options(resolution_time, 3)
    
    pdf.create_question("4.3. Detection Time Category:")
    detection_time = [
        "Immediate (minutes)", "Quick (hours)", "Medium (days)", 
        "Late (weeks)", "Very Late (months)", "Unknown"
    ]
    pdf.create_options(detection_time, 2)
    
    pdf.create_question("4.4. Detection Method:")
    detection_methods = [
        "Internal Security Team", "Security Product Alert", 
        "External Notification", "Anomaly Detection", 
        "Routine Audit", "User Report", 
        "Third-Party Security Service", "Other"
    ]
    pdf.create_options(detection_methods, 2)
    
    # Page 5: Security Posture
    pdf.add_page()
    pdf.create_section("5. SECURITY POSTURE AND INFRASTRUCTURE")
    
    pdf.create_question("5.1. Security Posture Assessment:")
    security_posture = ["Basic", "Intermediate", "Advanced", "Leading"]
    pdf.create_options(security_posture, 4)
    
    pdf.create_question("5.2. Cloud Adoption Level:")
    cloud_adoption = ["None", "Minimal", "Moderate", "High", "Full Cloud"]
    pdf.create_options(cloud_adoption, 5)
    
    pdf.create_question("5.3. Security Measures in Place Before the Incident:")
    security_measures = [
        "Regular Security Assessments", "Penetration Testing", 
        "Employee Security Training", "Incident Response Plan", 
        "Data Backup Strategy", "Patch Management Process",
        "Network Segmentation", "Access Control Policies", "Other"
    ]
    pdf.create_options(security_measures, 2)
    
    # Page 6: Additional Information
    pdf.add_page()
    pdf.create_section("6. ADDITIONAL INFORMATION")
    
    pdf.create_question("6.1. Please describe key lessons learned from this incident:")
    pdf.create_text_field(8)
    
    pdf.create_question("6.2. Please describe any additional details about the incident:")
    pdf.create_text_field(8)
    
    # Page 7: Confirmation
    pdf.add_page()
    pdf.create_section("CONFIRMATION")
    
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 6, "I confirm that all information provided in this questionnaire is accurate and complete to the best of my knowledge. I understand that this information will be used for cybersecurity analysis purposes.")
    pdf.ln(20)
    
    # Öğrenci bilgileri tekrar
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 10, "Prepared by:", 0, 1)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 10, "Student ID: 190444041", 0, 1)
    pdf.cell(0, 10, "Name: Murat KUZUCU", 0, 1)
    pdf.cell(0, 10, "Course: CENG 418", 0, 1)
    pdf.ln(10)
    
    pdf.create_question("Date:")
    pdf.create_text_field(1)
    
    pdf.create_question("Signature:")
    pdf.create_text_field(1)
    
    # Save the PDF
    docsPath = os.path.join(os.getcwd(), 'docs')
    if not os.path.exists(docsPath):
        os.makedirs(docsPath)
    
    pdfPath = os.path.join(docsPath, 'questionnaire.pdf')
    pdf.output(pdfPath)
    
    print(f"Updated questionnaire created: {pdfPath}")
    
    # Move script to trash-bin after execution
    script_path = os.path.realpath(__file__)
    trash_bin = os.path.join(os.getcwd(), 'trash-bin')
    if not os.path.exists(trash_bin):
        os.makedirs(trash_bin)
    
    try:
        import shutil
        filename = os.path.basename(script_path)
        target_path = os.path.join(trash_bin, filename)
        shutil.copy2(script_path, target_path)
        
        # Also move previous questionnaire scripts if they exist
        for prev_script_name in ['simple_questionnaire.py', 'create_questionnaire.py', 'improve_questionnaire.py']:
            prev_script = os.path.join(os.getcwd(), prev_script_name)
            if os.path.exists(prev_script):
                shutil.copy2(prev_script, os.path.join(trash_bin, prev_script_name))
                os.remove(prev_script)
        
        print(f"Script files moved to trash-bin")
    except Exception as e:
        print(f"Note: Could not move script to trash-bin: {e}")

if __name__ == "__main__":
    generate_cybersecurity_questionnaire()
