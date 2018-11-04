from pyeda.inter import *
import gvmagic as gv
from graphviz import Source

debug = False

def graph_BDD(bdd, filename):
    """Graph bdd; display it; save as filename
    """
    assert isinstance(bdd, BinaryDecisionDiagram)
    dot = bdd.to_dot()   # convert BDD object to raw DOT language str
    src = Source(dot)    # convert raw DOT language str to Source object
    src.render(filename, view=True)    

def generateEdgeExpr(modulo, nodes, offset):
    """Generate boolean function which returns true (1) if edge from a to b. Else false (0)
    """
    assert isinstance(modulo, int) and isinstance(nodes, int) and isinstance(offset, int)
    bits_needed = uint2exprs(nodes + offset - 1).size
    fullEdgeExpr = Or()

    if debug: print("Generating edge expression with...\nmodulo: {0}\nnodes: {1}\noffset: {2}".format(modulo, nodes, offset))

    for i in range(offset, nodes+offset):
        for j in range(offset, nodes+offset):
            # If we actually want to include this edge
            if (i+3)%modulo == j%modulo or (i+7)%modulo == j%modulo:
                # Get (2*bits_needed)-bit representation of ij (concatenated)
                edge_bin = uint2exprs(i%32, length=bits_needed) + uint2exprs(j%32, length=bits_needed)
                
                # Declare our bits_needed-bit variables as a bit-vector
                currEdge = exprvars('edge', bits_needed*2)

                # First bits_needed bits represent num #1, second represent num #2; '~' if 0, o.w. normal; then, '&' everything
                edgeExpr = And()
                for k in range(bits_needed):
                    edgeExpr &= (Not(currEdge[k]) if edge_bin[k] == expr(0) else currEdge[k]) \
                    & (Not(currEdge[k+bits_needed]) if edge_bin[k+bits_needed] == expr(0) else currEdge[k+bits_needed])
                if debug: print("Adding {0}".format(edgeExpr))

                # 'Or' it with our full expression, since any edge which satisfies this criteria should be included
                fullEdgeExpr |= edgeExpr
    return fullEdgeExpr

def numSatisfiesExpr(num, expression, bits_needed):
    """Ugly hack to determine whether an integer (num) satisfies a Boolean Expression
    """ 
    assert isinstance(num, int) and isinstance(expression, Expression)
    result = True

    # Get binary number string of num (using 'bits_needed' binary values)
    binNumStr = ''.join(reversed([str(binDigit) for binDigit in uint2bdds(num, length=bits_needed)]))
    if debug: print("Testing that {0} ({1}) satisfies expression.".format(num, binNumStr))

    # Iterate over each Boolean Point (represented by a dict in pyEDA) that satisfies expression
    for point in expression.satisfy_all():
        # 'point' is an unordered dictionary, so convert it to its correct binary string representation
        B = reversed(sorted([key for key in point.keys()]))

        # Now that keys (variable names) are sorted, get binary digits & join them into a string
        strOfPoint = ''.join([str(point[variableVal]) for variableVal in B])

        if strOfPoint == binNumStr:
            if debug: print("==> YES -- {0} ({1}) satisifies expression.".format(num, binNumStr))
            break
    else:
        if debug: print("==> NO -- {0} ({1}) doesn't satisify expression.".format(num, binNumStr))
        result = False
    return result
        

def main():
    # Step 1. Build Boolean Decision Diagram (BDD) denoted as F.
    """
    First build a Boolean expression; then convert it to BDD.
    The expression must accept 10 bit variables. If those 10 bits represent an edge, the expression will return true (1).

    I can then test my answer by calling numSatisfiesExpr(  (expr(i, length=5) + expr(j, length=5)).to_uint(), expr  )
    """
    nodes = 32
    modulo = 32
    offset = 0
    bits_needed = uint2exprs(nodes + offset - 1).size
    boolExpr = generateEdgeExpr(modulo, nodes, offset).simplify()
    for i in range(offset, nodes+offset):
        for j in range(offset, nodes+offset):
            if (i+3)%modulo == j%modulo or (i+7)%modulo == j%modulo:
                edgeNumber = (uint2exprs(i%32, length=bits_needed) + uint2exprs(j%32, length=bits_needed)).to_uint()
                assert numSatisfiesExpr(edgeNumber, boolExpr, bits_needed*2) == True
                print("There is an edge from {0} to {1}.".format(i,j))
    F = expr2bdd(boolExpr)
    graph_BDD(F, "img/F.gv")


    # Step 2. Compute the transitive closure of F, denoted as transitiveF
    """
    ...
    """

    # Step 3. Can node i reach node j in one or more steps?
    #         Also, from BDD transitiveF, is some property P satisfied?
    """
    ...
    """


if __name__ == '__main__':
    main()
