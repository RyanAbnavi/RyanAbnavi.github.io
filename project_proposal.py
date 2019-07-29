# Imports
import numpy as np
import pandas as pd

from plotly.offline import iplot, init_notebook_mode
import plotly.graph_objs as go

init_notebook_mode(connected=True)

import re
import string
import math
import random
import time

from IPython.display import display

import warnings  
warnings.filterwarnings('ignore')

# Settings

pd.set_option('display.max_columns', 100, 'display.width', 1024)
pd.options.mode.chained_assignment = None

DATA_PATH = '../Input/'


# Import Professionals
professionals = pd.read_csv(DATA_PATH + 'professionals.csv')
professionals = professionals.rename(columns={'professionals_location': 'location', 
                                              'professionals_id': 'professional_id',
                                              'professionals_industry': 'industry', 
                                              'professionals_headline': 'headline', 
                                              'professionals_date_joined': 'date_joined'})

professionals["date_joined"] = pd.to_datetime(professionals["date_joined"], infer_datetime_format=True)
professionals['headline'] = professionals['headline'].fillna('')
professionals['industry'] = professionals['industry'].fillna('')
professionals['location'] = professionals['location'].fillna('')

# Import Students
students = pd.read_csv(DATA_PATH + 'students.csv')
students = students.rename(columns={'students_location': 'location',
                                    'students_id': 'student_id',
                                    'students_date_joined': 'date_joined'})

students["date_joined"] = pd.to_datetime(students["date_joined"], infer_datetime_format=True)
students["location"] = students["location"].fillna("")


# Import Questions
questions = pd.read_csv(DATA_PATH + 'questions.csv', 
                        parse_dates=['questions_date_added'], 
                        infer_datetime_format=True)

questions = questions.rename(columns={'questions_author_id': 'author_id',
                                      'questions_id' :'question_id',
                                      'questions_date_added': 'date_added', 
                                      'questions_title': 'title', 
                                      'questions_body': 'body', 
                                      'questions_processed':'processed'})

# Import Answers
answers = pd.read_csv(DATA_PATH + 'answers.csv', 
                      parse_dates=['answers_date_added'], 
                      infer_datetime_format=True)

answers = answers.rename(columns={'answers_author_id':'author_id',
                                  'answers_id':'answer_id',
                                  'answers_question_id': 'question_id', 
                                  'answers_date_added': 'date_added', 
                                  'answers_body': 'body'})


# Import Tags
tags = pd.read_csv(DATA_PATH + 'tags.csv')
tags = tags.rename(columns={"tags_tag_id":"tag_id",'tags_tag_name': 'name'})

# Import Comments
comments = pd.read_csv(DATA_PATH + 'comments.csv', 
                       parse_dates = ["comments_date_added"], 
                       infer_datetime_format=True )

comments = comments.rename(columns={'comments_author_id': 'author_id',
                                    'comments_id':'comment_id',
                                    'comments_parent_content_id': 'parent_content_id', 
                                    'comments_date_added': 'date_added', 
                                    'comments_body': 'body' })


# Import School Memberships
school_memberships = pd.read_csv(DATA_PATH + 'school_memberships.csv')
school_memberships = school_memberships.rename(columns={'school_memberships_school_id': 'school_id', 
                                                        'school_memberships_user_id': 'user_id'})


# Groups Memberships
group_memberships = pd.read_csv(DATA_PATH + 'group_memberships.csv')
group_memberships = group_memberships.rename(columns={'group_memberships_group_id': 'group_id', 
                                                      'group_memberships_user_id': 'user_id'})


# Emails
emails = pd.read_csv(DATA_PATH + 'emails.csv', 
                     parse_dates = ["emails_date_sent"], 
                     infer_datetime_format=True)

emails = emails.rename(columns={'emails_recipient_id':'recipient_id',
                                "emails_id":"email_id",
                                'emails_date_sent': 'date_sent', 
                                'emails_frequency_level': 'frequency_level'})


# Questions-related stats
tag_questions = pd.read_csv(DATA_PATH + 'tag_questions.csv',)
tag_questions = tag_questions.rename(columns={'tag_questions_tag_id': 'tag_id', 
                                              'tag_questions_question_id': 'question_id'})

# tag_users
tag_users = pd.read_csv(DATA_PATH + 'tag_users.csv',)
tag_users = tag_users.rename(columns={'tag_users_tag_id': 'tag_id', 
                                      'tag_users_user_id': 'user_id'})


# Questions score
question_scores = pd.read_csv(DATA_PATH + 'question_scores.csv')
question_scores = question_scores.rename(columns = {"id":"question_id", "score":"question_score"})
# question_scores.head()

