# Symbolic Graph Search

## Usage
Set up environment on Ubuntu.
```
source ./scripts/setup.sh
```
Activate python virtual environment.
```
source ./venv/bin/activate
```
Ensure running ```which python``` prints the same as ```pwd``` + '/venv/bin/python'.

Next, install dependencies.
```
pip install -r requirements.txt
```
Run program.
```
python project.py
```
View any graphs produced in ```img``` directory.
Lastly, deactivate environment.
```
deactivate
```

## Description
This program solves a very abstract graph search problem.

Let S be an ordered sequence of numbers, starting from some offset, and ending at offset + numberOfNodes. The sequence is evenly spaced in increments of one, although the program will work even if this constraint is not guaranteed. There are no repeats in S, so S is a set. Let the elements of S represent nodes in some raph G. Given two numbers i and j in set S, there is an edge from node i to node j in G iff (i+3)%MODULO == j%MODULO or (i+7)%MODULO == j%MODULO, where MODULO is some integer.

The question at hand is: can every node i reach every other node j in graph G?

The approach to solving this problem is to encode the graph into bits using a boolean expression. We can then easily convert the boolean expression into a boolean decision diagram (another graph G'). If the indegree of output 0 is 0 in G' (see ```img/transitive_closure.gv.pdf```), then every node i can reach every other node j in graph G. It's that simple. Solving a problem indirectly like this can often prove simpler and more efficient than trying to solve it directly.