# Import the code to be tested
import os
import unittest

import inforion.helper.api_fields_helper as aph
import inforion.helper.sqllite as sql
from inforion.excelexport import *


class TestAPIFieldDB(unittest.TestCase):
    def test_fields_db_exists(self):
        assert os.path.isfile(aph.database) is True

    def test_fields_table_exists(self):
        conn = sql.create_connection(aph.database)
        assert sql.check_if_table_exists(conn, aph.table_name) is True

    def test_api_fields_exists(self):
        fields = aph.get_fields_list_from_db("CRS610MI")
        assert len(fields) > 0

    def test_get_numeric_fields_list(self):
        fields = aph.get_numeric_fields_list_from_db("CRS610MI")

        all_fields = aph.get_fields_list_from_db("CRS610MI")
        all_fields_filtered = list(filter(lambda x: x[4] == "number", all_fields))

        all_fields_filtered_name = [field[2] for field in all_fields_filtered]

        diff = list(set(fields) - set(all_fields_filtered_name))

        assert len(diff) == 0


if __name__ == "__main__":
    unittest.main()
