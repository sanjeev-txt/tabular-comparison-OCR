import pickle
import string
from nltk.corpus import stopwords
import re
import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

nltk.download('wordnet')

nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
def clean(text):
    text=text.lower()
    PUNCT_TO_REMOVE = string.punctuation

    def remove_punctuation(text):
        """custom function to remove the punctuation"""
        return text.translate(str.maketrans('', '', PUNCT_TO_REMOVE))

    text = remove_punctuation(text)
    STOPWORDS = set(stopwords.words('english'))

    def remove_stopwords(text):
        """custom function to remove the stopwords"""
        return " ".join([word for word in str(text).split() if word not in STOPWORDS])

    text = remove_stopwords(text)

    def remove_emoji(string):
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', string)

    text = remove_emoji(text)

    def remove_urls(text):
        url_pattern = re.compile(r'https?://\S+|www\.\S+')
        return url_pattern.sub(r'', text)

    text = remove_urls(text)

    def remove_html(text):
        html_pattern = re.compile('<.*?>')
        return html_pattern.sub(r'', text)

    text = remove_html(text)
    lemmatizer = WordNetLemmatizer()
    wordnet_map = {"N": wordnet.NOUN, "V": wordnet.VERB, "J": wordnet.ADJ, "R": wordnet.ADV}

    def lemmatize_words(text):
        pos_tagged_text = nltk.pos_tag(text.split())
        return " ".join(
            [lemmatizer.lemmatize(word, wordnet_map.get(pos[0], wordnet.NOUN)) for word, pos in pos_tagged_text])

    text = lemmatize_words(text)
    return text