import re
import threadpool
from bs4 import BeautifulSoup
from lib.item.ershou import *
from lib.zone.city import get_city
from lib.spider.base_spider import *
from lib.utility.date import *
from lib.utility.path import *
from lib.zone.area import *
from lib.request.proxy import *
from lib.utility.log import *
import lib.utility.version
import bs4
import traceback

sess = requests.Session()

def request_get(url, referer="http://www.{0}.com".format(SPIDER_NAME)):
    # proxy = ProxyIp.get_proxy_ip()
    headers = create_headers(referer)
    response = sess.get(url, timeout=10, headers=headers, proxies=None)
    html = response.content
    return BeautifulSoup(html, "lxml")