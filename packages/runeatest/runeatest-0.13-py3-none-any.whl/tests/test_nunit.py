import pytest
import json
from runeatest import nunit
from runeatest import pyspark
from runeatest import utils


def test_get_nunit_header(mocker):
    x = '{"notebook_path":"/Users/lorem.ipsum@fake.io/runeatest"}'
    context = json.loads(x)
    t = ("2020-9-13", "13:20:16")
    mocker.patch("runeatest.pyspark.getcontext", return_value=context)
    mocker.patch("runeatest.utils.get_date_and_time", return_value=t)
    print(context["notebook_path"])
    expected = '<test-results name="/Users/lorem.ipsum@fake.io/runeatest" total="##total##" date="2020-9-13" time="13:20:16">\n<environment nunit-version="2.6.0.12035" clr-version="2.0.50727.4963" os-version="Microsoft Windows NT 6.1.7600.0" platform="Win32NT" cwd="C:\\Program Files\\NUnit 2.6\\bin\\" machine-name="dummymachine" user="dummyuser" user-domain="dummy"/>\n<culture-info current-culture="en-US" current-uiculture="en-US"/>'
    actual = nunit.get_nunit_header()
    assert expected == actual


def test_get_nunit_footer():
    expected = "</results>\n</test-suite>\n</test-results>"
    actual = nunit.get_nunit_footer()
    assert expected == actual
