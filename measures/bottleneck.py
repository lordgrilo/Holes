##################################################################################
# Bottleneck distance functions 												 #	
##################################################################################
import numpy as np

def normalize_dict(G,M=None):
    if M==None:
        M=0;
        for g in G[0]:
            M=max(M,float(g.end));
    print M
    norm_dict={};
    for d in G:
        norm_dict[d]=[]
        for g in G[d]:
            gg=Phom.Cycle(d,g.composition,float(g.start)/M, float(g.end)/M);
            norm_dict[d].append(gg);

    return norm_dict;


def L_infinity_gen_distance(cycle1,cycle2, verbose=False):
	if cycle1!='None' and cycle2!='None':
	    x1,y1 = float(cycle1.start), float(cycle1.end);
	    x2,y2 = float(cycle2.start), float(cycle2.end);
	    norm = max(np.abs(x2-x1), np.abs(y2-y1))
	else:
	    if cycle1=='None':
	        norm = np.abs((float(cycle2.end)-float(cycle2.start))/2);
	    if cycle2=='None':
	        norm = np.abs((float(cycle1.end)-float(cycle1.start))/2);

	if norm==0 and verbose==True:
	    print 'norm=0: ';
	    cycle1.summary();
	    cycle2.summary();
	return norm;


def bottleneck_distance(gener1,gener2,dim, showfig=True):
    #in truth this is the Hausdorff distance (need to correct)
    import numpy as np
    gg1=gener1[dim];
    gg2=gener2[dim];
    if len(gg1)==0 and len(gg2)==0:
        print 'No generators at dimension ',dim;
        return None;
    
    print '# of generators in dictionaries: ', len(gg1), len(gg2)
    print 'Constructing distance matrix..';
    B=np.zeros((len(gg1),len(gg2)));
    for i,c in enumerate(gg1):
        for j,cc in enumerate(gg2):
            if i<=j:
                B[i][j]=L_infinity_gen_distance(c,cc);
                B[j][i]=B[i][j];
    print 'Parsing values to find Hausdorff distance..'
    if showfig==True:
        figure(figsize=(10,10)), pcolor(B), colorbar(), show();
    d_B=np.max(np.max(np.min(B,0)), np.max(np.min(B,1)));
    print d_B;
    return d_B;

