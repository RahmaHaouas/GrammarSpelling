# -*- coding: utf-8 -*-
"""LearningDifficulties.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1b3HqHzTlJgrHbwdMN9psyhHyHb_7ZVJG

**Import**
"""

import pandas as pd

"""**Dataset**"""

df = pd.read_csv('/content/drive/MyDrive/Grammar Correction.csv', sep=',')
print(f'Shape of data= {df.shape}')

df.head()

"""**Initial Data Analysis**"""

summary = df.describe(include='all')
summary

missing_values = df.isnull().sum()
missing_values

"""**Data Cleaning**"""

df_clean = df.drop_duplicates()
print(f'Shape of df_clean= {df_clean.shape}')

df_clean['Ungrammatical Statement'] = df_clean['Ungrammatical Statement'].str.strip()
df_clean['Standard English'] = df_clean['Standard English'].str.strip()

df_clean['Ungrammatical Statement'] = df_clean['Ungrammatical Statement'].str.replace(r'^\d+\.\s+', '', regex=True)
df_clean['Standard English'] = df_clean['Standard English'].str.replace(r'^\d+\.\s+', '', regex=True)

print(f'Shape of df_clean= {df_clean.shape}')

"""**Exploratory Data Analysis**"""

error_counts = df_clean['Error Type'].value_counts()
error_counts

df_clean['Ungrammatical Length'] = df_clean['Ungrammatical Statement'].apply(len)
df_clean['Standard Length'] = df_clean['Standard English'].apply(len)

df_clean.head()

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

plt.figure(figsize=(14, 10))
error_type_plot = sns.countplot(y=df_clean['Error Type'], order=df_clean['Error Type'].value_counts().index)
error_type_plot.set_title('Frequency of Each Type of Grammatical Error')
error_type_plot.set_xlabel('Frequency')
error_type_plot.set_ylabel('Error Type')

plt.figure(figsize=(14, 6))
plt.hist(df_clean['Ungrammatical Length'], bins=50, alpha=0.5, label='Ungrammatical Statements')
plt.hist(df_clean['Standard Length'], bins=50, alpha=0.5, label='Standard English Statements')
plt.title('Distribution of Sentence Lengths')
plt.xlabel('Length of Sentence')
plt.ylabel('Frequency')
plt.legend()


plt.show()

from collections import Counter
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')

# Calculate word frequency
def word_frequency(sentences):
    words = []
    for sentence in sentences:
        words.extend(word_tokenize(sentence.lower()))
    return Counter(words)

# Calculate word frequency for both ungrammatical and corrected statements
ungrammatical_freq = word_frequency(df_clean['Ungrammatical Statement'])
corrected_freq = word_frequency(df_clean['Standard English'])

# Get the top 20 most frequent words in each category
top_ungrammatical = ungrammatical_freq.most_common(20)
top_corrected = corrected_freq.most_common(20)

top_ungrammatical_df = pd.DataFrame(top_ungrammatical, columns=['Word', 'Frequency'])
top_corrected_df = pd.DataFrame(top_corrected, columns=['Word', 'Frequency'])

# Bar Graphs
plt.figure(figsize=(15, 6))

# Ungrammatical Statements
plt.subplot(1, 2, 1)
sns.barplot(x='Frequency', y='Word', data=top_ungrammatical_df)
plt.title('Top Words in Ungrammatical Statements')

# Corrected Statements
plt.subplot(1, 2, 2)
sns.barplot(x='Frequency', y='Word', data=top_corrected_df)
plt.title('Top Words in Corrected Statements')

plt.tight_layout()
plt.show()

# Displaying in Table Format
print("Top Words in Ungrammatical Statements:")
print(top_ungrammatical_df)

print("\nTop Words in Corrected Statements:")
print(top_corrected_df)

from nltk import pos_tag

nltk.download('averaged_perceptron_tagger')

# Function to perform POS tagging
def pos_tag_sentences(sentences):
    tagged_sentences = []
    for sentence in sentences:
        tokens = word_tokenize(sentence)
        tagged = pos_tag(tokens)
        tagged_sentences.extend(tagged)
    return tagged_sentences

# POS tagging for ungrammatical and corrected sentences
tagged_ungrammatical = pos_tag_sentences(df_clean['Ungrammatical Statement'])
tagged_corrected = pos_tag_sentences(df_clean['Standard English'])

