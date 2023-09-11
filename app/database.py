from app import mysql_config
import mysql.connector


def map_search(keyword, data, max_entries_ct):
    # return data
    headers = (
        'dr_no', 'date_rptd', 'date_occ', 'time_occ', 'area_code', 'area_name', 'rpt_dist_no', 'part', 'crm_cd',
        'crm_cd_desc', 'mocodes', 'vict_age', 'vict_sex', 'vict_descent', 'premis_cd', 'premis_desc',
        'weapon_used_cd', 'weapon_desc', 'status', 'status_desc', 'crime_cd_1', 'crime_cd_2', 'crime_cd_3',
        'crime_cd_4', 'location', 'cross_street', 'latitude', 'longitude'
    )

    # TODO: Write an appropriate sql query.
    cnx = mysql.connector.connect(**mysql_config)
    cur = cnx.cursor(buffered=True)
    cur.execute(f"SELECT {','.join(headers)} FROM Complete_Table "
                f"WHERE {keyword} LIKE '{data}%' OR {keyword} LIKE '%{data}' OR {keyword} LIKE '%{data}%' "
                f"LIMIT {max_entries_ct};")
    result = cur.fetchall()
    cur.close()
    cnx.close()

    return headers, result


def report(data):
    # return data
    cols = []
    vals = []
    err = None

    for col, val in data.items():
        if val:
            cols.append(col)
            vals.append(val)
    try:
        cnx = mysql.connector.connect(**mysql_config)
        cur = cnx.cursor(buffered=True)
        cur.execute(f"INSERT INTO Complete_Table ({','.join(cols)}) VALUES ({','.join(vals)})")
        cnx.commit()
        cur.close()
        cnx.close()
    except mysql.connector.Error as e:
        print("Something went wrong: {}".format(e))
        err = e
    return err


def update(data):
    # return data
    a_string = ''
    first = True
    err = None

    for col, val in data.items():
        if val and col != 'dr_no':
            if first:
                a_string += f"{col}={val}"
                first = False
            else:
                a_string += f", {col}={val}"
    try:
        cnx = mysql.connector.connect(**mysql_config)
        cur = cnx.cursor(buffered=True)
        print(f"UPDATE Complete_Table SET {a_string} WHERE dr_no={data['dr_no']}")
        cur.execute(f"UPDATE Complete_Table SET {a_string} WHERE dr_no={data['dr_no']}")
        cnx.commit()
        cur.close()
        cnx.close()
    except mysql.connector.Error as e:
        print("Something went wrong: {}".format(e))
        err = e
    return err


def delete(dr_no):
    err = None
    try:
        # return data
        cnx = mysql.connector.connect(**mysql_config)
        cur = cnx.cursor(buffered=True)
        cur.execute(f"DELETE FROM Complete_Table where dr_no={dr_no}")
        cnx.commit()
        cur.close()
        cnx.close()
    except mysql.connector.Error as e:
        print("Something went wrong: {}".format(e))
        err = e
    return err


def single_search(data):
    # return data
    headers = (
        'dr_no', 'date_rptd', 'date_occ', 'time_occ', 'area_code', 'area_name', 'rpt_dist_no', 'part', 'crm_cd',
        'crm_cd_desc', 'mocodes', 'vict_age', 'vict_sex', 'vict_descent', 'premis_cd', 'premis_desc',
        'weapon_used_cd', 'weapon_desc', 'status', 'status_desc', 'crime_cd_1', 'crime_cd_2', 'crime_cd_3',
        'crime_cd_4', 'location', 'cross_street', 'latitude', 'longitude'
    )

    cnx = mysql.connector.connect(**mysql_config)
    cur = cnx.cursor(buffered=True)
    cur.execute(f"SELECT {','.join(headers)} FROM Complete_Table WHERE dr_no='{data}';")
    result = cur.fetchall()
    cur.close()
    cnx.close()

    return headers, result


