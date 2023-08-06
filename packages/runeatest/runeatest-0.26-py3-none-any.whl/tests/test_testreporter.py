import pytest


def test_add_all_passed_test_cases():
    from runeatest import testreporter

    actual = []
    actual.append(testreporter.add_testcase("test name", True))
    actual.append(testreporter.add_testcase("test name 2", True))
    expected = "[{'test': 'test name', 'issuccess': 'True', 'result': 'success'}, {'test': 'test name 2', 'issuccess': 'True', 'result': 'success'}]"
    expected == actual


def test_add_passed_test_case():
    from runeatest import testreporter

    actual = []
    actual.append(testreporter.add_testcase("test name", True))
    expected = "[{'test': 'test name', 'issuccess': 'True', 'result': 'success'}]"
    expected == actual


def test_add_failed_test_case():
    from runeatest import testreporter

    actual = []
    actual.append(testreporter.add_testcase("test name", False))
    expected = "[{'test': 'test name', 'issuccess': 'False', 'result': 'failure'}]"
    expected == actual


def test_add_all_failed_test_cases():
    from runeatest import testreporter

    actual = []
    actual.append(testreporter.add_testcase("test name", True))
    actual.append(testreporter.add_testcase("test name 2", True))
    expected = "[{'test': 'test name', 'issuccess': 'False', 'result': 'failure'}, {'test': 'test name 2', 'issuccess': 'False', 'result': 'failure'}]"
    expected == actual


def test_add_one_passed_one_failed_test_cases():
    from runeatest import testreporter

    actual = []
    actual.append(testreporter.add_testcase("test name", True))
    actual.append(testreporter.add_testcase("test name 2", False))
    expected = "[{'test': 'test name', 'issuccess': 'True', 'result': 'success'}, {'test': 'test name 2', 'issuccess': 'False', 'result': 'failure'}]"
    expected == actual
