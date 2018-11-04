from pyeda.inter import *
import gvmagic as gv
from graphviz import Source

def graph_BDD(bdd, filename):
    assert isinstance(bdd, BinaryDecisionDiagram)
    dot = bdd.to_dot()   # convert BDD object to raw DOT language str
    src = Source(dot)    # convert raw DOT language str to Source object
    src.render(filename, view=True)    

def isEdgeBetweenExpr():
    """Return boolean function which returns true (1) if edge from a to b. Else false (0)
    """
    # assert isinstance(a, int) and isinstance(b, int)

    # Convert a and b to farray representations
    # a_bin_plus_three = uint2exprs((a+3)%32, length=5)
    # a_bin_plus_seven = uint2exprs((a+7)%32, length=5)
    # b_bin = uint2exprs(b%32, length=5)

    # # Store a_bin + bin(three) && a_bin + bin(seven)
    # ci = exprvar('ci', 5)
    # a_bin_plus_three = ~(a_bin ^ 
    # a_bin_plus_seven = 0

    # Mod ^^ by 32 and b_bin by 32.
    # a_bin_plus_three_mod_32 = a_bin_plus_three.rsh(5)
    # a_bin_plus_seven_mod_32 = a_bin_plus_seven.rsh(5)
    # b_bin_mod_32 = b_bin.rsh(5)

    # return ~(a_bin_plus_three ^ b_bin) | ~(a_bin_plus_seven ^ b_bin)

    # Return true if (a+3) % 32 == b or (a+7) % 32 == b
    # return ~(a_bin_plus_three_mod_32 ^ b_bin_mod_32) | ~(a_bin_plus_seven_mod_32 ^ b_bin_mod_32)
    three = uint2exprs(3, length=10)  # 5-bit representation of 3
    num = exprvars('X', 10)

    # Res is an expression that determines whether num == 3.
    res = (~(num ^ three)).uand()
    return res

def numSatisfiesExpr(num, expression, bits_needed):
    """Ugly hack to determine whether an integer (num) satisfies a Boolean Expression
    """ 
    assert isinstance(num, int) and isinstance(expression, Expression)
    result = True

    # Get binary number string of num (using 'bits_needed' binary values)
    binNumStr = ''.join(reversed([str(binDigit) for binDigit in uint2bdds(num, length=bits_needed)]))
    print("Testing that {0} ({1}) satisfies expression.".format(num, binNumStr))

    # Iterate over each Boolean Point (represented by a dict in pyEDA) that satisfies expression
    for point in expression.satisfy_all():
        # 'point' is an unordered dictionary, so convert it to its correct binary string representation
        B = reversed(sorted([key for key in point.keys()]))

        # Now that keys (variable names) are sorted, get binary digits & join them into a string
        strOfPoint = ''.join([str(point[variableVal]) for variableVal in B])

        if strOfPoint == binNumStr:
            print("==> YES -- {0} ({1}) satisifies expression.".format(num, binNumStr))
            break
    else:
        print("==> NO -- {0} ({1}) doesn't satisify expression.".format(num, binNumStr))
        result = False
    return result
        

def main():
    # Step 0. Generate 32 integers for graph.
    L = [i for i in range(32)]

    # Step 1. Build Boolean Decision Diagram (BDD) denoted as F.
    """
    ...
    """
    three = uint2exprs(3, length=5)  # 5-bit representation of 3
    seven = uint2exprs(7, length=5)  # 5-bit representation of 7
    # print(adder(three, seven))
    print(three)
    print(seven)
    num = exprvars('X', 5)
    print(~(num ^ three))
    # Res is an expression that determines whether num == 3.
    res = (~(num ^ three)).uand()
    assert numSatisfiesExpr(3, res, 5) == True
    assert numSatisfiesExpr(9, res, 5) == False


    pointsThatSatisfyRes = list(res.satisfy_all())
    # print("points: {0}".format(pointsThatSatisfyRes))
    # testStr = ''
    # for val in pointsThatSatisfyRes[0].values():
    #     testStr += str(val)
    # print("point in binary: {0}".format(testStr))

    # print("TYPE ==> {0}".format(type(pointsThatSatisfyRes[0])))
    # print(res)
    # print(type(res))
    # print(res.degree)
    # print(res.support)
    print(expr2truthtable(res))

    """
    Instead of passing in integers, I just need 5-bit variables. The expression must accept
    10 bit variables and then return all 10 bit variables which satisfy it.
    I can then test my answer by calling numSatisfiesExpr(  (expr(i, length=5) + expr(j, length=5)).to_uint(), expr  )
    """

    print("testing")
    for i in range(32):
        for j in range(32):
            edgeNumber = (uint2exprs(i, length=5) + uint2exprs(j, length=5)).to_uint()
            if numSatisfiesExpr(edgeNumber, isEdgeBetweenExpr(), 10) == True:
                print("There is an edge from {0} to {1}.".format(i,j))


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
    # a, b, c = map(bddvar, 'abc')
    # f = a & b | a & c | b & c
    # graph_BDD(f, "img/test.gv")


if __name__ == '__main__':
    main()
