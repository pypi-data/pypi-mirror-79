import pytest
from runeatest import nunit
def test_get_nunit_header():
    expected = '<test-results name=\"##notebookPath##\" total=\"##total##\" date=\"##getdate##\" time=\"##gettime##\">\n<environment nunit-version=\"2.6.0.12035\" clr-version=\"2.0.50727.4963\" os-version=\"Microsoft Windows NT 6.1.7600.0\" platform=\"Win32NT\" cwd=\"C:\\Program Files\\NUnit 2.6\\bin\\" machine-name=\"dummymachine\" user=\"dummyuser\" user-domain=\"dummy\"/>\n<culture-info current-culture=\"en-US\" current-uiculture=\"en-US\"/>'
    actual = nunit.get_nunit_header()
    assert expected == actual

def test_get_nunit_footer():
    expected = '</results>\n</test-suite>\n</test-results>'
    actual = nunit.get_nunit_footer()
    assert expected == actual