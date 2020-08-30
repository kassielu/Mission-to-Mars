#!/usr/bin/env python
# coding: utf-8

# # 10.3.3 - Scrape Mars Data: The News

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import requests


# In[2]:


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)


# In[3]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[4]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[5]:


slide_elem.find("div", class_='content_title')


# In[6]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[7]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# # 10.3.4 - Scrape Mars Data: Featured Image

# ### Featured Images

# In[8]:


# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[9]:


# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# In[10]:


# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# In[11]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[12]:


# Find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# In[13]:


# Use the base URL to create an absolute URL
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# # 10.3.5 - Scrape Mars Data: Mars Facts

# In[14]:


df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df


# In[15]:


# Convert our DataFrame back into HTML-ready code
df.to_html()


# ## Visit the NASA Mars News Site

# In[16]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[17]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[18]:


slide_elem.find("div", class_='content_title')


# In[19]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[20]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### JPL Space Images Featured Image

# In[21]:


# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[22]:


# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# In[23]:


# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# In[24]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[25]:


# find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# In[26]:


# Use the base url to create an absolute url
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# ### Mars Facts

# In[27]:


df = pd.read_html('http://space-facts.com/mars/')[0]

df.head()


# In[28]:


df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
df


# In[29]:


df.to_html()


# ### Mars Weather

# In[30]:


# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# In[31]:


# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# In[32]:


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[33]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[34]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# Parse the HTML
html = browser.html
html_soup = soup(html, 'html.parser')

div_result = html_soup.find('div', class_='result-list')
div_items = div_result.findAll('div', class_='item')

# 3. Write code to retrieve the image urls and titles for each hemisphere.
for div_item in div_items:
    #Create an empty dictionary, hemispheres = {}, inside the for loop.
    hemisphere = {}
    div_content = div_item.find('div', class_='description')
    
    title = div_content.find('h3').text
    hemisphere['title'] = title
    
    # Get the image URL 
    thumb_url = div_item.find('a', {"class":"itemLink product-item"})['href']
    thumb_url = f'https://astrogeology.usgs.gov{thumb_url}'
    
    # click on each hemisphere link, 
    browser.visit(thumb_url)
    html = browser.html
    image_soup = soup(html, 'html.parser')
    image_url = image_soup.find('div', class_='container').find('div', class_='wide-image-wrapper').find('a')['href']    
    hemisphere['image_url'] = image_url
    
    
    #print(hemisphere)
    hemisphere_image_urls.append(hemisphere)


# In[35]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[37]:


# 5. Quit the browser
browser.quit()

