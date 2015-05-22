# last-chance-deals
A service to push notifications to affiliates about hotel deals ending in the next 24 hours.

### Features:
* subscription page
 * includes an option to push a test notification
* demostration page for setting dates for testing

### How it Works:
* An affiliate tests their endpoint on the subscription page.
* The affiliate then subscribes by specifying the location that they want to recieve notifications for and their endpoint. An affiliate may submit the same endpoint for multiple locations.
* Go to the demostration page and specify a date to simulate an update of data in the Deals Service. Any deals for an affiliate's subscription will be pushed to their endpoint via a HTTP POST request.
