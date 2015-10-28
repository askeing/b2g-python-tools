import os
import optparse
import hashlib
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

'''
Author: Askeing (askeing@gmail.com)

ref: https://github.com/mozilla-b2g/b2g-manifest
Generate sources.xml:
  $B2G_HOME/gonk-misc/add-revision.py -o sources.xml --force .repo/manifest.xml
'''


def main():
    parser = optparse.OptionParser(description='Retrieve gaia/gecko revision from source.xml file')
    parser.add_option('-f', '--file', help='specify the source.xml file', action='store', type='string', dest='file')
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
            print 'GAIA_REV=%s' % project.get('revision')
            isGaiaFound = True
        elif project.get('path') == 'gecko':
            print 'GECKO_REV=%s' % project.get('revision')
            isGeckoFound = True
        if isGaiaFound and isGeckoFound:
            break


if __name__ == '__main__':
    main()
