Here zeroTrace.c is the clear method of NIST 800-88 then purge.c is the purge method 


eff_purge and smart_purge are logically built by me to only perform operations on the selected chunks ; 


i.e --> 

*st-1 : takes a chunk (lock / unmount / (as discussed in the call))

*st-2 : then verifies for data recovery  ---> if it is possible performs purge 
                |
                |
                V
*st-3 : else skip that chunk and move to (st-1)


