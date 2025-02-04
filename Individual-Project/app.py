from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

config = {
  "apiKey": "AIzaSyCJ9FAqbKqTXue0xRvC_y6BBLwvBHA66sI",
  "authDomain": "ppro-831ea.firebaseapp.com",
  "databaseURL": "https://ppro-831ea-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "ppro-831ea",
  "storageBucket": "ppro-831ea.appspot.com",
  "messagingSenderId": "586507247559",
  "appId": "1:586507247559:web:99cb4252377bdf222643e2",
  "databaseURL": "https://ppro-831ea-default-rtdb.europe-west1.firebasedatabase.app/"
};

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app  = Flask(__name__)

app.config['SECRET_KEY'] = 'passcode'
#Code goes below here

@app.route('/', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		password = request.form['password']
		email = request.form['email']
		try:
			login_session['user'] = auth.create_user_with_email_and_password(email, password)
		except:
			return render_template('signup.html')
		return redirect(url_for('home'))
	return render_template('signup.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
	flag = True
	if request.method == 'POST':
		topic = request.form['topic']
		topics =  db.child("topics").get().val()
		if topics is None:
			pass
		else:
			for i in topics:
				if topic == topics[i]:
					flag = False
		if flag:
			db.child("topics").child(topic).set("")
			topics = db.child("topics").get().val()
		return render_template('home.html', topics=topics)
	topics = db.child("topics").get().val()
	if topics is None:
		topics = {}
	return render_template('home.html', topics=topics)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
	if request.method == 'POST':
		password = request.form['password']
		email = request.form['email']
		try:
			login_session['user'] = auth.sign_in_with_email_and_password(email, password)
		except:
			return render_template('signin.html')		
		return redirect(url_for('home'))
	return render_template('signin.html')

@app.route('/topics/<string:topic>', methods=['GET', 'POST'])
def topic(topic):
	if request.method == 'POST':
		thought = request.form['thought']
		db.child("topics").child(topic).push(thought)
		thoughts = db.child("topics").child(topic).get().val()
		return render_template('topic.html', topic=topic, thoughts=thoughts)
	thoughts = db.child("topics").child(topic).get().val()
	return render_template('topic.html', topic=topic, thoughts=thoughts)

#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)