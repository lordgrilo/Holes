import networkx as nx 
import numpy as np
import Holes as ho

def weight_label_generators(gen_dict,G):
	weighted_generators={};

	for key in gen_dict:
		weighted_generators[key]=[];

	edge_weights=nx.get_edge_attributes(G,'weight').values();
	edge_weights=list(set(edge_weights));
	edge_weights=sorted(edge_weights, reverse=True);

	max_weight=edge_weights[0];

	for key in gen_dict:
		for rank_cycle in gen_dict[key]:
			b=int(float(rank_cycle.start));
			d=int(float(rank_cycle.end));
			comp=rank_cycle.composition;
			dim=rank_cycle.dim;
			#weighted_generators[key].append(ay.Cycle(dim,comp,max_weight-edge_weights[b],max_weight-edge_weights[d]));
			weighted_generators[key].append(ho.Cycle(dim,comp,edge_weights[b],edge_weights[d]));
	return weighted_generators;



