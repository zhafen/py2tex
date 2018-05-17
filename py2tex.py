#!/usr/bin/env python
'''Interface for saving data to TeX-readable files.

@author: Zach Hafen
@contact: zachary.h.hafen@gmail.com
@status: Development
'''

import numpy as np
import os
import warnings

import utilities

########################################################################
########################################################################


class TeXVariableFile( object ):
    '''Class for creating, adding to, and deleting a TeX file of variables with values.'''

    @utilities.store_parameters
    def __init__( self, filename ):
        '''Constructor.

        Args:
            filename (str) :
                Location of file.

        Returns:
            TeXVariableFile object.
        '''

        pass

    ########################################################################

    @property
    def data_dict( self ):
        '''Actual data stored in the file.'''

        if not hasattr( self, '_data_dict' ):

            try:
                # Read the file
                with open( self.filename, 'r' ) as f:
                    lines = f.readlines()
                # Parse
                self._data_dict = {}
                for line in lines:
                    name = line.split( '{' )[1].split( '\\' )[-1][:-1]
                    value = line[15+len(name):-2]

                    self._data_dict[name] = value

            except IOError:
                print( "No pre-existing file found. Writing will be done to a fresh file." )

                self._data_dict = {}
            
        return self._data_dict

    ########################################################################

    def write( self ):
        '''Write the stored data_dict to the file.'''

        lines = []

        for key, item in self.data_dict.items():

            line = '\\newcommand{\\' + key + '}{' + item + '}\n'

            lines.append( line )

        with open ( self.filename, 'w' ) as f:

            f.writelines( lines )

    ########################################################################

    def save_variable( self, key, item ):
        '''Save a variable to the TeX file.

        Args:
            key (str) :
                Name to store the variable as. Do not use numbers in the name!
                LaTeX does not work well with numbers in command names.

            item (str) :
                What the value to store to the variable, pre-formatted as a
                string.

        Modifies:
            self.data_dict :
                Stores the variable in this dictionary, and writes to the file.
        '''

        print( "Saving {} as {}".format( item, key ) )

        # Warn when overwriting.
        if key in self.data_dict.keys():
            if self.data_dict[key] != item:
                warnings.warn(
                    "Overwriting variable {}. New value {}, previous value {}".format(
                        key,
                        item,
                        self.data_dict[key],
                    )
                )

        self.data_dict[key] = item

        self.write()

    ########################################################################

    def delete_variable( self, key ):
        '''Delete a variable in the tex file.

        Args:
            key (str) :
                Delete the variable with this name from the tex file.

        Modifies:
            self.data_dict :
                Removes the variable from this dictionary, and writes to the
                file.
        '''

        print( "Deleting {}".format( key ) )

        del self.data_dict[key]

        self.write()


########################################################################
########################################################################

def to_tex_scientific_notation( value, sig_figs=2 ):
    '''Convert a float value to scientific notation, as would be displayed
    in TeX.

    Args:
        value (float) :
            Value to convert.

        sig_figs (int) :
            Number of significant figures to use.
            An astrophysicist wrote this code, so the default number of sig
            figs is 2 :) (1 would also be a good option...)

    Returns:
        formatted_value (str) :
            The specified value in scientific notation.

    Examples:
        >>> to_tex_scientific_notation( 1.2345e7, 2 )
        '1.2x10^{7}'
        >>> to_tex_scientific_notation( 321.5, 1 )
        '3x10^{2}'
        >>> to_tex_scientific_notation( 1.2345e7, 1 )
        '10^{7}'
    '''

    exponent, digits = str( np.log10( value ) ).split( '.' )

    formatted_exponent = '{' + exponent + '}'

    digits_value = 10.**float( '.{}'.format( digits ) )
    format_string = '{:.0' + str( sig_figs - 1 ) + 'f}'
    formatted_digits = format_string.format( digits_value )

    formatted_value = '{}\\times10^{}'.format( formatted_digits, formatted_exponent )

    # Check for a special case
    if formatted_value[:7] == '1\\times':
        return formatted_value[7:]

    return formatted_value

