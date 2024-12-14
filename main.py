from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scores.db'
db = SQLAlchemy(app)

class UserScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)

    def __init__(self, score):
        self.score = score

@app.route("/", methods=["GET", "POST"])
def home():
    
    best_score = db.session.query(db.func.max(UserScore.score)).scalar()
    if best_score is None: 
        best_score = 0

    result_message = None
    total_score = 0  

    if request.method == "POST":
        
        db.session.query(UserScore).delete()
        db.session.commit()

        q1_answer = request.form.get("q1", "")
        q2_answer = request.form.get("q2", "")
        q3_answer = request.form.get("q3", "")
        q4_answer = request.form.get("q4", "")

        if "YOLO" in q1_answer.upper(): 
            total_score += 25
        if q2_answer == "option1":  
            total_score += 25
        if q3_answer == "option1":  
            total_score += 25
        if "nltk" in q4_answer.lower(): 
            total_score += 25

        new_score = UserScore(total_score)
        db.session.add(new_score)
        db.session.commit()

        best_score = db.session.query(db.func.max(UserScore.score)).scalar()

        if total_score >= 75:
            result_message = "Başarılı"
        else:
            result_message = "Başarısız"

    return render_template("index.html", best_score=best_score, result_message=result_message, total_score=total_score)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)