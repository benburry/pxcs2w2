import re, datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import loader, Context, TemplateDoesNotExist
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from pxcs2w2.card.models import Card, CardSolve, SolveAttempt
from pxcs2w2.card.forms import build_answer_form


def solved_cards(request, username):
    user = get_object_or_404(User, username=username)
    solves = CardSolve.objects.filter(user=user)
    return render_to_response('card/solves.html', {'solves': solves})


def card_list(request):
    cards = Card.objects.all()
    
    if request.user.is_authenticated():
        card_dict = {}
        for card in cards:
            card_dict[card.pk] = card
        
        solves = CardSolve.objects.filter(user = request.user)
        for solve in solves:
            card_dict[solve.card_id].solved = True
    
    return render_to_response('index.html', {'card_list': cards})


@login_required
def view_card(request, card_id):
    card = get_object_or_404(Card, number=int(card_id))
    
    attempt = get_attempt(request, card)
    if attempt.cansolve:
        formtype = build_answer_form(card)
    
        c = Context({'card': card})
        t = loader.select_template(["card/view_%s.html" % card.key, 'card/view.html'])
        
        if request.method == 'POST':
            form = formtype(request.POST)
            c['form'] = form
        
            if form.is_valid():       
                correct = form.is_correct()
    
                c['correct'] = correct
                if correct:
                    del c['form']
                    try:
                        solve = CardSolve.objects.get(user=request.user, card=card)
                    except CardSolve.DoesNotExist:
                        solve = CardSolve(user=request.user, card=card)
                        solve.save()
                    
                else:
                    attempt.incr_attempt()
                
        else:
            form = formtype()
            c['form'] = form
        
    else:
        return render_to_response('card/exceeded.html', {'card': card})
        
    return HttpResponse(t.render(c))


def get_attempt(request, card):
    try:
        attempt = SolveAttempt.objects.get(user = request.user, card = card)
    except SolveAttempt.DoesNotExist:
        attempt = SolveAttempt(user = request.user, card = card)
    return attempt

    
    
