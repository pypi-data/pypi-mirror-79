import argparse



def Fasta_OnelineFasta(inputfile,outputfile):
    file1=open(inputfile,"r")
    file2=file1.read().strip().split(">")[1:]    
    for elements1 in file2:
        elements2 = elements1.strip().split("\n")
        name = elements2[0]
        length = len(elements2)
        i=1
        seq = ""
        while i < length:
            seq = seq + elements2[i]
            i = i+1
        i = 1
        with open(outputfile,"a+")as f:
            f.write(">" + name + "\n"  + seq +"\n" )


import operator
def fasta_sequence_count(inputfile,outputfile):
    file1=open(inputfile,"r")
    file2=file1.read().strip().split(">")[1:]
    a=[]
    for elements1 in file2:
        name = elements1.strip().split("\n")[0]
        length = len(elements1.strip().split("\n")[1])
        a.append(length)
    dict_1={}
    for item in a:
        dict_1[item] = a.count(item)
        sorted_x = sorted(dict_1.items(), key=operator.itemgetter(1), reverse=True)
    for k, v in sorted_x:
        with open(outputfile,"a+")as f:
            f.write(str(k) + "\t" + str(v)  +"\n" )


def main():
    parser = argparse.ArgumentParser(description="fasta-manipulate is used to merge multiple line sequences in fasta files into one line sequence and count the number of different length sequences in the fasta file.")
    parser.add_argument("fasta_file", help="your input fasta-file")
    parser.add_argument("output_file",help="your output-file name")
    parser.add_argument("-o","--oneline", action="store_true", help="merge multiple line sequences in fasta files into one line sequence")
    parser.add_argument("-c","--count", action="store_true", help="count the number of different length sequences in the fasta file")

    args = parser.parse_args()

    if args.oneline == True:
        print('oneline')
        return Fasta_OnelineFasta(args.fasta_file,args.output_file)

    if args.count == True:
        print("count")
        return fasta_sequence_count(args.fasta_file,args.output_file)

if __name__=="__main__":
    main()
