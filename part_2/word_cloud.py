# %%
# Necessary Imports
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
# %%
# Create a function that'll create the word cloud

def generate_weighted_wordcloud_from_dataframe(dataframe, text_column, score_column):    
    # Calculate the maximum and minimum scores
    max_score = dataframe[score_column].max()
    min_score = dataframe[score_column].min()
    
    # Apply a scaling factor to the scores based on the range of scores
    scale_factor = 100 / (max_score - min_score) if max_score != min_score else 1
    scores = {word: (score - min_score) * scale_factor for word, score in zip(dataframe[text_column], dataframe[score_column])}
    
    # Generate a word cloud image with weighted sizes
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(scores)

    # Display the generated image:
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

def unzip_my_file(zip_absolute_file_path):
    import zipfile
    import os

    directory = os.path.dirname(zip_absolute_file_path)
    file_name = os.path.splitext(os.path.basename(zip_absolute_file_path))[0]

    extract_dir = os.path.join(directory, file_name)
    os.makedirs(extract_dir, exist_ok=True)

    with zipfile.ZipFile(zip_absolute_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)


# %%
# unzip the zipped file
unzip_my_file('comments_containing_skills_full_scrape.zip')

# %%
# Read in the dataframe

df = pd.read_csv(r'F:\git\cuny-msds-project-3\part_2\comments_containing_skills_full_scrape\comments_containing_skills_full_scrape .csv', usecols=['word','score','Skills'])

# Count the number of occurances per word
reddit_df = df[['word','score']].groupby('word').count().reset_index().sort_values('score', ascending = False)

reddit_df.head()

reddit_df.head()
# %%
# Get the AFINN dataset
nrc = pd.read_csv(r'nrc.csv', usecols=['word','sentiment'])
nrc.head()

# %%
# Combine Afinn and the words dataset
out = reddit_df.merge(
    nrc,
    on = 'word'
)

out.head()
# %%
# Aggregate again but this time on the sentiment
wc_sentiment_df = out.groupby('sentiment').sum().reset_index().drop(columns='word')

wc_sentiment_df = wc_sentiment_df[~wc_sentiment_df['sentiment'].isin(['positive','negative'])].sort_values('score', ascending=False)

wc_sentiment_df
# %%
generate_weighted_wordcloud_from_dataframe(wc_sentiment_df, 'sentiment', 'score')
# %%
# Create another word cloud with the skills dataframe
wc_skill_df = df[df['Skills'].notna()][['Skills','word']].groupby('Skills').count().reset_index().sort_values('word', ascending=False).rename(columns={'word':'score'})

wc_skill_df

# %%
generate_weighted_wordcloud_from_dataframe(wc_skill_df.head(10), 'Skills','score')
# %%
