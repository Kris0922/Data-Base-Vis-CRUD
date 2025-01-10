from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

CORS(app, resources={
    r"/*": {
        "origins": "http://localhost:8000",
        "methods": ["GET", "POST", "DELETE", "OPTIONS"]
    }
})


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='your-database name',
            user='your-user',  # înlocuiește cu user-ul tău
            password='your-password',  # înlocuiește cu parola ta
            auth_plugin='mysql_native_password',
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
#############
# these could be custom for your app
# Endpoint pentru interogari simple
@app.route('/api/simple_query/<query_id>')
def simple_query(query_id):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            param = request.args.get('param')  # Preia parametru variabil din URL

            if query_id == '1':  # Lista modelelor, mentorilor lor și competițiilor unde au participat
                query = """
                SELECT m.Nume AS Model_Nume, m.Prenume AS Model_Prenume,
                       mt.mentor_nume AS Mentor_Nume, mt.mentor_prenume AS Mentor_Prenume,
                       c.Nume_Eveniment AS Competitie
                FROM Model m
                JOIN Mentor mt ON m.Mentor_Id = mt.Mentor_Id
                JOIN ModelCompetitie mc ON m.Model_ID = mc.Model_ID
                JOIN Competitie c ON mc.Competitie_ID = c.Competitie_ID
                            """
                cursor.execute(query)
                results = cursor.fetchall()  # Consumă rezultatele
                return jsonify(results)
            elif query_id == '2':  # Modele si competitiile la care au participat
                if not param:
                    return jsonify({"error": "Parameter 'param' is required"}), 400
                query = """
                SELECT m.Nume AS Model_Nume, m.Prenume AS Model_Prenume, 
                       c.Nume_Eveniment, mc.Data_participare
                FROM Model m
                JOIN ModelCompetitie mc ON m.Model_ID = mc.Model_ID
                JOIN Competitie c ON mc.Competitie_ID = c.Competitie_ID
                WHERE c.Nume_Eveniment = %s
                """
                cursor.execute(query, (param,))
                results = cursor.fetchall()  # Consumă rezultatele
                return jsonify(results)
            elif query_id == '3':  # Jurații și competițiile unde au fost implicați
                query = """
                SELECT j.Nume AS Jurat_Nume, j.Prenume AS Jurat_Prenume, 
                       c.Nume_Eveniment, jc.Rol
                FROM Jurat j
                JOIN JuratCompetitie jc ON j.Jurat_ID = jc.Jurat_ID
                JOIN Competitie c ON jc.Competitie_ID = c.Competitie_ID
                """
                cursor.execute(query)
                results = cursor.fetchall()  # Consumă rezultatele
                return jsonify(results)
            elif query_id == '4':  # Mentorii și modelele lor, inclusiv datele contractelor
                query = """
                SELECT mt.mentor_nume AS Mentor_Nume, mt.mentor_prenume AS Mentor_Prenume, 
                       m.Nume AS Model_Nume, m.Prenume AS Model_Prenume, mm.Data_semnare_contract, mm.Data_incheiere
                FROM Mentor mt
                JOIN MentorModel mm ON mt.Mentor_Id = mm.Mentor_Id
                JOIN Model m ON mm.Model_Id = m.Model_ID
                """
                cursor.execute(query)
                results = cursor.fetchall()  # Consumă rezultatele
                return jsonify(results)
            elif query_id == '5':  # Modelele cu detalii despre participarea la competiții
                query = """
                SELECT m.Nume AS Model_Nume, m.Prenume AS Model_Prenume, 
                       c.Nume_Eveniment, mc.Durata_participare
                FROM Model m
                JOIN ModelCompetitie mc ON m.Model_ID = mc.Model_ID
                JOIN Competitie c ON mc.Competitie_ID = c.Competitie_ID
                """
                cursor.execute(query)
                results = cursor.fetchall()  # Consumă rezultatele
                return jsonify(results)
            elif query_id == '6':  # Lista mentorilor fără modele asociate și competițiile lor
                query = """
                SELECT mt.mentor_nume AS Mentor_Nume, mt.mentor_prenume AS Mentor_Prenume,
                       c.Nume_Eveniment AS Competitie
                FROM Mentor mt
                LEFT JOIN Model m ON mt.Mentor_Id = m.Mentor_Id
                LEFT JOIN MentorModel mm ON mt.Mentor_Id = mm.Mentor_Id
                LEFT JOIN Competitie c ON mm.Mentor_Id = mt.Mentor_Id
                WHERE m.Mentor_Id IS NULL
                """
                cursor.execute(query)
                results = cursor.fetchall()  # Consumă rezultatele
                return jsonify(results)
            else:
                return jsonify({"error": "Invalid query ID"}), 400

            cursor.execute(query)
            results = cursor.fetchall()
            return jsonify(results)

        except Error as e:
            print(f"Error in simple_query (query_id={query_id}, param={param}): {e}")
            return jsonify({"error": str(e)}), 500
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    return jsonify({"error": "Could not connect to database"}), 500

