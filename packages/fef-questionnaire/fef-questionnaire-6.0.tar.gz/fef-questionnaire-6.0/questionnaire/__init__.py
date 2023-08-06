"""
questionnaire - Django Questionnaire App
========================================

Create flexible questionnaires.

Author: Robert Thomson <git AT corporatism.org>
"""

from django.dispatch import Signal

__all__ = ['question_proc', 'answer_proc', 'add_type', 'AnswerException',
           'questionset_done', 'questionnaire_done', ]

default_app_config = '{}.apps.QuestionnaireConfig'.format(__name__)

QuestionChoices = []
QuestionProcessors = {}  # supply additional information to the templates
Processors = {}  # for processing answers

questionnaire_start = Signal(providing_args=["runinfo", "questionnaire"])
questionset_start = Signal(providing_args=["runinfo", "questionset"])
questionset_done = Signal(providing_args=["runinfo", "questionset"])
questionnaire_done = Signal(providing_args=["runinfo", "questionnaire"])


class AnswerException(Exception):
    """Thrown from an answer processor to generate an error message"""
    pass
    
def question_proc(*names):
    """
    Decorator to create a question processor for one or more
    question types.

    Usage:
    @question_proc('typename1', 'typename2')
    def qproc_blah(request, question):
        ...
    """

    def decorator(func):
        global QuestionProcessors
        for name in names:
            QuestionProcessors[name] = func
        return func

    return decorator


def answer_proc(*names):
    """
    Decorator to create an answer processor for one or more
    question types.
    
    Usage:
    @question_proc('typename1', 'typename2')
    def qproc_blah(request, question):
        ...
    """

    def decorator(func):
        global Processors
        for name in names:
            Processors[name] = func
        return func

    return decorator


def add_type(id, name):
    """
    Register a new question type in the admin interface.
    At least an answer processor must also be defined for this
    type.
    
    Usage:
        add_type('mysupertype', 'My Super Type [radio]')
    """
    global QuestionChoices
    QuestionChoices.append((id, name))


