from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import psycopg2

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:1234@localhost/QA'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class QA(db.Model):
    __tablename__='QA'
    id=db.Column(db.Integer,primary_key=True)
    Ques=db.Column(db.String(1000))
    Ans=db.Column(db.String(1000))

    def __init__(self,Ques,Ans):
        self.Ques=Ques
        self.Ans=Ans



def preprocess_text(text):
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word.lower() for word in tokens if word.lower() not in stop_words]
    # Lemmatize words
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
    # Join the tokens back into single string
    preprocessed_text = ' '.join(lemmatized_tokens)
    return preprocessed_text



def find_most_similar_question_answer(input_question):
    # Preprocess the input question
    preprocessed_input = preprocess_text(input_question)
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname='QA',
        user='postgres',
        password='1234',
        host='localhost',
        
    )
    cur = conn.cursor()
 
    qa_pairs=QA.query.all()
    
    # Create a list to store preprocessed questions
    preprocessed_questions = []
    for qa_pair in qa_pairs:
        preprocessed_question = preprocess_text(qa_pair.Ques)
        preprocessed_questions.append(preprocessed_question)
    
    # Add input question to the list of preprocessed questions
    preprocessed_questions.append(preprocessed_input)
    
    # Convert preprocessed questions into TF-IDF vectors
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(preprocessed_questions)
    
    # Calculate cosine similarity between the input question and all questions in the database
    similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    
    # Find the index of the most similar question
    most_similar_index = similarities.argmax()
    
    # Retrieve the most similar question-answer pair
    most_similar_question = qa_pairs[most_similar_index].Ques
    most_similar_answer = qa_pairs[most_similar_index].Ans
    
    # Close the database connection
    cur.close()
    conn.close()
    
    return most_similar_question, most_similar_answer


@app.route('/api', methods=['POST'])
  
def find_similar_question_answer():
    input_question = request.json['question']
    most_similar_question, most_similar_answer = find_most_similar_question_answer(input_question)
    ques_pairs = {
        'most_similar_question': most_similar_question,
        'most_similar_answer': most_similar_answer
    }
    return jsonify(ques_pairs)



if __name__=="__main__":
    app.run(debug=True)
