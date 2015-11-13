from rest_framework import serializers
from django.contrib.auth.models import User
from models import *


class InvulmomentMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invulmoment
        fields = ('id', 'time')

class ProfielSerializer(serializers.ModelSerializer):
    invulmoment = InvulmomentMinSerializer()
    class Meta:
        model = Profiel
        fields = ('invulmoment', 'user', 'consument','verzamelaar','strateeg', 'netwerker', 'producent')
            
class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ('user','first_name', 'last_name', 'geslacht', 'leeftijd', 'opleiding', 'provincie')

class ProfileTextSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProfileText
        fields = ('user', 'text', 'profiel')

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    profiel = ProfielSerializer(many=True)
    account = AccountSerializer(read_only=True)
    texts = ProfileTextSerializer(many=True)
    class Meta:
        model = User
        fields = ('id','url', 'username', 'email', 'is_staff', 'first_name', 'last_name', 'account', 'profiel', 'texts')


class OrganisationSerializer(serializers.ModelSerializer):
    owners = UserSerializer(many=True)
    members = UserSerializer(many=True)
    class Meta:
        model = Organisation
        fields = ('id', 'url', 'name', 'owners', 'members')

# De serializers voor de enquetes
class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionChoice
        fields = ('id', 'choiceText')

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = ('id', 'questionText', 'qType', 'offset', 'text', 'choices')

class BlockSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    class Meta:
        model = QuestionBlock
        fields = ('id', 'name', 'description', 'questions')


class EnqueteSerializer(serializers.ModelSerializer):
    blocks = serializers.StringRelatedField(many=True)
    class Meta:
        model = Enquete
        fields = ('url', 'id', 'name', 'description', 'publishedDate', 'locked', 'blocks')

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id','invulmoment','user','blockID', 'answers')

class AnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('blockID', 'answers')

class OrganisationNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ('id','name')

class InvulMomentSerializer(serializers.ModelSerializer):
    organisation = OrganisationNameSerializer()
    enquete = EnqueteSerializer()
    class Meta:
        model = Invulmoment
        fields = ('id','organisation', 'time', 'enquete')
