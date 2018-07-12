# Importing the libraries
from collections import defaultdict 
import re
import pandas as pd
from collections import Counter
from sklearn import preprocessing
import PyPDF2

###############################################################################
#step 1. Extracting text from PDF file 

# creating a pdf file object
pdfFileObj = open('JavaBasics-notes.pdf', 'rb')
 
# creating a pdf reader object
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
 
# printing number of pages in pdf file
numPages = pdfReader.numPages

# collecting text in each page
text = []
for i in range(numPages):
    # creating a page object
    pageObj = pdfReader.getPage(i)
     
    # extracting text from page
    text.append(pageObj.extractText())
        
# closing the pdf file object
pdfFileObj.close()

###############################################################################
# Step2 : data preprocessing

# Expand some words
def decontracted(phrase):
    # specific
    phrase = re.sub(r"won't", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)

    # general
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    phrase = re.sub(r" v", " very", phrase)
    return phrase

file_text = []
for i in range(len(text)):
    file_text.append(decontracted(text[i]))
    
#cleaning unwanted symbols
comment_dict = defaultdict(list)
for i in range(len(file_text)):
    sentence = file_text[i]
    sentence = sentence.lower()
    sentence = sentence.split('.')
    for k in range(len(sentence)):
        review = sentence[k].split()
        sentence[k] =  ' '.join(review)
        comment_dict[i].append(sentence[k])
        
#delete unwanted '' words
for j in range(len(comment_dict)):
    comment_dict[j] = [comment_dict[j][i] for i in range(len(comment_dict[j])) if comment_dict[j][i] not in '']

for i in range(len(comment_dict)):
    file_text[i] = ('. '.join(comment_dict[i][j] for j in range(len(comment_dict[i]))))

#collecting all preprocessed text in pdf file.
text = ''
for i in range(len(file_text)):
    text = text + file_text[i]


###############################################################################
#Step 3 : Keywords Extraction 

# List of possible keywords    
keywords = list({'java', 'object', 'abstraction', 'encapsulation', 'inheritance', 'polymorphism', 'class', 
            'association', 'aggregation', 'composition', 'private', 'protected', 'public',
            'abstract', 'extends', 'final', 'implements', 'interface', 'native', 'new', 'static', 'strictfp', 
            'synchronized', 'transient', 'volatile', 'break', 'case', 'continue', 'default', 'do', 
            'else', 'for', 'if', 'instanceof', 'return', 'switch', 'while', 'import', 'package', 'boolean', 'byte',
            'char', 'double', 'float', 'int', 'long', 'short', 	'assert', 'catch', 'finally', 'throw', 'throws', 'try',
            'enum', 'super', 'this', 'void', 'const', 'goto', 'boolean', 'byte', 'switch', 'case', 'try', 'catch',
            'finally', 'char', 'int', 'continue', 'default', 'do', 'double', 'if', 'else', 'enum', 'extends',
            'final', 'float', 'for', 'implements', 'import', 'instanceOf', 'int', 'interface', 'long', 'native', 
            'new', 'package', 'private', 'protected', 'public', 'return', 'short', 'static', 'strictfp', 
            'super', 'synchronized', 'this', 'throw', 'throws', 'transient', 'void', 'volatile', 'while',
            'goto', 'const',  'abstract', 'assert', 'break', 'operator', 'expression', 'array', 'string', 
            'premitive', 'declaration', 'interface', 'applet', 'html', 'css', 'javascript', 'robustness'
            'security', 'portability', 'garbage collections', 'compile', 'method', 'instance', 'return', 'initialize'})

# Finding the maximum length from all keywords
maxx = 0
for i in range(len(keywords)):
    if(len(str(keywords[i])) > maxx):
        maxx = len(str(keywords[i]))

#List of all keywords present in pdf text.       
count = []
for i in range(len(text)):
    for j in range(maxx+1):
        if (text[i:i+j] in keywords):
            count.append(text[i:i+j])
        else: 
            continue

# No of occurrence of all keywords present in text        
c = Counter(count)
keyword_dict = dict()        
for i in keywords:
    keyword_dict[i] = c[i]
    
# Sorting keywords in descending order of their number of occurances   
from collections import OrderedDict        
key_words = OrderedDict(sorted(keyword_dict.items(), key=lambda x: x[1], reverse = True))       

# Printing all keywords        
print('Keywords :', key_words)

keys = list(key_words.keys())
values = list(key_words.values())

# Removing all keywords which are not present in text of pdf.
index = 0
for i in range(len(values)):
    if(values[i] > 0):
        index += 1    
keys = keys[: index]
values = values[: index]

# Creation of dataframe to calculate normalized score
dataframe = pd.DataFrame()
dataframe['No of occurrence'] = values

min_max_scaler = preprocessing.MinMaxScaler()
np_scaled = min_max_scaler.fit_transform(dataframe)
df_normalized = pd.DataFrame(np_scaled)
temp = list(df_normalized[0])

# Result obtained stored in dataframe named 'df'       
df = pd.DataFrame()
df['Keywords'] = keys
df['Normalized Weightage'] = temp
df['No of occurrence'] = values        

# Storing result in permanent storage of csv file.
df.to_csv('Result.csv')
   