import networkx as nx
from keytotext import pipeline

# Load the pre-trained model
nlp = pipeline("k2t")

# Set decoding parameters
params = {"do_sample": True, "num_beams": 4, "no_repeat_ngram_size": 3, "early_stopping": True}

# Read relations from the text file
relations = []
with open('../data/knowledge_base/Hinduism_knowledge_base.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        if line.startswith("  {"):
            relation = eval(line.strip())
            relations.append(relation)

# Generate sentences using the knowledge graph
graph = nx.Graph()
for relation in relations:
    source = relation['head']
    target = relation['tail']
    predicate = relation['type']
    graph.add_edge(source, target, relation=predicate)

nx.write_graphml(graph, '../data/knowledge_graph/Hinduism_knowledge_graph.graphml')

sentences = []
for edge in graph.edges(data=True):
    source = edge[0]
    target = edge[1]
    predicate = edge[2]['relation']
    keywords = [source, predicate, target]
    print(keywords)

    sentence = nlp(keywords, **params)
    print(sentence)
    sentences.append(sentence)

# Save the generated sentences to a text file
output_file = '../data/sentences/generated_sentences.txt'
with open(output_file, 'a') as file:
    for sentence in sentences:
        file.write(sentence + '\n')

print(f"Generated sentences saved to {output_file}.")
