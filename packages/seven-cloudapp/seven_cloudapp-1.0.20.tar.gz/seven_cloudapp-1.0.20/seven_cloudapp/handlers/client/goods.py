# -*- coding: utf-8 -*-
"""
@Author: CaiYouBin
@Date: 2020-05-28 14:50:27
@LastEditTime: 2020-09-07 15:17:37
@LastEditors: HuangJingCan
@Description: 
"""

from seven_cloudapp.handlers.seven_base import *
from seven_cloudapp.handlers.top_base import *

from seven_cloudapp.models.db_models.prize.prize_roster_model import *
from seven_cloudapp.models.db_models.app.app_info_model import *


class SubmitSkuHandler(SevenBaseHandler):
    """
    @description: 提交SKU
    @param {type} 
    @return: 
    @last_editors: CaiYouBin
    """
    @filter_check_params("sku_id")
    def get_async(self):
        app_id = self.get_taobao_param().source_app_id
        open_id = self.get_taobao_param().open_id

        user_prize_id = int(self.get_param("user_prize_id"))
        properties_name = self.get_param("properties_name")
        sku_id = self.get_param("sku_id")

        prize_roster_model = PrizeRosterModel()
        prize_roster = prize_roster_model.get_entity("id=%s", params=user_prize_id)
        if not prize_roster:
            return self.reponse_json_error("NoUserPrize", "对不起，找不到该奖品")
        if prize_roster.is_sku > 0:
            goods_code_list = json.loads(prize_roster.goods_code_list)
            goods_codes = [i for i in goods_code_list if str(i["sku_id"]) == sku_id]

            prize_roster.sku_id = sku_id
            prize_roster.properties_name = properties_name
            if goods_codes and ("goods_code" in goods_codes[0].keys()):
                prize_roster.goods_code = goods_codes[0]["goods_code"]

        prize_roster_model.update_entity(prize_roster)

        self.reponse_json_success()


class SkuInfoHandler(TopBaseHandler):
    """
    @description: 获取SKU信息
    @param {type} 
    @return: 
    @last_editors: HuangJingCan
    """
    def get_async(self):
        num_iids = self.get_param("num_iids")

        access_token = ""
        app_info = AppInfoModel().get_entity("app_id=%s", params=self.get_taobao_param().source_app_id)
        if app_info:
            access_token = app_info.access_token

        self.get_sku_info(num_iids, access_token)


class GoodsListHandler(TopBaseHandler):
    """
    @description: 导入商品列表(请求top接口)
    """
    def get_async(self):
        """
        @description: 导入商品列表(请求top接口)
        @param {type} 
        @return: 
        @last_editors: CaiYouBin
        """
        page_index = int(self.get_param("page_index", 0))
        page_size = self.get_param("page_size", 200)
        app_id = self.get_taobao_param().source_app_id

        access_token = ""
        app_info = AppInfoModel().get_entity("app_id=%s", params=app_id)
        if app_info:
            access_token = app_info.access_token

        self.get_goods_list_client(page_index, page_size, access_token)