import openpyxl

myfile = "clients.xlsx"
absolute_path = os.path.abspath(file.path)
workbook = openpyxl.load_workbook(absolute_path)
sheet = workbook.active
valeurs = list(sheet.values)
