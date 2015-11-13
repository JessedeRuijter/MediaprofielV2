from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from validate_email import validate_email

class Account(models.Model):
	user = models.OneToOneField(User)
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	geslacht_choices = (('M', "Man"),('V', "Vrouw"))
	geslacht = models.CharField(max_length='1', choices=geslacht_choices)
	leeftijd = models.IntegerField()
	opleiding_choices = ((None, 'Geen opleiding'), ('HA', "Havo"), ('VW', 'VWO'), ('MB', 'MBO'), ('HB', 'HBO'), ('WO', "WO"))
	opleiding = models.CharField(max_length='2', choices=opleiding_choices)
	provincie_choices = (
		(None, 'Geen provincie'),
		('GR', 'Groningen'),
		('FR', 'Friesland'),
		('DR', 'Drenthe'),
		('OV', 'Overijssel'),
		('FL', 'Flevoland'),
		('GE', 'Gelderland'),
		('UT', 'Utrecht'),
		('NO', 'Noord-Holland'),
		('ZU', 'Zuid-Holland'),
		('ZE', 'Zeeland'),
		('NB', 'Noord-Brabant'),
		("LI", "Limburg"),
		("BE", "Belgie"),
		("DU", "Duitsland"),
		("FA", "Frankrijk"),
		("VE", "Verenigd Koningkrijk"),
		("LU", "Luxemburg"),
		("AN", "Andere"))
	provincie = models.CharField(max_length='2', choices=provincie_choices)

# De vragen in database
class Enquete(models.Model):
	name 			= models.CharField(max_length=200)
	description 	= models.TextField()
	publishedDate 	= models.DateTimeField('date published')
	locked          = models.BooleanField(default=False)
	def __unicode__(self):
		return self.name

class Organisation(models.Model):
	name = models.CharField(max_length=200)
	color = models.CharField(max_length=100)
	owners = models.ManyToManyField(User, related_name="owners", blank=True)
	members = models.ManyToManyField(User, related_name="members", blank=True)
	def __unicode__(self):
		return str(self.name)

class Invulmoment(models.Model):
	organisation = models.ForeignKey(Organisation, related_name='organisationInvulMoment')
	time = models.DateField()
	enquete = models.ForeignKey(Enquete, related_name='enquete')
	def __unicode__(self):
		return ':'.join([str(self.time), str(self.organisation.name), str(self.enquete.name)])

class QuestionBlock(models.Model):
	enquete 	= models.ForeignKey(Enquete, related_name='blocks')
	name 		= models.CharField(max_length=200)
	description = models.TextField()
	def __unicode__(self):
		return str(self.id)

class Question(models.Model):
	block 			= models.ForeignKey(QuestionBlock, related_name='questions')
	questionText 	= models.TextField()
	typeChoices 	= (("Y", "YesNo"), ("M", "MultipleChoice"), ("S", "Slider"))
	qType 			= models.CharField(max_length=1, choices=typeChoices)
	offset			= models.IntegerField(default=-1)
	text			= models.CharField(max_length=200, blank=True)
	profiel_choices  = (
		("GE", "Geen profiel"),
		("Co","Consument"),
		("Ve", "Verzamelaar"),
		("St", "Strateeg"),
		("Ne", "Netwerker"),
		("On", "Ontwerper"))
	profiel = models.CharField(max_length='2', choices=profiel_choices)
	def __unicode__(self):
		return self.questionText

class ProfileText(models.Model):
	user = models.ForeignKey(User, related_name="texts")
	text = models.CharField(max_length=200)
	profiel_choices  = (
		("GE", "Geen profiel"),
		("Co","Consument"),
		("Ve", "Verzamelaar"),
		("St", "Strateeg"),
		("Ne", "Netwerker"),
		("On", "Ontwerper"))
	profiel = models.CharField(max_length='2', choices=profiel_choices)

