from rest_framework import viewsets, permissions, generics, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import detail_route, list_route
from serializers import *
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from models import *
from utils import addScore, getMaxPoints, getEnquetes
import csv, unicodedata
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404, render
from django import forms
from mailchimp_utils import getLists, makeOrganisation, addUsersOrganisation
import random
from django.contrib.admin.views.decorators import staff_member_required

class ManageForm(forms.Form):
    organisatie_naam = forms.CharField(max_length = 100, required = False)
    # mailchimp_lijst = forms.ChoiceField(choices = getLists())
    # enquete_id = forms.ChoiceField(choices = getEnquetes())

    def __init__(self, *args, **kwargs):
        super(ManageForm, self).__init__(*args, **kwargs)
        self.fields['mailchimp_lijst'] = forms.ChoiceField(choices = getLists())
        self.fields['enquete_id'] = forms.ChoiceField(choices= getEnquetes())


@staff_member_required
def manageView(request):
    if request.method == "POST":
        form = ManageForm(request.POST)
        if form.is_valid():
            formdata = form.cleaned_data
            r = lambda: random.randint(0,255)
            color = '#%02X%02X%02X' % (r(),r(),r())
            org_check = Organisation.objects.filter(name=formdata['organisatie_naam'])
            if org_check.count() == 0:
                result = makeOrganisation(formdata['organisatie_naam'], formdata['mailchimp_lijst'], formdata['enquete_id'], color)
                if result != True:
                    return render(request, 'vragenlijsten/manage.html', {'message':result})
                else:
                    return render(request, 'vragenlijsten/manage.html', {'message':"Organisatie toegevoegd!"})
            else:
                result = addUsersOrganisation(formdata['organisatie_naam'], formdata['mailchimp_lijst'], formdata['enquete_id'])
                if result == True:
                    return render(request, 'vragenlijsten/manage.html', {'message':"Alle gebruikers toegevoegd en voorzien van wachtwoord!"})
                else:
                    return render(request, 'vragenlijsten/manage.html', {'message':result})
        else:
            return render(request, 'vragenlijsten/manage.html', {'message':"Verkeerde input!"})
    form = ManageForm() 
    return render(request, 'vragenlijsten/manage.html', {'form':form})

@login_required
def index(req):
    return HttpResponse("Hello")

def question(req, id):
    return HttpResponse(id)

class currentUserView(APIView):
    """
    Return the information of the current authenticated user (Is this a hackz?)
    http://stackoverflow.com/questions/15770488/return-the-current-user-with-django-rest-framework
    """
    def get(self, request):
        user=request.user
        serialized = UserSerializer(user, context={'request':request})
        returndata = {}
        returndata['user'] = serialized.data
        try:
            invulmoment = user.members.all()[0].organisationInvulMoment.all().latest('time')
            serializedIM = InvulMomentSerializer(invulmoment, context={'request':request})
            returndata['invulmoment'] = serializedIM.data
            if user.profiel.filter(invulmoment=invulmoment).count() > 0:
                returndata['invulmoment_ingevuld'] = True
            else:    
                returndata['invulmoment_ingevuld'] = False
        except IndexError:
            returndata['invulmoment'] = {}
        return Response(returndata)

class changePasswordView(APIView):
    def post(self, request):
        print request.user
        x = request.data["password"]
        request.user.set_password(x)
        request.user.save()
        return Response("Password Changed!")


def get_highest_profile(profiel):
    consument = ('consument', profiel.consument)
    verzamelaar = ('verzamelaar', profiel.verzamelaar)
    strateeg = ('strateeg', profiel.strateeg)
    netwerker = ('netwerker', profiel.netwerker)
    producent = ('producent', profiel.producent)
    if [consument[1],verzamelaar[1],strateeg[1],netwerker[1],producent[1]] == [0,0,0,0,0]:
        return ('geen profiel')
    else:
        return max([consument,verzamelaar,strateeg,netwerker,producent], key=lambda t: t[1])[0]

def sumProfiles(profiles):
    pointCount = {'consument':0,
                  'verzamelaar':0,
                  'strateeg':0,
                  'netwerker':0,
                  'producent':0}
    for profile in profiles:
        pointCount['consument'] += profile.consument
        pointCount['verzamelaar'] += profile.verzamelaar
        pointCount['strateeg'] += profile.strateeg
        pointCount['netwerker'] += profile.netwerker
        pointCount['producent'] += profile.producent
    return pointCount

