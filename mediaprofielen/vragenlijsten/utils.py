	#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Deze module bevat alle helper functies die in views gebruikt worden
"""
from django.contrib.auth.models import User
from models import QuestionBlock, Enquete, Question, QuestionChoice, Answer, ProfileText, Profiel

def getMaxPointsEnquete(enquete):
	# enquetes = Enquete.objects.all()
	result = {}
	for profiel in Question.profiel_choices:
		result[profiel[1]] = 0
	for block in  QuestionBlock.objects.filter(enquete=enquete):
		questions =Question.objects.filter(block = block)
		for question in questions:
			print question
	print result

# def getMaxPoints():
# 	result = {}
# 	for profiel in Question.profiel_choices:
# 		result[profiel[0]] = 0
# 	questions = Question.objects.all()
# 	for question in questions:
# 		choices = QuestionChoice.objects.filter(question=question)
# 		print question.profiel
# 		result[question.profiel] += len(choices) -1
# 	return result


def getMaxPoints():
	questions = Question.objects.all()
	result = {
	"Consument":0,
	"Verzamelaar":0,
	"Strateeg":0,
	"Netwerker":0,
	"Producent":0
	}
	for question in questions:
		choices = len(question.choices.all()) - 1
		if question.profiel == "Co":
			result["Consument"] += choices
		elif question.profiel == "Ve":
		  	result["Verzamelaar"] += choices
		elif question.profiel == "St":
		  	result["Strateeg"] += choices 
		elif question.profiel == "Ne":
		  	result["Netwerker"] += choices
		elif question.profiel == "On":
		  	result["Producent"] += choices
	return result

def addScore(user, id_of_last_block, id_invulmoment):
	print user, id_of_last_block
	enquete = Enquete.objects.filter(blocks__id=id_of_last_block)
	enquete_blocks = QuestionBlock.objects.filter(enquete=enquete)
	invulmoment = Invulmoment.objects.get(id=id_invulmoment)
	# profielObject = userObject.profiel.all()
	# If there is no profile, create one. Store the result in profielObject
	# if len(profielObject) == 0:
	# 	profielObjects = profielObject.create(user=userObject)
	# else:
	# 	profielObject = profielObject[0]
	# profielObject = userObject.profiel.all()[0]
	profielObject = Profiel.create(user=user, invulmoment=id_invulmoment)
	for block in enquete_blocks:
		answers = Answer.objects.filter(user=user, blockID=block)
		print answers
		questions = Question.objects.filter(block=block)
		answers_split = answers[0].answers.encode('ascii','ignore').split(",")
		print answers_split
		if len(answers_split) != len(questions):
			print "Something went terribly wrong"
			break
		for i in range(len(answers_split)):
			currentq = questions[i]
			currenta = answers_split[i]
			print currentq.profiel
			print currenta
			if int(currenta) > 3 and currentq.text:
				p = ProfileText(user= user, text= currentq.text, profiel = currentq.profiel)
				p.save()
			if int(currenta) < 0:
				print "question not relevant for profile (score negative)"
			elif currentq.profiel == "GE":
				print "question not relevant (No profile)"
			elif currentq.qType =="Y":
				print "question not relevant (yes/no)"
			elif currentq.profiel == "Co":
				profielObject.consument = profielObject.consument + int(currenta)
			elif currentq.profiel == "Ve":
			  	profielObject.verzamelaar = profielObject.verzamelaar + int(currenta)
			elif currentq.profiel == "St":
			  	profielObject.strateeg = profielObject.strateeg + int(currenta)  
			elif currentq.profiel == "Ne":
			  	profielObject.netwerker = profielObject.netwerker + int(currenta)
			elif currentq.profiel == "On":
			  	profielObject.producent = profielObject.producent + int(currenta)
	profielObject.save()
	

	# print getMaxPoints()
	# blockId = answer['blockID']
	# answers = answer['answers'].encode('ascii','ignore').split(",")
	
	# # Get the user
	# userObject = User.objects.get(username=user.username)
	
	# # Get the associated profiel
	# profielObject = userObject.profiel.all()
	# # If there is no profile, create one. Store the result in profielObject
	# if len(profielObject) == 0:
	# 	profielObjects = profielObject.create(user=userObject)
	# else:
	# 	profielObject = profielObject[0]
	# profielObject = userObject.profiel.all()[0]
	# # Get the block
	# questionBlock = QuestionBlock.objects.get(id=blockId)

	# questionList = questionBlock.questions.all()
	# # Iterate over the questions
	# for questionIndex in range(len(questionList)):
	# 	currentQuestion = questionList[questionIndex]
	# 	choices = currentQuestion.choices.all()
	# 	currentAnswer = int(answers[questionIndex])
	# 	currentChoice = choices[currentAnswer]
	# 	currentScore = currentChoice.score.all()
	# 	if len(currentScore) != 0:
	# 		currentScore = currentScore[0]
	# 	else:
	# 		print "er is geen score!"
	# 		# New object!
	# 		currentScore = ChoiceScores()
	# 	profielObject.consument = profielObject.consument + currentScore.consument
	# 	profielObject.verzamelaar = profielObject.verzamelaar + currentScore.verzamelaar
	# 	profielObject.strateeg = profielObject.strateeg + currentScore.strateeg
	# 	profielObject.netwerker = profielObject.netwerker + currentScore.netwerker
	# 	profielObject.producent = profielObject.producent + currentScore.producent
	# 	profielObject.save()
	# completedblocks = profielObject.completedBlocks.encode('utf-8', 'None')
	# if completedblocks:
	# 	completedblocks = completedblocks + "," + str(blockId)
	# else:
	# 	completedblocks = blockId
	# print completedblocks
	# profielObject.completedBlocks = completedblocks
	# profielObject.save()
	
	

