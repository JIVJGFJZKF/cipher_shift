__version__ = '0.0.3'
__author__ = 'SRE'

from cipher import cipher
import string
import pandas as pd

class cipher_caesar(cipher):
    
    def __init__(self,val_shift:int=0):
        super().__init__()

        self._val_shift = val_shift
        self._val_key = ''
        self._val_chars = r'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.configure(val_shift=val_shift)
    
    def configure(self,val_shift:int=0) -> None:
        self.__val_shift__ = val_shift
        val_len = len(self._val_chars)
    
        self._val_key = {
            c: self._val_chars[(i + val_shift) % val_len]
            for i,c in enumerate(self._val_chars)}
        
    def configure_random(self) -> None:
        self.configure(val_shift=random.randint(a=0,b=len(self._val_chars)))

    def msg_encrypt(self,str_text_plain:str) -> str:
        self.prepare_text_encrypt(str_text_plain=str_text_plain,is_plaintext=True)
        self._txt_encrypted = ''.join(self._val_key[l] for l in self._txt_plain)
        return(self._txt_encrypted)

    def msg_decrypt(self,str_cipher_text:str) -> str:
        self.prepare_text_encrypt(str_text_plain=str_cipher_text,is_plaintext=False)
        tmp_flipped = {v: k for k, v in self._val_key.items()}
        str_decrypted = ''
        for i,val in enumerate(str_cipher_text):
            try:
                str_decrypted = str_decrypted+tmp_flipped[val]
            except:
                str_decrypted = str_decrypted+val
        self._txt_decrypted = str_decrypted
        return(self._txt_decrypted)

    def get_decrypts(self,str_txt_ciphered:str,is_try_reverse:bool=False):
        if(is_try_reverse):
            str_txt_ciphered = str_txt_ciphered[::-1]
        vec_n = list(range(len(string.ascii_lowercase)))
        vec_words = []
        for i in vec_n:
            self.configure(val_shift=i)
            vec_words.append(self.msg_decrypt(str_cipher_text=str_txt_ciphered))
        df = pd.DataFrame({'shift':vec_n,'decrypted':vec_words})
        df['percent_words'] = [self.test_if_words_are_real(x,is_return_percent=True) for x in df['decrypted']]
        df.sort_values(by=['percent_words','shift'],ascending=[False,True],inplace=True)
        df['type'] = 'Caesar Reversed' if is_try_reverse else 'Caesar Forward'
        if(is_try_reverse):
            df_not_reversed = self.get_decrypts(str_txt_ciphered=str_txt_ciphered[::-1],is_try_reverse=False)
            df = pd.concat([df,df_not_reversed],ignore_index=True)
            df.sort_values(by=['percent_words','shift'],ascending=[False,True],inplace=True)
        return(df)