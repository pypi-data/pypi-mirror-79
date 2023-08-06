# Micro Center Scraper Using Beautiful Soup

## Table of Contents
* [Project Description](#project-description)
* [How to Use](#how-to-use)
* [Packages Used](#packages-used)
* [Installation](#installation)
* [Other Requirements](#other-requirements)
* [To Do List](#to-do-list)

## Project Description
This is a simple Python web scraper to monitor prices on Micro Center's online store for a product you may be interested in.

## How to Use:
Upon running the program: there will be a prompt to provide a product to search:

* Enter the name of the product and hit Return.
* There will be a list of results with corresponding index values. Provide the index value for the product you want to monitor, and hit Return.
* Enter the price threshold you wish to receive a notification for and hit Return. The program will loop continuously until your product meets or goes below expected price and an email notification will be sent.

## Packages Used
* bs4: version 0.0.1
* beautifulsoup4: version 4.7.1
* requests: version 2.22.0
* lxml: version 4.3.4

## Installation
Install micro-center-price-monitor with pip:

```
pip install micro-center-price-monitor
```

## Other Requirements
* You will need a Gmail Account set up with "Allowing less secure apps to access your account" enabled. This is not recommended for a user's main Gmail account. Using a burner gmail account is recommended in this instance.

* Include login info in System User Variables:
    - "EMAIL_USER" -> set to gmail address
    - "EMAIL_PASS" -> set to gmail password

# TO-DO LIST:
* Inclusion of pages 2..n for search results longer than 1 page.