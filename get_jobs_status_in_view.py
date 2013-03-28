# -*- coding: utf-8 -*-

from optparse import OptionParser
from xml.etree import ElementTree
from xml.dom.minidom import parseString
from datetime import datetime
import urllib2
import re


def main():
    """
    Jenkins API
    api/xml?depth=2&tree=name,url,jobs[name,healthReport[description],lastBuild[number,result,building,url]]
    """

    # Added parser
    parser = OptionParser()
    parser.add_option('-d', '--debug',
                      action='store_true', dest='enable_debug',
                      default=False,
                      help='Display debug info. Default=False')
    parser.add_option('-s', '--https',
                      action='store_true', dest='enable_https',
                      default=False,
                      help='Enable https. Default=False')
    parser.add_option('-a', '--address',
                      action='store', type='string', dest='address',
                      default='localhost',
                      help='The Jenkins host address. Default=localhost')
    parser.add_option('-p', '--port',
                      action='store', type='int', dest='port',
                      default='8080',
                      help='The Jenkins host port. Default=8080')
    parser.add_option('-v', '--view',
                      action='store', type='string', dest='view',
                      default='All',
                      help='The View\'s name in Jenkins. Default=All')
    parser.add_option('-o', '--ouput-html',
                      action='store', type='string', dest='output',
                      help='The html output file.')
    (options, args) = parser.parse_args()

    print options
    #if len(args) <= 0:
    #    parser.print_help()
    #    parser.error('need more then one options.')
    
    # Setup Jenkins Server's URL
    protocol = 'http'
    if options.enable_https:
        protocol = 'https'

    url = '%s://%s:%s/view/%s/api/xml?depth=2&tree=name,url,jobs[name,lastBuild[description,number,url,result,building],healthReport[description]]' % (protocol, options.address, str(options.port), options.view)
    if options.enable_debug:
        print 'Enable https:', options.enable_https
        print 'Host: %s:%s' % (options.address, str(options.port))
        print 'View:', options.view
        print url
        print

    # enable HTML output
    enable_html = False
    if options.output is not None:
        enable_html = True

    # Retrieve info from Jenkins Server
    response = urllib2.urlopen(url)
    test_input = response.read()
    if options.enable_debug:
        print test_input
        print

    # Parse the output of API
    root = ElementTree.fromstring(test_input)

    # print list view name
    root_name = root.find('name').text
    print 'VIEW_NAME="%s"' % root_name
    now = datetime.now()
    print 'DATE="%s"' % now.strftime('%a, %d %b %Y %I:%M:%S')
    if enable_html:
        output_root_node = ElementTree.Element('div', attrib={'id': root_name})
        output_div_node = ElementTree.SubElement(output_root_node, 'div', attrib={'style': 'font-size: 150%; font-weight: bold'})
        output_div_node.text = root_name
        output_div_node = ElementTree.SubElement(output_root_node, 'div')
        output_div_node.text = "Date: " + now.strftime('%a, %d %b %Y %I:%M:%S')
        output_br_node = ElementTree.SubElement(output_root_node, 'br')

    # find all jobs
    idx_job = 0
    jobs = root.findall('job')
    for job in jobs:
        print ""
        # print job name
        job_name_node = job.find('name')
        if job_name_node is not None:
            job_name = job_name_node.text
            print 'VIEW_%s_JOB_NAME="%s"' % (idx_job, job_name)
            if enable_html:
                output_table_node = ElementTree.SubElement(output_root_node, 'table', attrib={'id': job_name, 'class': 'job_table'})
                output_th_node = ElementTree.SubElement(output_table_node, 'th', attrib={'class': 'job_name', 'colspan': '2', 'style': 'float: right; font-weight: bold'})
                output_th_node.text = job_name
        
        # get last build's info
        last_build = job.find('lastBuild')
        
        # get last build description
        last_build_desc_node = last_build.find('description')
        if last_build_desc_node is not None:
            last_build_desc = last_build_desc_node.text
            print 'VIEW_%s_LAST_BUILD_DESC="%s"' % (str(idx_job), last_build_desc)
            if enable_html:
                output_tr_node = ElementTree.SubElement(output_table_node, 'tr')
                output_td_node = ElementTree.SubElement(output_tr_node, 'td')
                output_td_node.text = "Build Description"
                output_td_node = ElementTree.SubElement(output_tr_node, 'td', attrib={'class': 'build_description'})
                output_td_node.text = last_build_desc

        # get last build number
        last_build_number_node = last_build.find('number')
        if last_build_number_node is not None:
            last_build_number = last_build_number_node.text
            print 'VIEW_%s_LAST_BUILD_NUMBER="%s"' % (str(idx_job), last_build_number)
            if enable_html:
                output_tr_node = ElementTree.SubElement(output_table_node, 'tr')
                output_td_node = ElementTree.SubElement(output_tr_node, 'td')
                output_td_node.text = "Build Number"
                output_td_node = ElementTree.SubElement(output_tr_node, 'td', attrib={'class': 'build_number'})
                output_td_node.text = last_build_number

        # get last build url
        last_build_url_node = last_build.find('url')
        if last_build_url_node is not None:
            last_build_url = last_build_url_node.text
            print 'VIEW_%s_LAST_BUILD_URL="%s"' % (str(idx_job), last_build_url)
            if enable_html:
                output_tr_node = ElementTree.SubElement(output_table_node, 'tr')
                output_td_node = ElementTree.SubElement(output_tr_node, 'td')
                output_td_node.text = "Build URL"
                output_td_node = ElementTree.SubElement(output_tr_node, 'td', attrib={'class': 'build_url'})
                output_td_node.text = last_build_url

        # get last build result
        last_build_result_node = last_build.find('result')
        if last_build_result_node is not None:
            last_build_result = last_build_result_node.text
            print 'VIEW_%s_LAST_BUILD_RESULT="%s"' % (str(idx_job), last_build_result)
            if enable_html:
                output_tr_node = ElementTree.SubElement(output_table_node, 'tr')
                output_td_node = ElementTree.SubElement(output_tr_node, 'td')
                output_td_node.text = "Build Result"
                output_td_node = ElementTree.SubElement(output_tr_node, 'td', attrib={'class': 'build_result'})
                output_td_node.text = last_build_result

        # get last building
        last_build_building_node = last_build.find('building')
        if last_build_building_node is not None:
            last_build_building = last_build_building_node.text
            print 'VIEW_%s_LAST_BUILD_BUILDING="%s"' % (str(idx_job), last_build_building)
            if enable_html:
                output_tr_node = ElementTree.SubElement(output_table_node, 'tr')
                output_td_node = ElementTree.SubElement(output_tr_node, 'td')
                output_td_node.text = "Building"
                output_td_node = ElementTree.SubElement(output_tr_node, 'td', attrib={'class': 'build_building'})
                output_td_node.text = last_build_building

        # get health reports
        idx_health_report = 0
        if enable_html:
            output_tr_node = ElementTree.SubElement(output_table_node, 'tr')
            output_td_node = ElementTree.SubElement(output_tr_node, 'td', attrib={'colspan': '2', 'class': 'build_health'})
            output_ul_node = ElementTree.SubElement(output_td_node, 'ul')
        for health_report in job.findall('healthReport'):
            health_report_desc_node = health_report.find('description')
            if health_report_desc_node is not None:
                health_report_desc = health_report_desc_node.text
                print 'VIEW_%s_HEALTH_REPORT_%s="%s"' % (str(idx_job), str(idx_health_report), health_report_desc)
                if enable_html:
                    output_li_node = ElementTree.SubElement(output_ul_node, 'li')
                    output_li_node.text = health_report_desc
            idx_health_report = idx_health_report + 1

        output_br_node = ElementTree.SubElement(output_root_node, 'br')
        idx_job = idx_job + 1

    if enable_html:
        f = open(options.output, 'w')
        xml = ElementTree.tostring(output_root_node)
        xml_dom = parseString(xml)
        f.write(xml_dom.toprettyxml())
        f.close()

if __name__ == '__main__':
    main()
