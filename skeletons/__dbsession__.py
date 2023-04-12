import sqlite3

# users database manager
class DBManager:

    connection: sqlite3.Connection
    cursor: sqlite3.Cursor

    def __init__(self, datasource: str) -> None:
        self.connection = sqlite3.connect(datasource)
        self.cursor = self.connection.cursor()
        return

    def execute(self, script: str) -> any:
        pass

    def insert(self, table: str, columns: tuple, values: tuple, where: str = None) -> None:
        if where is None:
            self.cursor.execute(f'INSERT INTO {table} {columns} VALUES {values}')
        else:
            self.cursor.execute(f'INSERT INTO {table} {columns} VALUES {values} WHERE {where}')
        return

    def update(self, table: str, columns: tuple, values: tuple, where: str) -> None:
        for column, value in columns, values:
            self.cursor.execute(f'UPDATE {table} SET {column}={value} WHERE {where}')
        return

    def select(self, values: str, table: str, where: str) -> any:
        return self.cursor.execute(f'SELECT {values} FROM {table} WHERE {where}').fetchall()
        return

    def delete(self, fromTable: str, where: str) -> None:
        self.cursor.execute(f'DELETE FROM {fromTable} WHERE {where}')

    def commit(self):
        self.connection.commit()


class UserManager(DBManager):
    def __init__(self, datasource) -> None:
        super().__init__(datasource=datasource)
        return

    def addUser(self, email: str, password: str, username: str) -> None:
        self.insert(table='USERS', columns=('EMAIL', 'PASSWORD', 'USERNAME'),
                    values=(f"{email}", f"{password}", f"{username}"))
        return

    def removeUser(self, email: str, password: str, username: str) -> None:
        self.delete(fromTable='USERS', where=f"EMAIL='{email}' AND PASSWORD='{password}' AND USERNAME='{username}'")
        return

    def changeUserEmail(self, usename: str, password: str, newEmail: str) -> None:
        self.update(table='USERS', columns=('EMAIL',), values=(newEmail,),
                    where=f"USERNAME='{usename}' AND PASSWORD='{password}'")
        return
