from abc import ABC, abstractmethod

import random
import re
from pprint import pprint
import nltk
from nltk.corpus import words
import pandas as pd

class cipher(ABC):

    def __init__(self) -> None:
        self._key = None
        self._txt_plain = ''
        self._txt_decrypted = ''
        self._txt_encrypted = ''
        
        nltk.download('words',quiet=True)
        self._vocab_words = set(w.lower() for w in words.words())

    @abstractmethod
    def configure(self,*args,**kwargs) -> None:
        '''Configure the cipher parameters...'''
        pass

    @abstractmethod
    def configure_random(self) -> None:
        '''Randomly configure the cipher.'''
        pass

    @abstractmethod
    def msg_encrypt(self,str_text_plain:str) -> str:
        '''Encrypt plaintext...'''
        pass

    @abstractmethod
    def msg_decrypt(self,str_cipher_text:str) -> str:
        '''Decrypt ciphertext...'''
        pass

    @abstractmethod
    def get_decrypts(self) -> pd.DataFrame:
        pass

    def prepare_text_encrypt(self,str_text_plain:str,is_plaintext:bool=True) -> None:
        '''Normalize text prior to encryption...'''
        if(is_plaintext):
            self._txt_plain = str_text_plain
        str_text_plain = re.sub(r'[^\w\s]','',str_text_plain)
        # str_text_plain = re.sub(r' ',r'',str_text_plain)
        str_text_plain = str_text_plain.upper()
        if(is_plaintext):
            self._txt_encrypted = ''
            self._txt_decrypted = str_text_plain
        else:
            self._txt_encrypted = str_text_plain
            self._txt_decrypted = ''
    
    def prepare_text_decrypt(self, str_text_plain:str) -> None:
        '''Normalize text prior to encryption...'''
        self.get_text_ready_encrypt(str_text_plain=str_text_plain,is_plaintext=False)

    def test_if_words_are_real(self,str_text:str,char_split:chr=' ',is_return_percent:bool=False):
        vec_text = [x.lower() for x in str_text.split(char_split)]
        rtn_val = [x in self._vocab_words for x in vec_text]
        if(is_return_percent):
            return(sum(rtn_val)/len(vec_text))
        return(rtn_val)
    
    def print_contents(self) -> None:
        '''Print the current cipher state...'''
        print(f'''Plain Text: {self._txt_plain}''')
        print(f'''Cipher Text: {self._txt_encrypted}''')
        print(f'''Decrytped Text: {self._txt_encrypted}''')