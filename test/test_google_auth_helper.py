
import pytest
from lkmltools.google_auth_helper import GoogleAuthHelper
import os
import json

@pytest.fixture(scope="module")
def get_raw_json():
    raw_json = {
        "type": "service_account",
        "project_id": "someproject",
        "private_key_id": "xxx",
        "private_key": "-----BEGIN PRIVATE KEY-----\nxxx-----END PRIVATE KEY-----\n",
        "client_email": "someuser@appspot.gserviceaccount.com",
        "client_id": "1234567890",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/someuser%40appspot.gserviceaccount.com"
    }
    return raw_json

@pytest.fixture(scope="module")
def get_encoded_json():
    # this is the encoded version of the raw_json above, so doesn't contain any proper secrets. 
    # The unit tests below confirm that decoding this byte string below matches the JSON above
    return b'eyd0eXBlJzogJ3NlcnZpY2VfYWNjb3VudCcsICdwcm9qZWN0X2lkJzogJ3NvbWVwcm9qZWN0JywgJ3ByaXZhdGVfa2V5X2lkJzogJ3h4eCcsICdwcml2YXRlX2tleSc6ICctLS0tLUJFR0lOIFBSSVZBVEUgS0VZLS0tLS1cbnh4eC0tLS0tRU5EIFBSSVZBVEUgS0VZLS0tLS1cbicsICdjbGllbnRfZW1haWwnOiAnc29tZXVzZXJAYXBwc3BvdC5nc2VydmljZWFjY291bnQuY29tJywgJ2NsaWVudF9pZCc6ICcxMjM0NTY3ODkwJywgJ2F1dGhfdXJpJzogJ2h0dHBzOi8vYWNjb3VudHMuZ29vZ2xlLmNvbS9vL29hdXRoMi9hdXRoJywgJ3Rva2VuX3VyaSc6ICdodHRwczovL29hdXRoMi5nb29nbGVhcGlzLmNvbS90b2tlbicsICdhdXRoX3Byb3ZpZGVyX3g1MDlfY2VydF91cmwnOiAnaHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vb2F1dGgyL3YxL2NlcnRzJywgJ2NsaWVudF94NTA5X2NlcnRfdXJsJzogJ2h0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL3JvYm90L3YxL21ldGFkYXRhL3g1MDkvc29tZXVzZXIlNDBhcHBzcG90LmdzZXJ2aWNlYWNjb3VudC5jb20nfQ=='

def test_encode_service_account():
    helper = GoogleAuthHelper()
    encoded_json = helper.encode_service_account(get_raw_json())
    assert encoded_json == get_encoded_json()
    
def test_decode_service_account():
    helper = GoogleAuthHelper()
    decoded_json = helper.decode_service_account(get_encoded_json())
    assert decoded_json == get_raw_json()

def test_write_decoded_sa_json_to_file():
    helper = GoogleAuthHelper()
    filename = "tmp_test_decoded.json"

    if os.path.exists(filename):
        os.remove(filename)

    helper.write_decoded_sa_json_to_file(get_encoded_json(), filename=filename)

    assert os.path.exists(filename)

    with open(filename, 'r') as f:
        data = json.load(f)

    assert data == get_raw_json()

    if os.path.exists(filename):
        os.remove(filename)
