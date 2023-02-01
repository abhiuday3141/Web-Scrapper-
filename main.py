import requests ## For accessing pages
from bs4 import BeautifulSoup #Web Scrapping
import pandas as pd ##Dataframes
from urllib.error import HTTPError ## Try catch blocks
import os # for file paths



def Positive_dict(text): #Positive dictionary
    Positive=[]
    words=text.split(' ')
    path='**Location of positve-words.txt**'
    sentences=0
    with open(path, 'r') as f:
        data = f.readlines()
        for positive_word in data:
            for word in words:
                if word==positive_word[0:-1]:
                    Positive.append(word)

    return Positive

def Negative_dict(text): ##Negative dictionary
    Negative=[]
    words = text.split(' ')
    path = '**Location of positve-words.txt**'
    with open(path, 'r') as f:
        data = f.readlines()
        for positive_word in data:
            for word in words:
                if word == positive_word[0:-1]:
                    Negative.append(word)

    return Negative



def Stop_Words(text): ## Removing all the words present in stop words folder
    path='** Root directory of all the stop words**'
    file_list=os.listdir(path)
    stopwords = []
    textwords = text.split()
    resultwords=[]
    for filename in file_list:
        f=open(path+'/'+filename,'r')
        data=f.readlines()

        for words in data:
            wd=words[0:-1]
            wd=wd.split(' ')[0]
            stopwords.append(wd)

        resultwords=[word for word in textwords if word not in stopwords]

    result = ' '.join(resultwords)
    Punctations=['.',',',':',';','?','()','!'] ## removing punctations
    punct=0

    for i in range(len(result)):
        if result[i]=='?' or result=='!':
            punct=punct+1
    for p in Punctations:
        result=result.replace(p,'')

    return result,punct


def get_Syllable_count(text): #Get the syllable count
    words = text.split(' ')
    vowels=('a', 'e', 'i', 'o', 'u');
    count=0
    for word in words:
        l=len(word)
        if l>2:
            last_two=word[l-2]+word[l-1]
            if last_two=='es' or last_two=='ed':
                count=count-1
            for x in word.lower():
                if x in vowels:
                    count=count+1

    return count


def get_Words(text): ## Getting the words in the could be improved using regex
    return len(text.split(' '))

def count_Pronouns(text): ## Counting the pronouns
    words = text.split(' ')
    count=0
    pronouns=['I','we','We','my','My','ours','Ours','us']
    for word in words:
        if word in pronouns:
            count=count+1

    return count

def get_Sentences_and_Complex(text): #getting number of sentences and complex words
    words=text.split(' ')
    sentences=1
    complex_words=0

    for word in words:
        l=len(word)
        if l>0 and word[-1]=='.':
            sentences=sentences+1
        if l>2:
            complex_words=complex_words+1

    return sentences,complex_words

def file_input(): #For creating the text files
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
        "Connection": "keep-alive"
    } ## to make the site feel a user is accessing

    df = pd.read_excel('Input.xlsx')
    for i in range(len(df)):
        ID=df.iloc[i]['URL_ID']
        URL=df.iloc[i]['URL']

        try:
            r = requests.get(URL, headers=headers)
        except HTTPError as http_error:
            print(http_error)
        else:
            ##print("fine worked")
            soup = BeautifulSoup(r.content, 'html5lib')
            try:
                article_title = soup.find('h1').text
                article_text = soup.findAll('p')
            except:
                print("Heading and text not found in",ID)
            else:
                filepath="TextFiles/"+ str(ID) + ".txt"
                already_present=os.path.exists(filepath)
                if already_present==False:
                    f = open(filepath, "w",encoding="utf-8")
                    f.writelines(article_title + "\n")
                    print("File Created")

                    for info in article_text:
                        f.writelines(info.text + "\n")
                    f.close()



def Read_input():#This function reads the text files and gathers all the data
    headings = ['URL_ID', 'URL', 'POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE',
            'SUBJECTIVITY SCORE', 'AVG SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS','FOG INDEX','AVG NUMBER OF WORDS',
            'COMPLEX WORD COUNT','WORD COUNT', 'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH']
    df = pd.read_excel('Input.xlsx')
    df1 = pd.DataFrame(columns=headings,index=range(1,len(df)))

    for i in range(len(df)):
        ID = df.iloc[i]['URL_ID']
        URL = df.iloc[i]['URL']
        path='TextFiles/'+str(ID)+'.txt'
        try:
            f=open(path,'r',encoding="utf-8")
        except:
            print("File not present")
        else:

            data=f.readlines()
            text=' '.join(data)

            complete_list=[]
            text,punct=Stop_Words(text)

            total_characters=len(text)

            total_words=get_Words(text)


            sentences,complex_words=get_Sentences_and_Complex(text)
            sentences=sentences+punct # To get sentences ending with punctuations


            Positive_Score=len(Positive_dict(text))


            Negative_Score=len(Negative_dict(text))


            Polarity_Score=(Positive_Score-Negative_Score)/(Positive_Score+Negative_Score+0.000001)


            Subjectivity_Score=(Positive_Score+Negative_Score)/(0.000001+total_words)


            Avg_Sentence_length=total_words/sentences


            Complex_word_percent=complex_words/total_words


            Fog_Index=0.4*(Avg_Sentence_length+Complex_word_percent)


            Avg_words_per_sentence=total_words/sentences


            Avg_word_length=total_characters/total_words


            syllables=get_Syllable_count(text)

            pronouns=count_Pronouns(text)

            data_append = [ID,  URL,  Positive_Score, Negative_Score,Polarity_Score, Subjectivity_Score,Avg_Sentence_length,
                          Complex_word_percent,Fog_Index, Avg_words_per_sentence,complex_words,total_words,syllables,
                           pronouns,   Avg_word_length]



            df1.loc[i+1]=data_append

    df1.to_csv('Output.csv')


def main():
    file_input()  #run this function to make the required text files
    Read_input()


if __name__ == "__main__":
    main()


# I tried to work with nltk but the main page to download neccessary files was unavailable so I used different method


# import nltk
# import ssl
#
# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context
#
# nltk.download()
