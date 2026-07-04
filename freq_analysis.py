__version__ = "0.0.1"
__author__ = "SRE"

#Frequency Analysis
import matplotlib.pyplot as plt
import pandas as pd

class FreqAnalysis:
    
    valFigWidth = 16
    valFigHeight = 10
    
    def getLetterCount(self,msg,valChars=r'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',width=valFigWidth,height=valFigHeight):
        self.valFigWidth= width
        self.valFigHeight = height
        letterCount = dict.fromkeys(valChars,0)
        #{'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}
        for letter in msg.upper():
            if letter in valChars:
                letterCount[letter] += 1
        return letterCount

    def getLetterPlot(self,msg,valChars=r'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',valTitle=''):
        pd.options.display.max_columns = 26
        valHistLets = self.getLetterCount(msg,valChars)
        df = pd.DataFrame.from_dict(valHistLets,orient='index')
        df.columns = ['Count']
        df['Letter'] = list(df.index)
        df = df.sort_values(['Letter'],ascending=[1])
        print(df.transpose().head(1))
        return(df,df.plot.bar(x='Letter',y='Count',title=valTitle,figsize=(self.valFigWidth,self.valFigHeight)))

    def getTwinPlot(self,df,valPlain,valEncr,valTitle):
        fig = plt.figure(figsize=(self.valFigWidth,self.valFigHeight))
        ax = fig.add_subplot(111)
        valWidth = 0.3
        df[valPlain].plot(kind='bar',color='green',width=valWidth,position=1,title=valTitle)
        df[valEncr].plot(kind='bar',color='red',width=valWidth,position=0)
        ax.set_ylabel('Character Count')
        plt.legend(loc='best')
        plt.show()