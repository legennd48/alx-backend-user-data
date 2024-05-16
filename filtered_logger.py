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
                 separator: chr) -> str:
    '''
    Filters log lines
    '''
    return re.sub(patterns['to_replace'](fields, separator),
                  patterns['replacement'](redaction), message)
