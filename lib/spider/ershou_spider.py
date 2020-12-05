#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 爬取二手房数据的爬虫派生类

import re
import threadpool
from bs4 import BeautifulSoup
from lib.item.ershou import *
from lib.zone.city import get_city
from lib.spider.base_spider import *
from lib.utility.date import *
from lib.utility.path import *
from lib.zone.area import *
from lib.request.request_func import *
from lib.utility.log import *
import lib.utility.version
import bs4
import traceback


class ErShouSpider(BaseSpider):
    def collect_area_ershou_data(self, city_name, area_name, fmt="csv"):
        """
        对于每个板块,获得这个板块下所有二手房的信息
        并且将这些信息写入文件保存
        :param city_name: 城市
        :param area_name: 板块
        :param fmt: 保存文件格式
        :return: None
        """
        district_name = area_dict.get(area_name, "")
        csv_file = self.today_path + "/{0}_{1}.csv".format(district_name, area_name)
        with open(csv_file, "w") as f:
            try:
                # 开始获得需要的板块数据
                ershous = self.get_area_ershou_info(city_name, area_name)
                # 锁定，多线程读写
                if self.mutex.acquire(1):
                    self.total_num += len(ershous)
                    # 释放
                    self.mutex.release()
                if fmt == "csv":
                    for ershou in ershous:
                        # print(date_string + "," + xiaoqu.text())
                        f.write(ershou.text() + "\n")
            except Exception as e:
                print("catch an exception {} when write to file {}".format(e, csv_file))
        print("Finish crawl area: " + area_name + ", save data to : " + csv_file)


    @staticmethod
    def get_area_ershou_info_single(single_ershou_url):
        soup = request_get(single_ershou_url)

        name = soup.find_all("div", "detailHeader VIEWDATA")[0].find_all("h1", "main")[0].text.strip()
        total_price = soup.find_all("span", "total")[0].text
        unit_price = soup.find_all("span", "unitPriceValue")[0].text
        house_age = soup.find_all("div", "houseInfo")[0].find("div", "area").find("div", "subInfo").text.split("年")[0]
        sub_district = soup.find_all("div", "communityName")[0].find("a", "info no_resblock_a").text
        district, area = [temp.text for temp in soup.find_all("div", "areaName")[0].find("span", "info").find_all("a")]

        base_info = {temp.find("span").text.strip(): temp.contents[1].strip() for temp in soup.find_all("div", "base")[0].find_all("li")}
        transaction_info = {temp.find("span").text.strip():
                                temp.contents[1].strip() if type(temp.contents[1]) == bs4.element.NavigableString else temp.find_all("span")[1].text.strip()
                            for temp in soup.find_all("div", "transaction")[0].find_all("li")}

        return ErShou(page_url=single_ershou_url, district=district, area=area, sub_district=sub_district,
                      total_price=total_price, unit_price=unit_price, name=name, house_type=base_info.get("房屋户型", ""),
                      storey=base_info.get("所在楼层", ""), house_area=base_info.get("建筑面积", ""),
                      house_layout=base_info.get("户型结构", ""), building_type=base_info.get("建筑类型", ""),
                      house_orientation=base_info.get("房屋朝向", ""), building_structure=base_info.get("建筑结构", ""),
                      decoration=base_info.get("装修情况", ""), elevator=base_info.get("梯户比例", ""),
                      listing_time=transaction_info.get("挂牌时间", ""), transaction_type=transaction_info.get("交易权属", ""),
                      last_transaction_time=transaction_info.get("上次交易", ""), house_usage=transaction_info.get("房屋用途", ""),
                      house_age=house_age, house_ownership=transaction_info.get("产权所属", ""),
                      mortgage_infomation=transaction_info.get("抵押信息", ""), house_certificates=transaction_info.get("房本备件", ""))


    @staticmethod
    def get_area_ershou_info(city_name, area_name):
        """
        通过爬取页面获得城市指定版块的二手房信息
        :param city_name: 城市
        :param area_name: 版块
        :return: 二手房数据列表
        """
        total_page = 0
        district_name = area_dict.get(area_name, "")
        # 中文区县
        chinese_district = get_chinese_district(district_name)
        # 中文版块
        chinese_area = chinese_area_dict.get(area_name, "")

        ershou_list = list()
        page = 'http://{0}.{1}.com/ershoufang/{2}/'.format(city_name, SPIDER_NAME, area_name)
        print(page)  # 打印版块页面地址
        BaseSpider.random_delay()
        headers = create_headers()
        response = requests.get(page, timeout=10, headers=headers)
        html = response.content
        soup = BeautifulSoup(html, "lxml")

        # 获得总的页数，通过查找总页码的元素信息
        try:
            page_box = soup.find_all('div', class_='page-box')[0]
            matches = re.search('.*"totalPage":(\d+),.*', str(page_box))
            total_page = int(matches.group(1))
        except Exception as e:
            print("\tWarning: only find one page for {0}".format(area_name))
            print(e)

        # 从第一页开始,一直遍历到最后一页
        for num in range(1, total_page + 1):
            page = 'http://{0}.{1}.com/ershoufang/{2}/pg{3}'.format(city_name, SPIDER_NAME, area_name, num)
            try:
                print(page)  # 打印每一页的地址
                BaseSpider.random_delay()
                soup = request_get(page)

                # 获得有小区信息的panel
                house_elements = soup.find_all('li', class_="clear")
                for house_elem in house_elements:
                    try:
                        BaseSpider.random_delay()
                        house_url = house_elem.find("a", "VIEWDATA CLICKDATA maidian-detail")["href"]
                        ershou = ErShouSpider.get_area_ershou_info_single(house_url)
                        ershou_list.append(ershou)
                    except Exception as e:
                        traceback.print_exc()
                        print("catch an exception {}, house_elem {}".format(e, house_elem))
            except Exception as e:
                print(page, e)

        return ershou_list

    def start(self):
        city = get_city()
        self.today_path = create_date_path("{0}/ershou".format(SPIDER_NAME), city, self.date_string)

        t1 = time.time()  # 开始计时

        # 获得城市有多少区列表, district: 区县
        districts = get_districts(city)
        print('City: {0}'.format(city))
        print('Districts: {0}'.format(districts))

        # 获得每个区的板块, area: 板块
        areas = list()
        for district in districts:
            areas_of_district = get_areas(city, district)
            print('{0}: Area list:  {1}'.format(district, areas_of_district))
            # 用list的extend方法,L1.extend(L2)，该方法将参数L2的全部元素添加到L1的尾部
            areas.extend(areas_of_district)
            # 使用一个字典来存储区县和板块的对应关系, 例如{'beicai': 'pudongxinqu', }
            for area in areas_of_district:
                area_dict[area] = district
        print("Area:", areas)
        print("District and areas:", area_dict)

        # 准备线程池用到的参数
        nones = [None for i in range(len(areas))]
        city_list = [city for i in range(len(areas))]
        args = zip(zip(city_list, areas), nones)
        # areas = areas[0: 1]   # For debugging

        # 针对每个板块写一个文件,启动一个线程来操作
        pool_size = thread_pool_size
        pool = threadpool.ThreadPool(pool_size)
        my_requests = threadpool.makeRequests(self.collect_area_ershou_data, args)
        [pool.putRequest(req) for req in my_requests]
        pool.wait()
        pool.dismissWorkers(pool_size, do_join=True)  # 完成后退出

        # 计时结束，统计结果
        t2 = time.time()
        print("Total crawl {0} areas.".format(len(areas)))
        print("Total cost {0} second to crawl {1} data items.".format(t2 - t1, self.total_num))


if __name__ == '__main__':
    pass
