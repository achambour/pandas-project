import pandas as pd
import random
pd.set_option('display.max_colwidth', None)
df = pd.read_csv('/Users/anastasiachambour/Desktop/jeopardy_starting/jeopardy.csv')

#rename columns for convenience
df = df.rename(
  columns={
    'Show Number': 'show_number',
    ' Air Date': 'air_date',
    ' Round': 'round',
    ' Category': 'category',
    ' Value': 'value',
    ' Question': 'question',
    ' Answer': 'answer'
  }
)

#lambda function for reference only
in_string = lambda lst, stri: all(x in stri for x in lst)

#check if the elements of the list are in each of the questions. This creates a new column : is_in_question
lst = ['Computer']
df['is_in_question'] = df.question.apply(lambda row: all(word.lower() in row.lower() for word in lst))

#nnumber of questions containing word(s) in list
contains_words_lst = df.is_in_question.sum()
print(str(contains_words_lst) + ' questions contain the word(s): ' + ', '.join(lst))

#mean value of all questions containing the word(s) in list
df['float_value'] = df.value.apply(lambda row: row.replace('$', '').replace(',','').replace('None','0'))
df['float_value'] = pd.to_numeric(df['float_value'], downcast='float')
df_containing_words = df[df.is_in_question == True]
print(str(df_containing_words.float_value.mean()) + ' is the mean value of all questions containing the word(s): ' + ','.join(lst))

#number of unique answers to each question containing the word(s) in list
answer_series = df_containing_words.answer
n_answers = pd.Series.value_counts(answer_series)
print(str(n_answers.count()) + ' unique answers to the questions containing the words:' + ', '.join(lst))

#no questions containing the word(s) in list for each year
df_time = df_containing_words[['air_date', 'question']].rename(columns= {'air_date': 'year'})
df_time['year'] = df_time.year.apply(lambda row: row[:4])
df_time = df_time.groupby('year').question.count()
print(df_time)

#number of each categories per round
category_per_round = df[['round', 'category']].groupby(['round', 'category']).category.count().sort_values(ascending=False)
print(category_per_round)

#QUIZZ:
print('~~~ Quizz Time ~~~ \n')
print('~~~ You have 3 trials for each question ~~~ \n')
question = random.choice(df.question.unique())
print(question)
answer = df.loc[df['question']==question, 'answer'].iloc[0]
i = 0 #counter for 3 trials
while i<3:
    user_answer = input()
    if user_answer == answer:
        print('Correct answer')
        break
    else:
        if i<2:
            print('Incorrect answer. You have {} more trials'.format(str(2-i)))
        if i==2:
            print('You have lost the game')
    i = i+1

