import pandas as pd
import numpy as np
from pathlib import Path
import os

def create_analysis_report():
    # camelCase kullanımına dikkat edelim
    dataPath = Path('data/RAW-cybersecurity_breach_data.csv')
    
    # Veri setini yükle
    if dataPath.exists():
        df = pd.read_csv(dataPath)
        print(f"Loaded data with {len(df)} records from {dataPath}")
    else:
        print(f"Data file not found at {dataPath}")
        return
    
    # Excel dosyasını oluştur
    outputPath = 'data/analysis_report.xlsx'
    writer = pd.ExcelWriter(outputPath, engine='xlsxwriter')
    workbook = writer.book
    
    # Formatları tanımla
    headerFormat = workbook.add_format({
        'bold': True,
        'font_color': 'white',
        'bg_color': '#2F75B5',
        'align': 'center',
        'valign': 'vcenter',
        'border': 1
    })
    
    numberFormat = workbook.add_format({
        'num_format': '#,##0',
        'align': 'center'
    })
    
    percentFormat = workbook.add_format({
        'num_format': '0.00%',
        'align': 'center'
    })
    
    currencyFormat = workbook.add_format({
        'num_format': '$#,##0.00',
        'align': 'center'
    })
    
    boldFormat = workbook.add_format({
        'bold': True,
        'align': 'center'
    })
    
    # 1. Özet Sayfası
    summarySheet = workbook.add_worksheet('Summary')
    
    # Toplam saldırı sayısı
    totalAttacks = len(df)
    
    # Finansal kayıp ortalaması
    avgFinancialLoss = df['Financial Loss (in Million $)'].mean()
    
    # En yaygın saldırı türü
    mostCommonAttack = df['Attack Type'].value_counts().idxmax()
    
    # En çok etkilenen sektör
    mostAffectedIndustry = df['Target Industry Standardized'].value_counts().idxmax()
    
    # En uzun çözüm süresine sahip saldırı türü
    avgResolutionByAttack = df.groupby('Attack Type')['Incident Resolution Time (in Hours)'].mean()
    longestResolutionAttack = avgResolutionByAttack.idxmax()
    
    # Özet tablo
    summaryData = [
        ['Total Cybersecurity Incidents', totalAttacks],
        ['Average Financial Loss (Million $)', avgFinancialLoss],
        ['Most Common Attack Type', mostCommonAttack],
        ['Most Affected Industry', mostAffectedIndustry],
        ['Attack Type with Longest Resolution Time', longestResolutionAttack]
    ]
    
    summarySheet.write_row('A1', ['Key Metrics', 'Value'], headerFormat)
    for i, row in enumerate(summaryData):
        summarySheet.write(i+1, 0, row[0], boldFormat)
        if isinstance(row[1], (int, float)) and i != 0:
            if i == 1:  # Financial loss
                summarySheet.write(i+1, 1, row[1], currencyFormat)
            else:
                summarySheet.write(i+1, 1, row[1], numberFormat)
        else:
            summarySheet.write(i+1, 1, row[1])
    
    # Sütun genişliklerini ayarla
    summarySheet.set_column('A:A', 35)
    summarySheet.set_column('B:B', 25)
    
    # 2. Finansal Etki Sayfası
    financialSheet = workbook.add_worksheet('Financial Impact')
    
    # Sektöre göre ortalama finansal kayıp
    financialByIndustry = df.groupby('Target Industry Standardized')['Financial Loss (in Million $)'].agg(['mean', 'sum', 'count']).reset_index()
    financialByIndustry = financialByIndustry.sort_values('sum', ascending=False)
    
    # Sektör bazlı finansal tablo
    financialSheet.write_row('A1', ['Industry', 'Average Loss (Million $)', 'Total Loss (Million $)', 'Incident Count'], headerFormat)
    
    for i, row in financialByIndustry.iterrows():
        financialSheet.write(i+1, 0, row['Target Industry Standardized'])
        financialSheet.write(i+1, 1, row['mean'], currencyFormat)
        financialSheet.write(i+1, 2, row['sum'], currencyFormat)
        financialSheet.write(i+1, 3, row['count'], numberFormat)
    
    # Sektör başına toplam kaybı gösteren formül
    formulaRow = len(financialByIndustry) + 2
    financialSheet.write(formulaRow, 0, 'Total', boldFormat)
    financialSheet.write_formula(formulaRow, 1, f'=AVERAGE(B2:B{formulaRow-1})', currencyFormat)
    financialSheet.write_formula(formulaRow, 2, f'=SUM(C2:C{formulaRow-1})', currencyFormat)
    financialSheet.write_formula(formulaRow, 3, f'=SUM(D2:D{formulaRow-1})', numberFormat)
    
    # Sütun genişliklerini ayarla
    financialSheet.set_column('A:A', 25)
    financialSheet.set_column('B:D', 20)
    
    # 3. Saldırı Analizi Sayfası
    attackSheet = workbook.add_worksheet('Attack Analysis')
    
    # Saldırı türüne göre istatistikler
    attackStats = df.groupby('Attack Type').agg({
        'Financial Loss (in Million $)': ['mean', 'sum'],
        'Incident Resolution Time (in Hours)': 'mean',
        'Attack Type': 'count'
    }).reset_index()
    
    attackStats.columns = ['Attack Type', 'Avg Loss', 'Total Loss', 'Avg Resolution Time', 'Count']
    attackStats = attackStats.sort_values('Count', ascending=False)
    
    # Saldırı analizi tablosu
    attackSheet.write_row('A1', ['Attack Type', 'Average Loss (Million $)', 'Total Loss (Million $)', 
                                 'Avg Resolution Time (Hours)', 'Incident Count'], headerFormat)
    
    for i, row in attackStats.iterrows():
        attackSheet.write(i+1, 0, row['Attack Type'])
        attackSheet.write(i+1, 1, row['Avg Loss'], currencyFormat)
        attackSheet.write(i+1, 2, row['Total Loss'], currencyFormat)
        attackSheet.write(i+1, 3, row['Avg Resolution Time'], numberFormat)
        attackSheet.write(i+1, 4, row['Count'], numberFormat)
    
    # Toplamlar/ortalamalar için formül
    formulaRow = len(attackStats) + 2
    attackSheet.write(formulaRow, 0, 'Total/Average', boldFormat)
    attackSheet.write_formula(formulaRow, 1, f'=AVERAGE(B2:B{formulaRow-1})', currencyFormat)
    attackSheet.write_formula(formulaRow, 2, f'=SUM(C2:C{formulaRow-1})', currencyFormat)
    attackSheet.write_formula(formulaRow, 3, f'=AVERAGE(D2:D{formulaRow-1})', numberFormat)
    attackSheet.write_formula(formulaRow, 4, f'=SUM(E2:E{formulaRow-1})', numberFormat)
    
    # Sütun genişliklerini ayarla
    attackSheet.set_column('A:A', 25)
    attackSheet.set_column('B:E', 22)
    
    # 4. Savunma Mekanizması Analizi
    defenseSheet = workbook.add_worksheet('Defense Mechanisms')
    
    # Savunma mekanizmalarına göre istatistikler
    defenseStats = df.groupby('Defense Mechanism Used').agg({
        'Financial Loss (in Million $)': ['mean', 'sum'],
        'Incident Resolution Time (in Hours)': 'mean',
        'Defense Mechanism Used': 'count'
    }).reset_index()
    
    defenseStats.columns = ['Defense Mechanism', 'Avg Loss', 'Total Loss', 'Avg Resolution Time', 'Count']
    defenseStats = defenseStats.sort_values('Avg Resolution Time')
    
    # Savunma mekanizması tablosu
    defenseSheet.write_row('A1', ['Defense Mechanism', 'Average Loss (Million $)', 'Total Loss (Million $)', 
                                 'Avg Resolution Time (Hours)', 'Incident Count'], headerFormat)
    
    for i, row in defenseStats.iterrows():
        defenseSheet.write(i+1, 0, row['Defense Mechanism'])
        defenseSheet.write(i+1, 1, row['Avg Loss'], currencyFormat)
        defenseSheet.write(i+1, 2, row['Total Loss'], currencyFormat)
        defenseSheet.write(i+1, 3, row['Avg Resolution Time'], numberFormat)
        defenseSheet.write(i+1, 4, row['Count'], numberFormat)
    
    # Toplamlar/ortalamalar için formül
    formulaRow = len(defenseStats) + 2
    defenseSheet.write(formulaRow, 0, 'Total/Average', boldFormat)
    defenseSheet.write_formula(formulaRow, 1, f'=AVERAGE(B2:B{formulaRow-1})', currencyFormat)
    defenseSheet.write_formula(formulaRow, 2, f'=SUM(C2:C{formulaRow-1})', currencyFormat)
    defenseSheet.write_formula(formulaRow, 3, f'=AVERAGE(D2:D{formulaRow-1})', numberFormat)
    defenseSheet.write_formula(formulaRow, 4, f'=SUM(E2:E{formulaRow-1})', numberFormat)
    
    # Sütun genişliklerini ayarla
    defenseSheet.set_column('A:A', 25)
    defenseSheet.set_column('B:E', 22)
    
    # 5. Yıllık Trend Analizi
    trendSheet = workbook.add_worksheet('Yearly Trends')
    
    # Yıla göre istatistikler
    yearlyStats = df.groupby('Year').agg({
        'Financial Loss (in Million $)': ['mean', 'sum'],
        'Incident Resolution Time (in Hours)': 'mean',
        'Year': 'count'
    }).reset_index()
    
    yearlyStats.columns = ['Year', 'Avg Loss', 'Total Loss', 'Avg Resolution Time', 'Incident Count']
    yearlyStats = yearlyStats.sort_values('Year')
    
    # Yıllık trend tablosu
    trendSheet.write_row('A1', ['Year', 'Average Loss (Million $)', 'Total Loss (Million $)', 
                                'Avg Resolution Time (Hours)', 'Incident Count', 'YoY Growth %'], headerFormat)
    
    for i, row in yearlyStats.iterrows():
        trendSheet.write(i+1, 0, row['Year'], numberFormat)
        trendSheet.write(i+1, 1, row['Avg Loss'], currencyFormat)
        trendSheet.write(i+1, 2, row['Total Loss'], currencyFormat)
        trendSheet.write(i+1, 3, row['Avg Resolution Time'], numberFormat)
        trendSheet.write(i+1, 4, row['Incident Count'], numberFormat)
    
    # Yıllık artış oranı hesaplama (formül ile)
    for i in range(1, len(yearlyStats)):
        rowNum = i + 2  # i+1 for zero-indexing and +1 for header
        prevRowNum = rowNum - 1
        trendSheet.write_formula(rowNum-1, 5, f'=(C{rowNum}/C{prevRowNum})-1', percentFormat)
    
    # Sütun genişliklerini ayarla
    trendSheet.set_column('A:A', 15)
    trendSheet.set_column('B:F', 22)
    
    # 6. Ülke Analizi
    countrySheet = workbook.add_worksheet('Country Analysis')
    
    # Ülkelere göre istatistikler
    countryStats = df.groupby('Country').agg({
        'Financial Loss (in Million $)': ['mean', 'sum'],
        'Incident Resolution Time (in Hours)': 'mean',
        'Country': 'count'
    }).reset_index()
    
    countryStats.columns = ['Country', 'Avg Loss', 'Total Loss', 'Avg Resolution Time', 'Incident Count']
    countryStats = countryStats.sort_values('Incident Count', ascending=False).head(15)  # Top 15 ülke
    
    # Ülke analizi tablosu
    countrySheet.write_row('A1', ['Country', 'Average Loss (Million $)', 'Total Loss (Million $)', 
                                'Avg Resolution Time (Hours)', 'Incident Count'], headerFormat)
    
    for i, row in countryStats.iterrows():
        countrySheet.write(i+1, 0, row['Country'])
        countrySheet.write(i+1, 1, row['Avg Loss'], currencyFormat)
        countrySheet.write(i+1, 2, row['Total Loss'], currencyFormat)
        countrySheet.write(i+1, 3, row['Avg Resolution Time'], numberFormat)
        # DÜZELTME: 'Count' yerine 'Incident Count' kullanıldı
        countrySheet.write(i+1, 4, row['Incident Count'], numberFormat)
    
    # Ülke başına toplam/ortalama formülleri
    formulaRow = len(countryStats) + 2
    countrySheet.write(formulaRow, 0, 'Total/Average', boldFormat)
    countrySheet.write_formula(formulaRow, 1, f'=AVERAGE(B2:B{formulaRow-1})', currencyFormat)
    countrySheet.write_formula(formulaRow, 2, f'=SUM(C2:C{formulaRow-1})', currencyFormat)
    countrySheet.write_formula(formulaRow, 3, f'=AVERAGE(D2:D{formulaRow-1})', numberFormat)
    countrySheet.write_formula(formulaRow, 4, f'=SUM(E2:E{formulaRow-1})', numberFormat)
    
    # Sütun genişliklerini ayarla
    countrySheet.set_column('A:A', 20)
    countrySheet.set_column('B:E', 22)
    
    # 7. Sektör ve Saldırı Tipi Çapraz Tablosu
    crossSheet = workbook.add_worksheet('Industry-Attack Cross')
    
    # Çapraz tablo oluştur
    crossTab = pd.crosstab(df['Target Industry Standardized'], df['Attack Type'])
    
    # Sütun başlıklarını yaz
    crossSheet.write_row('A1', ['Industry'] + list(crossTab.columns), headerFormat)
    
    # Tabloyu doldur
    for i, (idx, row) in enumerate(crossTab.iterrows()):
        crossSheet.write(i+1, 0, idx)
        for j, val in enumerate(row):
            crossSheet.write(i+1, j+1, val, numberFormat)
    
    # Sütun toplamları için formül
    rowCount = len(crossTab) + 1
    colCount = len(crossTab.columns) + 1
    
    crossSheet.write(rowCount, 0, 'Total', boldFormat)
    for j in range(1, colCount):
        colLetter = chr(65 + j)  # A, B, C...
        crossSheet.write_formula(rowCount, j, f'=SUM({colLetter}2:{colLetter}{rowCount})', numberFormat)
    
    # Satır toplamları için formül
    crossSheet.write(0, colCount, 'Total', headerFormat)
    for i in range(1, rowCount+1):
        crossSheet.write_formula(i, colCount, f'=SUM(B{i+1}:{chr(65+colCount-1)}{i+1})', numberFormat)
    
    # Sütun genişliklerini ayarla
    crossSheet.set_column('A:A', 25)
    crossSheet.set_column(1, colCount, 15)
    
    # 8. Öğrenci Bilgileri Sayfası (Yeni eklendi)
    studentSheet = workbook.add_worksheet('Student Info')
    
    studentSheet.merge_range('A1:E1', 'CYBERSECURITY BREACH ANALYSIS', headerFormat)
    studentSheet.merge_range('A2:E2', 'Detailed Excel Report', headerFormat)
    
    studentSheet.write('A4', 'Student ID:', boldFormat)
    studentSheet.write('B4', '190444041')
    
    studentSheet.write('A5', 'Student Name:', boldFormat)
    studentSheet.write('B5', 'Murat KUZUCU')
    
    studentSheet.write('A6', 'Course:', boldFormat)
    studentSheet.write('B6', 'CENG 418')
    
    studentSheet.write('A7', 'Date:', boldFormat)
    studentSheet.write('B7', pd.Timestamp.now().strftime('%Y-%m-%d'))
    
    studentSheet.set_column('A:A', 15)
    studentSheet.set_column('B:B', 25)
    
    # Excel dosyasını kaydet
    writer.close()
    
    print(f"Analysis report created: {outputPath}")
    
    # Script dosyasını trash-bin'e taşı
    scriptPath = os.path.realpath(__file__)
    trashBin = os.path.join(os.getcwd(), 'trash-bin')
    
    try:
        if not os.path.exists(trashBin):
            os.makedirs(trashBin)
            
        import shutil
        fileName = os.path.basename(scriptPath)
        targetPath = os.path.join(trashBin, fileName)
        
        # Önceki script dosyalarını da taşı
        for prevScriptName in ['create_excel_report.py', 'create_excel_report_v2.py']:
            prevScriptPath = os.path.join(os.getcwd(), prevScriptName)
            if os.path.exists(prevScriptPath):
                shutil.copy2(prevScriptPath, os.path.join(trashBin, prevScriptName))
                os.remove(prevScriptPath)
        
        print(f"Previous script files moved to trash-bin")
    except Exception as e:
        print(f"Note: Could not move scripts to trash-bin: {e}")

if __name__ == "__main__":
    create_analysis_report()
