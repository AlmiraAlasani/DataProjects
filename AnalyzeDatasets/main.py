#Read the files
#read paper1
f = open("c:\\Users\A\OneDrive\Desktop\DataProjects\AnalyzeDatasets\paper1.txt", "r")
print(f.read())
print('********************************************************************************************************************************************************************************************************')

#read paper2
f = open("c:\\Users\A\OneDrive\Desktop\DataProjects\AnalyzeDatasets\paper2.txt", "r")
print(f.read())
print('*************************************************************************************************************************************************************************************************')

# Generate word frequency list
#paper1
words = open("c:\\Users\A\OneDrive\Desktop\DataProjects\AnalyzeDatasets\paper1.txt", "r").read().split() #read the words into a list.
uniqWords = sorted(set(words)) #remove duplicate words and sort
for word in uniqWords:
    print (words.count(word), word)
print('**********************************************************************************************')
#paper2
words = open("c:\\Users\A\OneDrive\Desktop\DataProjects\AnalyzeDatasets\paper1.txt", "r").read().split() #read the words into a list.
uniqWords = sorted(set(words)) #remove duplicate words and sort
for word in uniqWords:
    print (words.count(word), word)
print('********************************************************************************************')

#Calculate cosine similarity

v1=[];
v2=[];
import torch
import torch.nn as nn

cos = nn.CosineSimilarity()
cos(torch.tensor([v1]), torch.tensor([v2])).item()

cos(torch.tensor(v1), torch.tensor(v2)).tolist()