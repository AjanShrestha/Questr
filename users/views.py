

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.http import Http404
from django.shortcuts import render, redirect
from .models import QuestrUserProfile, UserTransactional, QuestrToken
from .forms import QuestrUserChangeForm, QuestrUserCreationForm, QuestrLocalAuthenticationForm, QuestrSocialSignupForm, SetPasswordForm, PasswordChangeForm
import logging

from access.requires import verified, is_alive
from contrib import mailing, user_handler

from quests.contrib import quest_handler

# Create your views here.
def logout(request):
    """Logs out user"""
    auth_logout(request)
    # nextlink="signup"
    return redirect('index')
    
def login(request):
    """Home view, displays login mechanism"""
    pagetype="public"
    nav_link_1 = "/user/login"
    nav_link_1_label = "login"
    nav_link_2 = "/user/signup"
    nav_link_2_label ="signup"
    nav_link_3 = "#"
    nav_link_3_label ="about us"
    ## if authenticated redirect to user's homepage directly ##
    if request.user.is_authenticated():
        return redirect('home')
    if request.method == "POST":   
        auth_form = QuestrLocalAuthenticationForm(data=request.POST)
        if auth_form.is_valid():
            auth_login(request, auth_form.get_user())
            return redirect('home')
    return render(request, 'signin.html', locals())

def signup(request):
    """Signup, if request == POST, creates the user"""
    pagetype="public"
    nav_link_1 = "/user/login"
    nav_link_1_label = "login"
    nav_link_2 = "/user/signup"
    nav_link_2_label ="signup"
    nav_link_3 = "#"
    nav_link_3_label ="about us"
    ## if authenticated redirect to user's homepage directly ##
    if request.user.is_authenticated():
        return redirect('home')
    if request.method == "POST":
        user_form = QuestrUserCreationForm(request.POST)
        if user_form.is_valid():
            userdata = user_form.save()
            authenticate(username=userdata.email, password=userdata.password)
            userdata.backend='django.contrib.auth.backends.ModelBackend'
            auth_login(request, userdata)
            user_handler.send_verfication_mail(userdata)
            return render(request, 'thankyou.html', locals())
        return render(request, 'signup.html', locals())
    else:
        user_form = QuestrUserCreationForm()
        return render(request, 'signup.html', locals())

@login_required
def resend_verification_email(request):
    """
        Sends a email verification link to the corresponding email address
    """
    if request.user.is_authenticated():
        user_email = request.user
        try:
            user = QuestrUserProfile.objects.get(email=user_email)
            if user and not user.email_status:
                user_handler.send_verfication_mail(user)
        except QuestrUserProfile.DoesNotExist:
            return redirect('home')
    return redirect('home')

@login_required
@verified
def home(request):
    """Post login this is returned and displays user's home page"""
    pagetype="loggedin"
    secondnav="listquestsecondnav"
    user = request.user
    nav_link_1 = "/user/profile"
    nav_link_1_label = "my profile"
    nav_link_2 = "/user/settings"
    nav_link_2_label ="settings"
    nav_link_3 = "/user/logout"
    nav_link_3_label ="logout"
    allquests = quest_handler.listfeaturedquests()
    # logging.warn(allquests)
    return render(request,'homepage.html', locals())

@login_required
def profile(request):
    """This displays user's profile page"""
    pagetype="loggedin"
    user = request.user
    nav_link_1 = "/user/profile"
    nav_link_1_label = "my profile"
    nav_link_2 = "/user/settings"
    nav_link_2_label ="settings"
    nav_link_3 = "/user/logout"
    nav_link_3_label ="logout"
    try:
        user = QuestrUserProfile.objects.get(email=request.user)
    except QuestrUserProfile.DoesNotExist:
        raise Http404
        return render(request,'404.html')

    try:
        questsbyuser = getQuestsByUser(user.id)
    except Exception, e:
        raise e
        return render(request,'broke.html')
    return render(request,'profile.html', locals())

@login_required
def userSettings(request):
    """Change's user's personal settings"""
    pagetype="loggedin"
    user = request.user
    nav_link_1 = "/user/profile"
    nav_link_1_label = "my profile"
    nav_link_2 = "/user/settings"
    nav_link_2_label ="settings"
    nav_link_3 = "/user/logout"
    nav_link_3_label ="logout"
    settingstype="general"
    password = user_handler.passwordExists(user)
    try:
        user = QuestrUserProfile.objects.get(email=request.user)
    except QuestrUserProfile.DoesNotExist:
        raise Http404
        return render(request,'404.html', locals())

    if request.method == "POST":
        try:
            user_form = QuestrUserChangeForm(request.POST, instance=request.user)
        except QuestrUserProfile.DoesNotExist:
            raise Http404
            return render(request,'404.html', locals())        
        if user_form.is_valid():
            user_form.save()
            return redirect('settings')

    return render(request, "generalsettings.html",locals())

@login_required
def myTrades(request):
    pagetype="loggedin"
    user = request.user
    nav_link_1 = "/user/profile"
    nav_link_1_label = "my profile"
    nav_link_2 = "/user/settings"
    nav_link_2_label ="settings"
    nav_link_3 = "/user/logout"
    nav_link_3_label ="logout"
    return render(request, 'trades.html', locals())

