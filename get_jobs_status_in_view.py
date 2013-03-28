# -*- coding: utf-8 -*-

test_input="""
<listView>
<job>
<name>test_master</name>
<healthReport><description>Test Result: 0 test failing out of a total of 201 test.</description></healthReport>
<healthReport><description>Build stability: No recent builds failed.</description></healthReport>
<lastBuild>
<number>3928</number>
<result>SUCCESS</result>
<url>http://example.example/job/test_master/3928/</url>
</lastBuild>
</job>
<job>
<name>junit-runtime-suite</name>
<healthReport><description>Build stability: All recent builds failed.</description></healthReport>
<lastBuild>
<number>15184</number>
<result>FAILURE</result>
<url>http://example.example/job/junit-runtime-suite/15184/</url>
</lastBuild>
</job>
<job>
<name>test-artifact-manager</name>
<healthReport><description>Build stability: All recent builds failed.</description></healthReport>
<healthReport><description>Test Result: 1 test failing out of a total of 1 test.</description></healthReport>
<lastBuild>
<number>1353</number>
<result>SUCCESS</result>
<url>http://example.example/job/test-artifact-manager/1353/</url>
</lastBuild>
</job>
<name>Test Projects</name>
<url>http://example.example/view/Test%20Projects/</url></listView>
"""

import xml.etree.ElementTree as ET
import urllib2


"""
Jenkins API
api/xml?depth=2&tree=name,url,jobs[name,healthReport[description],lastBuild[number,result,url]]
"""

root = ET.fromstring(test_input)

# print list view name
root_name = root.find('name').text
print "VIEW_NAME=%s" % root_name

# find all jobs
idx_job = 0
jobs = root.findall('job')
for job in jobs:
    print ""
    # print job name
    job_name = job.find('name').text
    print "%s_JOB_NAME=%s" % (idx_job, job_name)
    # get last build's info
    last_build = job.find('lastBuild')
    last_build_result = last_build.find('result').text
    last_build_number = last_build.find('number').text
    last_build_url = last_build.find('url').text
    print '%s_LAST_BUILD_RESULT=%s' % (str(idx_job), last_build_result)
    print '%s_LAST_BUILD_NUMBER=%s' % (str(idx_job), last_build_number)
    print '%s_LAST_BUILD_URL=%s' % (str(idx_job), last_build_url)
    # get health reports
    idx_health_report = 0
    for health_report in job.findall('healthReport'):
        health_report_desc = health_report.find('description').text
        print '%s_HEALTH_REPORT_%s=%s' % (str(idx_job), str(idx_health_report), health_report_desc)
        idx_health_report = idx_health_report + 1
    idx_job = idx_job + 1
