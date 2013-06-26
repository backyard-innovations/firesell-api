Copyright (c) 2013,  Backyard Innovations UK Ltd.

See the LICENSE.txt file for licensing information.
The license in license.txt is applicable to all files in this
repository.

API description
===============

Create Auction:
---------------
    POST /auction/
Starts an auction. 
Parameters: 

    desc

Returns:

    Location: uuid

The admin uuid (via the Location: header)

Managing an auction:
--------------------

    GET /admin/uuid

Retrieves auction information + current status of all bids

    PUT /admin/uuid: 
    
Updates data. TBD

    POST: /admin/uuid 

Creates a new uuid for managment. TBD

Displaying an auction:
----------------------

    GET /auction/uuid
    
Retrieves the available public information

    POST /auction/public_UUID

Creates a new public uuid for referrals. TBD

Bidding:
--------

    PUT /auction/public_uuid

Performs a bid.  Parameters: 

    bidder
    amount
    contact


Misc:
-----

    GET /

returns placeholder page (index)

    GET /auctions

list all auctions (debug only!!)



Feature requests
================

    GET /auctions/auction_id/pictures/picture_id
rationale: for mobile app, to load/retrieve one pic at the time

    GET /auction/public_uuid/media 

retrieves all media files (images, video, etc.)
parameters: the number of images (for mobile?)
TBD
