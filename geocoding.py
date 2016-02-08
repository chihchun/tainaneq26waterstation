#!/usr/bin/Python
# vim: set fileencoding=utf-8 :
import sys
import csv
import urllib2
import json
import time
from pykml.factory import KML_ElementMaker as KML
from pykml.factory import GX_ElementMaker as GX
from pykml.factory import ATOM_ElementMaker as ATOM
from lxml import etree


doc = KML.kml(
    KML.Document(
      KML.name(u"台南臨時供水站地點 (105-02-08 18:20)"),
      KML.description(u"自來水處已於 2016-02-08 架設完成之臨時供水站地點<br>來源: http://www.water.gov.tw/06news/news_b_main2.asp?no_g=6226<br>編輯聯繫: rex.cc.tsai@gmail.com<br>"),
    )
)
stations = KML.Folder(KML.name(u'臨時供水站'), id='stations')
doc.append(stations)

with open('2016-02-08-1820.csv', 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='\"')
    for row in csvreader:
        response = urllib2.urlopen("http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % urllib2.quote(row[5]))
        data = json.load(response)

        # debug purpose
        if data['status'] != "OK" or len(data['results']) != 1:
            print "%s,%s,%s" % (row[0],row[5], data)
        assert(data['status'] == 'OK')
        assert(len(data['results']) == 1)

        # build placemakers
        pm = KML.Placemark(
            KML.name(u"%s%s" % (row[2].decode("utf8"), row[3].decode("utf8"))),
            KML.description(u"%s - %s%s%s<br>%s<br>%s %s" %
                (row[0],
                row[1].decode("utf8"),
                row[2].decode("utf8"),
                row[3].decode("utf8"),
                row[4].decode("utf8"),
                row[8].decode("utf8"),
                row[9].decode("utf8"),
                )),
            KML.styleUrl("#icon-1067"),
            KML.Point(
            KML.coordinates("%s,%s,0,0" % (data['results'][0]['geometry']['location']['lng'], data['results'][0]['geometry']['location']['lat']))
            )
        )
        print etree.tostring(pm, encoding='utf8', pretty_print=True)
        stations.append(pm)

# output a KML file (named based on the Python script)
outfile = file("stations.kml",'w')
outfile.write(etree.tostring(doc, encoding='utf8',pretty_print=True))
# print etree.tostring(stations, encoding='utf8', pretty_print=True)
