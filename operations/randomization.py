
##################################################################################
# Graph randomization			 												 #	
##################################################################################

import networkx as nx 
import random as rn 
import time 
def weight_reshuffling(G,weight_tag='weight'):
	'''
	Input: 
		G: an undirected weighted network
		IR_weight_cutoff: threshold on the minimum weight to reach
	Output: 
		E: an undirected weighted graph with the same connectivity of G, but
		   reshuffled weights. 
	'''

	print('Begin creation of weight reshuffled graph...');
	weight_dictionary=nx.get_edge_attributes(G,'weight');
	weight_sequence=weight_dictionary.values();

	#preliminary scan of edge weights to define filtration steps
	print('Preliminary scan of edge weights to define filtration steps...');
	edge_weights=list(set(nx.get_edge_attributes(G,weight_tag).values()));
	edge_weights=sorted(edge_weights, reverse=True);    
	print('Preliminary scan and sorting completed.');
	E=nx.Graph();
	E.add_nodes_from(G.nodes(data=True));
	E.add_edges_from(G.edges());
	E.remove_edges_from(E.selfloop_edges());
	weight_sequence_temp=weight_sequence;
	rn.shuffle(weight_sequence_temp);

	print('Setting new weights.');

	for e in E.edges_iter():
	    E.edge[e[0]][e[1]]['weight']=weight_sequence_temp[0];
	    weight_sequence_temp=weight_sequence_temp[1:];
	    
	print('Weights setup completed.');
	return E

def randomized_graph(G,num_randomization=None):
	'''
	Input: 
		G: an undirected weighted network
		IR_weight_cutoff: threshold on the minimum weight to reach
	Output: 
		E: an undirected weighted graph with the same degree and weight
		   sequence of G.
	'''

	if num_randomization==None:
		num_randomization=G.number_of_edges();

	max_index=0;

	print('Begin creation corresponding configuration model...');
	weight_dictionary=nx.get_edge_attributes(G,'weight');
	weight_sequence=list(weight_dictionary.values());
	degree_sequence=list(nx.degree(G).values());

	#preliminary scan of edge weights to define filtration steps
	print('Preliminary scan of edge weights to define filtration steps...');
	edge_weights=[];
	edge_weights=list(set(nx.get_edge_attributes(G,'weight').values()));
	edge_weights=sorted(edge_weights, reverse=True);
	    
	print('Preliminary scan and sorting completed.')

	rn.seed(rn.randint(0,1000000)+time.time());
	E=nx.configuration_model(degree_sequence);
	E=nx.Graph(E);
	E.remove_edges_from(E.selfloop_edges())
	weight_sequence_temp=weight_sequence;
	rn.shuffle(weight_sequence_temp);

	print('Setting new weights.');

	for e in E.edges_iter():
	    E.edge[e[0]][e[1]]['weight']=weight_sequence_temp[0];
	    weight_sequence_temp=weight_sequence_temp[1:];

	print('Weights setup completed.');
	return E
