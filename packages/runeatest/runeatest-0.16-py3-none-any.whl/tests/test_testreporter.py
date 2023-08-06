import pytest


def test_add_test_case():
    from runeatest import testreporter

    actual = []
    actual.append(testreporter.addtestcase("test name", True))
    actual.append(testreporter.addtestcase("test name 2", True))
    expected = "[{'test': 'test name', 'issuccess': 'True', 'result': 'success'}, {'test': 'test name 2', 'issuccess': 'True', 'result': 'success'}]"
    expected == actual
