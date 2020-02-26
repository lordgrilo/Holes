
"""
	Representation of cycles containing information about generators and persistence intervals.
"""
__all__=['Cycle']
import numpy as np

class Cycle(object):
	""" 
	Representation of cycles containing information about generators and persistence intervals.
	"""

	def __init__(self,dim,simplexes,start,end):
		self.start=start;
		self.end=end;
		self.composition=simplexes;
		self.dim=dim;	
	
	def persistence_interval(self):
		return float(self.end)-float(self.start);
	
	def summary(self):
		print('Homology group=',str(self.dim));
		print('Starting at '+str(self.start)+' and ending at '+str(self.end));
		print('Composed by:')
		for deh in self.composition:
			print(' '+str(deh) );
	
	def cycle_nodes(self):
		from sets import Set
		nodes=[];
		for el in self.composition:
			nodes.append(el[0]);
			nodes.append(el[1]);
		nodes=Set(nodes);
		return list(nodes);
