import textacy
import wikipediaapi
import spacy
from matplotlib import pyplot as plt
import networkx as nx
import pandas as pd
from nltk import WordNetLemmatizer

# Load English tokenizer, tagger, parser and NER
nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('coreferee')  # This is new
wiki_wiki = wikipediaapi.Wikipedia('en')


def draw_kg_for_most_common(txt, most_common_index=0):

    # from text to a list of sentences
    lst_docs = [sent for sent in nlp(txt).sents]
    print("total sentences:", len(lst_docs))

    ## extract entities and relations
    dic = {"id": [], "text": [], "entity": [], "relation": [], "object": []}

    def coref(parts):
        for part in parts:
            subj_ref = doc._.coref_chains.resolve(part)
            if subj_ref:
                for x in subj_ref:
                    yield x
            else:
                yield part

    for i, sentence in enumerate(lst_docs):
        for sent in textacy.extract.subject_verb_object_triples(sentence):
            subj = " ".join(map(str, coref(sent.subject)))
            obj = " ".join(map(str, coref(sent.object)))
            relation = " ".join(map(str, sent.verb))

            dic["id"].append(i)
            dic["text"].append(sentence.text)
            dic["entity"].append(subj)
            dic["object"].append(obj)
            dic["relation"].append(relation)

    ## create dataframe
    dtf = pd.DataFrame(dic)

    ## filter
    f = dtf["entity"].value_counts().head().index[most_common_index]
    tmp = dtf[(dtf["entity"] == f) | (dtf["object"] == f)]

    ## create small graph
    G = nx.from_pandas_edgelist(tmp, source="entity", target="object",
                                edge_attr="relation",
                                create_using=nx.DiGraph())

    # Save the graph as a GraphML file
    nx.write_graphml(G, '../chatbot/knowledge_graph.graphml')

    ## plot
    plt.figure(figsize=(15, 10))
    pos = nx.spring_layout(G, k=1)

    node_color = ["red" if node == f else "skyblue" for node in G.nodes]
    edge_color = ["red" if edge[0] == f else "black" for edge in G.edges]

    nx.draw(G, pos=pos, with_labels=True, node_color=node_color,
            edge_color=edge_color,
            node_size=2000, node_shape="o")

    nx.draw_networkx_edge_labels(G, pos=pos, label_pos=0.5,
                                 edge_labels=nx.get_edge_attributes(G, 'relation'),
                                 font_size=12, font_color='black', alpha=0.6)
    plt.show()


page_py = wiki_wiki.page('Mahatma_Gandhi')
text_py = page_py.text

doc = nlp(text_py)
draw_kg_for_most_common(text_py)
