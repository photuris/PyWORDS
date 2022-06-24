import unittest
import random
import sqlite3
import pywords.lookup as lookup
import pywords.definitions as definitions
from pywords.matchfilter import MatchFilter
from generate_database import verify_database


def build_dictline_from_str(s):
    ps = s[:34].split()
    senses = s[34:]
    pos = definitions.parts_of_speech[ps[0]]
    if pos == 'noun':
        return definitions.DictlineNounEntry(ps[0],ps[1],ps[2],ps[3],ps[4],ps[5],ps[6],ps[7],ps[8],ps[9],senses)
    if pos == 'adjective':
        return definitions.DictlineAdjectiveEntry(ps[0],ps[1],ps[2],ps[3],ps[4],ps[5],ps[6],ps[7],ps[8],senses)
    if pos == 'verb':
        return definitions.DictlineVerbEntry(ps[0],ps[1],ps[2],ps[3],ps[4],ps[5],ps[6],ps[7],ps[8],senses)
    if pos == 'adverb':
        return definitions.DictlineAdverbEntry(ps[0],ps[1],ps[2],ps[3],ps[4],ps[5],ps[6],senses)
    if pos == 'conjunction':
        return definitions.DictlineConjunctionEntry(ps[0],ps[1],ps[2],ps[3],ps[4],ps[5],senses)
    if pos in ['pronoun','pack (internal use only)']:
        return definitions.DictlinePronounEntry(ps[0],ps[1],ps[2],ps[3],ps[4],ps[5],ps[6],ps[7],ps[8],senses)
    if pos == 'number':
        return definitions.DictlineNumberEntry(ps[0],ps[1],ps[2],ps[3],ps[4],ps[5],ps[6],ps[7],ps[8],ps[9],senses)
    if pos == 'preposition':
        return definitions.DictlinePrepositionEntry(ps[0],ps[1],ps[2],ps[3],ps[4],ps[5],ps[6],senses)
    if pos == 'interjection':
        return definitions.DictlineInterjectionEntry(ps[0],ps[1],ps[2],ps[3],ps[4],ps[5],senses)


class TestDictlineClasses(unittest.TestCase):
    def test_dictline_noun_entry_eq(self):
        noun1 = definitions.DictlineNounEntry(pos='N',decl='1',variant='1',gender='M',noun_kind='T',age='A',area='Y',
                                              geog='C',freq='A',src='X',senses='definitions, arbitrarily filled')
        noun2 = definitions.DictlineNounEntry(pos='N',decl='1',variant='1',gender='M',noun_kind='T',age='A',area='Y',
                                              geog='C',freq='A',src='X',senses='definitions, arbitrarily filled')
        self.assertTrue(noun1 == noun2)

    def test_dictline_noun_entry_not_eq(self):
        noun1 = definitions.DictlineNounEntry(pos='N',decl='1',variant='1',gender='M',noun_kind='T',age='A',area='Y',
                                              geog='C',freq='A',src='X',senses='definitions, arbitrarily filled')
        noun3 = definitions.DictlineNounEntry(pos='N',decl='2',variant='1',gender='M',noun_kind='T',age='A',area='Y',
                                              geog='C',freq='A',src='X',senses='definitions, arbitrarily filled')
        self.assertFalse(noun1 == noun3)

    def test_dictline_pronoun_entry_eq(self):
        pron1 = definitions.DictlinePronounEntry(pos='PRON',decl='1',variant='1',pronoun_kind='PERS',age='A',area='Y',
                                                 geog='A',freq='X',src='A',senses='definitions, arbitrarily filled')
        pron2 = definitions.DictlinePronounEntry(pos='PRON',decl='1',variant='1',pronoun_kind='PERS',age='A',area='Y',
                                                 geog='A',freq='X',src='A',senses='definitions, arbitrarily filled')
        self.assertTrue(pron1 == pron2)

    def test_dictline_pronoun_entry_not_eq(self):
        pron1 = definitions.DictlinePronounEntry(pos='PRON',decl='1',variant='1',pronoun_kind='PERS',age='A',area='Y',
                                                 geog='A',freq='X',src='A',senses='definitions, arbitrarily filled')
        pron3 = definitions.DictlinePronounEntry(pos='PRON',decl='1',variant='2',pronoun_kind='PERS',age='A',area='Y',
                                                 geog='A',freq='X',src='A',senses='definitions, arbitrarily filled')
        self.assertFalse(pron1 == pron3)


