#!/usr/bin/env python3
'''
0. Regex-ing
'''
import logging
import mysql.connector
from os import getenv
import re
from typing import List

logger = logging.getLogger(__name__)
patterns = {
    'to_replace': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replacement': lambda x: r'\g<field>={}'.format(x)
}
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Filters a log message by redacting specified fields.

    This function replaces the values of fields in a log message
    with a provided redaction string.
    It uses regular expressions to match field names and their
    values based on a separator character.

    Args:
      fields: A list of field names to be redacted from the message.
      redaction: The string to be used for replacing the matched field values
      message: The log message string to be filtered.
      separator: The character used as a separator between fields
      and their values in the log message.

    Returns:
      A new string with the specified fields redacted
      using the provided redaction string.
    """
    return re.sub(patterns['to_replace'](fields, separator),
                  patterns['replacement'](redaction), message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''formats a logrecord
        '''
        raw = super(RedactingFormatter, self).format(record)
        formated_txt = filter_datum(self.fields,
                                    self.REDACTION, raw, self.SEPARATOR)
        return formated_txt


def get_logger() -> logging.Logger:
    """
    Creates and returns a logger or user_data
    """
    logger = logging.getLogger("user_data")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Creates a connector to a database.
    """
    db_host = getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = getenv("PERSONAL_DATA_DB_NAME", "")
    db_user = getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = getenv("PERSONAL_DATA_DB_PASSWORD", "")
    session = mysql.connector.connect(
        host=db_host,
        port=3306,
        user=db_user,
        password=db_pwd,
        database=db_name,
    )
    return session


def main():
    """Logs the information about user records in a table.
    """
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    columns = fields.split(',')
    query = "SELECT {} FROM users;".format(fields)
    info_logger = get_logger()
    session = get_db()
    with session.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            record = map(
                lambda x: '{}={}'.format(x[0], x[1]),
                zip(columns, row),
            )
            msg = '{};'.format('; '.join(list(record)))
            args = ("user_data", logging.INFO, None, None, msg, None, None)
            log_record = logging.LogRecord(*args)
            info_logger.handle(log_record)


if __name__ == "__main__":
    main()
