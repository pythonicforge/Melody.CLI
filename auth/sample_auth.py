import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyCPv2e0ygTq7URXgkOaob3bG8qhHv4XfB4",
  "authDomain": "melodicli.firebaseapp.com",
  "projectId": "melodicli",
  "storageBucket": "melodicli.appspot.com",
  "messagingSenderId": "774638509277",
  "appId": "1:774638509277:web:a71e51101d7f9c7dd30f34",
  "measurementId": "G-S2C3KB5P8M",
  "databaseURL": "https://melodicli-default-rtdb.firebaseio.com/"
};

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

def signUp(email, password):
    try:
        auth.create_user_with_email_and_password(email, password)
        print("User created")
        return True
    except:
        print("User already exists")
        return False
    
signUp(input("Enter your email: "), input("Enter your password: "))