# Count the frequency of each POS tag
ungrammatical_pos_counts = pd.Series([tag for _, tag in tagged_ungrammatical]).value_counts()
corrected_pos_counts = pd.Series([tag for _, tag in tagged_corrected]).value_counts()

# Display or visualize the results
print(ungrammatical_pos_counts)
print(corrected_pos_counts)

pos_df = pd.DataFrame({
    'Ungrammatical': ungrammatical_pos_counts,
    'Corrected': corrected_pos_counts
}).fillna(0)

# Plot
plt.figure(figsize=(20, 10))  # Adjust the size as necessary
pos_df.plot(kind='bar', color=['skyblue', 'salmon'])
plt.title('Frequency of POS Tags in Ungrammatical vs. Corrected Sentences')
plt.xlabel('POS Tags')
plt.ylabel('Frequency')
plt.xticks(rotation=90)
plt.legend(title='Sentence Type')
plt.tight_layout()
plt.show()

!pip install textstat

import textstat

# Compute the readability scores for ungrammatical sentences
ungrammatical_readability = [textstat.flesch_reading_ease(sentence) for sentence in df_clean['Ungrammatical Statement']]

# Compute the readability scores for corrected sentences
corrected_readability = [textstat.flesch_reading_ease(sentence) for sentence in df_clean['Standard English']]

# Calculate the average score for each or compare scores sentence by sentence
avg_ungrammatical_score = sum(ungrammatical_readability) / len(ungrammatical_readability)
avg_corrected_score = sum(corrected_readability) / len(corrected_readability)

# Output the average Flesch Reading Ease scores
print(f'Average Readability Score for Ungrammatical Sentences: {avg_ungrammatical_score}')
print(f'Average Readability Score for Corrected Sentences: {avg_corrected_score}')

!pip install python-Levenshtein

import numpy as np
from Levenshtein import distance as levenshtein_distance

# Assuming `ungrammatical_sentences` and `corrected_sentences` are lists of sentences
difficulty_index = []

for ungrammatical, corrected in zip(df_clean['Ungrammatical Statement'], df_clean['Standard English']):
    # Calculate the Levenshtein distance between each pair of sentences
    edit_distance = levenshtein_distance(ungrammatical, corrected)
    # Normalize by the length of the original (ungrammatical) sentence
    normalized_difficulty = edit_distance / max(len(ungrammatical), len(corrected))
    difficulty_index.append(normalized_difficulty)

# Convert to a numpy array for easier analysis
difficulty_index = np.array(difficulty_index)

# Define difficulty levels based on the index
difficulty_levels = ['Easy' if x < 0.2 else 'Medium' if x < 0.5 else 'Hard' for x in difficulty_index]

# Count how many sentences fall into each difficulty level
difficulty_counts = Counter(difficulty_levels)

difficulty_counts

from nltk import bigrams, trigrams
from collections import Counter

tokens = [nltk.word_tokenize(sentence.lower()) for sentence in df_clean['Ungrammatical Statement']]

# Generate bi-grams and tri-grams
bi_grams = [gram for sentence in tokens for gram in bigrams(sentence)]
tri_grams = [gram for sentence in tokens for gram in trigrams(sentence)]

# Count the frequency of each bi-gram and tri-gram
bi_gram_freq = Counter(bi_grams)
tri_gram_freq = Counter(tri_grams)

# Get the most common bi-grams and tri-grams
most_common_bi = bi_gram_freq.most_common(10)
most_common_tri = tri_gram_freq.most_common(10)

most_common_bi, most_common_tri

bi_grams, bi_freq = zip(*most_common_bi)
tri_grams, tri_freq = zip(*most_common_tri)

# Convert N-gram tuples to strings
bi_grams_str = [' '.join(gram) for gram in bi_grams]
tri_grams_str = [' '.join(gram) for gram in tri_grams]

plt.figure(figsize=(15, 10))

# Plotting bi-grams
plt.subplot(1, 2, 1)
plt.barh(bi_grams_str, bi_freq, color='skyblue')
plt.xlabel('Frequency')
plt.title('Top 10 Bi-grams in Ungrammatical Sentences')

# Plotting tri-grams
plt.subplot(1, 2, 2)
plt.barh(tri_grams_str, tri_freq, color='salmon')
plt.xlabel('Frequency')
plt.title('Top 10 Tri-grams in Ungrammatical Sentences')

plt.tight_layout()
plt.show()

from textblob import TextBlob

