from configparser import ConfigParser
import os.path
import logging

class CredentialRWTool:
    def __init__(self):
        self._key = 'djq%5cu#-jeq15abg$z9_i#_w=$o88m!*alpbedlbat8cr74sd'
        self._file_name = "config.ini"
        self.logger = logging.getLogger("credential_rw_tool")

    def _decrypt(self, s) -> str:
        dec_str = ""
        for i,j in zip(s.split("_")[:-1],self._key):
            # i 為加密字元，j為祕鑰字元
            tmp = chr(int(i) - ord(j)) # 解密字元 = (加密Unicode碼字元 - 祕鑰字元的Unicode碼)的單位元組字元
            dec_str = dec_str + tmp
        self.logger.info(f"[Done] decrypt the login credentail: {dec_str}")
        return dec_str

    def _encrypt(self, s) -> str:
        encry_str = ""
        for i,j in zip(s,self._key):
            # i為字元，j為祕鑰字元
            tmp = str(ord(i)+ord(j))+'_' # 加密字元 = 字元的Unicode碼 + 祕鑰的Unicode碼
            encry_str = encry_str + tmp
        self.logger.info(f"[Done] encrypt the login credentail: {encry_str}")
        return encry_str

    def write_ini(self, raw_id, raw_pwd): 
        id = self._encrypt(raw_id)
        pwd = self._encrypt(raw_pwd)

        config = ConfigParser()
        config['Credentials'] = {}
        config['Credentials']['ID'] = id
        config['Credentials']['password'] = pwd

        with open(self._file_name,'w') as f:
                config.write(f)
                self.logger.info("[Done] save the login credentails to the ini file")

    def read_ini(self):
        config = ConfigParser()
        try:
                assert os.path.exists(self._file_name)
                config.read(self._file_name)
                id, pwd = config['Credentials']['ID'], config['Credentials']['password']
                raw_id = self._decrypt(id)
                raw_pwd = self._decrypt(pwd)
                return raw_id, raw_pwd
        except Exception as e:
                self.logger.warning(f"while reading the credentials from the ini: {e}")
                return 'XXXXXX','XXXXXXXXXX'

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    cred_rw_tool = CredentialRWTool()
    cred_rw_tool.write_ini('123456', 'A123456789')
    id, pwd = cred_rw_tool.read_ini()
    try:
        assert id == '123456'
        assert pwd == 'A123456789'
        print("Pass")
    except Exception as e:
        print(f"[Error] dec/enc the id & pwd: {e}")
