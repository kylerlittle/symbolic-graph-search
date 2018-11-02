from pyeda.inter import *
import gvmagic as gv
from graphviz import Source

def graph_BDD(bdd, filename):
    assert isinstance(bdd, BinaryDecisionDiagram)
    dot = bdd.to_dot()   # convert BDD object to raw DOT language str
    src = Source(dot)    # convert raw DOT language str to Source object
    src.render(filename, view=True)

def main():
    # Step 1. Build Boolean Decision Diagram (BDD) denoted as F.
    """
    ...
    """

    # Step 2. Compute the transitive closure of F, denoted as transitiveF
    """
    ...
    """

    # Step 3. Can node i reach node j in one or more steps?
    #         Also, from BDD transitiveF, is some property P satisfied?
    """
    ...
    """


    # Test code
    a, b, c = map(bddvar, 'abc')
    f = a & b | a & c | b & c
    graph_BDD(f, "img/test.gv")


if __name__ == '__main__':
    main()
