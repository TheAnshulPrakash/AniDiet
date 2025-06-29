import firebase_admin
import flet as ft
from firebase_admin import credentials, db
import requests   
    
url = "https://gist.githubusercontent.com/TheAnshulPrakash/e3bf6d97c8c652fa4878e3011e9fc997/raw/f32385e12d4611ba8d789e063e70816b69301ddd/json"


response = requests.get(url)
key_json = response.json()
cred = credentials.Certificate(key_json)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://anvishit-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

users_ref = db.reference('Anidiet')

def from_firebase(handle):
    ref=db.reference(f'Anidiet/{handle}')
    print("Printing data", handle)
    user_data=ref.get()
    
    return user_data
    
def get_streak(handle):
    ref=db.reference(f'Anidiet/{handle}')
    print("Printing data", handle)
    return ref.get().get("streak")

def to_firebase(user_data):
    
    
    handle = user_data['handle']
    existing_user = users_ref.child(handle).get()

    if existing_user:
        print(f"User '{handle}' exists. Updating...")
        users_ref.child(handle).update(user_data)
    else:
        print(f"User '{handle}' not found. Creating new entry...")
        users_ref.child(handle).set(user_data)

    print("Operation complete.")
    print("Uploaded to firebase")

