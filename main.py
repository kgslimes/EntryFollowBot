import requests
import graphql
import os
from bs4 import BeautifulSoup as bs
import traceback
from fflask import thread
import json

pre_id = ''
id = ''

#로그인

with requests.Session() as s:
    loginPage = s.get('https://playentry.org/signin')
    soup = bs(loginPage.text, 'html.parser')
    csrf = soup.find('meta', {'name': 'csrf-token'})
    login_headers={'CSRF-Token': csrf['content'], "Content-Type": "application/json"}
    req = s.post('https://playentry.org/graphql',     
    headers=login_headers, json={'query':graphql.login, 'variables':{"username":os.environ['id'],"password":os.environ['pass']}})
    soup = bs(s.get("https://playentry.org").text, "html.parser")
    xtoken = json.loads(soup.select_one("#__NEXT_DATA__").get_text()
                        )["props"]["initialState"]["common"]["user"]["xToken"]
    headers = {'X-Token': xtoken, 'x-client-type': 'Client', 'CSRF-Token': csrf['content'], "Content-Type": "application/json"}

    def follow(lid):
        global pre_id
        s.post('https://playentry.org/graphql', headers=headers, json={'query':graphql.follow, "variables":{"user":lid}})
        print(f"{lid}님을 팔로우했어요!")


#글 읽고 답하기

    while True:
      try:
        req = s.post('https://playentry.org/graphql', headers=headers, json={'query':graphql.loadStory, "variables":{"category":"free","searchType":"scroll","term":"all","discussType":"entrystory","pageParam":{"display":1,"sort":"created"}}})
        story = req.text
        llid = story[story.index('"user"')+14:story.index('"user"')+14+24]
        if pre_id != llid:
          follow(llid)
          pre_id = llid
      except:
        print(traceback.format_exc())