def keyword_search(keyword, data, max_entries_ct):
    # return data
    headers = (
        'dr_no', 'date_rptd', 'date_occ', 'time_occ', 'area_code', 'area_name', 'rpt_dist_no', 'part', 'crm_cd',
        'crm_cd_desc', 'mocodes', 'vict_age', 'vict_sex', 'vict_descent', 'premis_cd', 'premis_desc',
        'weapon_used_cd', 'weapon_desc', 'status', 'status_desc', 'crime_cd_1', 'crime_cd_2', 'crime_cd_3',
        'crime_cd_4', 'location', 'cross_street', 'latitude', 'longitude'
    )

    # TODO: Write an appropriate sql query.
    cnx = mysql.connector.connect(**mysql_config)
    cur = cnx.cursor(buffered=True)
    cur.execute(f"SELECT {','.join(headers)} FROM Complete_Table "
                f"WHERE {keyword} LIKE '{data}%' OR {keyword} LIKE '%{data}' OR {keyword} LIKE '%{data}%' "
                f"LIMIT {max_entries_ct};")
    result = cur.fetchall()
    cur.close()
    cnx.close()

    return headers, result


def run_advanced_queries(option, max_entries_ct):
    if option == 1:
        return find_num_crime_with_places(max_entries_ct)
    elif option == 2:
        return find_crime_with_strong_arm_and_weapon_thrown(max_entries_ct)
    elif option == 3:
        return find_urgent_crimes()


# two advanced queries
def find_num_crime_with_places(max_entries_ct):  # done
    headers = ('longitude', 'latitude', 'Count')

    cnx = mysql.connector.connect(**mysql_config)
    cur = cnx.cursor(buffered=True)
    cur.execute(
        f"SELECT longitude, latitude, Count(*) "
        f"FROM Crime NATURAL JOIN Location GROUP BY longitude, latitude LIMIT {max_entries_ct};"
    )
    result = cur.fetchall()
    cur.close()
    cnx.close()

    return headers, result


def find_crime_with_strong_arm_and_weapon_thrown(max_entries_ct):
    headers = (
        'record_no', 'crime_code', 'crime_code_description', 'crime_code_1', 'crime_code_2', 'crime_code_3',
        'crime_code_4', 'mocodes', 'longitude', 'latitude', 'rpt_dist_no', 'address'
    )

    cnx = mysql.connector.connect(**mysql_config)
    cur = cnx.cursor(buffered=True)
    cur.execute(
        f"(SELECT * FROM Crime WHERE EXISTS"
        f"(SELECT * "
        f"FROM Use_table WHERE code = 306 AND record_no = Crime.record_no) UNION "
        f"SELECT * FROM Crime WHERE EXISTS"
        f"(SELECT * FROM Use_table WHERE code = 400 AND record_no = Crime.record_no))"
        f"LIMIT {max_entries_ct};"
    )
    result = cur.fetchall()
    cur.close()
    cnx.close()

    return headers, result


def find_urgent_crimes():  # done
    headers = ('Record Number', 'Weapon Used Code', 'Weapon Description', 'Urgency')

    cnx = mysql.connector.connect(**mysql_config)
    cur = cnx.cursor(buffered=True)
    cur.execute(f"CALL Find_Urgent;")
    result = cur.fetchall()
    cur.close()
    cnx.close()

    return headers, result


def run_manual_query(query):
    headers = (
        'dr_no', 'date_rptd', 'date_occ', 'time_occ', 'area_code', 'area_name', 'rpt_dist_no', 'part', 'crm_cd',
        'crm_cd_desc', 'mocodes', 'vict_age', 'vict_sex', 'vict_descent', 'premis_cd', 'premis_desc',
        'weapon_used_cd', 'weapon_desc', 'status', 'status_desc', 'crime_cd_1', 'crime_cd_2', 'crime_cd_3',
        'crime_cd_4', 'location', 'cross_street', 'latitude', 'longitude'
    )

    success = 0
    result = ''
    try:
        cnx = mysql.connector.connect(**mysql_config)
        cur = cnx.cursor(buffered=True)
        cur.execute(query)
        if cur is not None:
            result = cur.fetchall()
        cur.close()
        cnx.close()
        success = 1
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        result = err

    return success, result
