from __future__ import annotations

from collections import defaultdict

from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
from rdflib.graph import Graph, _ObjectType, _PredicateType, _SubjectType
from rdflib.namespace import RDF, VOID
from rdflib.term import IdentifiedNode, Literal, URIRef

from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, OWL
import networkx as nx

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("WebAgg")
# Create a graph
g = Graph()

# Define namespaces
EX = Namespace("music")
g.bind("music", EX)

# Define classes
g.add((EX.Song, RDF.type, OWL.Class))
g.add((EX.Artist, RDF.type, OWL.Class))

# Define properties
g.add((EX.by, RDF.type, OWL.DatatypeProperty))
g.add((EX.by, RDFS.domain, EX.Artist))

# Add individuals (instances)
song = EX["Тянет"]
artist = EX["Zoloto"]
g.add((song, RDF.type, EX.Song))
g.add((artist, RDF.type, EX.Artist))
g.add((song, EX.by, EX["Zoloto"]))


serialized_graph = g.serialize(format='turtle')

# Write to a file
with open('ontology.ttl', 'w') as f:
    f.write(serialized_graph)

print("Ontology created and populated. Saved as 'ontology.ttl'")

G = rdflib_to_networkx_multidigraph(g)

pos = nx.spring_layout(G, scale=2)
edge_labels = nx.get_edge_attributes(G, 'r')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
nx.draw(G, with_labels=True)

plt.show()

