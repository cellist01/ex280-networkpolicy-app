from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.sql import text
import threading
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@mysql.database.svc.cluster.local:3306/userdb'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    family_relation = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)

# 테이블 생성
with app.app_context():
    db.create_all()

def check_db_connection():
    while True:
        try:
            with app.app_context():
                db.session.execute(text('SELECT 1'))
                print("Database connection is active.")
        except Exception as e:
            print(f"Database connection error: {str(e)}")
        time.sleep(2)  # 2초마다 반복

# 백그라운드 스레드 시작
check_thread = threading.Thread(target=check_db_connection)
check_thread.daemon = True
check_thread.start()

@app.route('/')
def index():
    users = User.query.all()  # 사용자 정보를 모두 가져옴
    return render_template('index.html', users=users)  # 사용자 정보를 index.html에 전달

@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        birth_date = datetime.strptime(request.form['birth_date'], '%Y-%m-%d').date()
        family_relation = request.form['family_relation']
        address = request.form['address']

        new_user = User(username=username, email=email, birth_date=birth_date, family_relation=family_relation, address=address)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

