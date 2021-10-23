'''
p-search : Python Word Search
Author: C. Hosmer


Copyright (c) 2021 Chet Hosmer

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial 
portions of the Software.

'''

import time
import argparse                        # Python Standard Library - Parser for command-line options, arguments
import os                              # Standard Library OS functions
import sys                             # Standard Library sys module
import re                              # Standard Library regular expression processing

if sys.version_info[0] < 3:
    PYTHON_2 = True
else:
    PYTHON_2 = False

''' 
Import Optional PrettyTable Library
to install from the windows command line or linux/mac terminal
pip install prettytable
'''
try:
    from prettytable import PrettyTable
    PRETTY = True
except:
    PRETTY = False

#Psuedo Constants 
MIN_WORD          = 4                        # Minimum word size in bytes
MAX_WORD          = 15                       # Maximum word size in bytes
PREDECESSOR_SIZE  = 32                       # Values to print before match found
WINDOW_SIZE       = 128                      # Total values to dump when match found
MAXBUFF           = 1024 * 1024 * 16         # 16 Megabytes defines the size of 
                                             # of the memory chunks read
                                             # COMMON STOP WORDS LIST
                                             # What are stop_words: Words which are typically filtered 
                                             # out when processing natural language data (text)
                                             # feel free to add additional words to the list
                                             
STOP_WORDS =["able","about","above","accordance","according",
            "accordingly","across","actually","added","affected",
            "affecting","affects","after","afterwards","again",
            "against","almost","alone","along","already","also",
            "although","always","among","amongst","announce",
            "another","anybody","anyhow","anymore","anyone",
            "anything","anyway","anyways","anywhere","apparently",
            "approximately","arent","arise","around","aside",
            "asking","auth","available","away","awfully","back",
            "became","because","become","becomes","becoming",
            "been","before","beforehand","begin","beginning",
            "beginnings","begins","behind","being",
            "believe","below","beside","besides","between",
            "beyond","both","brief","briefly","came","cannot",
            "cause","causes","certain","certainly","come",
            "comes","contain","containing","contains","could",
            "couldnt","date","different","does","doing","done",
            "down","downwards","during","each","effect","eight",
            "eighty","either","else","elsewhere","end",
            "ending","enough","especially","even","ever",
            "every","everybody","everyone","everything",
            "everywhere","except","fifth","first","five",
            "followed","following","follows","former","formerly",
            "forth","found","four","from","further",
            "furthermore","gave","gets","getting",
            "give","given","gives","giving","goes",
            "gone","gotten","happens","hardly","has","have",
            "having","hence","here","hereafter","hereby",
            "herein","heres","hereupon","hers","herself",
            "himself","hither","home","howbeit","however",
            "hundred","immediate","immediately","importance",
            "important","indeed","index","information",
            "instead","into","invention","inward","itself",
            "just","keep","keeps","kept","know","known",
            "knows","largely","last","lately","later","latter",
            "latterly","least","less","lest","lets","like",
            "liked","likely","line","little","look","looking",
            "looks","made","mainly","make","makes","many",
            "maybe","mean","means","meantime","meanwhile",
            "merely","might","million","miss","more","moreover",
            "most","mostly","much","must","myself","name",
            "namely","near","nearly","necessarily","necessary",
            "need","needs","neither","never","nevertheless",
            "next","nine","ninety","nobody","none","nonetheless",
            "noone","normally","noted","nothing","nowhere",
            "obtain","obtained","obviously","often","okay",
            "omitted","once","ones","only","onto","other",
            "others","otherwise","ought","ours","ourselves",
            "outside","over","overall","owing","page","pages",
            "part","particular","particularly","past","perhaps",
            "placed","please","plus","poorly","possible","possibly",
            "potentially","predominantly","present","previously",
            "primarily","probably","promptly","proud","provides",
            "quickly","quite","rather","readily","really","recent",
            "recently","refs","regarding","regardless",
            "regards","related","relatively","research",
            "respectively","resulted","resulting","results","right",
            "run","said","same","saying","says","section","see",
            "seeing","seem","seemed","seeming","seems","seen",
            "self","selves","sent","seven","several","shall",
            "shed","shes","should","show","showed","shown",
            "showns","shows","significant","significantly",
            "similar","similarly","since","slightly","some",
            "somebody","somehow","someone","somethan",
            "something","sometime","sometimes","somewhat",
            "somewhere","soon","sorry","specifically","specified",
            "specify","specifying","still","stop","strongly",
            "substantially","successfully","such","sufficiently",
            "suggest","sure","take","taken","taking","tell",
            "tends","than","thank","thanks","thanx","that",
            "thats","their","theirs","them","themselves","then",
            "thence","there","thereafter","thereby","thered",
            "therefore","therein","thereof","therere",
            "theres","thereto","thereupon","there've","these",
            "they","think","this","those","thou","though","thought",
            "thousand","through","throughout","thru","thus",
            "together","took","toward","towards","tried","tries",
            "truly","trying","twice","under","unfortunately",
            "unless","unlike","unlikely","until","unto","upon",
            "used","useful","usefully","usefulness","uses","using",
            "usually","value","various","very","want","wants",
            "was","wasnt","welcome","went","were","what","whatever",
            "when","whence","whenever","where","whereafter","whereas",
            "whereby","wherein","wheres","whereupon","wherever",
            "whether","which","while","whim","whither","whod",
            "whoever","whole","whom","whomever","whos","whose",
            "widely","will","willing","wish","with","within","without",
            "wont","words","world","would","wouldnt",
            "your","youre","yours","yourself","yourselves"] 
                                                                        
