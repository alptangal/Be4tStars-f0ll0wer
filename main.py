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
PASSWORD=None
@client.event
async def on_ready():
    global RESULT,THREADS,TIMERAND,PASSWORD
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
        PASSWORD=RESULT['password']
        async for msg in RESULT['usernamesCh'].history():
            username=msg.content
            THREADS.append({
                'username':username
            })
        if not login.is_running():
            login.start()
        if not confirmOtp.is_running():
            confirmOtp.start()
        if not follower.is_running():
            follower.start(guild)
        await asyncio.sleep(60)
        if not updateData.is_running():
            updateData.start(guild)
@tasks.loop(seconds=60)
async def updateData(guild):
    global RESULT,THREADS,PASSWORD
    THREADS=[]
    print('updateData is running')
    try:
        for thread in RESULT['threadsCh'].threads:
            if len([msg async for msg in thread.history()])==2:
                url='https://core.prod.beatstars.net/graphql?op=getMemberProfileByUsername'
                data={"operationName":"getMemberProfileByUsername","variables":{"username":thread.name.split('@')[0]},"query":"query getMemberProfileByUsername($username: String!) {\n  profileByUsername(username: $username) {\n    ...memberProfileInfo\n    __typename\n  }\n}\n\nfragment memberProfileInfo on Profile {\n  ...partialProfileInfo\n  location\n  bio\n  tags\n  badges\n  achievements\n  profileInventoryStatsWithUserContents {\n    ...mpGlobalMemberProfileUserContentStatsDefinition\n    __typename\n  }\n  socialInteractions(actions: [LIKE, FOLLOW, REPOST])\n  avatar {\n    assetId\n    fitInUrl(width: 200, height: 200)\n    sizes {\n      small\n      medium\n      large\n      mini\n      __typename\n    }\n    __typename\n  }\n  socialLinks {\n    link\n    network\n    profileName\n    __typename\n  }\n  activities {\n    follow\n    play\n    __typename\n  }\n  __typename\n}\n\nfragment partialProfileInfo on Profile {\n  displayName\n  username\n  memberId\n  location\n  v2Id\n  avatar {\n    assetId\n    sizes {\n      mini\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment mpGlobalMemberProfileUserContentStatsDefinition on ProfileInventoryStats {\n  playlists\n  __typename\n}\n"}
                req=requests.post(url,json=data)
                memberId=req.json()['data']['profileByUsername']['memberId']
                url='https://core.prod.beatstars.net/graphql?op=getProfileContentTrackList'
                data={"operationName":"getProfileContentTrackList","variables":{"memberId":memberId,"page":0,"size":12},"query":"query getProfileContentTrackList($memberId: String!, $page: Int, $size: Int) {\n  profileTracks(memberId: $memberId, page: $page, size: $size) {\n    content {\n      ...MpPartialTrackV3Data\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment MpPartialTrackV3Data on Track {\n  id\n  description\n  releaseDate\n  hasContracts\n  status\n  title\n  v2Id\n  seoMetadata {\n    slug\n    __typename\n  }\n  bundle {\n    date\n    hls {\n      url\n      type\n      signedUrl\n      duration\n      __typename\n    }\n    stream {\n      url\n      type\n      signedUrl\n      duration\n      __typename\n    }\n    __typename\n  }\n  profile {\n    memberId\n    badges\n    displayName\n    username\n    v2Id\n    avatar {\n      sizes {\n        mini\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  price\n  metadata {\n    itemCount\n    tags\n    bpm\n    free\n    offerOnly\n    __typename\n  }\n  artwork {\n    ...MpItemArtwork\n    __typename\n  }\n  socialInteractions(actions: [LIKE])\n  __typename\n}\n\nfragment MpItemArtwork on Image {\n  fitInUrl(width: 700, height: 700)\n  sizes {\n    small\n    medium\n    mini\n    __typename\n  }\n  assetId\n  __typename\n}\n"}
                
                req=requests.post(url,json=data)
                songs=[]
                js=req.json()
                for item in js['data']['profileTracks']['content']:
                    songs.append(item['v2Id'])
                url='https://core.prod.beatstars.net/auth/oauth/token'
                data={
                    'username':thread.name,
                    'password':PASSWORD,
                    'client_id':'5615656127.beatstars.com',
                    'client_secret':'2a$16$b376aMFTHFXoI1XXa$5xXWHjnyZUP61sGr$GKwZjT$ApolQQW',
                    'grant_type':'password'
                }
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.9',
                    'cookie':'AWSALBTG=ZNzvLt/kbYwtESQeSCzXkOgmSQztpuTIx7NV/4G+eOo+/X3YHV5JE0Qc5BdEM6MeO7kiYThK3r8JSL8V1/yXdqNNebGDDAqQ52fdUE/Int+eHvxGfFzIQd9UjyezFVwmQqXVoTDiB0Tl5QBHaJwbiPKnVXAuYUkvmTzNQlfX7+YO; AWSALBTGCORS=ZNzvLt/kbYwtESQeSCzXkOgmSQztpuTIx7NV/4G+eOo+/X3YHV5JE0Qc5BdEM6MeO7kiYThK3r8JSL8V1/yXdqNNebGDDAqQ52fdUE/Int+eHvxGfFzIQd9UjyezFVwmQqXVoTDiB0Tl5QBHaJwbiPKnVXAuYUkvmTzNQlfX7+YO; AWSALB=8eyy5XXN8KTvyxeJV6ha4BcoNTW5Dg9AmnPnUqxVMUR13byCW7prbhrUmP7WGrGsW4SVfZAj1K3wbTtsCL6W3SEnzXctifgdYVvU2DKxZfqzcnC/+XuUiOA+ipK6; AWSALBCORS=8eyy5XXN8KTvyxeJV6ha4BcoNTW5Dg9AmnPnUqxVMUR13byCW7prbhrUmP7WGrGsW4SVfZAj1K3wbTtsCL6W3SEnzXctifgdYVvU2DKxZfqzcnC/+XuUiOA+ipK6'
                }
                req=requests.post(url,headers=headers,data=data)
                if req.status_code<400:
                    js=req.json()
                    token=js['refresh_token']
                    url='https://core.prod.beatstars.net/auth/oauth/token'
                    data={
                        'refresh_token':token,
                        'client_id':'5615656127.beatstars.com',
                        'client_secret':'2a$16$b376aMFTHFXoI1XXa$5xXWHjnyZUP61sGr$GKwZjT$ApolQQW',
                        'grant_type':'refresh_token'
                    }
                    req=requests.post(url,headers=headers,data=data)
                    if req.status_code<400:
                        js=req.json()
                        token1=js['access_token']
                    THREADS.append({
                    'username':thread.name,
                    'memberId':memberId,
                    'songs':songs,
                    'token':token1 if 'token1' in locals() else None
                })
    except:
        pass
