# FIRESELL unit-testing
# descriptions by bob
# code by lor
# super-early-rough-proof of concept

from webtest import TestApp
from bs4 import BeautifulSoup
import json
import simple

app = TestApp(simple.app)

# awesome stuff from http://stackoverflow.com/a/2257449/204634
import random
import string
def gen_randomstring(length=12, what=None):
    if what is None:
        what = string.ascii_uppercase + string.digits + string.ascii_lowercase
    return ''.join(random.choice(what) for x in range(length))

# Use Case 1, Auctioneer Creates Auction

# a test object
# TODO fill in with random URLs, XSS, attacks, vulns, long strings, etc. etc.
auction = dict()
auction['itemname'] = gen_randomstring()
auction['itemdesc'] = gen_randomstring(150)
auction['itemloc'] = gen_randomstring(255)
auction['itemprice'] = gen_randomstring(10)


def test_index():
    assert app.get('/').status == '200 OK'

def test_start_auction():
    # auctioneer opens page, fills in data and submits 
    post = app.post('/auctions', auction)
    # returns '201 created'
    assert post.status_int == 201
    # response parsing, save into local object for further tests
    # the .html is done through BeautifulSoup parsing, isn't it nice?
    auction['admin_url'] = post.html.find(id='admin_url').get('href')
    assert auction['admin_url'] is not None
    auction['public_url'] = post.html.find(id='public_url').get('href')
    assert auction['public_url'] is not None

    # check that the returned data actually matches what we POST'd
    check_dataMatches(post.html)

# data is beautifulsoup'd parsed html
def check_dataMatches(data):
    assert auction['itemname'] in data.find(id="itemname").get_text()
    assert auction['itemdesc'] in data.find(id="itemdesc").get_text()
    assert auction['itemloc'] in data.find(id="itemloc").get_text()
    assert auction['itemprice'] in data.find(id="itemprice").get_text()

def test_adminurl():
    res = app.get(auction['admin_url'])
    assert res.status == '200 OK'
    # test that the response has the public_url item
    check_dataMatches(res.html)

# hoping the tests are executed in the order they appear here..
def test_publicurl():
    res = app.get(auction['public_url'])
    assert res.status == '200 OK'
    # test that the data inserted matches
    check_dataMatches(res.html)


# Use Case 2, Bidder Receives Invitation, places bid

thisbid = { 'biddername': gen_randomstring(10),
        'amount': gen_randomstring(2),
        'question': gen_randomstring(255)
        }
def test_bid():
    # recycling the public url for now
    res = app.post(auction['public_url'], thisbid)
    # and the admin url for simple testing
    data = app.get(auction['admin_url'])
    for bid in data.html.find_all(id='bid'):
        if bid is None:
            continue
        if thisbid['biddername'] in bid.find(id='biddername').get_text() and thisbid['amount'] in bid.find(id='amount').get_text() and thisbid['question'] in bid.find(id='question').get_text():
            found = True
        else:
            found = False
    assert found
