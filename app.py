import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from gensim.parsing.preprocessing import STOPWORDS
from gensim.utils import simple_preprocess
import gensim
import matplotlib.pyplot as plt
from flask import *
import csv
import mysql.connector
import hashlib
from wtforms import SelectField
from flask_wtf import FlaskForm
import time
from livereload import Server
import pandas as pd
import nltk
from nltk import word_tokenize
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')

acyear = ["Select to continue", "2019-2020",
          "2020-2021", "2021-2022", "2022-2023"]


stop_words = []
app = Flask(__name__)
app.secret_key = "dont tell"

myconn = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="sa_feedback_system"
)


class Form(FlaskForm):
    acyear = SelectField('acyear', choices=[])
    yr = SelectField('year', choices=[])
    dept = SelectField('dept', choices=[])
    course = SelectField('course', choices=[])


@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        pass
    return render_template("index.html")


@app.route("/faculty/login", methods=['GET', 'POST'])
def faculty():
    if request.method == "POST":
        uname = request.form['uname']
        pwd = request.form['pwd']
        curr = myconn.cursor()
        curr.execute(
            """select * from adminlogin where username=%s and password=%s""", (uname, pwd))
        data = curr.fetchall()
        if data:
            session['loggedin'] = True
            return redirect(url_for("create_event"))
        else:
            error = 'Incorrect Credentials'
            return render_template("faculty_login.html", error=error)
    return render_template("faculty_login.html")


@app.route("/faculty/home", methods=["GET", "POST"])
def faculty_home():
    return render_template('faculty_home.html')


@app.route("/faculty/create", methods=["GET", "POST"])
def create_event():
    if not session.get('loggedin'):
        return redirect(url_for('faculty'))
    if request.method == "POST":
        if session['loggedin'] == True:
            academic_year = request.form['acyear']
            student_year = request.form['yr']
            department = request.form['dept']
            course_name = request.form['course']
            event_name = request.form['event_name']
            create_event_time = int(time.time())
            curr = myconn.cursor()
            curr.execute("""insert into feedback(academic_year, current_year, department, course_name, event_name, form_time, form_status) value(%s, %s, %s, %s, %s, %s, %s)""",
                         (academic_year, student_year, department, course_name, event_name, create_event_time, 0))
            myconn.commit()
            success = 'Event Created Successfully'
            form = Form()
            form.acyear.choices = acyear
            return render_template('faculty_create_event.html', success=success, form=form)
        else:
            return redirect(url_for('faculty'))
    form = Form()
    form.acyear.choices = acyear
    return render_template('faculty_create_event.html', form=form)


@app.route('/faculty/event_status', methods=["POST", "GET"])
def event_status():
    if not session.get('loggedin'):
        return redirect(url_for('faculty'))
    curr = myconn.cursor()
    curr.execute("""select * from feedback""")
    feedbacks = curr.fetchall()
    return render_template('faculty_view_event_status.html', feedbacks=feedbacks)


@app.route('/faculty/view_feedbacks', methods=["POST", "GET"])
def view_event():
    if not session.get('loggedin'):
        return redirect(url_for('faculty'))
    if request.method == "POST":
        yr = request.form['year']
        dept = request.form['dept']
        print(yr, dept)
        curr = myconn.cursor()
        curr.execute(
            """select * from feedback where current_year=%s and department=%s""", (yr, dept))
        feedbacks = curr.fetchall()
        print(feedbacks)
        return render_template('faculty_view_feedbacks.html', feedbacks=feedbacks)
    curr = myconn.cursor()
    curr.execute("""select * from feedback""")
    feedbacks = curr.fetchall()
    return render_template('faculty_view_feedbacks.html', feedbacks=feedbacks)


@app.route("/student/login", methods=["POST", "GET"])
def student():
    if request.method == "POST":
        uname = request.form['uname']
        pwd = request.form['pwd']
        curr = myconn.cursor()
        curr.execute(
            """select moodle_id, password from student_details where moodle_id=%s""", (uname,))
        data = curr.fetchall()
        if len(data) != 0:
            pass_hash = hashlib.sha256(pwd.encode('utf-8')).hexdigest()
            if data[0][1] == pass_hash:
                session['student_loggedin'] = True
                session['student_id'] = data[0][0]
                return redirect(url_for('student_home'))
            else:
                error = 'Incorrect Credentials'
                return render_template('student_login.html', error=error)
    return render_template("student_login.html")


