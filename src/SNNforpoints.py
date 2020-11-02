# SNN ALGORITHM
import numpy as np
import csv
import matplotlib.pyplot as plt
import time
def fileloader(filename):
	dataset = []
	line_data = csv.reader(open(filename, "rb"))
	included_cols = [3,4]
	for row in line_data:
        	content = list(row[i] for i in included_cols)
		new_content = [float(i) for i in content]		
		dataset.append(new_content)
		
	return dataset

class kinf(object):
    def __init__(self,p,dt,nsn,il):
        self.Point=p # neighbour
        self.DistTo=dt # distance to neighbour
        self.NumOfSharedNeigh=nsn # shared neighbour num
        self.IsLinked =il
class inf(object):
    def __init__(self,p,t,coord,kn,d,cid):
        self.Point = int(p) # id
        self.Type = t # Core/Border/Noise
        self.coord = map(lambda x: float(x), coord) # convert to float
        self.knearest = []       # [kinf1, ...] nearest neighbours, of class kinf
        self.Density =-1 # function(Sum of all link strength)
        self.ClusterID = cid
        
class SnnCluster(object):
    def __init__(self, SNNArray=[], K=7, EPS=7*3/10, MinPts=7*7/10, MyColec=[]):

        self.SNNArray = SNNArray

        self.K = K
        # even the same point will be judged as noise if its more than K. Some how it's wrong.
    
        self.EPS = EPS
        # the author use 'K * 3 / 10'
        
        self.MinPts = MinPts
        # the author use 'K * 7 / 10'
        
        self.MyColec = MyColec

    
    def add_point(self,p,t,coord,kn,d,cid):
        self.SNNArray.append(inf(p,t,coord,kn,d,cid))
        
    def calculate_distance(self, point_1, point_2):
        coord_1, coord_2 = np.array(point_1.coord), np.array(point_2.coord)
        dist = sum( (coord_1 - coord_2)**2 ) ** 0.5
    
        return dist

    def insertKN(self,i,val):
        kn = self.SNNArray[i].knearest
        kn.insert(len(kn)-1,val)

    def GetKnearest(self):
        for i in range(0,len(self.SNNArray)):
            Count = 0
            for j in range(0,len(self.SNNArray)):
                if i<>j:
                    Count = Count+1
                    dist = self.calculate_distance(self.SNNArray[i], self.SNNArray[j])
                
                    if Count <= self.K:
                        kn = kinf(self.SNNArray[j].Point,dist,None,0)
                    
                        self.insertKN(i,kn)
                    
                
                    else:
                        Ind = self.GetMax(self.SNNArray[i].knearest)
                        if self.SNNArray[i].knearest[Ind].DistTo > dist:
                        
                        
                            self.SNNArray[i].knearest[Ind].DistTo = dist
                            self.SNNArray[i].knearest[Ind].Point = self.SNNArray[j].Point
                            self.SNNArray[i].knearest[Ind].IsLinked = 0


        self.OrderKnearestArray()

    def OrderKnearestArray(self):
        temp=[]
        for i in range(0,len(self.SNNArray)):
            for j in range(0,len(self.SNNArray[i].knearest)-1):
                for l in range((j + 1),len(self.SNNArray[i].knearest)):
                    if self.SNNArray[i].knearest[j].DistTo > self.SNNArray[i].knearest[l].DistTo:
                        temp.insert(0,self.SNNArray[i].knearest[j])
                        self.SNNArray[i].knearest[j] = self.SNNArray[i].knearest[l]
                        self.SNNArray[i].knearest[l] = temp[0]

    def SN(self):
        for i in range(0,len(self.SNNArray)):
            for j in range(0,len(self.SNNArray[i].knearest)):
                for l in range(0,len(self.SNNArray)):
                    print i
                   
    def SharedNearest(self):
        for i in range(0,len(self.SNNArray)):
            for j in range(0,len(self.SNNArray[i].knearest)):
                CountShare = 0
                for l in range(0,len(self.SNNArray)):
                    if self.SNNArray[i].knearest[j].Point == self.SNNArray[l].Point:
                        # if the p_l is in the k nearest point of p_i
                        for n in range(0,len(self.SNNArray[l].knearest)):
                            if self.SNNArray[l].knearest[n].Point == self.SNNArray[i].Point:
                                # if the p_i is in the k nearest point of p_l
                                self.SNNArray[i].knearest[j].IsLinked = 1

                        if self.SNNArray[i].knearest[j].IsLinked == 0:
                            self.SNNArray[i].knearest[j].NumOfSharedNeigh = 0
                        
                        else:
                        
                            for n in range(0,len(self.SNNArray[l].knearest)):
                                for m in range(0,len(self.SNNArray[l].knearest)):
                                    if self.SNNArray[l].knearest[m].Point == self.SNNArray[i].knearest[n].Point:
                                        CountShare = CountShare + 1
                                        #break
                                
                        
                            self.SNNArray[i].knearest[j].NumOfSharedNeigh = CountShare
                        
                            break

    def CalcDensity(self):
        # print 'self.EPS',self.EPS
        for i in range(0,len(self.SNNArray)):
            for j in range(0,len(self.SNNArray[i].knearest)):
                if self.SNNArray[i].knearest[j].NumOfSharedNeigh >= self.EPS:
                    self.SNNArray[i].Density = self.SNNArray[i].Density + (1 * self.SNNArray[i].knearest[j].IsLinked)
                else:
                    self.SNNArray[i].Density = self.SNNArray[i].Density + (0 * self.SNNArray[i].knearest[j].IsLinked)

    def CheckCores(self):
        for i in range(0,len(self.SNNArray)):
            #print 'D',self.SNNArray[i].Density
            if self.SNNArray[i].Density >= self.MinPts:
                self.SNNArray[i].Type = "Core"
            
            
                self.MyColec.insert(len(self.MyColec),i)
            else:
                self.SNNArray[i].Type = "Border"
                self.MyColec.insert(len(self.MyColec),i)
            
    def GetClusters(self):
        ClusterID = 0
        for i in range(0,len(self.SNNArray)):
            if self.SNNArray[i].Type <> "Noise" and self.SNNArray[i].ClusterID == -1:
                ClusterID = ClusterID + 1
                self.SNNArray[i].ClusterID = ClusterID
                self.ClusterNeighbours(self.SNNArray[i].Point, ClusterID)

    def ClusterNeighbours(self,Point,ClusterID):
        Neighbours =[]
        Index = None
        NovoPto = None
        for m in range(0,len(self.SNNArray)):
            if self.SNNArray[m].Point == Point:
                Neighbours = self.SNNArray[m].knearest # all k's of the Snnarray(m).point
                Index = m
                break
        for j in range(0,len(Neighbours)):
            NovoPto = Neighbours[j].Point # 1 of the Snnarray(m).point K's
            for l in range(0,len(self.SNNArray)):
                if self.SNNArray[l].Point == NovoPto:
                    if self.SNNArray[l].Type <> "Noise" and self.SNNArray[l].ClusterID == -1 and Neighbours[j].NumOfSharedNeigh >= self.EPS:
                        self.SNNArray[l].ClusterID = ClusterID
                        self.ClusterNeighbours(NovoPto, ClusterID)

    def CheckSimilarity(self,i,j):
        result = 0
        for m in range(0,len(self.SNNArray[i].knearest)):
            if self.SNNArray[i].Point == self.SNNArray[j].knearest[m].Point:
                for n in range(0,len(self.SNNArray[i].knearest)):
                    if self.SNNArray[j].Point == self.SNNArray[i].knearest[n].Point:
                         result = self.SNNArray[i].knearest[n].Point
                         break
        return result

    def NoisePoints(self):
        Similarity1 = None
        Similarity2 = None
        for i in range(0,len(self.SNNArray)):
            Similarity1 = 0
            if self.SNNArray[i].Type == "Border":
                for j in range(0,len(self.MyColec)):
                    Similarity2 = self.CheckSimilarity(i, j)
                    if Similarity2 > Similarity1:
                        Similarity1 = Similarity2
                if Similarity1 < self.EPS:
                    self.SNNArray[i].Type = "Noise"
                    self.SNNArray[i].ClusterID = 0
                
    def GetMax(self,kn):
        Max = float
        for i in range(0,len(kn)):
            if i == 0:
                Max = kn[i].DistTo
                MaxInd = i
            elif kn[i].DistTo > Max:
                Max = kn[i].DistTo
                MaxInd = i
        return MaxInd

    def process(self):
        self.GetKnearest()
         
        self.SharedNearest()      
    
        self.CalcDensity()

        self.CheckCores()
      
        self.NoisePoints()
        
        self.GetClusters()


if __name__ == '__main__':
    snn_cluster = SnnCluster()
    filename = '/home/ashish/Desktop/Major_Project/final_dataset.csv'
    datavalues = fileloader(filename)
    for i in range(len(datavalues)):
        snn_cluster.add_point(i, "", [datavalues[i][0], datavalues[i][1]], None, None, -1)  
    start_time = time.time()         
    snn_cluster.process()
    print("--- %s seconds ---" % (time.time() - start_time))
    cluster_ids = map(lambda x: x.ClusterID, snn_cluster.SNNArray)
    is_core = map(lambda x: x.Type, snn_cluster.SNNArray)
    print np.unique(cluster_ids)
    #print cluster_ids
    #print np.unique(is_core)
    #print is_core