class currentOrganisationView(APIView):
    def get(self, request):
        user            = request.user
        owned_organisations   = user.owners.all()
        if owned_organisations:
            organisationList = []
            for i, organisation in enumerate(owned_organisations):
                orgDict = {} #Deze dict is voor alle info over de organisatie
                orgDict['Name'] = organisation.name
                orgDict['Id'] = organisation.id
                orgDict['invulmomenten'] = []
                orgDict['Owners'] = map(lambda x: str(x), organisation.owners.all())
                membercount = organisation.members.count()
                membercountprofile = organisation.members.filter(profiel__isnull=False).distinct().count()
                print "membercountprofile:", membercountprofile
                orgDict['memberCount'] = membercount
                for invulmoment in organisation.organisationInvulMoment.all():
                    invulmomentTemp = {}
                    invulmomentTemp['id']   = invulmoment.id 
                    invulmomentTemp['datum'] = invulmoment.time
                    invulmomentTemp['enquete'] = invulmoment.enquete.id
                    invulmomentTemp['ingevuldCount'] = invulmoment.invulmomentprofiel.count()
                    profileCount = {'geen profiel':0,
                                    'consument':0,
                                    'verzamelaar':0,
                                    'strateeg':0,
                                    'netwerker':0,
                                    'producent':0}
                    profielen = invulmoment.invulmomentprofiel.all()
                    for profiel in profielen:
                            profileCount[get_highest_profile(profiel)] += 1
                    invulmomentTemp['profielCount'] = profileCount
                    totalcount = sumProfiles(profielen)
                    invulmomentTemp['totalCount'] = totalcount
                    if membercountprofile > 0:
                        invulmomentTemp['averageCount'] = {k: float(v)/membercountprofile for k, v in totalcount.items()}
                    else:
                        invulmomentTemp['averageCount'] = {k: 0 for k, v in totalcount.items()}
                    orgDict['invulmomenten'].append(invulmomentTemp)
                organisationList.append(orgDict)
            return Response(organisationList)
        else:
            return Response("This user is no owner!")


def csv_view(request, index):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="mediaprofielen.csv"'
    try:
        user            = request.user
        organisations   = user.owners.filter(id=index)
        writer = csv.writer(response, delimiter=';')
        writer.writerow(['gebruikersnaam', 'voornaam', 'achternaam', 'geslacht', 'leeftijd', 'opleiding', 'provincie', 'consument', 'verzamelaar', 'strateeg', 'netwerker', 'producent'] + get_blocks_list())
        for member in organisations[0].members.all():
            try:
                writer.writerow([unicodedata.normalize('NFKD',member.username).encode('ascii','ignore'), unicodedata.normalize('NFKD',member.account.first_name).encode('ascii','ignore'), unicodedata.normalize('NFKD',member.account.last_name).encode('ascii','ignore'), member.account.geslacht, member.account.leeftijd, member.account.opleiding, member.account.provincie, member.profiel.all()[0].consument, member.profiel.all()[0].verzamelaar, member.profiel.all()[0].strateeg, member.profiel.all()[0].netwerker, member.profiel.all()[0].producent] + get_blocks_score(member))
            except Account.DoesNotExist:
                writer.writerow([unicodedata.normalize('NFKD',member.username).encode('ascii','ignore'), "Niet beschikbaar", "Niet beschikbaar", "Niet beschikbaar", "Niet beschikbaar", "Niet beschikbaar", "Niet beschikbaar", member.profiel.all()[0].consument, member.profiel.all()[0].verzamelaar, member.profiel.all()[0].strateeg, member.profiel.all()[0].netwerker, member.profiel.all()[0].producent] + get_blocks_score(member))
        return response
    except IndexError:
        return HttpResponse("Invalid Index!")

