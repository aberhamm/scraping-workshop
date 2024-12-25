#!/bin/bash

# Monitor for changes in Python files and restart Scrapy spider
watchmedo auto-restart --patterns="*.py" --recursive -- scrapy crawl splash_spider
