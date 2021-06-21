import telegram
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from bs4 import BeautifulSoup
import urllib.request as req
from selenium import webdriver
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
import pandas as pd
from GoogleNews import GoogleNews
from newspaper import Article
import pandas as pd
from io import StringIO


#########################################
######## Code - Webscraping part ########
#########################################

class Crawler:
    ## Crawler for the number of today's new covid case (in South Korea)
    def covid_case_crawler():
        code = req.urlopen(
            "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EC%BD%94%EB%A1%9C%EB%82%98+%ED%99%95%EC%A7%84%EC%9E%90&oquery=%EC%BD%94%EB%A1%9C%EB%82%98+%ED%99%95%EC%A7%84%EC%9E%90+%ED%8F%B4%EB%9E%80%EB%93%9C&tqi=hKGxglp0J1sssDzyOwdsssssszs-168681")
        soup = BeautifulSoup(code, "html.parser")
        info_num = soup.select("div.status_today em")
        # Since info_num (status_today) value is divided into 2 category:
        # 1)cases occurred in domestic + 2)cases occurred among whom entered Korea from abroad
        # so, to get today's current case #, we need to aggregate those two cases as below
        result = int(info_num[0].string) + int(info_num[1].string)
        return result

    ## Crawler for the recent news related to South Korea Covid
    def covid_news_crawler():
        googlenews = GoogleNews()
        googlenews.search('south korea covid')
        title = googlenews.get_texts()
        link = googlenews.get_links()
        output_result = list(zip(title, link))

        # Since 'print' function intrinsically doesn't have feature for saving printed result as variable,
        # I created return_print function to save it as variable to return it at the end
        def return_print(*message):
            io = StringIO()
            print(*message, file=io, end="")
            return io.getvalue()

        output_result = return_print("\n\n".join(["{} : {}".format(*l) for l in output_result]))
        return output_result

    ## Crawler for realted images with keyword 'how to fight covid'
    def covid_image_crawler(image_num=5):
        if not os.path.exists("./covidimage"):
            os.mkdir("./covidimage")

        # Before using chrome for scraping 'images', we need to download the chromedriver
        # which has same version with our chrome
        browser = webdriver.Chrome("/Users/jiyoungkim/Downloads/chromedriver")
        browser.implicitly_wait(3)
        wait = WebDriverWait(browser, 10)

        # For the images, we will scrape the images shown as a result of search keyword "how to fight covid" in google

        browser.get(
            "https://www.google.com/search?q=how+to+fight+covid&tbm=isch&ved=2ahUKEwiIm5DC6aTxAhXsxIsKHbK3AwcQ2-cCegQIABAA&oq=how+to+fight+covid&gs_lcp=CgNpbWcQAzICCAAyAggAMgIIADICCAAyAggAMgIIADICCAAyAggAMgIIADICCAA6BggAEAcQHlDdIlixKWCsLWgAcAB4AIABoAGIAaEJkgEDMC45mAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=NXrOYMisI-yJrwSy7444&bih=739&biw=1440&rlz=1C5CHFA_enKR837KR837")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.islrc a.wXeWr.islib.nfEiy div.bRMDJf.islir img")))
        img = browser.find_elements_by_css_selector("div.islrc a.wXeWr.islib.nfEiy div.bRMDJf.islir img")

        for i in img:
            img_url = i.get_attribute("src")
            req.urlretrieve(img_url, "./covidimage/{}.png".format(img.index(i)))
            if img.index(i) == image_num-1:
                break
        browser.close()


######################################
######## Code - Telegram part ########
######################################

token = "here, input your chatbot api token key you got from botfather(telegram)"
id = "input your chat_id"

bot = telegram.Bot(token)
info_message = '''- To check the number of New Cases(today) : Please input "case" or "number"
- News related to 'COVID' : Please input "news"
- Want to see the Images of "How to fight covid"? : Please input "image"'''
bot.sendMessage(chat_id=id, text=info_message)

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
updater.start_polling()


## Handler function contains the response messages of chatbot based on user's input

def handler(update, context):
    user_text = update.message.text  # keep user's input in as 'user_text' variable

    # 1) Response for the number of today's COVID case in Korea
    if (user_text == "case") or (user_text == "number"):
        covid_case = Crawler.covid_case_crawler()
        bot.send_message(chat_id=id, text="Today's new COVID case in South Korea : {} cases".format(covid_case))
        bot.sendMessage(chat_id=id, text=info_message)
        # our bot automatically sends info_message again to make users be able to check another info

    # 2) Response for the news related to COVID
    elif (user_text == "news"):
        covid_news = Crawler.covid_news_crawler()
        bot.send_message(chat_id=id, text="Below is the Recent News with keyword 'south korea covid' ")
        bot.send_message(chat_id=id, text=covid_news)
        bot.sendMessage(chat_id=id, text=info_message)

    # 3) Image related to COVID (keyword: how to fight covid)
    elif (user_text == "image"):
        bot.send_message(chat_id=id, text="Loading the image...")
        Crawler.covid_image_crawler(image_num=10)

        # Send multiple images(in here, 10 pieces of images) at once using 'for' statement
        photo_list = []
        for i in range(len(os.walk("./covidimage").__next__()[2])):
            photo_list.append(telegram.InputMediaPhoto(open("./covidimage/{}.png".format(i), "rb")))
        bot.sendMediaGroup(chat_id=id, media=photo_list)
        bot.sendMessage(chat_id=id, text=info_message)

    # 4) Error handling (if user was mistyping the word)
    else:
        bot.send_message(chat_id=id, text="Sorry, we didn't understand your word. Please input the correct word again")
        bot.sendMessage(chat_id=id, text=info_message)


echo_handler = MessageHandler(Filters.text, handler)
dispatcher.add_handler(echo_handler)
