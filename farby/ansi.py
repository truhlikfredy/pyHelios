
'''
     Module ....... ansi.py 

     Purpose ...... Demonstrate Ansi Escape Sequence Display

     Requires ..... ANSI.SYS Driver 

                    Add the following line to CONFIG.SYS
                    using the correct path on  YOUR  system ...

                        DEVICE=C:\WINDOWS\COMMAND\ANSI.SYS 

     NewsGroup .... comp.lang.python

     Date ......... 2002-08-23

     Posted_By .... Denis S. Otkidach

     Edited_By .... Stanley C. Kitching

'''

import sys

print '\n   ' , sys.argv[ 0 ] , '\n'


def colored( xStr , *opts ) :

    seq = {
           'clear'      : '0' ,
           'reset'      : '0' ,
           'bold'       : '1' ,
           'underline'  : '4' ,
           'underscore' : '4' ,
           'blink'      : '5' ,
           'reverse'    : '7' ,
           'concealed'  : '8' ,

           'black'      : '30' , 'on_black'   : '40' ,
           'red'        : '31' , 'on_red'     : '41' ,
           'green'      : '32' , 'on_green'   : '42' ,
           'yellow'     : '33' , 'on_yellow'  : '43' ,
           'blue'       : '34' , 'on_blue'    : '44' ,
           'magenta'    : '35' , 'on_magenta' : '45' ,
           'cyan'       : '36' , 'on_cyan'    : '46' ,
           'white'      : '37' , 'on_white'   : '47' }


    esc = '\x1b['
    sep = ';'
    end = 'm'

    if len( opts ) :

        seqs = []

        for opt in opts :

            seqs.append( seq[ opt ] )

        ae_Seq = esc + sep.join( seqs ) + end + xStr + esc + seq[ 'reset' ] + end

        return ae_Seq

    else :

        return xStr


def xMain() : 

    SP8 = '\x1b[8C'  # Move Right 8 spaces

    list_colors = [ 'red' ,     'green' , 'yellow' , 'blue' , 
                    'magenta' , 'cyan'  , 'white' ]


    for color_x in list_colors : 

        print SP8 , colored( ' ' + color_x , 'bold' , color_x , 'on_black' ) 


    print
   
    for color_x in list_colors : 

        str_Out  = '%-20s' % ( ' white  on  ' + color_x )

        color_bg = 'on_' + color_x

        print SP8 , colored( str_Out , 'bold' , 'white' ,  color_bg ) 

    
    str_Out  = '%-20s' % ( ' yellow on blue ' )

    print
    print SP8 , colored( str_Out , 'bold' , 'yellow' , 'on_blue' )


if __name__ == '__main__' :
   
   xMain()

