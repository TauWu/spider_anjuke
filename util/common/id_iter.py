# -*- coding: utf-8 -*-

def house_id_iter(data_iter, size):
    while True:
        house_id_list = list()
        for _ in range(0, size):
            try:
                while True:
                    pe_data = next(data_iter)
                    # 忽略已经完成数据获取的房源ID
                    if pe_data[1] != "0":
                        break
            except Exception:
                break
            else:
                house_id_list.append(pe_data[0])
        if len(house_id_list) == 0:
            break
        yield house_id_list