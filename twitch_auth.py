import json, requests
from urllib.parse import quote
from re import sub
from dotenv import dotenv_values
from pickle import dumps
from base64 import b64encode

def refresh_auth(prefix, refreshToken, clientID, clientSecret):
    headers = {
                "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
                "grant_type": "refresh_token",
                "refresh_token": quote(refreshToken),
                "client_id": clientID,
                "client_secret": clientSecret
    }
    resp = requests.post("https://id.twitch.tv/oauth2/token", headers=headers, data=data)
    if resp.status_code == 400:
        print("[-] Failed to get new access token.")
        return False
    else:
#        print(resp.text)
        new_codes = json.loads(resp.text)
        replace_keys(prefix, new_codes[f'access_token'], new_codes[f'refresh_token'])
        return new_codes[f'access_token']

def replace_keys(prefix: str, ACCESS_TOKEN, REFRESH_TOKEN):
#    print("Prefix: " + prefix)
#    print("Access Token: " + ACCESS_TOKEN)
#    print("Refresh Token: " + REFRESH_TOKEN)
    with open('.env', 'r+') as f:
        envContent = f.read()
        newContent = sub(f'{prefix}_ACCESS_TOKEN=\".*\"', f'{prefix}_ACCESS_TOKEN=\"{ACCESS_TOKEN}\"', envContent)
        newContent = sub(f'{prefix}_REFRESH_TOKEN=\".*\"',f'{prefix}_REFRESH_TOKEN=\"{REFRESH_TOKEN}\"', newContent)
        f.seek(0)
        f.write(newContent)
        f.truncate()

def main():
    config = dotenv_values()
    refresh_auth("SH", config["SH_REFRESH_TOKEN"], config["SH_CLIENT_ID"], config["SH_CLIENT_SECRET"])
    refresh_auth("AL", config["AL_REFRESH_TOKEN"], config["AL_CLIENT_ID"], config["AL_CLIENT_SECRET"])
    config_new = dotenv_values()
    data = dumps(config_new)
    print("Env Data: " + b64encode(data).decode())

if __name__ == '__main__':
    main()