class TestLookup(unittest.TestCase):
    def setUp(self):
        pass
        #verify_database()  # Build or verify database
        #self.db_conn = sqlite3.connect('words.db')
        #self.db_curs = self.db_conn.cursor()

    def tearDown(self):
        pass
        #self.db_conn.close()

    def test_find_endings_splices(self):
        self.assertEqual(lookup.find_endings("aqua"),[4,3,2])
        self.assertEqual(lookup.find_endings("aqua") , [4, 3, 2])
        self.assertEqual(lookup.find_endings("aquae") , [5, 4, 3])
        self.assertEqual(lookup.find_endings("epitome") , [7, 6, 5])
        self.assertEqual(lookup.find_endings("epitomes") , [8, 7, 6])
        self.assertEqual(lookup.find_endings("cometes") , [7, 6, 5])
        self.assertEqual(lookup.find_endings("cometae") , [7, 6, 5])
        self.assertEqual(lookup.find_endings("Archias") , [7, 6, 5, 4])
        self.assertEqual(lookup.find_endings("Archiae") , [7, 6, 5])
        self.assertEqual(lookup.find_endings("amicus") , [6, 5, 4])
        self.assertEqual(lookup.find_endings("amici") , [5, 4])
        self.assertEqual(lookup.find_endings("verbum") , [6, 4])
        self.assertEqual(lookup.find_endings("verbi") , [5, 4])
        self.assertEqual(lookup.find_endings("puer") , [4, 2])
        self.assertEqual(lookup.find_endings("pueri") , [5, 4, 3, 2])
        self.assertEqual(lookup.find_endings("ager") , [4, 2])
        self.assertEqual(lookup.find_endings("agri") , [4, 3, 2])
        self.assertEqual(lookup.find_endings("radius") , [6, 5, 4, 3])
        self.assertEqual(lookup.find_endings("radii") , [5, 4, 3])
        self.assertEqual(lookup.find_endings("atrium") , [6, 4, 3])
        self.assertEqual(lookup.find_endings("atrii") , [5, 4, 3])
        self.assertEqual(lookup.find_endings("atri") , [4, 3, 2])
        self.assertEqual(lookup.find_endings("filius") , [6, 5, 4, 3])
        self.assertEqual(lookup.find_endings("fili") , [4, 3])
        self.assertEqual(lookup.find_endings("Lucius") , [6, 5, 4, 3])
        self.assertEqual(lookup.find_endings("Lucii") , [5, 4, 3])
        self.assertEqual(lookup.find_endings("barbitos") , [8, 7, 6] )
        self.assertEqual(lookup.find_endings("barbiti") , [7, 6])
        self.assertEqual(lookup.find_endings("Androgeos") , [9, 8, 7])
        self.assertEqual(lookup.find_endings("Androgeo") , [8, 7, 6])
        self.assertEqual(lookup.find_endings("amphibrachys") , [12, 11])
        self.assertEqual(lookup.find_endings("amphibrachyos") , [13, 12, 11, 10])
        self.assertEqual(lookup.find_endings("chelys") , [6, 5])
        self.assertEqual(lookup.find_endings("Ilion") , [5, 3])
        self.assertEqual(lookup.find_endings("Ilii") , [4, 3, 2])
        self.assertEqual(lookup.find_endings("Panthus") , [7, 6, 5])
        self.assertEqual(lookup.find_endings("Panthi") , [6, 5])
        self.assertEqual(lookup.find_endings("miles") , [5, 4, 3, 2])
        self.assertEqual(lookup.find_endings("militis") , [7, 6, 5, 4, 3])
        self.assertEqual(lookup.find_endings("frater") , [6, 4])
        self.assertEqual(lookup.find_endings("fratris") , [7, 6, 5, 4])
        self.assertEqual(lookup.find_endings("soror") , [5, 3])
        self.assertEqual(lookup.find_endings("sororis") , [7, 6, 5, 4, 3])
        self.assertEqual(lookup.find_endings("pulchritudo") , [11, 10])
        self.assertEqual(lookup.find_endings("pulchritudinis") , [14, 13, 12])
        self.assertEqual(lookup.find_endings("legio") , [5, 4])
        self.assertEqual(lookup.find_endings("legionis") , [8, 7, 6])
        self.assertEqual(lookup.find_endings("varietas") , [8, 7, 6])
        self.assertEqual(lookup.find_endings("varietatis") , [10, 9, 8, 7, 6])
        self.assertEqual(lookup.find_endings("radix") , [5])
        self.assertEqual(lookup.find_endings("radicis") , [7, 6, 5])
        self.assertEqual(lookup.find_endings("nomen") , [5, 3])
        self.assertEqual(lookup.find_endings("nominis") , [7, 6, 5])
        self.assertEqual(lookup.find_endings("iter") , [4, 2])
        self.assertEqual(lookup.find_endings("itineris") , [8, 7, 6, 5, 4])
        self.assertEqual(lookup.find_endings("tempus") , [6, 5, 4])
        self.assertEqual(lookup.find_endings("temporis") , [8, 7, 6, 5, 4])
        self.assertEqual(lookup.find_endings("hostis") , [6, 5, 4, 3])
        self.assertEqual(lookup.find_endings("finis") , [5, 4, 3])
        self.assertEqual(lookup.find_endings("urbs") , [4, 3])
        self.assertEqual(lookup.find_endings("urbis") , [5, 4, 3, 2])
        self.assertEqual(lookup.find_endings("mons") , [4, 3])
        self.assertEqual(lookup.find_endings("montis") , [6, 5, 4, 3])
        self.assertEqual(lookup.find_endings("mare") , [4, 3, 2, 1])
        self.assertEqual(lookup.find_endings("maris") , [5, 4, 3, 2, 1])
        self.assertEqual(lookup.find_endings("animal") , [6])
        self.assertEqual(lookup.find_endings("animalis") , [8, 7, 6])
        self.assertEqual(lookup.find_endings("exemplar") , [8, 6])
        self.assertEqual(lookup.find_endings("exemplaris") , [10, 9, 8, 7, 6])
        self.assertEqual(lookup.find_endings("aer") , [3, 1])
        self.assertEqual(lookup.find_endings("aeris") , [5, 4, 3, 2, 1])
        self.assertEqual(lookup.find_endings("lampas") , [6, 5, 4])
        self.assertEqual(lookup.find_endings("lampados") , [8, 7, 6])
        self.assertEqual(lookup.find_endings("Moses") , [5, 4, 3, 2])
        self.assertEqual(lookup.find_endings("Mosis") , [5, 4, 3])
        self.assertEqual(lookup.find_endings("Ulixes") , [6, 5, 4])
        self.assertEqual(lookup.find_endings("Ulixis") , [6, 5, 4])
        self.assertEqual(lookup.find_endings("Ulixi") , [5, 4])
        self.assertEqual(lookup.find_endings("Ulixei") , [6, 5, 4])
        self.assertEqual(lookup.find_endings("Achilles") , [8, 7, 6, 5])
        self.assertEqual(lookup.find_endings("Achillis") , [8, 7, 6])
        self.assertEqual(lookup.find_endings("tigris") , [6, 5, 4, 3])
        self.assertEqual(lookup.find_endings("tigridis") , [8, 7, 6])
        self.assertEqual(lookup.find_endings("praxis") , [6, 5, 4])
        self.assertEqual(lookup.find_endings("praxios") , [7, 6, 5])
        self.assertEqual(lookup.find_endings("haeresis") , [8, 7, 6])
        self.assertEqual(lookup.find_endings("haereseos") , [9, 8, 7])
        self.assertEqual(lookup.find_endings("pater") , [5, 3])
        self.assertEqual(lookup.find_endings("patros") , [6, 5, 4])
        self.assertEqual(lookup.find_endings("manus") , [5, 4, 3])
        self.assertEqual(lookup.find_endings("passus") , [6, 5, 4])
        self.assertEqual(lookup.find_endings("genu") , [4, 3])
        self.assertEqual(lookup.find_endings("genus") , [5, 4, 3, 1])
        self.assertEqual(lookup.find_endings("cornu") , [5, 4])
        self.assertEqual(lookup.find_endings("cornus") , [6, 5, 4])
        self.assertEqual(lookup.find_endings("dies") , [4, 3, 2, 1])
        self.assertEqual(lookup.find_endings("diei") , [4, 3, 2])
        self.assertEqual(lookup.find_endings("res") , [3, 2, 1])
        self.assertEqual(lookup.find_endings("rei") , [3, 2, 1])
        self.assertEqual(lookup.find_endings("reibus") , [6, 5, 4, 2])
        self.assertEqual(lookup.find_endings("fas") , [3, 2, 1])

    def test__simple_match_nouns(self):
        # Build dictline entries we expect to see
        aqua_dictline_str   = "N      1 1 F T          X X X A O water; sea, lake; river, stream; rain, rainfall (pl.), rainwater; spa; urine;"
        Mos_dictline_str    = "N      1 1 F T          X X N E O river Maas/Meuse, in Holland/France/Belgium;"
        Moses_dictline_str  = "N      3 8 M P          E E Q E E Moses;"
        aqua_dl_entry = build_dictline_from_str(aqua_dictline_str)
        Mos_dl_entry = build_dictline_from_str(Mos_dictline_str)
        Moses_dl_entry = build_dictline_from_str(Moses_dictline_str)

        # Find endings 'aqua':'', 'aqu':'a', select only 'aqu':'a', find dictline for 'aqu', ignore deponent verb
        # 'aquor' because there is no 'a' ending in the passive voice (there is in the active however)
        self.assertEqual(lookup._simple_match('aqua'),[['aqu','a',{'stem1':'aqu','stem2':'aqu','stem3':'','stem4':'','entry':aqua_dl_entry}]])
        self.assertEqual(lookup._simple_match('aquae'),[['aqu','ae',{'stem1':'aqu','stem2':'aqu','stem3':'','stem4':'','entry':aqua_dl_entry}]])

        # Find endings 'Moses':'', 'Mos':'es', both return same noun
        self.assertEqual(lookup._simple_match('Moses'),[['Moses','',{'stem1':'Moses','stem2':'Mos','stem3':'','stem4':'','entry':Moses_dl_entry}],
                                                        ['Mos','es',{'stem1':'Moses','stem2':'Mos','stem3':'','stem4':'','entry':Moses_dl_entry}]])
        # Find endings 'Mos':'is' (x2), one for Mos and one for Moses
        self.assertEqual(lookup._simple_match('Mosis'),[['Mos','is',{'stem1':'Mos','stem2':'Mos','stem3':'','stem4':'','entry':Mos_dl_entry}],
                                                        ['Mos','is',{'stem1':'Moses','stem2':'Mos','stem3':'','stem4':'','entry':Moses_dl_entry}]])

        #self.assertEqual(lookup._simple_match('aquae'))
        #self.assertEqual(lookup._simple_match('epitome'))
        #self.assertEqual(lookup._simple_match('epitomes'))
        #self.assertEqual(lookup._simple_match('cometes'))
        #self.assertEqual(lookup._simple_match('cometae'))
        #self.assertEqual(lookup._simple_match('Archias'))
        #self.assertEqual(lookup._simple_match('Archiae'))
        #self.assertEqual(lookup._simple_match('amicus'))
        #self.assertEqual(lookup._simple_match('amici'))
        #self.assertEqual(lookup._simple_match('verbum'))
        #self.assertEqual(lookup._simple_match('verbi'))
        #self.assertEqual(lookup._simple_match('puer'))
        #self.assertEqual(lookup._simple_match('pueri'))
        #self.assertEqual(lookup._simple_match('ager'))
        #self.assertEqual(lookup._simple_match('agri'))
        #self.assertEqual(lookup._simple_match('radius'))
        #self.assertEqual(lookup._simple_match('radii'))
        #self.assertEqual(lookup._simple_match('atrium'))
        #self.assertEqual(lookup._simple_match('atrii'))
        #self.assertEqual(lookup._simple_match('atri'))
        #self.assertEqual(lookup._simple_match('filius'))
        #self.assertEqual(lookup._simple_match('fili'))
        #self.assertEqual(lookup._simple_match('Lucius'))
        #self.assertEqual(lookup._simple_match('Lucii'))
        #self.assertEqual(lookup._simple_match('barbitos'))
        #self.assertEqual(lookup._simple_match('barbiti'))
        #self.assertEqual(lookup._simple_match('Androgeos'))
        #self.assertEqual(lookup._simple_match('Androgeo'))
        #self.assertEqual(lookup._simple_match('amphibrachys'))
        #self.assertEqual(lookup._simple_match('amphibrachyos'))
        #self.assertEqual(lookup._simple_match('chelys'))
        #self.assertEqual(lookup._simple_match('Ilion'))
        #self.assertEqual(lookup._simple_match('Ilii'))
        #self.assertEqual(lookup._simple_match('Panthus'))
        #self.assertEqual(lookup._simple_match('Panthi'))
        #self.assertEqual(lookup._simple_match('miles'))
        #self.assertEqual(lookup._simple_match('militis'))
        #self.assertEqual(lookup._simple_match('frater'))
        #self.assertEqual(lookup._simple_match('fratris'))
        #self.assertEqual(lookup._simple_match('soror'))
        #self.assertEqual(lookup._simple_match('sororis'))
        #self.assertEqual(lookup._simple_match('pulchritudo'))
        #self.assertEqual(lookup._simple_match('pulchritudinis'))
        #self.assertEqual(lookup._simple_match('legio'))
        #self.assertEqual(lookup._simple_match('legionis'))
        #self.assertEqual(lookup._simple_match('varietas'))
        #self.assertEqual(lookup._simple_match('varietatis'))
        #self.assertEqual(lookup._simple_match('radix'))
        #self.assertEqual(lookup._simple_match('radicis'))
        #self.assertEqual(lookup._simple_match('nomen'))
        #self.assertEqual(lookup._simple_match('nominis'))
        #self.assertEqual(lookup._simple_match('iter'))
        #self.assertEqual(lookup._simple_match('itineris'))
        #self.assertEqual(lookup._simple_match('tempus'))
        #self.assertEqual(lookup._simple_match('temporis'))
        #self.assertEqual(lookup._simple_match('hostis'))
        #self.assertEqual(lookup._simple_match('finis'))
        #self.assertEqual(lookup._simple_match('urbs'))
        #self.assertEqual(lookup._simple_match('urbis'))
        #self.assertEqual(lookup._simple_match('mons'))
        #self.assertEqual(lookup._simple_match('montis'))
        #self.assertEqual(lookup._simple_match('mare'))
        #self.assertEqual(lookup._simple_match('maris'))
        #self.assertEqual(lookup._simple_match('animal'))
        #self.assertEqual(lookup._simple_match('animalis'))
        #self.assertEqual(lookup._simple_match('exemplar'))
        #self.assertEqual(lookup._simple_match('exemplaris'))
        #self.assertEqual(lookup._simple_match('aer'))
        #self.assertEqual(lookup._simple_match('aeris'))
        #self.assertEqual(lookup._simple_match('lampas'))
        #self.assertEqual(lookup._simple_match('lampados'))
        #self.assertEqual(lookup._simple_match('Moses'))
        #self.assertEqual(lookup._simple_match('Mosis'))
        #self.assertEqual(lookup._simple_match('Ulixes'))
        #self.assertEqual(lookup._simple_match('Ulixis'))
        #self.assertEqual(lookup._simple_match('Ulixi'))
        #self.assertEqual(lookup._simple_match('Ulixei'))
        #self.assertEqual(lookup._simple_match('Achilles'))
        #self.assertEqual(lookup._simple_match('Achillis'))
        #self.assertEqual(lookup._simple_match('tigris'))
        #self.assertEqual(lookup._simple_match('tigridis'))
        #self.assertEqual(lookup._simple_match('praxis'))
        #self.assertEqual(lookup._simple_match('praxios'))
        #self.assertEqual(lookup._simple_match('haeresis'))
        #self.assertEqual(lookup._simple_match('haereseos'))
        #self.assertEqual(lookup._simple_match('pater'))
        #self.assertEqual(lookup._simple_match('patros'))
        #self.assertEqual(lookup._simple_match('manus'))
        #self.assertEqual(lookup._simple_match('passus'))
        #self.assertEqual(lookup._simple_match('genu'))
        #self.assertEqual(lookup._simple_match('genus'))
        #self.assertEqual(lookup._simple_match('cornu'))
        #self.assertEqual(lookup._simple_match('cornus'))
        #self.assertEqual(lookup._simple_match('dies'))
        #self.assertEqual(lookup._simple_match('diei'))
        #self.assertEqual(lookup._simple_match('res'))
        #self.assertEqual(lookup._simple_match('rei'))
        #self.assertEqual(lookup._simple_match('fas'))

    def test__remove_enclitics(self):
        pass

    def test_match_word(self):
        pass

    def test_get_dictionary_string(self):
        pass


if __name__ == '__main__':
    unittest.main()

    #filt = MatchFilter(substantives=True)

    ## superlative adjective
    #words.lookup_word('maximum')
    #words.lookup_word('prior')
    #words.lookup_word('unus')
    ##words.lookup_word('vnvs')
    #words.lookup_word('paret')
    #words.lookup_word('imperat')
    #words.lookup_word('sumit')
    #words.lookup_inflections('maximum')
    #words.lookup_inflections('prior')
    #words.lookup_inflections('unus')
    #print("Should be the same:")
    #words.lookup_inflections('vnvs')
    #print("Moving on..")
    #words.lookup_inflections('paret')
    #words.lookup_inflections('imperat')
    #words.lookup_inflections('sumit')

    # Need to test a word from each declension-variant and conjugation-variant pair, and combinations
    # of e.g. comparison, verb type, etc, for all parts of speech
    # Need to test i/j and u/v interchanges

    # Whitaker provides a number of examples, see `docs/notes.txt`