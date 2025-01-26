from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import os
from .agents.main_guard_agent import GuardAgent
from .agents.classification_agent import ClassificationAgent
from .agents.shop_details_agent import Shop_DetailsAgent
from .agents.used_car_agent import UsedCar_details
from .agents.new_car_agent import NewCar_details
from .agents.agent_protocol import AgentProtocol
from .agents.apointment_agent import AppointmentScheduler
from .agents.new_calender import calendar
import re
from django.utils.html import mark_safe
from .agents.ttl import ttl

def format_message(content):
    """
    Replace \n with <br> and **text** with <strong>text</strong>.
    """
    content = content.replace("\n", "<br>")

    content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
    return mark_safe(content) 


@csrf_exempt
def chatbot_view(request):
    messages = request.session.get("messages", [])

    if request.method == "POST":
        if request.POST.get("clear_chat") == "true":
            request.session["messages"] = []  
            return render(request, "chatbot/index.html", {"messages": []})
        
        
        
        user_message = request.POST.get("message")
        if not user_message:
            return render(request, "chatbot/index.html", {"messages": messages})

        messages.append({"role": "user", "content": user_message})

        guard_agent = GuardAgent()
        classification_agent = ClassificationAgent()
        agent_dict: dict[str, AgentProtocol] = {
            "Shop Details": Shop_DetailsAgent(),
            "Used Car": UsedCar_details(),
            "New Car": NewCar_details(),
            "AppointmentSchedule": AppointmentScheduler(),
        }

   
        guard_agent_response = guard_agent.get_response(messages)
        try:
            if guard_agent_response["content"] :
                guard_agent_response["content"] = format_message(guard_agent_response["content"])
                
                audio_url = ttl(guard_agent_response["content"])
                print("AUDIO URL:",audio_url)
                if audio_url:
                    guard_agent_response["audio_url"] = audio_url  
        except:
            pass
        messages.append(guard_agent_response)
        

        if guard_agent_response["memory"]["guard_decision"] == "not allowed":
            request.session["messages"] = messages  
            return render(request, "chatbot/index.html", {"messages": messages})

        elif guard_agent_response["memory"]["guard_decision"] == "allowed":
      
            classification_agent_response = classification_agent.get_response(messages)
            classification_decision = classification_agent_response["memory"]["guard_decision"]


            agent = agent_dict[classification_decision]
            response = agent.get_response(messages)
            print("#############",response)
            if response["content"] :
                response["content"] = format_message(response["content"])
                
                audio_url = ttl(response["content"])
                print("AUDIO URL:",audio_url)
                if audio_url:
                    response["audio_url"] = audio_url  
                    
            messages.append(response)
            print(messages)

        request.session["messages"] = messages


    return render(request, "chatbot/index.html", {"messages": messages})

