# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import datetime                                 
from pytz import timezone                                                                                                          
import json                                                                                                             
import random                                                                                                           
from django.http import JsonResponse                                                                                    
from django.views.decorators.csrf import csrf_exempt                                                                    
@csrf_exempt                                                                                                            
def parser(request):                                                                                                     
    if request.method == "POST":
        print request.POST.get('message')
        data = request.POST.get('message').lower()                                                                      
        words = set(data.lower().strip().split())                                                                            
        json_data = json.load(open('greetings.json'))                                                                   
        faq_data = json.load(open('faq.json'))
        for word in words:
            if word in faq_data.keys():
                rdata = {
                        'message':faq_data[word]
                        }
                return JsonResponse(rdata)
        if data in json_data.keys():                                                                                    
            if type(json_data[data]) == list:                                                                           
                rdata = {                                                                                               
                        'message':random.choice(json_data[data])                                                        
                        }                                                                                               
            else:                                                                                                       
                rdata = {                                                                                               
                        'message':json_data[data]                                                                       
                        }                                                                                               
            return JsonResponse(rdata)                                                                                  
        elif ('create' in words) or ('add' in words):
            rdata = {                                                                                                   
                    'message':"create an event"                                                                         
                    }                                                                                               
            return JsonResponse(rdata)                                                                                  
        elif 'show' in words:                                                                                           
            if 'events' in words:                                                                                       
                pass                                                                                                    
            else:                                                                                                       
                pass

        elif ('feed' in words) or ('newsfeed' in words):                                                                
            feed = IncubatorPost.objects.all()[0:5]
            msg = ''
            for x in feed:
                msg = msg+x.incubator.name+x.title+'<br>'
            rdata={
                    'message':msg
                }
            return JsonResponse(rdata)

        elif ('top' in words):                                                                                          
            if ('startup' in words):                                                                                    
                pass                                                                                                    
            elif ('incubator' in words):                                                                                
                pass                                                                                                    
        elif ('time' in words):                                                                                         
            rdata = {                                                                                                   
                    'message':'The time is '+str(datetime.datetime.now(timezone('Asia/Kolkata')).time())[0:8]                                   
                    }                                                                                                   
            return JsonResponse(rdata)     
        else:
            rdata = {
                    'message':'I am sorry, I don\'t understand'
                    }
            return JsonResponse(rdata)
    if request.method == 'GET':                                                                                         
        return JsonResponse({"mesage":"No Get"})                                                                        
