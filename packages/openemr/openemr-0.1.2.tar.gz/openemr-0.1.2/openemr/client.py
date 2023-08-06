"""
Core openemr rest api client functionality.
"""

import requests
from urllib.parse import urlencode

from openemr import __version__
_USER_AGENT = "OpenEmrApiClientPython/%s" % __version__

class Client(object):
    """Performs requests to the OpenEmr rest API."""

    def __init__(self, client_user, client_pass, url = "https://localhost/apis/api", client_scope = "default"):
        """Base OpenEmr api client."""
        
        self.url = url
        self.client_user = client_user
        self.client_pass = client_pass
        self.client_scope = client_scope
        self.session = requests.Session()
        self._login()

    def _login(self):
        """Log in to the api by retrieving a Bearer token"""

        self.session.headers.update({
            'User-Agent': _USER_AGENT,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })

        payload = {
            "grant_type": "password",
            "username": self.client_user,
            "password": self.client_pass,
            "scope": self.client_scope
        }

        self.token = self.session.post(
            url = str(self.url + '/auth'),
            data = payload
        ).json()['access_token']

        self.session.headers.update({
            'User-Agent': _USER_AGENT,
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        })

    def _post(self, url, payload=None):
        """Performs HTTP POST with credentials, returning the body as JSON."""

        response = self.session.post(url, data=payload)
        if response.status_code == 401:
            self._login()
            response = self.session.post(url, data=payload)
        try:
            return response.json()
        except:
            return response.text
    
    def _post_json(self, url, payload=None):
        """Performs HTTP POST with credentials, returning the body as JSON."""

        response = self.session.post(url, json=payload)
        if response.status_code == 401:
            self._login()
            response = self.session.post(url, json=payload)
        try:
            return response.json()
        except:
            return response.text
    
    def _put(self, url, payload=None):
        """Performs HTTP PUT with credentials, returning the body as JSON."""

        response = self.session.put(url, json=payload)
        if response.status_code == 401:
            self._login()
            response = self.session.put(url, json=payload)
        try:
            return response.json()
        except:
            return response.text

    def _get(self, url, payload=None):
        """Performs HTTP GET with credentials, returning the body as JSON."""

        response = self.session.get(url)
        if response.status_code == 401:
            self._login()
            response = self.session.get(url)
        try:
            return response.json()
        except:
            return response.text

    def _patient(self, pid):
        """Patient info by id"""            
                
        return self._get(self.url + "/patient/" + pid)

    def _patient_search(self, **kwargs):
        """lookup patients, if no search terms given returns all patients"""

        # use keyword arguments as search terms like lname fname dob etc.
        searchterms = ""
        if kwargs is not None:
            for key, value in kwargs.items():
                searchterms = searchterms + "&%s=%s" %(key,value)
        else:
            searchterms = ""

        return self._get(self.url + "/patient" + searchterms)

    def _appointment(self):
        """list al appointments"""            
                
        return self._get(self.url + "/appointment")
    
    def _patient_encounter(self, pid):
        """Patient encounters"""            
                
        return self._get(self.url + "/patient/" + pid + "/encounter")

    def _patient_appointment(self, pid):
        """List patient appointments"""            
                
        return self._get(self.url + "/patient/" + pid + "/appointment")

    def _get_patient_document(self, pid):
        """Patient document by pid document id"""            
                
        return self.session.get(self.url + "/patient/" + pid + "/document")

    def _patient_message(self, pid):
        """Get a patient message"""            
                
        return self._get(self.url + "/patient/" + pid + "/message/1")
    
    def _new_patient(self, payload=None):
        """Create new patient"""

        # Check required fields
        try:
            city = payload['city']
            country_code = payload['country_code']
            dob = payload['dob']
            ethnicity = payload['ethnicity']
            fname = payload['fname']
            lname = payload['lname']
            mname = payload['mname']
            phone_contact = payload['phone_contact']
            postal_code = payload['postal_code']
            race = payload['race']
            sex = payload['sex']
            state = payload['state']
            street = payload['street']
            title = payload['title']
        except:
            print("not all fields are filled!")
            return None

        pid = str(int(self._patient_search()[-1]['pid']) + 1)
        exists = self._patient(pid=pid)
        if exists:
            print("The pid I suggested already exists, this is strange check openemr class.")
            return None

        # on success will return: {'pid': '5970'} use pid with newPid = class._new_patient(payload=payload)['pid']
        return self._post_json(self.url + "/patient", payload=payload)
