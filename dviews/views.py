from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
import requests
import json


def slack(request):

    query = request.POST.dict()
    querystr = query['text']
    if querystr == False:
        return HttpResponse("Couldn't find key text in POST:" + ''.join(request.body.items()) + " or GET:" + ''.join(request.body.items()))
        return render(request.POST, 'index.html')
    querystr = querystr[len(query['trigger_word'])+1:] 
    if querystr.partition(' ')[0]=="-exact":
        exact = True
        querystr = querystr[len(querystr.partition(' ')[0])+1:]
    else:
        exact = False
    r = requests.get('http://api.xivdb.com/search?string=' + querystr )
    obj = r.json()
    result = {"attachments":[{}]}
    try:
        if obj["items"]["total"] == 1:
            item = obj["items"]["results"].pop()  
            result['text']= 'Memeroon finds this item matches ' + querystr
            result['attachments'][0]['title'] = item["name"] 
            result['attachments'][0]['text'] = item["help"]
            result['attachments'][0]['fallback'] = item["name"] + item["help"]
            result['attachments'][0]['thumb_url'] = item["icon"] 
            result['attachments'][0]['title_link'] = item["url_xivdb"] 
        elif obj["items"]["total"] > 1:
            if exact:
                for item in obj["items"]["results"]:
                    if item["name"].lower() == querystr.lower():
                        result['text']= 'Memeroon finds this item matches ' + querystr + ' very muches'
                        result['attachments'][0]['title'] = item["name"] 
                        result['attachments'][0]['text'] = item["help"]
                        result['attachments'][0]['fallback'] = item["name"] + item["help"]
                        result['attachments'][0]['thumb_url'] = item["icon"] 
                        result['attachments'][0]['title_link'] = item["url_xivdb"] 
                if result['text'] =="":
                        result['text'] = "Memeroon did find no very muches matches " + querystr
            else:
                result['text']= 'Memeroon finds ' + str(obj["items"]["total"]) +' items matches ' + querystr 
                if obj["items"]["total"] > 5:
                    result['text'] = result['text'] + ", shows first 5"
                pos = 0
                result['attachments'][0]['fields'] =[]
                for item in obj["items"]["results"]:
                    result['attachments'][0]['fields'].append({"title":item["name"],"value":item["help"][:30]+"...","short":"true"})
                    pos = pos + 1
                    if pos == 5:
                        break
    except TypeError:
        result['text'] = "Memeroon did find no matches " + querystr
    return HttpResponse(json.JSONEncoder().encode(result))
    return render(request.POST, 'index.html')
