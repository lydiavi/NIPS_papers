import networkx as nx
from IPython.lib.display import IFrame
from pyvis.network import Network


def pyvis_graph(G: nx.Graph, name: str) -> IFrame | None:
    """Simplify pyvis graphing.

    Args:
        G (nx.Graph): _description_
        name (str): _description_

    Returns:
        IFrame | None: _description_
    """
    g = Network(notebook=True, cdn_resources="in_line")
    g.toggle_hide_edges_on_drag(False)
    g.from_nx(G)
    return g.show(f"{name}.html")
