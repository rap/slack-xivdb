from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
import requests
import json


def slack(request):

    result_num = 5
    exact = False
    #query = request
    result = {"attachments":[{}]}
    query = request.POST.dict()
    #comment above and uncomment below for test case
    #querystr = query['text']
    if querystr == False:
        return HttpResponse("Couldn't find key text in POST:" + ''.join(request.body.items()) + " or GET:" + ''.join(request.body.items()))
        return render(request.POST, 'index.html')
    querystr = querystr[len(query['trigger_word'])+1:] # replace with slack token string
    name = query['user_name']
    while querystr[:1] == '-':
        arraystr = querystr.split()
        if arraystr[0].lower() == '-help':
            result['text'] = (name +' can helps in following ways!\n' 
                'give ' +name + ' item name and ' +name + 'tries best to finds.\n' 
                + name + 'knows these trickys at a start\n' 
                '-exact and ' + name + 'only gives exact match!  \n' 
                '-results and ' +name+ 'will give that many! ' +name + 'doesn\'t think you should pick a big one... \n'
                '-help and ' +name+ 'will explains again.')
            return HttpResponse(json.JSONEncoder().encode(result))        
        if len(arraystr) == 1:
            result['text']= name +'can\'t help with '+ arraystr[0][1:] +' if you not tell what to do!'
            return HttpResponse(json.JSONEncoder().encode(result))        
        if arraystr[0].lower() == '-exact':
            exact = True
            querystr = querystr[len(arraystr[0])+1:]
        elif arraystr[0].lower() == '-results':
            if arraystr[1].isdigit():
                result_num = int(arraystr[1])
                querystr = querystr[len(arraystr[0])+len(arraystr[1])+2:]
            else:
                result['text']= name +' no can count to ' +str(arraystr[1]) +'!'
                return HttpResponse(json.JSONEncoder().encode(result))

    if len(querystr) < 1:
        result['text']= name +' no can match nothing! You expect miracle from ' + name + '!'
        return HttpResponse(json.JSONEncoder().encode(result))
    #print(querystr)
    r = requests.get('http://api.xivdb.com/search?string=' + querystr )
    obj = r.json()
    #print(r.text)
    try:
        if obj["items"]["total"] == '1':
            item = obj["items"]["results"].pop()  
            result['text']= name +' finds this item matches ' + querystr
            if exact:
                result['text'] += ' exactly'
            result['attachments'][0]['title'] = item["name"] 
            result['attachments'][0]['text'] = item["help"]
            result['attachments'][0]['fallback'] = item["name"] + item["help"]
            result['attachments'][0]['thumb_url'] = item["icon"] 
            result['attachments'][0]['title_link'] = item["url_xivdb"] 
        elif obj["items"]["total"] > 1:
            if exact:
                for item in obj['items']['results']:
                    if item['name'].lower() == exactstr.lower():
                        result['text']= name +' finds this item matches ' + querystr + 'exactly'
                        result['attachments'][0]['title'] = item["name"] 
                        result['attachments'][0]['text'] = item["help"]
                        result['attachments'][0]['fallback'] = item["name"] + item["help"]
                        result['attachments'][0]['thumb_url'] = item["icon"] 
                        result['attachments'][0]['title_link'] = item["url_xivdb"] 
                if result not in locals():
                    result['text'] = name +" did find no matches " + querystr
                    #print item['name'].lower()
                    #print exactstr.lower()
            else:
                resulst['text']= name +' finds ' + str(obj["items"]["total"]) +' items matches ' + querystr 
                if obj["items"]["total"] > result_num:
                    result['text'] = result['text'] + ", shows first " + str(result_num) 
                pos = 0
                result['attachments'][0]['fields'] =[]
                for item in obj["items"]["results"]:
                    result['attachments'][0]['fields'].append({"title":item["name"], "title_link":item["url_xivdb"],"value":item["help"][:30]+"..."})
                    pos = pos + 1
                    if pos == result_num:
                        break
    except TypeError:
        result['text'] = name +" did find no matches " + querystr
    print(json.JSONEncoder().encode(result))
    #return result
    return HttpResponse(json.JSONEncoder().encode(result))
    return render(request.POST, 'index.html')

#test= {'user_name':'Memeroon', 'trigger_word':'xivdb', 'text':'xivdb -results 2 allagan'}
#slack(test)