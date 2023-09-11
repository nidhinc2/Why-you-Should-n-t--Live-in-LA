from app import app
from flask import render_template, request, url_for, flash, redirect
from app import database as db_helper


@app.route('/', methods=['GET', 'POST'])
def index():
    headers = ''
    data = ''
    markers = []
    options = (
        'dr_no', 'date_rptd', 'date_occ', 'time_occ', 'area_code', 'area_name', 'rpt_dist_no', 'part', 'crm_cd',
        'crm_cd_desc', 'mocodes', 'vict_age', 'vict_sex', 'vict_descent', 'premis_cd', 'premis_desc',
        'weapon_used_cd', 'weapon_desc', 'status', 'status_desc', 'crime_cd_1', 'crime_cd_2', 'crime_cd_3',
        'location', 'cross_street', 'latitude', 'longitude'
    )
    if request.method == 'POST':
        column = request.form['column']
        keyword = request.form['keyword']
        max_entries_ct = request.form['max_entries_ct']

        print(column, keyword)

        if not column:
            flash('Column is required!')
        elif not keyword:
            flash('Keyword is required!')
        else:
            if not max_entries_ct:
                max_entries_ct = 20
            headers, data = db_helper.map_search(column, keyword, max_entries_ct)
            if data:
                markers = []
                for row in data:
                    if not (row[-1] == 0 and row[-2] == 0):
                        popup = dict(zip(headers, row))
                        markers.append({
                            'lon': row[-1],
                            'lat': row[-2],
                            'popup': popup
                        })

    return render_template('index.html', options=options, headers=headers, markers=markers)


@app.route('/report/', methods=('GET', 'POST'))
def report():
    if request.method == 'POST':
        dr_no = request.form['dr_no']
        date_rptd = request.form['date_rptd']
        date_occ = request.form['date_occ']
        time_occ = request.form['time_occ']
        area_code = request.form['area_code']
        area_name = request.form['area_name']
        rpt_dist_no = request.form['rpt_dist_no']
        part = request.form['part']
        crm_cd = request.form['crm_cd']
        crm_cd_desc = request.form['crm_cd_desc']
        mocodes = request.form['mocodes']
        vict_age = request.form['vict_age']
        vict_sex = request.form['vict_sex']
        vict_descent = request.form['vict_descent']
        premis_cd = request.form['premis_cd']
        premis_desc = request.form['premis_desc']
        weapon_used_cd = request.form['weapon_used_cd']
        weapon_desc = request.form['weapon_desc']
        status = request.form['status']
        status_desc = request.form['status_desc']
        crime_cd_1 = request.form['crime_cd_1']
        crime_cd_2 = request.form['crime_cd_2']
        crime_cd_3 = request.form['crime_cd_3']
        crime_cd_4 = request.form['crime_cd_4']
        location = request.form['location']
        cross_street = request.form['cross_street']
        latitude = request.form['latitude']
        longitude = request.form['longitude']

        if not dr_no:
            flash('Division of Records Number is required!')

        else:
            user_input_data = {
                'dr_no': dr_no,
                'date_rptd': _user_input_to_sql_syntax(date_rptd),
                'date_occ': _user_input_to_sql_syntax(date_occ),
                'time_occ': time_occ,
                'area_code': area_code,
                'area_name': _user_input_to_sql_syntax(area_name),
                'rpt_dist_no': rpt_dist_no,
                'part': part,
                'crm_cd': crm_cd,
                'crm_cd_desc': _user_input_to_sql_syntax(crm_cd_desc),
                'mocodes': _user_input_to_sql_syntax(mocodes),
                'vict_age': vict_age,
                'vict_sex': vict_sex,
                'vict_descent': vict_descent,
                'premis_cd': premis_cd,
                'premis_desc': _user_input_to_sql_syntax(premis_desc),
                'weapon_used_cd': weapon_used_cd,
                'weapon_desc': _user_input_to_sql_syntax(weapon_desc),
                'status': status,
                'status_desc': _user_input_to_sql_syntax(status_desc),
                'crime_cd_1': crime_cd_1,
                'crime_cd_2': crime_cd_2,
                'crime_cd_3': crime_cd_3,
                'crime_cd_4': crime_cd_4,
                'location': _user_input_to_sql_syntax(location),
                'cross_street': _user_input_to_sql_syntax(cross_street),
                'latitude': latitude,
                'longitude': longitude
            }

            err = db_helper.report(user_input_data)
            if err:
                flash(f"{err}")
            else:
                flash('Crime reported!')
            return redirect(url_for('report'))
    return render_template('report.html')


