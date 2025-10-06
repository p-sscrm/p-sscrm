# json2ce.py - quick script to generate Excel spreadsheet for P-SSCRM score data entry
# This probably should take arguments, e.g. the json file, an optional practice or task name, a directory in which to store the results

import json

import openpyxl
from openpyxl import load_workbook
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill, Color
from openpyxl.formatting.rule import ColorScaleRule, CellIsRule
from openpyxl.chart import (
    RadarChart,
    Reference,
)

data_dir = "/Users/pjmorris/github/p-sscrm-core/model"
output_file = "psscrm_ce.xlsx"

dv_indexes = ["A","B","C","D","E"]
dv_choices = ["No","Emerging","Progress Being Made","Almost There","Funded"]
dv_scores = [0,.25,.5,.75,1.0]

borderStyle = Border(left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin'))

practiceFont = Font(name='Arial',size=16,bold=False,color=Color(rgb='FFFFFF'))
practiceFill = PatternFill(patternType='solid',fgColor='ed7d31')

radarPractices = []
radarData = {}
radarRows = []

def makeFont(family,size,color,bold=False,italic=False):
    return Font(family,size,color,bold,italic)

def setCellFont(c,f):
    c.font = f

def makeFill(fillColor):
    return PatternFill(start_color=fillColor, end_color=fillColor, fill_type='solid')

def make_group(ws,g,row):
    # Complementary colors chosen from colorabout.com
    #groupColors = {"GOVERNANCE": "12485B", "PRODUCT": "33125B", "ENVIRONMENT": "5B122C", "DEPLOYMENT": "125B16"}
    #groupColors = {"GOVERNANCE": "0075CF", "PRODUCT": "8300CF", "ENVIRONMENT": "C8CF00", "DEPLOYMENT": "00CF30"}
    #groupColors = {"GOVERNANCE": "3700FF", "PRODUCT": "2FFF00", "ENVIRONMENT": "FF9D00", "DEPLOYMENT": "FF0093"}
    #groupColors = {"GOVERNANCE": "1F3D5C", "PRODUCT": "4A1F5C", "ENVIRONMENT": "5C1F25", "DEPLOYMENT": "1F5C31"}
    groupColors = {"GOVERNANCE": "4F62C8", "PRODUCT": "C86B4F", "ENVIRONMENT": "94C84F", "DEPLOYMENT": "4FC89C"}
    ws['A' + str(row)] = g['name']
    groupColor = "F0F0F0"
    if g['name'].upper() in groupColors:
        groupColor = groupColors[g['name'].upper()]
    groupFill = makeFill(groupColor)
    ws['A' + str(row)].font = Font(name='Arial',size=22,bold=True,color=Color(rgb='FFFFFF'))
    ws['A' + str(row)].fill = groupFill
    for col in ['B','C','D','E']:
        ws[col + str(row)].font = practiceFont
        ws[col + str(row)].fill = groupFill
    ws.column_dimensions['B'].width = 60
    return row + 1, groupFill

def make_practice(ws,p,groupFill,row):
    practiceName = p['id'] + " " + p['name']
    ws['B' + str(row)] = practiceName
    radarPractices.append(practiceName)
    radarRows.append(row)
    colIdx =  ord('E') - ord('A') + 1
    if practiceName not in radarData:
        radarData[practiceName] = Reference(ws,min_col=colIdx,min_row=row,max_col=colIdx,max_row=row)
    for col in ['A','B','C','D','E']:
        ws[col + str(row)].font = practiceFont
        ws[col + str(row)].fill = groupFill
        ws[col + str(row)].border = borderStyle
    ws['E' + str(row)] = "Summed Task Scores"
    ##border
    #cellRange = '{}{}:{}{}'.format(cell,startRow,"C",row)
    #for r in tab[cellRange]:
    #    for c in r:
    #        c.border = borderStyle
    return row + 1

def make_task(ws,t,row,dv):
    #breakpoint()
    # TOD: Dig t['questions'] out and add to task's cell
    questions = ""
    for q in t['questions']:
        questions += "\n" + str(q['text'])
    ws['B' + str(row)] = t['id'] + " "  + t['name'] + questions
    ws['B' + str(row)].alignment = Alignment(wrapText=True)
    dv.add(ws['C' + str(row)])
    ws['D' + str(row)] = "Score"
    #ws['D' + str(row)].value = '=IFERROR(INDEX(INDIRECT(' + 'C' + str(row) + '), MATCH('+ 'D' + str(row) + ', INDEX(INDIRECT(' + 'C' + str(row) + '), 0, 1), 0), 2), 0)'
    #ws['D' + str(row)].value = '==MATCH(C{},lookups!$A$1:$A$5)'.format(row)
    ws['D'+str(row)].value = '=IFERROR(VLOOKUP(C{},lookups!$A$1:$B$5,2,FALSE),0)'.format(row)

    return row + 1

# addRow(ws,row,'A',"Company Id:",font=None,fill=None)
def addRow(tab,row,cell,text,font=None,fill=None):
    tab[cell+str(row)] = text
    if fill != None:
        tab.fill = fill
    pass

def instructions(tab,cell,row):
    addRow(tab,row,cell,"Using a completed P-SSCRM questionnaire, or your own estimates,")
    row += 1
    addRow(tab,row,cell,"select the best answer from the dropdown in the answer column")
    row += 1  
    return row

def indicativeData(tab,cell,row):
    indicativeFont = makeFont('Arial',14,color=Color(rgb='FFFFFF'))
    startRow = row
    addRow(tab,row,cell,"Company Id:",indicativeFont)
    row += 1
    addRow(tab,row,cell,"Assessment Date:",indicativeFont)
    row += 1  
    addRow(tab,row,cell,"Team/Application:",indicativeFont)
    row += 1  
    addRow(tab,row,cell,"Assessor(s):",indicativeFont)
    row += 1  
    addRow(tab,row,cell,"Contributor(s):",indicativeFont)
    row += 1  
    addRow(tab,row,cell,"",indicativeFont)
    row += 1  
    # border
    #setBorder()
    cellRange = '{}{}:{}{}'.format(cell,startRow,"C",row)
    for r in tab[cellRange]:
        for c in r:
            c.border = borderStyle
    return row

# radarChart(ws,labels,data,"Spider Template","G5")
def radarChart(ws,labels,data,title,location):
    chart = RadarChart()
    #chart.type = "filled"
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(labels)
    chart.style = 26
    chart.title = title
    chart.y_axis.delete = True
    #ws.add_chart(chart, location)

def makeRadarTab(wb,ws,name,cols):
    tab = wb.create_sheet()
    tab.title = name
    for i in range(0,len(cols)):
        tab["A" + str(i+1)] = ws["B"+str(cols[i])].value
        tab["B" + str(i+1)] = ws["E"+str(cols[i])].value
    tab["A1"] = "Practice"
    tab["B1"] = "Score"

    labels = Reference(tab, min_col=1, min_row=2, max_row=i)
    data = Reference(tab, min_col=2, min_row=2, max_row=i)
    return tab, labels, data

def main():
    jfilename = "data/p-sscrm-2_0.json"
    template_wb ="data/ce_template.xlsx"
    ofilename = "psscrm_ce.xlsx"
    wb = load_workbook(template_wb)
    j = json.load(open(jfilename))

    #wb = openpyxl.Workbook()
    ws = wb.active

    #lookups = wb.create_sheet()
    #lookups.title = "lookups"
    #for i in range(0,5):
    #    lookups["A" + str(i+1)] = dv_choices[i]
    #    lookups["B" + str(i+1)] = dv_scores[i]

    dropdown = DataValidation(type="list", formula1=f'"{",".join(dv_choices)}"', showDropDown=False, allow_blank=True) 
    ws.add_data_validation(dropdown)
    ws.title = "DataEntry"
    row = 1
    row += instructions(ws,"B",row)
    row += indicativeData(ws,"A",row)

    addRow(ws,row,"C","Answer")
    addRow(ws,row,"D","Score")
    row += 1

    ws.column_dimensions['A'].width = 25
    ws.column_dimensions['B'].width = 90
    ws.column_dimensions['C'].width = 20
    ws.column_dimensions['D'].width = 10
    ws.column_dimensions['E'].width = 10 


    for g in j['groups']:
        row, groupFill = make_group(ws,g,row)
        for p in g['practices']:
            row = make_practice(ws,p,groupFill,row)
            practice_row = row - 1
            for t in p['tasks']:
                print("Task: ", t['name'],t['id'])
                row = make_task(ws,t,row,dropdown)
            ws['E'+str(practice_row)].value = '=AVERAGE({}!{}:{})'.format("DataEntry",practice_row+1,row-1)   

    #ntab,nlabels,ndata = makeRadarTab(wb,ws,"psscrm",radarRows)
    #radarChart(ntab,nlabels,ndata,"Spider Template","G5")
    wb.save("artifacts/" + ofilename)

if __name__ == '__main__':
    main()      
