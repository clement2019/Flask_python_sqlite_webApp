from contextlib import redirect_stderr
from flask import Flask, render_template, request,session,redirect,abort,flash,request, url_for
import sqlite3 as sql
app = Flask(__name__)


# ...
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


def get_db_connect():
    conn = sql.connect('data.db')
    conn.row_factory = sql.Row
    return conn
 
@app.route('/')
def index():
    conn = get_db_connect()
    rows = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template('index.html',rows=rows)

# ...

def get_student(student_id):
    conn = get_db_connect()
    collectedstudent = conn.execute('SELECT * FROM students WHERE id = ?',
                        (student_id,)).fetchone()
    conn.close()
    if collectedstudent is None:
        abort(404)
    return collectedstudent

# ...

@app.route('/enternew')
def new_student():
   return render_template('student.html')
  # return render_template("registrationform.html")
@app.route('/login')
def login():
   return render_template('login.html')



#Enter logic to login student below


#Enter logic to login student below

@app.route('/log', methods =['GET', 'POST'])
def log():
    message = ''
    if request.method == 'POST':
       nm = request.form['nm']
       pin = request.form['pin']
       with sql.connect("data.db") as con:
          cur = con.cursor()
          #cur.execute("SELECT name,pin FROM students WHERE name = '" + name +"'AND pin = '" + pin + "'")
          cur.execute("SELECT name,pin FROM students WHERE name = '"+nm+"' and pin='"+ pin+ "'")
          user = cur.fetchall()
      
          if len(user) == 0:
            #session['loggedin'] = True
            #session['userid'] = user['userid']
            #session['nm'] = user['nm']
            #session['pin'] = user['pin']
            message = 'Invalid student credentials supplied!'
            return render_template('errormessage.html', message = message)
          else:
            message = 'Logged in successfully !'
            return render_template('userplatform.html', message = message)
      
           
  
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('nm', None)
    session.pop('pin', None)
    #return redirect_stderr(url_for('login'))
    return render_template('login.html')

#Enter log to submit student records below

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   msg = ''
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         addr = request.form['addr']
         city = request.form['city']
         pin = request.form['pin']
         
         if not nm:
            msg='name is required!'
         elif not addr:
            #flash('address is required!')
            msg='address is required!'
         elif not city:
            #flash('city is required!')
             msg='city is required!'
         elif not pin:
            #flash('pin is required!')
            msg='pin is required!'
         else:
           
         
           con = get_db_connect()
          
            
         
           con.execute("INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)",(nm,addr,city,pin) )
            
           con.commit()
           con.close()
           msg = "Record successfully added"
           return render_template("result.html",msg = msg)
         
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
          print("close")
          return render_template("result.html",msg = msg)
         #con.close()
      
@app.route('/')
def list():
   con = sql.connect("data.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from students")
   
   rows = cur.fetchall();
   return render_template("index.html",rows = rows)



@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    post = get_student(id)

    if request.method == 'POST':
        name = request.form['name']
        addr = request.form['addr']
        city = request.form['city']
        pin = request.form['pin']
         
        if not name:
            msg='name is required!'
        elif not addr:
            #flash('address is required!')
            msg='address is required!'
        elif not city:
            #flash('city is required!')
             msg='city is required!'
        elif not pin:
            #flash('pin is required!')
            msg='pin is required!'

        else:
            conn = get_db_connect()
            conn.execute('UPDATE students SET name= ?, addr= ?,city= ?, pin= ?'
                         ' WHERE id = ?',
                         (name, addr,city,pin,id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

 # ...

@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    post = get_student(id)
    conn = get_db_connect()
    conn.execute('DELETE FROM students WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['name']))
    return redirect(url_for('index'))



if __name__ == '__main__':
   app.run(debug = True)