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
The script is divided into 4 major chunks.
1. Using Selenium to retrieve the html source code
2. Using BeautifulSoup to extract book-data from the html source code
3. Filtering and sorting the book-data for the required year
4. Generating the markdown for the jekyll blog using the filtered book-data.

These four steps are represented by the respective functions in the *main* scope.

{% highlight python linenos %}

if __name__ == '__main__':

    html_str = get_html_using_selenium(MAIN_URL)

    book_list = get_books_data(html_str)

    filtered_and_sorted_book_list = filter_and_sort_books(book_list, YEAR)

    create_markdown(filtered_and_sorted_book_list, YEAR, INTRO_PARA_OF_BLOG,
                    OUTPUT_MD_FILE_PATH)

{% endhighlight %}

<br>
## 0. Let's start with understanding the imports and global variables

{% highlight python linenos %}
 from selenium import webdriver
 import time
 from bs4 import BeautifulSoup
{% endhighlight %}

The [*Selenium*](https://pypi.org/project/selenium/) package is used to automate web browser interaction with python. We will use it to open and scroll the goodreads page in an automated way.

Time is the standard python library which will be used to insert delays in scrolling.

[*BeautifulSoup*](https://pypi.org/project/beautifulsoup4/) is a python library to scrap data from web pages.


{% highlight python linenos %}
 YEAR = '2020'
 OUTPUT_MD_FILE_PATH = 'markdown_file.md'
 INTRO_PARA_OF_BLOG = f'{YEAR} was a good reading year for me. The Covid induced work-from-home saved ample travel hours for me to fall in love with reading again. Here are the books that I read this year - some of them were delightful; others not so much.\n'
 CHROME_DRIVER_PATH = '/full/path/to/downloaded/chromedriver'
 MAIN_URL = 'https://www.goodreads.com/review/list/13487053-ankit-modi?order=d&ref=nav_mybooks&shelf=read&sort=date_read&utf8=%E2%9C%93'
{% endhighlight %}
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

<br>
## 1. Using Selenium to retrieve the html source code

Following is the code snippet for this function:

{% highlight python linenos %}
def get_html_using_selenium(url, CHROME_DRIVER_PATH):

    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
    driver.get (url)

    # handle infinite scroll
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match = False
    while(match==False):
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True

    # Page is fully scrolled now. Next step is to extract the source code from it.
    my_html = driver.page_source
    driver.quit()

    return my_html
{% endhighlight %}

*Line 2-4* will start a chrome session using the chrome driver and open the goodreads URL.

*Line 7-14* is used to handle the infinite scroll of the goodreads page. *Line 7* stores the current length of the page. The *while* loop starting at *line 9* scrolls down to the bottom of the page and waits for 3 seconds for the remaining book list to load. It measures the length of the page after the wait and checks if the length has increased. If not, the loop is exited.

*Line 17* stores the source code of the page.

*Line 18* exits the chrome driver and *line 20* returns the source code.



<br>
## 2. Using BeautifulSoup to extract book-data from the html source code

Following is the code snippet for this function:

{% highlight python linenos %}

def get_rating_from_text(rating_text):
    rating_dict = {'did not like it': '1',
                   'it was ok': '2',
                   'liked it': '3',
                   'really liked it': '4',
                   'it was amazing': '5'}

    return rating_dict[rating_text]


 def get_books_data(html_str):
    soup = BeautifulSoup(html_str, 'lxml')

    table = soup.find_all('table', {'id':'books'})[0]
    table_rows = table.find_all('tr')
    book_list = []

    for tr in table_rows[1:]:
        book_dict = {}

        # parse cover_url
        td = tr.find_all('td', {'class':'field cover'})[0]
        img = td.find_all('img')[0]
        book_dict['cover_url'] = img['src']

        # parse title and book's url
        td = tr.find_all('td', {'class':'field title'})[0]
        a_link = td.find_all('a')[0]
        book_dict['title'] = a_link.get('title')
        book_dict['book_url'] = a_link.get('href')

        # parse author and author_url
        td = tr.find_all('td', {'class':'field author'})[0]
        a_link = td.find_all('a')[0]
        book_dict['author_name'] = a_link.text
        book_dict['author_url'] = a_link.get('href')

        # parse rating
        td = tr.find_all('td', {'class':'field rating'})[0]
        span = td.find_all('span', {'class':'staticStars notranslate'})[0]
        rating_text = span.get('title')
        rating = get_rating_from_text(rating_text)
        book_dict['rating'] = rating

        # parse review
        review = ''
        td = tr.find_all('td', {'class':'field review'})
        if(len(td) > 0):
            td = td[0]
            span = td.find_all('span')
            if(len(span) > 0):
                span = span[-1]
                lines = [str(i) for i in span.contents]
                review = ' '.join(lines)
        book_dict['review'] = review

        # parse date_read
        td = tr.find_all('td', {'class':'field date_read'})[0]
        span = td.find_all('span', {'class':'date_read_value'})[0]
        date_read = span.text
        book_dict['date_read'] = date_read

        book_list.append(book_dict)

    return book_list
{% endhighlight %}
*Line 1-8* is a function for rating's conversion (from string to numbers). The html source code of the goodreads page has the ratings represented by these strings. *get_rating_from_text()* will convert them to their corresponding numeric value. This function is used in *line 42*.

*Line 11* defines the function to get the book data from the source code.

*Line 12* consumes the html source code to return a *BeautifulSoup* object.

By observing the html source closely (see the picture below), we can see that most of the book-related data is stored in a table whose *id* is *'books'*. We extract that table in *line 14*.

![]({{ site.url }}/images/scraping_goodreads/table_book.png)

Further, we extract all the the rows from the table in *line 15*. We initialize *book_list* to store all the extracted data in *line 16*.

In *line 18-63*, we will loop over all the rows/ books, create a dictionary to store data related to each book and append that dictionary to the *book_list*.

*Line 21-24* extracts the cover url. Let's understand that piece of code. Rest of the code snippets to extract title, book's url, author name etc will follow similarly. Let's look at the data format in the html source code.

![]({{ site.url }}/images/scraping_goodreads/cover_url.png)

We can see that each book has multiple *td* objects (cover, title, author etc.). *Line 22* takes the current book's *tr* object and finds the first *td* objects with *class 'cover'* in it. *Line 23* extracts the first *img* tag from the *td* object. *Line 24* extracts the image source (url) and puts it in *book_dict*. We do similar extractions for rest of the required fields.
