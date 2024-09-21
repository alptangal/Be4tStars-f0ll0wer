import asyncio
import os
import re
import discord
from discord.ext import commands, tasks
from discord.utils import get
import random
from suno import *
from guild import *
import server
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

intents = discord.Intents.default()
client = discord.Client(intents=intents)

GUILD_ID=1122707918177960047
RESULT=None
THREADS=[]
TIMERAND=None
@client.event
async def on_ready():
    global RESULT,THREADS,TIMERAND
    try:
        req=requests.get('http://localhost:8888')
        print(req.status_code)
        await client.close() 
        print('Client closed')
        exit()
    except:
        server.b()
        TIMERAND=random.randrange(0,23)
        guild = client.get_guild(GUILD_ID)
        RESULT=await getBasic(guild)
        for thread in RESULT['threadsCh'].threads:
            msgs=[msg async for msg in thread.history(oldest_first=True)]
            url='https://core.prod.beatstars.net/graphql?op=getMemberProfileByUsername'
            data={"operationName":"getMemberProfileByUsername","variables":{"username":msgs[0].content.split('/')[-1]},"query":"query getMemberProfileByUsername($username: String!) {\n  profileByUsername(username: $username) {\n    ...memberProfileInfo\n    __typename\n  }\n}\n\nfragment memberProfileInfo on Profile {\n  ...partialProfileInfo\n  location\n  bio\n  tags\n  badges\n  achievements\n  profileInventoryStatsWithUserContents {\n    ...mpGlobalMemberProfileUserContentStatsDefinition\n    __typename\n  }\n  socialInteractions(actions: [LIKE, FOLLOW, REPOST])\n  avatar {\n    assetId\n    fitInUrl(width: 200, height: 200)\n    sizes {\n      small\n      medium\n      large\n      mini\n      __typename\n    }\n    __typename\n  }\n  socialLinks {\n    link\n    network\n    profileName\n    __typename\n  }\n  activities {\n    follow\n    play\n    __typename\n  }\n  __typename\n}\n\nfragment partialProfileInfo on Profile {\n  displayName\n  username\n  memberId\n  location\n  v2Id\n  avatar {\n    assetId\n    sizes {\n      mini\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment mpGlobalMemberProfileUserContentStatsDefinition on ProfileInventoryStats {\n  playlists\n  __typename\n}\n"}
            req=requests.post(url,json=data)
            memberId=req.json()['data']['profileByUsername']['memberId']
            url='https://core.prod.beatstars.net/graphql?op=getProfileContentTrackList'
            data={"operationName":"getProfileContentTrackList","variables":{"memberId":memberId,"page":0,"size":12},"query":"query getProfileContentTrackList($memberId: String!, $page: Int, $size: Int) {\n  profileTracks(memberId: $memberId, page: $page, size: $size) {\n    content {\n      ...MpPartialTrackV3Data\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment MpPartialTrackV3Data on Track {\n  id\n  description\n  releaseDate\n  hasContracts\n  status\n  title\n  v2Id\n  seoMetadata {\n    slug\n    __typename\n  }\n  bundle {\n    date\n    hls {\n      url\n      type\n      signedUrl\n      duration\n      __typename\n    }\n    stream {\n      url\n      type\n      signedUrl\n      duration\n      __typename\n    }\n    __typename\n  }\n  profile {\n    memberId\n    badges\n    displayName\n    username\n    v2Id\n    avatar {\n      sizes {\n        mini\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  price\n  metadata {\n    itemCount\n    tags\n    bpm\n    free\n    offerOnly\n    __typename\n  }\n  artwork {\n    ...MpItemArtwork\n    __typename\n  }\n  socialInteractions(actions: [LIKE])\n  __typename\n}\n\nfragment MpItemArtwork on Image {\n  fitInUrl(width: 700, height: 700)\n  sizes {\n    small\n    medium\n    mini\n    __typename\n  }\n  assetId\n  __typename\n}\n"}
            
            req=requests.post(url,json=data)
            songs=[]
            js=req.json()
            for item in js['data']['profileTracks']['content']:
                songs.append(item['v2Id'])
            THREADS.append({
                'username':msgs[0].content.split('/')[-1],
                'memberId':memberId,
                'lastMsg':msgs[-1],
                'songs':songs
            })
        
        if not follower.is_running():
            follower.start(guild)
        await asyncio.sleep(60)
        if not updateData.is_running():
            updateData.start(guild)
