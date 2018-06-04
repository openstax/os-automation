# ospages

Chromedriver: http://chromedriver.chromium.org/downloads

Firefox: https://github.com/mozilla/geckodriver/releases

Safari:

    1. Ensure that the Develop menu is available. It can be turned on by opening Safari preferences (Safari > Preferences in the menu bar), going to the Advanced tab, and ensuring that the Show Develop menu in menu bar checkbox is checked.
    2. Enable Remote Automation in the Develop menu. This is toggled via Develop > Allow Remote Automation in the menu bar.
    3. Authorize safaridriver to launch the webdriverd service which hosts the local web server. To permit this, run /usr/bin/safaridriver once manually and complete the authentication prompt.

Clone the repository

    git clone https://github.com/openstax/ospages

Setup the enivronment

    pip install -r requirements.txt

Run the tests

    tox -- --driver chrome --duration=10

_may substitute `safari` or `firefox` for `chrome`_
