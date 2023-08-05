# Import the code to be tested
import os
import unittest

import inforion.helper.api_fields_helper as aph
from inforion.excelexport import *


class TestStringMethods(unittest.TestCase):

    valid_outputfilename = "TestMapping.xlsx"
    invalid_outputfilename = "/User/mmm/Test.xlsx"
    valid_program = "CRS610MI"

    api_endpoints_valid = [
        "CMBR02MI",
        "OIS005MI",
        "OIS320MI",
        "PPS001MI",
        "MWS410MI",
        "MOS450MI",
        "ENS100MI",
        "MMS240MI",
        "MHS200MI",
    ]
    api_endpoints_invalid = ["CMBR02CC"]

    def test_param1_missing(self):
        assert "Error: Program name is missing" in generate_api_template_file(
            None, self.valid_outputfilename
        )

    def test_param2_missing(self):
        assert "Error: Output filename is missing" in generate_api_template_file(
            self.valid_program, None
        )

    def test_template_file_exists(self):
        assert checkIfTemplateFileExists() is True

    def test_can_create_new_template_file(self):
        res = copyTemplateFile(self.valid_outputfilename)
        assert res is not None

    def test_generate_mapping_file(self):
        res = generate_api_template_file(self.valid_program, self.valid_outputfilename)
        assert res is True

    def setUp(self):
        print("Setup")

    def tearDown(self):
        try:
            os.remove(self.valid_outputfilename)
        except:
            print(self.valid_outputfilename, " doesn't exists")

    def test_validate_generated_file(self):
        generate_api_template_file(self.valid_program, self.valid_outputfilename)
        fields_list = aph.get_fields_list_from_db(self.valid_program)

        xfile = openpyxl.load_workbook(self.valid_outputfilename)

        # sheet = xfile.get_sheet_by_name('Mapping Template')
        sheet = xfile["Mapping Template"]

        isSame = True
        current_row = 11
        added_fields = []
        for field in fields_list:
            # Serial Number

            if(field[2].upper() in  added_fields):
                continue

            len  = sheet["V" + str(current_row)].value
            if len is None:
                len = ''

            isSame = isSame and sheet["A" + str(current_row)].value == current_row - 10
            isSame = isSame and sheet["B" + str(current_row)].value == field[0]

            isSame = isSame and sheet["P" + str(current_row)].value == field[2]
            isSame = isSame and sheet["Q" + str(current_row)].value == field[0]
            isSame = isSame and sheet["R" + str(current_row)].value == field[1]
            isSame = isSame and sheet["S" + str(current_row)].value == getTypeCode(field[4])
            isSame = isSame and len == field[6]
            isSame = isSame and sheet["W" + str(current_row)].value == (1 if field[5] else 0)
            isSame = isSame and sheet["X" + str(current_row)].value == field[3]
           
            if not isSame:
                break

            added_fields.append(field[2].upper())
            current_row = current_row + 1

        assert isSame is True


if __name__ == "__main__":
    unittest.main()
