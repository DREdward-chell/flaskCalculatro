import sqlite3
import typing

Path = typing.TypeVar('Path', bound=typing.Callable[..., typing.Any])


class UserAlreadyExistsError(Exception): ...
class UnknownUserError(Exception): ...
class WrongPassword(Exception): ...

# users database manager
class DBManager:

    connection: sqlite3.Connection
    cursor: sqlite3.Cursor

    def __init__(self, datasource: Path) -> None:
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

    def delete(self, fromTable: str, where: str) -> None:
        self.cursor.execute(f'DELETE FROM {fromTable} WHERE {where}')
        return

    def commit(self):
        self.connection.commit()
        return


class UserManager(DBManager):
    def __init__(self, datasource: Path) -> None:
        super().__init__(datasource=datasource)
        return

    def addUser(self, email: str, password: str, username: str) -> None:
        flag = False
        taken_email = self.select(values='USERNAME', table='USERS', where=f"EMAIL='{email}'")
        taken_username = self.select(values='USERNAME', table='USERS', where='TRUE')
        print(taken_username)
        for i in taken_username:
            if username in i:
                flag = True
        if flag or taken_email:
            raise UserAlreadyExistsError
        self.insert(table='USERS', columns=('EMAIL', 'PASSWORD', 'USERNAME'),
                    values=(f"{email}", f"{password}", f"{username}"))
        return

    def removeUser(self, email: str, password: str, username: str) -> None:
        self.delete(fromTable='USERS', where=f"EMAIL='{email}' AND PASSWORD='{password}' AND USERNAME='{username}'")
        return

    def changeUserEmail(self, username: str, password: str, newEmail: str) -> None:
        self.update(table='USERS', columns=('EMAIL',), values=(newEmail,),
                    where=f"USERNAME='{username}' AND PASSWORD='{password}'")
        return

    def changeUserPassword(self, username: str, password: str, newEmail: str) -> None:
        self.update(table='USERS', columns=('EMAIL',), values=(newEmail,),
                    where=f"USERNAME='{username}' AND PASSWORD='{password}'")

    def checkUserbyEmail(self, email: str, password: str) -> bool:
        flag = False
        __emails__ = self.select(values='EMAIL', table='USERS', where='TRUE')
        for i in __emails__:
            if email in i:
                flag = True
        if not flag:
            raise UnknownUserError
        __password__ = self.select(values='PASSWORD', table='USERS', where=f"EMAIL='{email}'")[0][0]
        if password != __password__:
            raise WrongPassword
        return True

    def checkUserbyUsername(self, username: str, password: str) -> bool:
        flag = False
        __names__ = self.select(values='EMAIL', table='USERS', where='TRUE')
        for i in __names__:
            if username in i:
                flag = True
        if not flag:
            raise UnknownUserError
        __password__ = self.select(values='PASSWORD', table='USERS', where=f"USERNAME='{username}'")[0][0]
        if password != __password__:
            raise WrongPassword
        return True
