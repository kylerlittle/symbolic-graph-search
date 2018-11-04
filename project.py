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

def compose(H, F):
    """Compose operator discussed in class
    """
    bitsPerNode = int(H.degree/2)
    Z = exprvars('Z', bitsPerNode)
    H = H.compose({H.inputs[i+bitsPerNode]: Z[i] for i in range(bitsPerNode)})
    F = F.compose({F.inputs[i]: Z[i] for i in range(bitsPerNode)})
    result = H & F

    # Now, check for existence... 
    # i.e. there exists z1, z2, ..., zk such that H(x1, x2, ..., xk, z1, ..., zk) & F(z1, ..., zk, y1, .... yk)
    result = result.smoothing(Z)
    return result

def computeTransitiveClosure(boolExpr):
    # Initialize _H as initial boolean expression
    _H = boolExpr
    H = Or()        # some random Expression not equal to _H
    edgesToReach = 2; max_iterations = 5
    canReachInXStepsExpr = {1:boolExpr}
    while _H.equivalent(H) == False and edgesToReach < max_iterations:
        H = _H
        _H = (compose(_H, H) | _H).simplify()
        canReachInXStepsExpr[edgesToReach] = _H
        edgesToReach += 1
    return canReachInXStepsExpr

def canReach(a, b, canReachInXStepsExpr, modulo, bits_needed):
    """Determines whether node a can reach node b. Returns number of edges to reach b if possible;
    otherwise, returns None
    """
    assert isinstance(a, int) and isinstance(b, int)
    for key in canReachInXStepsExpr.keys():
        expr = canReachInXStepsExpr[key]
        edgeNumber = (uint2exprs(a%modulo, length=bits_needed) + uint2exprs(b%modulo, length=bits_needed)).to_uint()
        if numSatisfiesExpr(edgeNumber, expr, bits_needed*2) == True:
            return key
    else:
        return None

def main():
    # Step 1. Build Boolean Decision Diagram (BDD) denoted as F.
    # Vary the following parameters to observe different program behavior.
    nodes = 32
    modulo = 32
    offset = 0
    bits_needed = uint2exprs(nodes + offset - 1).size

    # Build expr that accepts 10 1-bit variables. If those 10 bits represent an edge, the expression will return true
    boolExpr = generateEdgeExpr(modulo, nodes, offset).simplify()

    # Test code to ensure all edges are correct.
    for i in range(offset, nodes+offset):
        for j in range(offset, nodes+offset):
            if (i+3)%modulo == j%modulo or (i+7)%modulo == j%modulo:
                edgeNumber = (uint2exprs(i%modulo, length=bits_needed) + uint2exprs(j%modulo, length=bits_needed)).to_uint()
                assert numSatisfiesExpr(edgeNumber, boolExpr, bits_needed*2) == True
                print("There is an edge from {0} to {1}.".format(i,j))
    F = expr2bdd(boolExpr)
    graph_BDD(F, "img/F.gv")

    # Step 2. Compute the transitive closure of F, denoted as transitiveF
    canReachInXStepsExpr = computeTransitiveClosure(boolExpr)

    # Step 3. Can node i reach node j in one or more steps?
    for i in range(offset, nodes+offset):
        for j in range(offset, nodes+offset):
            result = canReach(i, j, canReachInXStepsExpr, modulo, bits_needed)
            if result is not None:
                print("Node {0} can reach node {1} in {2} edge(s)".format(i,j,result))

if __name__ == '__main__':
    main()