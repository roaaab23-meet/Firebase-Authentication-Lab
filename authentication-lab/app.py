from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'



firebaseConfig = {
  "apiKey": "AIzaSyAcENw4tbIX7nrTjpkpQXWTCBbWj6IR4nM",
  "authDomain": "authentication-lab-90b38.firebaseapp.com",
  "projectId": "authentication-lab-90b38",
  "storageBucket": "authentication-lab-90b38.appspot.com",
  "messagingSenderId": "552764983814",
  "appId": "1:552764983814:web:17d439f2d039b977d11187",
  "measurementId": "G-GEHY5GKK1L" ,
  "databaseURL" : "https://authentication-lab-90b38-default-rtdb.asia-southeast1.firebasedatabase.app/"
}
firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()
db= firebase.database()




@app.route('/', methods=['GET', 'POST'])
def signin():
    error=""
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        try:
            login_session['user']=auth.sign_in_with_email_and_password(email,password)
            return redirect(url_for('add_tweet'))

        except:
            error="authentication failed"
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error=""
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        try:
            login_session['user']=auth.create_user_with_email_and_password(email,password)
            user={"Email":request.form['Email'], "password":request.form['[password'], "full name":erquest.form['full_name'],"username":request.form['username'], "bio":request.form['bio']}
            db.child("user").child(login_session['user']['localId']).set(user) 
            return redirect(url_for('home'))

        except:
            error="authentication failed"
    return render_template("signup.html")


@app.route('/signout', methods=['GET', 'POST'])
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method=='POST':
        tweet={"title":request.form['title'],"text":request.form['text'], "uid":login_session['user']['localId']}
        db.child("Tweets").push(tweet)
    return render_template("add_tweet.html")


@app.route('/all_tweets', methods=['GET', 'POST'])
def tweets():
    if request.method=='GET':
        tweet_dict = db.child("Tweets").get().val()
    return render_template("tweets.html", tweet_dict=tweet_dict)


if __name__ == '__main__':
    app.run(debug=True)