@tasks.loop(seconds=60)
async def updateData(guild):
    global RESULT,THREADS
    THREADS=[]
    print('updateData is running')
    try:
        RESULT=await getBasic(guild)
        rows=[]
        for msg in RESULT['usernames']:
            rows.append(msg.content)
        for row in rows:
            user=row.split('/')[-1]
            isset=False
            for thread in RESULT['threadsCh'].threads:
                if user==thread.name:
                    isset=True
                    try:
                        msgs=[msg async for msg in thread.history(oldest_first=True)]
                        url='https://core.prod.beatstars.net/graphql?op=getMemberProfileByUsername'
                        data={"operationName":"getMemberProfileByUsername","variables":{"username":msgs[0].content.split('/')[-1]},"query":"query getMemberProfileByUsername($username: String!) {\n  profileByUsername(username: $username) {\n    ...memberProfileInfo\n    __typename\n  }\n}\n\nfragment memberProfileInfo on Profile {\n  ...partialProfileInfo\n  location\n  bio\n  tags\n  badges\n  achievements\n  profileInventoryStatsWithUserContents {\n    ...mpGlobalMemberProfileUserContentStatsDefinition\n    __typename\n  }\n  socialInteractions(actions: [LIKE, FOLLOW, REPOST])\n  avatar {\n    assetId\n    fitInUrl(width: 200, height: 200)\n    sizes {\n      small\n      medium\n      large\n      mini\n      __typename\n    }\n    __typename\n  }\n  socialLinks {\n    link\n    network\n    profileName\n    __typename\n  }\n  activities {\n    follow\n    play\n    __typename\n  }\n  __typename\n}\n\nfragment partialProfileInfo on Profile {\n  displayName\n  username\n  memberId\n  location\n  v2Id\n  avatar {\n    assetId\n    sizes {\n      mini\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment mpGlobalMemberProfileUserContentStatsDefinition on ProfileInventoryStats {\n  playlists\n  __typename\n}\n"}
                        req=requests.post(url,json=data)
                        memberId=req.json()['data']['profileByUsername']['memberId']
                        url='https://core.prod.beatstars.net/graphql?op=getProfileContentTrackList'
                        data={"operationName":"getProfileContentTrackList","variables":{"memberId":memberId,"page":0,"size":12},"query":"query getProfileContentTrackList($memberId: String!, $page: Int, $size: Int) {\n  profileTracks(memberId: $memberId, page: $page, size: $size) {\n    content {\n      ...MpPartialTrackV3Data\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment MpPartialTrackV3Data on Track {\n  id\n  description\n  releaseDate\n  hasContracts\n  status\n  title\n  v2Id\n  seoMetadata {\n    slug\n    __typename\n  }\n  bundle {\n    date\n    hls {\n      url\n      type\n      signedUrl\n      duration\n      __typename\n    }\n    stream {\n      url\n      type\n      signedUrl\n      duration\n      __typename\n    }\n    __typename\n  }\n  profile {\n    memberId\n    badges\n    displayName\n    username\n    v2Id\n    avatar {\n      sizes {\n        mini\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  price\n  metadata {\n    itemCount\n    tags\n    bpm\n    free\n    offerOnly\n    __typename\n  }\n  artwork {\n    ...MpItemArtwork\n    __typename\n  }\n  socialInteractions(actions: [LIKE])\n  __typename\n}\n\nfragment MpItemArtwork on Image {\n  fitInUrl(width: 700, height: 700)\n  sizes {\n    small\n    medium\n    mini\n    __typename\n  }\n  assetId\n  __typename\n}\n"}
                    
                        req=requests.post(url,json=data)
                        songs=[]
                        js=req.json()
                        for item in js['data']['profileTracks']['content']:
                            songs.append(item['v2Id'])
                        THREADS.append({
                            'username':msgs[0].content.split('/')[-1],
                            'memberId':memberId,
                            'lastMsg':msgs[-1],
                            'songs':songs
                        })
                    except:
                        pass
            if not isset:
                rs=await RESULT['threadsCh'].create_thread(name=user,content=row)
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.9',
                    }
                req=requests.get('https://main.v2.beatstars.com/musician?permalink='+user+'&fields=profile,user_contents,stats,bulk_deals,social_networks',headers=headers)
                if req.status_code<400:
                    js=req.json()
                    try:
                        await rs.thread.send(content=f"``FOLLOWERS``== **{js['response']['data']['stats']['followers']}** | ``PLAYS``== **{js['response']['data']['stats']['plays']}** | ``TRACKS``== **{js['response']['data']['stats']['tracks']}**")
                    except:
                        pass
    except:
        pass
