from pipeline_allgather import optimal_pipeline_spanning_trees, spanning_trees_to_xml
from to_xml import construct_algo_allgather, construct_algo_allgather
from topologies import arbitrary, a100_topology
from to_xml import construct_algo_allreduce
import xml.etree.ElementTree as ET
from xml.dom import minidom
import sys
from pathlib import PurePath

print(sys.argv[1])
G, gpus = arbitrary(sys.argv[1])
# G, gpus = a100_topology(1)
(U, k), (Ts, Cs) = optimal_pipeline_spanning_trees(G, compute_nodes=gpus)
print(f"Suggested Overlap: {k}")

tree_xml = spanning_trees_to_xml(Ts, Cs, k)
with open(str(PurePath(sys.argv[1]).stem) + ".xml", "w") as f:
    f.write(tree_xml)

'''
nodes = list(range(G.number_of_nodes()))
if sys.argv[2] == "ar":
    algo = construct_algo_allreduce(Ts, Cs, k, nodes, ninstance=1)
elif sys.argv[2] == "ag":
    algo = construct_algo_allgather(Ts, Cs, k, nodes, ninstance=1)
else:
    print("ar or ag?")
    exit()
s = ET.tostring(algo, 'utf-8')
s = minidom.parseString(s)
s = s.toprettyxml(indent="  ")
s = '\n'.join(s.split('\n')[1:])
print(s)
'''
