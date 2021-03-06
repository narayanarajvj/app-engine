import os

from flask import Flask
import psycopg2

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

app = Flask(__name__)


@app.route('/')
def main():
    # When deployed to App Engine, the `GAE_ENV` environment variable will be
    # set to `standard`
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        host = '/cloudsql/{}'.format(db_connection_name)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'

    cnx = psycopg2.connect(dbname=db_name, user=db_user,
                           password=db_password, host=host)
    with cnx.cursor() as cursor:
        cursor.execute('SELECT content FROM entries;')
        result = cursor.fetchall()
    current_time = result[0][0]
    cnx.commit()
    cnx.close()

    return str(current_time)
# [END gae_python3_cloudsql_psql]
# [END gae_python38_cloudsql_psql]


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
