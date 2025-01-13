from typing import List, Tuple

from rdflib import Graph, Namespace, RDF, RDFS, OWL

from graph.ontologies import Ontology


class GraphGenerator:

    def __init__(self, ontology: Ontology, namespace: str):
        self.ontology = ontology
        self.graph = Graph()
        self.ex = Namespace(namespace)
        self.graph.bind("music", self.ex)
        self.rfd_dict = {
            "DatatypeProperty": OWL.DatatypeProperty,
            "ObjectProperty": OWL.ObjectProperty,
            "type": RDF.type,
            "domain": RDFS.domain,
            "class": OWL.Class,
        }
        self._init_ontology_triplets()

    def _init_ontology_triplets(self):
        for class_name in self.ontology.classes:
            self.add_triplet(class_name)
        for prop in self.ontology.properties.keys():
            self.add_triplet(prop)

    def _to_rdf_objets(self, entity):
        if entity in self.rfd_dict.keys():
            return self.rfd_dict[entity]
        return self.ex[entity]

    def add_to_graph(self, triplet):
        triplet = [self._to_rdf_objets(t) for t in triplet]
        self.graph.add(tuple(triplet))

    def add_triplet(self, subject):
        if subject in self.ontology.classes:
            g_object = "Class"
            predicate = "type"
            self.add_to_graph((subject, predicate, g_object))

        elif subject in self.ontology.properties.keys():
            for key, value in self.ontology.properties[subject].items():
                self.add_to_graph((subject, key, value))

    def add_individual(self, individual, properties: List[Tuple], class_name):
        if class_name not in self.ontology.classes:
            print(f"Class {class_name} not found in the ontology")
            return
        self.graph.add((self.ex[individual], RDF.type, self.ex[class_name]))
        for prop in properties:
            self.graph.add((self.ex[individual], self.ex[prop[0]], self.ex[prop[1]]))

    def serialize(self, file_name: str):
        self.graph.serialize(file_name, format="turtle")
