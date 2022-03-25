from flask import Flask, jsonify, request,abort
import gnupg
APP = Flask(__name__)
gpg = gnupg.GPG('/home/root')
key_data = open('mykeyfile.asc').read()
import_result = gpg.import_keys(key_data)

@APP.route('/decryptMessage', methods=['POST'])
def decrypt_message():
    request_data = request.get_json()
    passphrase = request_data.get('passphrase')
    message = request_data.get('message')
    if not passphrase:
        abort(400)
    if not message:
        abort(400)
    decrypted_message=gpg.decrypt(message,passphrase=passphrase)
    return jsonify({"DecryptedMessage":str(decrypted_message),'status':decrypted_message.status})
      

if __name__ == '__main__':
    APP.run(port=8080,debug=True)