# Leader Behaviour Prediction
This project will deal with extracting and gathering information about the behaviour/ bad work (corresponding to predefined adjectives ) of a leader/ representative by constantly scraping news website.

## Installing required libraries

```
sudo pip install requirements.txt
```

## Scraping Times of India website

I have scraped [Times Of India Website](https://timesofindia.indiatimes.com/) specially for this purpose.

#### The dataset got after scraping Times of India website 

This dataset have the details of the scrapped article. We have to scrap the text and get the names.
Then we have to match the details of the adjective with the matched names that is got.

The dataset is present in the path :

```
LeaderBehaviour/leaderBehaviour/leaderBehaviour/spiders/newsTOI.sqlite
```

![Dataset](leaderBehaviour/img/TOI.png)


#### Scraped names of the members of parliaments in US :

```
LeaderBehaviour/getUSNames/getUSNames/spiders/getUSNames.json
```

#### SCraped the names of the members of parliaments in India :

```
LeaderBehaviour/getIndianPolNames/getIndianPolNames/spiders/getIndianPolNames.json
```

#### Additional Objectives :

    * used headers/ user-agent in scrapy.
    * need to use proxy/ integrate with Tor to make it completely untraceable.

