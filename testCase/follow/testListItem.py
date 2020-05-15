import unittest
import paramunittest
import readConfig as readConfig
from common.Log import MyLog
from common import common
from common import configHttp

locallistItem_xls = common.get_xls("followCase.xlsx", "listItem")
localConfigHttp = configHttp.ConfigHttp()
localReadConfig = readConfig.ReadConfig()


@paramunittest.parametrized(*locallistItem_xls)
class ListIteme(unittest.TestCase):

    def setParameters(self,case_name, method,token, userId, companyId, channelId, pageIndex,pageSize,result,resultCode,resultMessage):
        self.case_name = str(case_name)
        self.method = str(method)
        self.token = str(token)
        self.userId = str(userId)
        self.companyId = str(companyId)
        self.channelId = str(channelId)
        self.pageIndex = int(pageIndex)
        self.pageSize = int(pageSize)
        self.result = str(result)
        self.resultCode = str(resultCode)
        self.resultMessage = str(resultMessage)
        self.response = None
        self.info = None

    def description(self):
        """

        :return:
        """
        self.case_name= self.case_name

    def setUp(self):
        """

        :return:
        """
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()

    def testListIteme(self):
        """
        test body
        :return:
        """
        # set url
        self.url = common.get_url_from_xml('listItem')
        localConfigHttp.set_url(self.url)

        # set header
        if self.token == '0':
            token = self.login_token
        else:
            token = self.token
        header = {'token': token}
        localConfigHttp.set_headers(header)

        # set param
        data = {'userId': self.userId,
                'companyId': self.companyId,
                'channelId': self.channelId,
                'pageIndex': self.pageIndex,
                'pageSize': self.pageSize}
        localConfigHttp.set_data(data)

        # test interface
        self.response = localConfigHttp.post()

        # check result
        self.checkResult()

    def tearDown(self):
        """

        :return:
        """
        self.log.build_case_line(self.case_name, self.info['resultCode'], self.info['resultMessage'])

    def checkResult(self):
        """
        check test reslt
        :return:
        """
        self.info = self.response.json()
        common.show_return_msg(self.response)

        if self.result == '1':
            self.assertEqual(str(self.info['resultCode']), str(self.resultCode))
            self.assertEqual(str(self.info['resultMessage']),str(self.resultMessage))