def ValidateFileRead(theFile):
    
    ''' Validate the file paths is readable '''
    # Validate the path is a valid
    if not os.path.exists(theFile):
        raise argparse.ArgumentTypeError('File does not exist')

    # Validate the path is readable
    if os.access(theFile, os.R_OK):
        return theFile
    else:
        raise argparse.ArgumentTypeError('File is not readable')

class FileSearch:

    def __init__(self):
        
        self.ParseCommandLine()
        
    def ParseCommandLine(self):
    
        parser = argparse.ArgumentParser('Python Keyword Search and Word Indexing')
    
        parser.add_argument('-v', '--verbose',     help="enables printing of additional program messages", action='store_true')
        parser.add_argument('-k', '--keyWords',    type= ValidateFileRead, required=True, help="specify the file containing search words")
        parser.add_argument('-t', '--srchTarget',  type= ValidateFileRead, required=True, help="specify the target file to search")    
        parser.add_argument('-m', '--theMatrix',   type= ValidateFileRead, required=True, help="specify the weighted matrix file")     
        
        args = parser.parse_args()           
        
        if args.verbose:
            self.VERBOSE = True
        else:
            self.VERBOSE = False
            
        self.keywordFile = args.keyWords
        self.targetFile  = args.srchTarget
        self.matrix      = args.theMatrix
        self.fp = open(self.targetFile, 'rb')
        
        print("\nCommand Line Processed - Successfully\n")
        
    def readBUFF(self):

        # Read in a bytearray
        ba = self.fp.read(MAXBUFF) 
        if PYTHON_2:
            contents = ba
        else:
            contents = "".join(map(chr, ba))

        # substitute spaces for all non-ascii characters
        # this improves the performance and accuracy of the
        # regular expression searches 

        txt = re.sub('[^A-Za-z]', ' ', contents)
        txt = txt.lower()

        # Return the resulting text string that will be searched
        return txt     
        

    def SearchWords(self):
        
        ''' Search the file for keywords '''
        
        # Create an empty set of search words
        self.searchWords = set()
        
        # Create possible word dictionary
        self.possibleWords = {}

        # Create keyword found dictionary
        self.keywordDictionary = {}
    
        # Attempt to open and read search words
        try:
            with open(self.keywordFile) as fileWords:
                for line in fileWords:
                    self.searchWords.add(line.strip())    
        except Exception as err:
            sys.exit('Keyword File Failure: ' + str(err) + self.keywordFile)   
    
        wordCheck = class_Matrix(self.matrix)
        
        # Search Loop
        # step one, replace all non characters with zero's
        
        # Iterate through the file one chunk at a time

        cnt = 0
        for block in iter(self.readBUFF, ''):

            # Provides user feedback one dot = 16MB Chunk Processed
            if self.VERBOSE:
                if cnt < 64:
                    cnt +=1
                    print('.', end="")
                else:
                    # Print GB processed 
                    gbProcessed += 1
                    print
                    print("GB Processed: ", gbProcessed)
                    cnt = 0

            # step # 2 extract possible words from the bytearray
            # and then inspect the search word list
            # create an empty list of probable wnot found items
                    
            words = block.split()
            
            for newWord in words:
                if len(newWord) >= MIN_WORD and len(newWord) <= MAX_WORD:
                    
                    if newWord in self.searchWords:
                        try:
                            value = self.keywordDictionary[newWord]
                            value += 1
                            self.keywordDictionary[newWord] = value
                        except:
                            self.keywordDictionary[newWord] = 1

                    if wordCheck.isWordProbable(newWord):
                        if newWord not in STOP_WORDS:
                            try:
                                value = self.possibleWords[newWord]
                                value += 1
                                self.possibleWords[newWord] = value
                            except:
                                self.possibleWords[newWord] = 1                         


    def PrintKeywordsFound(self):
        print("\n\n")
        if PRETTY:
            # Create Pretty Table with Heading
            t = PrettyTable(['Occurrences', 'Keyword'])
            
            for eachWord in sorted(self.keywordDictionary, key=self.keywordDictionary.get, reverse=True):
                count = self.keywordDictionary[eachWord]
                t.add_row([count, eachWord])                      
            
            t.align = "l" 
            
            tabularResults = t.get_string()
            print(tabularResults)      
            
        else:
            
            print("Occurrences   Keyword")
            print("=====================")
            for eachWord in sorted(self.keywordDictionary, key=self.keywordDictionary.get, reverse=True):
                count = self.keywordDictionary[eachWord]
                print('{:<11}'.format(count), eachWord)
            print("\n")
            
        
    def PrintPossibleWords(self):
        
        print("\n\n")
        if PRETTY:
            # Create Pretty Table with Heading
            t = PrettyTable(['Occurrences', 'Possible Word'])
            
            for eachWord in sorted(self.possibleWords, key=self.possibleWords.get, reverse=True):
                count = self.possibleWords[eachWord]
                t.add_row([count, eachWord])                    
            
            t.align = "l" 
            
            tabularResults = t.get_string()
            print(tabularResults)   
            print("\n")
            
        else:
            print("Occurrences   Possible-Word")
            print("===========================")
            for eachWord in sorted(self.possibleWords, key=self.possibleWords.get, reverse=True):
                count = self.possibleWords[eachWord]
                print('{:<11}'.format(count), eachWord)
            print("\n")            
        
    def PrintKeywords(self):
        
        print("\n\n")
        if PRETTY:
            # Create Pretty Table with Heading
            t = PrettyTable(['Keywords to Search'])
            
            for kw in self.searchWords:
                t.add_row([kw])                    
            
            t.align = "l" 
            
            tabularResults = t.get_string()
            print(tabularResults)  
        else:
            print("Keywords to Search for")
            print("======================")
            kwList = list(self.searchWords)
            kwList.sort()
            for eachKW in kwList:
                print(eachKW)
            print("\n")                

                          
