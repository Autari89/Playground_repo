# Telegram Bot using python 3 and AWS

The aim of this silly repo is to build a telegram bot using Amazon AWS as hosting server for the code and python 3 as developing lenguage. The usage of AWS and lambda function was suggested by the fact that I didn't have a server to could contain the code for the bot :)

The functionalities of the bot are really basic. In the original idea it was meant to handle both translate requests of word (from english to italian) and provide weather information of a specified city or lacality. Due to my laziness the second point as never been implemented, though the weather functionality is still mentioned in the help message (I'm even too lazy to remove it from there). Regarding the first point, instead, I was not able to find a free dictionary API that could achieve my goal (maybe I didn't dig enough in the web), but I found that the Oxford dictionary has free API: unfortunately the completely free and very basic plan allows only to provide the english definition.

Eventually, I made peace with my mind and accepted what I could get: I was just trying to learn something new about telegram bot and engage myself in some python programming. I am well aware that this is not the optimal solution but that it was not my goal, as the previous sentence suggests.

## Preparatory steps

Since I ended up here trying to learn something new, I followed blogs/articles from other people who knew something about the topic. As far as I remember (since I'm writing this overview almost one year later I did the actual implementation), I found all the necessary information related to setting up the environment in Amazon AWS at this [link](https://dev.to/nqcm/-building-a-telegram-bot-with-aws-api-gateway-and-aws-lambda-27fg).

### Add external package dependancies

In most of the basic guides related to telegram bot, the mentioned easiest way to handle communication is using python library *requests*. The *requests* seems to be no more available in Botocore in AWS: as a result it must be added as external dependancy in the package that contains the core code of the lambda function uploaded to AWS. In order to so so, the best way is to follow the official [AWS Guidelines](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html#python-package-dependencies) which provides a thorough explanantion about how to include an external package to be used and upload it to the AWS environment. Up to now, I always uploaded the code as a **.zip** file directly from the Lambda section in AWS, containing both the code and the external dependancies.

Once the external dependacies have been correctly uploaded to the Lambda environment it is possible to easily import them within the functional code by simply adding the following piece of code when external libraries are needed.

```python
import os
import sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./vendored"))
import requests
```
In this way, assuming the external dependancies are stored in *vendored* folder, it is possible to import them in the current file and make use of them 
