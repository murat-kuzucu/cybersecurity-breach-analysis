import pandas as pd
import numpy as np
from pathlib import Path
import os
from scipy import stats

def create_enhanced_analysis():
    # camelCase değişken adları kullanımına dikkat edelim
    dataPath = Path('data/RAW-cybersecurity_breach_data.csv')
    outputPath = 'data/enhanced_analysis_report.xlsx'
    
    # Veri setini yükle
    df = pd.read_csv(dataPath)
    print(f"Loaded data with {len(df)} records from {dataPath}")
    
    # Excel dosyasını oluştur
    writer = pd.ExcelWriter(outputPath, engine='xlsxwriter')
    workbook = writer.book
    
    # Formatları tanımla
    headerFormat = workbook.add_format({
        'bold': True, 'font_color': 'white', 'bg_color': '#2F75B5',
        'align': 'center', 'valign': 'vcenter', 'border': 1
    })
    
    numberFormat = workbook.add_format({
        'num_format': '#,##0.00',
        'align': 'center'
    })
    
    currencyFormat = workbook.add_format({
        'num_format': '$#,##0.00',
        'align': 'center'
    })
    
    # 1. RAW DATA - Ham veriyi dahil et
    rawDataSheet = workbook.add_worksheet('Raw Data')
    
    # Başlıkları yaz
    for col_idx, col_name in enumerate(df.columns):
        rawDataSheet.write(0, col_idx, col_name, headerFormat)
    
    # Verileri yaz
    for row_idx, row in df.iterrows():
        for col_idx, value in enumerate(row):
            if isinstance(value, (int, float)) and col_idx == df.columns.get_loc('Financial Loss (in Million $)'):
                rawDataSheet.write(row_idx + 1, col_idx, value, currencyFormat)
            elif isinstance(value, (int, float)):
                rawDataSheet.write(row_idx + 1, col_idx, value, numberFormat)
            else:
                rawDataSheet.write(row_idx + 1, col_idx, value)
    
    # Sütun genişliklerini ayarla
    for i, col in enumerate(df.columns):
        rawDataSheet.set_column(i, i, 18)
    
    # 2. SUMMARY STATISTICS - Özet İstatistikler
    statsSheet = workbook.add_worksheet('Summary Statistics')
    
    # Başlıkları yaz
    statsSheet.write(0, 0, "Metric", headerFormat)
    
    numericCols = df.select_dtypes(include=[np.number]).columns.tolist()
    for col_idx, col_name in enumerate(numericCols):
        statsSheet.write(0, col_idx + 1, col_name, headerFormat)
    
    # İstatistikleri hesapla ve yaz
    statMetrics = ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
    numericStats = df[numericCols].describe().T
    
    for row_idx, metric in enumerate(statMetrics):
        statsSheet.write(row_idx + 1, 0, metric)
        for col_idx, col_name in enumerate(numericCols):
            if metric in numericStats.columns:
                value = numericStats.loc[col_name, metric]
                if 'Financial Loss' in col_name:
                    statsSheet.write(row_idx + 1, col_idx + 1, value, currencyFormat)
                else:
                    statsSheet.write(row_idx + 1, col_idx + 1, value, numberFormat)
    
    # Sütun genişliklerini ayarla
    statsSheet.set_column(0, 0, 15)
    statsSheet.set_column(1, len(numericCols), 22)
    
    # 3. DATA TYPES - Veri Tipleri
    dataTypesSheet = workbook.add_worksheet('Data Types')
    
    # Başlıkları yaz
    columnHeaders = ['Column', 'Data Type', 'Non-Null Count', 'Null Count']
    for col_idx, header in enumerate(columnHeaders):
        dataTypesSheet.write(0, col_idx, header, headerFormat)
    
    # Veri tipi bilgilerini yaz
    for row_idx, col_name in enumerate(df.columns):
        dataTypesSheet.write(row_idx + 1, 0, col_name)
        dataTypesSheet.write(row_idx + 1, 1, str(df[col_name].dtype))
        dataTypesSheet.write(row_idx + 1, 2, df[col_name].count(), numberFormat)
        dataTypesSheet.write(row_idx + 1, 3, df[col_name].isna().sum(), numberFormat)
    
    # Sütun genişliklerini ayarla
    dataTypesSheet.set_column(0, 0, 35)
    dataTypesSheet.set_column(1, 3, 15)
    
    # 4. FINANCIAL ANALYSIS - Finansal Analiz
    finSheet = workbook.add_worksheet('Financial Analysis')
    
    # Sektöre göre detaylı finansal istatistikler
    finColumns = ['Industry', 'Mean Loss', 'Median Loss', 'Std Dev', 'Min Loss', 'Max Loss', 'Total Loss', 'Count']
    
    # Başlıkları yaz
    for col_idx, header in enumerate(finColumns):
        finSheet.write(0, col_idx, header, headerFormat)
    
    # Grup istatistiklerini hesapla
    industries = df['Target Industry Standardized'].unique()
    
    for row_idx, industry in enumerate(industries):
        industryData = df[df['Target Industry Standardized'] == industry]['Financial Loss (in Million $)']
        
        finSheet.write(row_idx + 1, 0, industry)
        finSheet.write(row_idx + 1, 1, industryData.mean(), currencyFormat)
        finSheet.write(row_idx + 1, 2, industryData.median(), currencyFormat)
        finSheet.write(row_idx + 1, 3, industryData.std(), currencyFormat)
        finSheet.write(row_idx + 1, 4, industryData.min(), currencyFormat)
        finSheet.write(row_idx + 1, 5, industryData.max(), currencyFormat)
        finSheet.write(row_idx + 1, 6, industryData.sum(), currencyFormat)
        finSheet.write(row_idx + 1, 7, len(industryData), numberFormat)
    
    # Sütun genişliklerini ayarla
    finSheet.set_column(0, 0, 25)
    finSheet.set_column(1, 7, 15)
    
    # 5. ATTACK ANALYSIS - Saldırı Analizi
    attackSheet = workbook.add_worksheet('Attack Analysis')
    
    # Saldırı türüne göre istatistikler
    attackColumns = ['Attack Type', 'Avg Loss', 'Total Loss', 'Avg Resolution Time', 'Count', '% of Total']
    
    # Başlıkları yaz
    for col_idx, header in enumerate(attackColumns):
        attackSheet.write(0, col_idx, header, headerFormat)
    
    # Grup istatistiklerini hesapla
    attackTypes = df['Attack Type'].value_counts().index.tolist()
    totalIncidents = len(df)
    
    for row_idx, attackType in enumerate(attackTypes):
        attackData = df[df['Attack Type'] == attackType]
        
        attackSheet.write(row_idx + 1, 0, attackType)
        attackSheet.write(row_idx + 1, 1, attackData['Financial Loss (in Million $)'].mean(), currencyFormat)
        attackSheet.write(row_idx + 1, 2, attackData['Financial Loss (in Million $)'].sum(), currencyFormat)
        attackSheet.write(row_idx + 1, 3, attackData['Incident Resolution Time (in Hours)'].mean(), numberFormat)
        attackSheet.write(row_idx + 1, 4, len(attackData), numberFormat)
        attackSheet.write(row_idx + 1, 5, len(attackData) / totalIncidents, workbook.add_format({'num_format': '0.00%'}))
    
    # Sütun genişliklerini ayarla
    attackSheet.set_column(0, 0, 25)
    attackSheet.set_column(1, 5, 18)
    
    # 6. VULNERABILITY ANALYSIS - Güvenlik Açığı Analizi
    vulnSheet = workbook.add_worksheet('Vulnerability Analysis')
    
    # Güvenlik açığı türlerine göre istatistikler
    vulnColumns = ['Vulnerability Type', 'Avg Loss', 'Total Loss', 'Avg Resolution Time', 'Count', '% of Total']
    
    # Başlıkları yaz
    for col_idx, header in enumerate(vulnColumns):
        vulnSheet.write(0, col_idx, header, headerFormat)
    
    # Grup istatistiklerini hesapla
    vulnTypes = df['Security Vulnerability Type'].value_counts().index.tolist()
    
    for row_idx, vulnType in enumerate(vulnTypes):
        vulnData = df[df['Security Vulnerability Type'] == vulnType]
        
        vulnSheet.write(row_idx + 1, 0, vulnType)
        vulnSheet.write(row_idx + 1, 1, vulnData['Financial Loss (in Million $)'].mean(), currencyFormat)
        vulnSheet.write(row_idx + 1, 2, vulnData['Financial Loss (in Million $)'].sum(), currencyFormat)
        vulnSheet.write(row_idx + 1, 3, vulnData['Incident Resolution Time (in Hours)'].mean(), numberFormat)
        vulnSheet.write(row_idx + 1, 4, len(vulnData), numberFormat)
        vulnSheet.write(row_idx + 1, 5, len(vulnData) / totalIncidents, workbook.add_format({'num_format': '0.00%'}))
    
    # Sütun genişliklerini ayarla
    vulnSheet.set_column(0, 0, 25)
    vulnSheet.set_column(1, 5, 18)
    
    # 7. DEFENSE MECHANISMS - Savunma Mekanizmaları
    defenseSheet = workbook.add_worksheet('Defense Mechanisms')
    
    # Savunma mekanizmalarına göre istatistikler
    defenseColumns = ['Defense Mechanism', 'Avg Loss', 'Total Loss', 'Avg Resolution Time', 'Count', 'Effectiveness Score']
    
    # Başlıkları yaz
    for col_idx, header in enumerate(defenseColumns):
        defenseSheet.write(0, col_idx, header, headerFormat)
    
    # Grup istatistiklerini hesapla
    defenseMechs = df['Defense Mechanism Used'].value_counts().index.tolist()
    
    # Etkinlik skoru hesaplama - daha düşük çözüm süresi ve daha düşük finansal kayıp = daha yüksek etkinlik
    maxResTime = df['Incident Resolution Time (in Hours)'].max()
    maxLoss = df['Financial Loss (in Million $)'].max()
    
    for row_idx, defenseMech in enumerate(defenseMechs):
        defenseData = df[df['Defense Mechanism Used'] == defenseMech]
        
        avgResTime = defenseData['Incident Resolution Time (in Hours)'].mean()
        avgLoss = defenseData['Financial Loss (in Million $)'].mean()
        
        # Etkinlik skoru (0-100) - Düşük çözüm süresi ve düşük kayıp = yüksek etkinlik
        effectivenessScore = 100 - (((avgResTime / maxResTime) * 0.5 + (avgLoss / maxLoss) * 0.5) * 100)
        
        defenseSheet.write(row_idx + 1, 0, defenseMech)
        defenseSheet.write(row_idx + 1, 1, avgLoss, currencyFormat)
        defenseSheet.write(row_idx + 1, 2, defenseData['Financial Loss (in Million $)'].sum(), currencyFormat)
        defenseSheet.write(row_idx + 1, 3, avgResTime, numberFormat)
        defenseSheet.write(row_idx + 1, 4, len(defenseData), numberFormat)
        defenseSheet.write(row_idx + 1, 5, effectivenessScore, numberFormat)
    
    # Sütun genişliklerini ayarla
    defenseSheet.set_column(0, 0, 25)
    defenseSheet.set_column(1, 5, 18)
    
    # 8. YEARLY TRENDS - Yıllık Trendler
    trendSheet = workbook.add_worksheet('Yearly Trends')
    
    # Yıla göre istatistikler
    trendColumns = ['Year', 'Avg Loss', 'Total Loss', 'Avg Resolution Time', 'Incident Count', 'YoY Growth']
    
    # Başlıkları yaz
    for col_idx, header in enumerate(trendColumns):
        trendSheet.write(0, col_idx, header, headerFormat)
    
    # Yılları sırala
    years = sorted(df['Year'].unique())
    previousYearLoss = None
    
    for row_idx, year in enumerate(years):
        yearData = df[df['Year'] == year]
        totalLoss = yearData['Financial Loss (in Million $)'].sum()
        
        trendSheet.write(row_idx + 1, 0, year, numberFormat)
        trendSheet.write(row_idx + 1, 1, yearData['Financial Loss (in Million $)'].mean(), currencyFormat)
        trendSheet.write(row_idx + 1, 2, totalLoss, currencyFormat)
        trendSheet.write(row_idx + 1, 3, yearData['Incident Resolution Time (in Hours)'].mean(), numberFormat)
        trendSheet.write(row_idx + 1, 4, len(yearData), numberFormat)
        
        # YoY büyüme oranı
        if previousYearLoss is not None and previousYearLoss != 0:
            yoyGrowth = (totalLoss / previousYearLoss) - 1
            trendSheet.write(row_idx + 1, 5, yoyGrowth, workbook.add_format({'num_format': '0.00%'}))
        
        previousYearLoss = totalLoss
    
    # Sütun genişliklerini ayarla
    trendSheet.set_column(0, 0, 10)
    trendSheet.set_column(1, 5, 18)
    
    # 9. STATISTICAL TESTS - İstatistiksel Testler
    statsTestSheet = workbook.add_worksheet('Statistical Tests')
    
    # Başlık
    statsTestSheet.write(0, 0, "Statistical Test Results", headerFormat)
    statsTestSheet.merge_range('A1:D1', "Statistical Test Results", headerFormat)
    
    # 9.1 ANOVA - Sektörlere göre finansal kayıp farklılıklarını test et
    statsTestSheet.write(2, 0, "ANOVA: Target Industry vs Financial Loss", workbook.add_format({'bold': True}))
    statsTestSheet.write_row(3, 0, ["Metric", "Value"], headerFormat)
    
    # ANOVA testini gerçekleştir
    industryGroups = []
    for industry in df['Target Industry Standardized'].unique():
        industryData = df[df['Target Industry Standardized'] == industry]['Financial Loss (in Million $)']
        if len(industryData) > 5:  # Yeterli veri olduğundan emin ol
            industryGroups.append(industryData.values)
    
    if len(industryGroups) >= 2:  # En az iki grup olmalı
        fValue, pValue = stats.f_oneway(*industryGroups)
        
        statsTestSheet.write(4, 0, "F-value")
        statsTestSheet.write(4, 1, fValue, numberFormat)
        
        statsTestSheet.write(5, 0, "p-value")
        statsTestSheet.write(5, 1, pValue, numberFormat)
        
        statsTestSheet.write(6, 0, "Significant at α=0.05")
        statsTestSheet.write(6, 1, "Yes" if pValue < 0.05 else "No")
    
    # 9.2 KORELASYON - Sayısal değişkenler arasındaki korelasyon
    statsTestSheet.write(8, 0, "Correlation Analysis: Numerical Variables", workbook.add_format({'bold': True}))
    
    # Sayısal değişkenleri seç
    numCorrelations = df[['Financial Loss (in Million $)', 'Number of Affected Users', 
                          'Incident Resolution Time (in Hours)']].corr()
    
    # Korelasyon matrisini yaz
    for i, col in enumerate(numCorrelations.columns):
        statsTestSheet.write(9, i+1, col, headerFormat)
        statsTestSheet.write(i+10, 0, col, headerFormat)
    
    for i, row in enumerate(numCorrelations.index):
        for j, col in enumerate(numCorrelations.columns):
            statsTestSheet.write(i+10, j+1, numCorrelations.loc[row, col], 
                                workbook.add_format({'num_format': '0.000'}))
    
    # 9.3 CHI-SQUARE - Kategorik değişkenler arasındaki ilişkiler
    statsTestSheet.write(15, 0, "Chi-Square Tests: Categorical Variables", workbook.add_format({'bold': True}))
    statsTestSheet.write_row(16, 0, ["Variable 1", "Variable 2", "Chi-Square", "p-value", "Significant"], headerFormat)
    
    # Chi-square testlerini gerçekleştir
    catVars = ['Attack Type', 'Target Industry Standardized', 'Attack Source', 'Security Vulnerability Type']
    chiRow = 17
    
    for i, var1 in enumerate(catVars):
        for j, var2 in enumerate(catVars):
            if i < j:  # Her çifti sadece bir kez test et
                # Çapraz tablo oluştur
                crosstab = pd.crosstab(df[var1], df[var2])
                
                # Chi-square testi uygula
                chi2, p, dof, expected = stats.chi2_contingency(crosstab)
                
                statsTestSheet.write(chiRow, 0, var1)
                statsTestSheet.write(chiRow, 1, var2)
                statsTestSheet.write(chiRow, 2, chi2, numberFormat)
                statsTestSheet.write(chiRow, 3, p, numberFormat)
                statsTestSheet.write(chiRow, 4, "Yes" if p < 0.05 else "No")
                
                chiRow += 1
    
    # 10. CROSS TABULATION - Çapraz Tablolar
    crossTabSheet = workbook.add_worksheet('Cross Tabulation')
    
    # Başlık
    crossTabSheet.write(0, 0, "Sector vs Attack Type: Average Financial Loss", headerFormat)
    crossTabSheet.merge_range('A1:D1', "Sector vs Attack Type: Average Financial Loss", headerFormat)
    
    # Çapraz tablo oluştur
    crossTab = pd.crosstab(
        df['Target Industry Standardized'], 
        df['Attack Type'],
        values=df['Financial Loss (in Million $)'],
        aggfunc='mean',
        margins=True,
        margins_name='Total'
    ).fillna(0)
    
    # Sektörleri ve saldırı türlerini al
    sectors = list(crossTab.index[:-1])  # Son satır (Total) hariç
    attackTypes = list(crossTab.columns[:-1])  # Son sütun (Total) hariç
    
    # Saldırı tiplerini yaz (başlıklar)
    for col_idx, attackType in enumerate(attackTypes):
        crossTabSheet.write(2, col_idx + 1, attackType, headerFormat)
    crossTabSheet.write(2, len(attackTypes) + 1, "Total", headerFormat)
    
    # Sektör ve değerleri yaz
    for row_idx, sector in enumerate(sectors):
        crossTabSheet.write(row_idx + 3, 0, sector, headerFormat)
        
        for col_idx, attackType in enumerate(attackTypes):
            crossTabSheet.write(row_idx + 3, col_idx + 1, crossTab.loc[sector, attackType], currencyFormat)
        
        # Sektör toplamı
        crossTabSheet.write(row_idx + 3, len(attackTypes) + 1, crossTab.loc[sector, 'Total'], currencyFormat)
    
    # Toplam satırını yaz
    crossTabSheet.write(len(sectors) + 3, 0, "Total", headerFormat)
    for col_idx, attackType in enumerate(attackTypes):
        crossTabSheet.write(len(sectors) + 3, col_idx + 1, crossTab.loc['Total', attackType], currencyFormat)
    
    # Genel toplam (sağ alt köşe)
    crossTabSheet.write(len(sectors) + 3, len(attackTypes) + 1, crossTab.loc['Total', 'Total'], currencyFormat)
    
    # Sütun genişliklerini ayarla
    crossTabSheet.set_column(0, 0, 25)
    crossTabSheet.set_column(1, len(attackTypes) + 1, 15)
    
    # Excel dosyasını kaydet
    writer.close()
    
    print(f"Enhanced analysis report created: {outputPath}")
    
    # Script dosyasını trash-bin'e taşı
    scriptPath = os.path.realpath(__file__)
    trashBin = os.path.join(os.getcwd(), 'trash-bin')
    
    try:
        if not os.path.exists(trashBin):
            os.makedirs(trashBin)
            
        import shutil
        fileName = os.path.basename(scriptPath)
        targetPath = os.path.join(trashBin, fileName)
        shutil.copy2(scriptPath, targetPath)
        
        # Önceki script dosyalarını da taşı
        for prevScriptName in ['create_basic_analysis.py', 'enhance_analysis_report.py', 'enhance_analysis_report_fixed.py']:
            prevScriptPath = os.path.join(os.getcwd(), prevScriptName)
            if os.path.exists(prevScriptPath):
                shutil.copy2(prevScriptPath, os.path.join(trashBin, prevScriptName))
                try:
                    os.remove(prevScriptPath)
                except:
                    pass
        
        print(f"Script files moved to trash-bin")
    except Exception as e:
        print(f"Note: Could not move script to trash-bin: {e}")

if __name__ == "__main__":
    create_enhanced_analysis()
