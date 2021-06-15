# <h1 align=center>Optical Character Recognition Bot</h1>

<p align=center><img src="assets/images/ocr.png" alt="logo" width="250px" height="250px"/></p>

<h3 align=center>A Telegram bot to extract text from image using python</h3>

---

## About

You can send an image containing text to this bot and it will respond quickly with the extracted text from the picture!

Start chat with this bot on [telegram](https://telegram.me/the_ocr_bot)

--- 
## Requirements

* Bot token from [Bot Father](https://t.me/BotFather), If you don't know how to get bot token, read [this](https://core.telegram.org/bots#6-botfather)

* OCR api key, get your api key from [here](https://ocr.space/ocrapi)

---
## Installation 

#### You can fork the repo and deploy it on Heroku :)  

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

OR

* Clone this repository using
```sh
$ git clone https://github.com/amit-y11/the_ocr_bot
```
* Enter the directory and install all the requirements using
```sh
$ pip3 install -r requirements.txt
```
* Edit line 12 and paste your ocr api key
```sh
12        api_key = "Your Api key from https://ocr.space/ocrapi"
```
* Edit line 13 and paste your Bot token
```sh
13       token="Your Bot Token"
```
#### Run Your Bot using the following command :
```sh
$  python3 bot.py
```