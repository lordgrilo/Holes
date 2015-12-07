# This is a Jython script calculated the persistent homology of a clique dictionary. 
# It has been developed to work with a weighted clique filtration, but it 
# can adapted to be used to any series of persistent homology dictionaries
#
# NOTE: THIS CODE RUNS IN JYTHON, NOT PYTHON!!! 

import pickle, sys, os 
from collections import defaultdict
import Holes 

def list2simplexes(list,dim):
	num=dim+1;
	simplexes=[];
	for i in xrange(0,len(list),num):
		simplexes.append(list[i:i+num]);
	return simplexes
			
prime=13;

if len(sys.argv)>=4:
	clique_dic_file=str(sys.argv[1]);
	dimension=int(sys.argv[2]);                                               
	dir=str(sys.argv[3]);
	stringie=str(sys.argv[4]);
	javaplex_path=str(sys.argv[5]);
else:
	print('This code needs as input:');
	print('1) full filtration file name');
	print('2) the maximum homology dimension to calculate');
	print('3) the directory name for output');
	print('4) the tag name for the output files');
	print('6) the full path to your javaplex directory');
	sys.exit();

print('Opening filtration file...');
file=open(clique_dic_file,'r');
Clique_dictionary=pickle.load(file);                                                                                        

## NOTE: you need to put here the path to the javaPlex distribution on your system
libs = [                                                                                                 
	 os.path.join(javaplex_path,'javaplex.jar')
 	]                    
print libs                                                  

for s in libs:                                                                                           
	sys.path.append(s)                                                                                      
print sys.path

import edu.stanford.math.plex4                                                                              
import edu.stanford.math.plex4.api
import edu.stanford.math.plex.Persistence
import edu.stanford.math.plex4.streams.derived.DualStream
import edu.stanford.math.plex4.api.Plex4;
import edu.stanford.math.plex4.homology.barcodes.BarcodeCollection;
from edu.stanford.math import *;
from edu.stanford.math.plex4.homology.barcodes import AnnotatedBarcodeCollection;
from edu.stanford.math.plex4.homology.chain_basis import Simplex;
from edu.stanford.math.plex4.homology.interfaces import AbstractPersistenceAlgorithm;
from edu.stanford.math.plex4.streams.derived import DualStream;
from edu.stanford.math.plex4.autogen.homology import IntAbsoluteHomology;
from edu.stanford.math.primitivelib.algebraic.impl import ModularIntField;
from edu.stanford.math.plex4.homology.chain_basis import SimplexComparator;
from java.util import *;
from java.lang import *;
from edu.stanford.math.plex4.streams.impl import ExplicitSimplexStream;
from edu.stanford.math.plex4 import *;
from edu.stanford.math.plex4.homology.interfaces import AbstractPersistenceBasisAlgorithm;


complex=edu.stanford.math.plex4.api.Plex4.createExplicitSimplexStream();
max_index=0;
print "Clique dictionary: parsing started.";
for key in Clique_dictionary:
	original_key=key;
	key=str(key);    
	key=key.strip('[]');
	key=key.split(', ');
	key_buona=[];
	for n in range(len(key)):
		key_buona.append(int(float(eval(key[n]))));
	if len(key_buona)==1:
		complex.addVertex(key_buona[0],0);
	else:	
		complex.addElement(key_buona, int(Clique_dictionary[original_key][0]));
		if int(Clique_dictionary[original_key][0])>max_index:
			max_index=int(Clique_dictionary[original_key][0]);

print "Parsing over. Closing now."
complex.finalizeStream();
print "Complex is valid? ", complex.validateVerbose();
print "Size of complex filtration:" , complex.getSize();
max_filtration_value=max_index;

print "Starting Cohomology calculation..."
annotated_coalgorithm = IntAbsoluteHomology(ModularIntField.getInstance(prime), Collections.reverseOrder(SimplexComparator.getInstance()), 0, dimension+1);
costream = DualStream(complex);
annotated_cointervals = annotated_coalgorithm.computeAnnotatedIntervals(costream);
print "Done!"
print "Results incoming:"
infinite_barcodes = annotated_cointervals.getInfiniteIntervals()
betti_numbers_string = infinite_barcodes.getBettiNumbers()
print 'The betti numbers are:', betti_numbers_string;
print 'while the annotated intervals are: \n', annotated_cointervals;

# Here we save the full generator dictionary and save the interval files in order to be
# able to reopen them later for other purposes, for example comparison of random and null 
# models.. 


gendir=dir+'gen'
if not os.path.exists(gendir):
    os.makedirs(gendir)

Generator_dictionary={};
import re
import string
for h in range(dimension+1):
	Generator_dictionary[h]=[];
	list_gen=list(annotated_cointervals.getGeneratorsAtDimension(h))
	list_intervals=list(annotated_cointervals.getIntervalsAtDimension(h))
	for n,key in enumerate(list_gen):
		test=str(list_intervals[n]).split(',');
		test[0]=test[0].strip(' [')
		test[1]=test[1].strip(' )')
		if test[1]=='infinity':
			test[1]=str(max_filtration_value);
		line=str(key);
		line = line.translate(string.maketrans('', ''), '-[]')
		line = re.sub('[,+ ]', ' ', line)
		line=line.split();
		tempcycle=Holes.Cycle(h,list2simplexes(line,h),test[0],test[1]);
		Generator_dictionary[h].append(tempcycle);
		del tempcycle;		
	for cycle in Generator_dictionary[h]:
		cycle.summary();

generator_dict_file=open(gendir+'generators_'+str(stringie)+'.pck','w');
pickle.dump(Generator_dictionary,generator_dict_file);
print 'Generator dictionary dumped to '+ gendir+'generators_'+str(stringie)+'.pck',
generator_dict_file.close();



	
	
