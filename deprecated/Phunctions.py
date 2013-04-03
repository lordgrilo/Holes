'''
Persistence homology class 
'''
import numpy as np
import networkx as nx
import Phom
import pylab 
try:
	import cpickle as pickle
except:
	import pickle

# 
# 
# class Cycle:
# 	"""Representation of cycles containing information about generators and persistence intervals."""
# 	def __init__(self,dim,simplexes,start,end):
# 		self.start=start;
# 		self.end=end;
# 		self.composition=simplexes;
# 		self.dim=dim;	
# 	def persistence_interval(self):
# 		return float(self.end)-float(self.start);
# 	def summary(self):
# 		print 'Homology group=',str(self.dim);
# 		print 'Starting at '+str(self.start)+' and ending at '+str(self.end) ;
# 		print 'Composed by:'
# 		for deh in self.composition:
# 			print(' '+str(deh) );
# 	def cycle_nodes(self):
# 		from sets import Set
# 		nodes=[];
# 		for el in self.composition:
# 			nodes.append(el[0]);
# 			nodes.append(el[1]);
# 		nodes=Set(nodes);
# 		return list(nodes);
# 		
# def Add_H_1_generator(G, C, w=80, cycle_id=0):
# 	import networkx;
# 	for el in C.composition:
# 		G.add_edge(el[0],el[1], weight=w, cycle=cycle_id);
# 
# 
# def Add_significant_H_1_generators(G, H_1_gen_list, thr=1, tag_cycles=True):
# 	if tag_cycles==True:
# 		for i, cycle in enumerate(H_1_gen_list):
# 			if cycle.persistence_interval()>thr:
# 				Add_H_1_generator(G,cycle,cycle.persistence_interval(),i);
# 	else:
# 		for i, cycle in enumerate(H_1_gen_list):
# 			if cycle.persistence_interval()>thr:
# 				Add_H_1_generator(G,cycle,cycle.persistence_interval(),0);
# 
# def Add_early_significant_H_1_generators(G, H_1_gen_list, earlyness, thr=1, tag_cycles=True):
# 	if tag_cycles==True:
# 		for i, cycle in enumerate(H_1_gen_list):
# 			if cycle.persistence_interval()>thr and float(cycle.start)<earlyness:
# 				Add_H_1_generator(G,cycle,cycle.persistence_interval(),i);
# 	else:
# 		for i, cycle in enumerate(H_1_gen_list):
# 			if cycle.persistence_interval()>thr and float(cycle.start)<earlyness:
# 				Add_H_1_generator(G,cycle,cycle.persistence_interval(),0);
# 
# 
# def print_node_labels_H_1(G, H_1_gen,label_dictionary):	
# 	for cycle in H_1_gen:
# 			print cycle.persistence_interval();
# 			for el in cycle.composition:
# 				print label_dictionary[el[0]], label_dictionary[el[1]]
# 			print '-----------'
# 		
# 
# def print_node_labels_H_1(G, H_2_gen,label_dictionary):	
# 	for cycle in H_2_gen:
# 			print cycle.persistence_interval();
# 			for el in cycle.composition:
# 				print label_dictionary[el[0]], label_dictionary[el[1]], label_dictionary[el[2]]
# 			print '-----------'
# 
# 
# def create_significant_loops_graph(G, H_1_gen_list, thr=1, tag_cycles=True):
# 	G1=nx.Graph();
# 	G1.add_nodes_from(G.nodes(data=True));
# 	G1.Add_significant_H1_generators(G,H_1_gen_list, thr, tag_cycles);
# 	return G1;
# 	
# 	
# def cycle_community_connectivity(G,cycle_dictionary,partition):
# 	'''
# 	Returns a dictionary containing the number of communities
# 	each cycle crosses. 
# 	'''	
# 	from sets import Set
# 	nodes=Set()
# 	for cycle in cycle_dictionary:
# 		for el in cycle_composition:
# 			nodes.add(el[0]);
# 			nodes.add(el[1]);
# 	nodes=Set(nodes);
	

def node_cycle_simple_partecipation(G,H_1_dict,add_attrs=True):
	import networkx as nx
	partecipation={}
	for n in G.nodes():
		partecipation[n]=[];
		partecipation[n]=0;
	for cycle in H_1_dict:
		for el in cycle.composition:
			partecipation[el]=partecipation[el]+1;
	if add_attrs==True:
		nx.set_node_attributes(G,'simple_cycle_partecipation',partecipation);
	return partecipation;
		