@app.route("/student/registration", methods=["GET", "POST"])
def student_registration():
    if request.method == "POST":
        id = request.form['id']
        sname = request.form['sname']
        year = request.form['year']
        department = request.form['department']
        pwd = request.form['pwd']
        cpwd = request.form['cpwd']
        if pwd != cpwd:
            error = "Password Not Matched"
            return render_template('student_registration.html', error=error)
        curr = myconn.cursor()
        curr.execute(
            """select * from student_details where moodle_id=%s""", (id,))
        data = curr.fetchall()
        if len(data) != 0:
            error = "Moodle ID Already Exists"
            return render_template('student_registration.html', error=error)
        else:
            moodle_email_id = id+"@apsit.edu.in"
            pass_hash = hashlib.sha256(pwd.encode('utf-8')).hexdigest()
            curr.execute(
                """insert into student_details(moodle_id, name, year, department, password, moodle_email_id) values(%s,%s,%s,%s,%s,%s)""", (id, sname, year, department, pass_hash, moodle_email_id))
            myconn.commit()
            return redirect(url_for('student'))
    return render_template("student_registration.html")


@app.route("/student/home", methods=["GET", "POST"])
def student_home():
    if not session.get('student_loggedin'):
        return redirect(url_for('student'))
    curr = myconn.cursor()
    curr.execute(
        '''select year, department from student_details where moodle_id=%s''', (session['student_id'],))
    stu_details = curr.fetchall()
    curr.execute('''select * from feedback where current_year=%s and department=%s''',
                 (stu_details[0][0], stu_details[0][1]))
    feedback_forms = curr.fetchall()
    print(feedback_forms)
    curr.execute('''select form_id from registered where moodle_id=%s''',
                 (session['student_id'],))
    already_registered = curr.fetchall()
    registered = []
    for i in already_registered:
        registered.append(i[0])
    return render_template('student_home.html', feedback_forms=feedback_forms, registered=registered)


@app.route("/student/registered", methods=["GET", "POST"])
def student_registered():
    if not session.get('student_loggedin'):
        return redirect(url_for('student'))
    curr = myconn.cursor()
    curr.execute(
        "select feedback.id, feedback.event_name, feedback.course_name, feedback.current_year, feedback.department, registered.review_status from feedback left join registered on feedback.id=registered.form_id where registered.moodle_id=%s", (session['student_id'],))
    data = curr.fetchall()
    print(data)
    return render_template('student_registered.html', data=data)


@app.route("/register_for", methods=["GET", "POST"])
def register_for_event():
    if not session.get('student_loggedin'):
        return redirect(url_for('student'))
    if request.method == "POST":
        moodle_id = session['student_id']
        form_id = request.form['register']
        curr = myconn.cursor()
        curr.execute(
            '''Insert into registered(form_id, moodle_id, review_status) values(%s, %s, %s)''', (form_id, moodle_id, 0))
        myconn.commit()
        return redirect(url_for('student_registered'))


@app.route("/deregister_for", methods=["GET", "POST"])
def deregister_for_event():
    if not session.get('student_loggedin'):
        return redirect(url_for('student'))
    if request.method == "POST":
        moodle_id = session['student_id']
        form_id = request.form['register']
        curr = myconn.cursor()
        curr.execute(
            '''delete from registered where form_id=%s and moodle_id=%s''', (form_id, moodle_id))
        myconn.commit()
        return redirect(url_for('student_home'))


@app.route("/student/givefeedback/<int:id>", methods=["GET", "POST"])
def questions(id):
    if not session.get('student_loggedin'):
        return redirect(url_for('student'))
    if request.method == "POST":
        rank = request.form['rating']
        rank1 = request.form['rating1']
        rank2 = request.form['rating2']
        rank3 = request.form['rating3']
        review = request.form['feedback-comments']
        curr = myconn.cursor()
        curr.execute(
            '''update registered set relatable=%s, useful=%s, helpful=%s, overall=%s, review=%s, review_status=%s where form_id=%s and moodle_id=%s''', (rank, rank1, rank2, rank3, review, 1, id, session['student_id']))
        myconn.commit()
        return redirect(url_for('student_registered'))
    return render_template('student_questionnaire.html', id=id)


@app.route("/change_status", methods=["POST", "GET"])
def change_status():
    if not session.get('loggedin'):
        return redirect(url_for('faculty'))
    if request.method == "POST":
        id = request.form['edit']
        curr = myconn.cursor()
        curr.execute("""
        update feedback
        set form_status=case form_status
        when 0 Then 1
        when 1 then 0
        end
        where id=%s""", (id,))
        myconn.commit()
        return redirect(url_for('event_status'))


