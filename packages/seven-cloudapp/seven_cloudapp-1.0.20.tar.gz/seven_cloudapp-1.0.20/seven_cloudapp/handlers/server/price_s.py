# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2020-06-22 10:30:00
@LastEditTime: 2020-08-17 12:25:04
@LastEditors: HuangJingCan
@Description: 价格档位
"""
from seven_cloudapp.handlers.seven_base import *
from seven_cloudapp.models.seven_model import PageInfo
from seven_cloudapp.models.enum import *
from seven_cloudapp.models.db_models.price.price_gear_model import *
from seven_cloudapp.models.db_models.app.app_info_model import *
from seven_cloudapp.models.db_models.act.act_info_model import *
from seven_cloudapp.models.db_models.machine.machine_info_model import *

import decimal


class PriceHandler(SevenBaseHandler):
    """
    @description: 保存价格档位
    """
    @filter_check_params("act_id,price")
    def get_async(self):
        """
        @description: 保存价格档位
        @param price：价格
        @return: reponse_json_success
        @last_editors: HuangJianYi
        """
        app_id = self.get_param("app_id")
        open_id = self.get_taobao_param().open_id
        price_gear_id = int(self.get_param("price_gear_id", "0"))
        act_id = int(self.get_param("act_id", "0"))
        price = self.get_param("price")
        goods_id = self.get_param("goods_id", "")
        sku_id = self.get_param("sku_id", "")
        if act_id <= 0:
            return self.reponse_json_error_params()
        price_gear = None
        act_info_model = ActInfoModel()
        price_gear_model = PriceGearModel()
        if price_gear_id > 0:
            price_gear = price_gear_model.get_entity_by_id(price_gear_id)

        is_add = False
        if not price_gear:
            is_add = True
            price_gear = PriceGear()

        try:
            price = decimal.Decimal(price)
        except Exception as ex:
            return self.reponse_json_error("ParamError", "参数price类型错误")

        if goods_id != "":
            condition = "act_id!=%s and goods_id=%s"
            price_gear_goodsid = price_gear_model.get_entity(condition, params=[act_id, goods_id])
            if price_gear_goodsid:
                act_info = act_info_model.get_entity("id=%s", params=[price_gear_goodsid.act_id])
                actName = act_info.act_name if act_info else ""
                return self.reponse_json_error("Error", f"此商品ID已关联活动{actName},无法使用")

        old_price_gear = price_gear
        price_gear.act_id = act_id
        price_gear.app_id = app_id
        price_gear.price = price
        price_gear.goods_id = goods_id
        price_gear.sku_id = sku_id
        price_gear.effective_date = self.get_now_datetime()
        price_gear.modify_date = self.get_now_datetime()
        if is_add:
            if sku_id != "":
                price_gear_goodsid_skuid = price_gear_model.get_entity("sku_id=%s", params=[sku_id])
                if price_gear_goodsid_skuid:
                    return self.reponse_json_error("Error", f"当前SKUID已绑定价格档位,请更换")
            price_gear.effectiveTime = self.get_now_datetime()
            price_gear.id = price_gear_model.add_entity(price_gear)
            # 记录日志
            self.create_operation_log(OperationType.add.value, price_gear.__str__(), "PriceHandler", None, self.json_dumps(price_gear.__dict__))
        else:
            if sku_id != "":
                price_gear_goodsid_skuid = price_gear_model.get_entity("id!=%s and sku_id=%s", params=[price_gear.id, sku_id])
                if price_gear_goodsid_skuid:
                    return self.reponse_json_error("Error", f"当前SKUID已绑定价格档位,请更换")
            price_gear_model.update_entity(price_gear)
            self.create_operation_log(OperationType.update.value, price_gear.__str__(), "PriceHandler", self.json_dumps(old_price_gear.__dict__), self.json_dumps(price_gear.__dict__))

        self.reponse_json_success(price_gear.id)


class PriceListHandler(SevenBaseHandler):
    """
    @description: 价格档位信息
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description: 获取价格档位列表
        @param act_id：活动id
        @param page_index：页索引
        @param page_size：页大小
        @return: list
        @last_editors: HuangJianYi
        """
        act_id = int(self.get_param("act_id", "0"))
        page_index = int(self.get_param("page_index", 0))
        page_size = int(self.get_param("page_size", 10))

        if act_id <= 0:
            return self.reponse_json_error_params()

        page_list, total = PriceGearModel().get_page_list("*", page_index, page_size, "act_id=%s and is_del=0", "", "id desc", act_id)

        new_list = []
        for page in page_list:
            price_gear = {}
            price_gear["id"] = page.id
            price_gear["price"] = page.price
            price_gear["goods_id"] = page.goods_id
            price_gear["sku_id"] = page.sku_id
            new_list.append(price_gear)

        page_info = PageInfo(page_index, page_size, total, new_list)

        self.reponse_json_success(page_info.__dict__)


class PriceListRecoverHandler(SevenBaseHandler):
    """
    @description: 价格档位回收站
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description: 价格档位回收站
        @param act_id：活动id
        @param page_index：页索引
        @param page_size：页大小
        @return: list
        @last_editors: HuangJianYi
        """
        act_id = int(self.get_param("act_id", "0"))
        page_index = int(self.get_param("page_index", 0))
        page_size = int(self.get_param("page_size", 10))

        if act_id <= 0:
            return self.reponse_json_error_params()

        page_list, total = PriceGearModel().get_page_list("*", page_index, page_size, "act_id=%s and is_del=1", "", "id desc", act_id)

        new_list = []
        for page in page_list:
            price_gear = {}
            price_gear["id"] = page.id
            price_gear["price"] = page.price
            price_gear["goods_id"] = page.goods_id
            price_gear["sku_id"] = page.sku_id
            new_list.append(price_gear)

        page_info = PageInfo(page_index, page_size, total, new_list)

        self.reponse_json_success(page_info.__dict__)


class PriceStatusHandler(SevenBaseHandler):
    """
    @description: 价格档位删除和恢复
    """
    @filter_check_params("price_gear_id")
    def get_async(self):
        """
        @description: 删除价格档位
        @param price_gear_id：价格档位id
        @return: reponse_json_success
        @last_editors: HuangJianYi
        """
        open_id = self.get_taobao_param().open_id
        app_id = self.get_param("app_id")
        price_gear_id = int(self.get_param("price_gear_id", "0"))
        status = int(self.get_param("status", "0"))
        if status > 0:
            status = 1
        if price_gear_id <= 0:
            return self.reponse_json_error_params()
        price_gear_model = PriceGearModel()
        # machine_info_model = MachineInfoModel()
        # machine_info = machine_info_model.get_entity("app_id=%s and price_gears_id=%s", params=[app_id,price_gear_id])
        # if machine_info:
        #     return self.reponse_json_error("Error", "当前档位已关联中盒,请取消关联再删除")
        price_gear_model.update_table(f"is_del={status},goods_id='',sku_id=''", "id=%s", price_gear_id)
        if status == 1:
            self.create_operation_log(OperationType.delete.value, "price_gear_tb", "PriceStatusHandler", None, price_gear_id)

        self.reponse_json_success()