# Pastebin Scraper

The scraper here is based on the one from [six519](https://github.com/six519/PastebinPython). Thank you very much for giving us this present :-)

## Installation

Simply clone it:

```
cd /your/desired/directory
clone https://github.com/six519/PastebinPython.git
pip install -r requirements.txt
```

## Usage

This fork of the PastebinPython project downloads all pastebin entries ... or well at least it starts downloading as much as it can.

The results will be saved within a MongoDB collection. Another script will be triggered to identify keywords, which have to be provided in front.

The second step results in new collections where each keyword gets one new collection and all found pastebin entries will be copied there.

The third step might be the accumulator. It identifies specific words (similiar to step 2) but also specials like eMail addresses, Bitcoin addresses, URLs, IP Adresses etc. 

### 1. pastebin_scrape.py

For this one to work good you need an API key. I bought a lifetime access to the pastebin API a while ago for 29,99 USD. It doesn't make you poor.

You will also need to update your Scraping IP, in order to make it work: [Change Scraping IP](https://pastebin.com/doc_scraping_api)

        python pastebin_scrape.py -v 1 -db 1 -api <YOUR_PASTE_BIN_API_KEY>

### 2. pastebin_analyze.py

### 3. pastebin_accumulate.py

### Access Data via Flask API

Finally you can either write yourself a clean data retriever or you can use this Flask API implementation here:

```
# start it in debug and verbose mode first!
python pastebin_api.py -d -v
```

Well there is only one API method. Grab yourself a browser or use curl:

```
http://localhost:5000/api/getpastebins/<keyword>
```

The result should be a nice JSON document collection. Maybe too large to handle for a browser. Anyway this is just intended for demonstration reasons. 

If you want to use that data somehow, you might find the JSON format handy and start to parse it for your own purpose.