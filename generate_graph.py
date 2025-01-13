from graph.ontologies import Ontology
from graph.graphs import GraphGenerator

ontology = Ontology(
    properties={
        "by": {"type": "DatatypeProperty", "domain": "Artist"},
        "inAlbum": {"type": "DatatypeProperty", "domain": "Album"},
        "inGenre": {"type": "DatatypeProperty", "domain": "Genre"},
    },
    classes=["Song", "Artist", "Album", "Genre"]
)

generator = GraphGenerator(ontology, "music")
generator.add_individual("song1", [("by", "artist1"), ("inAlbum", "album1"), ("inGenre", "genre1")], "Song")

generator.serialize("music.ttl")