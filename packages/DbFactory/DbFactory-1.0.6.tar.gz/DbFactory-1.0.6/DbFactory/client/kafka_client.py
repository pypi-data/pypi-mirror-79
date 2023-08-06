# coding:utf-8
# author caturbhuja
# date   2020/9/7 3:06 下午 
# wechat chending2012
# python pack

# third part pack


# self pack
from .db_base import DbBase, config


class KafkaClient(DbBase):
    def __init__(self, **kwargs):
        self._kwargs = kwargs
        super(KafkaClient, self).__init__(**kwargs)
        self.__init_db_base_args()

    def __init_db_base_args(self):
        """处理kafka基础参数"""
