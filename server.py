from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk

# Download NLTK data 
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
    # Tokenization
    tokens = word_tokenize(text)
    # Removing stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word.lower() for word in tokens if word.lower() not in stop_words]
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
    return lemmatized_tokens


def get_similar_question_from_database(input_question):
    input_question_tokens = preprocess_text(input_question)

    # Retrieve all questions from the database
    all_questions = QA.query.all()

    # Preprocess database questions
    database_question_tokens = [preprocess_text (qa_pair.Ques) for qa_pair in all_questions]

    # Manual similarity check (replace with your desired logic)
    similar_question_answer_pairs = []
    for qa, db_tokens in zip(all_questions, database_question_tokens):
        # Example similarity check (replace with more sophisticated logic)
        if any(word in input_question_tokens for word in db_tokens):
                similar_question_answer_pairs.append(qa.Ans)

        return {'similar_pairs': similar_question_answer_pairs}

#API Route
@app.route("/api")
def render_similar_question_answer_pairs():
    # if request.method == 'POST':
    #     input_question = request.POST['question']
    # else:
    input_question = "whats"

    similar_question_answer_pairs = get_similar_question_from_database(input_question)
    return jsonify(similar_question_answer_pairs)




# def get_qa_data():
#     try:
#         # Query all records from the QA table
#         qa_records = QA.query.all()

#         # Initialize an empty list to store the results
#         qa_data = []

#         # Iterate over the records and extract the necessary information
#         for record in qa_records:
#             qa_data.append({
#                 'id': record.id,
#                 'question': record.Ques,
#                 'answer': record.Ans
#             })

#         return qa_data
#     except Exception as e:
#         # Handle any exceptions, such as database errors
#         print(f"An error occurred: {e}")
#         return None

# def submit():
#   fname= request.form['fname']
#   lname=request.form['lname']
#   pet=request.form['pets']

#   student=Student(fname,lname,pet)
#   db.session.add(student)
#   db.session.commit()

  #fetch a certain student2
#   studentResult=db.session.query(QA).filter(QA.id==1)
#   for result in studentResult:
#     print(result.Ques)

#   return render_template('success.html', data=fname)
  

@app.route("/members")
# def get_members():
#     members = ['members1', 'members2', 'members3']
#     return {'members': members}, 200, {'Content-Type': 'application/json'}

def menbers():
    return {'members':['members1','members2','members3']}



if __name__=="__main__":
    app.run(debug=True)
