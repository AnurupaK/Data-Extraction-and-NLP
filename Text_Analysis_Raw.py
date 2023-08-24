##IMPORTING IMPORTANT LIBRARIES
import os
import pandas as pd
import string
import re
import nltk
# nltk.download('punkt')
# nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

##STOPWORDS

os.chdir("C:/Users/USER/Downloads/BlackCoffer/StopWords")
stop_words_files = os.listdir()

filtered_stop_words = []

for stop_file in stop_words_files:
    with open(stop_file, 'r', encoding='latin-1') as file:
        lines = file.readlines()
        for line in lines:
            # print(line)
            word = line.split('|')[0].strip()
            word_small = word.lower()
            filtered_stop_words.append(word_small)

##NLTK STOPWORDS

nltk_stopwords = set(stopwords.words('english'))


##POSITIVE AND NEGATIVE WORDS

os.chdir("C:/Users/USER/Downloads/BlackCoffer/MasterDictionary")
pos_words, neg_words = [], []
with open("positive-words.txt", 'r', encoding='latin-1') as file:
    words = file.read().split()
    pos_words.extend(words)
with open("negative-words.txt", 'r', encoding='latin-1') as file:
    words = file.read().split()
    neg_words.extend(words)




##GET THE INPUT FILES

data = pd.read_excel("C:/Users/USER/Downloads/BlackCoffer/Input.xlsx")
df1 = data.copy()
df1["URL_ID"] = df1["URL_ID"].astype(str)



###TEXT ANALYSIS AND PARAMETERS CALCULATION

os.chdir("C:/Users/USER/Downloads/BlackCoffer/Text_files_new")

text_files = os.listdir()
print("Number of text files:", len(text_files))

url_id_list2, number_of_words_list = [], []
pos_score_list, neg_score_list, pol_score_list, sub_score_lst = [], [], [], []
avg_sen_len_list, per_complex_list, Fog_index_list = [], [], []
avg_num_words_list = []
complex_word_list = []
syllable_per_word_list = []
personal_pronoun_count_list = []
num_of_words_nltk_list = []
# pp_count_list = []   ### This list is for personal pronoun counts without using regex (just for checking)
avg_word_length_list = []

