'''
##################################################################################
# Functions for the handling of Perseus output  								 #
##################################################################################

For all informations on Perseus, please refer to Vidit Nanda's Perseus webpage: 
http://www.sas.upenn.edu/~vnanda/perseus/

If you use Perseus through Holes, please do cite:
Konstantin Mischaikow and Vidit Nanda. 
Morse Theory for Filtrations and Efficient Computation of Persistent Homology. 
Discrete & Computational Geometry, Volume 50, Issue 2, pp 330-353, September 2013.

'''

__author__ = """\n""".join(['Giovanni Petri (petri.giovanni@gmail.com)']);

import numpy as np;
from Holes import Cycle;
import sys;


def write_perseus_filtration(fil, output_file, verbose=False):
    '''
    Writes a Perseus-friendly file representing the given filtration.

    A non-uniform triangulation in Perseus can be represented as follows:
    
        1: this is the number of coordinates per vertex. 
        2 1 3 5 1: this is the 2D simplex with vertices 1, 3 and 5; the birth time is 1.
        3 1 2 4 6 2 this is the 3D simplex with vertices 1, 2, 4 and 6; the birth time 2.
        6 1 2 3 4 5 6 7 4: 6D simplex, vertices 1 through 7. 
        and so on.

    We use here natural numbers to label simplex vertices and integers for their appearance along 
    the filtration. 
    This function is currently designed to work with the output of one of the filtration functions 
    in this module. 
    Each entry in a filtration dict is of the form:
    "[u'v1', u'v2', u'v3', u'v4']": ['birth', 'weight']
    This will output for each line something of the form:
    dimesion_of_the_simplex v1 v2 v3 v4 birth 

    Input:

    fil: filtration dictionary
    output_file: name of output file

    Output: 
    guess..
    '''

    f = open(output_file,'w');
    f.write('1\n');

    for key in fil:
        k = eval(key);
        t = [];
        t.append(str(len(k)-1));
        t.extend(map(str,k));
        t.append(str(int(fil[key][0])+1)+'\n');
        if verbose==True:
            print t, ' '.join(t); 
        f.write(' '.join(t));
    f.close();
    return;



def perseus_intervals(betti_file,infinite_or_not=1):
    '''
    This is a brute Python translation of Vidit Nanda's original Matlab script.
    
    
    output_file: name of file containing the perseus output
    plot_type: 0 plots ALL intervals
               1 plots only intervals that die
    '''
    
    # extract birth and death indices
    ints = np.genfromtxt(betti_file);

    # extract indices of those intervals which die
    if infinite_or_not==False:
        ints = ints[deaths != -1];
    return ints;


def calculate_perseus_intervals(input_file, output_directory, tmp_output='raw_outputs/', perseus_path=None, mode='nmfsimtop', max_index=None, name_tag=None):
    '''
    This function takes a Perseus input file and outputs 
    the persistent Betti intervals.

    The output of Perseus takes the form of a series of output_*.txt files. 
    This function produces a generator file akin to the others produced by Holes 
    (.pck file, populated by Cycle class objects). 

    It returns the generator in the output_directory (usually, 'gen').

    '''
    import os;
    if not os.path.exists(output_directory):
        os.makedirs(output_directory);
    if not os.path.exists(output_directory+tmp_output): # might consider actually checking if it's there 
        os.makedirs(output_directory+tmp_output);       # and just removing it if it's there.

    # persisten homology calculation
    from subprocess import call;
    if perseus_path == None:
        diodir = os.path.dirname(Holes.__file__);
        if sys.platform == 'darwin':
            perseus_path = diodir + 'perseus_utils/bin/perseusMac '; 
        if sys.platform == 'linux2':
            perseus_path = diodir + 'perseus_utils/bin/perseusLin ';
        if sys.platform in ['win32', 'cygwin']:
            perseus_path = diodir + 'perseus_utils/bin/perseusWin.exe ';
        if perseus_path == None:
            print 'Unsupported operating system. Cannot calculate persistent homology with Perseus.'
            return;
    call([perseus_path, mode, input_file, output_directory+tmp_output+'output']);

    # generator dict creation
    gen = {};
    intervals =  {};
    import glob;
    l = glob.glob(output_directory+tmp_output+'output_*.txt');
    
    max_index_temp = -1;

    for d in range(len(l)-1):
        intervals[d] = np.genfromtxt(output_directory+tmp_output+'output_'+str(d)+'.txt');
        gen[d] = [];
        if max_index == None:
            max_index_temp = np.max([max_index_temp , np.max(intervals[d])]);

    if max_index == None:
        max_index = max_index_temp;

    for d in intervals.keys():
        intervals[d][intervals[d][:,1] == -1 ,1] = max_index;
        gen[d] = map(lambda x: Cycle(d,[],x[0],x[1]) , intervals[d]);
        #print d, gen[d];
    try:
        import cPickle as pk;
    except:
        import pickle as pk;

    if name_tag == None:
        outfile = open(output_directory+'/generators_' + str(len(l)-2) + '.pck','w');
        pk.dump(gen, outfile);
    else:
        outfile = open(output_directory+'/generators_' + name_tag + '_' + str(len(l)-2) + '.pck','w');
        pk.dump(gen, outfile);
    outfile.close();

    return

