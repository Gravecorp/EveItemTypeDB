#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2, json
import MySQLdb as mdb
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, fromstring
from xml.dom import minidom
import codecs
# encoding=utf8
import sys

reload(sys)
sys.setdefaultencoding('utf8')

# mysql connection data
dbhost = ''
dbuser = ''
dbpassword = ''
dbdatabase = ''


# settings
output = u"xml"
xmlRowFormat = u"<{0} {1}=\"{2}\" {3}=\"{4}\" />"
xmlRowName = u"item"
xmlTypeIdName = u"id"
xmlTypeName = u"name"

# global
mysqlConnection = None
xmlDoc = None

def getPage(url):
    print("url: " + url)
    request = urllib2.urlopen(url)
    data = json.load(request)
    processData(data)
    nexturl = getNext(data)
    if(nexturl != None):
        # finishProcessing()
        getPage(nexturl)
    else:
        finishProcessing()


def getNext(data):
    ret = None
    if 'next' in data:
        ret = data['next']['href']
    return ret

def processData(data):
    items = data['items']
    values = {}
    for item in items:
        itemid = str(item['id']).encode("utf-8")
        itemname = item['name'].encode('utf-8')
        values.update({itemid: itemname})
    insertIntoOutput(values)

def insertIntoOutput(values):
    if(output == 'xml'):
        insertIntoXml(values)
    if(output == 'mysql'):
        insertIntoDB(values)

def insertIntoXml(values):
    doc = getXmlDoc()
    for itemid, itemname in values.iteritems():
        xmlstring = xmlRowFormat.format(xmlRowName, xmlTypeIdName, itemid, xmlTypeName, itemname)
        print (xmlstring)
        ele = fromstring(xmlstring)
        doc.append(ele)

def getXmlDoc():
    ret = None
    if(xmlDoc == None):
        ret = generateXmlDoc()
    else:
        ret = xmlDoc
    return ret

def generateXmlDoc():
    global xmlDoc
    xmlDoc = Element('eveitemid')
    return xmlDoc

def insertIntoDB(values):
    con = getDatabase()
    for itemid, itemname in values.iteritems():
        print("itemID: " + itemid + " itemName: " + itemname)

def getDatabase():
    ret = None
    if(mysqlConnection == None):
        ret = None
        # connect to db here

    return ret

def finishProcessing():
    if (output == 'xml'):
        rough_string = tostring(getXmlDoc(), 'utf-8')
        reparsed = minidom.parseString(rough_string)
        prettyxml = reparsed.toprettyxml(indent="  ")
        with codecs.open("itemid.xml", "w", encoding="utf-8") as f:
            f.write(prettyxml)
    if(output == 'mysql'):
        # close the connection here
        thingie = 0

# startup logic
getPage("https://public-crest.eveonline.com/types/?page=28")