import random
import fastapi
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import networkx as nx
import json
import numpy as np
from pydantic import BaseModel

router = fastapi.APIRouter(tags=["qubo"])
templates = Jinja2Templates(directory="app/templates")

# TODO change "bps" to the abbreviation of the use case you're implementing


class Edge(BaseModel):
    from_city: str
    to_city: str
    weight: float


class GraphData(BaseModel):
    nodes: list[str]
    edges: list[Edge]


# USE CASE DOCUMENTATION
# Here we set the URL under which the template will be shown
# BPS DESCRIPTION
@router.get("/", response_class=HTMLResponse)
async def documentation(request: fastapi.Request) -> HTMLResponse:
    context = {"request": request}
    return templates.TemplateResponse("description.html", context)


# BPS DESCRIPTION
@router.get("/code", response_class=HTMLResponse)
async def documentation(request: fastapi.Request) -> HTMLResponse:
    context = {"request": request}
    return templates.TemplateResponse("traveling-salesperson-problem.html", context)


# PLATFORM IFRAME MOCKUP LOCAL DEVELOPEMENT
# for testing communication between iframe and platform in local development(temporary)
@router.get("/platform-local", response_class=HTMLResponse)
def platform_mockup(request: fastapi.Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "platform_mockup.html",
        {"request": request, "iframe_url": "http://localhost:8000"},
    )


# PLATFORM IFRAME MOCKUP STAGING
# for testing communication between iframe and platform in staging environment(temporary)
@router.get("/platform-staging", response_class=HTMLResponse)
def platform_mockup(request: fastapi.Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "platform_mockup.html",
        {"request": request, "iframe_url": "https://qucun-bps-app.azurewebsites.net"},
    )

# USE CASE SOLUTION VISUALIZATION
@router.post("/tsp/solution")
def solution(request: fastapi.Request, solution: dict = fastapi.Body()) -> HTMLResponse:
    # matrix = solution["config"]["dist_matrix"]
    # solution_binary = solution["result"]["samples"][0]
    # city_nodes = solution["result"]["city_nodes"][0]
    Graph_Data = json.loads(solution["result"]["graphData"])
    graph_data = GraphData(**Graph_Data)
    # n_nodes=len(matrix)
    # distance_matrix = np.array(matrix)
    # city_rows = np.array(solution_binary).reshape((n_nodes, n_nodes))
    # visit_order = []

    # for i in range(n_nodes):
    #     visit_order.append(np.argmax(city_rows[:, i]))
    # visit_order.append(visit_order[0])

    # total_distance = 0

    # for i in range(len(visit_order) - 1):
    #     total_distance += distance_matrix[visit_order[i]][visit_order[i + 1]]

    G = nx.Graph()
    for edge in graph_data.edges:
        G.add_edge(edge.from_city, edge.to_city, weight=edge.weight)
    for node in graph_data.nodes:
        if node not in G:
            G.add_node(node)
    distance_matrix = nx.to_numpy_array(G, nodelist=graph_data.nodes)
    distance_matrix = np.nan_to_num(distance_matrix, nan=np.max(distance_matrix) * 10)
    city_order = list(graph_data.nodes)
    random.shuffle(city_order)

    total_distance = 0
    for i in range(len(city_order) - 1):
        from_index = graph_data.nodes.index(city_order[i])
        to_index = graph_data.nodes.index(city_order[i + 1])
        total_distance += distance_matrix[from_index][to_index]

    from_index = graph_data.nodes.index(city_order[-1])
    to_index = graph_data.nodes.index(city_order[0])
    total_distance += distance_matrix[from_index][to_index]

    solution = {
        "visit_order": city_order,
        "total_distance": total_distance,
    }

    return solution


# PLATFORM IFRAME MOCKUP
# for testing communication between iframe and platform (temporary)
# just for dev purposes
# @router.get("/platform-dev", response_class=HTMLResponse)
# def platform_mockup(request: fastapi.Request) -> HTMLResponse:
#     return templates.TemplateResponse("platform_mockup.html", {"request": request})
