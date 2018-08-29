# pypph
Chowdhury, S. and Mémoli, F., Persistent Path Homology of Directed Networks. SODA 2018.

This is a Python 2.7 implementation of the Persistent Path Homology (PPH) package described in the aforementioned paper. 

To test that the code is running properly, type in the following from the command line:

  python pph.py tests\cycleNet11.txt

The output should look like:

['pph.py', 'tests\\cycleNet11.txt']
('pers bars are', [['0-dim bars are ', [(0.0, 1.0), (0.0, 1.0), (0.0, 1.0), (0.0, 1.0), (0.0, 1.0), (0.0, 1.0), (0.0, 1.0), (0.0, 1.0), (0.0, 1.0), (0.0, 1.0), (0.0, 10000.0)]], ['1-dim bars are ', [(1.0, 6.0)]]])



The tests folder contains code for generating cycle networks on n nodes. To run, type the following in from the command line:

  python cycleNet.py n
  
Here n is the number of nodes. E.g.
  
  python cycleNet.py 11