# Endpoint pentru interogari complexe
@app.route('/api/complex_query/<query_id>')
def complex_query(query_id):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            param = request.args.get('param')

            if query_id == '1':  # Modele cu mentori care au participat la cel puțin o competiție
                query = """
                SELECT m.Nume AS Model_Nume, m.Prenume AS Model_Prenume
                FROM Model m
                WHERE EXISTS (
                    SELECT 1
                    FROM Mentor mt
                    JOIN MentorModel mm ON mt.Mentor_Id = mm.Mentor_Id
                    WHERE m.Mentor_Id = mt.Mentor_Id
                )
                """
                cursor.execute(query)
            elif query_id == '2':  # Jurați implicați în competiții după un anumit an
                if not param:
                    return jsonify({"error": "Parameter 'param' is required"}), 400
                query = """
                SELECT j.Nume, j.Prenume
                FROM Jurat j
                WHERE EXISTS (
                    SELECT *
                    FROM JuratCompetitie jc
                    JOIN Competitie c ON jc.Competitie_ID = c.Competitie_ID
                    WHERE jc.Jurat_ID = j.Jurat_ID AND YEAR(c.Data) >= %s
                )
                """
                cursor.execute(query, (param,))
            elif query_id == '3':  # Modele implicate în competiții multiple
                query = """
                SELECT m.Nume, m.Prenume
                FROM Model m
                WHERE (
                    SELECT COUNT(*)
                    FROM ModelCompetitie mc
                    WHERE mc.Model_ID = m.Model_ID
                ) > 1
                """
                cursor.execute(query)
            elif query_id == '4':  # # Competiții populare cu modele multiple
                query = """
                SELECT c.Nume_Eveniment, c.Data
                FROM Competitie c
                WHERE (
                    SELECT COUNT(DISTINCT mc.Model_ID)
                    FROM ModelCompetitie mc
                    WHERE mc.Competitie_ID = c.Competitie_ID
                ) > 1
                """
                cursor.execute(query)
            else:
                return jsonify({"error": "Invalid query ID"}), 400

            results = cursor.fetchall()
            return jsonify(results)

        except Error as e:
            print(f"Error in complex_query (query_id={query_id}, param={param}): {e}")
            return jsonify({"error": str(e)}), 500
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    return jsonify({"error": "Could not connect to database"}), 500
#############

@app.route('/api/tables')
def get_tables():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SHOW TABLES")
            tables = [table[0] for table in cursor.fetchall()]
            return jsonify({"tables": tables})
        except Error as e:
            return jsonify({"error": str(e)}), 500
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    return jsonify({"error": "Could not connect to database"}), 500


@app.route('/api/table/<table_name>')
def get_table_data(table_name):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)

            # Fetch table structure -- this finally works
            cursor.execute(f"DESCRIBE {table_name}")
            columns = [column['Field'] for column in cursor.fetchall()]

            # Fetch table data
            cursor.execute(f"SELECT * FROM {table_name}")
            data = cursor.fetchall()

            return jsonify({
                "columns": columns,
                "data": data
            })
        except Error as e:
            print(f"Error fetching data for table {table_name}: {e}")  # Log the error
            return jsonify({"error": str(e)}), 500
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    return jsonify({"error": "Could not connect to database"}), 500


@app.route('/api/table/<table_name>/add', methods=['POST'])
def add_record(table_name):
    data = request.json  # JSON payload sent by the frontend
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Fetch the primary key column
            cursor.execute(f"DESCRIBE {table_name}")
            table_structure = cursor.fetchall()
            primary_key = None
            for column in table_structure:
                if column[3] == 'PRI':  # Check if the column is a primary key
                    primary_key = column[0]
                    break

            if not primary_key:
                return jsonify({"error": f"Table {table_name} does not have a primary key"}), 400

            # Check if the primary key is missing or empty
            if primary_key not in data or not data[primary_key]:
                cursor.execute(f"SELECT `{primary_key}` FROM {table_name} ORDER BY `{primary_key}`")
                existing_ids = [row[0] for row in cursor.fetchall()]
                # Find the smallest missing ID
                next_id = 1
                for existing_id in existing_ids:
                    if next_id < existing_id:
                        break
                    next_id += 1
                data[primary_key] = next_id  # Assign the next available ID

            # Insert the new record
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

            cursor.execute(query, list(data.values()))
            connection.commit()

            return jsonify({"message": "Record added successfully", "id": data[primary_key]}), 201

        except Error as e:
            print(f"Error inserting data into {table_name}: {e}")
            return jsonify({"error": str(e)}), 500
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    return jsonify({"error": "Could not connect to database"}), 500


@app.route('/api/table/<table_name>/delete', methods=['DELETE'])
def delete_record(table_name):
    data = request.json  # JSON payload sent by the frontend (e.g., {"primary_key": "id", "value": 123})
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Create DELETE SQL query
            query = f"DELETE FROM {table_name} WHERE {data['primary_key']} = %s"
            cursor.execute(query, (data['value'],))
            connection.commit()

            # Check if a record was deleted
            if cursor.rowcount > 0:
                return jsonify({"message": "Record deleted successfully"}), 200
            else:
                return jsonify({"error": "Record not found"}), 404

        except Error as e:
            print(f"Error deleting record from {table_name}: {e}")
            return jsonify({"error": str(e)}), 500
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    return jsonify({"error": "Could not connect to database"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=8000)
