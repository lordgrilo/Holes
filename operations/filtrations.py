##################################################################################
# Filtrations 					 												 #	
##################################################################################
import numpy as np;
import networkx as nx;
import itertools

def standard_weight_clique_rank_filtration(G,IR_weight_cutoff=None,verbose=False):
    
    if IR_weight_cutoff==None:
    	IR_weight_cutoff=np.min(nx.get_edge_attributes(G,'weight').values());

    print('Preliminary scan of edge weights to define filtration steps...');
    edge_weights=nx.get_edge_attributes(G,'weight').values();
    edge_weights=list(set(edge_weights));
    edge_weights=sorted(edge_weights, reverse=True);
    max_index=len(edge_weights);
        
    # Define the clique dictionary
    Clique_dictionary={};
    print('Constructing filtration...');
    #Beginning of filtration construction
    G_supplementary=nx.Graph();

    #the max index will be used for the persistent homology computation 
    max_index=0; 

    for index,thr in enumerate(edge_weights):
        if thr>=IR_weight_cutoff:
            #print "Index: "+str(index)+". IR_weight_cutoffeshold: "+str(IR_weight_cutoff);
            for edge in G.edges(data=True):
                if edge[2]['weight']>=thr:
                	G_supplementary.add_edge(edge[0],edge[1]);
            
            #clique detection in partial graph
            cliques=nx.find_cliques_recursive(G_supplementary);
            # adding cliques to the filtration
            for clique in cliques: #loop on new clique
                clique.sort();

                for k in range(1,len(clique)+1): #loop on clique dimension to find missed faces of simplex
                    for subclique in itertools.combinations(clique,k):
                        if str(list(subclique)) not in Clique_dictionary:
                            Clique_dictionary[str(list(subclique))]=[];
                            Clique_dictionary[str(list(subclique))].append(str(index));
                            Clique_dictionary[str(list(subclique))].append(str(thr))
                            max_index=index;

    print('Max filtration value: '+str(max_index));              
    print('Clique dictionary created.');
    return Clique_dictionary;


def limited_weight_clique_rank_filtration(G,max_clique_dim,IR_weight_cutoff=None,verbose=False):
    
    if IR_weight_cutoff==None:
        IR_weight_cutoff=np.min(nx.get_edge_attributes(G,'weight').values());

    print('Preliminary scan of edge weights to define filtration steps...');
    edge_weights=nx.get_edge_attributes(G,'weight').values();
    edge_weights=list(set(edge_weights));
    edge_weights=sorted(edge_weights, reverse=True);
    max_index=len(edge_weights);
        
    # Define the clique dictionary
    Clique_dictionary={};
    print('Constructing filtration...');
    #Beginning of filtration construction
    G_supplementary=nx.Graph();

    #the max index will be used for the persistent homology computation 
    max_index=0; 

    for index,thr in enumerate(edge_weights):
        if thr>=IR_weight_cutoff:
            #print "Index: "+str(index)+". IR_weight_cutoffeshold: "+str(IR_weight_cutoff);
            for edge in G.edges(data=True):
                if edge[2]['weight']>=thr:
                    G_supplementary.add_edge(edge[0],edge[1]);
            
            #clique detection in partial graph
            cliques=nx.find_cliques_recursive(G_supplementary);
            # adding cliques to the filtration
            for clique in cliques: #loop on new clique
                clique.sort();

                for k in range(1,np.min([max_clique_dim, len(clique)])+1): #loop on clique dimension to find missed faces of simplex
                    for subclique in itertools.combinations(clique,k):
                        if str(list(subclique)) not in Clique_dictionary:
                            Clique_dictionary[str(list(subclique))]=[];
                            Clique_dictionary[str(list(subclique))].append(str(index));
                            Clique_dictionary[str(list(subclique))].append(str(thr))
                            max_index=index;

    print('Max filtration value: '+str(max_index));              
    print('Clique dictionary created.');
    return Clique_dictionary;




