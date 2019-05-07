import json
import requests

from requests.exceptions import Timeout
DEF_TIMEOUT = 10
TEAM_NAME = "NETWORK HEALTH CHECK (NP1)"
ROOM_TITLE = "NP1"

requests.packages.urllib3.disable_warnings()

def createTeam(botToken=''):
    postUrl     = "https://api.ciscospark.com/v1/teams"
    headers     = {"Authorization": "Bearer " + botToken,
                   "Content-Type": "application/json; charset=utf-8"}
    body_json   = {"name": TEAM_NAME}

    try:
        response = requests.post(postUrl, json.dumps(body_json), headers=headers, verify=False, timeout=DEF_TIMEOUT)
    except Timeout as e:
        raise Timeout(e)
    else:
        response = response.json()
        if 'errors' in response.keys():
            raise BaseException('Bot API error: %s' % response['errors'][0]['description'])
        else:
            return response["id"]

def createRoomInTeam(botToken='', teamId=''):
    postUrl     = "https://api.ciscospark.com/v1/rooms"
    headers     = {"Authorization": "Bearer " + botToken,
                   "Content-Type": "application/json; charset=utf-8"}
    body_json   = { "title" : ROOM_TITLE, "teamId" : teamId }

    try:
        response = requests.post(postUrl, json.dumps(body_json), headers=headers, verify=False, timeout=DEF_TIMEOUT)
    except Timeout as e:
        raise Timeout(e)
    else:
        response = response.json()
        if 'errors' in response.keys():
            raise BaseException('Bot API error: %s' % response['errors'][0]['description'])
        else:
            return response["id"]

def addPeopleToSpace(roomId='', listOfEmails=[], botToken=''):
    postUrl = "https://api.ciscospark.com/v1/memberships"
    headers = {"Authorization": "Bearer " + botToken,
               "Content-Type": "application/json; charset=utf-8"}

    for index, email in enumerate(listOfEmails):
        body_json = {"roomId" : roomId,
                     "personEmail" : email}
        if not email == '':
            try:
                response = requests.post(postUrl, json.dumps(body_json), headers=headers, verify=False, timeout=DEF_TIMEOUT)
            except Timeout as e:
                raise Timeout(e)
            else:
                status, response = response.status_code, response.json()
                if 'errors' in response.keys():
                    raise BaseException('Bot API error: %s' % response['errors'][0]['description'])
                print(str(index) + " Email: "+ email + " Status: " + str(status) + "\n")

def printMessage(roomId='', message='', botToken=''):
    postUrl     = "https://api.ciscospark.com/v1/messages"
    headers     = {"Authorization": "Bearer " + botToken,
                   "Content-Type": "application/json; charset=utf-8"}
    body_json   = {"roomId" : roomId,
                   "text" : message}
    try:
        response = requests.post(postUrl, json.dumps(body_json), headers=headers, verify=False, timeout=DEF_TIMEOUT)
    except Timeout as e:
        raise Timeout(e)
    else:
        response = response.json()
        if 'errors' in response.keys():
            raise BaseException('Bot API error: %s' % response['errors'][0]['description'])
        print('Message sending to Webex room [%s]\n\n' % roomId, response)

if __name__ == "__main__":
    #Access Token accessToken

    accessToken = ""

    headers = {"Authorization": "Bearer " + accessToken,
               "Content-Type": "application/json; charset=utf-8"}
    listOfEmails = [
        "",
        "",
    ]
    welcomeMessage = "Hi, it's Network Health check. "

    printMessage(roomId, test, accessToken)
