import psycopg2
import psycopg2.extras
import yaml

with open('config/config.yml', 'r') as file:
    config = yaml.safe_load(file)

datasource = config['datasource']
def get_connection():
    conn = psycopg2.connect(user=datasource['username'],
                    password=datasource['password'],
                    host=datasource['host'],
                    port=datasource['port'],
                    dbname=datasource['database'])
    
    return conn


def execute_insert(query):
    conn = get_connection()
    
    cur = conn.cursor()

    cur.execute(query)
    
    conn.commit()
    cur.close()
    conn.close()
    

def execute_and_get_result(query):
    conn = get_connection()
    
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

    cur.execute(query)
    results = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    
    return results

def execute_write_only(query):
    conn = get_connection()
    
    cur = conn.cursor()

    cur.execute(query)
    
    conn.commit()
    cur.close()
    conn.close()


def get_szz_variants():
    query = "SELECT * from szz_variant;"
    return execute_and_get_result(query)


def insert_szz_result(repo_url: str, bugfix_commit_hash: str, bug_commit_hashes: list, szz_variant: str):
    query = f"""INSERT INTO execution_result (repository_url, szz_variant, bugfix_commit_hash, bug_commit_hashes) values (%s, %s, %s, %s);"""
    conn = get_connection()
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

    cur.execute(query, (repo_url, szz_variant, bugfix_commit_hash, bug_commit_hashes))

    conn.commit()
    cur.close()
    conn.close()

def find_processed_bugfix_commits(repo_url: str, fix_commit_list: list, szz_variant: str):
    in_clause = f"{fix_commit_list}".replace('[', '(').replace(']',  ')')
    query = f"""SELECT * 
                FROM execution_result
                WHERE repository_url = '{repo_url}'
                    AND bugfix_commit_hash IN {in_clause}
                    AND szz_variant = '{szz_variant}'
            """
    
    result = execute_and_get_result(query)
    return result


def insert_request(repo_url: str, szz_variant: str, fix_commit_list: list):
    query = f"""INSERT INTO request (repository_url, szz_variant, bugfix_commit_hashes, commit_count) values (%s, %s, %s, %s) returning request_id;"""
    conn = get_connection()
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

    cur.execute(query, (repo_url, szz_variant, fix_commit_list, len(fix_commit_list)))

    request_id = cur.fetchone()['request_id']
    conn.commit()
    cur.close()
    conn.close()
    return request_id


def insert_request_status(request_id: int, bugfix_commit_hash: str, finished: bool = False):
    query = f"""INSERT INTO commit_to_request_link (request_id, bugfix_commit_hash, finished) values (%s, %s, %s);"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(query, (request_id, bugfix_commit_hash, finished))

    conn.commit()
    cur.close()
    conn.close()

def complete_request(request_id: int, fix_commit_hash: str):
    query = f"""UPDATE commit_to_request_link SET finished = TRUE WHERE request_id = {request_id} AND bugfix_commit_hash = '{fix_commit_hash}';"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(query)

    conn.commit()
    cur.close()
    conn.close()

def check_request_finished(request_id):
    query = f"""SELECT count(*) 
                FROM commit_to_request_link 
                WHERE request_id = (%s) 
                    AND finished = true;"""
    conn = get_connection()
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

    cur.execute(query, (request_id, ))

    finished_count = cur.fetchone()['count']
    conn.commit()
    cur.close()
    conn.close()
    return finished_count


def get_request_data(request_id):
    query = f"""SELECT *  from request where request_id = (%s);"""
    conn = get_connection()
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

    cur.execute(query, (request_id, ))

    result = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return result



    

    



