from re_common.baselibrary.utils.core.requests_core import MsgCode


class MRequest(object):

    def __init__(self, logger=None):
        if logger is None:
            from re_common.baselibrary import MLogger
            logger = MLogger().streamlogger
        self.logger = logger
        self.html = None
        self.resp = None
        self.marks = []
        self.middler_list = [self.status_code_middlerwares, self.end_middlerwares, self.marks_middlerwares]
        self.status_code = None
        self.header = None
        self.refer = None
        self.proxies = None
        self.url = None
        self.params = None
        self.data = None
        self.cookies = None
        self.sn = None
        self.files = None
        self.auth = None
        self.timeout = None
        self.allow_redirects = True
        self.hooks = None
        self.stream = None
        self.verify = None
        self.cert = None
        self.json = None

    def set_marks(self, marks: list):
        """
        设置验证码
        :param marks:
        :return:
        """
        self.marks = marks

    def set_timeout(self, timeout):
        """
        设置超时
        :param timeout:
        :return:
        """
        self.timeout = timeout

    def set_header(self, header):
        """
        设置header
        :return:
        """
        self.header = header
        return self

    def set_refer(self, refer):
        """
        设置header中的refer，每次请求有可能变化
        :return:
        """
        self.refer = refer
        return self

    def set_proxy(self, proxy):
        """
        设置代理
        :return:
        """
        self.proxy = proxy
        return self

    def set_url(self, url):
        """
        设置请求的url
        :return:
        """
        self.url = url
        return self

    def set_params(self, params):
        """
        get 请求参数
        :return:
        """
        self.params = params
        return self

    def set_data(self, data):
        """
        设置请求参数
        :return:
        """
        self.data = data
        return self

    def set_cookie(self, cookie):
        """
        设置cookie
        :return:
        """
        self.cookie = cookie
        return self

    def set_sn(self, sn):
        """
        设置会话
        :return:
        """
        self.sn = sn
        return self

    def builder(self):
        """
        建造成需要的对象用于接下来请求使用
        :return:
        """
        if self.refer != "":
            self.header["refer"] = self.refer

    def get(self):
        """
        get 请求
        :return:
        """
        pass

    def post(self):
        """
        post 请求
        :return:
        """

    def on_request_start(self):
        """
        请求前的钩子函数
        :return:
        """

    def on_request_end(self):
        """
        请求结束的钩子函数
        :return:
        """


    def status_code_middlerwares(self, status_code=200):
        """
        验证返回码
        :return:
        """
        if self.status_code != status_code:
            dicts = {"code": self.status_code,
                     "msg": "status_code err {}".format(self.status_code)}
            return False, dicts
        return True, {}

    def end_middlerwares(self, endstring="</html>"):
        """
        必须以什么结束
        :return:
        """
        if not self.html.endswith(endstring):
            dicts = {"code": MsgCode.END_STRING_ERROR,
                     "msg": "not endswith {}".format(endstring)}
            return False, dicts
        return True, {}

    def have_end_middlerwares(self, havestring="</html>"):
        if not self.html.endswith(havestring):
            dicts = {"code": MsgCode.END_STRING_ERROR,
                     "msg": "not have endswith {}".format(havestring)}
            return False, dicts
        return True, {}

    def marks_middlerwares(self):
        """
        建议至少两个，
        一个是id 防止因为cookie请求到其他的页面
        一个为验证该html关键词，用于改版预测
        :param marks: 一个列表
        :return:
        """
        mark_str = ""
        for mark in self.marks:
            if self.html.find(mark) == -1:
                mark_str = mark_str + mark + ";"

        if mark_str != "":
            dicts = {"code": MsgCode.MARK_ERROR,
                     "msg": "mark Feature err: {}".format(mark_str)}
            return False, dicts
        else:
            return True, {}
