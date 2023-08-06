import setuptools 
setuptools.setup (
    name = "webscraperz",
    version="0.1",
    author="Pyae Phyo Hein",
    author_email="pyaephyohein.info.3326@gmail.com",
    descripton="Web Scraperz",
    packages=["web_scraperz"],
    entry_points = {
        'console_scripts' : ['webscraperz=web_scraperz.scraper:scraper']
    }

    )