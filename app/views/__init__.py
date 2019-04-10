from app.views.view import app
from flask import render_template

@app.route('/index.html', methods=['GET'])
def homes():
    return render_template('index.html')

@app.route('/signup.html', methods=['GET'])
def register_page():
    return render_template('signup.html')

@app.route('/addmembers.html', methods=['GET'])
def addmembers_page():
    return render_template('addmembers.html')

@app.route('/delete_member.html', methods=['GET'])
def delete_members_page():
    return render_template('delete_member.html')

@app.route('/drafts.html', methods=['GET'])
def drafts_page():
    return render_template('drafts.html')

@app.route('/editname.html', methods=['GET'])
def editname_page():
    return render_template('editname.html')

@app.route('/group.html', methods=['GET'])
def group_page():
    return render_template('group.html')

@app.route('/groupmail.html', methods=['GET'])
def groupmail_page():
    return render_template('groupmail.html')

@app.route('/inbox.html', methods=['GET'])
def inbox_page():
    return render_template('inbox.html')

@app.route('/mygroups.html', methods=['GET'])
def mygroups_page():
    return render_template('mygroups.html')

@app.route('/new.html', methods=['GET'])
def new_page():
    return render_template('new.html')

@app.route('/password_reset.html', methods=['GET'])
def password_reset_page():
    return render_template('password_reset.html')

@app.route('/sent.html', methods=['GET'])
def sent_page():
    return render_template('sent.html')