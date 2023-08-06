from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    url='https://github.com/Nintendude64/micro-center-price-monitor',
    author="Martin Daniels",
    author_email="martindaniels02@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
    name='micro_center_price_monitor',
    version='0.0.6',
    description='Price monitor tool for Micro Center',
    py_modules=["scraper","price_checker","mail","data","custom_exceptions","__init__"],
    packages=["micro_center_price_monitor"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    extras_require= {
        "dev": [
            "beautifulsoup4>==4.7.1",
            "bs4==0.0.1",
            "lxml==4.3.4",
            "requests==2.22.0",
        ]
    },
    entry_points={
        "console_scripts": [            
            "micro_center_price_monitor=micro_center_price_monitor.__main__:main"
        ]
    }
        
    
)