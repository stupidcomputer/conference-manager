from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

from statistics import mean

class Person(models.Model):
    # generic stuff
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)

    # personal information
    phone_number = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    city = models.CharField(max_length=256)
    state = models.CharField(max_length=256)

class GeneralAssembly(models.Model):
    class Color(models.TextChoices):
        RED = 'RED', _('Red')
        WHITE = 'WHI', _('White')
        BLUE = 'BLU', _('Blue')
        NONE = 'NON', _('None')

    color = models.CharField(
        max_length=3,
        choices=Color.choices,
        default=Color.NONE,
    )
    docket = models.ArrayField(BillTeam)

class Committee(models.Model):
    number = models.IntegerField(default=1)
    docket = models.ArrayField(BillTeam)
    general_assembly = models.ForeignKey(GeneralAssembly)

class RollCallVoteResult(models.Model):
    all_for = models.IntegerField()
    all_against = models.IntegerField()
    all_abstaining = models.IntegerField()

class RankingVoteResult(models.Model):
    def average(self):
        return mean(
            [vote.average for vote in self.rankingvotes_set.all()]
        )
    
class RankingVotes(models.Model):
    field1 = models.IntegerField()
    field2 = models.IntegerField()
    field3 = models.IntegerField()
    field4 = models.IntegerField()
    field5 = models.IntegerField()
    result = models.ForeignKey(RankingVoteResult)

    def average(self):
        return sum(
            self.field1,
            self.field2,
            self.field3,
            self.field4,
            self.field5
        ) / 5

class BillVoteResults(models.Model):
    plenary = models.ForeignKey(RollCallVoteResult)
    general_assembly = models.ForeignKey(RollCallVoteResult)
    committee = models.ForeignKey(RankingVoteResult)

class Bill(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField()
    topic = models.CharField(max_length=256)
    votes = models.ForeignKey(BillVoteResults)

class BillTeam(models.Model):
    class Color(models.TextChoices):
        RED = 'RED', _('Red')
        WHITE = 'WHI', _('White')
        BLUE = 'BLU', _('Blue')
        NONE = 'NON', _('None')

    color = models.CharField(
        max_length=3,
        choices=Color.choices,
        default=Color.NONE,
    )
    delegates = models.ManyToManyField(Person)
    country = models.TextField(blank=True)
    bill = models.ForeignKey(Bill)
    committee = models.ForeignKey(Committee)

class MUNConference(models.Model):
    name = models.CharField(max_length=256)
    docket = models.ArrayField(BillTeam) # plenary docket

    def __str__(self):
        return self.name

