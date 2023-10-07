# Chatbot for NLP Assignment 
# student: jaimy monsuur 668040

## python version: 3.10

This repository contains a chatbot designed for the NLP assignment. The chatbot is capable of answering simple questions related to Gandhi, India, and Hinduism. It utilizes a knowledge base generated using the Babelscape/rebel-large models, which are stored in the `Knowledge_base` directory. Additionally, the knowledge base is represented as a graph in the form of `.graphml` files, which can be found in the `Knowledge_graph` directory. The `Sentences` directory contains both the generated and cleaned sentences used by the chatbot.

## Data Generation

- `Knowledge_graph.py`: This script represents the initial attempt to generate a knowledge graph from a Wikipedia page. It is based on code from the lectures and serves as the foundation for building the knowledge base.
- `Knowledge_base.py`: This script generates a knowledge base similar to the knowledge graph. It utilizes imported transformer models, specifically the Babelscape/rebel-large model, to generate the knowledge base.
- `keys_to_text.py`: This script generates sentences from the knowledge base or knowledge graph. It utilizes the imported keytotext model for this purpose.

## Image Placeholders

To provide a visual representation of the project, the following image placeholders are available:

- Chatbot example 1: ![Chatbot example 1](chatbot/img/Screenshot%202023-06-13%20102247.png)
- Chatbot example 2: ![Chatbot example 2](chatbot/img/Screenshot%202023-06-13%20102617.png)
- Chatbot example 3: ![Chatbot example 3](chatbot/img/Screenshot%202023-06-13%20103030.png)


## Usage

To use the chatbot, follow these steps:

1. Install the required dependencies mentioned in the `requirements.txt` file.
2. For running the chatbot you can skip step 3 and 4
3. Execute the `Knowledge_base.py` script to generate the knowledge base using the transformer models.
4. Utilize the `keys_to_text.py` script to generate sentences from the knowledge base or knowledge graph.
5. Run the `chatbot.py`. Interact with the chatbot by asking questions about Gandhi, India, or Hinduism.


