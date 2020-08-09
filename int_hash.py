from ansible import errors
import crypt
import hashlib
import random
from hashlib import sha1

def get_hash(data, hashtype='sha1'):

    try: # see if hash is supported
        h = hashlib.new(hashtype)
    except:
        return None

    h.update(data.encode('utf-8'))
    return h.hexdigest()

def get_int_hash(data, min=0, max=None):
    hex_hash = get_hash(data, hashtype='sha512')
    int_hash = int(hex_hash, 16)
    if max is None:
        if min != 0:
            raise errors.AnsibleFilterError('|int_hash expects a max value to be given together with min')
        return int_hash
    else:
        if min >= max:
            raise errors.AnsibleFilterError('|int_hash expects max to be higher than min')
        if min < 0:
            raise errors.AnsibleFilterError('|int_hash expects min to be a positive integer')
        return min + int_hash % (max + 1 - min)

def get_mysql_password(string):
    if string:
        return '*' + sha1(sha1(string.encode('utf-8')).digest()).hexdigest().upper()
    else:
        return ''

class FilterModule(object):
    ''' custom jinja2 filters for working with collections '''

    def filters(self):
        return {
            'int_hash': get_int_hash,
            'mysql_password': get_mysql_password,
        }