@tasks.loop(seconds=60)
async def login():
    global THREADS,RESULT,PASSWORD
    print('login is running')
    for data in THREADS:
        isset=False
        for thread in RESULT['threadsCh'].threads:
            if thread.name==data['username']:
                isset=thread
        if not isset:
            rs=await RESULT['threadsCh'].create_thread(name=data['username'],content='https://www.beatstars.com/'+data['username'].split('@')[0])
            isset=rs.thread
        if not isset or len([msg async for msg in isset.history()])==1:
            url='https://core.prod.beatstars.net/auth/oauth/token'
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.9',
                'cookie':'AWSALBTG=ZNzvLt/kbYwtESQeSCzXkOgmSQztpuTIx7NV/4G+eOo+/X3YHV5JE0Qc5BdEM6MeO7kiYThK3r8JSL8V1/yXdqNNebGDDAqQ52fdUE/Int+eHvxGfFzIQd9UjyezFVwmQqXVoTDiB0Tl5QBHaJwbiPKnVXAuYUkvmTzNQlfX7+YO; AWSALBTGCORS=ZNzvLt/kbYwtESQeSCzXkOgmSQztpuTIx7NV/4G+eOo+/X3YHV5JE0Qc5BdEM6MeO7kiYThK3r8JSL8V1/yXdqNNebGDDAqQ52fdUE/Int+eHvxGfFzIQd9UjyezFVwmQqXVoTDiB0Tl5QBHaJwbiPKnVXAuYUkvmTzNQlfX7+YO; AWSALB=8eyy5XXN8KTvyxeJV6ha4BcoNTW5Dg9AmnPnUqxVMUR13byCW7prbhrUmP7WGrGsW4SVfZAj1K3wbTtsCL6W3SEnzXctifgdYVvU2DKxZfqzcnC/+XuUiOA+ipK6; AWSALBCORS=8eyy5XXN8KTvyxeJV6ha4BcoNTW5Dg9AmnPnUqxVMUR13byCW7prbhrUmP7WGrGsW4SVfZAj1K3wbTtsCL6W3SEnzXctifgdYVvU2DKxZfqzcnC/+XuUiOA+ipK6'
            }
            data={
                'username':data['username'],
                'password':PASSWORD,
                'client_id':'5615656127.beatstars.com',
                'client_secret':'2a$16$b376aMFTHFXoI1XXa$5xXWHjnyZUP61sGr$GKwZjT$ApolQQW',
                'grant_type':'password'
            }
            req=requests.post(url,headers=headers,data=data)
            print(22222,req.text)
            if req.status_code>400:
                js=req.json()
                if js['code']=='MFA_VERIFICATION_ACTION':
                    await rs.thread.send(content='Enter otp sent to email '+data['username'])
            else:
                js=req.json()
                token=js['refresh_token']
                url='https://core.prod.beatstars.net/graphql?op=getMemberProfileByUsername'
                data={"operationName":"getMemberProfileByUsername","variables":{"username":data['username'].split('@')[0]},"query":"query getMemberProfileByUsername($username: String!) {\n  profileByUsername(username: $username) {\n    ...memberProfileInfo\n    __typename\n  }\n}\n\nfragment memberProfileInfo on Profile {\n  ...partialProfileInfo\n  location\n  bio\n  tags\n  badges\n  achievements\n  profileInventoryStatsWithUserContents {\n    ...mpGlobalMemberProfileUserContentStatsDefinition\n    __typename\n  }\n  socialInteractions(actions: [LIKE, FOLLOW, REPOST])\n  avatar {\n    assetId\n    fitInUrl(width: 200, height: 200)\n    sizes {\n      small\n      medium\n      large\n      mini\n      __typename\n    }\n    __typename\n  }\n  socialLinks {\n    link\n    network\n    profileName\n    __typename\n  }\n  activities {\n    follow\n    play\n    __typename\n  }\n  __typename\n}\n\nfragment partialProfileInfo on Profile {\n  displayName\n  username\n  memberId\n  location\n  v2Id\n  avatar {\n    assetId\n    sizes {\n      mini\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment mpGlobalMemberProfileUserContentStatsDefinition on ProfileInventoryStats {\n  playlists\n  __typename\n}\n"}
                req=requests.post(url,json=data)
                memberId=req.json()['data']['profileByUsername']['memberId']
                url='https://core.prod.beatstars.net/graphql?op=getProfileContentTrackList'
                data={"operationName":"getProfileContentTrackList","variables":{"memberId":memberId,"page":0,"size":12},"query":"query getProfileContentTrackList($memberId: String!, $page: Int, $size: Int) {\n  profileTracks(memberId: $memberId, page: $page, size: $size) {\n    content {\n      ...MpPartialTrackV3Data\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment MpPartialTrackV3Data on Track {\n  id\n  description\n  releaseDate\n  hasContracts\n  status\n  title\n  v2Id\n  seoMetadata {\n    slug\n    __typename\n  }\n  bundle {\n    date\n    hls {\n      url\n      type\n      signedUrl\n      duration\n      __typename\n    }\n    stream {\n      url\n      type\n      signedUrl\n      duration\n      __typename\n    }\n    __typename\n  }\n  profile {\n    memberId\n    badges\n    displayName\n    username\n    v2Id\n    avatar {\n      sizes {\n        mini\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  price\n  metadata {\n    itemCount\n    tags\n    bpm\n    free\n    offerOnly\n    __typename\n  }\n  artwork {\n    ...MpItemArtwork\n    __typename\n  }\n  socialInteractions(actions: [LIKE])\n  __typename\n}\n\nfragment MpItemArtwork on Image {\n  fitInUrl(width: 700, height: 700)\n  sizes {\n    small\n    medium\n    mini\n    __typename\n  }\n  assetId\n  __typename\n}\n"}
                
                req=requests.post(url,json=data)
                songs=[]
                js=req.json()
                for item in js['data']['profileTracks']['content']:
                    songs.append(item['v2Id'])
                url='https://core.prod.beatstars.net/auth/oauth/token'
                data={
                    'refresh_token':token,
                    'client_id':'5615656127.beatstars.com',
                    'client_secret':'2a$16$b376aMFTHFXoI1XXa$5xXWHjnyZUP61sGr$GKwZjT$ApolQQW',
                    'grant_type':'refresh_token'
                }
                req=requests.post(url,headers=headers,data=data)
                if req.status_code<400:
                    js=req.json()
                    token1=js['access_token']
                await isset.send(content=json.dumps(headers))
                THREADS.append({
                    'username':isset.name,
                    'memberId':memberId,
                    'songs':songs,
                    'token':token1 if 'token1' in locals() else None
                })
