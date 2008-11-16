import copy, re
from django.utils.datastructures import SortedDict
from django import forms

class AnswerForm(forms.Form):
    pass


def _correct(self):
    if len(self.fields) == 0:
        return False
        
    for match in (re.match(f.field.answer, f.data.strip(), re.I) for f in self):
        if match is None:
            return False
            
    return True
            
            
def add_field_attrs(field, answer):
    field.label = answer.prompt or 'Answer'
    field.answer = answer.value


def cardform_factory(card, fieldobj):
    attrs = SortedDict()
    for answer in card.answer_set.order_by('sequence'):
        field = copy.copy(fieldobj)
        add_field_attrs(field, answer)
        attrs['field%s' % answer.pk] = field
    attrs['is_correct'] = _correct
    return type('AnswerForm%s' % card.key, (AnswerForm,), attrs)


def simple_factory(card):
    return cardform_factory(card, forms.CharField(max_length=128))


def selection_factory(card):
    options = ((item.split(',')[0], item.split(',')[1]) for item in card.data.split('|'))
    return cardform_factory(card, forms.ChoiceField(choices=options))


def multiselection_factory(card):
    attrs = SortedDict()
    for answer in card.answer_set.order_by('pk'):
        if answer.data:
            field = forms.ChoiceField(choices=((item.split(',')[0], item.split(',')[1]) for item in answer.data.split('|')))
        else:
            field = forms.CharField(max_length=128)
        add_field_attrs(field, answer)
        attrs['field%s' % answer.pk] = field
    attrs['is_correct'] = _correct
    return type('AnswerForm%s' % card.key, (AnswerForm,), attrs)

    
def build_answer_form(card):
    factoryname = '%s_factory' % card.factory or 'simple'
    
    try:
        form_factory = eval(factoryname)
    except NameError:
        form_factory = simple_factory
        
    return form_factory(card)


