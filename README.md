Copyright (c) 2013,  Backyard Innovations UK Ltd.

See the LICENSE.txt file for licensing information.
The license in license.txt is applicable to all files in this
repository.

== API description ==


    GET /
returns placeholder page (index)

    GET /auctions
list all auctions (debug only!!)

    POST /auction/
Starts an auction. 
Parameters: 
    desc
Returns:
    string: the ADMIN UUID (via the Location: header)

    GET /auction/admin_uuid </code>
Retrieves auction information + current status of all bids

    PUT /auction/admin_uuid: updates data
TBD

    POST: (?) creates a new admin_uuid?
TBD

    GET /auction/public_uuid
Retrieves the public information

    POST /auction/public_UUID
TBD: creates a new public uuid for referrals 

    PUT /auction/public_uuid
Performs a bid. 
Parameters: 
    bidder
    amount
    contact

    GET /auction/public_uuid/media 
retrieves all media files (images, video, etc.)
parameters: the number of images (for mobile?)
TBD

== Feature requests ==
    GET /auctions/auction_id/pictures/picture_id
rationale: for mobile app, to load/retrieve one pic at the time
