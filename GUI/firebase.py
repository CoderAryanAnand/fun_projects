import pyrebase

# ****** PYREBASE ******
config = {
    "apiKey": "AIzaSyDUthwERPqVpLtR4gQ2Im8PjynqKNnbrVc",
    "authDomain": "password-manager-1c46f.firebaseapp.com",
    "databaseURL": "https://password-manager-1c46f.firebaseio.com",
    "projectId": "python-password-manager-1c46f",
    "storageBucket": "python-password-manager-1c46f.appspot.com",
    "messagingSenderId": "114287286592",
    "appId": "1:114287286592:web:68ce5e79b12aca3f0b42a5",
    "measurementId": "G-CEERN2EP83",
    "serviceAccount": "secretKey.json"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

path_on_cloud = 'passwords/emails.txt'
local_path = 'emails.txt'

storage.child(path_on_cloud).download("emails.txt")
