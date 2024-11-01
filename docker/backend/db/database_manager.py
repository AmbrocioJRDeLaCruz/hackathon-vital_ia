import pyodbc
from typing import List, Tuple

class DatabaseManager:
    def __init__(self, server: str, database: str, username: str, password: str):
        """
        Initializes the DatabaseManager with connection parameters.

        Parameters:
            server (str): The database server name or IP address.
            database (str): The database name.
            username (str): The database username.
            password (str): The database password.
        """
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.connection = None

    def connect(self):
        """Establishes a connection to the SQL Server database."""
        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={self.server};"
            f"DATABASE={self.database};"
            f"UID={self.username};"
            f"PWD={self.password};"
            "Encrypt=yes;"
        )
        self.connection = pyodbc.connect(connection_string)
        
    def fetch_one(self, query, params=None):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            columns = [column[0] for column in cursor.description]
            row = cursor.fetchone()
            return dict(zip(columns, row)) if row else None
        finally:
            cursor.close()
        
    def get_user(self, username: str) -> Tuple[str, str]:
        """
        Retrieves a user from the database by username.

        Parameters:
            username (str): The username to search for.

        Returns:
            Tuple[str, str]: The username and password of the user, or None if not found.
        """
        self.connect()
        cursor = self.connection.cursor()
        print(f"Executing SQL query with username: {username}")
        cursor.execute("SELECT Nombres, Clave FROM Usuario WHERE Nombres = ?", (username,))
        user = cursor.fetchone()
        if user:
            print(f"Database returned: {user}")
        else:
            print("No user found in database")
        return user
    
    def get_recommendations(self, user_id: int) -> Tuple[str, str]:
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(F"SELECT Detalle FROM RecAlimentarias WHERE IdUsuario = ?", (user_id))
        rows = cursor.fetchall()
        data = {
            "dietary": [row[0] for row in rows]
            }
        
        cursor.execute(F"SELECT Detalle FROM RecEnfermedades WHERE IdUsuario = ?", (user_id))
        rows = cursor.fetchall()
        data["diseases"] = [row[0] for row in rows]
        return data
    
    def email_exists(self, email):
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT 1 FROM Usuario WHERE Correo = ?", (email,))
            return cursor.fetchone() is not None
        finally:
            cursor.close()
    
    def create_user(self, username, password, lastname, email, phone):
        if self.email_exists(email):
            print(f"Error creating user: Email {email} already exists.")
            return False
        
        cursor = self.connection.cursor()
        try:
            cursor.execute("INSERT INTO Usuario (Nombres, Clave, Apellido, Correo, Celular) VALUES (?, ?, ?, ?, ?)", (username, password, lastname, email, phone))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
        finally:
            cursor.close()
            
    def insert_product(self, nombre: str, cantidad: int = None, categoria: str = None, 
                    porcentaje_consumo: float = None, fecha_vencimiento: str = None, 
                    costo: float = None, id_boleta: int = None):
        """Inserts a product into the Productos table."""
        cursor = self.connection.cursor()
        query = """
        INSERT INTO Productos (Nombre, Cantidad, Categoria, PorcentajeConsumo, 
                            FechaVencimiento, Costo, IdBoleta)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (nombre, cantidad, categoria, porcentaje_consumo, 
                            fecha_vencimiento, costo, id_boleta))
        self.connection.commit()
        
    def fetch_all(self, query, params=None):
        
        cursor = self.connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            columns = [column[0] for column in cursor.description]
            
            results = []
            for row in cursor.fetchall():
                row_dict = {}
                for i, value in enumerate(row):
                    if value is None:
                        row_dict[columns[i]] = None
                    else:
                        row_dict[columns[i]] = value
                results.append(row_dict)
            
            return results
        finally:
            cursor.close()
            
    def insert_boleta(self, user_id):
        cursor = self.connection.cursor()
        try:
            query = """
            INSERT INTO Boleta (IdUsuario, FechaBoleta) 
            OUTPUT INSERTED.IdBoleta
            VALUES (?, GETDATE())
            """
            cursor.execute(query, (user_id,))
            row = cursor.fetchone()
            self.connection.commit()
            return row[0]
        finally:
            cursor.close()

    def close_connection(self):
        """Closes the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
            
    def build_insert_query(self, table_name: str, columns: List[str], id_column: str = None) -> str:
        # Join columns with commas for the SQL statement
        columns_str = ", ".join(columns)
        # Generate placeholders ('?') based on the number of columns
        placeholders = ", ".join(["?" for _ in columns])
        
        # Build the final SQL statement
        if not id_column is None:
            query = f"INSERT INTO {table_name} ({columns_str}) OUTPUT INSERTED.{id_column} VALUES ({placeholders});"
        else:
            query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders});"
            
        return query

    def insert_data(self, table_name: str, columns: List[str], data: List[Tuple], id_column: str = None):
        """
        Inserts data into the specified table.

        Parameters:
            table_name (str): The name of the table where data will be inserted.
            data (List[Tuple]): A list of tuples, each representing a row to insert.
        """
        if not self.connection:
            raise ConnectionError("Database connection is not established.")

        insert_query = self.build_insert_query(table_name, columns, id_column)
        
        try:
            with self.connection.cursor() as cursor:
                inserted_id = None
                cursor.executemany(insert_query, data)
                
                if len(data) == 1:
                    inserted_id = cursor.fetchone()[0]
                    print(f"Inserted ID: {inserted_id}")
                    
                self.connection.commit()
                print(f"Inserted {len(data)} rows into '{table_name}' successfully.")
                return inserted_id
        except pyodbc.Error as e:
            print("Error while inserting data:", e)
            self.connection.rollback()
        
    def insert_precedent(self, precedent: str, user_id: int = None):
        """Inserts a predecent into the RecPrecedent table."""
        cursor = self.connection.cursor()
        query = """
        INSERT INTO RecPrecedentes (Detalle, IdUsuario)
        VALUES (?, ?)
        """
        cursor.execute(query, (precedent, user_id))
        self.connection.commit()

    def __enter__(self):
        """Context management entry method to automatically open connection."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Context management exit method to automatically close connection."""
        self.close_connection()