def node_cycle_simple_persistence_partecipation(G,H_1_dict, add_attrs=True):
	import networkx as nx
	partecipation={}
	for n in G.nodes():
		partecipation[n]=[];
		partecipation[n]=0;
	for cycle in H_1_dict:
		for el in cycle.composition:
			partecipation[el]=partecipation[el]+cycle.persistence_interval();
	if add_attrs==True:
		nx.set_node_attributes(G,'simple_cycle_persistence_partecipation',partecipation);

	return partecipation;
			 
def node_cycle_average_persistence_partecipation(G,H_1_dict,tag='',add_attrs=True):
	import networkx as nx
	from sets import Set
	partecipation={}
	for n in G.nodes():
		partecipation[n]=[];
		partecipation[n].append(0);
		partecipation[n].append(0);
	print len(partecipation);
	for cycle in H_1_dict:
		nodes=[]
		for el in cycle.composition:
			print el[0], el[1]
			nodes.append(float(el[0]));
			nodes.append(float(el[1]));
		nodes=set(nodes);
		for e in nodes:
			if e in partecipation:
				partecipation[e][0]=partecipation[e][0]+cycle.persistence_interval();
				partecipation[e][1]=partecipation[e][1]+1;
# 			else:
# 				partecipation[e]=[];
# 				partecipation[e].append(cycle.persistence_interval());
# 				partecipation[e].append(1);
	results={}		
	for n in partecipation:
		results[n]=[];
		if partecipation[n][1]!=0:
			results[float(n)]=partecipation[n][0]/partecipation[n][1];
		else:
			results[n]=0;
	if add_attrs==True:
		nx.set_node_attributes(G,'av_cycle_persistence_partecipation'+tag,results);
	return results;

def print_cycles_layout(G,pos,cycle,dir,tag,id=0,quantity='modularity_networkx'):
	import matplotlib.pyplot as plt
	import matplotlib as mt
	import numpy as np
	import networkx as nx
	plt.figure()
	pp=mt.backends.backend_pdf.PdfPages(dir+'/'+tag+'_cycle_'+str(id)+'.pdf');
	cycle_graph=nx.Graph();
	cycle_graph.add_nodes_from(G.nodes(data=True));
	Phom.Add_H_1_generator(cycle_graph, cycle, cycle.persistence_interval(), id);
	nx.draw_networkx_edges(cycle_graph,pos,width=5,alpha=1, edge_color='r')
	nx.draw_networkx_nodes(cycle_graph,pos,node_color=nx.get_node_attributes(cycle_graph,quantity).values(),alpha=0.5, node_size=5)
	plt.title(tag+' cycle '+str(id)+'start '+str(cycle.start)+' persistence '+str(cycle.persistence_interval()));
	plt.savefig(pp, format='pdf');#ag+'_cycle_'+str(id)+'.png');
	pp.close();

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


def barcode_creator(cycles,W=None,size=10):
	import matplotlib.pyplot as plt;
	import numpy as np
	if W==None:
		W=0;
		for cycle in cycles:
			if float(cycle.end)>float(W):
				W=float(cycle.end);
	fig=plt.figure(figsize=(size,size));
	L=len(cycles);
	factor=np.sqrt(L);
	for i,cycle in enumerate(cycles):
		plt.plot([float(cycle.start)/float(W),float(cycle.end)/float(W)],[factor*(L-i), factor*(L-i)],'o-');
   


def cycle_community_spread(partition,cycle_dict):
	'''
	
	'''
	from sets import Set
	cycle_spread=[];
	for cycle in cycle_dict:
		list_comms=[];
		for el in cycle.composition:
			for i in range(len(el)):
				if partition.has_key(el[i]):
					list_comms.append(partition[el[i]]);
				else: 
					print 'not in partition:',el[i], type(el[i])

		cycle_spread.append(len(Set(list_comms)));
	#print cycle_spread
	return cycle_spread;
	
			
