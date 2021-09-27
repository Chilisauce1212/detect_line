def Slope(line):
    if(line[0][0]==line[0][2]):
        return 0
    else:
        return (line[0][3]-line[0][1])/(line[0][2]-line[0][0])