def csv_answer_view(request, inv_id):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="mediaprofielen_invulmoment_' + inv_id + '.csv"'
    try:
        user = request.user
        organisations = user.owners.all()
        csv_header = [u'gebruikersnaam', u'voornaam', u'achternaam', u'geslacht', u'leeftijd', u'opleiding', u'provincie', u'consument', u'verzamelaar', u'strateeg', u'netwerker', u'producent']
        writer = csv.writer(response, delimiter=';')

        current_invulmoment = Invulmoment.objects.get(id=inv_id)
        if not current_invulmoment.organisation in organisations:
            return HttpResponseForbidden("Not the owner of this organisation")
        current_enquete =  current_invulmoment.enquete
        current_blocks = current_enquete.blocks.all()
        user_answer_dict = {}
        users = current_invulmoment.organisation.members.all()
        for user in users:
            user_answer_dict[user.username] = []
        print users
        for block in current_blocks:
            for question in block.questions.all():
                csv_header.append(question.questionText)
            for user in users:
                try:
                    answer = block.blockanswers.get(invulmoment=current_invulmoment, user=user)
                    user_answer_dict[user.username] += (answer.answers.split(","))
                except Answer.DoesNotExist:
                    user_answer_dict[user.username] += ["Niet beschikbaar" for question in block.questions.all()]
        writer.writerow(map(lambda s: unicodedata.normalize('NFKD', s).encode('ascii','ignore'), csv_header))
        for key, value in user_answer_dict.items():
            user = User.objects.get(username=key)
            try:
                user_profile = user.profiel.get(invulmoment=current_invulmoment)
                profiel_part = [user_profile.consument, user_profile.verzamelaar, user_profile.strateeg, user_profile.netwerker, user_profile.producent]
            except Profiel.DoesNotExist:
                profiel_part = ["Niet beschikbaar", "Niet beschikbaar", "Niet beschikbaar", "Niet beschikbaar", "Niet beschikbaar"]
            except Profiel.MultipleObjectsReturned:
                user_profile = user.profiel.filter(invulmoment=current_invulmoment)
                # DELETE DOUBLE ACCOUNTS, THIS IS A BUG THAT SHOULD BE FIXED!
                for fake in user_profile[:len(user_profile)]:
                    fake.delete()
                user_profile = user_profile[len(user_profile)]
                profiel_part = [user_profile.consument, user_profile.verzamelaar, user_profile.strateeg, user_profile.netwerker, user_profile.producent]
            try:
                writer.writerow([unicodedata.normalize('NFKD',user.username).encode('ascii','ignore'), unicodedata.normalize('NFKD',user.account.first_name).encode('ascii','ignore'), unicodedata.normalize('NFKD',user.account.last_name).encode('ascii','ignore'), user.account.geslacht, user.account.leeftijd, user.account.opleiding, user.account.provincie] + profiel_part + value)
            except Account.DoesNotExist:
                writer.writerow([unicodedata.normalize('NFKD',user.username).encode('ascii','ignore'), "Niet beschikbaar", "Niet beschikbaar", "Niet beschikbaar", "Niet beschikbaar", "Niet beschikbaar", "Niet beschikbaar"]+ profiel_part + value)
        return response
    except Invulmoment.DoesNotExist:
        return HttpResponseBadRequest("No invulmoment with that id!")



def get_blocks_list():
    blocks = QuestionBlock.objects.all()
    result = []
    for block in blocks:
        result.append(block.name)
    return result

def get_blocks_score(user):
    result = []
    blocks = QuestionBlock.objects.all()
    for block in blocks:
        answer  = Answer.objects.filter(user=user, blockID=block.id)
        if answer:
            blockscore = 0
            answers_split = answer[0].answers.encode('ascii','ignore').split(",")
            for score in answers_split:
                if int(score) > 0:
                    blockscore += int(score)
            result.append(blockscore)
        else:
            result.append("Niet ingevuld")
    return result





class maxPointsView(APIView):
    def get(self, request, enquete_id):
        enquete = get_object_or_404(Enquete, id=enquete_id)
        x = getMaxPoints(enquete) 
        return Response(x)


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    filter_fields = ('leeftijd', 'opleiding', 'geslacht')

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class EnqueteViewSet(viewsets.ModelViewSet):
    queryset = Enquete.objects.all()
    serializer_class = EnqueteSerializer

class BlockViewSet(viewsets.ModelViewSet):
    queryset = QuestionBlock.objects.all()
    serializer_class = BlockSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return AnswerCreateSerializer
        return AnswerSerializer

    def perform_create(self, serializer):
        Answer.objects.filter(user=self.request.user, blockID=serializer.validated_data['blockID'], invulmoment=serializer.validated_data['invulmoment']).delete()
        serializer.save(user=self.request.user)
        if 'last' in self.request.data:
            if self.request.data['last'] == "true":
                if 'invulmoment' in self.request.data:
                    print "invulmomentid gekregen:"
                    print self.request.data['invulmoment']
                addScore(self.request.user, serializer.data['blockID'], self.request.data['invulmoment'])

class OrganisationViewSet(viewsets.ModelViewSet):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    filter_fields = ('owners','members')

class InvulmomentViewSet(viewsets.ModelViewSet):
    queryset = Invulmoment.objects.all()
    serializer_class = InvulMomentSerializer