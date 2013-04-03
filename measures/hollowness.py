##################################################################################
# Hollowness measures 															 #	
##################################################################################


def network_hollowness(gen_list,max_index):
	if len(gen_list)>0:
		pc=0;
		for cycle in gen_list:
			pc+=float(cycle.persistence_interval())/float(max_index);
		N=float(len(gen_list));
	else:
		pc=0;
		N=1;
	return pc/N;
	
def network_weighted_hollowness(G,gen_list,max_index):
	if len(gen_list)>0:
		pc=0;
		for cycle in gen_list:
			pc+=float(len(cycle.composition)/float(G.number_of_nodes()))*float(cycle.persistence_interval())/float(max_index);
		N=float(len(gen_list));
	else:
		pc=0;
		N=1;
	return pc/N;

