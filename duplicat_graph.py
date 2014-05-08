import networkx as nx

def duplicated_graph(D, maxweight = 0, weight='weight'):
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
