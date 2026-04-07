from pipeline_allgather import OptimalBranchingsAlgo
import networkx as nx
import sys
from pathlib import Path
import json

def ingest_emap(fname: str):
        G = nx.DiGraph()
        with open(fname, mode='r') as f_raw:
                f = f_raw.read()
                for from_node, line in enumerate(f.split("\n")):
                        from_ident = int(from_node)
                        for to_node, deg in enumerate(line.split()):
                                deg_n = int(deg)
                                if deg_n != 0:
                                        to_ident = int(to_node)
                                        G.add_edge(from_ident, to_ident, capacity=deg_n)
        return G

def kill_switch(topo, compute_nodes: list):
        algo = OptimalBranchingsAlgo(topo, compute_nodes=compute_nodes)
        U, k = algo.binary_search()
        print(f"Suggested overlap: {k}")
        print("Removing switch...")
        return algo.removeSwitchNodes(U, k)

def dump_map(fname: str, topo, recover_dict: dict):
        adj_mat = nx.adjacency_matrix(topo, nodelist=list(range(0, topo.number_of_nodes())), weight="capacity")
        adj_mat = adj_mat.toarray()
        with open(fname + ".map", mode="w") as f:
                for rows in adj_mat:
                        for item in rows:
                                f.write(f"{item} ")
                        f.write("\n")

        recover_list = list()
        for edge in recover_dict.keys():
                item = recover_dict[edge]
                json_item = dict()
                json_item["switch"] = list(item.keys())[0]
                json_item["flow"] = list(item.values())[0]
                json_item["edge"] = edge
                recover_list.append(json_item)
        with open(fname + ".json", mode="w") as f:
                f.write(json.dumps(recover_list))
        print(f"Wrote switchless map to {fname}.map")
        print(f"Wrote recovery dict to {fname}.json")

def main():
        if len(sys.argv) != 3:
                print("Usage: killswitch.py <emap file> <switch start id>")
        print(f"Killswitch for {sys.argv[1]}, compute is [0, {sys.argv[2]})")
        topo = ingest_emap(sys.argv[1])
        compute_nodes = list(range(0, int(sys.argv[2])))
        topo, recover = kill_switch(topo, compute_nodes)
        dump_map(Path(sys.argv[1]).stem, topo, recover)

if __name__ == "__main__":
        main()
