import shutil

class PrintPlus:
    def __init__(self):
        self.message = ''
        self.fillBlankWith = ' '
        self.endWith = '\n'
        self.align = 0
        self.colors = {'VIOLET':'\033[95m','BLUE':'\033[94m','GREEN':'\033[92m','YELLOW':'\033[93m','RED':'\033[91m','ENDC':'\033[0m','BOLD':'\033[1m','UNDERLINE':'\033[4m','HIGHLIGHT':'\033[1;30;47m'}

    def getTerminalSize(self):
        return shutil.get_terminal_size((80,80)).columns

    def show(self):
        processed = self.message
        indexes = list(range(len(processed)))
        for i in self.colors.values():
            try:
                while True:
                    del indexes[processed.index(i):processed.index(i)+len(i)]
                    processed = processed.replace(i,'',1)
            except ValueError:
                continue
        terminal_size = self.getTerminalSize()
        diff = (terminal_size - len(processed))//2
        if(diff>=0):
            if(self.align==1):
                print(self.fillBlankWith*diff+self.message+self.fillBlankWith*diff,end=self.endWith)
            elif(self.align==2):
                print(self.fillBlankWith*(diff*2)+self.message,end=self.endWith)
            else:
                print(self.message+self.fillBlankWith*(diff*2),end=self.endWith)
        else:
            startpos = (len(processed)//terminal_size)*terminal_size
            firstPart = self.message[:indexes[startpos]]
            secondPart = self.message[indexes[startpos]:]
            diff = (terminal_size - len(processed[startpos:]))//2
            if(self.align==1):
                print(firstPart+self.fillBlankWith*diff+secondPart,end=self.endWith)
            elif(self.align==2):
                print(firstPart+self.fillBlankWith*(diff*2)+secondPart,end=self.endWith)
            else:
                print(firstPart+secondPart+self.fillBlankWith*(diff*2),end=self.endWith)
        self.message = ''
        self.align=0
        self.fillBlankWith = ' '


    def end(self,char:chr = '\n'):
        self.endWith = char
        return self

    def getColored(self,message,color):
        processed = message.split(self.colors['ENDC'])
        res = ''
        for i in processed:
            res+=(str(color)+i)
        return res.strip()+str(self.colors['ENDC'])

    def text(self,message:str = ''):
        self.message += message
        return self

    def red(self):
        self.message = self.getColored(self.message,self.colors['RED'])
        return self

    def green(self):
        self.message = self.getColored(self.message,self.colors['GREEN'])
        return self
    
    def blue(self):
        self.message = self.getColored(self.message,self.colors['BLUE'])
        return self
    
    def bold(self):
        self.message = self.getColored(self.message,self.colors['BOLD'])
        return self
    
    def highlight(self):
        self.message = self.getColored(self.message,self.colors['HIGHLIGHT'])
        return self
    
    def underline(self):
        self.message = self.getColored(self.message,self.colors['UNDERLINE'])
        return self
    
    def yellow(self):
        self.message = self.getColored(self.message,self.colors['YELLOW'])
        return self
    
    def violet(self):
        self.message = self.getColored(self.message,self.colors['VIOLET'])
        return self
    
    def center(self):
        self.align=1
        return self
    
    def right(self):
        self.align=2
        return self

    def blanks(self,char:chr = ' '):
        self.fillBlankWith = str(char)
        return self
    
    