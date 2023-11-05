import sqlite3 as sql
def init_db():
    connection = sql.connect('data.db')

    with open('sqlschema.sql') as f:
       connection.executescript(f.read())

    cur = connection.cursor()

    cur.execute("INSERT INTO students(name,addr,city,pin) VALUES (?,?,?,?)",
            ('stephen Ayeni','Agege motor road','Agege','6785')
            )
    
    cur.execute("INSERT INTO students(name,addr,city,pin) VALUES (?,?,?,?)",
            ('mama ojo','12 mushin street','mushin','6745')
            )
    cur.execute("INSERT INTO students(name,addr,city,pin) VALUES (?,?,?,?)",
            ('Olarewaju kola','24 marina street lagos','Lagos','2785')
            )
    



        
    connection.commit()
    connection.close()
    print('Recoords successfuly posted into the database.')
        
init_db()     