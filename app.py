import datetime
import os
from flask import Flask,render_template,request,redirect,url_for,flash
from werkzeug.utils import secure_filename
import sqlite3 as sql
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/retrieve')
def retrieve():
    con=sql.connect("user_db.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from user_table")
    data=cur.fetchall()
    return render_template('retrieve.html',datas=data)

@app.route('/create',methods=['POST','GET'])
def create():
    if request.method=='POST':
        name=request.form['name']
        contact=request.form['contact']
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename_path = secure_filename(file.filename)
            split_filename_path = os.path.splitext(filename_path)
            ct = datetime.datetime.now()
            ts = ct.timestamp()
            new_filename_path = str(ts)+split_filename_path[1]
            disnation = os.path.join(app.config['UPLOAD_FOLDER'], new_filename_path)
            file.save(disnation)
            con=sql.connect("user_db.db")
            cur=con.cursor()
            cur.execute("insert into user_table(name,contact,filename) values(?,?,?)",[name,contact,new_filename_path])
            con.commit()
            flash('Data Saved','success')
            return redirect(url_for("retrieve"))
        else:
            flash('File formate must be png, jpg, jpeg and gif','warning')
            return render_template('create.html')
    return render_template('create.html')

@app.route('/update/<string:id>',methods=['POST','GET'])
def update(id):
    con=sql.connect("user_db.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from user_table where id=?",[id])
    data=cur.fetchone()
    if request.method=='POST':
        name=request.form['name']
        contact=request.form['contact']
        file = request.files['file']
        filename_path = secure_filename(file.filename)
        if filename_path == '':
            con=sql.connect("user_db.db")
            cur=con.cursor()
            cur.execute("update user_table set name=?,contact=? where id=?",[name,contact,id])
        else:
            if file and allowed_file(file.filename):
                split_filename_path = os.path.splitext(filename_path)
                ct = datetime.datetime.now()
                ts = ct.timestamp()
                new_filename_path = str(ts)+split_filename_path[1]
                disnation = os.path.join(app.config['UPLOAD_FOLDER'], new_filename_path)
                file.save(disnation)
                con=sql.connect("user_db.db")
                cur=con.cursor()
                cur.execute("update user_table set name=?,contact=?,filename=? where id=?",[name,contact,new_filename_path,id])
            else:
                flash('File formate must be png, jpg, jpeg and gif','warning')
                return render_template('update.html',datas=data)
        con.commit()
        flash('Data updated','success')
        return redirect(url_for("retrieve"))
    return render_template('update.html',datas=data)

@app.route('/delete/<string:id>',methods=['GET'])
def delete(id):
    con=sql.connect("user_db.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("delete from user_table where id=?",[id])
    con.commit()
    flash('Data Deleted','warning')
    return redirect(url_for("retrieve"))

if __name__ =='__main__':
    app.secret_key='admin123'
    app.run(debug=True)
