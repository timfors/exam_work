from django.db import models
from django.core import validators


# Create your models here.
class Question(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return u'%s' % self.text

    class Meta:
        ordering = ('id',)


class Planet(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return u'%s' % self.name

    class Meta:
        ordering = ('name',)


class Sith(models.Model):
    name = models.CharField(max_length=50, unique=True)
    planet = models.ForeignKey(Planet, on_delete=models.CASCADE)
    hands_count = models.IntegerField(default=0)
    max_hands = models.IntegerField(default=3)

    def __str__(self):
        return u'%s: %s' % (self.name, self.planet.name)

    class Meta:
        ordering = ('name',)



class Recruit(models.Model):
    name = models.CharField(max_length=50)
    planet = models.ForeignKey(Planet, on_delete=models.CASCADE)
    email = models.CharField(max_length=50, unique=True, validators=[validators.EmailValidator("Not an email")])
    age = models.IntegerField(default=1, validators=[validators.MinValueValidator(1, 'Incorrect age!')])

    def __str__(self):
        return u'%s - %s: %s' % (self.name, self.email, self.planet.name)


class Answer(models.Model):
    text = models.CharField(max_length=255)
    owner = models.ForeignKey(Recruit, on_delete=models.CASCADE)

    def __str__(self):
        return u'%s: %s' % (self.owner, self.text)

    class Meta:
        ordering = ('owner', 'id')
