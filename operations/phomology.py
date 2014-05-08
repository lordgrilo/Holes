
##################################################################################
# Persistent homology calculation                                                                    #  
##################################################################################

def persistent_homology_calculation(clique_dictionary_file,max_homology_dimension,dataset_tag, output_dir,jython_call="jython ", script_dir=None, m1=2048,m2=2048,javaplex_directory=None):
    import os, sys
    import Holes
    from subprocess import call
    mem_options='-J-Xms'+str(m1)+'m -J-Xmx'+str(m2)+'m ';  
        
    if script_dir==None:
        diodir = os.path.dirname(Holes.__file__)
        script = diodir+'/jython_utils/persistent_homology_calculation.py';
    else:
        script = script_dir + '/jython_utils/persistent_homology_calculation.py';
    
    if javaplex_directory==None:
            diodir =   os.path.dirname(Holes.__file__)
            javaplex_directory = diodir+'/jython_utils/lib/';
    
    #here goes the modified jython script

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    #file to be called
    print 'Calling: '+ jython_call+" "+mem_options+" "+script+" "+clique_dictionary_file+' '+str(max_homology_dimension)+" "+output_dir+" "+dataset_tag+"_ "+javaplex_directory;

    try:
        retcode = call(jython_call+" "+mem_options+" "+script+" "+clique_dictionary_file+' '+str(max_homology_dimension)+" "+output_dir+" "+dataset_tag+"_ "+javaplex_directory, shell=True)
        if retcode < 0:
            print >>sys.stderr, "Child was terminated by signal", -retcode
        else:
            print >>sys.stderr, "Child returned", -retcode
    except OSError, e:
        print >>sys.stderr, "Execution failed:", e
