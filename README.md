# Selenium-Phishing-Detector

![alt Selenium](./res/selenium.png| width=100)
![alt InfluxDB](./res/influx.png | width=100)
![alt Graphana](./res/graphana.png | width=100)
![alt MongoDB](./res/mongodb.png | width=100)


## Project overview
- A New Heuristic Based Phishing Detection Approach Utilizing Selenium Web-driver
- [Publication at University of Tartu](http://comserv.cs.ut.ee/ati_thesis/datasheet.php?id=58598&year=2017)

### Setup

Use `Python 2.7` for back-end

All the requirements have been described in `requirements.txt`. Make sure you add all your back-end requirements there as well!
Initial requirements include:
- [Selenium](https://selenium-python.readthedocs.io/) Selenium web driver
- [Alexa_scrapper](https://github.com/vivekpatani/alexa-scraper) Scrapper for Alexa to get new Legit webpages
- [Google_scrapper](https://www.django-rest-framework.org/) Scrapper for google
- [MongoDB](https://www.mongodb.com/) Main database
- [InfluxDB](https://www.influxdata.com/time-series-platform/influxdb/) Logging Database
- [Graphana](http://docs.grafana.org/) Graph server for Influx db to show log data
- [Dnspython](http://www.dnspython.org/examples.html) Dns package for python
- [Whois](https://pypi.org/project/whois/) whois python package

 Scrapping login pages from google

    GoogleScraper -m http --keyword "login" -n 10 -p 1000 --num-workers 10 --search-engines "google" --output-filename legit.json

scrapping Phishing pages from phishtank

    cd scraper
    ./scrapper.sh

### Running the application

    python phish_detect.py
    
Run Graphana and check results 
    
    http://localhost:3306 

 


