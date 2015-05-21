from flask import Flask
from flask import request
from flask import render_template
import urllib.request
import json
import contextlib

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
        subscriberCount = subscribers.count()
        message = 'Conratulations, the URL ' + url + ' is now subscribed to Last Chance Deals for ' + destination
        return render_template('LastChanceDeals.html', message=message, subscriberCount=subscriberCount)
    elif request.form['submit'] == 'Test':
        data = open('sample.json', 'r').readline().encode('utf-8')
        req = urllib.request.Request(url, data, {'Content-Type': 'application/json'})
        try:
            urllib.request.urlopen(req)
            testMessage = 'Test json successfully sent to ' + url
        except:
            testMessage = 'Failed to send test response to ' + url
        return render_template('LastChanceDeals.html', message=testMessage)
    elif request.form['submit'] == 'Get Deals':
        deals = retrieveDeals()
        response = dailyDealCheck(destination)
        filterDate('5/21/2015', response)
        return render_template('LastChanceDeals.html', message=response)

def retrieveDeals():
    deals = [ ]
    for destination in uniqueDestinations():
        response = dailyDealCheck(destination)
        deals.append(Deal(destination, response))
    return deals

def uniqueDestinations():
    uniqueDestinationList = set()
    for Subscription in subscribers:
        uniqueDestinationList.add(Subscription.destination)
    return uniqueDestinationList

def filterDate(dateToBeFiltered, response):
    jsonResponse = json.loads(response)

def dailyDealCheck(location):
    url = 'http://phelcodenauts-deals-prototype001.karmalab.net:7400/ean-services/rs/hotel/v3/deals?destinationString='
    with contextlib.closing(urllib.request.urlopen(url + location)) as x:
        responseString = x.read().decode('utf-8')
    return responseString

class Deal:
    def __init__(self, destination, response):
        self.destination = destination
        self.response = response

class Subscription:
    subscriberCount = 0

    def __init__(self, url, destination):
        self.url = url
        self.destination = destination
        Subscription.subscriberCount += 1

    def displayCount(self):
        return self.subscriberCount

    def displaySubscriber(self):
        print("nothing")



if __name__ == '__main__':
    subscribers = [ ]
    #TEMP CODE
    subscribers.append (Subscription('testurl1', 'Chicago'))
    subscribers.append (Subscription('testurl2', 'Denver'))
    subscribers.append (Subscription('testurl2', 'Chicago'))

    app.run(debug=True)
