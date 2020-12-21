---
layout: post
title: Scraping Goodreads using Python to create your own "My year in books" blog
categories: Technology
css: highlights
---

I like reading books and writing reviews on Goodreads. And I wanted to create an year end blog post to share those books and reviews. However, copy-pasting all these reviews from Goodreads didn't seem like a good idea - specially if you want to do it every year.

What's the answer to avoid doing something repeatedly? Automation. This seemed like a nice weekend project to learn web scraping and automate the creation of such blog. I am sharing the project in this blog. If you directly want to access the script, pleae visit this [link](https://github.com/ankitmodi/year_end_book_blog_using_python/blob/main/main.py).

## Major steps
The script is divided into 4 major steps.
1. Using Selenium to get the html source code.
2. Using BeautifulSoup to extract book-data from the html
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
