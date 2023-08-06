from unittest import TestCase

from cifter import parser


class TestParser(TestCase):

    def test_check_comments_true(self):
        comment_line = "/!! Start of file"
        self.assertTrue(parser.is_comment(comment_line))

    def test_check_comments_false(self):
        non_comment = "BSNY532909805249809200000001 POO2T07    124207004 EMU319 100D     B        P"
        self.assertFalse(parser.is_comment(non_comment))

    def test_single_record(self):
        itterable = EXAMPLE_SINGLE_RECORD.split('\n')
        document = parser.parse_itterable(itterable)
        self.assertEqual(len(document.schedule_records), 1)


EXAMPLE_SINGLE_RECORD = """BSNQ458352009072009111111100 1XX1A5651  124632104 EMU    100      B            N
BX         SWYSW430300                                                          
LOALTON   1644 16441         TB                                                 
LIBNTEY   1650 1651      165016511        T                                     
LIFARNHAM 1656 1658      165616581        T X                                   
LIALDRSHT 1703H1704H     170417041        T                                     
LIALDRSJN           1706H00000000                                               
LIASHVALE 1708 1709      17081709         T                                     
LIPRBRITJ           1713H00000000   SL                                          
LIBRKWOOD 1715H1716      17161716         T                                     
LIWOKINGJ           1719H00000000                                               
LIWOKING  1720H1722H     172117221        T                                     
LIWBYFLET 1726H1727H     17271727         T                                     
LIBYFLANH           1729H00000000                                               
LIWEYBDGE           1730H000000002                                              
LIHCRTJN            1735 00000000                                               
LISURBITN 1736H1738      173717381  FL SL T             2                       
LINEWMLDN           1744 00000000                                               
LIWDON              1746 000000006                      1                       
LICLPHMJM 1751H1753      175217537  MFL   T             3H                      
LTWATRLMN 1804 180414    TF                                                     """