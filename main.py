
import requests, random, time, string, hashlib,hmac,sys,uuid,json,os
from user_agent import *
if sys.version_info.major == 3:
    import urllib.parse


class BasicAPI:
    def __init__(self, username, password):
        self.r = requests.session()
        self.uuid = str(uuid.uuid4())
        self.username = username
        self.password = password
        self.isloggedin = False
        self.useragent = 'Instagram 37.0.0.9.96 (iPhone10,3; iOS 11_2_6; ru_UA; ru-UA; scale=3.00; gamut=wide; 1125x2436)'
        self.IG_SIG_KEY = '109513c04303341a7daf27bb41b268e633b30dcc65a3fe14503f743176113869'
        

    def signature(self, data):
        body = (hmac.new(self.IG_SIG_KEY.encode("utf-8"), data.encode("utf-8"), hashlib.sha256).hexdigest()+ "."+ urllib.parse.quote(data))
        signature = "signed_body={body}&ig_sig_key_version=4"
        return signature.format(body=body)

    def generateDeviceId(self, seed):
        volatile_seed = "12345"
        m = hashlib.md5()
        m.update(seed.encode('utf-8') + volatile_seed.encode('utf-8'))
        return 'android-' + m.hexdigest()[:16]

    def generateUUID(self, type):
        generated_uuid = str(uuid.uuid4())
        if (type):return generated_uuid
        else:return generated_uuid.replace('-', '')

    def SendRequest(self,url, data=None, headers=None):
        if headers == None:
            self.r.headers.update({'Connection': 'close','Accept': '*/*','Content-type': 'application/x-www-form-urlencoded; charset=UTF-8','Cookie2': '$Version=1','Accept-Language': 'en-US','User-Agent': self.useragent})
        else:self.r.headers.update(headers)
        if data == None:
            while True:
                try:api = self.r.get(url);break
                except: pass
        else:
            while True:
                try:api = self.r.post(url, data=data);break
                except:pass
        try:self.Json = json.loads(api.text)
        except:self.Json = 'Error'
        if api.status_code == 200:
            return True
        else:print(api.text, api.status_code);return False
        

    def loggin(self):
        try:
            m =hashlib.md5();m.update(self.username.encode('utf-8') + self.password.encode('utf-8'));device_id = self.generateDeviceId(m.hexdigest());self.r.headers.update({'Connection': 'close','Accept': '*/*','Content-type': 'application/x-www-form-urlencoded; charset=UTF-8','Cookie2': '$Version=1','Accept-Language': 'en-US','User-Agent': self.useragent});response = requests.get('https://www.instagram.com')
            try:csrf = response.cookies['csrftoken']
            except:letters = string.ascii_lowercase;csrf = ''.join(random.choice(letters) for i in range(8))
            LastResponse = self.r.get('https://i.instagram.com/api/v1/si/fetch_headers/?challenge_type=signup&guid=' + self.generateUUID(False));data = {'phone_id': self.generateUUID(True),'_csrftoken': csrf,'username': self.username,'guid': self.generateUUID(True),'device_id': device_id,'password': self.password,'login_attempt_count': '0'}
            while True:
                try:login = self.r.post('https://b.i.instagram.com/api/v1/accounts/login/', self.signature(json.dumps(data)));break
                except Exception as e:
                    print(e)
            if 'logged_in_user' in login.text:self.session=login.cookies['sessionid']; self.username_id = login.json()["logged_in_user"]["pk"];self.token = self.r.cookies["csrftoken"];print('Logged In!\n');self.isloggedin=True
            else:print(login.text)

        except Exception as e:print(e)

    def getInbox(self):
        urinbox = 'https://i.instagram.com/api/v1/direct_v2/inbox/?persistentBadging=true&cursor='
        hed1 = { 'accept': '*/*', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'ar,en-US;q=0.9,en;q=0.8', 'cookie': 'ig_did=77A45489-9A4C-43AD-9CA7-FA3FAB22FE24; ig_nrcb=1; mid=YGwlfgALAAEryeSgDseYghX2LAC-; csrftoken=EMbT4gJqC4q9NTF2JVgBrAnTNC2MGPQA; ds_user_id=47432466264; datr=9D0-YLR0rApS9iOG6npp3drV; shbid=489; shbts=1616344547.8202462; rur=ASH; sessionid='+self.session, 'origin': 'https://www.instagram.com', 'referer': 'https://www.instagram.com/', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 Edg/91.0.864.71', 'x-ig-app-id': '936619743392459', 'x-ig-www-claim': 'hmac.AR0EWvjix_XsqAIjAt7fjL3qLwQKCRTB8UMXTGL5j7pkgbG4' }
        return self.SendRequest(urinbox,data=None,headers=hed1)
    
    def delChat(self,json):
        hed1 = { 'accept': '*/*', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'ar,en-US;q=0.9,en;q=0.8', 'content-length': '0', 'content-type': 'application/x-www-form-urlencoded', 'cookie': 'ig_did=77A45489-9A4C-43AD-9CA7-FA3FAB22FE24; ig_nrcb=1; mid=YGwlfgALAAEryeSgDseYghX2LAC-; csrftoken=EMbT4gJqC4q9NTF2JVgBrAnTNC2MGPQA; ds_user_id=47432466264; datr=9D0-YLR0rApS9iOG6npp3drV; shbid=489; shbts=1616344547.8202462; rur=ASH; sessionid='+self.session, 'origin': 'https://www.instagram.com', 'referer': 'https://www.instagram.com/', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 Edg/91.0.864.71', 'x-csrftoken': 'EMbT4gJqC4q9NTF2JVgBrAnTNC2MGPQA', 'x-ig-app-id': '1217981644879628', 'x-ig-www-claim': 'hmac.AR24Fkd2DvunQ5ELQD_I_6FoVMTbIdkiDD08ZF2jyPhpEmIg', 'x-instagram-ajax': '753ce878cd6d'}
        for item in json['inbox']['threads']:
            try:
                user = item['users'][0]['username']
                thread = str(item['thread_id'])
                url = f'https://i.instagram.com/api/v1/direct_v2/threads/{thread}/hide/'
                start =self.r.post(url,headers=hed1)
                if '"status":"ok"' in start.text:
                    print(f'Deleted chat for => {user}')
                else:print(f'Error deleting chat for => {user} | {start.text}')
            except IndexError:continue
            


    
if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    user = input("[+] Enter username: ")
    pasw = input("[+] Enter password: ")
    api = BasicAPI(user, pasw)
    api.loggin()
    if api.isloggedin:
      api.getInbox()
      while 'client_context' in str(api.Json):
          api.delChat(api.Json)
          time.sleep(5) #time delay to avoid 429
          api.getInbox()
      input('\n[Done] All DMs Deleted! Press Enter To Exit...')
