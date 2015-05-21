import contextlib
from datetime import datetime
from flask import Flask
from flask import request
from flask import render_template
import urllib.request
import json

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
        subscriberCount = subscriber.displayCount()
        message = 'Conratulations, the URL ' + url + ' is now subscribed to Last Chance Deals for ' + destination
        return render_template('LastChanceDeals.html', message=message, subscriberCount=subscriberCount)
    elif request.form['submit'] == 'Test':
        data = open('sample.json', 'r').readline().encode('utf-8')
        testMessage = notify(data, url)
        return render_template('LastChanceDeals.html', message=testMessage)
    elif request.form['submit'] == 'Get Deals':
        response = dailyDealCheck(destination)
        response = filterDate(request.form['date'], response)
        response = notify(response, url)
        return render_template('LastChanceDeals.html', message=response)


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
          'destinationString=Seattle,+WA,+US'
    with contextlib.closing(urllib.request.urlopen(url + location)) as x:
        responseString = x.read().decode('utf-8')
    return responseString

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
    app.run(debug=True)
