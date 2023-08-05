
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class PrizeRosterModel(BaseModel):
    def __init__(self, db_connect_key='db_mang_he', sub_table=None, db_transaction=None):
        super(PrizeRosterModel, self).__init__(PrizeRoster, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction

    #方法扩展请继承此类
    
class PrizeRoster:

    def __init__(self):
        super(PrizeRoster, self).__init__()
        self.id = 0  # id
        self.app_id = ""  # app_id
        self.act_id = 0  # act_id
        self.open_id = ""  # open_id
        self.machine_id = 0  # 机台id
        self.machine_name = ""  # 机台名称
        self.machine_price = 0  # 机台价格
        self.prize_id = 0  # 奖品标识
        self.prize_name = ""  # 奖品名称
        self.prize_price = 0  # 奖品价值
        self.prize_pic = ""  # 奖品图片
        self.prize_detail = ""  # 奖品详情图
        self.tag_id = 0  # 奖品标签
        self.award_id = ""  # 奖项标识
        self.award_name = ""  # 奖项名称
        self.user_nick = ""  # 用户昵称
        self.prize_code = ""  # 中奖码
        self.order_status = 0  # 订单状态（0未发货1已发货2不予发货）
        self.is_sku = 0  # 是否有SKU
        self.prize_order_id = 0  # 奖品订单id
        self.prize_order_no = ""  # 奖品订单号
        self.sku_id = ""  # sku_id
        self.properties_name = ""  # sku属性
        self.goods_id = 0  # 商品id
        self.goods_code = ""  # 商品编码
        self.goods_code_list = ""  # 多个sku商品编码
        self.order_no = ""  # 淘宝订单号
        self.frequency_source = 0  # 次数来源（0-购买，1商家配置）
        self.sku_detail = ""  # sku详情
        self.create_date = "1900-01-01 00:00:00"  # 创建时间

    @classmethod
    def get_field_list(self):
        return ['id', 'app_id', 'act_id', 'open_id', 'machine_id', 'machine_name', 'machine_price', 'prize_id', 'prize_name', 'prize_price', 'prize_pic', 'prize_detail', 'tag_id', 'award_id', 'award_name', 'user_nick', 'prize_code', 'order_status', 'is_sku', 'prize_order_id', 'prize_order_no', 'sku_id', 'properties_name', 'goods_id', 'goods_code', 'goods_code_list', 'order_no', 'frequency_source', 'sku_detail', 'create_date']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "prize_roster_tb"
    