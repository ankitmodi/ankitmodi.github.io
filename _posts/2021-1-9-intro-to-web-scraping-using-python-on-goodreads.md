---
layout: post
title: Scraping Goodreads to create your year-end blog of books &#58; An intro to Web Scraping using Python
categories: Technology
css: highlights
---

I like reading books and writing reviews on Goodreads. And I wanted to create a year-end blog post to share those books and reviews. However, copy-pasting all these reviews from Goodreads didn't seem like a good idea - especially if you want to repeat the task every year.

What's the obvious answer to avoid repetition? Well, if you're a programmer, it's *automation*. Moreover, this seemed like a nice little project to learn web scraping. So, I wrote a python script to automate this task. This blog expands upon my learnings and explains the script in detail. If you directly want to access the script, please visit this [link](https://github.com/ankitmodi/year_end_book_blog_using_python/blob/main/main.py). Keep reading if you're new to web-scraping or python.

Note that I am using *python3* in this script.

## Major steps
The script is divided into 4 major chunks.
1. Using Selenium to retrieve the Html source code
2. Using BeautifulSoup to extract book-data from the Html source code
3. Filtering and sorting the book-data for the required year
4. Generating the markdown for the Jekyll blog using the filtered book-data

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

The [*Selenium*](https://pypi.org/project/selenium/) package is used to automate web browser interaction with python. We will use it to open and scroll the Goodreads page in an automated way.

*time* is the standard python library that will be used to enact delays in scrolling.

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

*INTRO_PARA_OF_BLOG* is the string that becomes the first paragraph of your markdown (md) blog. You can also edit this paragraph directly in the resultant md file.

*CHROME_DRIVER_PATH* is the path of the chromedriver to be used by selenium. Download the latest version from [here](https://chromedriver.chromium.org/) and assign the full path of the downloaded file to this variable.

*MAIN_URL* is the URL that we need to open in selenium. Follow the following steps to generate a similar URL for your profile:
* Login into [Goodreads](https://www.goodreads.com/) and hit the *My Books* tab on the top left.

![]({{ site.url }}/images/scraping_goodreads/my_books.png)

* Click on the *read* shelf

![]({{ site.url }}/images/scraping_goodreads/read.png)


* Sort the book list by *date read*. Make sure that the sorting is in descending order. If not, click on *date read* again.

![]({{ site.url }}/images/scraping_goodreads/sort_read.png)

Notice how the URL is changing while following these steps. Copy the final URL and assign it to the *MAIN_URL* variable.


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

*Line 2-4* will start a chrome session using the chrome driver and open the Goodreads URL.

*Line 7-14* is used to handle the infinite scroll of the Goodreads page. *Line 7* stores the current length of the page. The *while* loop starting at *line 9* scrolls down to the bottom of the page and waits for 3 seconds for the remaining book list to load. It measures the length of the page after the wait and checks if the length has increased. If not, the loop is exited.

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
*Line 1-8* is a function to convert ratings from strings to numbers. The Html source code of the Goodreads page has the ratings represented by these strings. The function *get_rating_from_text()* will convert them to their corresponding numeric value. This function is used in *line 42*.

*Line 11* defines the function to get the book data from the source code.

*Line 12* consumes the Html source code to return a *BeautifulSoup* object.

By observing the Html source closely (see the picture below), we can see that most of the book-related data is stored in a table whose *id* is *'books'*. We extract that table in *line 14*.

![]({{ site.url }}/images/scraping_goodreads/table_book.png)

Further, we extract all the rows from the table in *line 15*. We initialize *book_list* to store all the extracted data in *line 16*.

In *line 18-63*, we loop over all the rows/ books, create a dictionary to store data related to each book, and append that dictionary to the *book_list*.

*Line 21-24* extracts the cover URL. Let's understand that piece of code. The rest of the code snippet works similarly to extract the title, book's URL, author name, etc. Let's look at the data format in the Html source code.

![]({{ site.url }}/images/scraping_goodreads/cover_url.png)

We can see that each book has multiple *td* objects (cover, title, author, etc.). *Line 22* takes the current book's *tr* object and finds the first *td* objects with *class 'cover'* in it. *Line 23* extracts the first *img* tag from the *td* object. *Line 24* extracts the image source (URL) and puts it in *book_dict*. We do similar extractions for the rest of the required fields.



<br>
## 3. Filtering and sorting the book-data for the required year

The next step is to filter the books of the required year which is *2020* in this case (see variable *YEAR*). Following is the code snippet for this function:

{% highlight python linenos %}
 def filter_and_sort_books(book_list, year):
     filtered_list = [i for i in book_list if year in i['date_read']]
     sorted_list = sorted(filtered_list, key=lambda k: k['rating'], reverse=True)
     return sorted_list
{% endhighlight %}

*Line 2* filters the list for the books read in 2020.

*Line 3* sorts the filtered list by the reader's ratings.



<br>
## 4. Generating the markdown for the Jekyll blog using the filtered book-data

Our next function will consume the filtered & sorted book data and generate the markdown file that we can directly use in our jekyll blog. Here is the code snippet for this function:

{% highlight python linenos %}
def create_markdown(filtered_and_sorted_book_list, year, intro_para,
                    md_file_path):
    url_prefix = 'https://www.goodreads.com/'

    with open(md_file_path, 'w') as f:
        f.write('---\n')
        f.write('layout: post\n')
        f.write(f'title: My Year in Books - {year}\n')
        f.write('---\n')
        f.write(f'{intro_para}\n')

        # loop over book list and create md paragraphs for each book
        for i in range(len(filtered_and_sorted_book_list)):
            curr_book = filtered_and_sorted_book_list[i]

            # title, book_url
            book_url = url_prefix + curr_book['book_url']
            f.write(f"### <a href='{book_url}' target='_blank'>{i+1}. {curr_book['title']}</a>\n")

            #cover_url
            small_cover_url = curr_book['cover_url']
            basename = small_cover_url.split('/')[-1]
            s = basename.index('._')
            e = basename.index('_.') + 1
            new_basename = basename[:s] + basename[e:]
            big_cover_url = small_cover_url.replace(basename, new_basename)
            f.write(f"![cover image]({big_cover_url})" + "{: height='300' width='200px' style='float:left; padding-right:20px; padding-bottom:5px; padding-top:5px' }\n")

            # author_name, author_url
            author_str = curr_book['author_name']
            author_arr = [i.strip() for i in author_str.split(',')]
            author_name = ' '.join(author_arr[::-1])
            author_url = url_prefix + curr_book['author_url']
            f.write(f"Author: <a href='{author_url}' target='_blank'>_{author_name}_</a>\n")
            f.write('<br>\n')

            # my rating
            f.write(f"My rating: ___{curr_book['rating']} out of 5 stars___\n")
            f.write('<br><br>\n')

            # review
            f.write(curr_book['review'] + '\n')
            f.write('<br clear="all"><br>\n\n\n\n')

    print('Markdown created !!')
{% endhighlight %}

*Line 5-11* opens the markdown file from the provided path and writes the blueprint of a Jekyll blog (layout, title, initial paragraph)in it.

We loop over the book list in *Line 13-43* and create the markdown paragraph for each book. Here's a screenshot to show how each book paragraph looks like:

![]({{ site.url }}/images/scraping_goodreads/book_para1.png)

*Line 14* assigns the current book dictionary to *curr_book* variable.

*Line 17-18* adds the book heading with its URL pointing to its Goodreads link.

*Line 21-27* extracts the link for the cover page and places it on the left side as shown in the picture above.

*Line 30-35* adds the author's name and links it to his/her Goodreads page as shown in the top right part of the above image.

*Line 38-39* adds *My rating* just below the author's name as shown in the image.

*Line 42-43* adds the review below it.

These paragraphs are created for each book in the *book_list*.
<br><br>

That's it. Your markdown file is created. The file is ready to be copied and pasted in your Jekyll blog (typically inside the *_posts* folder). You're set to share your books and reviews with your friends now!

Keep reading & keep sharing!