@tasks.loop(seconds=1)
async def follower(guild):
    print('follower is running')
    global RESULT,THREADS,TIMERAND
    for thread in THREADS:
            username=thread['username']
            url='https://core.prod.beatstars.net/graphql?op=follow'
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.9',
                'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImJ0cy1rZXktaWQifQ.eyJhdWQiOlsib2F1dGgyLXJlc291cmNlIl0sInVzZXJfbmFtZSI6Ik1SNzA2MDA2MiIsInNjb3BlIjpbInJlYWQiLCJ3cml0ZSIsInRydXN0Il0sImV4cCI6MTcyOTUyNDExMCwiYXV0aG9yaXRpZXMiOlsiUk9MRV9VU0VSIl0sImp0aSI6InVRYmZ3b1doZ2pmRTEtS0hPVUdXaTRPVjA2VSIsImNsaWVudF9pZCI6IjU2MTU2NTYxMjcuYmVhdHN0YXJzLmNvbSJ9.SqgMt-SnHu1oeGOk6kI0JMIikzYeS9YfJE2gQgtHGHl0yYyg1Cn62InP5hK9TCh43ilGtdLirCbBwg5j1JeamL1KOpIW4ZPQ6KeuLb-7R2LT8bXyBkpFY5PNwU34Q-Pu2irQ4rupb_MaaJCfQzoQolL_VXI4KT02fcsaNZU3bp75OwJaahEUiF0QT0ON9OEg-MiGQeFP0aIkcH0Ykc0Lp3L-eSPe1tjSKAyl6EzYk4HO6mNYabtu5UTT_ohW5q4bdNedQsoLkFf4NNmxS3y3Wl37dNvI-FYbpWCZeGLh7LbmYNrAoPxrsj07HXuV6Dp0xtRB1fe4bsl02ZkcyckZJA',

            }
            for songId in thread['songs']:
                data={"operationName":"follow","variables":{"itemId":thread['memberId'],"options":{}},"query":"mutation follow($itemId: String!, $options: InteractionItemContextInput) {\n  follow(itemId: $itemId, options: $options)\n}\n"}
                req=requests.post(url,headers=headers,json=data)
                if req.status_code<400:
                    print('Increament 1 Played')
            if datetime.now().hour==TIMERAND and datetime.now().minute==0:
                req=requests.get('https://main.v2.beatstars.com/musician?permalink='+username+'&fields=profile,user_contents,stats,bulk_deals,social_networks')
                js=req.json()
                try:
                    await thread.lastMsg.edit(content=f"``FOLLOWERS``== **{js['response']['data']['stats']['followers']}** | ``PLAYS``== **{js['response']['data']['stats']['plays']}** | ``TRACKS``== **{js['response']['data']['stats']['tracks']}**")
                except:
                    pass
client.run(os.environ.get('botToken'))

