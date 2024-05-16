#!/usr/bin/env python3
'''
0. Regex-ing
'''
import logging
import re
from typing import List
logger = logging.getLogger(__name__)
patterns = {
    'to_replace': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replacement': lambda x: r'\g<field>={}'.format(x)
}


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
      redaction: The string to be used for replacing the matched field values.
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
        raw = super(RedactingFormatter, self).format(record)
        formated_txt = filter_datum(self.fields,
                                    self.REDACTION, raw, self.SEPARATOR)
        return formated_txt


if __name__ == "__main__":
    main()
