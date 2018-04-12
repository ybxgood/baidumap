# -*- coding:utf-8 -*-
import pymysql
import traceback
from functools import partial
from multiprocessing import Pool, cpu_count

import requests

from location import isInBound, get_boundaries
from dataHandle import DataHandle

mysql = DataHandle()


def get_task_list(corner, delta_y=0.05, delta_x=0.05):
    '''
    将大矩形区域划分为长delta_x,宽为delta_y的小矩形
    :param corner:
    :param delta_y:
    :param delta_x:
    :return:
    '''
    task_list = []
    j = 0
    while True:
        loc1_y = float(corner['lower_left_corner']['lat']) + j * delta_y
        if loc1_y >= float(corner['upper_right_corner']['lat']):
            break
        if float(corner['lower_left_corner']['lat']) + (j + 1) * delta_y > float(corner['upper_right_corner']['lat']):
            loc2_y = float(corner['upper_right_corner']['lat'])
        else:
            loc2_y = float(corner['lower_left_corner']
                           ['lat']) + (j + 1) * delta_y
        i = 0
        while True:
            loc1_x = float(corner['lower_left_corner']['lng']) + i * delta_x
            if loc1_x >= float(corner['upper_right_corner']['lng']):
                break
            if float(corner['lower_left_corner']['lng']) + (i + 1) * delta_x > float(
                    corner['upper_right_corner']['lng']):
                loc2_x = float(corner['upper_right_corner']['lng'])
            else:
                loc2_x = float(corner['lower_left_corner']
                               ['lng']) + (i + 1) * delta_x
            bounds = (loc1_y, loc1_x, loc2_y, loc2_x)
            task_list.append(bounds)
            i += 1
        j += 1
    return task_list


def get_data(bounds, keyword, boundary):
    # 矩形区域检索
    params = {
        "ak": "***********************",  # 填写秘钥
        "bounds": "%f,%f,%f,%f" % tuple(bounds),
        "output": "json",
        "page_num": 0,
        "page_size": 20,
        "query": keyword
    }
    url = "http://api.map.baidu.com/place/v2/search"
    while True:
        req = requests.get(url, params=params)
        req.encoding = "utf-8"
        if not req.text:
            continue
        json_data = req.json()
        results = json_data.get('results')
        if results:
            data = []
            for result in results:
                aname = result.get('name')
                location = result.get('location')
                if location:
                    lat = location.get('lat')
                    lng = location.get('lng')
                    point = {'lat': lat, 'lng': lng}
                else:
                    continue
                address = result.get('address')
                telephone = result.get('telephone', '')
                uid = result.get('uid')
                print(aname)
                # 保存区域内检索结果
                if isInBound(point, boundary):
                    data.append(
                        (uid, aname, lng, lat, address, telephone, keyword))
            if data:
                mysql.save_data(data)
            params['page_num'] += 1
        else:
            break


def main(keyword, city, delta_y=0.05, delta_x=0.05):

    boundaries = get_boundaries(city)
    corner = boundaries['corner']
    boundary = boundaries['boundary']
    task_list = get_task_list(corner, delta_y, delta_x)
    task_func = partial(get_data, keyword=keyword, boundary=boundary)
    pool = Pool(cpu_count())
    pool.map(task_func, task_list)


if __name__ == '__main__':
    main('加油站', '新余市')  # ”加油站“：keyword
