import requests
from bs4 import BeautifulSoup
from micro_center_price_monitor.data import Browser, WebPage, Product
from lxml import html, etree
from micro_center_price_monitor.custom_exceptions import *

"""

Micro Center Price Scraper

Able to search for and print a list of first page search results (if there are any matches)
Once user chooses from list, search for price after n seconds to see if it dips below a certain price range.
If it goes below, push notification to email


"""

class MicroCenterScraper:   

    def __init__(self, search_term: str):
        self.data = WebPage(search_term)
        self.key_product = Product()
    
    # Retrieves parsed html content from new request
    def get_page_content(self, url):
        self.page = requests.get(url, headers=Browser.HEADER)
        self.soup = BeautifulSoup(self.page.content, 'html.parser')
        self.tree = html.fromstring(self.page.content)

    # GET request for search results      
    def search_for_products(self):
        self.get_page_content(self.data.search_url)
        self.products = self.tree.xpath(_path=self.data.PRODUCT_LINKS)
        self.products_currency = self.tree.xpath(_path=self.data.PRODUCTS_CURRENCY_SYMBOL)[0].text

    # GET request for individual product chosen.
    def check_product_price(self):
        self.get_page_content(self.data.product_url)            
        self.key_product.price = self.tree.xpath(_path=self.data.SELECTED_PRODUCT_PRICE)[0].get(self.data.CONTENT_ATTR)
        self.key_product.name = self.tree.xpath(_path=self.data.SELECTED_PRODUCT_NAME)[0].get(self.data.PRODUCT_NAME)
        self.key_product.currency = self.tree.xpath(_path=self.data.SELECTED_PRODUCT_CURRENCY_SYMBOL)[0].text
        
        
    @property
    def page(self):
        return self.__page
    
    @page.setter
    def page(self, var):
        if var.status_code == 200:
            self.__page = var
        else:
            raise StatusCodeError('Page failed to load.')
    
    @property
    def soup(self):
        return self.__soup
    
    @soup.setter
    def soup(self, var):
        self.__soup = var

    @property
    def tree(self):
        return self.__tree
    
    @tree.setter
    def tree(self, val):
        self.__tree = val

    # Product list getter/setter methods
    @property
    def products(self):
        return self.__products
    
    @products.setter
    def products(self, val):
        self.__products = val
    
    # Prints the name and price of each product from search results on first page
    def get_products(self):   
        print("Select one of the products below by providing it's respective index value:")     
        for (i, product) in enumerate(self.products, 0):
            print("%s: %s - %s%s" % (i, product.get(self.data.PRODUCT_NAME), self.products_currency, str(product.get(self.data.PRODUCT_PRICE))))

    # Sets the product url by index chosen
    def select_product(self, index: int):
        try:
            if self.products is not None and type(self.products) == list:                
                # set selected product to url
                self.data.product_url = self.products[index].get(self.data.PRODUCT_HYPERLINK_ATTR)
            else:
                raise ProductsNotFoundError
        except IndexError:
            print('Index chosen is out of range.')
        except ProductsNotFoundError:
            print('Unable to find products.')
        except TypeError:
            print('Invalid value provided.')
    




    