ungrammatical_sentiments = [TextBlob(sentence).sentiment.polarity for sentence in df_clean['Ungrammatical Statement']]
corrected_sentiments = [TextBlob(sentence).sentiment.polarity for sentence in df_clean['Standard English']]

# Calculate average sentiment, compare individual sentence sentiment.
avg_ug_sentiment = sum(ungrammatical_sentiments) / len(ungrammatical_sentiments)
avg_corr_sentiment = sum(corrected_sentiments) / len(corrected_sentiments)

print(f'Average Sentiment for Ungrammatical Sentences: {avg_ug_sentiment}')
print(f'Average Sentiment for Corrected Sentences: {avg_corr_sentiment}')

# Sentiment scores
scores = [avg_ug_sentiment, avg_corr_sentiment]
labels = ['Ungrammatical Sentences', 'Corrected Sentences']

plt.figure(figsize=(8, 6))
plt.bar(labels, scores, color=['blue', 'green'])
plt.ylabel('Average Sentiment Score')
plt.title('Comparison of Average Sentiment Scores')
plt.ylim(0, 0.2)
plt.show()

from nltk import word_tokenize

nltk.download('punkt')

def align_and_find_changes(sentence1, sentence2):
    tokens1 = word_tokenize(sentence1)
    tokens2 = word_tokenize(sentence2)
    max_len = max(len(tokens1), len(tokens2))
    aligned_tokens1 = tokens1 + [''] * (max_len - len(tokens1))
    aligned_tokens2 = tokens2 + [''] * (max_len - len(tokens2))

    changes = []
    for token1, token2 in zip(aligned_tokens1, aligned_tokens2):
        if token1 != token2:
            changes.append((token1, token2))
    return changes

# Apply the function to each pair of sentences
df_clean['Changes'] = df_clean.apply(lambda row: align_and_find_changes(row['Ungrammatical Statement'], row['Standard English']), axis=1)

# View the DataFrame with identified changes
df_clean.head()

from collections import Counter

# Flatten the list of changes and count the occurrences
all_changes = [change for changes in df_clean['Changes'] for change in changes]
change_counter = Counter(all_changes)

# Display the most common changes
most_common_changes = change_counter.most_common(20)
print("Most Common Changes:")
for change, frequency in most_common_changes:
    print(f"{change}: {frequency}")

changes, frequencies = zip(*most_common_changes)

# Convert change tuples to string format for labeling
change_labels = [f'{original} -> {corrected}' for original, corrected in changes]


plt.figure(figsize=(15, 8))
plt.barh(change_labels, frequencies)
plt.xlabel('Frequency')
plt.title('Most Common Grammatical Corrections')
plt.gca().invert_yaxis()  # To display the highest frequency at the top
plt.show()

def categorize_change(change):
    original, corrected = change
    if original == '':
        return 'Insertion'
    elif corrected == '':
        return 'Deletion'
    else:
        return 'Substitution'

df_clean['Change Types'] = df_clean['Changes'].apply(lambda changes: [categorize_change(change) for change in changes])
df_clean.head()

from collections import Counter

change_type_counter = Counter([change_type for change_types in df_clean['Change Types'] for change_type in change_types])

change_types, frequencies = zip(*change_type_counter.items())

plt.figure(figsize=(10, 6))
plt.bar(change_types, frequencies, color='teal')
plt.xlabel('Change Type')
plt.ylabel('Frequency')
plt.title('Frequency of Different Types of Grammatical Changes')
plt.show()

context_window = 2

def extract_context(sentence, index, window):
    words = nltk.word_tokenize(sentence)
    start = max(0, index - window)
    end = min(len(words), index + window + 1)
    return ' '.join(words[start:end])

df_clean['Contexts'] = df_clean.apply(lambda row: [extract_context(row['Ungrammatical Statement'], i, context_window) for i, _ in enumerate(nltk.word_tokenize(row['Ungrammatical Statement'])) if (row['Ungrammatical Statement'][i], row['Standard English'][i]) in row['Changes']], axis=1)
df_clean.head()

from wordcloud import WordCloud

# Flatten the list of contexts
all_contexts = [context for contexts in df_clean['Contexts'] for context in contexts]

# Join all contexts into a single string
all_contexts_string = ' '.join(all_contexts)

# Create a word cloud
wordcloud = WordCloud(width = 1000, height = 600,
                background_color ='white',
                min_font_size = 10).generate(all_contexts_string)

# Plot the word cloud
plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)

plt.show()