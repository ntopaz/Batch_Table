from Bio import SeqIO, Entrez
import re, os, tempfile

Entrez.email = raw_input('Enter NCBI email: ')
my_seqs_1 = raw_input('Input File: ')

count = 0
gi_result = []
org_result = []
len_result = []
i = 0

temp_file = open("temp","w")
for record in SeqIO.parse(my_seqs_1, 'fasta'):
		split_id = str.split(record.id)
		my_gi = str.split(split_id[0], '|')
		handle = Entrez.efetch(db="protein", id=my_gi[1],rettype = "fasta",retmode= "xml")
		temp_file.write(handle.read().strip() +"\n")
		count = count + 1
		
temp_file.close()

my_seqs_2 = open("temp","r")
text = my_seqs_2.read()

gi_str = '<TSeq_gi>([\d\.]+)</TSeq_gi>'
gi_result = re.findall(gi_str,text)
org_str = '<TSeq_orgname>(.+)</TSeq_orgname>'
org_result = re.findall(org_str,text)
len_str = '<TSeq_length>([\d\.]+)</TSeq_length>'
len_result = re.findall(len_str,text)
desc_str = '<TSeq_defline>(.+)</TSeq_defline>'
desc_result = re.findall(desc_str,text)

#sets up output file and writes results to it
maximum_value = max(len(gi_result),len(org_result),len(len_result),len(desc_result))
output_file = open("report.txt","w")
output_file.write("GI Number: | Organism: | Description: | Sequence Length: \n")
while i != maximum_value:
	output_file.write(gi_result[i] + " | " + org_result[i] + " | " + desc_result[i] + " | " + len_result[i] + "\n")
	i += 1

print(str(i) + " sequences written to report.txt")
output_file.close()
my_seqs_2.close()
os.remove("temp")
raw_input()

