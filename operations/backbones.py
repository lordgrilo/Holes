import networkx as nx

def Homological_persistence_backbone(G, gen_dict,k,W=0):
	'''
	Generates the homological backbone of dimension k 
	from the cycles in the given generator dict. 
	Input:
		G: original graph
		gen_dict: dictionary containing the full homology generators
		k: H_k to be used for the backbone
		W: optional normalization term for the cycle start and end terms. 

	Output: 
		E: k-th homological backbone of graph G.  

	'''
	import itertools;
	E=nx.Graph();
	E.add_nodes_from(G.nodes(data=True));
	if W==0:
		for cycle in gen_dict[0]:
			if float(cycle.end)>float(W):
				W=float(cycle.end);
	cycle_data=gen_dict[k];
	for cycle in cycle_data:
		for face in cycle.composition:
			for couple in itertools.combinations(face,2):
				if E.has_edge(couple[0],couple[1]):
					E[couple[0]][couple[1]]['weight']=E[couple[0]][couple[1]]['weight']+float(cycle.persistence_interval())/float(W);
				else:
					E.add_edge(couple[0],couple[1],weight=(float(cycle.persistence_interval())/float(W)));
	return E;



def Homological_frequency_backbone(G, gen_dict,k,W=0):
	'''
	Generates the homological frequency backbone of dimension k 
	from the cycles in the given generator dict. 
	Input:
		G: original graph
		gen_dict: dictionary containing the full homology generators
		k: H_k to be used for the backbone
		W: optional normalization term for the cycle start and end terms. 

	Output: 
		E: k-th homological frequency backbone of graph G.  

	'''
	E=nx.Graph();
	E.add_nodes_from(G.nodes(data=True));
	
	import itertools 
	if W==0:
		for cycle in gen_dict[0]:
			if float(cycle.end)>float(W):
				W=float(cycle.end);
	gen_dict=gen_dict[k];
	for cycle in gen_dict:
		for face in cycle.composition:
			for couple in itertools.combinations(face,2):
				if E.has_edge(couple[0],couple[1]):
					E[couple[0]][couple[1]]['weight']+=1;
				else:
					E.add_edge(couple[0],couple[1],weight=1);
	return E;

