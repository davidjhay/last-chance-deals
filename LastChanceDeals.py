import contextlib
from datetime import datetime
from flask import Flask
from flask import request
from flask import render_template
import urllib.request
import json
import Subscription

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('LastChanceDeals.html')

@app.route('/', methods=['POST'])
def my_form_post():
    url = request.form['url']
    destination = request.form['destination']
    if request.form['submit'] == 'Subscribe':
        subscriber = Subscription(url, destination)
        subscribers.append(subscriber)
        message = 'Conratulations, the URL ' + url + ' is now subscribed to Last Chance Deals for ' + destination
        return render_template('LastChanceDeals.html', message=message)
    elif request.form['submit'] == 'Test':
        data = open('sample.json', 'r').readline().encode('utf-8')
        testMessage = notify(data, url)
        return render_template('LastChanceDeals.html', message=testMessage)
    elif request.form['submit'] == 'Get Deals':
        filteredDeals = retrieveDeals()
        #response = dailyDealCheck(destination)
        #response = filterDate(request.form['date'], response)
        for Subscription in subscribers:
            for Deal in filteredDeals:
                if Subscription.destination == Deal.destination:
                    response = notify(Deal.response, Subscription.url)

        return render_template('LastChanceDeals.html', message='DONE')

def retrieveDeals():
    deals = [ ]
    for destination in uniqueDestinations():
        response = dailyDealCheck(destination)
        response = filterDate(request.form['date'], response)
        deals.append(Deal(destination, response))
    return deals

def uniqueDestinations():
    uniqueDestinationList = set()
    for Subscription in subscribers:
        uniqueDestinationList.add(Subscription.destination)
    return uniqueDestinationList

class Deal:
    def __init__(self, destination, response):
        self.destination = destination
        self.response = response

def notify(data, url):
    req = urllib.request.Request(url, data, {'Content-Type': 'application/json'})
    try:
        urllib.request.urlopen(req)
        notificationMessage = 'Notification successfully sent to ' + url
    except:
        notificationMessage = 'Failed to notify ' + url
    return notificationMessage

def filterDate(dateToBeFiltered, response):
    jsonResponse = json.loads(response)
    filteredJsonResponse = []
    for deal in jsonResponse:
        effectiveEndDate = deal["effectiveEndDate"]
        if isWithin24Hours(dateToBeFiltered, effectiveEndDate):
            filteredJsonResponse.append(deal)
    return bytes(json.dumps(filteredJsonResponse), encoding='utf-8')

def isWithin24Hours(dateToBeFiltered, effectiveEndDate):
    endDate = datetime.strptime(effectiveEndDate, '%Y-%m-%d %H:%M:%S')
    if dateToBeFiltered == '':
        now = datetime.now()
    else:
        now = datetime.strptime(dateToBeFiltered, '%Y-%m-%d %H:%M:%S')
    return (endDate - now).days == 0

def dailyDealCheck(location):
    url = 'http://phelcodenauts-deals-prototype001.karmalab.net:7400/ean-services/rs/hotel/v3/deals?' \
          'destinationString='
    with contextlib.closing(urllib.request.urlopen(url + location)) as x:
        responseString = x.read().decode('utf-8')
    return responseString

if __name__ == '__main__':
    subscribers = [ ]
    #TEMP CODE
    subscribers.append (Subscription('testurl1', 'Chicago'))
    subscribers.append (Subscription('testurl2', 'Denver'))
    subscribers.append (Subscription('testurl2', 'Chicago'))

    app.run(debug=True)
