
##################################################################################
# Persistent homology calculation                                                                    #  
##################################################################################

def persistent_homology_calculation(clique_dictionary_file,max_homology_dimension,dataset_tag, output_dir,jython_call="jython ",script='/Users/lordgrilo/Dropbox/Holes/jython_utils/persistent_homology_calculation.py',m1=2048,m2=2048,javaplex_directory="/Users/lordgrilo/Documents/Tools/javaplex"):
    import os
    from subprocess import call
    mem_options='-J-Xms'+str(m1)+'m -J-Xmx'+str(m2)+'m ';  

    #here goes the modified jython script

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    #file to be called

    try:
        retcode = call(jython_call+" "+script+" "+clique_dictionary_file+' '+str(max_homology_dimension)+" "+output_dir+" "+dataset_tag+"_ "+javaplex_directory, shell=True)
        if retcode < 0:
            print >>sys.stderr, "Child was terminated by signal", -retcode
        else:
            print >>sys.stderr, "Child returned", retcode
    except OSError, e:
        print >>sys.stderr, "Execution failed:", e
