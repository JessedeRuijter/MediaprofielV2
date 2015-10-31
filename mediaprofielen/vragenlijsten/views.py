from rest_framework import viewsets, permissions, generics, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import detail_route, list_route
from serializers import *
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from models import *
from utils import addScore, getMaxPoints
import csv, unicodedata
from django.contrib.auth import logout

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
        except IndexError:
            returndata['invulmoment'] = "None"
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
        member_organisations = user.members.all()
        if owned_organisations:
            organisationDict = {}
            for i, organisation in enumerate(owned_organisations):
                orgDict = {} #Deze dict is voor alle info over de organisatie
                orgDict['Type'] = 'Owner'
                orgDict['Name'] = organisation.name
                orgDict['Id'] = organisation.id
                profileCount = {'geen profiel':0,
                                'consument':0,
                                'verzamelaar':0,
                                'strateeg':0,
                                'netwerker':0,
                                'producent':0}
                for member in organisation.members.all():
                        profileCount[get_highest_profile(member.profiel.all()[0])] += 1
                orgDict['profileCount'] = profileCount
                organisationDict["Organisation" + str(i+1)] = orgDict
                orgDict['totalCount'] = sumProfiles(Profiel.objects.filter(user =organisation.members.all()))
                orgDict['averageCount'] = {}
                for key, value in orgDict['totalCount'].items():
                    orgDict['averageCount'][key] = float(value) / organisation.members.count()
            return Response(organisationDict.values())
        if member_organisations:
            serialized = OrganisationSerializer(member_organisations[0], context={'request': request})
            return Response(serialized.data)
        else:
            return Response("No organisation owner/member.")


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
    def get(self, request):
        x = getMaxPoints()
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
        Answer.objects.filter(user=self.request.user, blockID=serializer.data['blockID']).delete()
        serializer.save(user=self.request.user)
        if 'last' in self.request.data:
            print "hai!"
            if self.request.data['last'] and self.request.data['invulmoment']:
                addScore(self.request.user, serializer.data['blockID'], self.request.data['invulmoment'])

class OrganisationViewSet(viewsets.ModelViewSet):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    filter_fields = ('owners','members')

class InvulmomentViewSet(viewsets.ModelViewSet):
    queryset = Invulmoment.objects.all()
    serializer_class = InvulMomentSerializer