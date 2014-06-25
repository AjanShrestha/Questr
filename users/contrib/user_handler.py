

from random import choice
from django.conf import settings
from django.http import Http404

import mailing
from users.models import QuestrUserProfile, UserTransactional, QuestrToken
from quests.models import Quests

def get_random_password():
	"""
	Generates a random password.
	"""
	random_password = ''.join([choice('1234567890qwertyuiopasdfghjklzxcvbnm') for i in range(7)])
	return random_password

def __get_verification_url(user=None): 
    """
        Returns the verification url.
    """
    verf_link = ""
    if user:
        try:
            prev_transactional = UserTransactional.objects.get(email = user.email, status = False)
            if prev_transactional:
                prev_transactional.status = True
                prev_transactional.save()
        except UserTransactional.DoesNotExist:
            pass
        count = UserTransactional.objects.count()
        transcational = UserTransactional(id=count+1,email=user.email)
        transcational.save()
        token_id = transcational.get_token_id()
        questr_token = QuestrToken(token_id=token_id)
        questr_token.save()
        verf_link = "{0}/user/email/confirm/{1}?questr_token={2}".format(settings.QUESTR_URL , transcational.get_truncated_user_code(), token_id)
    return verf_link

def send_verfication_mail(user):
    """
        Sends the verification email to the user
    """
    verf_link = __get_verification_url(user)
    mailing.send_verification_email(user, verf_link)

def getShipper(shipper_id):
    """List all the quests by a particular user"""
    try:
        shipper = QuestrUserProfile.objects.filter(id=shipper_id)
    except QuestrUserProfile.DoesNotExist:
        raise Http404
        return render('404.html', locals())
    return shipper

def getShippers():
    """List all the quests by a particular user"""
    shippers = QuestrUserProfile.objects.filter(is_shipper='t')
    return shippers

def getShippersOfQuest(questname):
    """List of on shippers for a given quest"""
    shippers = str(Quests.objects.get(id=questname).shipper).split(',')
    return shippers

def isShipper(user):
    """Checks if the user is a shipper or a regular questr"""
    if user.is_shipper == True:
        return True #is a shipper
    return False #is a regular questr

def getAccountStatus(status_id):
    '''Get account status of user'''
    status_list = ["Normal","Starred","Warned","Suspended","Closed"]
    if status_id < len(status_list):
        return status_list[status_id]

def isActive(status):
    """Returns if the account is active for the user"""
    return "Yes" if status else "No"

def isEmailVerified(status):
    """Returns if the email of the user has been verified"""
    return "Yes" if status else "No"

def usernameExists(user):
    """Checks if the user by the provided displayname exists already"""
    try:
        user = QuestrUserProfile.objects.get(displayname=user)
    except QuestrUserProfile.DoesNotExist:
        return False
    if user:
        return True

def userExists(user_id):
    """Checks if the user by the provided displayname exists already"""
    try:
        user = QuestrUserProfile.objects.get(id=user_id)
    except QuestrUserProfile.DoesNotExist:
        return False
    if user:
        return True

def passwordExists(user):
    """Checks if the user has created a password for himself, passwords created by PSA are unusable"""
    return user.has_usable_password()
        
def emailExists(email):
    """Checks if the user with the provided email exists already"""
    try:
        user = QuestrUserProfile.objects.get(email=email)
    except QuestrUserProfile.DoesNotExist:
        return False
    if user:
        return True