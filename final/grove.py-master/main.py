import requests
import datetime
import time
import firebase_admin
from firebase_admin import credentials, db
from grove.display.jhd1802 import JHD1802

lcd = JHD1802()


cred = credentials.Certificate('/home/kgx/Desktop/final/grove.py-master/cred.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://book-kiosk-93f35-default-rtdb.europe-west1.firebasedatabase.app'
})

API_KEY = 'AIzaSyARlrYxIKVkTUQLXA796cQjxWZXcx-BHFI'


#def set_RGB(r,g,b):9781612680194

 #   lcd.setRGB(r,g,b)


def display_message1(line1=''):
    lcd.home()   
    lcd.write(line1)      

def display_message2(line2=''):
    lcd.setCursor(1,0)
    lcd.write(line2)  


def getbook(isbn):
    url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key={API_KEY}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
       
        if 'items' in data:
            book_title = data['items'][0]['volumeInfo']['title']
            return book_title
 
        else:

            return "No book found"
    else:
        return "Failed to retrieve data."

def write_book():
    counter = 1
    while True:
        display_message1("Drop Your Book!")
        #set_RGB(255,0,0)

        display_message2("Scan Your Book:")
        #set_RGB(0,0,0)
        
        isbn_book1 = input()

        time.sleep(2)

        lcd.clear()
        

        book1 = getbook(isbn_book1)

        

        exception_val = ["No book found"] 

        if book1 in exception_val:
            display_message1("No book found")
            time.sleep(2)
            lcd.home()
            continue
        
        
        display_message1("Book Title")
        display_message2(f"{book1}")
        #set_RGB(255,0,0)

        time.sleep(2)

        lcd.clear()

        display_message1("Scan New Book!!")
        #display_message2()
        #set_RGB(255,0,0)
        isbn_book2 = input()
    
        time.sleep(2)

        lcd.clear()
        

        val_1 = datetime.datetime.now().isoformat()
        book2 = getbook(isbn_book2)
        
        
        display_message1(f"Book Title")
        display_message2(f"{book2}")
        #set_RGB(255,0,0)

        time.sleep(2)

        lcd.clear()
        
        data = {
            'ID': f'{counter}',
            'book_1': f'{book1}',
            'book_2': f'{book2}',
            'date_time': f'{val_1[:19]}'
        }
        

        ref = db.reference('books')
        ref.push(data)
        
        counter += 1

write_book()