import urllib
import urllib2
import unittest
import json
import mimetools
import collections

baseurl = 'http://localhost:8080' 
import os
if os.getenv("BASEURL") is not None:
    baseurl = os.getenv("BASEURL")

# beautiful, but no longer used. Yet, worth keeping ;)
# from http://stackoverflow.com/a/1254499/204634
def convert(data):
    if isinstance(data, unicode):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data

# awesome stuff from http://stackoverflow.com/a/2257449/204634
import random
import string
def genRandomString(length=12, what=None):
    if what is None:
        what = string.ascii_uppercase + string.digits + string.ascii_lowercase
    return ''.join(random.choice(what) for x in range(length))

# thanks to: http://abhinandh.com/12/20/2010/making-http-delete-with-urllib2.html
class RequestWithMethod(urllib2.Request):
    """Workaround for using DELETE with urllib2"""
    def __init__(self, url, method, data=None, headers={},\
        origin_req_host=None, unverifiable=False):
        self._method = method
        urllib2.Request.__init__(self, url, data, headers,\
                 origin_req_host, unverifiable)
    def get_method(self):
        if self._method:
            return self._method
        else:
            return urllib2.Request.get_method(self) 

class testFiresell(unittest.TestCase):
    createdAuctions = list()

    #def test_05simpleGet(self):
    #    req = urllib2.Request(baseurl)
    #    f = urllib2.urlopen(req) # GET /
    #    status = f.getcode()
    #    f.close()
    #    assert (status == 200)

    def test_10createAuction(self):
        auction = {'desc': 'test desc'}
        data = json.dumps(auction)
        req = urllib2.Request(baseurl + '/auction', 
                data, 
                {'Content-Type': 'application/json'})
        f = urllib2.urlopen(req)
        # status
        status = f.getcode()
        # headers
        meta = f.info()
        # data
        response = f.read()
        f.close()

        assert (status == 201) # resource created
        # find the new location and save it
        for header in meta.headers:
            if 'Location: ' in header:
                # get whatever it's after 'Location: '
                # returns a list, so get the second item
                url = header.split('Location: ', 1)[1]
                url = url.rstrip('\r\n')
                auction['admin_url'] = url
        # save
        self.createdAuctions.append(auction)

    # ugly; do properly, merge with above
    def test_15createAuctionNonJson(self):
        auction = {'desc': 'test desc non-json'}
        data = urllib.urlencode(auction)
        req = urllib2.Request(baseurl + '/auction', data, 
                {'Content-Type': 'application/x-www-form-urlencoded'})
        f = urllib2.urlopen(req)
        # status
        status = f.getcode()
        # headers
        meta = f.info()
        # data
        response = f.read()
        f.close()

        assert (status == 201) # resource created
        # find the new location and save it
        for header in meta.headers:
            if 'Location: ' in header:
                # get whatever it's after 'Location: '
                # returns a list, so get the second item
                url = header.split('Location: ', 1)[1]
                url = url.rstrip('\r\n')
                auction['admin_url'] = url
        # save
        self.createdAuctions.append(auction)

        
    # testing the Location result
    def test_20getAuctionAdminInfo(self):
        for auction in self.createdAuctions:
            # GET auction
            req = urllib2.Request(baseurl + auction['admin_url'])
            f = urllib2.urlopen(req)
            # status
            status = f.getcode()
            # headers
            meta = f.info()
            # data
            response = f.read()
            f.close()
            assert (status == 200) # hit
            desc = json.loads(response)
            assert (desc['desc'] == auction['desc'])
            auction['public_urls'] = desc['public_urls']

    def test_30getAuctionInfo(self):
        for auction in self.createdAuctions:
            for public_url in auction['public_urls']:
                # GET auction
                req = urllib2.Request(baseurl + '/auction/' + public_url)
                f = urllib2.urlopen(req)
                # status
                status = f.getcode()
                # headers
                meta = f.info()
                # data
                response = f.read()
                f.close()
                assert (status == 200) # hit
                data = json.loads(response)
                assert (data['desc'] == auction['desc'])

    # make bid
    def test_40bid(self, 
            name='bidder name 1', amount=42, contact='me@aol.com'):
        for auction in self.createdAuctions:
            if 'bids' not in auction:
                auction['bids'] = list()
            for public_url in auction['public_urls']:
                bid = {'bidder': name,
                        'amount': amount,
                        'contact': contact,
                        }
                        #'url': public_url}
                data = json.dumps(bid)
                req = RequestWithMethod(baseurl + '/auction/' + public_url,
                        'PUT',
                        data, 
                        {'Content-Type': 'application/json'})
                f = urllib2.urlopen(req)
                # status
                status = f.getcode()
                # headers
                meta = f.info()
                # data
                response = f.read()
                f.close()
                assert (status == 201) # resource created
                auction['bids'].append(bid)

    # a trick to make multiple bids
    def test_50multipleBids(self):
        # make a few bids
        for i in range(random.randrange(1, 3)):
            self.test_40bid(genRandomString(10), 
                    random.randrange(42), 
                    genRandomString(30))

    # check the bids we performed were actually saved
    def test_60checkBids(self):
        for auction in self.createdAuctions:
            # GET auction
            req = urllib2.Request(baseurl + auction['admin_url'])
            f = urllib2.urlopen(req)
            # status
            status = f.getcode()
            # headers
            meta = f.info()
            # data
            response = f.read()
            f.close()
            assert (status == 200) # hit
            data = json.loads(response)
            for b in data['bids']:
                assert (b in auction['bids'])

    def test_debugIndex(self):
        req = urllib2.Request(baseurl + '/auctions')
        f = urllib2.urlopen(req) # GET /
        status = f.getcode()
        # headers
        meta = f.info()
        # data
        response = f.read()
        f.close()
        #assert (status == 200) # hit
        data = json.loads(response)
        assert (status == 200)

