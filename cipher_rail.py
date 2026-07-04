__version__ = '0.0.1'
__author__ = 'SRE'

from cipher import cipher
import pandas as pd

class cipher_rail(cipher):
    
    def __init__(self,val_rails:int=1):
        super().__init__()
        self._val_rails = val_rails
    
    def configure(self,val_rails:int=1) -> None:
        self._val_rails = val_rails
        
    def configure_random(self,val_max:int=10) -> None:
        if(val_max<=0):
            val_max = 10
        self._val_rails = random.randint(a=0,b=val_max)

    def msg_encrypt(self,str_text_plain:str) -> str:
        self.prepare_text_encrypt(str_text_plain=str_text_plain,is_plaintext=True)
        if(self._val_rails<=1):
            return(str_text_plain)
    
        vec_fence = [[] for _ in range(self._val_rails)]
        val_cur_rail = 0
        val_dir = 1  # 1 means moving down, -1 means moving up
    
        for str_char in str_text_plain:
            vec_fence[val_cur_rail].append(str_char)
            val_cur_rail += val_dir
            if val_cur_rail == 0 or val_cur_rail == self._val_rails - 1:
                val_dir *= -1
        self._txt_encrypted = ''.join(''.join(row) for row in vec_fence)
        return(self._txt_encrypted)

    def msg_decrypt(self,str_cipher_text:str) -> str:
        self.prepare_text_encrypt(str_text_plain=str_cipher_text,is_plaintext=False)
        if(self._val_rails<=1):
            return(str_cipher_text)
    
        # Step 1: Reconstruct the pattern markers ('*') to find character positions
        vec_fence = [['\n'] * len(str_cipher_text) for _ in range(self._val_rails)]
        
        rail = 0
        val_dir = 1
    
        for i in range(len(str_cipher_text)):
            vec_fence[rail][i] = '*'
            rail += val_dir
            if rail == 0 or rail == self._val_rails - 1:
                val_dir *= -1
    
        # Step 2: Fill the marked matrix positions row by row with ciphertext
        cipher_index = 0
        for r in range(self._val_rails):
            for c in range(len(str_cipher_text)):
                if vec_fence[r][c] == '*' and cipher_index < len(str_cipher_text):
                    vec_fence[r][c] = str_cipher_text[cipher_index]
                    cipher_index += 1
    
        # Step 3: Read out the matrix diagonally to recover the plaintext
        result = []
        rail = 0
        val_dir = 1
    
        for i in range(len(str_cipher_text)):
            result.append(vec_fence[rail][i])
            rail += val_dir
            if rail == 0 or rail == self._val_rails - 1:
                val_dir *= -1
        self._txt_decrypted = ''.join(result)
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