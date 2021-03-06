# Telegram Bot using python 3 and AWS

The aim of this silly repo is to build a telegram bot using Amazon AWS as hosting server for the code and python 3 as developing lenguage. The usage of AWS and lambda function was suggested by the fact that I didn't have a server to could contain the code for the bot :)

The functionalities of the bot are really basic. In the original idea it was meant to handle both translate requests of word (from english to italian) and provide weather information of a specified city or lacality. Due to my laziness the second point as never been implemented, though the weather functionality is still mentioned in the help message (I'm even too lazy to remove it from there). Regarding the first point, instead, I was not able to find a free dictionary API that could achieve my goal (maybe I didn't dig enough in the web), but I found that the Oxford dictionary has free API: unfortunately the completely free and very basic plan allows only to provide the english definition.

Eventually, I made peace with my mind and accepted what I could get: I was just trying to learn something new about telegram bot and engage myself in some python programming. I am well aware that this is not the optimal solution but that it was not my goal, as the previous sentence suggests.

## Preparatory steps

Since I ended up here trying to learn something new, I followed blogs/articles from other people who knew something about the topic. As far as I remember (since I'm writing this overview almost one year later I did the actual implementation), I found all the necessary information related to setting up the environment in Amazon AWS at this [link](https://dev.to/nqcm/-building-a-telegram-bot-with-aws-api-gateway-and-aws-lambda-27fg).
As suggested in many articles, it is better to store all the personal information in local variables (like the personal token of the bot or the key for the API) and let the code retrieve them when necessary. AWS Lambda function allows this possibility, since it contains a dedicated space for environmental variables that can be easily accessed from the code by calling a function provided by the os library:

```python
telegram_token = os.environ['TELEGRAM_BOT_TOKEN']
```
Further readings can be found in the dedicated [documentation](https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html).

### Add external package dependancies

In most of the basic guides related to telegram bot, the mentioned easiest way to handle communication is using python library *requests*. This library seems to be no more available in Botocore in AWS: as a result it must be added as external dependancy in the package that contains the core code of the lambda function uploaded to AWS. In order to so so, the best way is to follow the official [AWS Guidelines](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html#python-package-dependencies) which provides a thorough explanantion about how to include an external package to be used and upload it to the AWS environment. Up to now, I always uploaded the code as a **.zip** file directly from the Lambda section in AWS, containing both the code and the external dependancies.

Once the external dependacies have been correctly uploaded to the Lambda environment it is possible to easily import them within the functional code by simply adding the following piece of code when external libraries are needed.

```python
import os
import sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./vendored"))
import requests
```
In this way, assuming the external dependancies are stored in *vendored* folder, it is possible to import them in the current file and make use of them 

### Add vocabulary API

As already mentioned, the final choice fell on the Oxford dictionary. The first step consists in the registration to the [Oxford website](https://developer.oxforddictionaries.com/) to obtain the API key necessary to make requests from the bot (and each kind of application in general). The plan I chose is the completaly free one, called Prototype: since I'm just playing around with telegram bot and its accessories, I thought it was not worth it to spend money on it. After the requested information are entered, the *tuple* (API Base URL, Application ID, Application Keys) is available in the Oxford personal account. The personal information should be stored in environmental variables accessible by the Lambda function and not directly written in the code. Assuming this, the snippet code to make use of this API should be something like this:

```python 
app_id = os.environ['OXFORD_APP_ID']
app_key = os.environ['OXFORD_APP_KEY']
language = 'en-gb'
dic_api_url = 'https://od-api.oxforddictionaries.com:443/api/v2/entries/'  + language + '/'

headers = {
    'app_id': f"{app_id}",
    'app_key': f"{app_key}"
}

new_url = dic_api_url + word_to_translate
response = requests.get(new_url, headers=headers)
```
Basic documentation related to requests can be found [here](https://developer.oxforddictionaries.com/documentation/making-requests-to-the-api). By implementing this solution it is possible to have a fixed string that contains the basic URL and append every time the specific word to be translated.
However, Oxford dictionary API allows more refined way to retrieve information from its database: a deeper overview of the API possibilities can be found at this [link](https://developer.oxforddictionaries.com/documentation#!/Entries/get_entries_source_lang_word_id).
In particular, this is possbile by simply adding a *field* specification in the url request: the variable *dic_api_url* metioned in the previous code snippet will become something like this

```python 
dic_api_url = 'https://od-api.oxforddictionaries.com:443/api/v2/entries/'  + language + '/word_id?fields=definitions&strictMatch=false'

```
where *word_id* represents the word whose definition we are looking for. Additionally, at first sigth it appears clear that two or more fields can be combined in the request. In order to do so it is possible to simply apply the boolean logic to the possible entries. In order to know exactly which are the allowed fields to be retrieved it is possible to make use of the previously menioned link.

