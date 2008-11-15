from django import forms

class AnswerForm(forms.Form):
    pass
    
def build_answer_form(card):
    classname = 'AnswerForm%s' % card.key
    
    try:
        formtype = eval(classname)
    except NameError:
        attrs = {}
        for answer in card.answer_set.order_by('key'):
            field = forms.CharField(max_length=128)
            field.correct = answer.value
            attrs[answer.key] = field
        formtype = type(classname, (AnswerForm,), attrs)
        
    return formtype


