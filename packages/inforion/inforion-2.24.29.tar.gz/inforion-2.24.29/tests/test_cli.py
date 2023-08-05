import os
import uuid

import pytest
from click.testing import CliRunner
from inforion.__main__ import create
from inforion.__main__ import datalake_get
from inforion.__main__ import datalake_list
from inforion.__main__ import delete
from inforion.__main__ import upload

__credentials_file = "credentials/credentials.ionapi"
__data_file = "data/sample.csv"
__schema_file = "data/catalog_schema.json"
__properties_file = "data/catalog_properties.json"


def test_catalog_create():
    runner = CliRunner()
    result = runner.invoke(
        create,
        args="--ionfile {} --name CSVSchema2 --schema_type DSV --schema {} "
        "--properties {}".format(__credentials_file, __schema_file, __properties_file),
    )
    assert not result.exception
    assert "Data catalog schema CSVSchema2 was created." in result.output


@pytest.mark.skip()
def test_catalog_delete():
    schema_name = str(uuid.uuid1())
    runner = CliRunner()
    result = runner.invoke(
        create,
        args="--ionfile credentials/credentials.ionapi --name {} "
        "--schema_type DSV --schema data/catalog_schema.json --properties "
        "data/catalog_properties.json".format(schema_name),
    )
    assert not result.exception
    assert "Data catalog schema {} was created.".format(schema_name) in result.output

    runner2 = CliRunner()
    result2 = runner2.invoke(delete, args="--name {}".format(schema_name))
    assert not result2.exception
    assert "Data catalog schema {} was deleted.".format(schema_name) in result2.output


def test_datalake_upload():
    runner = CliRunner()
    result = runner.invoke(
        upload,
        args="--ionfile {} --schema CSVSchema2 --logical_id lid://infor.ims.mongooseims "
        "--file {}".format(__credentials_file, __data_file),
    )
    assert not result.exception
    assert "Document uploaded successfully." in result.output


def test_datalake_list():
    runner = CliRunner()
    result = runner.invoke(
        datalake_list,
        args="--ionfile {} --list_filter \"dl_document_name eq 'CSVSchema2'\"".format(
            __credentials_file
        ),
    )
    assert not result.exception
    assert "numFound" in result.output


def test_datalake_get():
    runner = CliRunner()
    result = runner.invoke(
        datalake_get,
        args="--ionfile {} -id 1-7e476691-b17c-3e8d-8f0c-ea13222f56ef".format(
            __credentials_file
        ),
    )
    assert not result.exception
    assert "ID,FIRST_NAME,LAST_NAME,COUNTRY" in result.output
