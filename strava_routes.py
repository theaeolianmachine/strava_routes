import sys
import re

from xml.etree import ElementTree

GPX_NAMESPACE = 'http://www.topografix.com/GPX/1/1'
ElementTree.register_namespace('', GPX_NAMESPACE)

def register_namespace(root_element):
    namespace = re.match(r'\{(.*?)\}', root_element.tag).group(1)
    ElementTree.register_namespace('', namespace)
    return namespace

def qualify_tag(namespace, tag_name):
    return '{{{}}}{}'.format(namespace, tag_name)

def main(file_name):
    tree = ElementTree.parse(file_name)
    gpx_root = tree.getroot()
    namespace = register_namespace(gpx_root)
    for track in gpx_root.findall(qualify_tag(namespace, 'trk')):
        solo_segment = ElementTree.Element(qualify_tag(namespace, 'trkseg'))
        for seg in track.findall(qualify_tag(namespace, 'trkseg')):
            solo_segment.extend(seg.findall(qualify_tag(namespace, 'trkpt')))
            track.remove(seg)
        track.append(solo_segment)
    tree.write(
        'movescount.gpx', xml_declaration=True, short_empty_elements=False)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: strava_routes.py [file_name]")
    main(sys.argv[1])
