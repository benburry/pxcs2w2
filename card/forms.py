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
    
    
def _positional_correct(self):
    if len(self.fields) == 0:
        return False
    pos = None
    for f in self:
        answers = f.field.answer.split(' ')
        if pos is None:
            for i in range(0, len(answers)):
                if re.match(answers[i], f.data.strip(), re.I) is not None:
                    pos = i
                    break
            else:
                return False
        else:
            if re.match(answers[pos], f.data.strip(), re.I) is None:
                return False
    return True
    
            
def add_field_attrs(field, answer):
    field.label = answer.prompt or 'What is the answer?'
    field.answer = answer.value


def cardform_factory(card, fieldobj):
    attrs = SortedDict()
    for answer in card.answers:
        field = copy.copy(fieldobj)
        add_field_attrs(field, answer)
        attrs['field%s' % answer.sequence or answer.pk] = field
    attrs['is_correct'] = _correct
    return type('AnswerForm%s' % card.key, (AnswerForm,), attrs)


def simple_factory(card):
    return cardform_factory(card, forms.CharField(max_length=128))


def selection_factory(card):
    options = ((item.split(',')[0], item.split(',')[1]) for item in card.data.split('|'))
    return cardform_factory(card, forms.ChoiceField(choices=options))


def multiselection_factory(card):
    attrs = SortedDict()
    for answer in card.answers:
        if answer.data:
            field = forms.ChoiceField(choices=((item.split(',')[0], item.split(',')[1]) for item in answer.data.split('|')))
        else:
            field = forms.CharField(max_length=128)
        add_field_attrs(field, answer)
        attrs['field%s' % answer.sequence or answer.pk] = field
    attrs['is_correct'] = _correct
    return type('AnswerForm%s' % card.key, (AnswerForm,), attrs)
    
    
def simplepositional_factory(card):
    attrs = SortedDict()
    for answer in card.answers:
        field = forms.CharField(max_length=128)
        add_field_attrs(field, answer)
        field.answer = answer.data
        attrs['field%s' % answer.sequence or answer.pk] = field
    attrs['is_correct'] = _positional_correct
    return type('AnswerForm%s' % card.key, (AnswerForm,), attrs)


def form106_factory(card):
    return cardform_factory(card, forms.CharField(max_length=1, widget=forms.TextInput(attrs={'size':'1'})))
    
    
def form147_factory(card):
    attrs = SortedDict()
    for answer in card.answers:
        field = forms.CharField(max_length=128, initial=answer.value[1].upper())
        add_field_attrs(field, answer)
        attrs['field%s' % answer.sequence or answer.pk] = field
    attrs['is_correct'] = _correct
    return type('AnswerForm%s' % card.key, (AnswerForm,), attrs)


def form205_factory(card):
    attrs = SortedDict()
    for answer in card.answers:
        if answer.data:
            field = forms.ChoiceField(choices=((item.split(',')[0], item.split(',')[1]) for item in answer.data.split('|')))
        else:
            field = forms.CharField(max_length=1, widget=forms.TextInput(attrs={'size':'1'}))
        add_field_attrs(field, answer)
        attrs['field%s' % answer.sequence or answer.pk] = field
    attrs['is_correct'] = _correct
    return type('AnswerForm%s' % card.key, (AnswerForm,), attrs)
    

def build_answer_form(card):
    factoryname = '%s_factory' % (card.factory or 'form%s' % card.key)
    print factoryname
    try:
        form_factory = eval(factoryname)
    except NameError:
        form_factory = simple_factory
        
    return form_factory(card)


