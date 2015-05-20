from flask import Flask
from flask import request
from flask import render_template

import time

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
        message='just testing url ' + url
        return render_template('LastChanceDeals.html', message=message)

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

def dailyDealCheck():
    print( time.ctime())

if __name__ == '__main__':
    app.run(debug=True)
