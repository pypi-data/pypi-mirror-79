# -*- coding: utf-8 -*-
from gt_push_sdk.igetui.template.style.INotifyStyle import *
from gt_push_sdk.protobuf import *


class AbstractNotifyStyle(INotifyStyle):
    def __init__(self):
        self.isRing = True
        self.isVibrate = True
        self.isClearable = True

        # Android 8.0 新增字段
        self.channel = "Default"
        self.channelName = "Default"
        self.channelLevel = 3

        actionChainBuilder = gt_req_pb2.ActionChain()
        actionChainBuilder.actionId = 10000
        actionChainBuilder.type = gt_req_pb2.ActionChain.mmsinbox2
        actionChainBuilder.stype = "notification"
        actionChainBuilder.next = 10010
        self.actionChainBuilder = actionChainBuilder
