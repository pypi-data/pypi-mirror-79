#!/usr/bin/python
import codecs
from six import StringIO
import csv
from six import text_type as unicodestr

from django.conf import settings
try:
    use_session = settings.QUESTIONNAIRE_USE_SESSION
except AttributeError:
    use_session = False

def cmp(x, y):
    """
    Replacement for built-in function cmp that was removed in Python 3

    Compare the two objects x and y and return an integer according to
    the outcome. The return value is negative if x < y, zero if x == y
    and strictly positive if x > y.
    """

    return (x > y) - (x < y)

def split_numal(val):
    """Split, for example, '1a' into (1, 'a')
>>> split_numal("11a")
(11, 'a')
>>> split_numal("99")
(99, '')
>>> split_numal("a")
(0, 'a')
>>> split_numal("")
(0, '')
    """
    if not val:
        return 0, ''
    for i in range(len(val)):
        if not val[i].isdigit():
            return int(val[0:i] or '0'), val[i:]
    return int(val), ''

        

def numal_sort(a, b):
    """Sort a list numeric-alphabetically

>>> vals = "1a 1 10 10a 10b 11 2 2a z".split(" "); \\
... vals.sort(numal_sort); \\
... " ".join(vals)
'z 1 1a 2 2a 10 10a 10b 11'
    """
    anum, astr = split_numal(a)
    bnum, bstr = split_numal(b)
    cmpnum = cmp(anum, bnum)
    if(cmpnum == 0):
        return cmp(astr.lower(), bstr.lower())
    return cmpnum

def numal0_sort(a, b):
    """
    numal_sort on the first items in the list
    """
    return numal_sort(a[0], b[0])

def get_runid_from_request(request):
    if use_session:
        return request.session.get('runcode', None)
    else:
        return request.runinfo.run.runid

if __name__ == "__main__":
    import doctest
    doctest.testmod()

