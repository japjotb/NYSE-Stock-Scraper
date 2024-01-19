import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time

#connect to MONGODB database
client = MongoClient('mongodb://localhost:27017/')
db = client['yahoo-db']
collection = db['stocks']

#display the data from the collection
def display_data():
    z = collection.find()
    for document in z:
        print(document)

#delete the data from the collection
def delete():
    collection.drop()

#function to convert the variable num to a float
def isfloat(num):
    try:
        cast=float(num)
        return True
    except Exception as e:
        return False

#retrieve stock data from Yahoo Finance and store it in the database
def retrieve_stocks():
    delete()

  #url used to scrape data
    url = 'https://finance.yahoo.com/most-active'

    try:
      #send a get request to yahoo finance
        response = requests.get(url)
        print("Status Code:", response.status_code)
        page = BeautifulSoup(response.text, "html.parser")
        rows = page.find_all("tr")
      #store all the data
        fields = {"index": [], "Symbol": [], "Name": [], "Price (Intraday)": [], "Change": [], "Volume": []}
        index = 1

      #loop through each row in the table and extract stock data
        for row in rows:
            fields["index"].append(index)
            index = index + 1

            for column in row:
                field = column.get("aria-label")
                
                if field in fields.keys():
                    if field != "Volume":
                        fields[field].append(float(column.text) 
                        if isfloat(column.text) 

                        else 
                          column.text)
                    else:
                        fields[field].append(float(column.text[0:-1]))
                        

      #insert the stock data into the database
        for i in range(len(fields["Symbol"])):
            symbol = fields["Symbol"][i]
            if collection.count_documents({'Symbol': symbol}) == 0:
                getindex = fields["index"][i]
                name = fields["Name"][i]
                price = fields["Price (Intraday)"][i]
                change = fields["Change"][i]
                volume = fields["Volume"][i]
                collection.insert_one({'_id': getindex, 'Symbol': symbol, 'Name': name, 'Price': price, 'Change': change, 'Volume': volume})

    except Exception as e:
        print("Connection error:", str(e))

#loop that runs 5 times, retrieves data, displays it and sleeps for 3 minutes
run_count = 0
while run_count < 5:
  retrieve_stocks()
  display_data()
  time.sleep(180)
  run_count = run_count + 1