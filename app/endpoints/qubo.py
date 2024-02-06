import fastapi
from pydantic import BaseModel
from app.gen_qubo import gen_qubo_matrix
import networkx as nx
import numpy as np
import random

router = fastapi.APIRouter(tags=["qubo"])

# Endpoints regarding QUBOs and without template rendering go here

class Edge(BaseModel):
    from_city: str
    to_city: str
    weight: float

class GraphData(BaseModel):
    nodes: list[str]
    edges: list[Edge]


# TSP QUBO example
@router.post("/api/qubo", response_model=dict)
async def get_qubo(graph_data: GraphData):

    G = nx.Graph()
    for edge in graph_data.edges:
        G.add_edge(edge.from_city, edge.to_city, weight=edge.weight)


    for node in graph_data.nodes:
        if node not in G:
            G.add_node(node)


    distance_matrix = nx.to_numpy_array(G, nodelist=graph_data.nodes)

 
    distance_matrix = np.nan_to_num(distance_matrix, nan=np.max(distance_matrix)*10)

    
    qubo = gen_qubo_matrix(distance_matrix.tolist())

    # city_order = list(graph_data.nodes)
    # random.shuffle(city_order)

    # total_distance = 0
    # for i in range(len(city_order) - 1):
    #     from_index = graph_data.nodes.index(city_order[i])
    #     to_index = graph_data.nodes.index(city_order[i + 1])
    #     total_distance += distance_matrix[from_index][to_index]

    
    # from_index = graph_data.nodes.index(city_order[-1])
    # to_index = graph_data.nodes.index(city_order[0])
    # total_distance += distance_matrix[from_index][to_index]

    return {"qubo": qubo.tolist(), "dist_matrix": distance_matrix.tolist()}
