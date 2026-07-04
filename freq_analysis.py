__version__ = '0.0.2'
__author__ = 'SRE'

#Frequency Analysis
import matplotlib.pyplot as plt
import pandas as pd

class freq_analysis:
    
    val_fig_width = 14.
    val_fig_height = 6.

    str_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    
    def get_letter_count(self,msg,val_chars:str=str_chars,
                         width:float=val_fig_width,
                         height:float=val_fig_height):
        self.val_fig_width= width
        self.val_fig_height = height
        letter_count = dict.fromkeys(val_chars,0)
        for letter in msg.upper():
            if letter in val_chars:
                letter_count[letter] += 1
        return letter_count

    def get_letter_plot(self,msg,val_chars:str=str_chars,
                        val_title=''):
        pd.options.display.max_columns = 26
        val_hist_lets = self.get_letter_count(msg,val_chars)
        df = pd.DataFrame.from_dict(val_hist_lets,orient='index')
        df.columns = ['Count']
        df['Letter'] = list(df.index)
        df = df.sort_values(['Letter'],ascending=[1])
        print(df.transpose().head(1))
        return(df,df.plot.bar(x='Letter',y='Count',title=val_title,figsize=(self.val_fig_width,self.val_fig_height)))

    def get_twin_plot(self,df:pd.DataFrame,val_plain,val_encr,val_title:str):
        fig = plt.figure(figsize=(self.val_fig_width,self.val_fig_height))
        ax = fig.add_subplot(111)
        val_width = 0.3
        df[val_plain].plot(kind='bar',color='green',width=val_width,position=1,title=val_title)
        df[val_encr].plot(kind='bar',color='red',width=val_width,position=0)
        ax.set_ylabel('Character Count')
        plt.legend(loc='best')
        plt.show()