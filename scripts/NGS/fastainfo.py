import string
import sys
import os
from Bio import SeqIO

for i in range(1,len(sys.argv)):
  data=[]
  fasta_parser=SeqIO.parse(sys.argv[i],'fasta')
  for fasta in fasta_parser:
     data.append(str(fasta.seq))
  length=0
  for j in range(len(data[0])):
    flag=0
    for k in range(len(data)):
      if data[k][j]!='-':
        flag=1
    length=length+flag

  #output_name=sys.argv[i]+'.info'
  output_name='infoall_incident_3mon'
  with open(output_name,'a') as f:
    print >>f,'Name:',sys.argv[i],len(data)