class class_Matrix:
    
    ''' Performs word approximation '''
    
    weightedMatrix = set()
    
    def __init__(self, theMatrixFile):
        try:
            with open(theMatrixFile) as matrix:
                for line in matrix:
                    value = line.strip()
                    self.weightedMatrix.add(int(value,16))       
        except Exception as err:
            sys.exit('Matrix File Error: ' + str(err) + theMatrixFile)   

    
    def isWordProbable(self, theWord):
        
        if len(theWord) < 5:
            return False
        
        if (len(theWord) < MIN_WORD):
            return False
        else:
            BASE = 96
            wordWeight = 0
            
            for i in range(4,0,-1):
                charValue = (ord(theWord[i]) - BASE)
                shiftValue = (i-1)*8
                charWeight = charValue << shiftValue
                wordWeight = (wordWeight | charWeight)        
                
            if ( wordWeight in self.weightedMatrix):
                    return True
            else:
                    return False

if __name__ == '__main__':
    ''' p-search version 2.0 python 3 support '''

    PSEARCH_VERSION = '2.0 May 2019 '
    
    print("Welcome to p-search Version" + PSEARCH_VERSION)

    # Record the Starting Time
    startTime = time.time()
    
    srchObj = FileSearch()
    
    srchObj.SearchWords()
    srchObj.PrintKeywords()
    srchObj.PrintKeywordsFound()
    srchObj.PrintPossibleWords()
    
    # Record the Ending Time
    endTime = time.time()    
    duration = endTime - startTime   
    
    print('Elapsed Time: ' + str(duration) + ' seconds')
    print('Program Terminated Normally')

    
    
    


   

        






