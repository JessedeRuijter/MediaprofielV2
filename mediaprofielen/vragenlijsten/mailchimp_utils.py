from config import MailChimpConfig
import requests
import json
try:
    import urlparse
except ImportError:
    from urllib import parse as urlparse
from models import Organisation, User, Invulmoment, Enquete, Profiel
from datetime import date

def getLists():
    result = []
    config = MailChimpConfig()
    endpoint = urlparse.urljoin(config.api_root, 'lists')
    response = requests.get(endpoint, auth=('apikey', config.apikey), verify=False)
    for apilist in response.json()['lists']:
        result.append((apilist['id'], apilist['name']))
    return result

def makeOrganisation(name, list_id, enquete_id, color):
    # Keep a list of added users for the deletion upon error
    userlist = []

    # Create a batch operation
    batch = {"operations":[]}

    config = MailChimpConfig()
    # Create a organisation
    new_organisation = Organisation(name=name, color=color)
    new_organisation.save()

    # Retrieve the enquete
    enquete = Enquete.objects.get(id=enquete_id)
    
    # Create a invulmoment
    new_invulmoment = Invulmoment(organisation=new_organisation, enquete=enquete, time=date.today())
    new_invulmoment.save()

    # Get the list members
    list_endpoint_string = 'lists/' + list_id + '/members'
    list_endpoint = urlparse.urljoin(config.api_root, list_endpoint_string)
    list_response = requests.get(list_endpoint, auth=('apikey', config.apikey), verify=False)
    
    # Add a new Merge tag to the list
    mergetags_endpoint_string = 'lists/' + list_id +'/merge-fields'
    mergetags_endpoint = urlparse.urljoin(config.api_root, mergetags_endpoint_string)
    mergetags_post_data = {"tag":"PWD", "name":"Password", "required":False, "public":False, "type":"text"}
    mergetags_response = requests.post(mergetags_endpoint, auth=('apikey', config.apikey), verify=False, data=json.dumps(mergetags_post_data))
    if mergetags_response.reason != "OK":
        new_organisation.delete()
        new_invulmoment.delete()
        return "Response error!: " + mergetags_response.reason + " , bestaat de Password Mergetag al in Mailchimp?"

    for member in list_response.json()['members']:
        userCheck = User.objects.filter(username=member['email_address'].lower())
        
        if not userCheck.count() == 0:
            new_invulmoment.delete()
            new_organisation.delete()
            if len(userlist) > 0:
                for user in userlist:
                    user.delete()
            return "Gebruiker bestaat al: " + member['email_address'].lower() + " (Geen organisatie aangemaakt!)"
        # For every user add them to the db and patch them to mailchimp (provide pwd merge tag)
        newUser = User(username=member['email_address'].lower(), email=member['email_address'])
        password = User.objects.make_random_password()
        newUser.set_password(password)
        newUser.save()
        userlist.append(newUser)

        # Patch the user (add it to batch operation)
        path_string = "/lists/" + list_id + "/members/" + member['id']
        operation_data = {"merge_fields":{"PWD":password}}
        operation = {"method":"PATCH", "path":path_string, "body":json.dumps(operation_data)}
        batch["operations"].append(operation)

        # Add the user to the organisation
        new_organisation.members.add(newUser)

        # Create a profiel object for this user
        # newProfiel = Profiel(user=newUser, invulmoment=new_invulmoment)
        # newProfiel.save()


    batch_endpoint = urlparse.urljoin(config.api_root, "batches")
    batch_response = requests.post(batch_endpoint, auth=('apikey', config.apikey), verify=False, data=json.dumps(batch))
    print batch_response.text
    if batch_response.reason != "OK":
        new_invulmoment.delete()
        new_organisation.delete()
        if len(userlist) > 0:
            for user in userlist:
                user.delete()
        return "Response Error!: " + batch_response.reason
    return True



