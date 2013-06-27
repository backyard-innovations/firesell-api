Functional tests for firesell APIs
----------------------------------

Setup:

    mkdir env
    virtualenv env
    source env/bin/activate
    pip install nose

Run the tests (not that if BASEURL is not defined, it defaults to http://localhost:8080):

    source env/bin/activate
    export BASEURL=http://.......elasticbeanstalk.com
    nosetests .
