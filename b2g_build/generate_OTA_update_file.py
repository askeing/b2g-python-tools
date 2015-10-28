import os
import optparse
import hashlib
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

'''
Author: Askeing (askeing@gmail.com)

ref: https://wiki.mozilla.org/B2G/Updating

<?xml version='1.0'?>
<updates>
  <update type='minor' appVersion='19.0' version='19.0' extensionVersion='19.0' buildID='20130101000000'
          licenseURL='http://www.mozilla.com/test/sample-eula.html'
          detailsURL='http://www.mozilla.com/test/sample-details.html'>
    <patch type='complete' URL='http://path.to.update.file/b2g-gecko-update.mar'
           hashFunction='SHA512' hashValue='2d70e806f55c2f2a87eae4bda9a91306e5e2d157de892001a84e7464cc170d9d95e35654d8aec02e06c1e0b102474d125e072ef024e702474d125e072ef024e7'
           size='78900000'/>
  </update>
</updates>
'''


def main():
    parser = optparse.OptionParser(description='Generate OTA update.xml file')
    parser.add_option('-f', '--file', help='specify the update mar file', action='store', type='string', dest='file')
    parser.add_option('-b', '--buildid', help='specify the BuildID', action='store', type='int', dest='buildid', default=0)
    parser.add_option('-p', '--partial', help='specify the type of the update is partial, not complete', action='store_true', dest='partial', default=False)
    parser.add_option('-M', '--major', help='specify the update is major update, not minor', action='store_true', dest='major', default=False)
    parser.add_option('-v', '--version', help='specify the update version', action='store', type='int', dest='version', default=22)
    parser.add_option('-u', '--url', help='specify the URL of update mar file', action='store', type='string', dest='url', default='')
    parser.add_option('-o', '--output', help='specify the output update.xml file', action='store', type='string', dest='output', default='out/update.xml')
    (options, args) = parser.parse_args()

    # if there is no OTA MAR update file exist, quit.
    if options.file == None:
        parser.print_help()
        exit(-1)
    if not os.path.isfile(options.file):
        print 'File not exist.'
        exit(-1)

    # calculate OTA MAR update file SHA512
    f = open(options.file)
    ota_sha = sha512_for_file(f)
    f.close()

    # calculate OTA MAR update file size
    ota_size = os.path.getsize(options.file)

    # Generate OTA update.xml skeleton
    output_updates = ET.Element('updates')
    output_update = ET.SubElement(output_updates, 'update')
    output_patch = ET.SubElement(output_update, 'patch')

    # Generate OTA update.xml update info
    if options.major:
        output_update.set('type', 'major')
    else:
        output_update.set('type', 'minor')
    update_version = str(float(options.version))
    output_update.set('appVersion', update_version)
    output_update.set('version', update_version)
    output_update.set('extensionVersion', update_version)
    output_update.set('buildID', str(options.buildid))
    output_update.set('licenseURL', 'http://www.mozilla.com/test/sample-eula.html')
    output_update.set('detailsURL', 'http://www.mozilla.com/test/sample-details.html')

    # Generate OTA update.xml patch info
    if options.partial:
        output_patch.set('type', 'partial')
    else:
        output_patch.set('type', 'complete')
    output_patch.set('URL', options.url)
    output_patch.set('hashFunction', 'SHA512')
    output_patch.set('hashValue', ota_sha)
    output_patch.set('size', str(ota_size))

    # Output OTA update.xml file
    #ET.dump(output_updates)
    output_file = options.output
    if not os.path.exists(output_file):
        try:
            os.makedirs(output_file[:output_file.rindex('/')])
        except OSError as e:
            print e.message
    f = open(output_file, 'w')
    xml = ET.tostring(output_updates)
    xml_dom = parseString(xml)
    f.write(xml_dom.toprettyxml())
    f.close()


def sha512_for_file(f, block_size=2 ** 20):
    sha512 = hashlib.sha512()
    while True:
        data = f.read(block_size)
        if not data:
            break
        sha512.update(data)
    return sha512.hexdigest()


if __name__ == '__main__':
    main()
