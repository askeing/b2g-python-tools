import os
import optparse
import hashlib
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

'''
Author: Askeing (askeing@gmail.com)

ref: https://github.com/mozilla-b2g/b2g-manifest
'''


def main():
    parser = optparse.OptionParser(description='Retrieve gaia/gecko version from manifest.xml file')
    parser.add_option('-f', '--file', help='specify the manifest file', action='store', type='string', dest='file', default="")
    (options, args) = parser.parse_args()

    # if there is no OTA MAR update file exist, quit.
    if options.file == None:
        parser.print_help()
        exit(-1)
    if not os.path.isfile(options.file):
        print 'File not exist.'
        exit(-1)

    isGaiaFound = False
    isGeckoFound = False

    tree = ET.parse(options.file)
    root = tree.getroot()
    for project in root.findall('project'):
        if project.get('path') == 'gaia':
            print 'GAIA_BRANCH=%s/%s' % (project.get('remote'), project.get('revision'))
            isGaiaFound = True
        elif project.get('path') == 'gecko':
            print 'GECKO_BRANCH=%s/%s' % (project.get('remote'), project.get('revision'))
            isGeckoFound = True
        if isGaiaFound and isGeckoFound:
            break


if __name__ == '__main__':
    main()