def upward_weight_clique_rank_filtration(G,UV_weight_cutoff=None,verbose=False):
    if UV_weight_cutoff==None:
        UV_weight_cutoff=np.max(nx.get_edge_attributes(G,'weight').values());

    print('Preliminary scan of edge weights to define filtration steps...');
    edge_weights=nx.get_edge_attributes(G,'weight').values();
    edge_weights=list(set(edge_weights));
    edge_weights=sorted(edge_weights);
    max_index=len(edge_weights);
        
    # Define the clique dictionary
    Clique_dictionary={};
    print('Constructing filtration...');
    #Beginning of filtration construction
    G_supplementary=nx.Graph();

    #the max index will be used for the persistent homology computation 
    max_index=0; 

    for index,thr in enumerate(edge_weights):
        if verbose==True:
            print index, thr;
        if thr<=UV_weight_cutoff:
            #print "Index: "+str(index)+". IR_weight_cutoffeshold: "+str(IR_weight_cutoff);
            for edge in G.edges(data=True):
                if edge[2]['weight']<=thr:
                    G_supplementary.add_edge(edge[0],edge[1]);
            #clique detection in partial graph
            cliques=nx.find_cliques_recursive(G_supplementary);
            # adding cliques to the filtration
            for clique in cliques: #loop on new clique
                clique.sort();

                for k in range(1,len(clique)+1): #loop on clique dimension to find missed faces of simplex
                    for subclique in itertools.combinations(clique,k):
                        if str(list(subclique)) not in Clique_dictionary:
                            Clique_dictionary[str(list(subclique))]=[];
                            Clique_dictionary[str(list(subclique))].append(str(index));
                            Clique_dictionary[str(list(subclique))].append(str(thr))
                            max_index=index;

    print('Max filtration value: '+str(max_index));              
    print('Clique dictionary created.');
    return Clique_dictionary;






def dense_graph_weight_clique_rank_filtration(G0,max_homology_dimension,IR_weight_cutoff=None):   
    G=nx.Graph();
    G.add_nodes_from(G0.nodes(data=True));
    G.add_edges_from(G0.edges());
    
    if IR_weight_cutoff==None:
        IR_weight_cutoff=np.min(np.array(nx.get_edge_attributes(G0,'weight').values()));
    
    #preliminary scan of edge weights to define filtration steps
    print('Preliminary scan of edge weights to define filtration steps...');
    edge_weights=nx.get_edge_attributes(G0,'weight').values();
    edge_weights=list(set(edge_weights));
    edge_weights=sorted(edge_weights, reverse=True);
    max_rank=len(edge_weights);
    print('Preliminary scan and sorting completed.')
    print('Max rank: '+str(max_rank));
    #Relabel edge weights with respective rank
    edge_weight_dict=dict.fromkeys(G.edges());
    for edge in G.edges():
        edge_weight_dict[edge]=edge_weights.index(G0[edge[0]][edge[1]]['weight']);
    nx.set_edge_attributes(G,'weight',edge_weight_dict);
    #Define the clique dictionary
    Clique_dictionary={};
    print('Constructing filtration...');
    #Beginning of filtration construction
    for n in G.nodes():
        Clique_dictionary[str(n)]=[];
        Clique_dictionary[str(n)].append(str(0));
    for k in range(2,max_homology_dimension+3):
        print 'Scanning cliques of dimension: ',k;
        for clique in itertools.combinations(G.nodes(),k):
            w=[];
            valid_clique=1;
            for link in itertools.combinations(clique,2):
                if G.has_edge(link[0],link[1]):
                    w.append(G[link[0]][link[1]]['weight']);
                else:
                    valid_clique=0;
                    break;
            if valid_clique==1:
                Clique_dictionary[str(list(clique))]=[];
                Clique_dictionary[str(list(clique))].append(str(max(w)));
    print('Clique dictionary created.');
    return Clique_dictionary;




