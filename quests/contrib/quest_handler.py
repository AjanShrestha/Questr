

from django.shortcuts import render, redirect
from django.conf import settings

from quests.models import Quests

import logging
# Create your views here.
def listfeaturedquests(questrs_id):
    """List all the featured quests"""
    allquests = Quests.objects.filter(ishidden=False)
    return allquests

def getQuestsByUser(questrs_id):
    """List all the quests by a particular user"""
    try:
        questsbysuer = Quests.objects.filter(questrs_id=questrs_id, ishidden=False, shipper=None)
    except Quests.DoesNotExist:
        raise Http404
        return render(request,'404.html')
    return questsbysuer

def getQuestDetails(quest_id):
    try:
        questdetails = Quests.objects.get(id=quest_id)
    except Quests.DoesNotExist:
        raise Http404
        return render(request,'404.html')
    return questdetails

def getMyShipmnets(shipper_id):
    myshipments = Quests.objects.filter(shipper=shipper_id)
    return myshipments

def getQuestsWithOffer(questrs_id):
    """Lists a user's quest where offers are put"""
    try:
        questsWithOffer = Quests.objects.filter(questrs_id=questrs_id, ishidden=False).exclude(shipper=None)
    except Quests.DoesNotExist:
        raise Http404
        return render(request,'404.html')
    return questsWithOffer

def isShipperForQuest(shipper_id, questname):
    """Returns if the current shipper is listed in for the quest, the shipper_id has to be converted to string"""
    try:
        questdetails = Quests.objects.get(id=questname)
    except Quests.DoesNotExist:
        raise Http404
        return render(request,'404.html')

    current_shipper = questdetails.shipper
    if current_shipper != None:
        if shipper_id in current_shipper:
            return True
        return False
    return False

def addShipper(shipper_id, questname):
    """adds a shipper to a posted quest"""
    try:
        questdetails = Quests.objects.get(id=questname)
    except Quests.DoesNotExist:
        raise Http404
        return render(request,'404.html')

    current_shipper = questdetails.shipper
    # for first application
    logging.warn(current_shipper)
    if current_shipper==None:
        current_shipper = []
    else:
        current_shipper = current_shipper.split(',')
    # check if shipper has already applied
    if not shipper_id in current_shipper:
        current_shipper.append(shipper_id)
        current_shipper = ','.join(current_shipper)
    else:
        return redirect('home')

    try:
        Quests.objects.filter(id=questname).update(shipper=current_shipper)
    except Quests.DoesNotExist:
        raise Http404
        return render(request,'404.html')

def delShipper(shipper_id, questname):
    """adds a shipper to a posted quest"""
    try:
        questdetails = Quests.objects.get(id=questname)
    except Quests.DoesNotExist:
        raise Http404
        return render(request,'404.html')

    current_shipper = questdetails.shipper
    if current_shipper==None:
        #If no user has bid so far , redirect to home
        return redirect('home')
    else:
        current_shipper = current_shipper.split(',')
    # check if shipper has already applied
    if shipper_id in current_shipper:
        current_shipper.remove(shipper_id)
        if current_shipper:
            current_shipper = ','.join(current_shipper)
        else:
            current_shipper=None
    else:
        return redirect('home')

    try:
        Quests.objects.filter(id=questname).update(shipper=current_shipper)
    except Quests.DoesNotExist:
        raise Http404
        return render(request,'404.html')

def prepNewQuestNotification(user, questdetails):
    """Prepare the details for notification emails for new quests"""
    template_name="New_Quest_Notification"
    subject="New Quest Notification"
    # quest_browse_link=settings.QUESTR_URL+"/quest"
    quest_support_email="support@questr.co"
    questr_unsubscription_link="http://questr.co/unsub"

    email_details = {
                        'subject' : subject,
                        'template_name' : template_name,
                        'global_merge_vars': {
                                                'quest_public_link' : settings.QUESTR_URL+'/quest/'+str(questdetails.id),
                                                'quest_description' : questdetails.description,
                                                'user_first_name'   : user.first_name,
                                                'email_unsub_link'  : questr_unsubscription_link,
                                                'quest_title'       : questdetails.title,
                                                'quest_size'      : questdetails.size,
                                                'quest_reward'      : str(questdetails.reward),
                                                'quest_distance'      : str(questdetails.distance),
                                                'quest_creation_date'      : questdetails.creation_date.strftime('%m-%d-%Y'),
                                                'quest_support_mail': quest_support_email,
                                                'questr_unsubscription_link' : questr_unsubscription_link,
                                                'quest_application_link' : settings.QUESTR_URL+'/quest/'+str(questdetails.id)+'/apply/',
                                                'company'           : "Questr Co",

                                                },
                    }
    return email_details

