from odoo import models
import base64 # => Remember at report there was (src) attribute that dynamically make sure the image field data in a (base64) format there. Here it is
import io
# I/O => stands for Input/Output. It refers to the flow of data between two entities: A computer program and an external system or device (e.g., a file, the user, a printer). Or between different parts of a program (e.g., memory and disk).
# When you see I/O in programming, it refers to handling: Data Input- Reading data from a user, a file, or a device. Data Output- Writing data to a file, sending it to a device, or displaying it to the user.


# The below to create a excel report
class PatientCardXlsx(models.AbstractModel):
    # AbstractModel:- Not a Database Table It’s purely for logic, functionality, and structure that can be shared across other models.
    _name = 'report.hospetal.report_patient_card_id_xlsx'
    # _name = 'report.module_name.report_name' (<field name="report_name"> :- at action record)
    _inherit = 'report.report_xlsx.abstract'
    # This is a base abstract model provided by Odoo for generating XLSX reports. It is defined as part of Odoo’s report_xlsx module (or a similar custom module).
    # what is means by (report.report_xlsx.abstract) refer to (/Hospetal/data/My_Doc_lessons) => search by (How To Create Excel Report In Odoo 14) => You will find the explanation in this lesson.

    # def generate_xlsx_report(self, workbook, data, patients):
    """
    workbook: Represents the workbook object, which is the Excel file being created that provided by the xlsxwriter library (used by Odoo for generating Excel files). And It is used to add sheets, write data, and apply styles to the Excel file.
    patients: Represents the records that related to model (from <record id="report_patient_card_xls" model="ir.actions.report"> => <field name="model"> => hospital.patient model) for which the report is being generated. It’s iterable, meaning it contains multiple patient records.
    data:Likely additional data passed to the method, typically used for configuration or context. (probably like vals) but Typically used for passing contextual or configuration data for the report.
    ex: data = {'start_date': '2024-01-01', 'end_date': '2024-01-31'}
        self.generate_xlsx_report(workbook, data, patients)
    """

    # for obj in patients:              # Loops through each obj in the patients collection. Means Each obj is a record of the hospital.patient mode, So This ensures the report can include data for all selected patients.
    #     obj_name = obj.name        # save name of the patient at variable named (report_name)
    #
    #     sheet = workbook.add_worksheet(report_name[:31])          # 1: create xml (workbook) sheet named sheet. and give to report_name (name) maximum 31 characters. means (ahmed sayed sayed ahmed mahmoud) accepted but add space ( ) after mahmoud error
    #
    #     bold = workbook.add_format({'bold': True})                # Creates a format object (bold) with the style bold: True. his is part of the xlsxwriter library, which allows styling cells in Excel files. This format will be applied to cells where you want the text to appear bold.
    #
    #     sheet.write(0, 0, obj.name, bold)                         # (0, 0,): At Sheet Writes data to the first cell (row 0, column 0) of the worksheet. at that cell put report_name (obj.name) and format object bold
    #

    # At the below def I will get more than one patient at same sheet
    def generate_xlsx_report(self, workbook, data, patients):
        sheet_variable = workbook.add_worksheet("patients sheet")
        # create xml (workbook) sheet named patients sheet
        bold = workbook.add_format({'bold': True})
        left_align = workbook.add_format({'align':'left'})
        formar1 = workbook.add_format({'bold':True,'align':'center','bg_color':'yellow'})
        # When I add this format instead of bold the field will takes features of formar1 ('bg_color':'yellow'=> cell colore)
        row = 0
        col = 0
        a = 1

        for obj in patients:
            sheet_variable.merge_range(row, col, row, col + 1, f'Patient number: {a}', formar1)
            # At merge_range add 1st (row and colum) then 2nd (row and colum), And it`s 1st step at (0 row), (a colum) and (0 row), (b colum) put text with format1
            row = row + 1
            # Add row by 1 we go to (1 row) and will return back to (colum a)
            if obj.image:
                production_image = io.BytesIO(base64.b64decode(obj.image))
                # change (obj.image) to bytes by used the functionality of method (BytesIO) that created at model (io)
                sheet_variable.set_column(col, col, 11)  # Set column width
                sheet_variable.set_row(row, 65)  # Set row height
                sheet_variable.insert_image(row,col,'image.png',{'image_data':production_image,'x_scale':0.5,'y_scale':0.5})

            row = row + 1
            sheet_variable.write(row, col, 'Name:', bold)
            # at => sheet_variable => row= 1 and colum= a add => Name
            sheet_variable.write(row, col + 1, obj.name, bold)
            # at => sheet_variable => row= 1 and colum= b add => name of patient
            row = row + 1
            # add +1 to row cuz when select 3 patients from list or add more than one field like age and ref so after finsh 1st field (Name and patient name) go to 2nd row and I do that To prevent writing data at same row (the functionality of xls report if add alot of fields at same place delete field Before the other and keep last field
            sheet_variable.write(row,col,'Age:',bold)
            # row = 2 and col = a CUZ colum Increase by 1 only between brackets out () back to b, Why dont do that at row ? because colum (a) and (b) fixed in all equations BUT I must add 1 to row each time To prevent writing data at same row
            sheet_variable.write(row,col+1,obj.age,left_align)
            # row = 2 and col = b
            row = row + 1
            sheet_variable.write(row,col,'Reference:',bold)
            sheet_variable.write(row,col+1,obj.ref,bold)
            row +=1
            sheet_variable.write(row,col,'Gender:',bold)
            sheet_variable.write(row,col+1,obj.gender)
            # For your kindly information (FYKI) if u need writ data horizontal, Fix row Add one to col
            row +=2
            # To add a gab row between each patient
            a+=1



        sheet_variable.set_column('B:C', 15)
        # increase the colum width to 15




