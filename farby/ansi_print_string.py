import sys

NL  = '\n'

SP  = ' ' 
SP3 = SP * 3
SP7 = SP * 7

module_this = sys.argv[ 0 ]

print '\033[33;1m' ,                                  # yellow
print '%s    %s '  % ( NL , module_this )
print
print SP7 , '\033[32;1mGreetings, huMon ....'         # green
print
print SP7 , SP3 , '\033[36;1m How are you ????'       # cyan
print '\033[0m'                                       # reset
