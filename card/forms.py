import copy
from django import forms

class AnswerForm(forms.Form):
    pass

def cardform_factory(card, fieldobj):
    attrs = {}
    for answer in card.answer_set.order_by('pk'):
        field = copy.copy(fieldobj)
        field.label = answer.prompt or 'Answer'
        field.answer = answer.value
        attrs['field%s' % answer.pk] = field
    return type('AnswerForm%s' % card.key, (AnswerForm,), attrs)


def simple_factory(card):
    return cardform_factory(card, forms.CharField(max_length=128))


def selection_factory(card):
    options = ((item.split(',')[0], item.split(',')[1]) for item in card.data.split('|'))
    return cardform_factory(card, forms.ChoiceField(choices=options))


def multiselection_factory(card):
    attrs = {}
    for answer in card.answer_set.order_by('pk'):
        field = forms.ChoiceField(choices=((item.split(',')[0], item.split(',')[1]) for item in answer.data.split('|')))
        field.label = answer.prompt or 'Answer'
        field.answer = answer.value
        attrs['field%s' % answer.pk] = field
    return type('AnswerForm%s' % card.key, (AnswerForm,), attrs)

    
def build_answer_form(card):
    factoryname = '%s_factory' % card.factory or 'simple'
    
    try:
        form_factory = eval(factoryname)
    except NameError:
        form_factory = simple_factory
        
    return form_factory(card)


