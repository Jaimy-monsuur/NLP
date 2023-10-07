import wikipediaapi
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import math


# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("Babelscape/rebel-large")
model = AutoModelForSeq2SeqLM.from_pretrained("Babelscape/rebel-large")


def extract_relations_from_model_output(text):
    relations = []
    relation, subject, relation, object_ = '', '', '', ''
    text = text.strip()
    current = 'x'
    text_replaced = text.replace("<s>", "").replace("<pad>", "").replace("</s>", "")
    for token in text_replaced.split():
        if token == "<triplet>":
            current = 't'
            if relation != '':
                relations.append({
                    'head': subject.strip(),
                    'type': relation.strip(),
                    'tail': object_.strip()
                })
                relation = ''
            subject = ''
        elif token == "<subj>":
            current = 's'
            if relation != '':
                relations.append({
                    'head': subject.strip(),
                    'type': relation.strip(),
                    'tail': object_.strip()
                })
            object_ = ''
        elif token == "<obj>":
            current = 'o'
            relation = ''
        else:
            if current == 't':
                subject += ' ' + token
            elif current == 's':
                object_ += ' ' + token
            elif current == 'o':
                relation += ' ' + token
    if subject != '' and relation != '' and object_ != '':
        relations.append({
            'head': subject.strip(),
            'type': relation.strip(),
            'tail': object_.strip()
        })
    return relations


class knowledge_base():
    def __init__(self):
        self.relations = []

    def are_relations_equal(self, r1, r2):
        return all(r1[attr] == r2[attr] for attr in ["head", "type", "tail"])

    def exists_relation(self, r1):
        return any(self.are_relations_equal(r1, r2) for r2 in self.relations)

    def add_relation(self, r):
        if not self.exists_relation(r):
            self.relations.append(r)

    def print(self):
        print("Relations:")
        for r in self.relations:
            print(f"  {r}")


def from_text_to_kb(text, verbose=False):
    kb = knowledge_base()

    # Tokenizer text
    model_inputs = tokenizer(text, max_length=1020, padding=True, truncation=True,
                             return_tensors='pt')
    if verbose:
        print(f"Num tokens: {len(model_inputs['input_ids'][0])}")

    # Generate
    gen_kwargs = {
        "max_length": 216,
        "length_penalty": 0,
        "num_beams": 3,
        "num_return_sequences": 3
    }
    generated_tokens = model.generate(
        **model_inputs,
        **gen_kwargs,
    )
    decoded_preds = tokenizer.batch_decode(generated_tokens, skip_special_tokens=False)

    # create kb
    for sentence_pred in decoded_preds:
        relations = extract_relations_from_model_output(sentence_pred)
        for r in relations:
            kb.add_relation(r)

    return kb


def split_text_into_chunks(text, chunk_size):
    chunks = []
    num_chunks = math.ceil(len(text) / chunk_size)
    for i in range(num_chunks):
        start_idx = i * chunk_size
        end_idx = (i + 1) * chunk_size
        chunk = text[start_idx:end_idx]
        chunks.append(chunk)
    return chunks


def save_kb_to_file(kb, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for r in kb.relations:
            file.write(f"  {r}\n")


wiki_wiki = wikipediaapi.Wikipedia('en')
page_py = wiki_wiki.page('Hinduism')
text_py = page_py.text

chunk_size = 4020
text_chunks = split_text_into_chunks(text_py, chunk_size)

kb = knowledge_base()

for chunk in text_chunks:
    kb_chunk = from_text_to_kb(chunk, verbose=True)
    kb.relations.extend(kb_chunk.relations)

kb.print()
save_kb_to_file(kb, '../data/knowledge_base/Hinduism_knowledge_base.txt')
