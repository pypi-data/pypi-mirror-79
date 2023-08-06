import ast
from json import dumps
from django.conf import settings
from django.utils.translation import ugettext as _
from ..utils import get_runid_from_request
from .. import add_type, question_proc, answer_proc, AnswerException

@question_proc('range', 'number')
def question_range_or_number(request, question):
    cd = question.getcheckdict()
    
    rmin, rmax = parse_range(cd)
    rstep = parse_step(cd)
    runit = cd.get('unit', '')
    
    #try loading current from database before just setting to min
    possibledbvalue = question.get_value_for_run_question(get_runid_from_request(request))
    
    #you can't eval none nor can you eval empty
    if not possibledbvalue == None and len(possibledbvalue) > 0:
        valueaslist = ast.literal_eval(possibledbvalue)
        current = valueaslist[0]
    else:        
        current = request.POST.get('question_%s' % question.number, rmin)   

    jsinclude = []
    if question.type == 'range':
        jsinclude = [settings.STATIC_URL+'range.js']

    return {
        'required' : True,
        'type': question.type,
        'rmin' : rmin,
        'rmax' : rmax,
        'rstep' : rstep,
        'runit' : runit,
        'current' : current,
        'jsinclude' : jsinclude
    }

@answer_proc('range', 'number')
def process_range_or_number(question, answer):
    cd = question.getcheckdict()

    rmin, rmax = parse_range(cd)
    rstep = parse_step(cd)

    convert = range_type(rmin, rmax, rstep)

    ans = answer['ANSWER']
    if not ans:
        required = question.getcheckdict().get('required', 0)
        if required:
            raise AnswerException(_(u"Field cannot be blank"))
        else:
            return []

    try:
        ans = convert(ans)
    except:
       raise AnswerException(_(u"Could not convert the number"))
    
    if ans > convert(rmax) or ans < convert(rmin):
        raise AnswerException(_(u"Out of range"))

    return dumps([ans])

add_type('range', 'Range of numbers [select]')
add_type('number', 'Number [input]')

def parse_range(checkdict):
    "Given a checkdict for a range widget return the min and max string values."

    Range = checkdict.get('range', '1-5')

    try:
        rmin, rmax = Range.split('-', 1)
    except ValueError:
        rmin, rmax = '1', '5'

    return rmin, rmax

def parse_step(checkdict):
    "Given a checkdict for a range widget return the step as string value."

    return checkdict.get('step', '1')

def range_type(rmin, rmax, step):
    """Given the min, max and step value return float or int depending on
    the number of digits after 0.

    """

    if any((digits(rmin), digits(rmax), digits(step))):
        return float
    else:
        return int

def digits(number):
    "Given a number as string return the number of digits after 0."
    if '.' in number or ',' in number:
        if '.' in number:
            return len(number.split('.')[1])
        else:
            return len(number.split(',')[1])
    else:
        return 0