@app.route('/update/', methods=('GET', 'POST'))
def update():
    if request.method == 'POST':
        dr_no = request.form['dr_no']
        date_rptd = request.form['date_rptd']
        date_occ = request.form['date_occ']
        time_occ = request.form['time_occ']
        area_code = request.form['area_code']
        area_name = request.form['area_name']
        rpt_dist_no = request.form['rpt_dist_no']
        part = request.form['part']
        crm_cd = request.form['crm_cd']
        crm_cd_desc = request.form['crm_cd_desc']
        mocodes = request.form['mocodes']
        vict_age = request.form['vict_age']
        vict_sex = request.form['vict_sex']
        vict_descent = request.form['vict_descent']
        premis_cd = request.form['premis_cd']
        premis_desc = request.form['premis_desc']
        weapon_used_cd = request.form['weapon_used_cd']
        weapon_desc = request.form['weapon_desc']
        status = request.form['status']
        status_desc = request.form['status_desc']
        crime_cd_1 = request.form['crime_cd_1']
        crime_cd_2 = request.form['crime_cd_2']
        crime_cd_3 = request.form['crime_cd_3']
        crime_cd_4 = request.form['crime_cd_4']
        location = request.form['location']
        cross_street = request.form['cross_street']
        latitude = request.form['latitude']
        longitude = request.form['longitude']

        if not dr_no:
            flash('Division of Records Number is required!')
        else:
            user_input_data = {
                'dr_no': dr_no,
                'date_rptd': _user_input_to_sql_syntax(date_rptd),
                'date_occ': _user_input_to_sql_syntax(date_occ),
                'time_occ': time_occ,
                'area_code': area_code,
                'area_name': _user_input_to_sql_syntax(area_name),
                'rpt_dist_no': rpt_dist_no,
                'part': part,
                'crm_cd': crm_cd,
                'crm_cd_desc': _user_input_to_sql_syntax(crm_cd_desc),
                'mocodes': _user_input_to_sql_syntax(mocodes),
                'vict_age': vict_age,
                'vict_sex': vict_sex,
                'vict_descent': vict_descent,
                'premis_cd': premis_cd,
                'premis_desc': _user_input_to_sql_syntax(premis_desc),
                'weapon_used_cd': weapon_used_cd,
                'weapon_desc': _user_input_to_sql_syntax(weapon_desc),
                'status': status,
                'status_desc': _user_input_to_sql_syntax(status_desc),
                'crime_cd_1': crime_cd_1,
                'crime_cd_2': crime_cd_2,
                'crime_cd_3': crime_cd_3,
                'crime_cd_4': crime_cd_4,
                'location': _user_input_to_sql_syntax(location),
                'cross_street': _user_input_to_sql_syntax(cross_street),
                'latitude': latitude,
                'longitude': longitude
            }
            print(crime_cd_2)
            print(type(crime_cd_2))
            print(date_rptd)
            print(type(date_rptd))
            err = db_helper.update(user_input_data)
            if err:
                flash(f"{err}")
            else:
                flash('Record updated!')

            return redirect(url_for('update'))

    return render_template('update.html')


@app.route('/delete/', methods=('GET', 'POST'))
def delete():
    if request.method == 'POST':
        dr_no = request.form['dr_no']

        if not dr_no:
            flash('Division of Records Number is required!')
        else:
            err = db_helper.delete(dr_no)
            if err:
                flash(f"{err}")
            else:
                flash('Record deleted!')
            return redirect(url_for('delete'))

    return render_template('delete.html')


@app.route('/single_search/', methods=('GET', 'POST'))
def single_search():
    headers = ''
    data = ''
    if request.method == 'POST':
        dr_no = request.form['dr_no']

        if not dr_no:
            flash('Division of Records Number is required!')
        else:
            headers, data = db_helper.single_search(dr_no)

    return render_template('single_search.html', headers=headers, data=data)


@app.route('/keyword_search/', methods=('GET', 'POST'))
def keyword_search():
    headers = ''
    data = ''
    options = (
        'dr_no', 'date_rptd', 'date_occ', 'time_occ', 'area_code', 'area_name', 'rpt_dist_no', 'part', 'crm_cd',
        'crm_cd_desc', 'mocodes', 'vict_age', 'vict_sex', 'vict_descent', 'premis_cd', 'premis_desc',
        'weapon_used_cd', 'weapon_desc', 'status', 'status_desc', 'crime_cd_1', 'crime_cd_2', 'crime_cd_3',
        'location', 'cross_street', 'latitude', 'longitude'
    )
    if request.method == 'POST':
        column = request.form['column']
        keyword = request.form['keyword']
        max_entries_ct = request.form['max_entries_ct']

        print(column, keyword)

        if not column:
            flash('Column is required!')
        elif not keyword:
            flash('Keyword is required!')
        else:
            if not max_entries_ct:
                max_entries_ct = 200
            headers, data = db_helper.keyword_search(column, keyword, max_entries_ct)
            print('~~~~')
            print(headers)
            print(data)
            print('~~~~')

    return render_template('keyword_search.html', options=options, headers=headers, data=data)


@app.route('/advanced_queries/', methods=('GET', 'POST'))
def advanced_queries():
    headers = ''
    data = ''
    if request.method == 'POST':
        max_entries_ct = request.form['max_entries_ct']
        if not max_entries_ct:
            max_entries_ct = 200

        if request.form.get('q1'):
            headers, data = db_helper.run_advanced_queries(1, max_entries_ct)
        elif request.form.get('q2'):
            headers, data = db_helper.run_advanced_queries(2, max_entries_ct)
        elif request.form.get('q3'):
            headers, data = db_helper.run_advanced_queries(3, max_entries_ct)

    return render_template('advanced_queries.html', headers=headers, data=data)


@app.route('/manual_query/', methods=('GET', 'POST'))
def manual_query():
    result = ''
    if request.method == 'POST':
        query = request.form['content']
        if not query:
            flash('Please type your query.')
        else:
            success, result = db_helper.run_manual_query(query)
            if not success:
                flash(result)
                result = ''
            print(result)
    return render_template('manual_query.html', result=result)


def _user_input_to_sql_syntax(var):
    return f"'{var}'" if var else var
