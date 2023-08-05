""" **Description**

        Resolution interface.

    **Example**

        ::

            from diamondback.interfaces.IResolution import IResolution


            class Test( IResolution ) :

                def __init__( self ) :

                    super( ).__init__( )

                    self.resolution = 0.5

            test = Test( )

            test.resolution = 0.1

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-07-12.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual
import numpy


class IResolution( IEqual ) :

    """ Resolution interface.
    """

    @property
    def resolution( self ) :

        """ Resolution ( float ).
        """

        return self._resolution

    @resolution.setter
    def resolution( self, resolution ) :

        if ( resolution <= 0.0 ) :

            raise ValueError( 'Resolution = ' + str( resolution ) )

        self._resolution = resolution

    def __eq__( self, other ) :

        """ Evaluates equality condition.

            Arguments :

                other - Other object ( object ).

            Returns :

                equality - Equality condition ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( numpy.isclose( self.resolution, other.resolution ) ) )

    def __init__( self ) :

        """ Initializes an instance.
        """

        super( ).__init__( )

        self._resolution = 1.0
