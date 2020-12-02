# Telegram Bot using python 3 and AWS

The aim of this silly repo is to build a telegram bot using Amazon AWS as hosting server for the code and python 3 as developing lenguage. The usage of AWS and lambda function was suggested by the fact that I didn't have a server to could contain the code for the bot :)

The functionalities of the bot are really basic. In the original idea it was meant to handle both translate requests of word (from english to italian) and provide weather information of a specified city or lacality. Due to my laziness the second point as never been implemented, though the weather functionality is still mentioned in the help message (I'm even too lazy to remove it from there). Regarding the first point, instead, I was not able to find a free dictionary API that could achieve my goal (maybe I didn't dig enough in the web), but I found that the Oxford dictionary has free API: unfortunately the completely free and very basic plan allows only to provide the english definition.

Eventually, I made peace with my mind and accepted what I could get: I was just trying to learn something new about telegram bot and engage myself in some python programming. I am well aware that this is not the optimal solution but that it was not my goal, as the previous sentence suggests.

## Preparatoy steps

Since I ended up here trying to learn something new, I followed blogs/articles from other people who knew something about the topic. As far as I remember (since I'm writing this overview almost one year later I did the actual implementation), I found all the necessary information related to setting up the environment in Amazon AWS at this [link](https://dev.to/nqcm/-building-a-telegram-bot-with-aws-api-gateway-and-aws-lambda-27fg).

## Usage

```bash
pip install foobar
```

```python
import foobar

foobar.pluralize('word') # returns 'words'
foobar.pluralize('goose') # returns 'geese'
foobar.singularize('phenomena') # returns 'phenomenon'
```

### Subsection

It is also possible to add a further subsection by increasing the number of the # before entering the name

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
