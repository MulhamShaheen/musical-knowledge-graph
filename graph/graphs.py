from typing import List, Tuple

import pandas as pd
from rdflib import Graph, Namespace, RDF, RDFS, OWL

from graph.ontologies import Ontology
from graph.utils import clean_string_for_graph


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
        self.individuals_set = set()
        self.titles_map = {c : {} for c in self.ontology.classes}

    def _init_ontology_triplets(self):
        for class_name in self.ontology.classes:
            self.add_triplet(class_name)
        for prop in self.ontology.properties.keys():
            self.add_triplet(prop)

    def _to_rdf_objets(self, entity):
        if entity in self.rfd_dict.keys():
            return self.rfd_dict[entity]
        return self.ex[entity]


    def load_graph_from_file(self, file_name: str, format="turtle"):
        self.graph.parse(file_name, format=format)

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
        if individual in self.individuals_set:
            print(f"Individual {individual} already exists")
        else:
            self.graph.add((self.ex[individual], RDF.type, self.ex[class_name]))
        for prop in properties:
            self.graph.add((self.ex[individual], self.ex[prop[0]], self.ex[prop[1]]))
        self.individuals_set.add(individual)

    def serialize(self, file_name: str, format="turtle"):
        self.graph.serialize(file_name, format=format)

    def load_dataset(self, csv_file: str, main_class_col: str):
        df = pd.read_csv(csv_file)
        props = {p_name: p["domain"].lower() for p_name, p in self.ontology.properties.items() if "domain" in p}
        for _, row in df.iterrows():
            for class_name in self.ontology.classes:
                individual = clean_string_for_graph(str(row[class_name.lower()]))
                if class_name.lower() in row:
                    if main_class_col == class_name.lower():
                        self.add_individual(individual,
                                            [(prop_name, clean_string_for_graph(str(row[domain]))) for prop_name, domain in props.items()
                                             if domain != class_name.lower()],
                                            class_name)
                    else:
                        self.add_individual(individual, [], class_name)


