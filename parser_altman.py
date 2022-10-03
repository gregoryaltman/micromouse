import shlex
import re
import csv
from pyamaze import maze,COLOR,agent

class Micromouse:
    def __init__(self, ifile, origPos =(1,1)):
        self.ifile = ifile
        self.csvfile='tmp.csv'
        self.origPos=origPos
        self.maze = maze(rows=4, cols=4)
        self.dict ={}
        # read the input file and get tokenizer for dictionary list
        self.processInput()
        # process the dictionary list and sort the dictionary list
        # before write the list into a cvs file (self.csvfile)
        self.processDict()
        

    # this function will take an input line and parse into 5 fields
    # field 1: cell., field 2: north distance...
    def parsefunc(self, line):
        line = line.replace(",", ", ")
        output = shlex.split(line)
        output = [re.sub(r",$","",w) for w in output]
        print(len(output))
        return output

    # this function will take an input file and get each line
    # and pass each line to parse the line for 5 fields
    # then add them into the dictionary
    def processInput(self):
        file1 = open(self.ifile, 'r')
        Lines = file1.readlines()
        count = 0
        # Strips the newline character
        for line in Lines:
            count += 1
            #print("Line{}: {}".format(count, line.strip()))
            voutput = self.parsefunc(line.strip())
            for indx in range(1,5):
                if float( voutput[indx]) > 0.25:
                    voutput[indx] ='1'
                else:
                    voutput[indx] ='0'
            
            # translation to pyamaze formatting 
            txt=voutput[0]
            txt=txt.split("(")
            a=txt[1].split(")")
            a=a[0].split(",")
            print("("+a[1]+", "+a[0]+")")
            self.dict["("+a[1]+", "+a[0]+")"] ={"cell": voutput[0], "E":  voutput[2],"W": voutput[3],"N": voutput[4], "S":voutput[1]}

    # the dictionary is completed after reading each file
    # we can write back the dictionary into a csv file base on the order
    # of each cell
    def processDict(self):
        info = ['cell', 'E', 'W', 'N','S'] # column header info
        items=self.dict.items()
        sortList=sorted(items) # puts items in order for pyamaze format
        newDict = dict(sortList)
        
        filename = 'tmp.csv'
        with open(filename, 'w', newline='') as myfile:
            writer = csv.writer(myfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(info)
            for i in newDict:
                writer.writerow(list(newDict[i].values()))
        
    def createMaze(self):
        # maze created based the self.csvfile
        self.maze.CreateMaze(x=self.origPos[0], y=self.origPos[1], loopPercent=100, loadMaze=self.csvfile)
        # displace the maze based the created maze
        self.maze.run()


if __name__=="__main__":
    a = Micromouse('inputfile.txt', (4,2))
    a.createMaze()
 