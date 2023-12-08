########################################################
 # anomaly.py
 # find anomalies in given data
 #
 # Amgad Alghabra, 15.07.2022
 # amgad.alghabra1996@gmail.com
 #######################################################


import argparse
import numpy as np
import os
from collections import defaultdict





def anomaly(L):

    n = len(L)//25          # n contains the number of positions of the test part to identify the data set and non-random numbers
    anom = []               # This list will contain the anomaly positions
    CounterElement = {}               # This set contains the number of times each element exists in the data set
    CounterElement = defaultdict(lambda:0,CounterElement)             # Give the value 0 to each element as the default value
    LastPosition = {}                 # The last position in which the number last appeared
    LastPosition = defaultdict(lambda:0,LastPosition)                 # Give each position of each item the value 0 as the default
    CounterDistance = {}              # This set contains the distance between the same element
    CounterDistance = defaultdict(lambda:0,CounterDistance)           # Give each distance the value 0 as the default
    LastDistance = {}                 # The last distance between the same element
    CounterElementInDistance = {}                         # This set contains how often the elements have the same distance
    not_random = set()                # This set contains the numbers that are not random
    k = 0                   # This element contains the last position in the test part of the data set
    LastPositionInGroup = 0           # The last position in each group of non-random numbers


    # test part    
    for i in range(len(L)):
      CounterElement[L[i]] += 1
      if i < n:                        
        
          if LastPosition[L[i]] == 0:     # when the element occurs for the first time in the data set
            LastPosition[L[i]] = i
      
          else:
            LastDistance[L[i]] = i - LastPosition[L[i]]         
            if CounterDistance[LastDistance[L[i]]] == 0:             # When distance first occurs
              CounterElementInDistance[LastDistance[L[i]]] = {}     # Create a set at each distance and give the default value 0 to each element in the distance
              CounterElementInDistance[LastDistance[L[i]]] = defaultdict(lambda:0,CounterElementInDistance[LastDistance[L[i]]])

            CounterDistance[LastDistance[L[i]]] += 1
            CounterElementInDistance[LastDistance[L[i]]][L[i]] += 1
            if CounterElementInDistance[LastDistance[L[i]]][L[i]] > 3:    # If the element in the distance has occurred more than 3 times
              not_random.add(L[i])
                
      else:
          CounterNot_Random = []              # This list contains how often the non-random numbers occurred
          for j in not_random:
            CounterNot_Random.append(CounterElement[j])
          k = i
          if (CounterNot_Random[1:] == CounterNot_Random[:-1]) and (L[i] in not_random):
            LastPositionInGroup = i
            break

      LastPosition[L[i]] = i



    pattern = ""                        # "pattern" contains what the group looks like
    tmp = not_random.copy()
    i = k + 1
    FirstPositionInGroup = ""           # The first position in group of non-random numbers
    Distance = 0                        # The distance between the last item in a group and the first item of another group

    while(i<len(L)):

      if (not FirstPositionInGroup) and (L[i] in not_random):         # If "FirstPositionInGroup" is empty and the element "L[i]" is not random
          FirstPositionInGroup = i
          Distance = FirstPositionInGroup - LastPositionInGroup
      
      if L[i] in tmp:                              
          pattern = pattern + "1"                   # if the element is not random
          tmp.remove(L[i])
          if not tmp:                               # If "tmp" is empty
            LastPositionInGroup = i
            
      elif pattern and tmp:                       # if "pattern" and "tmp" is not empty
          pattern = pattern + "0"                 # if the element is random
      
      elif (not tmp) and (i == LastPositionInGroup + Distance): 
          for j in range(0,len(pattern)):
            if (i+j < len(L)) and (L[i+j] not in not_random) and (pattern[j] == '1'):
              anom.append(i+j)
          i = i + len(pattern)-1                      # The last position in the pattern
          LastPositionInGroup = i
      
      elif (not tmp) and (i < LastPositionInGroup + Distance) and (L[i] in not_random):   # When the non-random number or group occurs early
          anom.append(i) 
          i = i + len(pattern)-1                      # The last position in the pattern
          LastPositionInGroup = i
      
      i = i+1
    
      
    
    
    return("\n".join(map(str, anom)))
    


# for command line
parser = argparse.ArgumentParser()
parser.add_argument("--file",help = "Filename of the Datenset", type=str, required=True)
parser.add_argument("--dir", help = "Output Directory", type=str, required=True)
parser.add_argument("--name", help = "Your Name" ,type=str, required=True)

args = parser.parse_args()

l = open(args.file)
da = l.readlines()
data=list(map(int,da))

filePathAndName, file_extension = os.path.splitext(args.file)

if '/' in filePathAndName:
  arr = filePathAndName.split('/') 
  filename = arr[len(arr)-1]
else:  
  arr = filePathAndName.split('\\')
  filename = arr[len(arr)-1]


f = open(args.dir + "/" + args.name + filename + "Marker" + file_extension, "w")
f.write(str(anomaly(data)))
