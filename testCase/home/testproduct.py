import unittest
import paramunittest
import readConfig as readConfig
from common import Log as Log
from common import common
from common import configHttp as ConfigHttp

homePageTJ_xls = common.get_xls("PageTJCase.xlsx", "homePageTJ")
localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
#info = {}


@paramunittest.parametrized(*homePageTJ_xls)
class Login(unittest.TestCase):
    def setParameters(self, case_name, method, mid, cityCode, latitude,longitude,debug, mini_h5_function,result, state, message):
        """
        set params
        :param case_name:
        :param method:
        :param mid:
        :param cityCode:
        :param latitude:
        :param longitude:
        :param debug:
        :param mini_h5_function:
        :param result:
        :param state:
        :param message:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.mid = str(mid)
        self.cityCode = str(cityCode)
        self.latitude = str(latitude)
        self.longitude = str(longitude)
        self.debug = str(debug)
        self.mini_h5_function = str(mini_h5_function)
        self.result = str(result)
        self.state = str(state)
        self.message = str(message)
        self.return_json = None
        self.info = None

    def description(self):
        """
        test report description
        :return:
        """
        self.case_name

    def setUp(self):
        """

        :return:
        """
        self.log = Log.MyLog.get_log()
        self.logger = self.log.get_logger()
        print(self.case_name+"测试开始前准备")

    def testPageTJ(self):
        """
        test body
        :return:
        """
        # set url
        self.url = common.get_url_from_xml('homePageTJ')
        configHttp.set_url(self.url)
        print("第一步：设置url  "+self.url)

        # get visitor token
        '''if self.token == '0':
            token = localReadConfig.get_headers("token_v")
        elif self.token == '1':
            token = None

        # set headers
        header = {"token": str(token)}
        configHttp.set_headers(header)
        print("第二步：设置header(token等)")'''

        # set params
        data = {"mid": self.mid, "cityCode": self.cityCode,"latitude": self.latitude,
                "longitude": self.longitude,"debug": self.debug,"mini_h5_function": self.mini_h5_function
                }
        configHttp.set_data(data)
        print("第三步：设置发送请求的参数")

        # test interface
        self.return_json = configHttp.post()
        method = str(self.return_json.request)[int(str(self.return_json.request).find('['))+1:int(str(self.return_json.request).find(']'))]
        print("第四步：发送请求\n\t\t请求方法："+method)

        # check result
        self.checkResult()
        print("第五步：检查结果")

    def tearDown(self):
        """

        :return:
        """
        info = self.info
        if info['state'] == 0:
            # get uer token
            token_u = common.get_value_from_return_json(info, 'member', 'token')
            # set user token to config file
            localReadConfig.set_headers("TOKEN_U", token_u)
        else:
            pass
        self.log.build_case_line(self.case_name, self.info['state'], self.info['message'])
        print("测试结束，输出log完结\n\n")

    def checkResult(self):
        """
        check test result
        :return:
        """
        self.info = self.return_json.json()
        # show return message
        common.show_return_msg(self.return_json)

        if self.result == '0':
            email = common.get_value_from_return_json(self.info, 'member', 'email')
            self.assertEqual(self.info['state'], self.state)
            self.assertEqual(self.info['message'], self.message)
            self.assertEqual(email, self.email)

        if self.result == '1':
            self.assertEqual(self.info['state'], self.state)
            self.assertEqual(self.info['message'], self.message)
