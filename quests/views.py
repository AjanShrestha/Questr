from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import Http404
from django.contrib.auth.decorators import login_required

from libs import email_notifier

from contrib import quest_handler
from users.contrib.user_handler import isShipper, getShippers
from .forms import QuestCreationForm, QuestChangeForm
from .models import Quests

import logging

@login_required
def listallquests(request):
    # pagetype="loggedin"
    # user = request.user
    # allquests = Quests.objects.all()
    # return render(request, 'listallquest.html', locals())
    pagetitle="home"
    return redirect("home")

@login_required
def viewquest(request, questname):
    pagetype="loggedin"
    user = request.user
    questname=questname
    try:
        questdetails = Quests.objects.get(id=questname)
        pagetitle = questdetails.title
    except Quests.DoesNotExist:
        raise Http404
        return render(request,'404.html')

    # Check if the owner and the user are the same
    if questdetails.questrs.id == request.user.id:
        isOwner = True

    isShipperForQuest=quest_handler.isShipperForQuest(str(user.id), questname)
    return render(request, 'viewquest.html', locals())

@login_required
def editquest(request, questname):
    pagetype="loggedin"
    user = request.user
    questname=questname
    try:
        questdetails = Quests.objects.get(id=questname)
    except Quests.DoesNotExist:
        raise Http404
        return render(request,'404.html')

    if request.method=="POST":
        if questdetails.questrs.id == request.user.id:
            instance=get_object_or_404(Quests, id=questname)
            user_form = QuestChangeForm(data=request.POST, instance=instance)
            # logging.warn(user_form.errors)
            # logging.warn(user_form.is_valid())
            if user_form.is_valid():
                quest_data = user_form.save(commit=False)
                quest_data.save()
                message = "Your quest has been updated!"
                return redirect('viewquest', questname=questname)

    # Check if the owner and the user are the same
    if questdetails.questrs.id == request.user.id:
        pagetitle="Edit - " + questdetails.title
        return render(request, 'editquest.html', locals())

    raise Http404
    return render(request,'404.html')

@login_required
def createquest(request):
    """creates new quest and sends notification to shippers"""
    from users.contrib.user_handler import getShipper
    pagetype="loggedin"
    user = request.user

    if request.method=="POST":
        now = timezone.now()
        user_form = QuestCreationForm(data=request.POST)
        # logging.warn(user_form.errors)
        # logging.warn(user_form.is_valid())
        if user_form.is_valid():
            quest_data = user_form.save(commit=False)
            quest_data.questrs_id=request.user.id
            quest_data.creation_date=now
            quest_data.save()
            try:
                shippers = getShippers()
                for shipper in shippers: # send notifcations to all the shippers
                    email_details = quest_handler.prepNewQuestNotification(shipper, quest_data)
                    email_notifier.send_email_notification(shipper, email_details)
            except Exception, e:
                logging.warn(e)
                pass
            message="Your quest has been created!"
            return redirect('home')
    pagetitle = "Create a Quest"
    return render(request, 'newquest.html', locals())  

@login_required
def applyForQuest(request, questname):
    """Takes in applications for a quest"""
    pagetype="loggedin"
    shipper = request.user # the guy logged in is the shipper
    questname = questname
    try:
        questdetails = Quests.objects.get(id=questname, isaccepted=False)
    except Quests.DoesNotExist:
        raise Http404
        return render(request,'404.html')
    # Check if the owner and the user are the same
    if questdetails.questrs.id == request.user.id:
        return redirect('home')
    # add a shipper to the quest
    quest_handler.addShipper(str(shipper.id), questname)
    message="Your application has been sent to the quest owner"
    logging.warn(message)
    return redirect('viewquest', questname=questname)

@login_required
def withdrawFromQuest(request, questname):
    """Takes in applications for a quest"""
    pagetype="loggedin"
    shipper = request.user # the guy logged in is the shipper
    questname = questname
    try:
        questdetails = Quests.objects.get(id=questname, isaccepted=False)
    except Quests.DoesNotExist:
        raise Http404
        return render(request,'404.html')
    # Check if the owner and the user are the same
    if questdetails.questrs.id == request.user.id:
        return redirect('home')
    # remove the shipper from the quest
    quest_handler.delShipper(str(shipper.id), questname)
    message="You have retracted yourself from the quest"
    logging.warn(message)
    return redirect('viewquest', questname=questname)