__version__ = '0.0.1'
__author__ = 'SRE'

from cipher import cipher
import cipher_caesar
import pandas as pd
import random

class cipher_vigenere(cipher):
    
    def __init__(self,val_key:str='vigenere'):
        super().__init__()
        self.configure()
    
    def configure(self,val_key:str='vigenere') -> None:
        self._val_key = val_key.lower()
        self._vec_ciphers = []
        for i in self._val_key:
            tmp_key = ord(i.lower())-ord('a')
            self._vec_ciphers.append(cipher_caesar.cipher_caesar(val_shift=tmp_key))
        
    def configure_random(self) -> None:
        self.configure(val_key=random.choice(list(self._vocab_words)))

    def msg_encrypt(self,str_text_plain:str) -> str:
        self.prepare_text_encrypt(str_text_plain=str_text_plain,is_plaintext=True)
        str_text_plain = self._txt_plain.upper()
        tmp_txt = ''
        val_len_cipher = len(self._vec_ciphers)
        val_idx_cipher = 0
        for val_char in str_text_plain:
            if(val_idx_cipher>=val_len_cipher):
                val_idx_cipher = 0
            if(val_char==' '):
                tmp_txt += ' '
            else:
                tmp_txt += self._vec_ciphers[val_idx_cipher].msg_encrypt(str_text_plain=str(val_char))
                val_idx_cipher += 1
        self._txt_encrypted = tmp_txt
        return(self._txt_encrypted)

    def msg_decrypt(self,str_cipher_text:str) -> str:
        self.prepare_text_encrypt(str_text_plain=str_cipher_text,is_plaintext=False)
        str_cipher_text = self._txt_encrypted.upper()
        tmp_txt = ''
        val_len_cipher = len(self._vec_ciphers)
        val_idx_cipher = 0
        for val_char in str_cipher_text:
            if(val_idx_cipher>=val_len_cipher):
                val_idx_cipher = 0
            if(val_char==' '):
                tmp_txt += ' '
            else:
                tmp_txt += self._vec_ciphers[val_idx_cipher].msg_decrypt(str_cipher_text=str(val_char))
                val_idx_cipher += 1
        self._txt_decrypted = tmp_txt
        return(self._txt_decrypted)


    def get_decrypts(self,str_txt_ciphered:str,val_n_rails:int=5):
        vec_n = list(range(val_n_rails))
        vec_words = []
        for i in vec_n:
            self.configure(val_rails=i)
            vec_words.append(self.msg_decrypt(str_cipher_text=str_txt_ciphered))
        df = pd.DataFrame({'shift':vec_n,'decrypted':vec_words})
        df['percent_words'] = [self.test_if_words_are_real(x,is_return_percent=True) for x in df['decrypted']]
        df.sort_values(by=['percent_words','shift'],ascending=[False,True],inplace=True)
        df['type'] = 'Rail'
        return(df)