from datetime import datetime, timedelta
import sqlite3

from loguru import logger


class ReminderModel:
    _conn = sqlite3.connect('reminder.sqlite', check_same_thread=False)

    def __init__(self):
        self._date = None
        self._message = ''

    @property
    def date(self) -> datetime:
        return self._date

    @date.setter
    def date(self, value: datetime):
        self._date = value.replace(second=0, microsecond=0)

    @property
    def message(self) -> str:
        return self._message

    @message.setter
    def message(self, value: str):
        self._message = value

    @classmethod
    def from_duration(cls, hours=0, minutes=0, message=''):
        now = datetime.now()
        delta = timedelta(hours=hours, minutes=minutes)

        reminder = cls()
        reminder.date = now + delta
        reminder.message = message
        return reminder

    def save(self):
        self._create_table()

        sql = '''
        INSERT INTO Reminders (datetimeReminder, message) VALUES (?, ?);
        '''

        with self._conn:
            cur = self._conn.cursor()
            logger.info(f'Saving reminder: {self}')
            cur.execute(sql, (self.date, self.message))

    def reminders_now(self):
        self._create_table()

        sql_select = '''
        SELECT * FROM Reminders
        WHERE Reminders.datetimeReminder <= datetime('now', 'localtime');
        '''

        sql_delete = '''
        DELETE FROM Reminders
        WHERE Reminders.id == (?);
        '''

        with self._conn:
            cur = self._conn.cursor()
            cur.execute(sql_select)
            results = list(cur.fetchall())
            if results:
                cur.executemany(sql_delete, [(i, ) for i, date, message in results])

        return [(date, message) for i, date, message in results]

    def _create_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS Reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetimeReminder DATETIME NOT NULL,
            message TEXT NULL
        );
        '''

        with self._conn:
            cur = self._conn.cursor()
            cur.execute(sql)

    def __str__(self):
        return f'(Reminder: {self.date}, {self.message})'