@login_required
def myPosts(request):
    pagetype="loggedin"
    user = request.user
    nav_link_1 = "/user/profile"
    nav_link_1_label = "my profile"
    nav_link_2 = "/user/settings"
    nav_link_2_label ="settings"
    nav_link_3 = "/user/logout"
    nav_link_3_label ="logout"
    return render(request, 'trades2.html', locals())

@login_required
def getUserInfo(request, displayname):
    '''This is used to display user's public profile'''
    pagetype="loggedin"
    user = request.user
    nav_link_1 = "/user/profile"
    nav_link_1_label = "my profile"
    nav_link_2 = "/user/settings"
    nav_link_2_label ="settings"
    nav_link_3 = "/user/logout"
    nav_link_3_label ="logout"
    try:
        publicuser = QuestrUserProfile.objects.get(displayname=displayname)
    except QuestrUserProfile.DoesNotExist:
        raise Http404
        return render(request,'404.html')

    try:
        questsbyuser = getQuestsByUser(publicuser.id)
    except Exception, e:
        raise e
        return render(request,'broke.html')

    return render(request,'publicprofile.html', locals())

@login_required
def createPassword(request):
    """Create a password for socially logged in user"""
    pagetype="loggedin"
    user = request.user
    nav_link_1 = "/user/profile"
    nav_link_1_label = "my profile"
    nav_link_2 = "/user/settings"
    nav_link_2_label ="settings"
    nav_link_3 = "/user/logout"
    nav_link_3_label ="logout"
    settingstype="password"

    if passwordExists(request.user):
        return redirect('home')
    
    if request.method == "POST":
        user_form = SetPasswordForm(user, request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('home')
    return render(request, "createpassword.html", locals())

@login_required
def changePassword(request):
    """Change's user's personal settings"""
    pagetype="loggedin"
    user = request.user
    nav_link_1 = "/user/profile"
    nav_link_1_label = "my profile"
    nav_link_2 = "/user/settings"
    nav_link_2_label ="settings"
    nav_link_3 = "/user/logout"
    nav_link_3_label ="logout"
    settingstype="password"
    ##check if the user has password, if they don't they'd be provided with a link to create one for them
    password = passwordExists(user)
    # logging.warn(user)
    # logging.warn(password)

    if request.method == "POST":
        user_form = PasswordChangeForm(user, request.POST)
        logging.warn(user_form.errors)
        if user_form.is_valid():
            user_form.save()
            return redirect('changepassword')
    return render(request, "passwordsettings.html",locals())

@login_required
def cardSettings(request):
    """Change's user's personal settings"""
    pagetype="loggedin"
    user = request.user
    nav_link_1 = "/user/profile"
    nav_link_1_label = "my profile"
    nav_link_2 = "/user/settings"
    nav_link_2_label ="settings"
    nav_link_3 = "/user/logout"
    nav_link_3_label ="logout"
    settingstype="card"
    return render(request, "cardsettings.html",locals())

@login_required
def emailSettings(request):
    """Change's user's personal settings"""
    pagetype="loggedin"
    user = request.user
    nav_link_1 = "/user/profile"
    nav_link_1_label = "my profile"
    nav_link_2 = "/user/settings"
    nav_link_2_label ="settings"
    nav_link_3 = "/user/logout"
    nav_link_3_label ="logout"
    settingstype="email"
    return render(request, "emailsettings.html",locals())

def saveUserInfo(request):
    """This save's additional user info post the social login is successfull"""
    user_data = request.session.get('details')
    if request.method == "POST":
        user_form = QuestrSocialSignupForm(request.POST)
        if user_form.is_valid():
            request.session['first_name'] = request.POST['first_name']
            request.session['last_name'] = request.POST['last_name']
            request.session['email'] = request.POST['email']
            request.session['displayname'] = request.POST['displayname']        
            backend = request.session['partial_pipeline']['backend']
            return redirect('social:complete', backend=backend)
        return render(request, "user/edituserinfo.html",locals())
    else:
        return render(request, "user/edituserinfo.html",locals())

@is_alive
def verify_email(request, user_code):
    """
        Verifies email of the user and redirect to the home page
    """
    if user_code:
        try:
            transcational = UserTransactional.objects.get(user_code__regex=r'^%s' % user_code)
            if transcational:
                if transcational.status:
                    try:
                        user = QuestrUserProfile.objects.get(id=transcational.id)
                        if user:
                            user.email_status = True
                            user.save()
                            transcational.status = True
                            transcational.save()
                    except QuestrUserProfile.DoesNotExist:
                        logging.debug('User does not exist')
                        return redirect('home')
                else:
                    message = "Please use the latest verification email sent."
                    return redirect('home', locals())
        except UserTransactional.DoesNotExist:
            return redirect('home')
    return redirect('home')

def resetpassword(request):
    """
    Mail new random password to the user.
    """
    if request.method=="POST":
        user_email = request.POST['email']
        try:
            user = QuestrUserProfile.objects.get(email = user_email)
        except Exception, e:
            message ="Bruh, a user with that email doesnt exist!"
            return render(request, "resetpassword.html", locals())
        if user:
            new_random_password = user_handler.get_random_password()
            user.set_password(new_random_password)
            user.save()
            mailing.send_reset_password_email(user, new_random_password)
            message = "Please check your inbox for your new password"
            return render(request, "homepage.html", locals())

    return render(request,"resetpassword.html", locals())
