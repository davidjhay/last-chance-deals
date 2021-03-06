import concurrent.futures
import contextlib
from datetime import datetime
from flask import Flask
from flask import request
from flask import render_template
import urllib.request
import urllib.parse
import json
from Subscription import Subscription

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('LastChanceDeals.html')

@app.route('/', methods=['POST'])
def my_form_post():
    url = request.form['url']
    destination = request.form['destination']
    if request.form['submit'] == 'Subscribe':
        subscribers.append(Subscription(url, destination))
        message = 'Conratulations, the URL ' + url + ' is now subscribed to Last Chance Deals for ' + destination
        return render_template('LastChanceDeals.html', message=message)
    elif request.form['submit'] == 'Test End Point':
        data = open('sample.json', 'r').readline().encode('utf-8')
        testMessage = notify(data, url)
        return render_template('LastChanceDeals.html', message=testMessage)
    elif request.form['submit'] == 'Get Deals':
        filteredDeals = retrieveDeals()
        responses = [ ]
        for subscription in subscribers:
            for Deal in filteredDeals:
                if subscription.destination == Deal.destination:
                    responses.append(notify(Deal.response, subscription.url) + ' for ' + Deal.destination)
        return render_template('LastChanceDeals.html', responses=responses)

@app.route('/demo', methods=['GET', 'POST'])
def demo():
    if request.method == 'POST':
        if request.form['submit'] == 'Get Deals':
            filteredDeals = retrieveDeals()
            responses = [ ]
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                for subscription in subscribers:
                    for Deal in filteredDeals:
                        if subscription.destination == Deal.destination:
                            executor.submit(futureNotify, responses, Deal, subscription)
            return render_template('Demo.html', responses=responses)
    else:
        return render_template('Demo.html')

def futureNotify(responses, Deal, subscription):
    responses.append(notify(Deal.response, subscription.url) + ' for ' + Deal.destination)

def retrieveDeals():
    deals = [ ]
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for destination in uniqueDestinations():
            futures.append(executor.submit(dailyDealCheck, destination))
        for future in futures:
            response = future.result()
            if response[1] != '' and response[1] is not None:
                filteredResponse = filterDate(request.form['date'], response[1])
                deals.append(Deal(response[0], filteredResponse))
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
    url = 'http://phelcodenauts-deals-prototype001.karmalab.net:7400/ean-services/rs/hotel/v3/deals?'
    response = urllib.request.urlopen(url + urllib.parse.urlencode({'destinationString':location}))
    with contextlib.closing(response) as x:
        responseString = x.read().decode('utf-8')
    return (location, responseString)

if __name__ == '__main__':
    subscribers = [ ]
    app.run(debug=True)
