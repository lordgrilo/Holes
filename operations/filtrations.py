##################################################################################
# Filtrations 					 												 #	
##################################################################################

def standard_weight_clique_rank_filtration(G,IR_weight_cutoff=None):

    if IR_weight_cutoff==None:
    	IR_weight_cutoff=np.min(nx.get_edge_attributes(G,'weight'));

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

    for index,IR_weight_cutoff in enumerate(edge_weights):
        if IR_weight_cutoff>IR_weight_cutoff:
            #print "Index: "+str(index)+". IR_weight_cutoffeshold: "+str(IR_weight_cutoff);
            for edge in G.edges(data=True):
                if edge[2]['weight']>=IR_weight_cutoff:
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
                            Clique_dictionary[str(list(subclique))].append(str(IR_weight_cutoff))
                            max_index=index;

    print('Max filtration value: '+str(max_index));              
    print('Clique dictionary created.');
    return Clique_dictionary;



def dense_graph_weight_clique_rank_filtration(G0,max_homology_dimension,IR_weight_cutoff=None):   
    G=nx.Graph();
    G.add_nodes_from(G0.nodes(data=True));
    G.add_edges_from(G0.edges());
    
    if IR_weight_cutoff==None:
        IR_weight_cutoff=np.min(np.array(nx.get_edge_attributes(G,'weights').values()));
    
    #preliminary scan of edge weights to define filtration steps
    print('Preliminary scan of edge weights to define filtration steps...');
    edge_weights=nx.get_edge_attributes(G,'weight').values();
    edge_weights=list(set(edge_weights));
    edge_weights=sorted(edge_weights, reverse=True);
    max_rank=len(edge_weights);
    print('Preliminary scan and sorting completed.')
    print('Max rank: '+str(max_rank));
    #Relabel edge weights with respective rank
    edge_weight_dict=dict.fromkeys(G.edges());
    for edge in G.edges():
        edge_weight_dict[edge]=edge_weights.index(G[edge[0]][edge[1]]['weight']);
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
