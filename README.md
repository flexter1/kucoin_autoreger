# kucoin_autoreger

## Description

This software helps you registering KuCoin accounts automatically with Rambler mails. (supports Selenium)

## Features

1) Changes Rambler password
2) Registers KuCoin account
3) Set trading password
4) Get USDT TRC20 deposit wallet address
5) Switch deposit method from main to trading account
6) Get KuCoin account's UID

## Installation

It works via Selenium and https://anti-captcha.com/ extension. 

You need to refill anti-captcha account before starting the work. 


Also download chromedriver for your current Chrome version and system. You can download it here: https://chromedriver.chromium.org/downloads

Copy chromedriver to project folder.

Write in terminal:

```
pip install -r requirements.txt
```

Enter your `API_KEY`, prefer `trading password` and `processes count` in `config file`.

## WARNING! DO NOT ENTER MORE THAN 5 PROCESSES, OTHERWISE SELENIUM CAN START TO WORK UNCORRECTLY

## Developers

- [Flexter](https://github.com/flexter1)
- 
  [Telegram](https://t.me/flexterwork)