@tasks.loop(seconds=60)
async def confirmOtp():
    global THREADS,RESULT,PASSWORD
    print('confirmOtp is running')
    for thread in RESULT['threadsCh'].threads:
        msgs=[msg async for msg in thread.history()]
        if len(msgs)==3 and 'enter otp' in msgs[1].content.lower():
            url='https://core.prod.beatstars.net/auth/graphql'
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.9',
                'cookie':'AWSALBTG=ZNzvLt/kbYwtESQeSCzXkOgmSQztpuTIx7NV/4G+eOo+/X3YHV5JE0Qc5BdEM6MeO7kiYThK3r8JSL8V1/yXdqNNebGDDAqQ52fdUE/Int+eHvxGfFzIQd9UjyezFVwmQqXVoTDiB0Tl5QBHaJwbiPKnVXAuYUkvmTzNQlfX7+YO; AWSALBTGCORS=ZNzvLt/kbYwtESQeSCzXkOgmSQztpuTIx7NV/4G+eOo+/X3YHV5JE0Qc5BdEM6MeO7kiYThK3r8JSL8V1/yXdqNNebGDDAqQ52fdUE/Int+eHvxGfFzIQd9UjyezFVwmQqXVoTDiB0Tl5QBHaJwbiPKnVXAuYUkvmTzNQlfX7+YO; AWSALB=8eyy5XXN8KTvyxeJV6ha4BcoNTW5Dg9AmnPnUqxVMUR13byCW7prbhrUmP7WGrGsW4SVfZAj1K3wbTtsCL6W3SEnzXctifgdYVvU2DKxZfqzcnC/+XuUiOA+ipK6; AWSALBCORS=8eyy5XXN8KTvyxeJV6ha4BcoNTW5Dg9AmnPnUqxVMUR13byCW7prbhrUmP7WGrGsW4SVfZAj1K3wbTtsCL6W3SEnzXctifgdYVvU2DKxZfqzcnC/+XuUiOA+ipK6'
            }
            data={"operationName":"verifyMfa","variables":{"verifyMfaRequest":{"identifier":thread.name.split('@')[0],"pin":msgs[0].content}},"query":"mutation verifyMfa($verifyMfaRequest: VerifyMfaRequestInput!) {\n  verifyMfa(verifyMfaRequest: $verifyMfaRequest)\n}\n"}
            req=requests.post(url,headers=headers,json=data)
            if req.status_code<400:
                js=req.json()
                if js['data']['verifyMfa'].lower()=='ok':
                    for i,msg in enumerate(msgs):
                        if i!=len(msgs)-1:
                            await msg.delete()
                    data={}
                    data['headers']=headers
                    url='https://core.prod.beatstars.net/graphql?op=getMemberProfileByUsername'
                    data={"operationName":"getMemberProfileByUsername","variables":{"username":msgs[0].content.split('@')[0]},"query":"query getMemberProfileByUsername($username: String!) {\n  profileByUsername(username: $username) {\n    ...memberProfileInfo\n    __typename\n  }\n}\n\nfragment memberProfileInfo on Profile {\n  ...partialProfileInfo\n  location\n  bio\n  tags\n  badges\n  achievements\n  profileInventoryStatsWithUserContents {\n    ...mpGlobalMemberProfileUserContentStatsDefinition\n    __typename\n  }\n  socialInteractions(actions: [LIKE, FOLLOW, REPOST])\n  avatar {\n    assetId\n    fitInUrl(width: 200, height: 200)\n    sizes {\n      small\n      medium\n      large\n      mini\n      __typename\n    }\n    __typename\n  }\n  socialLinks {\n    link\n    network\n    profileName\n    __typename\n  }\n  activities {\n    follow\n    play\n    __typename\n  }\n  __typename\n}\n\nfragment partialProfileInfo on Profile {\n  displayName\n  username\n  memberId\n  location\n  v2Id\n  avatar {\n    assetId\n    sizes {\n      mini\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment mpGlobalMemberProfileUserContentStatsDefinition on ProfileInventoryStats {\n  playlists\n  __typename\n}\n"}
                    req=requests.post(url,json=data)
                    print(11111,req.text)
                    memberId=req.json()['data']['profileByUsername']['memberId']
                    url='https://core.prod.beatstars.net/graphql?op=getProfileContentTrackList'
                    data={"operationName":"getProfileContentTrackList","variables":{"memberId":memberId,"page":0,"size":12},"query":"query getProfileContentTrackList($memberId: String!, $page: Int, $size: Int) {\n  profileTracks(memberId: $memberId, page: $page, size: $size) {\n    content {\n      ...MpPartialTrackV3Data\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment MpPartialTrackV3Data on Track {\n  id\n  description\n  releaseDate\n  hasContracts\n  status\n  title\n  v2Id\n  seoMetadata {\n    slug\n    __typename\n  }\n  bundle {\n    date\n    hls {\n      url\n      type\n      signedUrl\n      duration\n      __typename\n    }\n    stream {\n      url\n      type\n      signedUrl\n      duration\n      __typename\n    }\n    __typename\n  }\n  profile {\n    memberId\n    badges\n    displayName\n    username\n    v2Id\n    avatar {\n      sizes {\n        mini\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  price\n  metadata {\n    itemCount\n    tags\n    bpm\n    free\n    offerOnly\n    __typename\n  }\n  artwork {\n    ...MpItemArtwork\n    __typename\n  }\n  socialInteractions(actions: [LIKE])\n  __typename\n}\n\nfragment MpItemArtwork on Image {\n  fitInUrl(width: 700, height: 700)\n  sizes {\n    small\n    medium\n    mini\n    __typename\n  }\n  assetId\n  __typename\n}\n"}
                
                    req=requests.post(url,json=data)
                    songs=[]
                    js=req.json()
                    for item in js['data']['profileTracks']['content']:
                        songs.append(item['v2Id'])
                    url='https://core.prod.beatstars.net/auth/oauth/token'
                    data={
                        'username':thread.name,
                        'password':PASSWORD,
                        'client_id':'5615656127.beatstars.com',
                        'client_secret':'2a$16$b376aMFTHFXoI1XXa$5xXWHjnyZUP61sGr$GKwZjT$ApolQQW',
                        'grant_type':'password'
                    }
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.9',
                        'cookie':'AWSALBTG=ZNzvLt/kbYwtESQeSCzXkOgmSQztpuTIx7NV/4G+eOo+/X3YHV5JE0Qc5BdEM6MeO7kiYThK3r8JSL8V1/yXdqNNebGDDAqQ52fdUE/Int+eHvxGfFzIQd9UjyezFVwmQqXVoTDiB0Tl5QBHaJwbiPKnVXAuYUkvmTzNQlfX7+YO; AWSALBTGCORS=ZNzvLt/kbYwtESQeSCzXkOgmSQztpuTIx7NV/4G+eOo+/X3YHV5JE0Qc5BdEM6MeO7kiYThK3r8JSL8V1/yXdqNNebGDDAqQ52fdUE/Int+eHvxGfFzIQd9UjyezFVwmQqXVoTDiB0Tl5QBHaJwbiPKnVXAuYUkvmTzNQlfX7+YO; AWSALB=8eyy5XXN8KTvyxeJV6ha4BcoNTW5Dg9AmnPnUqxVMUR13byCW7prbhrUmP7WGrGsW4SVfZAj1K3wbTtsCL6W3SEnzXctifgdYVvU2DKxZfqzcnC/+XuUiOA+ipK6; AWSALBCORS=8eyy5XXN8KTvyxeJV6ha4BcoNTW5Dg9AmnPnUqxVMUR13byCW7prbhrUmP7WGrGsW4SVfZAj1K3wbTtsCL6W3SEnzXctifgdYVvU2DKxZfqzcnC/+XuUiOA+ipK6'
                    }
                    req=requests.post(url,headers=headers,data=data)
                    if req.status_code<400:
                        js=req.json()
                        token=js['refresh_token']
                        url='https://core.prod.beatstars.net/auth/oauth/token'
                        data={
                            'refresh_token':token,
                            'client_id':'5615656127.beatstars.com',
                            'client_secret':'2a$16$b376aMFTHFXoI1XXa$5xXWHjnyZUP61sGr$GKwZjT$ApolQQW',
                            'grant_type':'refresh_token'
                        }
                        req=requests.post(url,headers=headers,data=data)
                        if req.status_code<400:
                            js=req.json()
                            token1=js['access_token']
                    THREADS.append({
                        'username':thread.name,
                        'memberId':memberId,
                        'songs':songs,
                        'token':token1 if 'token1' in locals() else None
                    })
                    await thread.send(content=json.dumps(headers))
@tasks.loop(seconds=1)
async def follower(guild):
    print('follower is running')
    global RESULT,THREADS,TIMERAND
    for thread in THREADS:
        if 'token' in thread:
            for item in THREADS:
                if item['username']!=thread['username']:
                    url='https://core.prod.beatstars.net/graphql?op=follow'
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.9',
                        'Authorization': 'Bearer '+thread['token']
                        }
                    data={"operationName":"follow","variables":{"itemId":item['memberId'],"options":{}},"query":"mutation follow($itemId: String!, $options: InteractionItemContextInput) {\n  follow(itemId: $itemId, options: $options)\n}\n"}
                    req=requests.post(url,headers=headers,json=data)
                    print(req.text)
                    if req.status_code<400:
                        print('Increament 1 Follower')
client.run(os.environ.get('t'))

