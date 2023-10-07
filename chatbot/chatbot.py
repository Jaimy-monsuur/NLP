import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Step 2: Load the text file
with open('data/sentences/cleaned_sentences.txt', 'r') as file:
    responses = file.readlines()

# Step 3: Preprocess the data
preprocessed_responses = [' '.join(nltk.word_tokenize(response.lower())) for response in responses]

# Step 4: Vectorize the data with TF-IDF weighting
vectorizer = TfidfVectorizer()
response_vectors = vectorizer.fit_transform(preprocessed_responses)

while True:
    # Step 5: Process the input question
    input_question = input("User: ")
    preprocessed_question = ' '.join(nltk.word_tokenize(input_question.lower()))
    question_vector = vectorizer.transform([preprocessed_question])

    # Step 6: Calculate similarity
    similarity_scores = cosine_similarity(response_vectors, question_vector)

    # Step 7: Retrieve the best response
    best_response_index = similarity_scores.argmax()
    best_response = responses[best_response_index].strip()

    print("Bot: " + best_response)
