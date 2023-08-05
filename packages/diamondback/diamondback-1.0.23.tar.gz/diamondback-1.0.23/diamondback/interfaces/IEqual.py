""" **Description**

        Equal interface.

    **Example**

        ::

            from diamondback.interfaces.IEqual import IEqual
            from diamondback.interfaces.IPhase import IPhase


            class Test( IEqual, IPhase ) :

                def __eq__( self, other ) :

                    return ( ( super( ).__eq__( other ) ) and ( numpy.isclose( self.phase, other.phase ) ) )

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-01-23.

    **Definition**

"""

class IEqual( object ) :

    """ Equal interface.
    """

    def __eq__( self, other ) :

        """ Evaluates equality condition.

            Arguments :

                other - Other object ( object ).

            Returns :

                equality - Equality condition ( bool ).
        """

        return ( ( isinstance( other, self.__class__ ) ) and ( ( id( self ) == id( other ) ) or ( super( ).__eq__( other ) ) ) )

    def __init__( self ) :

        """ Initializes an instance.
        """

        pass

    def __ne__( self, other ) :

        """ Evaluates inequality condition.

            Arguments :

                other - Other object ( object ).

            Returns :

                inequality - Inequality condition ( bool ).
        """

        return not ( self == other )