def create_flow_graph(G,gamma,weight_string='weight'):
	'''
	Creates the flow graph corresponding to a generalized random
	walk process on biased with s_i^\gamma. 
	
	Ref. Lambiotte, R., Sinatra, R., Delvenne, J. C., Evans, T., Barahona, M., & Latora, V. (2011).
	 Flow graphs: Interweaving dynamics and structure. 
	 Physical Review E, 84(1). doi:10.1103/PhysRevE.84.017102
	'''
	F=nx.DiGraph();
	F.add_nodes_from(G.nodes(data=True));
	strengths=G.degree(weight=weight_string);
	for edge in G.edges(data=True):
		F.add_edge(edge[0],edge[1],weight=edge[2][weight_string]*float(strengths[edge[0]]**gamma)*float(strengths[edge[1]]**gamma));
		F.add_edge(edge[0],edge[1],weight=edge[2][weight_string]*float(strengths[edge[0]]**gamma)*(strengths[edge[1]]**gamma));
	
	return F;


def strength_preserving_reshuffling(G,weight_name='weight'):
	import random;
	E=G.to_directed();

	for n in E.nodes():
		nn=E.neighbors(n);
		weight_set=[];
		for v in nn:
			weight_set.append(E[n][v][weight_name]);
		random.shuffle(weight_set);
		for i,v in enumerate(nn):
			F.add_edge(n,v,weight=weight_set[i]);
	return E;
	
	
def inverse_weight_shortest_path(G,weight_name='weight',dir='./',filename=' '):
	if G.is_directed():
		T=nx.DiGraph();
	else: 
		T=nx.Graph();
	T.add_nodes_from(G.nodes(data=True));	
	T.add_edges_from(G.edges());
	for e in G.edges(data=True):
		T[e[0]][e[1]][weight_name]=float(1/float(G[e[0]][e[1]][weight_name]));
	
	distances=nx.floyd_warshall(T, weight=weight_name);
	
	if filename!=' ':
		nx.write_gexf(T,dir+filename.split('.')[-2]+'_inverse_edge_weight.gexf');
		pickle.dump(distances,open(dir+filename+'_inverse_weight_shortest_path.pck','w'));
		print 'Distance file saved to '+dir+filename+'_inverse_weight_shortest_path.pck'
	return distances;

def inverse_weight_graph(G,weight_name='weight'):
	if G.is_directed():
		T=nx.DiGraph();
	else: 
		T=nx.Graph();
	T.add_nodes_from(G.nodes(data=True));	
	T.add_edges_from(G.edges());
	for e in G.edges(data=True):
		T[e[0]][e[1]][weight_name]=float(1/float(G[e[0]][e[1]][weight_name]));
	return T;
	
def maximum_spanning_graph(G,weight_name='weight'):
	if G.is_directed():
		T=nx.DiGraph();
	else: 
		T=nx.Graph();

	T.add_nodes_from(G.nodes(data=True));
	tree=T.copy();
	for e in G.edges(data=True):
		T.add_edge(e[0],e[1],weight=-e[2][weight_name]);
	
	negative_tree=nx.minimum_spanning_tree(T,weight_name);		

	for e in negative_tree.edges(data=True):
		tree.add_edge(e[0],e[1],weight=-e[2][weight_name]);
	return tree;



def global_network_efficiency(G,distances):
	Relabel=dict.fromkeys(G.nodes());
	for i,n in enumerate(G.nodes()):
		Relabel[n]=i;
	T=nx.relabel_nodes(G,Relabel);
	n=len(distances);
	E=float(0)
	E_norm=float(0);
	for i in range(len(distances)):
		for j in range(len(distances[i])):
			if i!=j:
				if distances[i][j]!=0:
					if T.has_edge(i,j):
						E+=float(1/distances[i][j]);
					E_norm+=float(1/distances[i][j]);
	E=E/(n*(n-1));
	E_norm=E_norm/(n*(n-1));
	return E/E_norm;
			
def local_network_efficiency(G,distances):

	N=float(G.number_of_nodes());
#	print N
	E=float(0);
	for n in G.nodes():
		E_single=float(0);
		E_single_norm=float(0);
		neigh=G.neighbors(n);
		neigh.append(n);
		sub=nx.Graph(G.subgraph(neigh));
		for s in sub.nodes():
			for t in sub.nodes():
				if s!=t:
					if sub.has_edge(s,t):
						E_single+=float(1/float(distances[s][t]));
					E_single_norm+=float(1/float(distances[s][t]));
		E+=E_single/E_single_norm;
	E=E/N;
	return E;
			
def cycle_nodes(cycle):
	from sets import Set
	nodes=[];
	for el in cycle.composition:
		for e in el:
			nodes.append(e);
##		nodes.append(el[1]);
	nodes=Set(nodes);
	return list(nodes);

