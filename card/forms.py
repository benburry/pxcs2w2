from django import forms

class AnswerForm(forms.Form):
    pass
    
def build_answer_form(card):
    
    attrs = {}
    for answer in card.answer_set.order_by('key'):
        field = forms.CharField(max_length=128)
        field.correct = answer.value
        attrs[answer.key] = field

    return type('AnswerForm%s' % card.key, (AnswerForm,), attrs)


