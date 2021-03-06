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

### Usage

The .txt files provided in the tests folder are examples of input files to pypph. 
The first line in the input file should be the number of nodes. In the following
lines, each row has three entries: the first two describe the edge, and the 
third entry is the corresponding edge weight.


### Output

The value of 10,000 just means "Infinity" - this should only appear in the
0-dimensional case. Infinitely long 0-dimensional bars represent connected 
components that live forever. 
