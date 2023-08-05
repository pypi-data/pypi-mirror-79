#!/usr/bin/python
# -*- coding:utf-8 -*-
# Copyright 2019 Huawei Technologies Co.,Ltd.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License.  You may obtain a copy of the
# License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations under the License.

import os
import re
from obs import const
import threading

class NoneTokenException(Exception):
    def __init__(self,errorInfo):
        super(NoneTokenException, self).__init__(self)
        self.errorInfo = errorInfo

    def __str__(self):
        return self.errorInfo

class ENV(object):
    
    @staticmethod
    def search():
        reAccessKey = 'OBS_ACCESS_KEY_ID'
        reSecretKey = 'OBS_SECRET_ACCESS_KEY'
        reSecurityToken = 'OBS_SECURITY_TOKEN'

        accessKey = os.environ.get(reAccessKey)
        secretKey = os.environ.get(reSecretKey)
        securityToken = os.environ.get(reSecurityToken)

        if accessKey is None or secretKey is None:
            raise NoneTokenException('get token failed')

        return  {'accessKey':accessKey,
                 'secretKey':secretKey,
                 'securityToken':securityToken}

class ECS(object):
    ak = None
    sk = None
    token = None
    expires = None
    lock = threading.Lock()

    @staticmethod
    def search():
        if const.IS_PYTHON2:
            import httplib
        else:
            import http.client as httplib   
        from datetime import datetime
        from datetime import timedelta

        hostIP = '169.254.169.254'
        contactURL = '/openstack/latest/securitykey'

        if ECS.expires is not None:
            token_datenow = datetime.utcnow()
            if token_datenow < (ECS.expires - timedelta(minutes = 10)):
                return {'accessKey':ECS.ak,
                        'secretKey':ECS.sk,
                        'securityToken':ECS.token}

        if ECS.lock.acquire():
            try:
                if ECS.expires is not None and datetime.utcnow() < (ECS.expires - timedelta(minutes = 10)):
                    return {'accessKey':ECS.ak,
                            'secretKey':ECS.sk,
                            'securityToken':ECS.token}
               
                accessKey = None
                secretKey = None
                securityToken = None
                expiresAt = None
                try:
                    conn = httplib.HTTPConnection(hostIP)
                    conn.request('GET', contactURL)
                    result = conn.getresponse(True) if const.IS_PYTHON2 else conn.getresponse()
                    responseBody = result.read()
                except Exception:
                    if ECS.expires is not None and datetime.utcnow() < ECS.expires:
                        return {'accessKey':ECS.ak,
                                'secretKey':ECS.sk,
                                'securityToken':ECS.token}
                    raise
                finally:
                    conn.close()

                try:
                    reAccessKey = r'.*"access": "(.*?)",'
                    reSecretKey = r'.*"secret": "(.*?)",'
                    reSecurityToken = r'.*"securitytoken": "(.*?)",'
                    reExpires = r'.*"expires_at": "(.*?)"'

                    patternA = re.compile(reAccessKey)
                    patternS = re.compile(reSecretKey)
                    patternT = re.compile(reSecurityToken)
                    patternE = re.compile(reExpires)

                    if not const.IS_PYTHON2:
                        responseBody = responseBody.decode('utf-8')

                    resultS = patternS.match(responseBody)
                    resultA = patternA.match(responseBody)
                    resultT = patternT.match(responseBody)
                    resultE = patternE.match(responseBody)
                except Exception:
                    if ECS.expires is not None and datetime.utcnow() < ECS.expires:
                        return {'accessKey':ECS.ak,
                                'secretKey':ECS.sk,
                                'securityToken':ECS.token}        
                    raise

                if resultA is None or resultS is None or resultT is None or resultE is None:
                    if ECS.expires is not None and datetime.utcnow() < ECS.expires:
                        return {'accessKey':ECS.ak,
                                'secretKey':ECS.sk,
                                'securityToken':ECS.token}           
                    raise NoneTokenException('get token failed')

                accessKey = resultA.group(1) 
                secretKey = resultS.group(1)
                securityToken = resultT.group(1)
                expiresAt = resultE.group(1)

                ECS.ak = accessKey
                ECS.sk = secretKey
                ECS.token = securityToken
                ECS.expires = datetime.strptime(expiresAt,'%Y-%m-%dT%H:%M:%S.%fZ')

                return {'accessKey':accessKey,
                        'secretKey':secretKey,
                        'securityToken':securityToken}
            finally:
                ECS.lock.release()