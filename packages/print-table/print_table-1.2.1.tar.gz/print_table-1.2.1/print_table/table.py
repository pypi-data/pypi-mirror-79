import shutil



#Table Class
class Table:
    def __init__(self,numberOfCols: int = 0):
        self.rows = []
        self.cols = numberOfCols
        self.colors = {'ENDC':'\033[0m','BOLD':'\033[1m'}
    

    def head(self,headers: list):
        self.rows.insert(0,headers)
        return self
    
    def row(self,row: list):
        self.rows.append(row)
        return self
    
    def getTerminalSize(self):
        return shutil.get_terminal_size((80,80)).columns

    def printResponsive(self,msg = '',padding='-',spaceAbove=True):
        processed = msg
        processed = processed.replace(self.colors['BOLD'],'').replace(self.colors['ENDC'],'')
        terminal_size = self.getTerminalSize()
        diff = max(0,(terminal_size - len(processed)))//2
        if(spaceAbove):
            print()
        print(padding*diff+msg+padding*diff)

    def getColored(self,msg,color):
        return str(color)+msg+str(self.colors['ENDC'])

    def printTable(self):
        if(self.cols!=0 and len(self.rows)>0):
            for row in self.rows:
                if(len(row)<self.cols):
                    for _ in range(self.cols-len(row)):
                        row.append(' ')
                elif(len(row)>self.cols):
                    row = row[:self.cols]
            terminal_size = self.getTerminalSize()
            per_col = (terminal_size-self.cols-1)//self.cols
            pattern = '-'*(per_col*self.cols+self.cols+1)
            self.printResponsive(pattern,padding=' ',spaceAbove=False)
            for i in range(len(self.rows)):
                row = self.rows[i]
                row = [self.paddColumn(per_col,str(r)) for r in row]
                if(i==0):
                    row = [self.getColored(r,self.colors['BOLD']) for r in row]
                row = '|'+'|'.join(row)+'|'
                self.printResponsive(row,padding=' ',spaceAbove=False)
                if(i!=len(self.rows)-1):
                    self.printMidLine(terminal_size)
            self.printResponsive(pattern,padding=' ',spaceAbove=False)

    def paddColumn(self,perCol,col):
        if(len(col)>perCol):
            return col[:perCol]
        dif = perCol - len(col)
        if(dif%2==0):
            return ' '*(dif//2) + col + ' '*(dif//2)
        return ' '*(dif//2) + col + ' '*(dif//2 +1)


    def printMidLine(self,t_size):
        per_col = (t_size-self.cols-1)//self.cols
        pattern_temp = '-'*(per_col*self.cols+self.cols+1)
        pattern = ''
        for i in range(len(pattern_temp)):
            if(i==0 or i == len(pattern_temp)-1):
                pattern+='|'
            elif(i%(per_col+1)==0):
                pattern+='+'
            else:
                pattern += pattern_temp[i]
        
        self.printResponsive(pattern,padding=' ',spaceAbove=False)