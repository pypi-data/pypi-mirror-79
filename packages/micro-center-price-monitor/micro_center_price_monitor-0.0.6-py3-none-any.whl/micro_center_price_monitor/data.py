class Browser:
    # User Agenct header for requests    
    HEADER = {'User-agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1; Microsoft; RM-1152) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Mobile Safari/537.36 Edge/15.15254'}
    
# Page content info for Micro Center webpage.
class WebPage:
    # Seconds to wait before making another request
    REFRESH_SECS = 3600
    # Seperator for keywords in URL address
    SEARCH_SEPARATOR = "+"

    # Product hyperlink elements xpath : these will contain the 
    # attributes we need for name/price, as well as product links.
    PRODUCT_LINKS = "//a[contains(@class,'ProductLink')]"
    # Currency symbol for product list
    PRODUCTS_CURRENCY_SYMBOL = "//span[@itemprop='price']/span[@class='upper']"
    # Final price xpath
    SELECTED_PRODUCT_PRICE = "//span[@id='pricing']"
    # Product Name xpath
    SELECTED_PRODUCT_NAME = "//span[contains(@class, 'ProductLink')]"
    # Currency symbol xpath for selected product
    SELECTED_PRODUCT_CURRENCY_SYMBOL = "//span[@id='pricing']/span[@class='upper']"
    # Attribute for product name
    PRODUCT_NAME = 'data-name'
    # Attribute for product price
    PRODUCT_PRICE = 'data-price'
    # Attribute for product hyperlink
    PRODUCT_HYPERLINK_ATTR = 'href'
    # Content attribute for individual product price
    CONTENT_ATTR = 'content'
    # Base URL for microcenter
    BASE_URL = 'https://www.microcenter.com'

    def __init__(self, search_str: str):
        # url for get request
        self.search_url = search_str
        # url for product we want to track
        self.product_url = ''
    
    """

    Getter/setter methods for:
    search_url: stores the url address for product searches
    product_url: url address for selected product.

    """

    @property
    def search_url(self):
        return self.__search_url
    
    @search_url.setter
    def search_url(self, val):
        self.__search_url = f"https://www.microcenter.com/search/search_results.aspx?N=&cat=&Ntt={val.replace(' ', self.SEARCH_SEPARATOR)}&searchButton=search"                       

    @property
    def product_url(self):
        return self.__product_url
        
    @product_url.setter
    def product_url(self, val):
        self.__product_url = self.BASE_URL + val


# Product class which manages name, price, and currency
class Product:

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, val):
        self.__price = val
    
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, val):
        self.__name = val

    @property
    def currency(self):
        return self.__currency

    @currency.setter
    def currency(self, val):
        self.__currency = val
    
