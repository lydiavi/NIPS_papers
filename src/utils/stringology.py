import re

import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download("stopwords")
nltk.download("punkt")


nltk.download("wordnet")
stop = stopwords.words("english")


lemmatizer = WordNetLemmatizer()


def cleaned_text(text) -> str:
    """_summary_.

    Args:
        text (_type_): _description_

    Returns:
        str: _description_
    """
    clean = re.sub("\n", " ", text)
    clean = clean.lower()
    clean = re.sub(r"[~.,%/:;?_&+*=!-]", " ", clean)
    clean = re.sub("[^a-z]", " ", clean)
    clean = clean.lstrip()
    clean = re.sub(r"\s{2,}", " ", clean)
    return clean


def preprocess_text(s: pd.Series) -> pd.Series:
    """_summary_.

    Args:
        s (pd.Series): _description_

    Returns:
        pd.Series: _description_
    """
    s_clean = s.apply(cleaned_text)
    s_clean_token = s_clean.apply(
        lambda x: nltk.word_tokenize(" ".join([word for word in x.split() if word not in (stop)]))
    )

    s_clean_lem = s_clean_token.apply(
        lambda x: " ".join([lemmatizer.lemmatize(word) for word in x])
    )
    return s_clean_lem