@app.route("/delete", methods=["POST", "GET"])
def delete():
    if not session.get('loggedin'):
        return redirect(url_for('faculty'))
    if request.method == "POST":
        id = request.form['delete']
        curr = myconn.cursor()
        curr.execute("""delete from feedback where id=%s""", (id,))
        curr.execute("""delete from registered where form_id=%s""", (id,))
        myconn.commit()
        return redirect(url_for('event_status'))


@app.route("/view/<int:id>", methods=["GET", "POST"])
def view(id):
    if not session.get('loggedin'):
        return redirect(url_for('faculty'))
    if request.method == "POST":
        curr = myconn.cursor()
        curr.execute(
            """select current_year,department,event_name from feedback where id=%s""", (id,))
        data = curr.fetchall()
        curr.execute(
            '''select review from registered where form_id=%s and review_status=%s''', (id, 1))
        feedback_data = curr.fetchall()
        curr.execute(
            '''select avg(relatable), avg(useful), avg(helpful), avg(overall) from registered where form_id=%s and review_status=%s''', (id, 1))
        avgs = curr.fetchall()
        df = []
        df_cleaned = []
        for i in feedback_data:
            df.append(i[0])

        avg = 0
        for i in range(len(avgs[0])):
            avg = avg+int(avgs[0][i])
        avg /= 5

        stop_words = stopwords.words('english')
        stop_words.extend(['from', 'subject', 're', 'edu', 'use'])

        def preprocess(text):
            result = []
            for token in gensim.utils.simple_preprocess(text):
                if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3 and token not in stop_words:
                    result.append(token)
            return result

        for i in range(len(df)):
            df_cleaned.append(preprocess(df[i]))

        df_cleaner = []
        for i in range(len(df_cleaned)):
            df_cleaner.append(" ".join(df_cleaned[i]))

        with open('tfidf.pickle', 'rb') as f:
            tfvect = pickle.load(f)
        df_cleaned = tfvect.transform(df_cleaner)

        print(df_cleaner)
        with open('RFC.pickle', 'rb') as f:
            model = pickle.load(f)
        result = model.predict(df_cleaned)

        result = list(result)
        one = result.count(1)
        minus_one = result.count(-1)
        zero = 2
        print(one, minus_one, zero)

        content = ["Positive", "Neutral", "Negative"]
        gms = [one, zero, minus_one]
        colors = ['green' if x == 'Positive' else 'yellow' if x ==
                  'Neutral' else 'red' for x in content]
        plt.pie(gms, labels=content, autopct="%.2f%%", explode=[
                0, 0, 0.1], shadow=True, colors=colors)
        plt.title("Feedback Sentiment")
        plt.savefig('static/pie_plot.png')
        plt.close()

        plt.bar(content, gms, color=["green", "yellow", "red"], width=0.4)
        plt.xlabel("content")
        plt.ylabel("gms")
        plt.title("FeedbackCount")
        plt.savefig('static/bar_chart.png')
        plt.close()

        return render_template('feedbacks_sentiment.html', feedback_data=feedback_data, avg=avg)


@app.route("/logout")
def logout():
    if session.get('loggedin'):
        session["loggedin"] = False
        return redirect(url_for('faculty'))
    else:
        session['student_loggedin'] = False
        return redirect(url_for('student'))


@app.route('/year')
def year():
    curr = myconn.cursor()
    curr.execute("""select distinct year from courses""")
    year = curr.fetchall()
    year.sort()
    get_year = ["Select to continue"]
    for i in year:
        yearobj = {}
        yearobj['year'] = i
        get_year.append(yearobj)
    return jsonify({'year': get_year})


@app.route('/dept')
def dept():
    curr = myconn.cursor()
    curr.execute("""select distinct department from courses""")
    dept = curr.fetchall()
    dept.sort()
    get_dept = ["Select to continue"]
    for i in dept:
        deptobj = {}
        deptobj['dept'] = i
        get_dept.append(deptobj)
    return jsonify({'dept': get_dept})


@app.route('/course/<get_dept>/<get_year>')
def course(get_dept, get_year):
    curr = myconn.cursor()
    curr.execute(
        """select course_name from courses where department=%s and year=%s""", (get_dept, get_year))
    course = curr.fetchall()
    course.sort()
    get_course = ["Select to continue"]
    for i in course:
        courseobj = {}
        courseobj['course'] = i
        get_course.append(courseobj)
    return jsonify({'course': get_course})


if __name__ == "__main__":
    app.run(debug=True)
