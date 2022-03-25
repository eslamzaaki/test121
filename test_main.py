import json
import pytest
import main

passphrase="topsecret"
encrypted_message="-----BEGIN PGP MESSAGE-----\r\n\r\nhQEMA6S4AvrGbhwpAQf/ckbgtfJfXKXfRbl+Bs+7va7W7mN/Dz9YfAIRc2Kx7Btp\r\npsHJxPrvVWsiFQE/TgqDQ66mNuAeRwxVqVdc1Pps0HWMnKvhh+ezqSHrnl9LR8ww\r\n1wxNqbeOlLKjkMZ8CT1h3RzNBzSI12itYeCVEi1Ak83UvXLtE9fO7mDo83gMyyFq\r\n1dKO7aSimu6R2tmP9deseAVqTxtUuYWi1wAU46bYI4ROL1DACW44qES/plpUDeKq\r\nj9dQhZ41tc51ifupWQ6qyvLxYqkg5IhjbWQgNZJHVU3d8VjiM3FhZ0zzl0uTbmcO\r\nUOJwf7+MNbsUIdxIQcnp4VI8fbBRxKWN2PVTOKdjbNRKAQkCELt5MM/jRFt9Nm9p\r\nSUM0FBtcSs416P/Az4/KzDAApiJmY3JsLWOpPkfo7HfVuK3tJFrazRhvpeQOOE23\r\nSOtJ7Z5QvkAg6LE=\r\n=rVbb\r\n-----END PGP MESSAGE-----\r\n"
decrypted_message='eslam'

@pytest.fixture
def client():
    main.APP.config['TESTING'] = True
    client = main.APP.test_client()
    yield client

#test right request with message and passphrase
def test_decryption_success(client):
    body = {'passphrase':passphrase,
            'message': encrypted_message}
    response = client.post('/decryptMessage', data=json.dumps(body),content_type='application/json')

    assert response.status_code == 200
    print(response.json['status'])
    decrypted_m = response.json['DecryptedMessage']
    assert decrypted_m==decrypted_message


#test bad request one parameter not found
def test_decryption_bad_request(client):
    body = {'message':encrypted_message}
    response = client.post('/decryptMessage', 
                           data=json.dumps(body),
                           content_type='application/json')
    assert response.status_code == 400


#test can't decrypt message case
def test_decryption_dummy_parameters(client):
    body = {'passphrase':passphrase,"message":"wrong message to fail"}
    response = client.post('/decryptMessage', 
                           data=json.dumps(body),
                           content_type='application/json')

    assert response.status_code == 200
    message = response.json['message']
    assert message=='could not decrypt your message'
#test method not allowed
def test_method_not_allowed(client):
    response = client.get('/decryptMessage')
    assert response.status_code == 405

