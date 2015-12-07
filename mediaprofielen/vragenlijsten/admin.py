from django.contrib import admin
from vragenlijsten.models import *
from nested_inline.admin import NestedStackedInline, NestedModelAdmin, NestedTabularInline
from django.core.management import call_command
from django.contrib import admin
from ajax_select import make_ajax_form

class ChoiceInline(NestedTabularInline):
    model = QuestionChoice
    extra = 0
    fk_name = 'question'

class QuestionInline(NestedTabularInline):
    model = Question
    extra = 0
    fk_name = 'block'
    inlines = [ChoiceInline]

class QuestionBlockInline(NestedStackedInline):
    model = QuestionBlock
    extra = 0
    fk_name = 'enquete'
    inlines = [QuestionInline]

class EnqueteAdmin(NestedModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
        ('Description',      {'fields': ['description']}),
        ('Date information', {'fields': ['publishedDate']}),        
        ('Locked', {'fields': ['locked']})
    ]
    inlines = [QuestionBlockInline]

# @admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    readonly_fields= ('members',)
    form = make_ajax_form(Organisation, {
        # fieldname: channel_name
        'owners': 'users'
    })

# class OrganisationAdmin(admin.ModelAdmin):
#     list_display = ('name',)
    # readonly_fields= ('members',)
#     actions = ['mail_organisation']
#     def mail_organisation(self, request, queryset):
#         for org in queryset:
#             for member in org.members.all():
#                 password = User.objects.make_random_password()
#                 member.set_password(password)
#                 member.save()
#                 message = """ 
#             Welkom 
# bij de mediaprofiel.nl 

# Het e-mailadres dat je hebt gebruikt om het account aan te maken is tevens je gebruikersnaam. 

# We hebben een wachtwoord voor je aangemaakt: 

# {1}

# Als je een nieuw wachtwoord wilt kiezen, log in bij mediaprofiel.nl om je wachtwoord te wijzigen.
 
# Belangrijk: werk met de NIEUWSTE versies van de internetbrowsers zoals Google Chrome, Safari of Mozilla. 

# Veel plezier met het invullen van de vragenlijst. Het invullen duurt ongeveer 15 minuten. De resultaten zijn direct zichtbaar op de profielpagina. 

# Je gegevens worden strikt vertrouwelijk behandeld.
# Indien het onderzoek onderdeel uitmaakt van een organisatie-analyse, dan worden de resultaten gebruikt t.b.v. het organisatieprofiel. Deze analyse wordt uitgevoerd door een geautoriseerde medewerker van de organisatie. 


# Met vriendelijke groet,
# Team Mediaprofiel.nl
#             """
#                 htmlMessage = """ 
#                 <h1>Welkom</h1> 
#     bij de <a href="www.mediaprofiel.nl">mediaprofiel.nl</a><br> 

#     <p>Het e-mailadres dat je hebt gebruikt om het account aan te maken is tevens je gebruikersnaam.</p> 

#     <p>We hebben een wachtwoord voor je aangemaakt:</p> 
#     <br>
#     {1}
#     <br>
#     <p>Als je een nieuw wachtwoord wilt kiezen, log in bij mediaprofiel.nl om je wachtwoord te wijzigen.
#     <br>
#     <strong>Belangrijk: werk met de NIEUWSTE versies van de internetbrowsers zoals Google Chrome, Safari of Mozilla.</strong> 
#     <br>
#     <p>Veel plezier met het invullen van de vragenlijst. Het invullen duurt ongeveer 15 minuten. De resultaten zijn direct zichtbaar op de profielpagina. </p>
#     <br>
#     <i>Je gegevens worden strikt vertrouwelijk behandeld.
#     Indien het onderzoek onderdeel uitmaakt van een organisatie-analyse, dan worden de resultaten gebruikt t.b.v. het organisatieprofiel. Deze analyse wordt uitgevoerd door een geautoriseerde medewerker van de organisatie.</p></i> 
#     <br>
#     <p>Met vriendelijke groet,
#     Team Mediaprofiel.nl</p>
#                 """
#                 htmlMessage = htmlMessage.format(member.username, password)
#                 message = message.format(member.username, password)
#                 mail.send(member.email, 'mediaprofiel@gmail.com',subject = "Welkom bij Mediaprofielen!", message = message, html_message= htmlMessage)
#         self.message_user(request, "Mails verstuurd!")    
#     mail_organisation.short_description = "Mail wachtwoord aan leden"



admin.site.register(Enquete, EnqueteAdmin)
admin.site.register(Profiel)
admin.site.register(Invulmoment)
admin.site.register(Account)
admin.site.register(Answer)
admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(ProfileText)
