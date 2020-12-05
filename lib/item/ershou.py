#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 二手房信息的数据结构


class ErShou(object):
    def __init__(self, page_url, district, area, sub_district, total_price, unit_price, name, house_type, storey,
                 house_area, house_layout, building_type, house_orientation, building_structure, decoration, elevator,
                 listing_time, transaction_type,last_transaction_time, house_usage, house_age, house_ownership,
                 mortgage_infomation, house_certificates):
        self.page_url = page_url
        self.id = page_url.strip().split('/')[-1].split('.')[0]
        self.city = page_url.strip().split('/')[2].split('.')[0]
        self.district = district
        self.area = area
        self.sub_district = sub_district
        self.total_price = total_price
        self.unit_price = unit_price
        self.name = name
        self.house_type = house_type
        self.storey = storey
        self.house_area = house_area
        self.house_layout = house_layout
        self.building_type = building_type
        self.house_orientation = house_orientation
        self.building_structure = building_structure
        self.decoration = decoration
        self.elevator = elevator
        self.listing_time = listing_time
        self.transaction_type = transaction_type
        self.last_transaction_time = last_transaction_time
        self.house_usage = house_usage
        self.house_age = house_age
        self.house_ownership = house_ownership
        self.mortgage_infomation = mortgage_infomation
        self.house_certificates = house_certificates


    def text(self):
        return '\t'.join([self.page_url, self.id, self.city, self.district, self.area, self.sub_district, self.total_price,
                          self.unit_price, self.name, self.house_type, self.storey, self.house_area, self.house_layout,
                          self.building_type, self.house_orientation, self.building_structure, self.decoration, self.elevator,
                          self.listing_time, self.transaction_type, self.last_transaction_time, self.house_usage, self.house_age,
                          self.house_ownership, self.mortgage_infomation, self.house_certificates])

    def str(self):
        return self.__dict__