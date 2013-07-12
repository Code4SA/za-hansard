from __future__ import with_statement

from datetime import datetime

from django.test import TestCase
from zah.parse import ZAHansardParser
from lxml import etree

import itertools
import sys, os

class ZAHansardParsingTests(TestCase):

    docname = '502914_1'
    xml = None

    @classmethod
    def setUpClass(cls):
        cls._in_fixtures = os.path.join('zah', 'fixtures', 'test_inputs')
        obj = cls.do_parse(cls.docname)
        cls.xml = obj.akomaNtoso
        cls.xml_string = etree.tostring(obj.akomaNtoso, pretty_print=True)

    @classmethod
    def do_parse(cls, docname):
        filename = os.path.join( cls._in_fixtures, '%s.%s' % (docname, 'doc') )
        return ZAHansardParser.parse(filename)

    def test_basic_parse(self):
        xml_path = os.path.join( self._in_fixtures, '%s.%s' % (self.docname, 'xml') )
        xml_expected = open( xml_path ).read()

        xml_expected = xml_expected.replace('YYYY-MM-DD', datetime.now().strftime('%Y-%m-%d'))

        if self.xml_string != xml_expected:
            outname = './%s.%s' % (self.docname, 'xml')
            open( outname, 'w').write(self.xml_string)
            self.assertTrue( self.xml_string == xml_expected, "XML not correct, see %s for output" % outname )

    def test_xsd(self):
        xsd_path = os.path.join( self._in_fixtures, 'release-23.xsd')
        xsd_parser = etree.XMLParser(dtd_validation=False)
        xsd = etree.XMLSchema(
                etree.parse(xsd_path, xsd_parser))
        parser = etree.XMLParser(schema = xsd)
        try:
            xml = etree.fromstring(self.xml_string, parser)
            self.assertEqual(xml.tag, '{http://docs.oasis-open.org/legaldocml/ns/akn/3.0/CSD03}akomaNtoso', 'Validated ok')
        except etree.XMLSyntaxError as e:
            self.assertTrue(False, e)

    def test_properties(self):
        xml = self.xml

        self.assertEqual(xml.tag, '{http://docs.oasis-open.org/legaldocml/ns/akn/3.0/CSD03}akomaNtoso')

        preface_p = xml.debate.preface.p
        self.assertEqual(preface_p.text, 'Thursday, ')
        docDate = preface_p.docDate
        self.assertEqual(docDate.text, '14 February 2013')
        self.assertEqual(docDate.get('date'), '2013-02-14')

        debateBody = xml.debate.debateBody
        mainSection = debateBody.debateSection
        self.assertEqual(mainSection.get('id'), 'db0')
        self.assertEqual(mainSection.get('name'), 'proceedings-at-joint-sitting')
        self.assertEqual(mainSection.heading.text, 'PROCEEDINGS AT JOINT SITTING')
        self.assertEqual(mainSection.p.text, 'Members of the National Assembly and the National Council of Provinces assembled in the Chamber of the National Assembly at ')
        recordedTime = mainSection.p.recordedTime
        self.assertEqual(recordedTime.text, '19:01')
        self.assertEqual(recordedTime.get('time'), '19:01:00')
        self.assertEqual(mainSection.prayers.p.text, 'The Speaker took the Chair and requested members to observe a moment of silence for prayers or meditation.')
        
        subSections = mainSection.findall('{*}debateSection')
        #for s in subSections:
            # print >> sys.stderr, s.get('id')
        self.assertEqual(len(subSections), 3)

        dbs1 = subSections[0]
        self.assertEqual(dbs1.get('id'), 'dbs1')
        self.assertEqual(dbs1.heading.text, 'CALLING OF JOINT SITTING')
        speech = dbs1.speech
        self.assertEqual(speech.get('by'), '#the-speaker')
        self.assertEqual(speech['from'].text, 'The SPEAKER')
        self.assertEqual(speech.p.text, 'Hon members, the President has called this Joint Sitting of the National Assembly and the National Council of Provinces in terms of section 84(2)(d) of the Constitution of the Republic of South Africa, read with Joint Rule 7(1)(a), to enable him to deliver his state of the nation address to Parliament. I now invite the honourable the President to address the Joint Sitting. [Applause.]')

        dbs2 = subSections[1]
        self.assertEqual(dbs2.get('id'), 'dbs2')
        self.assertEqual(dbs2.heading.text, 'ADDRESS BY PRESIDENT OF THE REPUBLIC')
        speech = dbs2.speech
        self.assertEqual(speech.get('by'), '#the-president-of-the-republic')
        self.assertEqual(speech['from'].text, 'The PRESIDENT OF THE REPUBLIC')
        ps = speech.findall('{*}p')
        self.assertEqual(len(ps), 141)
        self.assertEqual(ps[1], '... anizukusho ukuthi hayi iyaziqhenya le nsizwa bo. Ikhuluma, ikhulume bese isula ngeduku. [... that you will not label me as somebody who is very proud, who speaks for a while and then wipes his face with a handkerchief.]')

        dbs3 = subSections[2]
        self.assertEqual(dbs3.get('id'), 'dbs3')
        speeches = dbs3.findall('{*}speech')
        self.assertEqual(len(speeches), 2)

        self.assertEqual(len(speeches[1].findall('{*}p')), 2)

        adjournment = dbs3.adjournment
        self.assertEqual(adjournment.p.text, 'The Joint Sitting rose at ')
        recordedTime = adjournment.p.recordedTime
        self.assertEqual(recordedTime.text, '20:28')
        self.assertEqual(recordedTime.get('time'), '20:28:00')

        # TEST that references have been gathered correctly
        tlcpersons = xml.debate.meta.references.findall('{*}TLCPerson')
        self.assertEqual( len(tlcpersons), 3 )
        speeches_by_speaker = filter(
                lambda s: s.get('by') == '#the-speaker',
                mainSection.findall('.//{*}speech'))
        self.assertEqual( len(speeches_by_speaker), 2 )
        for speech in speeches_by_speaker:
            self.assertEqual( speech['from'].text, 'The SPEAKER' )

    def test_second_parse(self):
        obj = self.do_parse('NA290307')
        xml = obj.akomaNtoso
        self.assertTrue(xml is not None)
        debateBody = xml.debate.debateBody
        mainSection = debateBody.debateSection 
        subSections = mainSection.findall('{*}debateSection')
        self.assertEqual(len(subSections), 13)