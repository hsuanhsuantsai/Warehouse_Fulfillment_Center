# Warehouse_Fulfillment_Center
Web Service: Warehouse Fulfillment Center

Live Demo available [Here](https://stack-warehouse.herokuapp.com/)

----
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
