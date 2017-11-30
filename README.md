# Warehouse_Fulfillment_Center
SaaS Web Service: Warehouse Fulfillment Center

[Live Demo available here](https://stack-warehouse.herokuapp.com/)

----
## Descriptions
* Offers a modern, HTTP-based web service so that sellers can build their own internal tools to keep track of their warehouse activities.
* A website that enables a seller's technical employees to sign up for a developer account, so that they can gain access to the web service.
* API endpoints that enable developers to use the web service to store items, check status of items, and be notified of status changes of items  

## Requirements
- [x] \(Required\) [5 points] Landing Page, Sign Up, and Documentation  
- [x] \(Required) [5 points] Inventory Status  
- [x] \(Required) [5 points] Inventory Replenishment  
- [x] \(Optional) [10 points] Place Order for Shipment  
- [x] \(Optional) [10 points] JavaScript Drop-In  
- [x] \(Optional) [10 points] Push Notifications  
- [x] Submit Your Project with live service  

## Usage
* Make sure you have .env file in your directory with the following crednetials:  
  1. SECRET_KEY
  2. DEBUG
  3. ALLOWED_HOSTS
  4. SOCIAL_AUTH_GITHUB_KEY
  5. SOCIAL_AUTH_GITHUB_SECRET
  6. SOCIAL_AUTH_TWITTER_KEY
  7. SOCIAL_AUTH_TWITTER_SECRET

* Make migrations
  * python manage.py makemigrations
  * python manage.py migrate

* Create a super user
  * python manage.py createsuperuser

* Run your app on localhost or deploy your app online
