import urllib.request
import urllib.parse
req = urllib.request.Request('https://resort-1-zn3k.onrender.com/api/registrations', data=b"{}", headers={'Origin': 'https://resort-omega-henna.vercel.app', 'Content-Type': 'application/json'})
try:
    response = urllib.request.urlopen(req)
except urllib.error.HTTPError as e:
    print(e.code)
    print(e.headers)
