import json
from TDhelper.network.http.REST_HTTP import GET, POST
class RPC:
    '''
        RPC
    '''
    def __init__(self,service_center_uri, secret):
        '''
            初始化
            - params:
            -   service_center_uri:<string>, 服务中心获取API接口URI.
            -   secret: <string>, 访问密钥
        '''
        self._access_token= secret
        self._sc_uri= service_center_uri
        self._apisTable= {}

    def _getApi(self, service, method):
        if service not in self._apisTable:
            # 远程获取
            m_heads= {"api-token": self._access_token}
            status, body= GET(uri= self._sc_uri+"?key="+service+"&method="+method,time_out=15, http_headers= m_heads)
            if status==200:
                self._apisTable[service]=json.loads(str(body, encoding='utf-8'))
        # 从本地获取API配置
        if service in self._apisTable:
            if self._apisTable[service]['state']==200:
                return True, self._apisTable[service]['msg']
            else:
                return False, self._apisTable[service]['msg']
        else:
            return False, "can't found %s api." % service

    def call(self, service, method, **kwargs):
        state, ret= self._getApi(service, method)
        if state:
            try:
                m_uri= ret['uri']
                m_params= ret['params']
                m_method= ret['method']
                params_data= ''
                m_count= 0
                for param in m_params:
                    if param['key'] in kwargs:
                        params_data+= param['key']+'='+ str(kwargs[param['key']])
                    else:
                        params_data+= param['key']+'='+ param['defaultValue']
                    m_count+=1
                    if m_count < len(kwargs):
                        params_data+="&"
                try:
                    if m_method== u"GET":
                        m_uri+= "?"+ params_data
                        return GET(m_uri,time_out= 15)
                    elif m_method== u"POST":
                        return POST(m_uri, bytes(params_data, encoding= 'utf-8'), time_out= 15)
                    elif m_method== u"PUT":
                        # 还没有写PUT方法
                        raise Exception('urllib PUT方法还没写.')
                    elif m_method== u"DELETE":
                        # 还没有写DELETE方法
                        raise Exception("urllib delete 方法还没写.")
                    else:
                        raise Exception('restful method is error.')
                except Exception as e:
                    return e
            except Exception as e:
                raise e
        else:
            return ret

if __name__ == '__main__':
    m_rpc= RPC("http://127.0.0.1:8000/api/rpc/","349304398403804983048034")
    print(m_rpc.call("test_service","service_test", **{"p1":1}))
    