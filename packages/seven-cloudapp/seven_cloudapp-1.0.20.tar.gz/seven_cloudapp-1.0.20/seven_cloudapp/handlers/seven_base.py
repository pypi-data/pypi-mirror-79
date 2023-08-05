# -*- coding: utf-8 -*-
"""
@Author: HuangJingCan
@Date: 2020-05-12 20:11:48
@LastEditTime: 2020-09-07 17:17:25
@LastEditors: HuangJingCan
@Description: SevenBaseHandler
"""
import ast
import random
from seven_framework.web_tornado.base_handler.base_api_handler import *
from seven_framework.redis import *

from seven_cloudapp.models.taobao_model import *
from seven_cloudapp.models.db_models.operation.operation_log_model import *
from seven_cloudapp.models.db_models.user.user_info_model import *


class SevenBaseHandler(BaseApiHandler):
    """
    @description: 
    @param {type} 
    @return: 
    @last_editors: HuangJingCan
    """
    def options_async(self):
        self.reponse_json_success()

    def check_xsrf_cookie(self):
        return

    def json_dumps(self, rep_dic):
        """
        @description: 用于将字典形式的数据转化为字符串
        @param rep_dic：字典对象
        @return: str
        @last_editors: HuangJingCan
        """
        if hasattr(rep_dic, '__dict__'):
            rep_dic = rep_dic.__dict__
        return json.dumps(rep_dic, ensure_ascii=False, cls=JsonEncoder)

    def reponse_custom(self, rep_dic):
        """
        @description: 输出公共json模型
        @param rep_dic: 字典类型数据
        @return: 将dumps后的数据字符串返回给客户端
        @last_editors: HuangJingCan
        """
        self.http_reponse(self.json_dumps(rep_dic))

    def reponse_common(self, success=True, data=None, error_code="", error_message=""):
        """
        @description: 输出公共json模型
        @param success: 布尔值，表示本次调用是否成功
        @param data: 类型不限，调用成功（success为true）时，服务端返回的数据
        @param errorCode: 字符串，调用失败（success为false）时，服务端返回的错误码
        @param errorMessage: 字符串，调用失败（success为false）时，服务端返回的错误信息
        @return: 将dumps后的数据字符串返回给客户端
        @last_editors: HuangJingCan
        """
        if hasattr(data, '__dict__'):
            data = data.__dict__
        template_value = {}
        template_value['success'] = success
        template_value['data'] = data
        template_value['error_code'] = error_code
        template_value['error_message'] = error_message

        rep_dic = {}
        rep_dic['success'] = True
        rep_dic['data'] = template_value

        self.http_reponse(self.json_dumps(rep_dic))

    def reponse_json_success(self, data=None):
        """
        @description: 通用成功返回json结构
        @param data: 返回结果对象，即为数组，字典
        @return: 将dumps后的数据字符串返回给客户端
        @last_editors: HuangJingCan
        """
        self.reponse_common(data=data)

    def reponse_json_error(self, error_code="", error_message=""):
        """
        @description: 通用错误返回json结构
        @param errorCode: 字符串，调用失败（success为false）时，服务端返回的错误码
        @param errorMessage: 字符串，调用失败（success为false）时，服务端返回的错误信息
        @return: 将dumps后的数据字符串返回给客户端
        @last_editors: HuangJingCan
        """
        self.reponse_common(False, None, error_code, error_message)

    def reponse_json_error_params(self):
        """
        @description: 通用参数错误返回json结构
        @param desc: 返错误描述
        @return: 将dumps后的数据字符串返回给客户端
        @last_editors: ChenXiaolei
        """
        self.reponse_common(False, None, "params error", "参数错误")

    def redis_init(self, db=None):
        """
        @description: redis初始化
        @return: redis_cli
        @last_editors: HuangJingCan
        """
        host = config.get_value("redis")["host"]
        port = config.get_value("redis")["port"]
        if not db:
            db = config.get_value("redis")["db"]
        password = config.get_value("redis")["password"]
        redis_cli = RedisHelper.redis_init(host, port, db, password)
        return redis_cli

    def get_taobao_param(self):
        """
        @description: 获取淘宝上下文参数
        @param {type} 
        @return: 
        @last_editors: HuangJingCan
        """
        app_key = self.get_param("app_key")
        user_nick = self.get_param("user_nick")
        open_id = self.get_param("open_id")
        env = self.get_param("env")
        mini_app_id = self.get_param("mini_app_id")
        access_token = self.get_param("access_token")
        sign = self.get_param("sign")
        mix_nick = self.get_param("mix_nick")
        user_id = self.get_param("user_id")
        main_user_id = self.get_param("main_user_id")
        source_app_id = self.get_param("source_app_id")
        request_id = self.get_param("request_id")

        #region 指定测试账号和小程序,用于在IDE上测试(前端通过source_app_id关联数据,后端通过user_nick关联数据)
        if source_app_id == config.get_value("client_template_id"):
            #前端（在IDE上返回前端模板id，在千牛上返回正确的id）
            source_app_id = config.get_value("test_source_app_id")
        if source_app_id == "":
            #后端（在IDE上返回空，在千牛上返回后端模板ids）
            source_app_id = config.get_value("test_source_app_id")
            user_nick = config.get_value("test_user_nick")
            open_id = config.get_value("test_open_id")
        #endregion

        info = TaoBaoParam()
        info.app_key = app_key
        info.user_nick = user_nick
        info.open_id = open_id
        info.env = env
        info.mini_app_id = mini_app_id
        info.access_token = access_token
        info.sign = sign
        info.mix_nick = mix_nick
        info.user_id = user_id
        info.main_user_id = main_user_id
        info.source_app_id = source_app_id
        info.request_id = request_id

        return info

    def create_order_id(self, ran=5):
        """
        @description: 生成订单号
        @param ran：随机数位数，默认5位随机数（0-5）
        @return: 25位的订单号
        @last_editors: HuangJingCan
        """
        ran_num = ""
        if ran == 1:
            ran_num = random.randint(0, 9)
        elif ran == 2:
            ran_num = random.randint(10, 99)
        elif ran == 3:
            ran_num = random.randint(100, 999)
        elif ran == 4:
            ran_num = random.randint(1000, 9999)
        elif ran == 5:
            ran_num = random.randint(10000, 99999)
        # cur_time = TimeHelper.get_now_format_time('%Y%m%d%H%M%S%f')
        cur_time = TimeHelper.get_now_timestamp(True)
        order_id = str(cur_time) + str(ran_num)
        return order_id

    def get_now_datetime(self):
        """
        @description: 获取当前时间加8小时
        @return: str
        @last_editors: HuangJingCan
        """
        return TimeHelper.add_hours_by_format_time(hour=8)

    def create_operation_log(self, operation_type=1, model_name="", handler_name="", detail=None, update_detail=None):
        """
        @description: 创建操作日志
        @param operation_type：操作类型：1-add，2-update，3-delete
        @param model_name：模块或表名称
        @param handler_name：handler名称
        @param detail：当前信息
        @param update_detail：更新之后的信息
        @return: 
        @last_editors: HuangJingCan
        """
        operation_log = OperationLog()
        operation_log_model = OperationLogModel()

        operation_log.user_nick = self.get_taobao_param().user_nick
        operation_log.app_id = self.get_taobao_param().source_app_id
        operation_log.act_id = int(self.get_param("act_id", 0))
        operation_log.open_id = self.get_taobao_param().open_id
        operation_log.request_params = self.request_params
        operation_log.method = self.request.method
        operation_log.protocol = self.request.protocol
        operation_log.request_host = self.request.host
        operation_log.request_uri = self.request.uri
        operation_log.remote_ip = self.get_remote_ip()
        operation_log.create_date = TimeHelper.get_now_format_time()
        operation_log.operation_type = operation_type
        operation_log.model_name = model_name
        operation_log.handler_name = handler_name
        operation_log.detail = detail
        operation_log.update_detail = update_detail

        if isinstance(operation_log.request_params, dict):
            operation_log.request_params = self.json_dumps(operation_log.request_params)
        if isinstance(detail, dict):
            operation_log.detail = self.json_dumps(detail)
        if isinstance(update_detail, dict):
            operation_log.update_detail = self.json_dumps(update_detail)

        operation_log_model.add_entity(operation_log)

    def get_default_user(self, act_id):
        """
        @description: 默认用户信息
        @param {type} 
        @return: 
        @last_editors: CaiYouBin
        """
        open_id = self.get_taobao_param().open_id
        app_id = self.get_taobao_param().source_app_id

        user_info = UserInfo()
        user_info.open_id = open_id
        user_info.act_id = act_id
        user_info.user_nick = ""
        user_info.avatar = ""
        user_info.is_auth = 0
        user_info.app_id = app_id
        user_info.is_new = 1
        user_info.pay_price = 0
        user_info.pay_num = 0
        user_info.surplus_integral = 0
        user_info.user_state = 0
        user_info.create_date = self.get_now_datetime()
        user_info.modify_date = self.get_now_datetime()

        return user_info

    def get_is_test(self):
        """
        @description: 判断是否本地测试
        @return: str
        @last_editors: HuangJianYi
        """
        if self.get_taobao_param().env != "online":
            return True
        return False

    def check_post(self, redis_key, expire=1):
        """
         @description: 请求太频繁校验
         @return: str
         @last_editors: HuangJianYi
         """
        post_value = self.redis_init().get(redis_key)
        if post_value == None:
            self.redis_init().set(redis_key, 10, ex=expire)
            return True
        return False

    def check_lpush(self, queue_name, value, limitNum=100):
        """
         @description: 入队列校验
         @return: str
         @last_editors: HuangJianYi
         """
        list_len = self.redis_init().llen(queue_name)
        if int(list_len) >= int(limitNum):
            return False
        self.redis_init().lpush(queue_name, json.dumps(value))
        return True

    def lpop(self, queue_name):
        """
         @description: 出队列
         @return: str
         @last_editors: HuangJianYi
         """
        result = self.redis_init().lpop(queue_name)
        return result

    def acquire_lock(self, lock_name, acquire_time=10, time_out=5):
        """
        @description: 获取一个分布式锁
        @param lock_name：锁定名称
        @param acquire_time: 客户端等待获取锁的时间
        @param time_out: 锁的超时时间
        @return bool
        @last_editors: HuangJianYi
        """
        identifier = str(uuid.uuid4())
        end = time.time() + acquire_time
        lock = "lock:" + lock_name
        while time.time() < end:
            if self.redis_init().setnx(lock, identifier):
                # 给锁设置超时时间, 防止进程崩溃导致其他进程无法获取锁
                self.redis_init().expire(lock, time_out)
                return identifier
            if not self.redis_init().ttl(lock):
                self.redis_init().expire(lock, time_out)
            time.sleep(0.001)
        return False

    def release_lock(self, lock_name, identifier):
        """
        @description: 释放一个锁
        @param lock_name：锁定名称
        @param identifier: identifier
        @return bool
        @last_editors: HuangJianYi
        """
        lock = "lock:" + lock_name
        pip = self.redis_init().pipeline(True)
        while True:
            try:
                pip.watch(lock)
                lock_value = self.redis_init().get(lock)
                if not lock_value:
                    return True
                if lock_value.decode() == identifier:
                    pip.multi()
                    pip.delete(lock)
                    pip.execute()
                    return True
                pip.unwatch()
                break
            except redis.excetions.WacthcError:
                pass
        return False

    def random_weight(self, random_prize_dict_list):
        """
        @description:  根据权重算法获取商品
        @param {type} 
        @return: 
        @last_editors: HuangJianYi
        """
        total = sum(random_prize_dict_list.values())  # 权重求和
        ra = random.uniform(0, total)  # 在0与权重和之前获取一个随机数
        curr_sum = 0
        ret = None
        keys = random_prize_dict_list.keys()
        for k in keys:
            curr_sum += random_prize_dict_list[k]  # 在遍历中，累加当前权重值
            if ra <= curr_sum:  # 当随机数<=当前权重和时，返回权重key
                ret = k
                break
        return ret