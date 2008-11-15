from django import forms

class AnswerForm(forms.Form):
    pass
    
def build_answer_form(card):
    
    attrs = {}
    for answer in card.answer_set.order_by('key'):
        attrs[answer.key] = forms.CharField(max_length=128)

    return type('AnswerForm%s' % card.key, (AnswerForm,), attrs)()


