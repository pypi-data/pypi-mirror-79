from micro_center_price_monitor.scraper import MicroCenterScraper
from micro_center_price_monitor.mail import Email
import datetime, time

class PriceChecker:

    """
    
    PriceChecker:

    Manages execution flow for:
        -> Retrieving search results list
        -> Selected wanted product
        -> Monitoring price
        -> Sending product email

    """
    def search(self):

        try:
            # Prompt to enter a product name
            search_for = input('Enter a product:\n')
            # Init scraper obj, passing user input for search term
            scraper = MicroCenterScraper(search_term=search_for)
            # GET request to retrieve first page results
            scraper.search_for_products()
            # Print search results
            scraper.get_products()
            # Prompt to search for one of list items
            product_selection = int(input('Select a product:\n'))
            # Selects product from list
            scraper.select_product(product_selection)
            # Prompt to enter expected price at discount
            expected_price = float(input('Enter your expected price\n'))

            while True:
                # update pricing info
                scraper.check_product_price()
                # Get float value of price attribute
                price = float(str(scraper.key_product.price).replace(',',''))
                # currency symbol for output (e.g., "$"" for USD)
                currency_symbol = scraper.key_product.currency
                # Print current time and price
                print('Price at: %s -> %s%s' % (datetime.datetime.now(), 
                                                currency_symbol, 
                                                str(price)))

                # Email if the price is beneath expected threshold. Otherwise, continue to loop.
                if price <= expected_price:
                    print('Price at or below %s%.2f at %s%.2f' % (currency_symbol, expected_price, currency_symbol, price))
                    print('Sending email now...')
                    email = Email(scraper.key_product.name, 
                                  currency_symbol + scraper.key_product.price, 
                                  scraper.data.product_url)
                    email.send_email()
                    break
                # sleep for n seconds
                time.sleep(scraper.data.REFRESH_SECS) 

        except ValueError:
            print('Invalid product selection value provided. Please try again later.')
        except IndexError:
            print('Unable to find any search results. Please try again.')
        except Exception as e:
            print('Unexpected error has occured. %s' % e)



