# %%
import pandas as pd
from src.const import RAW_DATA_DIR
from src.dataloader.csv_loader import CSVLoader
from src.utils.stringology import preprocess_text
from gensim import corpora
from gensim.models.ldamodel import LdaModel

# %%
# https://www.kaggle.com/code/jl18pg052/word-embedding-word2vec-topic-modelling-lda#Text-Cleaning
loader = CSVLoader(RAW_DATA_DIR)
data = loader.read_filter_data(years=[2017])
authors_df = data["authors"]
paper_authors_df = data["paper_authors"]
papers_df = data["papers"]

# %%
papers_df.columns

papers_df["clean_title"] = preprocess_text(papers_df["title"])
papers_df["clean_abstract"] = preprocess_text(papers_df["abstract"])
papers_df["clean_paper_text"] = preprocess_text(papers_df["paper_text"])
# %%
dictionary = corpora.Dictionary(papers_df["clean_title"].apply(lambda x: x.split(" ")))
doc_term_matrix = [
    dictionary.doc2bow(rev) for rev in papers_df["clean_title"].apply(lambda x: x.split(" "))
]

# %%
lda_model = LdaModel(
    corpus=doc_term_matrix,
    id2word=dictionary,
    num_topics=10,
    random_state=100,
    chunksize=200,
    passes=100,
)
lda_model.print_topics()


# %%
def format_topics_sentences(ldamodel: LdaModel, corpus=None, texts=data):
    # Init output
    sent_topics_df = pd.DataFrame()

    # Get main topic in each document
    for i, row_list in enumerate(ldamodel[corpus]):
        row = row_list[0] if ldamodel.per_word_topics else row_list
        # print(row)
        row = sorted(row, key=lambda x: (x[1]), reverse=True)  # type: ignore
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = pd.concat([sent_topics_df,
                    pd.Series([int(topic_num), round(prop_topic, 4), topic_keywords])],
                )
            else:
                break
    sent_topics_df.columns = ["Dominant_Topic", "Perc_Contribution", "Topic_Keywords"]

    # Add original text to the end of the output
    contents = pd.Series(texts)
    sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
    return sent_topics_df


df_topic_sents_keywords = format_topics_sentences(
    ldamodel=lda_model, corpus=doc_term_matrix, texts=papers_df["clean_title"].apply(lambda x: x.split(" "))
)

# Format
df_dominant_topic = df_topic_sents_keywords.reset_index()
df_dominant_topic.columns = [
    "Document_No",
    "Dominant_Topic",
    "Topic_Perc_Contrib",
    "Keywords",
    "Text",
]
df_dominant_topic.head(10)

# %%
