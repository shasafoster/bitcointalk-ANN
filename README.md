# bitcointalk-ANN
Aim: To scrape a 1000+ bitcointalk [ANN] thread into a single highly readible html document for better reading and analysis
An example of such a thread: https://bitcointalk.org/index.php?topic=421615.20

## Introduction
Currently reading the bitcointalk [ANN] thread for a crypto-currency is useful tool for (investment) analysis of crypto-currency.
The issues faces by a reader of a bitcointalk [ANN] are
1. Their are  often 1000+ pages in the [ANN] thread so you have to click the 'next button' 1000+ times
2.There are ads, user footer/motto's, icons ... that effect readibility
3. The styling is un-appealing

## Timeline
The three issues outlined above outline the timeline of the project.
The first challenge has been addressed and completed.

### To Do.
1. Remove the ads, annoying icons, user footers and mottos from the document
2. Make the styling attractive and highly readible (think medium.com)


## Install / Use

#### Install packages
Scrapy: https://scrapy.org/  $ pip install scrapy
BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/ $ pip install beautifulsoup4
lxml: http://lxml.de/installation.html $ pip install lxml

#### Step 1.
Create a new directory (folder) on your computer

#### Step 2.
Clone the repository into this new directory on your computer

#### Step 3.
Open the command propmt in this new directory 

#### Step 4. 
Enter:
```
$python runfile.py
```
* *The command prompt will ask you to enter the name of the crpyto-currencies you want to create the [ANN] document for.*
* *This command should take 1-3 seconds to run*

#### Step 5.
Enter: 
```
$scrapy crawl bitcointalk
```
* *This command will run the spider*
* *This command will take much longer to run (it depends highly on the number of webpages the spider has to parse)*

#### Step 6.
After the spider has finished running, if there were no errors, an .html document should have been created in the new top level directory that you created.
