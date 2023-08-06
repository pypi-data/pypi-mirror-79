from runeatest import pyspark
from runeatest import utils


def get_nunit_header():
    context = pyspark.get_context()
    now = utils.get_date_and_time()
    print(now)
    now_date = now[0]
    now_time = now[1]
    nunit_header = '<test-results name="##name##" total="##total##" date="##getdate##" time="##gettime##">\n<environment nunit-version="2.6.0.12035" clr-version="2.0.50727.4963" os-version="Microsoft Windows NT 6.1.7600.0" platform="Win32NT" cwd="C:\\Program Files\\NUnit 2.6\\bin\\" machine-name="dummymachine" user="dummyuser" user-domain="dummy"/>\n<culture-info current-culture="en-US" current-uiculture="en-US"/>'
    nunit_header = (
        nunit_header.replace("##name##", context["extraContext"]["notebook_path"])
        .replace("##getdate##", now_date)
        .replace("##gettime##", now_time)
    )
    return nunit_header


def get_nunit_footer():
    nunit_footer = "</results>\n</test-suite>\n</test-results>"
    return nunit_footer


def convert_to_nunit_results_format(testresults):
    h = get_nunit_header()
    f = get_nunit_footer()
    return h + f
