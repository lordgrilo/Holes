'''
##################################################################################
# Visualization functions for the statistical properties of the cycle generators #
##################################################################################
'''

__author__ = """\n""".join(['Giovanni Petri (petri.giovanni@gmail.com)']);

import numpy as np 

def cycle_persistence_distribution(Gen_dict,W=None,tag=' ',nbins=100):
	import networkx as nx;
	import matplotlib.pyplot as plt
	persistence=[];
	if W==None:
		W=0;
		for cycle in Gen_dict:
			if float(cycle.end)>float(W):
				W=cycle.end;
	for cycle in Gen_dict:
		persistence.append(float(cycle.persistence_interval())/float(W));
	plt.figure();
	# the histogram of the data
	n, bins, patches = plt.hist(persistence, nbins, normed=True, facecolor='green', alpha=0.75)
	if tag!=' ':
		plt.savefig(tag+'_persistence_distribution.png');
	return n, bins

def cycle_length_distribution(Gen_dict,tag=' ',nbins=100):
	import networkx as nx;
	import matplotlib.pyplot as plt
	length_cycles=[];
	
	for cycle in Gen_dict:
		length_cycles.append(len(cycle.composition));
	plt.figure();
	n, bins, patches = plt.hist(length_cycles, nbins, normed=True, facecolor='green', alpha=0.75)
	if tag!=' ':
		plt.savefig(tag+'_cycle_length_distribution.png');
	return n, bins

def cycle_start_distribution(Gen_dict,W=None,tag=' ',nbins=100):
	import networkx as nx;
	import matplotlib.pyplot as plt
	start_cycles=[];
	if W==None:
		W=0;
		for cycle in Gen_dict:
			if float(cycle.end)>float(W):
				W=float(cycle.end);
	for cycle in Gen_dict:
		start_cycles.append(float(cycle.start)/float(W));
	plt.figure();
	n, bins, patches = plt.hist(start_cycles, nbins, normed=True, facecolor='green', alpha=0.75)
	if tag!=' ':
		plt.savefig(tag+'_cycle_start_distribution.png');
	return n, bins

def barcode_creator(cycles,W=None,sizea=10,sizeb=10,verbose=False):
	import matplotlib.pyplot as plt;
	import numpy as np
	if W==None:
		W=0;
		for cycle in cycles:
			if float(cycle.end)>float(W):
				W=float(cycle.end);
	if verbose==True:
		print 'Maximum W=',W;
	fig=plt.figure(figsize=(sizea,sizeb));
	L=len(cycles);
	factor=np.sqrt(L);
	for i,cycle in enumerate(cycles):
		plt.plot([float(cycle.start)/float(W),float(cycle.end)/float(W)],[factor*(L-i), factor*(L-i)],'o-');



def complete_persistence_diagram(gen_list,W=None,normalized=True,factor_l=20.0,factor_p=1.0,show=False):
	import matplotlib.pyplot as plt;
	b=[];
	d=[];
	l=[];
	p=[];
	if normalized==True:
		if W==None:
	 		W=0;
	 		for cycle in gen_list:
	 			if float(cycle.end)>W:
	 				W=float(cycle.end);

		for cycle in gen_list:
			b.append(float(cycle.start)/float(W));
			d.append(float(cycle.end)/float(W));
			if len(cycle.composition)>0:
				l.append(float(len(cycle.composition))*factor_l);
			else:
				l.append(4.0*factor_l);
			p.append(float(cycle.persistence_interval())/float(W)*factor_p);	
	else:
		for cycle in gen_list:
			b.append(float(cycle.start));
			d.append(float(cycle.end));
			if len(cycle.composition)>0:
				l.append(float(len(cycle.composition))*factor_l);
			else:
				l.append(4.0*factor_l);
			p.append(float(cycle.persistence_interval())*factor_p);	
	plt.scatter(b,d,l,p);
	plt.xlim(0,1.1*np.max([np.max(b),np.max(d)]));
	plt.ylim(0,1.1*np.max([np.max(b),np.max(d)]));
	plt.xlabel('Birth');
	plt.ylabel('Death');
	plt.colorbar();
	plt.tight_layout();
	if show==True:
		plt.show();
	return;


	