def global_cycle_efficiency(G,cycle,distances):
	Relabel=dict.fromkeys(G.nodes());
	for i,n in enumerate(G.nodes()):
		Relabel[n]=i;
	sub_nodes=cycle_nodes(cycle);
	R=G.subgraph(sub_nodes);
	sub_relabel=nx.relabel_nodes(R,Relabel);
	return global_network_efficiency(sub_relabel,distances);
	
def cycle_H_1_efficiency(cycle,distances):
	G=nx.Graph();
	for el in cycle.composition:
		G.add_edge(el[0],el[1]);
	return float(local_network_efficiency(G,distances));
	

def local_cycle_efficiency(G,cycle,distances):
	from sets import Set;
	sub_nodes=cycle_nodes(cycle);
	extra_nodes=[];
	for n in sub_nodes:
		extra_nodes.extend(G.neighbors(n));
	sub_nodes.extend(extra_nodes);
	sub_nodes=list(Set(sub_nodes));
	R=G.subgraph(sub_nodes);
	return R.number_of_nodes(), float(local_network_efficiency(R,distances));
	
def local_cycle_restricted_efficiency(G,cycle,distances):
	sub_nodes=cycle_nodes(cycle);
	R=G.subgraph(sub_nodes);
	return float(local_network_efficiency(R,distances));

	
def weight_preserving_configuration_model(G,filename=' '):
	import random as rn
	import time
	weight_dictionary=nx.get_edge_attributes(G,'weight');
	weight_sequence=weight_dictionary.values();
	degree_sequence=list(nx.degree(G).values());

	rn.seed(rn.randint(0,1000000)+time.time());
	E=nx.configuration_model(degree_sequence);
	E=nx.Graph(E);
	E.remove_edges_from(E.selfloop_edges());
	weight_sequence_temp=weight_sequence;
	for t in range(100):
		rn.shuffle(weight_sequence_temp);
		
	for e in E.edges_iter():
		E.edge[e[0]][e[1]]['weight']=weight_sequence_temp[0];
		weight_sequence_temp=weight_sequence_temp[1:];
	
	if filename!=' ':
		nx.write_weighted_edgelist(E, filename , delimiter=' ', encoding='utf-8')
		print('Randomized edgelist dumped to '+ filename);
	
	return E;
	
def clique_efficiency(G,distances):
	cliques=nx.find_cliques(G);
	for e in cliques:
		print len(e), local_cycle_restricted_efficiency(G,cycle,distances);
		

def fundamental_cycles_analysis(G,gen_dict,tree):
	E=dict.fromkeys(tree.edges());
	


def strength_rich_club_coefficient(G,ranking,thr,weight_name='weight',normalized=False):
	'''
	Calculates the members of the rich club given the ranking
	and the coefficient, normalized on the randomized version of the 
	network
	
	This does not work in general, needs to be improved
	Works now only for strength preserving randomization and strength ranking 
	'''
	from sets import Set
	club_nodes=[];
	for n in G.nodes():
		if ranking[n]>=thr:
			club_nodes.append(n);
	
	Club=nx.Graph(G.subgraph(club_nodes));
	W_club=float(np.sum(nx.get_edge_attributes(Club,weight_name).values()));
#	print Club.number_of_nodes()
	Extended_club=nx.Graph();
	for n in Club.nodes():
		Extended_club.add_node(n);
		for nn in G.neighbors(n):
			Extended_club.add_edge(n,nn,weight=G[n][nn][weight_name]);

	print Extended_club.number_of_nodes()
	W_ext=float(np.sum(nx.get_edge_attributes(Extended_club,weight_name).values()));
	
	if normalized==True:
		RandomGraph=Phom.strength_preserving_reshuffling(G,weight_name).to_undirected();
		club_nodes=[];
		for n in RandomGraph.nodes():
			if ranking[n]>=thr:
				club_nodes.append(n);
		
		Club=nx.Graph(RandomGraph.subgraph(club_nodes));
		W_club_r=float(np.sum(nx.get_edge_attributes(Club,weight_name).values()));
#		print Club.number_of_nodes()
		Extended_club=nx.Graph();
		for n in Club.nodes():
			Extended_club.add_node(n);
			for nn in RandomGraph.neighbors(n):
				Extended_club.add_edge(n,nn,weight=RandomGraph[n][nn][weight_name]);
	
		print Extended_club.number_of_edges()
		W_ext_r=float(np.sum(nx.get_edge_attributes(Extended_club,weight_name).values()));
		ranking_random=ranking;
		return (W_club/W_ext)/(W_club_r/W_ext_r);		
	else:
		return W_club/W_ext;
	
	

