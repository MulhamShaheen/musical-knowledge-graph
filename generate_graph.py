from graph.ontologies import Ontology
from graph.graphs import GraphGenerator

ontology = Ontology(
    properties={
        "by": {"type": "DatatypeProperty", "domain": "Artist"},
        "inAlbum": {"type": "DatatypeProperty", "domain": "Album"},
        "inGenre": {"type": "DatatypeProperty", "domain": "Genre"},
        "inPlaylist": {"type": "DatatypeProperty", "domain": "Playlist"},
    },
    classes=["Song", "Artist", "Album", "Genre"]
)

generator = GraphGenerator(ontology, "music:")
generator.add_individual("song1", [("by", "artist1"), ("inAlbum", "album1"), ("inGenre", "genre1")], "Song")

generator.load_dataset("data/yandex.csv", "song")
generator.serialize("music1.owl", format="xml")
generator.load_graph_from_file("music1.owl", format="xml")
generator.save_triplets("triplets.csv")
