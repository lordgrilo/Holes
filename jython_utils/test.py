import sys
sys.path.append('./lib/javaplex.jar')
import edu.stanford.math.plex4.api.Plex4;
import edu.stanford.math.plex4.homology.barcodes.BarcodeCollection;
from edu.stanford.math import *;
from edu.stanford.math.plex4.homology.barcodes import AnnotatedBarcodeCollection;
from edu.stanford.math.plex4.homology.chain_basis import Simplex;
from edu.stanford.math.plex4.homology.interfaces import AbstractPersistenceAlgorithm;
from edu.stanford.math.plex4.streams.derived import DualStream;
from edu.stanford.math.plex4.autogen.homology import IntAbsoluteHomology;
from edu.stanford.math.plex4.autogen.homology import IntPersistentHomology;

from edu.stanford.math.primitivelib.algebraic.impl import ModularIntField;
from edu.stanford.math.plex4.homology.chain_basis import SimplexComparator;
from java.util import *;
from java.lang import *;
from edu.stanford.math.plex4.streams.impl import ExplicitSimplexStream;
from edu.stanford.math.plex4 import *;
from edu.stanford.math.plex4.homology.interfaces import AbstractPersistenceBasisAlgorithm;

prime=13;
max_hom = 1;
d=2
complex = edu.stanford.math.plex4.api.Plex4.createExplicitSimplexStream();
complex.addVertex(0,0)
complex.addVertex(1,0)
complex.addVertex(2,0)
complex.addElement([0,1],1)
complex.addElement([1,2],1)
complex.addElement([0,2],1)
complex.addElement([0,1,2],2)

print "Parsing over. Closing now."
complex.finalizeStream();
print "Complex is valid? ", complex.validateVerbose();
print "Size of complex filtration:" , complex.getSize();

pH=edu.stanford.math.plex4.api.Plex4.getModularSimplicialAlgorithm(2,2);
print "Starting pH calculation..."
complex_computation=pH.computeIntervals(complex);
print "Done!"
print "Results incoming:"
infinite_barcodes = complex_computation.getInfiniteIntervals()
annotated_intervals = pH.computeAnnotatedIntervals(complex);
betti_numbers_string = infinite_barcodes.getBettiNumbers()
print 'The betti numbers are:', betti_numbers_string;
print 'while the annotated intervals are: \n', annotated_intervals;

annotated_coalgorithm = IntAbsoluteHomology(ModularIntField.getInstance(prime), Collections.reverseOrder(SimplexComparator.getInstance()), 0, d+1);
#annotated_coalgorithm = IntPersistentHomology(ModularIntField.getInstance(prime), Collections.reverseOrder(SimplexComparator.getInstance()), 0, max_hom+1);

costream = DualStream(complex);
print "Parsing over. Closing now."
costream.finalizeStream();
#print "Complex is valid? ", costream.validate();
print "Size of complex filtration:" , costream.getSize();

annotated_cointervals = annotated_coalgorithm.computeAnnotatedIntervals(costream);
#pH=edu.stanford.math.plex4.api.Plex4.getModularSimplicialAlgorithm(dimension+1,2);
#annotated_cointervals = pH.computeAnnotatedIntervals(costream);
print "Cohomology basis for file:"
print annotated_cointervals;
