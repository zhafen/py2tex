'''Testing for data_management.py
'''

import os
import unittest

import py2tex

########################################################################

filename = './tests/data/analysis_output.tex'

########################################################################
########################################################################

class TestReadTeXVariableFile( unittest.TestCase ):

    def test_data_dict( self ):

        tex_vfile = py2tex.TeXVariableFile( filename )

        expected = {
            'a' : '1',
            'b' : '-100',
        }

        actual = tex_vfile.data_dict

        self.assertEqual( expected, actual )

    ########################################################################

    def test_file_contains_scientific_notation( self ):

        tex_vfile = py2tex.TeXVariableFile(
            './tests/data/analysis_output2.tex'
        )

        expected = {
            'a' : '1',
            'b' : '-100',
            'c' : r'5.23\times10^{10}',
        }

        actual = tex_vfile.data_dict

        self.assertEqual( expected, actual )

########################################################################
########################################################################


class TestTeXVariableFileReset( unittest.TestCase ):

    def setUp( self ):

        self.tex_vfile = py2tex.TeXVariableFile( filename )

    def tearDown( self ):

        if os.path.isfile( filename ):
            os.remove( filename )

        with open( filename, 'w' ) as f:
            f.write( '\\newcommand{\\a}{1}\n\\newcommand{\\b}{-100}\n' )

    ########################################################################

    def test_data_dict_no_file( self ):

        os.remove( filename )

        expected = {}

        actual = self.tex_vfile.data_dict

        self.assertEqual( expected, actual )

    ########################################################################

    def test_write_data( self ):

        self.tex_vfile._data_dict = {
            'a' : '3',
            'b' : '2',
            'c' : '1',
        }

        self.tex_vfile.write()

        with open( filename, 'r' ) as f:
            actual = f.read()

        # Try two different orderings for the file (depends on python version)
        try:
            expected  = '\\newcommand{\\a}{3}\n\\newcommand{\\c}{1}\n\\newcommand{\\b}{2}\n'
            self.assertEqual( expected, actual )
        except:
            expected  = '\\newcommand{\\a}{3}\n\\newcommand{\\b}{2}\n\\newcommand{\\c}{1}\n'
            self.assertEqual( expected, actual )

    ########################################################################

    def test_save_variable( self ):

        self.tex_vfile.save_variable( 'c', '9000' )

        with open( filename, 'r' ) as f:
            actual = f.read()

        try:
            expected  = '\\newcommand{\\a}{1}\n\\newcommand{\\c}{9000}\n\\newcommand{\\b}{-100}\n'
            self.assertEqual( expected, actual )
        except:
            expected  = '\\newcommand{\\a}{1}\n\\newcommand{\\b}{-100}\n\\newcommand{\\c}{9000}\n'
            self.assertEqual( expected, actual )

        
########################################################################
########################################################################

class TestHelperFunctions( unittest.TestCase ):

    def test_to_tex_scientific_notation( self ):

        value = 12.3456e7

        expected = r'1.2\times10^{8}'

        actual = py2tex.to_tex_scientific_notation( value, 2 )

        self.assertEqual( expected, actual )

    ########################################################################

    def test_to_tex_scientific_notation_special_case( self ):
        '''When we would produce '1\\times10^{X}',
        instead return just '10^{X}'
        '''

        value = 12.3456e7

        expected = r'10^{8}'

        actual = py2tex.to_tex_scientific_notation( value, 1 )

        self.assertEqual( expected, actual )

    ########################################################################

    def test_to_tex_scientific_notation_special_case_two( self ):
        '''When we would produce 'X\\times10^{0]'
        instead return just X
        '''

        value = 3.45

        expected = r'3'

        actual = py2tex.to_tex_scientific_notation( value, 1 )

        self.assertEqual( expected, actual )

    ########################################################################

    def test_to_tex_scientific_notation_neg_one_to_zero( self ):
        '''Test that when we provide a value between 0.1 and 1 things work
        still
        '''

        value = 0.12

        expected = r'1.2\times10^{-1}'

        actual = py2tex.to_tex_scientific_notation( value, 2 )

        self.assertEqual( expected, actual )

    ########################################################################

    def test_to_tex_scientific_notation_small_fraction( self ):
        '''Test that when we provide a value between 0.1 and 1 things work
        still
        '''

        value = 0.0067

        expected = r'7\times10^{-3}'

        actual = py2tex.to_tex_scientific_notation( value, 1 )

        self.assertEqual( expected, actual )

    ########################################################################

    def test_to_tex_scientific_notation_no_digits( self ):
        '''When we would produce '9\\times10^{X}',
        instead return just '10^{X+1}', when sig_figs==0
        '''

        value = 5.5e70

        expected = r'10^{71}'

        actual = py2tex.to_tex_scientific_notation( value, 0 )

        self.assertEqual( expected, actual )

########################################################################

class TestToTeXPercentage( unittest.TestCase ):

    def test_to_tex_precentage( self ):

        value = 0.573

        expected = r'60\%'

        actual = py2tex.to_tex_percentage( value, 0 )

        self.assertEqual( expected, actual )
    
    ########################################################################

    def test_to_tex_precentage( self ):

        value = 0.573

        expected = r'57\%'

        actual = py2tex.to_tex_percentage( value, 1 )

        self.assertEqual( expected, actual )
    
