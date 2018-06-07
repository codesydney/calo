from flask import g
import mysql.connector

def connect_db(flaskmysql):
    con = flaskmysql.connect()
    return con

def get_db(flaskmysql):
    if not hasattr(g, 'mysql_db'):
        g.mysql_db = connect_db(flaskmysql)
    return g.mysql_db

'''
def execute_query(query):
    if app.config['MYSQL_DATABASE_HOST'] == '127.0.0.1':
        with sshtunnel.SSHTunnelForwarder(
        ('ssh.pythonanywhere.com'),
        ssh_username='engramar', ssh_password='calo123456',
        remote_bind_address=('engramar.mysql.pythonanywhere-services.com', 3306)
    ) as tunnel:
            print(tunnel.local_bind_port)
            app.config['MYSQL_DATABASE_PORT'] = tunnel.local_bind_port
            conn = flaskmysql.connect()
            cursor = conn.cursor()
            cursor.execute(query)
            rv = cursor.fetchall()
            conn.close()
    else:
        conn = flaskmysql.connect()
        cursor = conn.cursor()
        cursor.execute(query)
        rv = cursor.fetchall()
        conn.close()
    return rv
'''
