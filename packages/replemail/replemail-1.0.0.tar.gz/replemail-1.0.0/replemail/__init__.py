import requests, base64

class ReplEmail(object):
    def __init__(self, username, api_key):
        self.base = 'https://repl.email/api'

        self.session = requests.Session()
        self.session.headers.update({
            'user': username,
            'token': api_key,
        })
        self._load()
    
    # internal
    def _call(self, route, data={}, retry=True):
        r = self.session.post(f'{self.base}{route}', json=data)
        try:
            res = r.json()
            if 'err' in res:
                if retry:
                    self._load()
                    return self._call(route, data=data, retry=False)
        except:
            pass
        finally:
            return r
    
    def _load(self):
        return self._call('/load', data={
            'user': self.session.headers['user'],
            'token': self.session.headers['token']
        }).text
    
    # user functions
    def pfp(self, username):
        """Get repl.it user profile picture by username"""
        return self._call('/profile', data={'username': username}).json()
    
    def contacts(self):
        """Get a list of contacts"""
        return self._call('/contacts').json()
    
    def send(self, to: list, subject: str, text: str=None, html: str=None, send_at=None):
        """Send an email"""
        return self._call('/send', data={
            'to': to,
            'subject': subject,
            'text': text,
            'html': html,
            'send_at': send_at,
        }).json()
    
    def settings(self, **kwargs):
        """Get/Update settings (from kwargs)"""
        return self._call('/settings', data=kwargs).json()
    
    def delete(self, id):
        """Mark email as DELETED from ID"""
        return self._call('/delete', data={'id': id}).text
    
    def permadelete(self, id):
        """Permanently delete an email from ID"""
        return self._call('/delete/forever', data={'id': id}).text
    
    def fetch(self, num=-1):
        """Fetch emails"""
        return self._call('/get', {'num': num}).json()
    
    def flag(self, emails: dict):
        """Change message flags (not update, change)"""
        return self._call('/flags', emails).text
    
    def sent(self):
        """Get sent messages"""
        return self._call('/sent').json()
    
    def upload(self, raw, filename):
        return self._call('/upload', {
            'filename': filename,
            'data': base64.b64encode(raw).decode()
        }).json()