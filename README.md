A Credit Card Validation Case Study
===================================

This case study provides an API that can be used to validate and
collect data about credit card numbers. It uses Django and the Django
Rest Framework. It is purely for demonstration purposes. It was
designed and tested on Linux, but should run on MacOS and will
possibly run on Windows.

About as much effort has been put into comments and documentation as
into code, though it should be fairly fast, clear, and bug-free. Any
questions or comments can be sent to <mtsaavedra@gmail.com>.


Setup Instructions
-------------------

1. Make sure Python 3.7 and Pipenv are installed on the test system.
Older versions of python might work, but have not been tested.

2. Clone the repository into an appropriate local directory
following the instructions on github.

3. In a terminal, change directories to the cloned repository

4. Initialize Pipenv:<br />
`pipenv --python 3.7`

4. Install dependencies:<br />
`pipenv update`


Testing Instructions
--------------------

1. Enter the project's virtualenv:<br />
`pipenv shell`

3. Run the test suite:<br />
`python manage.py test`

4. Run a test server on the localhost on port 8000:<br />
`python manage.py runserver`

5. Open a browser with the following URL which should return a Django
Rest Framework page:<br />
(http://localhost:8000/cc_numbers/random)

6. Follow the validation_link field to the other endpoint. It should
load a DRF page too.


API Usage
---------

There are two endpoints in this service:

1. /cc_numbers/validation/{card_number} - a GET request to this service
returns the validity and collected data about the card number.

2. /cc_numbers/random?network={network} - a GET request returns a random
credit card number and a link to validate it. The network querystring
parameter can be used to choose the network of the new number. If the
parameter is omitted, a random network is chosen.

There is also a swagger endpoint available at:<br />

(http://localhost:8000/cc_numbers/swagger)

This built-in API-browsing system contains very detailed usage information
about this service.


