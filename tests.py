import unittest
import __init__ as nxigraph

class TestNameAttributes(unittest.TestCase):
    """
    Tests attribute name compatibility between igraph and networkx.

    ..  note:: I am assuming the convention of using "name" to refer to the
        name of vertices following the tutorial_.

        .. _tutorial: http://www.cs.rhul.ac.uk/home/tamas/development/igraph/tutorial/tutorial.html#setting-and-retrieving-attributes
    """

    def setUp(self):
        edgelist = [('blue', 'purple'), # Our sample network of strings
                         ('blue', 'green'),
                         ('blue', 'red'),
                         ('yellow', 'green'),
                         ('green', 'orange')]
        self.nxg = nxigraph.NXiGraph() # Sample object
        self.nxg.add_edges_from(edgelist) # Use standard networkx api

    def testNames(self):
        "Simple name test"
        self.assertEqual(self.nxg.nodes(), self.nxg.igraph.vs["name"])

    def testNamesAndDegree(self):
        """
        Tests names more stringently using degree.

        .. note:: Ambiguous names outside the scope of this test.
        """

        for n in self.nxg.nodes():
            node_name = str(n)
            igraph_node = self.nxg.igraph.vs.select(name_eq=node_name)
            self.assertEqual(self.nxg.degree(n), igraph_node.degree()[0])
        
if __name__ == '__main__':
    unittest.main()
