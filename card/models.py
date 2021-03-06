import datetime
from django.db import models
from django.contrib.auth.models import User

CARD_COLOURS = (
    ('Red', 'Red'),
    ('Orange', 'Orange'),
    ('Yellow', 'Yellow'),
    ('Green', 'Green'),
    ('Blue', 'Blue'),
    ('Purple', 'Purple'),
    ('Black', 'Black'),
    ('Silver', 'Silver'),
)

class Card(models.Model):
    number = models.PositiveSmallIntegerField(unique=True)
    name = models.CharField(max_length=64)
    colour = models.CharField(max_length=16, choices=CARD_COLOURS)
    hint = models.CharField(max_length=256, null=True, blank=True)
    notes = models.CharField(max_length=256, null=True, blank=True)
    question = models.CharField(max_length=256,null=True, blank=True)
    factory = models.CharField(max_length=16, null=True, blank=True)
    data = models.CharField(max_length=256, null=True, blank=True)
    
    def __unicode__(self):
        return "#%s - %s" % (self.key, self.name)
        
    @models.permalink
    def get_absolute_url(self):
        return ('card_view', [self.key])
        
    @property
    def key(self):
        return "%03u" % self.number
        
    @property
    def answers(self):
        return self.answer_set.order_by('sequence', 'prompt')
        
    class Meta:
        ordering = ["number"]


class Answer(models.Model):
    card = models.ForeignKey(Card)
    prompt = models.CharField(max_length=64, null=True, blank=True)
    value = models.CharField(max_length=128)
    data = models.CharField(max_length=256, null=True, blank=True)
    sequence = models.PositiveSmallIntegerField(null=True, blank=True)
    
    def __unicode__(self):
        return self.value
        
    class Meta:
        ordering = ['sequence','pk']
        order_with_respect_to = 'card'


class CardSolve(models.Model):
    user = models.ForeignKey(User)
    card = models.ForeignKey(Card)
    solved = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = (('user', 'card'),)
        ordering = ['solved',]


class SolveAttempt(models.Model):
    user = models.ForeignKey(User)
    card = models.ForeignKey(Card)
    
    solve_start = models.DateTimeField(auto_now_add=True)
    attempt_count = models.PositiveSmallIntegerField(default=0)
    
    class Meta:
        unique_together = (('user', 'card'),)
    
    def _expired(self):
        if self.solve_restart:
            return datetime.datetime.now() >= self.solve_restart
        return True

    @property
    def cansolve(self):
        return self._expired() or self.attempt_count < 3
        
    @property
    def solve_restart(self):
        if self.solve_start:
            return self.solve_start + datetime.timedelta(days=1)
        return None
        
    def incr_attempt(self):
        if self._expired():
            self.solve_start = datetime.datetime.now()
            self.attempt_count = 1
        else:
            self.attempt_count += 1
        self.save()
        
