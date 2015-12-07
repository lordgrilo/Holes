
##################################################################################
# Persistent homology calculation                                                                    #  
##################################################################################

def persistent_homology_calculation(clique_dictionary_file,max_homology_dimension,dataset_tag, output_dir,jython_call="jython ", script_dir=None, m1=2048,m2=2048,javaplex_directory=None,save_generators=False):
    import os, sys
    import Holes
    from subprocess import call
    
    os.environ["JAVA_MEM"] = "-Xmx"+str(m2)+"m"
    os.environ["JAVA_STACK"] = "-Xms"+str(m1)+"m"
    
    if script_dir==None:
        diodir = os.path.dirname(Holes.__file__)
        script = os.path.join(diodir,'jython_utils','persistent_homology_calculation.py');
    else:
        script = os.path.join(script_dir,'jython_utils','persistent_homology_calculation.py');
    
    if javaplex_directory==None:
            diodir =   os.path.dirname(Holes.__file__)
            javaplex_directory = os.path.join(diodir,'jython_utils','lib');
    
    #here goes the modified jython script

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    #file to be called
    print 'Calling: ' + jython_call+" "+script+" "+clique_dictionary_file+' '+str(max_homology_dimension)+" "+output_dir+" "+dataset_tag+"_ "+javaplex_directory+' '+str(save_generators);

    try:
        retcode = call(jython_call+" "+script+" "+clique_dictionary_file+' '+str(max_homology_dimension)+" "+output_dir+" "+dataset_tag+"_ "+javaplex_directory+' '+str(save_generators), shell=True)
        if retcode < 0:
            print >>sys.stderr, "Child was terminated by signal", -retcode
        else:
            print >>sys.stderr, "Child returned", -retcode
    except OSError, e:
        print >>sys.stderr, "Execution failed:", e

def persistent_cohomology_calculation(clique_dictionary_file,max_homology_dimension,dataset_tag, output_dir,jython_call="jython ", script_dir=None, m1=2048,m2=2048,javaplex_directory=None):
    import os, sys
    import Holes
    from subprocess import call
    
    os.environ["JAVA_MEM"] = "-Xmx"+str(m2)+"m"
    os.environ["JAVA_STACK"] = "-Xms"+str(m1)+"m"
    
    if script_dir==None:
        diodir = os.path.dirname(Holes.__file__)
        script = os.path.join(diodir,'jython_utils','persistent_cohomology_calculation.py');
    else:
        script = os.path.join(script_dir,'jython_utils','persistent_cohomology_calculation.py');
    
    if javaplex_directory==None:
            diodir =   os.path.dirname(Holes.__file__)
            javaplex_directory = os.path.join(diodir,'jython_utils','lib');
    
    #here goes the modified jython script

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    #file to be called
    print 'Calling: ' + jython_call+" "+script+" "+clique_dictionary_file+' '+str(max_homology_dimension)+" "+output_dir+" "+dataset_tag+"_ "+javaplex_directory;

    try:
        retcode = call(jython_call+" "+script+" "+clique_dictionary_file+' '+str(max_homology_dimension)+" "+output_dir+" "+dataset_tag+"_ "+javaplex_directory, shell=True)
        if retcode < 0:
            print >>sys.stderr, "Child was terminated by signal", -retcode
        else:
            print >>sys.stderr, "Child returned", -retcode
    except OSError, e:
        print >>sys.stderr, "Execution failed:", e