for txt_file in text_files:
    URL_ID = txt_file.split('.')[0]
    URL_ID = str(URL_ID)
    print("URL ID:", URL_ID, "\n")
    url_id_list2.append(URL_ID)

    text = open(txt_file, encoding="utf-8").read()  ##Opening the text files

    text = text.lower()
    sentences = sent_tokenize(text)     ##Calculating number of sentenses
    number_of_sentences = len(sentences)
    word_list = word_tokenize(text)
    text_new = text.translate(str.maketrans('', '', string.punctuation + '“”'))
    word_list2 = word_tokenize(text_new)  ##This list contains all words along with stopwords but no punctuations
    number_of_words = len(word_list2)
    print("Number of words before cleaning:",number_of_words)

    ##This step is to remove the stopwords
    clean_tokenized_words = []
    for word in word_list2:
        if word not in filtered_stop_words:
            clean_tokenized_words.append(word)
    number_of_words_after_cleaning = len(clean_tokenized_words)
    print("Number of words after cleaning with provided stowords:",number_of_words_after_cleaning)


    ##This step is to remove the stopwords (from nltk package)
    clean_text2 = []
    for word in word_list2:
        if word not in nltk_stopwords:
            clean_text2.append(word)
    num_of_words_nltk = len(clean_text2)
    num_of_words_nltk_list.append(num_of_words_nltk)
    print("Number of words after cleaning with nltk stopwords:",num_of_words_nltk)


    ##POSITIVE, NEGATIVE, POLARITY AND SUBJECTIVE SCORE

    pos_score = []
    neg_score = []
    other_words = []
    for word in clean_tokenized_words:
        if word in pos_words:
            pos_score.append(1)
        elif word in neg_words:
            neg_score.append(-1)
        else:
            other_words.append(word)

    print("Positive words found +:", len(pos_score), "| Negative words found -:", len(neg_score),
          "| other words found:", len(other_words))
    positive_score = sum(pos_score)
    negative_score = sum(neg_score) * (-1)

    Polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    Subjectivity_score = (positive_score + negative_score) / (number_of_words_after_cleaning + 0.000001)
    print("Positive Score:", positive_score, "| Negative Score:", negative_score,
          "| Polarity: {:.5f},| Subjectivity: {:.5f}".format(Polarity_score, Subjectivity_score))

    pos_score_list.append(positive_score)
    neg_score_list.append(negative_score)
    pol_score_list.append(Polarity_score)
    sub_score_lst.append(Subjectivity_score)

    ##AVERAGE NUMBER OF WORDS PER SENTENCE
    average_number_of_words_per_sentence = number_of_words / number_of_sentences

    avg_num_words_list.append(average_number_of_words_per_sentence)

    ##SYLLABLE PER WORD
    vowel_count_current_list = []
    vowel_count_total = 0
    for word in word_list2:
        current_vowel_count = 0
        if word[-2:] == 'es' or word[-2:] == 'ed':
            store = word[0:-2]
            for letter in store:
                if letter in {'a', 'e', 'i', 'o', 'u'}:
                    vowel_count_total = vowel_count_total + 1
                    current_vowel_count = current_vowel_count + 1
            vowel_count_current_list.append(current_vowel_count)
        else:
            for letter in word:
                if letter in {'a', 'e', 'i', 'o', 'u'}:
                    vowel_count_total = vowel_count_total + 1
                    current_vowel_count = current_vowel_count + 1
            vowel_count_current_list.append(current_vowel_count)

    print("Total Vowel in the text:", vowel_count_total)
    syllable_per_word = vowel_count_total / number_of_words
    syllable_per_word_list.append(syllable_per_word)

    ##COMPLEX WORD COUNT
    complex_count = 0
    for i in vowel_count_current_list:
        if i > 2:
            complex_count = complex_count + 1
    complex_word_list.append(complex_count)
    print("Total number of complex words:", complex_count)

    ##ANALYSIS OF READABILITY
    average_sentence_length = number_of_words / number_of_sentences
    Per_complex_words = (complex_count / number_of_words) * 100
    Fog_index = 0.4 * (average_sentence_length + Per_complex_words)

    avg_sen_len_list.append(average_sentence_length)
    per_complex_list.append(Per_complex_words)
    Fog_index_list.append(Fog_index)
    print("Average Sentence Length: {:.2f}| Average number of words per sentence: {:.2f} | Percenatge of Complex Words:{:.2f} | Fog index:{:.2f}".format(
            average_sentence_length, average_number_of_words_per_sentence, Per_complex_words, Fog_index))

    ##PERSONAL PRONOUNS
    pronouns = r'\b(i|we|my|ours|us)\b'

    matches = [word for word in word_list2 if re.match(pronouns, word, flags=re.IGNORECASE)]
    personal_pronoun_count = len(matches)
    personal_pronoun_count_list.append(personal_pronoun_count)

    print("Personal Pronouns:", personal_pronoun_count)

    ##TO CHECK THE PERSONAL PRONOUN CALCULATION WITHOUT USING REGEX
    # count = 0
    # for word in word_list2:
    #     if word in ("i","we","my","ours","us"):
    #         count = count+1
    # pp_count_list.append(count)
    # print("PP count:",count)

    ##AVERAGE WORD LENGTH
    character_list = []
    for word in word_list2:
        a = len(word)
        character_list.append(a)

    total_number_of_character = sum(character_list)
    avg_word_length = total_number_of_character / number_of_words
    avg_word_length_list.append(avg_word_length)
    print("Average word Length:", avg_word_length)

    print("--------------------------------------------------------------------------------------------------")

##MAKING THE OUTPUT FILE
df2 = pd.DataFrame({"URL_ID": url_id_list2, "POSITIVE_SCORE": pos_score_list, "NEGATIVE_SCORE": neg_score_list,
                    "POLARITY_SCORE": pol_score_list, "SUBJECTIVITY_SCORE": sub_score_lst,
                    "AVG_SENTENCE_LENGTH": avg_sen_len_list, "PERCENTAGE_OF_COMPLEX_WORD": per_complex_list,
                    "FOG_INDEX": Fog_index_list, "AVG_NUMBER_OF_WORDS_PER_SENTENCE": avg_num_words_list,
                    "COMPLEX_WORD_COUNT": complex_word_list,
                    "WORD_COUNT": num_of_words_nltk_list, "SYLLABLE_PER_WORD": syllable_per_word_list,
                    "PERSONAL_PRONOUNS": personal_pronoun_count_list,
                    "AVG WORD LENGTH": avg_word_length_list})

print(df2)
merged_df = pd.merge(df1, df2, on='URL_ID', how='left')
print(merged_df)

os.chdir("C:/Users/USER/Downloads/BlackCoffer")
merged_df.to_excel("Output_Data_Structure.xlsx")

