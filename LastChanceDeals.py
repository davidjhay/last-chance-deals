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
        req = urllib.request.Request(url, data, {'Content-Type': 'application/json'})
        try:
            urllib.request.urlopen(req)
            testMessage = 'Test json successfully sent to ' + url
        except:
            testMessage = 'Failed to send test response to ' + url
        return render_template('LastChanceDeals.html', message=testMessage)
    elif request.form['submit'] == 'Get Deals':
        response = dailyDealCheck(destination)
        filterDate('5/21/2015', response)
        return render_template('LastChanceDeals.html', message=response)

def filterDate(dateToBeFiltered, response):
    jsonResponse = json.loads(response)
    print(jsonResponse["effectiveEndDate"])


def dailyDealCheck(location):
    url = 'http://phelcodenauts-deals-prototype001.karmalab.net:7400/ean-services/rs/hotel/v3/deals?destinationString='
    req = urllib.request.Request(url + location)
    response = urllib.request.urlopen(req)
    return response.read().decode('utf-8')

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
