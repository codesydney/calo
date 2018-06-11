from flask import Flask, render_template, url_for, g, request, redirect, flash
from flaskext.mysql import MySQL
#import sshtunnel
import os
from database import connect_db, get_db
from flask_wtf import Form
from forms import InstForm, Institution

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24) #os.random generates a random string of 24 characters

#sshtunnel.SSH_TIMEOUT = 5.0
#sshtunnel.TUNNEL_TIMEOUT = 5.0

# MySQL configurations (localhost)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'trial'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

# MySQL configurations (pythonanywhere local)
# app.config['MYSQL_DATABASE_USER'] = 'engramar'
# app.config['MYSQL_DATABASE_PASSWORD'] = '12er34ty'
# app.config['MYSQL_DATABASE_DB'] = 'engramar$default'
# app.config['MYSQL_DATABASE_HOST'] = 'engramar.mysql.pythonanywhere-services.com'

# MySQL configurations (pythonanywhere remote)
#app.config['MYSQL_DATABASE_USER'] = 'engramar'
#app.config['MYSQL_DATABASE_PASSWORD'] = '12er34ty'
#app.config['MYSQL_DATABASE_DB'] = 'engramar$default'
#app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'

flaskmysql = MySQL()
flaskmysql.init_app(app)

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'mysql_db'):
        g.mysql_db.close()

@app.route('/',methods=['GET','POST'])
def index():
    #Query PythonAnywhere MySQL database
    #result = execute_query('''SELECT * FROM engramar$default.demo_institutionmodel limit 5;''')
    con = get_db(flaskmysql)
    cur = con.cursor()

    srt = '1'
    srt_order = 'CRICOS_NAME'
    if request.method == 'POST':
        srt = request.form['sort']
        if srt=='0':
            srt_order = 'CRICOS_PROVIDER_CODE'
        elif srt=='1':
            srt_order = 'CRICOS_NAME'
        elif srt=='2':
            srt_order = 'CRICOS_WEBSITE'
    cur.execute('SELECT INSTITUTION_ID, CRICOS_PROVIDER_CODE, CRICOS_NAME, CRICOS_TOTAL_CAPACITY, CRICOS_WEBSITE, FAVOURITE, STATUS FROM demo_institutionmodel ORDER BY ' + srt_order)
    res = cur.fetchall()
    return render_template('home.html',institutes=res,srt=srt)

@app.route('/inst_detail/<id>')
def inst_detail(id):
    con = get_db(flaskmysql)
    cur = con.cursor()
    cur.execute('SELECT * FROM demo_institutionmodel WHERE institution_id = "%s"' % id)
    res = cur.fetchone()
    return render_template('inst_detail.html',inst_detail=res)

@app.route('/inst_edit/<id>',methods=['GET','POST'])
def inst_edit(id):
    con = get_db(flaskmysql)
    cur = con.cursor()

    cur.execute('SELECT * FROM demo_institutionmodel WHERE institution_id = "%s"' % id)
    res = cur.fetchone()
    inst = Institution(res)
    form = InstForm(obj=inst)

    if request.method == 'POST':
        if request.form['btn_submit'] == 'Update':
            if form.validate_on_submit():
                try:
                    cur.execute('UPDATE demo_institutionmodel \
                        SET cricos_provider_id = %s, cricos_provider_code = %s, \
                        cricos_trading_name = %s, cricos_name = %s, cricos_type = %s, \
                        cricos_total_capacity = %s, cricos_website = %s, cricos_postal_address = %s, \
                        locations = %s, favourite = %s, status = %s \
                        WHERE institution_id = %s', (request.form['provider_id'], request.form['provider_code'], \
                        request.form['trading_name'], request.form['name'], request.form['type'], \
                        request.form['total_capacity'], request.form['website'], request.form['postal_address'], \
                        request.form['locations'], request.form['favourite'], request.form['status'], id))
                    con.commit()

                    flash('Record updated successfully')
                    return redirect(url_for('inst_detail',id=id))
                except Exception as e:
                    flash('Update record failed')
                    return redirect(url_for('inst_edit',id=id))

        elif request.form['btn_submit'] == 'Delete':
            try:
                cur.execute('DELETE FROM demo_institutionmodel WHERE institution_id = %s',id)
                con.commit()
                flash('Record deleted successfully')
                return redirect(url_for('index'))
            except Exception as e:
                flash('Delete record failed')
                return redirect(url_for('index'))

    return render_template('inst_edit.html',form=form)

@app.route('/inst_add',methods=['GET','POST'])
def inst_add():
    form = InstForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            con = get_db(flaskmysql)
            cur = con.cursor()
            try:
                cur.execute('INSERT INTO demo_institutionmodel \
                    (cricos_provider_id, cricos_provider_code, cricos_trading_name, \
                    cricos_name, cricos_type, cricos_total_capacity, cricos_website, \
                    cricos_postal_address, locations, favourite, status) \
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',(form.provider_id.data, \
                    form.provider_code.data, form.trading_name.data, form.name.data, form.type.data, \
                    form.total_capacity.data, form.website.data, form.postal_address.data, \
                    form.locations.data, form.favourite.data, form.status.data))
                id = cur.lastrowid
                con.commit()
                flash('Record added successfully')
                return redirect(url_for('inst_detail',id=id))
            except Exception as e:
                flash('Create record failed')
                return redirect(url_for('index'))

    return render_template('inst_add.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
