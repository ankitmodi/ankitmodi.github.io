---
layout: post
title: Scraping Goodreads using Python to create your "My year in books" blog
categories: Technology
css: highlights
---

I like reading books and writing reviews on Goodreads. And I wanted to create an year end blog post to share those books and reviews. However, copy-pasting all these reviews from Goodreads didn't seem like a good idea - specially if you want to do it every year.

Sp, what's the obvious answer to avoid repeatedly a task? Automation. Moreover, this seemed like a nice weekend project to learn web scraping and automate the creation of such blog. If you directly want to access the script, pleae visit this [link](https://github.com/ankitmodi/year_end_book_blog_using_python/blob/main/main.py).

Note that I am using *python3*.

## Major steps
The script is divided into 4 major steps.
1. Using Selenium to retrieve the html source code
2. Using BeautifulSoup to extract book-data from the html source code
3. Filtering and sorting the book-data for the required year
4. Generating the markdown for the jekyll blog using the filtered book-data.

These four steps are represented by the respective functions in the *main* scope.

```py

if __name__ == '__main__':
    html_str = get_html_using_selenium(MAIN_URL)

    book_list = get_books_data(html_str)

    filtered_and_sorted_book_list = filter_and_sort_books(book_list, YEAR)

    create_markdown(filtered_and_sorted_book_list, YEAR, INTRO_PARA_OF_BLOG,
                    OUTPUT_MD_FILE_PATH)

```
## 0. Let's start with understanding the imports and global variables

```py
from selenium import webdriver
import time
from bs4 import BeautifulSoup
```

The [*Selenium*](https://pypi.org/project/selenium/) package is used to automate web browser interaction with python. We will use it to open and scroll the goodreads page in an automated way.

Time is the standard python library which will be used to insert delays in scrolling.

[*BeautifulSoup*](https://pypi.org/project/beautifulsoup4/) is a python library to scrap data from web pages.


```py
YEAR = '2020'
OUTPUT_MD_FILE_PATH = 'markdown_file.md'
INTRO_PARA_OF_BLOG = f'{YEAR} was a good reading year for me. The Covid induced work-from-home saved ample travel hours for me to fall in love with reading again. Here are the books that I read this year - some of them were delightful; others not so much.\n'
CHROME_DRIVER_PATH = '/full/path/to/downloaded/chromedriver'
MAIN_URL = 'https://www.goodreads.com/review/list/13487053-ankit-modi?order=d&ref=nav_mybooks&shelf=read&sort=date_read&utf8=%E2%9C%93'
```
*YEAR* is the year for which you want to create your blog for.

*OUTPUT_MD_FILE_PATH* is the path where you want to dump your markdown blog file.

*INTRO_PARA_OF_BLOG* is the string that becomes the first paragraph of your markdown (md) blog. You can also edit this paragraph directly in the md file created.

*CHROME_DRIVER_PATH* is the path of the chromedriver to be used by selenium. Download the latest version from [here](https://chromedriver.chromium.org/) and assign the full path of the downloaded file to this variable.

*MAIN_URL* is the URL that we need to open in selenium. Follow the following steps to generate a similar URL for your profile:
* Login into [Goodreads](https://www.goodreads.com/) and hit the *My Books* tab on top left.

![]({{ site.url }}/images/scraping_goodreads/my_books.png)

* Click on the *read* shelf

![]({{ site.url }}/images/scraping_goodreads/read.png)


* Sort the book list by *date read*. Make sure that the sorting is in descending order. If not, click on *date read* again.

![]({{ site.url }}/images/scraping_goodreads/sort_read.png)

Notice how the URL is changing while making all the changes. Copy the final URL and put assign it to the *MAIN_URL* variable.


Now that we have seen the imports and variable names, let's move on to the meat of the code.

## 1. Using Selenium to retrieve the html source code

Following is the code snippet for this function
