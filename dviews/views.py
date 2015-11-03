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
    querystr = query['text']
    #print(query)
    if querystr == False:
        return HttpResponse("Couldn't find key text in POST:" + ''.join(request.body.items()) + " or GET:" + ''.join(request.body.items()))
        return render(request.POST, 'index.html')
    querystr = querystr[len(query['trigger_word'])+1:] # replace with slack token string
    name = query['user_name']
    while querystr[:1] == '-':
        arraystr = querystr.split()
        if arraystr[0].lower() == '-help':
            result['text'] = ('Memeroon can helps in following ways!\n' 
                'Give Memeroon item name and Memeroon tries best to finds.\Memeroon' 
                'n knows these trickys at a start\n' 
                '-exact and Memeroon only gives exact match!  \n' 
                '-results and Memeroon will give that many! Mememroon doesn\'t think you should pick a big one... \n'
                '-help and Memeroon will explains again.')
            return HttpResponse(json.JSONEncoder().encode(result))        
        if len(arraystr) == 1:
            result['text']= 'Mememroon can\'t help with '+ arraystr[0][1:] +' if you not tell what to do!'
            return HttpResponse(json.JSONEncoder().encode(result))        
        if arraystr[0].lower() == '-exact':
            exact = True
            querystr = querystr[len(arraystr[0])+1:]
        elif arraystr[0].lower() == '-results':
            if arraystr[1].isdigit():
                result_num = int(arraystr[1])
                querystr = querystr[len(arraystr[0])+len(arraystr[1])+2:]
            else:
                result['text']= 'Memeroon no can count to ' +str(arraystr[1]) +'!'
                return HttpResponse(json.JSONEncoder().encode(result))

    if len(querystr) < 1:
        result['text']= 'Memeroon no can match nothing! You expect miracle from Memeroon!'
        return HttpResponse(json.JSONEncoder().encode(result))
    #print(querystr)
    r = requests.get('http://api.xivdb.com/search?string=' + querystr )
    obj = r.json()
    #print(r.text)
    try:
        if obj["items"]["total"] == '1':
            item = obj["items"]["results"].pop()  
            result['text']= 'Memeroon finds this item matches ' + querystr
            if exact:
                result['text'] += ' exactly'
            result['attachments'][0]['title'] = item["name"] 
            result['attachments'][0]['text'] = item["help"]
            result['attachments'][0]['fallback'] = item["name"] + item["help"]
            result['attachments'][0]['thumb_url'] = item["icon"] 
            result['attachments'][0]['title_link'] = item["url_xivdb"] 
        elif obj["items"]["total"] > 1:
            #print('hit')
            if exact == True:
                for item in obj['items']['results']:
                    if item['name'].lower() == querystr.lower():
                        result['text']= 'Memeroon finds this item matches ' + querystr + ' exactly'
                        result['attachments'][0]['title'] = item["name"] 
                        result['attachments'][0]['text'] = item["help"]
                        result['attachments'][0]['fallback'] = item["name"] + item["help"]
                        result['attachments'][0]['thumb_url'] = item["icon"] 
                        result['attachments'][0]['title_link'] = item["url_xivdb"] 

                if 'text' not in result["attachments"][0]:
                    result['text'] = name +" did find no matches " + querystr
                    #print item['name'].lower()
                    #print exactstr.lower()
            else:
                result['text']= 'Memeroon finds ' + str(obj["items"]["total"]) +' items matches ' + querystr 
                if obj["items"]["total"] > result_num:
                    result['text'] = result['text'] + ", shows first " + str(result_num) 
                pos = 0
                result['attachments'][0]['fields'] =[]
                for item in obj["items"]["results"]:
                    print (result)
                    result['attachments'][0]['fields'].append({"title":item["name"],"value":'<'+ item["url_xivdb"]  +'|Link> ' +item["help"]})
                    pos = pos + 1
                    if pos == result_num:
                        break
    except TypeError:
        result['text'] = "Memeroon did find no matches " + querystr
    #print(json.JSONEncoder().encode(result))
    #return result
    return HttpResponse(json.JSONEncoder().encode(result))
    return render(request.POST, 'index.html')

#test= {'user_name':'Memeroon', 'trigger_word':'xivdb', 'text':'xivdb -results 2 allagan'}
#slack(test)