# Answers score
answer_scores = pd.read_csv(DATA_PATH + 'answer_scores.csv')
answer_scores = answer_scores.rename(columns = {"id":"answer_id", "score":"answer_score"})
# answer_scores.head()

# Import matches
matches = pd.read_csv(DATA_PATH + "matches.csv")
matches = matches.rename(columns = {"matches_email_id" : "email_id", "matches_question_id":"question_id"})

# Import groups
groups = pd.read_csv(DATA_PATH + "groups.csv")
groups = groups.rename(columns = {"groups_id":"group_id", "groups_group_type":"group_type"})

# Professionals Activity
pros_without_answer = len(professionals) - answers['author_id'].nunique()

prosA = answers['author_id'].value_counts().sort_values()

one_answer = prosA[prosA.values==1].count()
twoto5_answer = prosA[(prosA.values>1) & (prosA.values<6)].count()
fiveto10_answer = prosA[(prosA.values>5) & (prosA.values<11)].count()
tento20_answer = prosA[(prosA.values>10) & (prosA.values<21)].count()
twenyto50_answer = prosA[(prosA.values>20) & (prosA.values<51)].count()
fiftymore_answer = prosA[(prosA.values>50)].count()

# First Plot
fig = {
  "data": [
    {
      "values": [pros_without_answer,
                 one_answer,
                 twoto5_answer, 
                 fiveto10_answer, 
                 tento20_answer, 
                 twenyto50_answer, 
                 fiftymore_answer],
      "labels": [
        "Professionals without answers",
        "only one answer",
        "2 to 5 answers",
        "5 to 10 answers",
        "10 to 20 answers",
        "20 to 50 answers",
        "more than 20 answers"
      ],
      "domain": {"column": 0},
      "name": "Professional activity",
      "hoverinfo":"label+percent+name",
      "hole": .6,
      "type": "pie"
    }],
  "layout": {
        "title":"Professional contribution in answering questions",
        "grid": {"rows": 1, "columns": 1},
        "annotations": [
            {
                "font": {
                    "size": 20
                },
                "showarrow": False,
                "text": " ",
                "x": 0.50,
                "y": 0.5
            }
        ]
    }
}
iplot(fig, filename='donut')

# Professional activitity over time
professionals["year"] = professionals["date_joined"].dt.year
professionals_joining_over_time = pd.DataFrame(professionals
                                           .groupby("year")["professional_id"]
                                           .count())
professionals_joining_over_time = professionals_joining_over_time.rename(columns = {"professional_id":"number of professionals added"})
professionals_joining_over_time = professionals_joining_over_time.reset_index()

total_number_of_pros = []
sum = 0
for i in range (len(professionals_joining_over_time)):
    sum+=professionals_joining_over_time["number of professionals added"].values[i]
    total_number_of_pros.append(sum)


professionals_joining_over_time["total_number_of_pros"] = total_number_of_pros

answers["year"] = answers["date_added"].dt.year
Active_professional_over_time =pd.DataFrame(answers.groupby("year")["author_id"].nunique()) 
Active_professional_over_time = Active_professional_over_time.rename(columns = {"author_id":"number of active professionals"})
Active_professional_over_time = Active_professional_over_time.reset_index()

pro = professionals_joining_over_time.merge(Active_professional_over_time)
pro["number of non-active professionals"] = pro["total_number_of_pros"]-pro["number of active professionals"]

# Second Plot

trace1 = go.Bar(
    x=pro["year"],
    y=pro["number of non-active professionals"],
    name='Inactive',
    marker=dict(
        color='rgb(55, 83, 109)'
    )
)
trace2 = go.Bar(
    x=pro["year"],
    y=pro["number of active professionals"],
    name='Active',
    marker=dict(
        color='rgb(26, 118, 255)'
    )
)
data = [trace1, trace2]
layout = go.Layout(
    title='Professionals Activity over Time',
    xaxis=dict(
        title='Year',
        titlefont=dict(
            size=16,
            color='rgb(107, 107, 107)'
        ),
        tickfont=dict(
            size=14,
            color='rgb(107, 107, 107)'
        )
    ),
    yaxis=dict(
        title='Number of Professionals',
        titlefont=dict(
            size=16,
            color='rgb(107, 107, 107)'
        ),
        tickfont=dict(
            size=14,
            color='rgb(107, 107, 107)'
        )
    ),
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    font=dict(
            family='sans-serif',
            size=16,
            color='#000'
        ),
    barmode='stack',
    bargap=0.15,
    bargroupgap=0.1
)

fig = go.Figure(data=data, layout=layout)
iplot(fig, filename='style-bar')



