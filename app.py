from flask import Flask, render_template, request, redirect, url_for
from flask import Flask, render_template, request, redirect, url_for, session
from github import Github
import os
import time
from datetime import datetime
app = Flask(__name__)


app.secret_key = "#STF017632"

from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import os
from datetime import datetime
import pymysql
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sachin@123'
app.config['MYSQL_DB'] = 'sachin'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

db = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='sachin@123',
    database='sachin'
)
cur = db.cursor()


import MySQLdb

# Define your MySQL connection parameters
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'sachin@123',
    'database': 'sachin',
}


# Replace with your GitHub credentials
GITHUB_TOKEN = "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"  # Generate a personal access token
# Initialize GitHub API
github = Github(GITHUB_TOKEN)
# User information dictionary
USERS = {
    'admin': 'abc',
    'user1': '1',
    'user2': '2',
    'user3': '3',
    'user4': '4'
}
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        # Check if the provided username and password match any user in USERS
        if username in USERS and USERS[username] == password:
           session['username'] = username
           return redirect(url_for("upload"))
        else:
            return render_template('login.html')
    return render_template('login.html')

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        username = session.get('username')
        reason = request.form['reason']
        changes = request.form['changes']
        
        file = request.files["file"]
        if file:
            timestamp = str(int(time.time()))  # Unix timestamp as filename
            filename = timestamp + ".sql" #+ file.filename
            file.save(filename)
            file = request.files['file']
            file.save(os.path.join('uploads', filename))
            
            Data = datetime.now()
            formatted_timestamp = Data.strftime("%Y-%m-%d %H:%M:%S")
            upload_datetime = formatted_timestamp
            
            #filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}-{file.filename}"
            #file.save(os.path.join('uploads', filename))
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO uploads (reason, changes, filename,upload_datetime, uploaded_by) VALUES (%s, %s, %s, %s,%s)",(reason, changes, filename, upload_datetime,username))  # Include username here     
            mysql.connection.commit()
            cur.close()
            
            # Read the SQL content from the uploaded file
            with open(filename, 'r') as sql_file:
                sql_content = sql_file.read()

                # Initialize the cursor and connection
                cur = mysql.connection.cursor()

                try:
                    # Execute the SQL commands from the uploaded file
                    cur.execute(sql_content)

                    # Move to the next result set (if any)
                    cur.nextset()

                    # Commit the changes to the database
                    mysql.connection.commit()

                except Exception as e:
                    # If an error occurs, rollback the transaction and handle the exception
                    mysql.connection.rollback()
                    print(f"An error occurred: {e}")

                finally:
                    # Close the cursor
                    cur.close()




            # with open(filename, 'r') as sql_file:
            #     sql_content = sql_file.read()
            #     cur = mysql.connection.cursor()

            #     # Execute the SQL commands from the uploaded file
            #     cur.execute(sql_content)
            #     # mysql.connection.commit()
            #     # Execute the SQL commands from the uploaded file with multi=True
            #     # cur.execute(sql_content, multi=True)
            #     # Commit the changes
            #     #cur = mysql.connection.cursor()
            #     mysql.connection.commit()
            #     #cur.commit()
            #     cur.close()

            
                    
            # Upload to GitHub
            repo = github.get_repo("MapplesoftAccount/parisMysql")  # Replace with your GitHub username and repository name
            with open(filename, "rb") as f:
                content = f.read()
                repo.create_file(filename, f"Upload {filename}", content)
            os.remove(filename)  # Remove the uploaded file
            
            return redirect(url_for('view_files'))

            #return "File Upload on Github and information save in mysql database successful!"
        #return "No file uploaded."
    return render_template("upload.html")



#@app.route('/view')
#def view_files():
#    query = "SELECT * FROM uploads"
#    cur.execute(query)
#    files = cur.fetchall()
#    return render_template('view_files.html', files=files)

@app.route('/view_files', methods=['GET'])
def view_files():
    uploader = request.args.get('uploader', None)
    query = "SELECT * FROM uploads"
    cur.execute(query)
    files = cur.fetchall()
    

    #if uploader:
    #    filtered_files = [file for file in files if file['uploaded_by'] == uploader]
    #else:
    #    filtered_files = files
    filtered_files = []

    for file in files:
        if uploader is None or file[4] == uploader:  # Use the correct index for the 'uploaded_by' column
            filtered_files.append(file)
    return render_template('view_files.html', files=filtered_files)


if __name__ == "__main__":
    app.run(debug=True)