def network_hollowness(gen_dict,max_index):
	if len(gen_dict)>0:
		pc=0;
		for cycle in gen_dict:
			pc+=float(cycle.persistence_interval())/float(max_index);
		N=float(len(gen_dict));
	else:
		pc=0;
		N=1;
	return pc/N;
	

def network_weighted_hollowness(G,gen_dict,max_index):
	if len(gen_dict)>0:
		pc=0;
		for cycle in gen_dict:
			pc+=float(len(cycle.composition)/float(G.number_of_nodes()))*float(cycle.persistence_interval())/float(max_index);
		N=float(len(gen_dict));
	else:
		pc=0;
		N=1;
	return pc/N;


def random_h(G,stringie,dimension,num_iter,max_index):
	h=[];
	ht=[];
	for i in range(num_iter):
		namefile=stringie+str(i)+'.pck';
		gen_temp=pickle.load(open(namefile));
		if gen_temp.has_key(dimension):
			h.append(network_hollowness(gen_temp[dimension],max_index));
			ht.append(network_weighted_hollowness(G,gen_temp[dimension],max_index));
	print 'h='+str(np.mean(h))+'+-'+str(np.std(h));
	print 'ht='+str(np.mean(ht))+'+-'+str(np.std(ht));
	if len(h)>=1:
		a=np.mean(h);
		b=np.std(h);
	else:
		a=0;
		b=0;
	if len(ht)>1:
		c=np.mean(ht);
		d=np.std(ht);
	else:
		c=0;
		d=0;
	return a,b,c,d;
	
def filtration_average_network_hollowness(gen_dict,max_index,dt):
	'''
	Calculates average network hollowness over a moving window 
	along the filtration, where the average is performed over 
	the total number of generators appearing in the homology group. 
	'''
	av_h=[];
	std_h=[];
	lista_indici=range(0,max_index,dt);
	data={};#dict.fromkeys(lista_indici,[]);
	if len(gen_dict)>0:
		N=float(len(gen_dict));
		data[lista_indici[0]]=[];
		for l,el in enumerate(lista_indici[1:]):
			data[el]=[];
			for cycle in gen_dict: 
		#		print l, lista_indici[l], el, cycle.start, cycle.end
				if (float(cycle.start)<=float(el)) and (float(cycle.end)>=float(lista_indici[l])):
		#			print 'in!'
					data[el].append((float(min(float(cycle.end),float(el))-max(float(cycle.start),float(lista_indici[l])))/float(dt)));
		print data
		for i in lista_indici:
			print i, data[i]
			if data[i]:
				av_h.append(np.mean(data[i]));
				std_h.append(np.std(data[i]));
			else:
				av_h.append(0);
				std_h.append(0);

		return lista_indici, av_h, std_h;
	else:
		print 'Cycle dictionary is empty';

def filtration_net_network_hollowness(gen_dict,max_index,dt):
	'''
	Calculates net network hollowness over a moving window 
	along the filtration. 
	The result is the sum of all persistence intervals over
	a given window.
	
	'''
	av_h=[];
	std_h=[];
	lista_indici=range(0,max_index,dt);
	data={};#dict.fromkeys(lista_indici,[]);
	if len(gen_dict)>0:
		N=float(len(gen_dict));
		data[lista_indici[0]]=[];
		for l,el in enumerate(lista_indici[1:]):
			data[el]=[];
			for cycle in gen_dict: 
	#			print l, lista_indici[l], el, cycle.start, cycle.end
				if (float(cycle.start)<=float(el)) and (float(cycle.end)>=float(lista_indici[l])):
	#				print 'in!'
					data[el].append((float(min(float(cycle.end),float(el))-max(float(cycle.start),float(lista_indici[l])))/float(dt)));
		print data
		for i in lista_indici:
			print i, data[i]
			if data[i]:
				av_h.append(np.sum(data[i]));
				std_h.append(np.std(data[i]));
			else:
				av_h.append(0);
				std_h.append(0);

		return lista_indici, av_h, std_h;
	else:
		print 'Cycle dictionary is empty';