def upward_dense_graph_weight_clique_rank_filtration(G0,max_homology_dimension,UV_weight_cutoff=None):   

    G=nx.Graph();
    G.add_nodes_from(G0.nodes(data=True));
    G.add_edges_from(G0.edges());
    
    if UV_weight_cutoff==None:
        UV_weight_cutoff=np.max(nx.get_edge_attributes(G0,'weight').values());
        print 'Uv cut', UV_weight_cutoff
    print('Preliminary scan of edge weights to define filtration steps...');
    edge_weights=nx.get_edge_attributes(G0,'weight').values();
    edge_weights=list(set(edge_weights));
    edge_weights=sorted(edge_weights);
    max_index=len(edge_weights);
    print('Preliminary scan and sorting completed.')

    #Relabel edge weights with respective rank
    edge_weight_dict=dict.fromkeys(G.edges());
    for edge in G.edges():
        edge_weight_dict[edge]=edge_weights.index(G0[edge[0]][edge[1]]['weight']);
    nx.set_edge_attributes(G,'weight',edge_weight_dict);
    
    #Define the clique dictionary
    Clique_dictionary={};
    print('Constructing filtration...');
    
    #Beginning of filtration construction
    for n in G.nodes():
        Clique_dictionary[str(n)]=[];
        Clique_dictionary[str(n)].append(str(0));
    for k in range(2,max_homology_dimension+3):
        print 'Scanning cliques of dimension: ',k;
        for clique in itertools.combinations(G.nodes(),k):
            w=[];
            valid_clique=1;
            for link in itertools.combinations(clique,2):
                if G.has_edge(link[0],link[1]):
                    w.append(G[link[0]][link[1]]['weight']);
                else:
                    valid_clique=0;
                    break;
            if valid_clique==1:
                Clique_dictionary[str(list(clique))]=[];
                Clique_dictionary[str(list(clique))].append(str(max(w)));
    print('Clique dictionary created.');
    return Clique_dictionary;



def metrical_filtration(distance_graph, max_dim=None):
    '''
    A metrical filtration is just a normal ascending filtration on a distance graph
    obtained from the original graph
    
    input:
            - distance graph
            - maximum dimension for which to calculate clique dimension
    returns:
            - filtration 
    '''
    if max_dim==None:
        clique_dict=upward_dense_graph_weight_clique_rank_filtration(distance_graph,max_dim=distance_graph.number_of_nodes());
    else:
        clique_dict=upward_dense_graph_weight_clique_rank_filtration(distance_graph,max_dim);

    return clique_dict;
    
    
def distance_graph(G,metric='shortest_path_inverse'):
    '''
    Supported distances:
     - shortest_path_inverse : shortest path calculated on inverted weight (a strong link means the two nodes are close)
     - shortest_path : standard shortest path (strong link means nodes are far away from each other)

    '''
    if metric=='shortest_path_inverse':
        G_suppl=nx.Graph();
        G_suppl.add_nodes_from(G.nodes(data=True));
        for e in G.edges(data=True):
            if 'weight' in e[2]:
                G_suppl.add_edge(e[0],e[1],weight=float(1/e[2]['weight']));
            else:
                G_suppl.add_edge(e[0],e[1],weight=float(1));
        distance_dict=nx.shortest_path_length(G_suppl,weight='weight');
        del G_suppl;

    if metric=='shortest_path':
        G_suppl=nx.Graph();
        G_suppl.add_nodes_from(G.nodes(data=True));
        for e in G.edges(data=True):
            if 'weight' in e[2]:
                G_suppl.add_edge(e[0],e[1],weight=float(e[2]['weight']));
            else:
                G_suppl.add_edge(e[0],e[1],weight=float(1));
        distance_dict=nx.shortest_path_length(G_suppl,weight='weight');
        del G_suppl;

    distance_graph=nx.Graph();
    distance_graph.add_nodes_from(G.nodes(data=True));
    for i,n in enumerate(distance_dict.keys()):
        for j,m in enumerate(distance_dict.keys()[i:]):
            if j>i:
                distance_graph.add_edge(n,m,weight=distance_dict[n][m]);

    return distance_graph;



##################################################################################
# Network manipulations                                                          #  
##################################################################################


