import psycopg2
import tempfile
import time
from fabric.api import local


CONTAINER_RUN_CMD = ("docker run -d -p 26257:26257"
                     " -p 8080:8080 -v {temp_dir}/1:/cockroach/cockroach-data"
                     " cockroachdb/cockroach:beta-20161103 start --insecure")


def execute_sql(container_id, sql_statement, user=None, database=None):
    if user and database:
        local('docker exec {container_id} ./cockroach sql --database={db} --user={user} -e "{ddl}"'.format(
              user=user,
              db=database,
              container_id=container_id,
              ddl=sql_statement))
    else:
        local('docker exec {container_id} ./cockroach sql -e "{ddl}"'.format(
            container_id=container_id, ddl=sql_statement))


def start_database():
    temp_dir = tempfile.mkdtemp()
    run_cmd = ("docker run -d -p 26257:26257"
               " -p 8080:8080 -v {temp_dir}/1:/cockroach/cockroach-data"
               " cockroachdb/cockroach:beta-20161103 start --insecure")
    run_cmd = run_cmd.format(temp_dir=temp_dir)
    return local(run_cmd, capture=True)


def stop_database(container_id):
    local("docker stop {}".format(container_id))
    local("docker rm {}".format(container_id))


def demo_table_insert_and_query():
    """ use a database driver to do some stuff"""
    conn = psycopg2.connect(database='test', user='admin', host='localhost', port=26257)
    conn.set_session(autocommit=True)

    try:
        cur = conn.cursor()

        cur.execute("INSERT INTO accounts (id, balance) VALUES (1, 1000), (2, 250)")
        cur.execute("SELECT id, balance FROM accounts")

        rows = cur.fetchall()
        print 'Initial balances:'
        for row in rows:
            print [str(cell) for cell in row]

    finally:
        cur.close()
        conn.close()


def main():
    container_id = start_database()
    try:
        time.sleep(1)
        execute_sql(container_id, "CREATE DATABASE test;")
        execute_sql(container_id, "GRANT ALL ON DATABASE test TO admin")
        execute_sql(container_id, "CREATE TABLE accounts (id INT PRIMARY KEY, balance INT)", "admin", "test")
        demo_table_insert_and_query()
    finally:
        stop_database(container_id)

if __name__ == "__main__":
    main()