def complete_persistence_diagram(gen_dict,factor_l=20,factor_p=1,show=False):
	import matplotlib.pyplot as plt;
	b=[];
	d=[];
	l=[];
	p=[];
	W=0;
	for cycle in gen_dict:
		if float(cycle.end)>float(W):
			W=cycle.end;
	for cycle in gen_dict:
		b.append(float(cycle.start)/float(W));
		d.append(float(cycle.end)/float(W));
		l.append(float(len(cycle.composition))*factor_l);
		p.append(float(cycle.persistence_interval())/float(W)*factor_p);	
	plt.scatter(b,d,l,p);
	plt.xlim(0,1.1*max(max(b),max(d)));
	plt.ylim(0,1.1*max(max(b),max(d)));
	plt.xlabel('Birth');
	plt.ylabel('Death');
	plt.colorbar();
	if show==True:
		plt.show();

def complete_persistence_diagram_improved(gen_dict,W,factor_l=20,factor_p=1,show=False,):
	import matplotlib.pyplot as plt;
	b=[];
	d=[];
	l=[];
	p=[];
	for cycle in gen_dict:
		b.append(float(cycle.start)/float(W));
		d.append(float(cycle.end)/float(W));
		l.append(float(len(cycle.composition))*factor_l);
		p.append(float(cycle.persistence_interval())/float(W)*factor_p);	
	plt.scatter(b,d,l,p);
	plt.xlim(0,1.1*max(max(b),max(d)));
	plt.ylim(0,1.1*max(max(b),max(d)));
	plt.xlabel('Birth');
	plt.ylabel('Death');
	plt.colorbar();
	if show==True:
		plt.show();





def persistence_vs_length(gen_dict,factor_l=1,factor_p=1,show=False):
	import matplotlib.pyplot as plt;
	l=[];
	p=[];
	for cycle in gen_dict:
		l.append(float(len(cycle.composition))*factor_l);
		p.append(float(cycle.persistence_interval())*factor_p);	
	plt.plot(p,xl,'.');
	if show==True:
		plt.show();
	
def generator_lengths(gen_dict,std=False):
	import numpy as np
	l=[];
	for cycle in gen_dict:
		l.append(float(len(cycle.composition)));
	print 'Average generator length: '+str(np.mean(l))+' +- '+str(np.std(l));
	if std==True:
		return np.mean(l), np.std(l);
	else:
		return np.mean(l);


def cumulated_weight_over_threshold(G,weight_thr,weight_name='weight'):
	cum=0;
	cum_tot=0;
	for edge in G.edges(data=True):
		if edge[2][weight_name]>=weight_thr: cum+=edge[2][weight_name];
		cum_tot+=edge[2][weight_name];
	return cum/cum_tot;

def num_link_over_threshold(G,weight_thr,weight_name='weight'):
	cum=0;
	for edge in G.edges(data=True):
		if edge[2][weight_name]>=weight_thr: cum+=1;
	return cum/float(G.number_of_edges());
	

def community_spread_analysis(comm_partition,gen,k,dir,dataset,factor_l=20, factor_p=1):
	import matplotlib.pyplot as plt;
	pers=[];
	community_spread=cycle_community_spread(comm_partition,gen);
	length=[];
	b=[];
	d=[];
	for cycle in gen:
		pers.append(float(cycle.persistence_interval())*factor_p);
		length.append(float(len(cycle.composition))*factor_l);
		b.append(float(cycle.start));
		d.append(float(cycle.end));
	if gen:
		plt.scatter(b,d,length,community_spread);
		plt.xlim(0, 1.1*max(max(b),max(d)));
		plt.ylim(0, 1.1*max(max(b),max(d)));
		plt.colorbar()
		plt.title('Scatter PD with community spread for H_'+str(k));
		if dataset!=' ':
			plt.savefig(dir+dataset+'_scatter_PD_community_spread_H_'+str(k)+'.pdf');
		plt.show()
	renormalized_comm_spread=[];
	for i,w in enumerate(community_spread):
		renormalized_comm_spread.append(float(w)/float(length[i]));
	if gen:
		plt.scatter(b,d,length,renormalized_comm_spread);
		plt.xlim(0, 1.1*max(max(b),max(d)));
		plt.ylim(0, 1.1*max(max(b),max(d)));
		plt.colorbar()
		plt.title('Scatter PD with renormalized community spread for H_'+str(k));
		if dataset!=' ':
			plt.savefig(dir+dataset+'_renormalized_scatter_PD_community_spread_H_'+str(k)+'.pdf');
		plt.show()
	return b,d,length, renormalized_comm_spread; 
	