def prepOfferAcceptedNotification(user, questdetails):
    """Prepare the details for notification emails for new quests"""
    template_name="Offer_Accepted_Notification"
    subject="Questr - Offer Accepted"
    # quest_browse_link=settings.QUESTR_URL+"/quest"
    quest_support_email="support@questr.co"
    questr_unsubscription_link="http://questr.co/unsub"

    email_details = {
                        'subject' : subject,
                        'template_name' : template_name,
                        'global_merge_vars': {
                                                'quest_public_link' : settings.QUESTR_URL+'/quest/'+str(questdetails.id),
                                                'quest_description' : questdetails.description,
                                                'user_first_name'   : user.first_name,
                                                'email_unsub_link'  : questr_unsubscription_link,
                                                'quest_title'       : questdetails.title,
                                                'quest_size'      : questdetails.size,
                                                'quest_reward'      : str(questdetails.reward),
                                                'quest_distance'      : str(questdetails.distance),
                                                'quest_creation_date'      : questdetails.creation_date.strftime('%m-%d-%Y'),
                                                'quest_support_mail': quest_support_email,
                                                'questr_unsubscription_link' : questr_unsubscription_link,
                                                'quest_shipment_link' : settings.QUESTR_URL+'/user/trades/',
                                                'company'           : "Questr Co"

                                                },
                    }
    return email_details

def prepQuestAppliedNotification(shipper, questr, questdetails):
    """Prepare the details for notification emails for new quests"""
    template_name="Quest_Applied_Notification"
    subject="Questr - Application Received"
    # quest_browse_link=settings.QUESTR_URL+"/quest"
    quest_support_email="support@questr.co"
    questr_unsubscription_link="http://questr.co/unsub"

    email_details = {
                        'subject' : subject,
                        'template_name' : template_name,
                        'global_merge_vars': {
                                                'quest_public_link' : settings.QUESTR_URL+'/quest/'+str(questdetails.id),
                                                'quest_description' : questdetails.description,
                                                'questr_first_name'   : questr.first_name,
                                                'shipper_first_name': shipper.first_name,                                                
                                                'shipper_last_name': shipper.last_name,                                                
                                                'shipper_user_name': shipper.displayname,                                                
                                                'shipper_profile_link'  : settings.QUESTR_URL+'/user/'+shipper.displayname,                                                
                                                'email_unsub_link'  : questr_unsubscription_link,
                                                'quest_title'       : questdetails.title,
                                                'quest_size'      : questdetails.size,
                                                'quest_reward'      : str(questdetails.reward),
                                                'quest_distance'      : str(questdetails.distance),
                                                'quest_creation_date'      : questdetails.creation_date.strftime('%m-%d-%Y'),
                                                'quest_support_mail': quest_support_email,
                                                'quest_shipment_link' : settings.QUESTR_URL+'/user/trades/',
                                                'company'           : "Questr Co"

                                                },
                    }
    return email_details

def prepQuestCompleteNotification(shipper, questr, questdetails, review_link):
    """Prepare the details for notification emails for completion of quests"""
    template_name="Quest_Completion_Notification"
    subject="Questr - Quest Completed"
    # quest_browse_link=settings.QUESTR_URL+"/quest"
    quest_support_email="support@questr.co"
    questr_unsubscription_link="http://questr.co/unsub"

    email_details = {
                        'subject' : subject,
                        'template_name' : template_name,
                        'global_merge_vars': {
                                                'quest_public_link' : settings.QUESTR_URL+'/quest/'+str(questdetails.id),
                                                'review_link' : review_link,
                                                'quest_description' : questdetails.description,
                                                'user_first_name'   : questr.first_name,
                                                'quest_title'       : questdetails.title,
                                                'quest_size'      : questdetails.size,
                                                'quest_reward'      : str(questdetails.reward),
                                                'quest_distance'      : str(questdetails.distance),
                                                'quest_creation_date'      : questdetails.creation_date.strftime('%m-%d-%Y'),
                                                'quest_support_mail': quest_support_email,
                                                'questr_unsubscription_link' : questr_unsubscription_link,
                                                'company'           : "Questr Co"

                                                },
                    }

    logging.warn(email_details)
    return email_details

def get_review_link(quest_id, shipper_id):
    review_link = "{0}/review/{1}/{2}".format(settings.QUESTR_URL , quest_id, shipper_id)
    return review_link

def update_resized_image(quest_id):
    import os
    from django.core.files.storage import default_storage as storage
    questdetails = getQuestDetails(quest_id)
    if not questdetails.item_images:
        return ""
    file_path = questdetails.item_images.name
    logging.warn(file_path)
    filename_base, filename_ext = os.path.splitext(file_path)
    normal_file_path = "%s_%s_normal.jpg" % (filename_base, questdetails.id)
    logging.warn(normal_file_path)
    try:
        Quests.objects.filter(id=quest_id).update(item_images=normal_file_path)
    except Quests.DoesNotExist:
        raise Http404
        return render(request,'404.html')
    logging.warn(storage.exists(file_path))
    if storage.exists(file_path):
        storage.delete(file_path)
    return ""