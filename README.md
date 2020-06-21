zendesk-google-analytics
========

This demo code monitors Realtime Google Analytics page views for Zendesk articles. When an article localization is viewed its Zendesk _Flag for translation_ is set.


### Use case ###

Zendesk articles are translated with raw machine translation without human post-editing.
<<<<<<< HEAD
The articles are published and Google Analytics is used to monitor how well they are doing.
 Based on collected metrics the articles are categorized as high-value or low-value (eg. articles with a high number of visits are considered high-value content).

In this demo code, an article is considered high-value when it received at least one visit
(for demonstration purposed, realtime analytics are used. In real implementation, the metrics 
would be collected slowly over a given period of time).
When an article is visited, this demo code will connect to Zendesk and will set the article's
_Flag for translation_.

Translation Management Systems, such as Memsource, is configured to monitor the flag. The articles
with the flag set are pulled by the TMS and sent through a translation workflow that includes post-editing step.


### Installation ###

1. Make sure you have Python installed on your computer (this demo script was tested with Python 3).
1. Install `requests`, `oauth2client` v2.2.0 and `google-api-python-client`. The installation command may differ based on your OS (eg. macOS: `pip3 install --user requests oauth2client==2.2.0 google-api-python-client`).
1. Download this demo repository to your local drive.
1. Run `zendesk-hash.py` (eg. `python3 zendesk-hash.py`), enter your Zendesk account information and replace `PASTE_HASH_HERE` on the first line in `realtime.py` with the generated hash code.
1. Follow the instructions on [this page](https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py#pip) to enable the Google API and create a connection key. Download given JSON file and save it as `client_secrets.json` to the same location where you keep this `realtime.py` script.
1. Login to your Google Analytics account, navigate to Admin, and open View Settings. Copy the numerical `View ID` and replace the `PASTE_VIEW_ID_HERE` on the second line in `realtime.py`.
1. Run `realtime.py` (eg. `python3 zendesk.py`)
1. Visit translation of a Zendesk page. Realtime GA will report its view, this script will report its view and will flag its Zendesk copy for translation.