# De antwoorden per user per enquete
class Answer(models.Model):
	"""Antwoorden op questionblocks"""
	user = models.ForeignKey(User)
	blockID = models.ForeignKey(QuestionBlock)
	answers = models.CharField(max_length=1000)
	def __unicode__(self):
		return str(self.user) + " " + str(self.blockID) + " " + str(self.answers)

# Dit model is een volledig ingevulde enquete!
class EnqueteAnswer(models.Model):
	"""Antwoorden op een enquete"""
	user = models.ForeignKey(User)
	answers = models.CommaSeparatedIntegerField(max_length=1000)
	invulmoment = models.ForeignKey(Invulmoment, related_name='invulmoment', blank=True)

class QuestionChoice(models.Model):
	question 		= models.ForeignKey(Question, related_name='choices')
	choiceText 		= models.CharField(max_length=200)

class Profiel(models.Model):
	"""Scores bij profielen en een historie van completed blocks"""
	invulmoment		= models.ForeignKey(Invulmoment, related_name='invulmomentprofiel')
	user 			= models.ForeignKey(User, related_name='profiel')
	consument    	= models.IntegerField(default=0)
	verzamelaar 	= models.IntegerField(default=0)
	strateeg    	= models.IntegerField(default=0)
	netwerker   	= models.IntegerField(default=0)
	producent   	= models.IntegerField(default=0)
	def __unicode__(self):
		return str(self.consument)+ " " + str(self.verzamelaar)+ " " + str(self.strateeg)+ " " + str(self.netwerker)+ " " + str(self.producent)


# Signals:

# @receiver(post_save, sender=User)
# def user_save_handler(sender, **kwargs):
# 	if kwargs['created']:
# 		newUser = kwargs['instance']
# 		newProfile = Profiel(user=newUser)
# 		newProfile.save()
	# user = kwargs['instance']
	# password = User.objects.make_random_password()
	# message = "Welkom bij Mediaprofielen {0}, je wachtwoord is {1} ".format(user.username, password)
	# print message
	# # send_mail('Welkom bij Mediaprofielen', 'Here is the message.', 'from@example.com',
 # #    ['to@example.com'], fail_silently=False)
	# user.set_password(password)

# @receiver(post_save, sender=Organisation)
# def organisation_save_handler(sender, **kwargs):
# 	organisation = kwargs['instance']
# 	organisation.csvMembers.open(mode='rb')
# 	organisation.csvOwners.open(mode='rb')
# 	for line in organisation.csvMembers.read().splitlines(): 
# 		if validate_email(line):
# 			print "Valid:"
# 			print line
# 			password = User.objects.make_random_password()
# 			if User.objects.filter(username=line):
# 				newUser = User.objects.filter(username=line)[0]
# 			else:
# 				newUser = User(username=line.lower(), email=line)
# 				newUser.set_password(password)
# 				# message = "Welkom bij Mediaprofielen {0}, je wachtwoord is {1} ".format(newUser.username, password)
# 				# send_mail('Welkom bij Mediaprofielen', message, 'mediaprofielen', [line], fail_silently=False)
# 				newUser.save()
# 			organisation.members.add(newUser)
# 		else:
# 			print "Non valid email:"
# 			print line
# 	for line in organisation.csvOwners.readlines():
# 		if validate_email(line):
# 			print "Valid:"
# 			print line
# 			password = User.objects.make_random_password()
# 			if User.objects.filter(username=line):
# 				newUser = User.objects.filter(username=line)[0]
# 			else:
# 				newUser = User(username=line.lower(), email=line)
# 				newUser.set_password(password)
# 				# message = "Welkom bij Mediaprofielen {0}, je wachtwoord is {1} ".format(newUser.username, password)
# 				# send_mail('Welkom bij Mediaprofielen', message, 'mediaprofielen', [line], fail_silently=False)
# 				newUser.save()
# 			organisation.owners.add(newUser)
# 		else:
# 			print "Non valid email:"
# 			print line