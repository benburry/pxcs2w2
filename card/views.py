import re
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import loader, Context, TemplateDoesNotExist
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from pxcs2w2.card.models import Card, SolverProfile
from pxcs2w2.card.forms import build_answer_form

@login_required
def view_card(request, card_id):
    card = get_object_or_404(Card, number=int(card_id))
    
    profile = get_profile(request)
    if profile.cansolve:
        formtype = build_answer_form(card)
    
        c = Context({'card': card})
        try:
            t = loader.get_template("card/view_%s.html" % card.key)
        except TemplateDoesNotExist:
            t = loader.get_template("card/view.html")
    
    
        if request.method == 'POST':
            form = formtype(request.POST)
            c['form'] = form
        
            if form.is_valid():       
                correct = True
                for match in (re.match(f.data, f.field.correct, re.I) for f in form):
                    correct = correct and match is not None
                    if not correct:
                        break
    
                c['correct'] = correct
                if correct:
                    del c['form']
                else:
                    profile.incr_attempt()
                
        else:
            form = formtype()
            c['form'] = form
        
    else:
        return HttpResponseRedirect(reverse('card_exceeded'))
        
    return HttpResponse(t.render(c))


def get_profile(request):
    try:
        profile = request.user.get_profile()
    except SolverProfile.DoesNotExist:
        profile = SolverProfile(user = request.user)
        profile.save()
    return profile

    
    
