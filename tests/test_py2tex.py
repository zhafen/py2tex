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

    def setUp( self ):

        self.tex_vfile = py2tex.TeXVariableFile( filename )

    ########################################################################
    
    def test_data_dict( self ):

        expected = {
            'a' : '1',
            'b' : '-100',
        }

        actual = self.tex_vfile.data_dict

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

        expected = r'1.2x10^{8}'

        actual = py2tex.to_tex_scientific_notation( value, 2 )

        self.assertEqual( expected, actual )

    ########################################################################

    def test_to_tex_scientific_notation_special_case( self ):
        '''When we would produce '1x10^{X}', instead return just '10^{X}'
        '''

        value = 12.3456e7

        expected = r'10^{8}'

        actual = py2tex.to_tex_scientific_notation( value, 1 )

        self.assertEqual( expected, actual )