def duplicated_graph(D, maxweight = 0, weight='weight'):
    import networkx as nx
    G=D.copy()
    W=nx.DiGraph()
    W=G
    if type(G) == nx.MultiGraph or type(G) == nx.MultiDiGraph:
        raise Exception("stochastic_graph not implemented for multigraphs")
    if  maxweight==0:
        for (u,v,d) in G.edges(data=True):
            if d > maxweight:
                maxweight = d
    L = len(G.nodes())
    if min(G.nodes())==0:
        N=L+1
    else:
        N=L
    for u in G.nodes():
            W.add_edge(u,u+N,maxweight)
 
    
    for (u,v,p) in G.edges(data=True):
        u_v = 0
        
        if v>u:
                W.add_edge(u,v,p)
        elif v<u:
            W.add_edge(u+N,v+N,p)
            e = (u,v)
            G.remove_edge(*e)
            
        elif v==u:
            if 10+u not in G.nodes():
                u_v=10+u
            elif 100+u not in G.nodes():
                u_v=100+u
            elif 1000+u not in G.nodes():
                u_v=1000+u
            elif 10000+u not in G.nodes():
                c=10000
                u_v=10000+u
            else:
                print "Problemi col nome dei nodi per eliminare i self loop (specification construction)"
            G.add_edge(u,u_v,p)
            #print (u,u_v,p)
            v2=v+N
            G.add_edge(u_v,v2,maxweight)
            #u__v=u_v+N
            #G.add_edge(u_v,u__v,weight=maxweight)
            #G.add_edge(u__v,v+N,weight=maxweight)#nota u_v maggiore di v

            e = (u,v)
            G.remove_edge(*e)
#        print "G:  ", G.edges()
                  #for (u,v,d) in G.edges(data=True):
    return W




def local_standard_weight_clique_rank_filtration(G,IR_weight_cutoff=None,verbose=False):
    
    if IR_weight_cutoff==None:
        IR_weight_cutoff=np.min(nx.get_edge_attributes(G,'weight').values());

    print('Preliminary scan of edge weights to define filtration steps...');
    edge_weights=nx.get_edge_attributes(G,'weight');
    weight_edge = {}
    for e,w in edge_weights.items():
        if w not in weight_edge:
            weight_edge[w] = []
        weight_edge[w].append(e);

    edge_weights=list(set(edge_weights.values()));
    edge_weights=sorted(edge_weights, reverse=True);
    max_index=len(edge_weights);
        
    # Define the clique dictionary
    Clique_dictionary={};
    print('Constructing filtration...');
    #Beginning of filtration construction
    G_supplementary=nx.Graph();

    #the max index will be used for the persistent homology computation 
    max_index=0; 
    current_nodes = []
    
    for index,thr in enumerate(edge_weights):
        new_nodes = [];
        if thr>=IR_weight_cutoff:
            G_supplementary.add_edges_from(weight_edge[thr]);
            [new_nodes.extend(edge) for edge in weight_edge[thr]];
            new_nodes = list(set(new_nodes));

            ## clique detection in partial graph, where there cliques are found only on the
            ## new nodes.
            relevant_nodes = []
            [relevant_nodes.extend(G_supplementary.neighbors(n)) for n in new_nodes];
            relevant_nodes = list(set(relevant_nodes));
            G_supp_supp = nx.subgraph(G_supplementary,relevant_nodes);
            cliques=nx.find_cliques_recursive(G_supp_supp);
            # adding cliques to the filtration
            for clique in cliques: #loop on new clique
                clique.sort();

                for k in range(1,len(clique)+1): #loop on clique dimension to find missed faces of simplex
                    for subclique in itertools.combinations(clique,k):
                        if str(list(subclique)) not in Clique_dictionary:
                            Clique_dictionary[str(list(subclique))]=[];
                            Clique_dictionary[str(list(subclique))].append(str(index));
                            Clique_dictionary[str(list(subclique))].append(str(thr))
                            max_index=index;

    print('Max filtration value: '+str(max_index));              
    print('Clique dictionary created.');
    return Clique_dictionary;



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




