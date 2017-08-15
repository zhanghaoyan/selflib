#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from django.utils.safestring import mark_safe

def page(current_click_page,data,per_page_display_data_num=10,max_link_num=11,urlstr="/?p=",classstr="",activeclass=""):
    """
    这个函数用于在django中对数据切片并返回切片数据结果和链接字符串
    :param current_click_page: 当前点击的页面页码
    :param data: 用于切片的所有数据
    :param per_page_display_data_num: 每页上显示的数据条数
    :param max_link_num: 页面上最多显示的页码个数
    :param urlstr: 生成的链接字符串中的url
    :param classstr: 每个非当前点击的页码的css字符串
    :param activeclass: 当前点击的页码的css字符串
    :return: 返回切片后的数据和安全声明后的链接字符串元组
    """
    current_click_page = int(current_click_page)
    data_length = len(data)
    link_count, tag = divmod(data_length, per_page_display_data_num)
    if tag:
        link_count += 1
    if data_length >= per_page_display_data_num * max_link_num:
        link_num = max_link_num
        if current_click_page <= (link_num + 1)/2:
            link_start = 1
            link_end = link_num + 1
        elif current_click_page > link_count - int((link_num + 1)/2):
            link_start = link_count - link_num + 1
            link_end = link_count + 1
        else:
            link_start = current_click_page - int((link_num - 1)/2)
            link_end = current_click_page + int((link_num - 1)/2) + 1
    else:
        link_num,last = divmod(data_length,per_page_display_data_num)
        if last:
            link_num += 1
        link_start = 1
        link_end = link_start + link_num
    display_start_data_pos = (current_click_page - 1) * per_page_display_data_num
    display_end_data_pos = current_click_page * per_page_display_data_num
    display_data = data[display_start_data_pos:display_end_data_pos]
    link_list = []
    firstpage = '<li><a href="%s1">第一页</a></li>' %urlstr
    link_list.append(firstpage)
    if current_click_page != 1:
        tmp = '<li><a href="%s%s">上一页</a></li>' %(urlstr,(current_click_page - 1))
    else:
        tmp = '<li><a style="background-color: #eee;">上一页</a></li>'
    link_list.append(tmp)
    for item in range(link_start,link_end):
        if item == current_click_page:
            tmp = '<li><a href="%s%s" class="%s">%s </a></li>' %(urlstr,item,activeclass,item)
        else:
            tmp = '<li><a href="%s%s">%s <span class="%s"></span></a></li>'%(urlstr,item,item,classstr)
        link_list.append(tmp)
    if link_end - 1 == current_click_page:
        tmp = '<li><a style="background-color: #eee;">下一页</a></li>'
    else:
        tmp = '<li><a href="%s%s">下一页</a></li>' %(urlstr,(current_click_page + 1))
    link_list.append(tmp)
    tmp = '<li><a href="%s%s">最后一页</a></li>' % (urlstr,link_count)
    link_list.append(tmp)
    link_str = "".join(link_list)
    link_str = mark_safe(link_str)
    # print("current_click_page:%s data_length:%s link_num:%s link_count:%s link_start:%s link_end:%s " %(current_click_page,data_length,link_num,link_count,link_start,link_end))
    return display_data,link_str