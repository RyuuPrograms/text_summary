
from flask import Flask, render_template, request, session, redirect, url_for
from numpy import conj
from jinja_filters import my_enumerate
from text_summary import summarizer
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "your-secret-key"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'text_summary'

mysql = MySQL(app)

def fetch_document_details(user_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT document_title, document_text FROM user_documents WHERE user_id = %s", (user_id,))
        documents = cursor.fetchall()  
        cursor.close()
        if documents:
            return documents
        else:
            return None
    except Exception as e:
        print("An error occurred while fetching document details:", e)
        return None
    
@app.route('/view_document', methods=['POST'])
def view_document():
    if 'username' in session:
        user_id = session['user_id']
        documents = fetch_document_details(user_id)
        if documents:
            return render_template('Recent_Document1.html', documents=documents)
        else:
            app.logger.error("No documents found for the user")
            return "No documents found for the user."
    else:
        return redirect(url_for('login'))
    
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, username, password FROM tbl_users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user and pwd == user[2]:  
            session['user_id'] = user[0]  
            session['username'] = user[1]  
            return redirect(url_for('Userpage'))
        else:
            error = "Invalid username or password"
            return render_template('login.html', error=error)  
    return render_template("login.html")


@app.route('/change_password', methods=['POST'])
def change_password():
    if 'username' in session:
        user_id = session['user_id']
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if new_password != confirm_password:
            return "New password and confirm password do not match. Please try again."

        try:
            cur = mysql.connection.cursor()

            cur.execute("SELECT password FROM tbl_users WHERE id = %s", (user_id,))
            stored_password = cur.fetchone()[0]

            if old_password != stored_password:
                return "Incorrect old password. Please try again."

            cur.execute("UPDATE tbl_users SET password = %s WHERE id = %s",
                        (new_password, user_id))
            mysql.connection.commit()
            cur.close()

            return redirect(url_for('Userpage'))

        except Exception as e:
            print("An error occurred while updating password:", e)
            return "An error occurred while updating password. Please try again later."

    else:
        return redirect(url_for('login'))

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'username' in session:
        user_id = session['user_id']
        fullname = request.form.get('fullname')
        username = request.form.get('username')  
        email = request.form.get('email')  
        birthday = request.form.get('birthday')
        gender = request.form.get('gender')

        try:
            cur = mysql.connection.cursor()
            cur.execute("UPDATE tbl_users SET fullname = %s, username = %s, email = %s, birthday = %s, gender = %s WHERE id = %s",
                        (fullname, username, email, birthday, gender, user_id))  
            mysql.connection.commit()
            cur.close()

            session['username'] = username  
            session['email'] = email  
            session['fullname'] = fullname
            session['birthday'] = birthday
            session['gender'] = gender

            return redirect(url_for('Userpage')) 
        except Exception as e:
            print("An error occurred while updating profile:", e)
            return "An error occurred while updating profile. Please try again later."
    else:
        return redirect(url_for('login'))

    

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        pwd = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tbl_users (username, email, password) VALUES (%s, %s, %s)", (username, email, pwd))
        mysql.connection.commit()
        cur.close()
        session['email'] = email

        return redirect(url_for('login'))  

    return render_template('register.html')

@app.route('/Userpage')
def Userpage():
    if 'username' in session:
        user_id = session['user_id']
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT id, document_title, document_text FROM user_documents WHERE user_id = %s", (user_id,))
            documents = cur.fetchall()
            cur.close()
            return render_template('Userpage.html', username=session['username'], documents=documents)
        except Exception as e:
            print("An error occurred while fetching user documents:", e)
            return "An error occurred while fetching user documents."
    else:
        return redirect(url_for('login'))


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.pop('username', None)
        return redirect(url_for('login'))
    
    return redirect(url_for('login'))


@app.route('/Document', methods=['GET', 'POST'])
def Document():
    return render_template('Document.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    document_title = request.form.get('document_title', '')  
    rawtext = request.form.get('rawtext', '') 
    if rawtext:  
        summary, original_txt, len_orig_txt, len_summary = summarizer(rawtext)
        return render_template('Document.html', document_title=document_title, summary=summary, original_txt=original_txt, len_orig_txt=len_orig_txt, len_summary=len_summary)
    else:
        return "Please enter some text in the textarea."
    
@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            docx_content = extract_docx_text(file)
            return docx_content
    return 'Error'
    
def extract_docx_text(file):
    docx = Document(file)
    text = ''
    for paragraph in docx.paragraphs:
        text += paragraph.text + '\n'
    return text

@app.route('/save', methods=['POST'])
def save():
    if 'username' in session:
        user_id = session['user_id']
        document_title = request.form.get('document_title', '')
        document_text = request.form.get('rawtext', '')
        

        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO user_documents (user_id, document_title, document_text) VALUES (%s, %s, %s)", (user_id, document_title, document_text))
            mysql.connection.commit()
            cur.close()

            return redirect(url_for('Userpage'))
        except Exception as e:
            print("An error occurred while saving the document:", e)
            return "An error occurred while saving the document. Please try again later."
    else:
        return redirect(url_for('login'))
    
app.jinja_env.filters['my_enumerate'] = my_enumerate

if __name__ == "__main__":
    try:
        app.run(debug=True)
    except Exception as e:
        print("An exception occurred:", e)
