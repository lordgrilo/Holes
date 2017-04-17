import networkx as nx 
import numpy as np
import Holes as ho

def weight_label_generators(gen_dict,G,ascending=False):
	weighted_generators={};

	for key in gen_dict:
		weighted_generators[key]=[];

	edge_weights=nx.get_edge_attributes(G,'weight').values();
	edge_weights=list(set(edge_weights));

	if ascending==False:
		edge_weights=sorted(edge_weights, reverse=True);
		max_weight=edge_weights[0];
	else:
		edge_weights=sorted(edge_weights);
		max_weight=edge_weights[-1];

	for key in gen_dict:
		for rank_cycle in gen_dict[key]:
			b=int(float(rank_cycle.start));
			d=int(float(rank_cycle.end));
			comp=rank_cycle.composition;
			dim=rank_cycle.dim;
			if ascending==True:
				weighted_generators[key].append(ho.Cycle(dim,comp,edge_weights[b],edge_weights[d]));
			else: 
				weighted_generators[key].append(ho.Cycle(dim,comp,edge_weights[d],edge_weights[b]));

	return weighted_generators;

def running_betti_number(gen,dim,base_vector,invert=False):
    counts = np.zeros_like(base_vector);
    for g in gen[dim]:
        if invert==False:
            v = (base_vector>float(g.start)) & (base_vector<float(g.end));
        else:
            v = (base_vector<float(g.start)) & (base_vector>float(g.end));
        v = v.astype(int);
        counts+=v;
    return counts;
    



