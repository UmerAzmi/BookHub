import streamlit as st
from PIL import Image
import pandas as pd
import random
import numpy as np
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
image=Image.open('logo.png')
st.image(image)
st.title("-- Book Recommender System📔--")
st.markdown("Hey there! 📚 Excited about finding your next great read? BookHub is your personalized book buddy, crafting recommendations just for you based on what you love. We use nifty collaborative filtering tricks to offer up a handpicked selection of book titles that'll make your reading journey even more delightful! Plus, we've got a special treat for engineering enthusiasts with our unique section dedicated to recommending top-notch engineering books. Ready to dive in and discover your next favorite?")
st.subheader("Enter your Name")
user_name = st.text_input("")
Item_based = pd.read_csv('https://github.com/aasimshaikh98/BookHub/blob/master/item_based.csv?raw=true')
Item_based1 = pd.read_csv('https://github.com/aasimshaikh98/BookHub/blob/master/item_based1.csv?raw=true')
if user_name:
 ## Define the options
 options = ['Overall Library', 'Exclusive MU Engineering Library']
 ## Create the select box
 st.subheader("")
 st.subheader("Choose a section which you would like to explore")
 selected_option = st.radio('', options)
 if selected_option=='Overall Library':
  st.markdown("### ------------ Welcome to BookHub's Overall Library -----------")
  st.markdown(" Step into our Overall Library section, where an array of captivating reads awaits! From thrilling page-turners to heartwarming tales, there's a book for every mood and interest. Explore and discover your next favorite read today! 📚")
  st.subheader("Which Book are you looking for?")
  col=st.columns(1)
  book=col[0].text_input("##### Enter something related to the book you're looking !!!","")
  if book:
   # Applying TfidfVectorizer to the altered title column
   vectorizer =TfidfVectorizer()
   tfidf=vectorizer.fit_transform(Item_based['altered_title'])
   # Creating a function to return books with similar names to the query
   def similar_books(book_name:str):
    # The book name entered is converted into lower case and removing the additional characters and additional space using regular expressions
    book_name= re.sub('[^a-zA-Z0-9]',' ',book_name.lower())
    book_name=re.sub('\s+'," ",book_name)
    # Transforming the book name into TFIDF Vectorizer
    book_vector=vectorizer.transform([book_name])
    # Computing the similarities between the book name query vector and the tfid matrix
    similarity= cosine_similarity(book_vector,tfidf).flatten()
    # After getting the similarities, we are getting the top 20 book index similar to query using numpy arg partition
    similar_book_id = np.flip(np.argpartition(similarity,-20)[-20:])
    # With the book index of the books we are creating a dataframe
    similar_books_df = pd.DataFrame(columns=['Book-Title','Mean-Rating','Book-Author'])
    # using for loop to iterate over the similar book id list and appending the data to the similar_books_df
    for i in similar_book_id:
     similar_books_df = pd.concat([similar_books_df,pd.DataFrame(Item_based.iloc[i][['Book-Title','Mean-Rating','Book-Author']]).transpose()])
    similar_books_df.reset_index(drop=True,inplace=True)
    similar_books_df.drop_duplicates(inplace=True)
    similar_books_df['Book & Author'] = similar_books_df['Book-Title']+ '   '+'---'+'   '+['Mean-Rating']+ '   '+'---'+'   '+similar_books_df['Book-Author']
    # Returning the similar book Data Frame
    return similar_books_df
   final = similar_books(book)
   st.markdown("<hr>", unsafe_allow_html=True)
   d="List of recommendations"
   sm='📕'
   b='📓'
   p="✍🏻"
   s="⭐"
   st.subheader(f"{d} for {user_name} {sm}{b}{sm}")
   for i in range(len(final)):
    st.write(f"{b}{final.iloc[i]['Book-Title']}{b}---{s}{final.iloc[i]['Mean-Rating']}{s}---{p}{final.iloc[i]['Book-Author']}{p}")     
   st.subheader("Filter by ⭐ Ratings")
   rating = st.slider(" ", 0, 5)
   d="Here are recommendations filtered by ratings"
   sm='📕'
   b='📓'
   p="✍🏻"
   s="⭐"
   st.subheader(f"{d}{sm}{b}{sm}")
   if rating:
    for i in range(len(final)):
     if(final.iloc[i]['Mean-Rating'] == rating):
      #st.write(f"{b} {final.iloc[i]['Book-Title']}  --- {p}{final.iloc[i]['Book-Author']} ")
      st.write(f"{b}{final.iloc[i]['Book-Title']}{b} --- {s}{final.iloc[i]['Mean-Rating']}{s}---{p}{final.iloc[i]['Book-Author']}{p}")    
 else:
  st.markdown("### -- Welcome to BookHub's Exclusive Engineering Library --")
  st.markdown("Hey engineering fans! Welcome to our Exclusive Engineering Library, filled with books from Mumbai University! Learn about different subjects in various branches. Let's explore engineering together! 📚")
  st.markdown("#### Which Branch are you looking for")
  options = ['Information Technology', 'Computer Engineering', 'Civil Engineering', 'Mechanical Engineering', 'Electronics and Telecommunication']
  selected_branch = st.radio('', options)
  if selected_branch=='Information Technology':
   st.markdown("#### Which year to look for")
   year = st.slider(" ", 1, 4)
   if year==1: 
    st.markdown("#### View Syllabus for First Year Information Technology")
    def create_link(text, link):
     return f'<a href="{link}" target="_blank">{text}</a>'
     # Display the clickable link to open the PDF
    pdf_link = create_link("Syllabus for Semester 1 and Semester 2 (F.E.I.T)", "https://muquestionpapers.com/storage/syllabus/be_first-year-engineering_fe-all-branches-semester-2-rev-2019-c-scheme.pdf")
    st.markdown(pdf_link, unsafe_allow_html=True)
   if year==2: 
    st.markdown("#### View Syllabus for Second Year Information Technology")
    def create_link(text, link):
     return f'<a href="{link}" target="_blank">{text}</a>'
     # Display the clickable link to open the PDF
    pdf_link = create_link("Syllabus for Semester 3 and Semester 4 (S.E.I.T)", "https://drive.google.com/file/d/1x0Ct8YCAkOfQb9qhNGgv6j0EwJPQtcoO/view")
    st.markdown(pdf_link, unsafe_allow_html=True)
   if year==3: 
    st.markdown("#### View Syllabus for Third Year Information Technology")
    def create_link(text, link):
     return f'<a href="{link}" target="_blank">{text}</a>'
     # Display the clickable link to open the PDF
    pdf_link = create_link("Syllabus for Semester 5 and Semester 6 (T.E.I.T)", "https://drive.google.com/file/d/1Wjq5hT-ckDMoSyQCynaIL7lEp3Edx_nh/view")
    st.markdown(pdf_link, unsafe_allow_html=True) 
   if year==4: 
    st.markdown("#### View Syllabus for Final Year Information Technology ")
    def create_link(text, link):
     return f'<a href="{link}" target="_blank">{text}</a>'
     # Display the clickable link to open the PDF
    pdf_link = create_link("Syllabus for Semester 7 and Semester 8 (B.E.I.T)", "https://drive.google.com/file/d/1tEhZ99K9UHtoPZ391Ct0RvMlxCbwcmSJ/view")
    st.markdown(pdf_link, unsafe_allow_html=True)    
  if selected_branch=='Computer Engineering':
   st.markdown("#### Which year to look for")
   year = st.slider(" ", 1, 4)
   if year==1: 
    st.markdown("#### View Syllabus for First Year Computer Engineering")
    def create_link(text, link):
     return f'<a href="{link}" target="_blank">{text}</a>'
     # Display the clickable link to open the PDF
    pdf_link = create_link("Syllabus for Semester 1 and Semester 2 (F.E.C.S)", "https://muquestionpapers.com/storage/syllabus/be_first-year-engineering_fe-all-branches-semester-2-rev-2019-c-scheme.pdf")
    st.markdown(pdf_link, unsafe_allow_html=True)
   if year==2: 
    st.markdown("#### View Syllabus for Second Year Computer Engineering")
    def create_link(text, link):
     return f'<a href="{link}" target="_blank">{text}</a>'
     # Display the clickable link to open the PDF
    pdf_link = create_link("Syllabus for Semester 3 and Semester 4 (S.E.C.S)", "https://drive.google.com/file/d/11uHFmn0TaBt3RYibwUY8TnqARNmqFzDM/view")
    st.markdown(pdf_link, unsafe_allow_html=True)
   if year==3: 
    st.markdown("#### View Syllabus for Third Year Computer Engineering")
    def create_link(text, link):
     return f'<a href="{link}" target="_blank">{text}</a>'
     # Display the clickable link to open the PDF
    pdf_link = create_link("Syllabus for Semester 5 and Semester 6 (T.E.C.S)", "https://drive.google.com/file/d/12yuGcyOc7xYVSSSfdN0JVo9izISQN2kR/view")
    st.markdown(pdf_link, unsafe_allow_html=True) 
   if year==4: 
    st.markdown("#### View Syllabus for Final Year Computer Engineering")
    def create_link(text, link):
     return f'<a href="{link}" target="_blank">{text}</a>'
     # Display the clickable link to open the PDF
    pdf_link = create_link("Syllabus for Semester 7 and Semester 8 (B.E.C.S)", "https://drive.google.com/file/d/1utccilpirkpw5qpj7mdPlHX0sDuH6rma/view")
    st.markdown(pdf_link, unsafe_allow_html=True)  
  if selected_branch=='Civil Engineering':
   st.markdown("#### Which year to look for")
   year = st.slider(" ", 1, 4)
   if year==1: 
    st.markdown("#### View Syllabus for First Year Civil Engineering")
    def create_link(text, link):
     return f'<a href="{link}" target="_blank">{text}</a>'
     # Display the clickable link to open the PDF
    pdf_link = create_link("Syllabus for Semester 1 and Semester 2 (F.E.Civil)", "https://muquestionpapers.com/storage/syllabus/be_first-year-engineering_fe-all-branches-semester-2-rev-2019-c-scheme.pdf")
    st.markdown(pdf_link, unsafe_allow_html=True)
   if year==2: 
    st.markdown("#### View Syllabus for Second Year Civil Engineering")
    def create_link(text, link):
     return f'<a href="{link}" target="_blank">{text}</a>'
     # Display the clickable link to open the PDF
    pdf_link = create_link("Syllabus for Semester 3 and Semester 4 (S.E.Civil)", "https://drive.google.com/file/d/1-V0lOKQrt480YXV3M3ukqhCpC6qNH8vO/view")
    st.markdown(pdf_link, unsafe_allow_html=True)
   if year==3: 
    st.markdown("#### View Syllabus for Third Year Civil Engineering")
    def create_link(text, link):
     return f'<a href="{link}" target="_blank">{text}</a>'
     # Display the clickable link to open the PDF
    pdf_link = create_link("Syllabus for Semester 5 and Semester 6 (T.E.Civil)", "https://drive.google.com/file/d/1RQUuKTh7yieEZYFhu5liW6Xpt-Rmn7p9/view")
    st.markdown(pdf_link, unsafe_allow_html=True) 
   if year==4: 
    st.markdown("#### View Syllabus for Final Year Civil Engineering")
    def create_link(text, link):
     return f'<a href="{link}" target="_blank">{text}</a>'
     # Display the clickable link to open the PDF
    pdf_link = create_link("Syllabus for Semester 7 and Semester 8 (B.E.Civil)", "https://drive.google.com/file/d/1MlcID1lbp6rcyoa5nd09yNwD-uRwlb5T/view")
    st.markdown(pdf_link, unsafe_allow_html=True)  
  if selected_branch=='Mechanical Engineering':
   st.markdown("#### Which year to look for")
   year = st.slider(" ", 1, 4)
   if year==1: 
    st.markdown("#### View Syllabus for First Year Mechanical Engineering")
    def create_link(text, link):
     return f'<a href="{link}" target="_blank">{text}</a>'
     # Display the clickable link to open the PDF
    pdf_link = create_link("Syllabus for Semester 1 and Semester 2 (F.E.Mech)", "https://muquestionpapers.com/storage/syllabus/be_first-year-engineering_fe-all-branches-semester-2-rev-2019-c-scheme.pdf")
    st.markdown(pdf_link, unsafe_allow_html=True)
   if year==2: 
    st.markdown("#### View Syllabus for Second Year Mechanical Engineering")
    def create_link(text, link):
     return f'<a href="{link}" target="_blank">{text}</a>'
     # Display the clickable link to open the PDF
    pdf_link = create_link("Syllabus for Semester 3 and Semester 4 (S.E.Mech)", "https://drive.google.com/file/d/1ZGiisduJevFCIG74nzA1WvvymM9b6vXF/view")
    st.markdown(pdf_link, unsafe_allow_html=True)
   if year==3: 
    st.markdown("#### View Syllabus for Third Year Mechanical Engineering")
    def create_link(text, link):
     return f'<a href="{link}" target="_blank">{text}</a>'
     # Display the clickable link to open the PDF
    pdf_link = create_link("Syllabus for Semester 5 and Semester 6 (T.E.Mech)", "https://drive.google.com/file/d/1mMlfQL2N0vSPnGqAWzsjuCXHxCZPjHgx/view")
    st.markdown(pdf_link, unsafe_allow_html=True) 
   if year==4: 
    st.markdown("#### View Syllabus for Final Year Mechanical Engineering")
    def create_link(text, link):
     return f'<a href="{link}" target="_blank">{text}</a>'
     # Display the clickable link to open the PDF
    pdf_link = create_link("Syllabus for Semester 7 and Semester 8 (B.E.Mech)", "https://drive.google.com/file/d/1r_OARZNQjILXayw74qERVJyR8e4aRpwC/view")
    st.markdown(pdf_link, unsafe_allow_html=True)
  if selected_branch=='Electronics and Telecommunication':
   st.markdown("#### Which year to look for")
   year = st.slider(" ", 1, 4)
   if year==1: 
    st.markdown("#### View Syllabus for First Year Electronics and Telecommunication")
    def create_link(text, link):
     return f'<a href="{link}" target="_blank">{text}</a>'
     # Display the clickable link to open the PDF
    pdf_link = create_link("Syllabus for Semester 1 and Semester 2 (F.E.EXTC)", "https://muquestionpapers.com/storage/syllabus/be_first-year-engineering_fe-all-branches-semester-2-rev-2019-c-scheme.pdf")
    st.markdown(pdf_link, unsafe_allow_html=True)
   if year==2: 
    st.markdown("#### View Syllabus for Second Year Electronics and Telecommunication")
    def create_link(text, link):
     return f'<a href="{link}" target="_blank">{text}</a>'
     # Display the clickable link to open the PDF
    pdf_link = create_link("Syllabus for Semester 3 and Semester 4 (S.E.EXTC)", "https://drive.google.com/file/d/1mXnXFBtmfc0_UxjlEB5JyStln2ntmKgR/view")
    st.markdown(pdf_link, unsafe_allow_html=True)
   if year==3: 
    st.markdown("#### View Syllabus for Third Year Electronics and Telecommunication")
    def create_link(text, link):
     return f'<a href="{link}" target="_blank">{text}</a>'
     # Display the clickable link to open the PDF
    pdf_link = create_link("Syllabus for Semester 5 and Semester 6 (T.E.EXTC)", "https://drive.google.com/file/d/1EcJALzERJ4Ct48kSrThsGRm2T3va9DBS/view")
    st.markdown(pdf_link, unsafe_allow_html=True) 
   if year==4: 
    st.markdown("#### View Syllabus for Final Year Electronics and Telecommunication")
    def create_link(text, link):
     return f'<a href="{link}" target="_blank">{text}</a>'
     # Display the clickable link to open the PDF
    pdf_link = create_link("Syllabus for Semester 7 and Semester 8 (B.E.EXTC)", "https://drive.google.com/file/d/1mPm9roQ8jjalon52q9x_Zm4pdZf_30_-/view")
    st.markdown(pdf_link, unsafe_allow_html=True)  
  st.markdown("#### Which Subject Book are you looking for?")
  col=st.columns(1)
  book=col[0].text_input("##### Enter something related to the book you're looking !!!","")
  if book:
   # Applying TfidfVectorizer to the altered title column
   vectorizer =TfidfVectorizer()
   tfidf=vectorizer.fit_transform(Item_based1['altered_title'])
   # Creating a function to return books with similar names to the query
   def similar_books(book_name:str):
    # The book name entered is converted into lower case and removing the additional characters and additional space using regular expressions
    book_name= re.sub('[^a-zA-Z0-9]',' ',book_name.lower())
    book_name=re.sub('\s+'," ",book_name)
    # Transforming the book name into TFIDF Vectorizer
    book_vector=vectorizer.transform([book_name])
    # Computing the similarities between the book name query vector and the tfid matrix
    similarity= cosine_similarity(book_vector,tfidf).flatten()
    # After getting the similarities, we are getting the top 5 book index similar to query using numpy arg partition
    similar_book_id = np.flip(np.argpartition(similarity,-5)[-5:])
    # With the book index of the books we are creating a dataframe
    similar_books_df = pd.DataFrame(columns=['Book-Title','Book-Author'])
    # using for loop to iterate over the similar book id list and appending the data to the similar_books_df
    for i in similar_book_id:
     similar_books_df = pd.concat([similar_books_df,pd.DataFrame(Item_based1.iloc[i][['Book-Title','Book-Author']]).transpose()])
    similar_books_df.reset_index(drop=True,inplace=True)
    similar_books_df.drop_duplicates(inplace=True)
    similar_books_df['Book & Author'] = similar_books_df['Book-Title']+ '   '+'---'+'   '+similar_books_df['Book-Author']
    # Returning the similar book Data Frame
    return similar_books_df
   final = similar_books(book)
   st.markdown("<hr>", unsafe_allow_html=True)
   d="List of recommendations"
   sm='📕'
   b='📓'
   p="✍🏻"
   s="⭐"
   st.subheader(f"{d} for {user_name} {sm}{b}{sm}")
   for i in range(len(final)):
    st.write(f"{b}{final.iloc[i]['Book-Title']}{b}---{p}{final.iloc[i]['Book-Author']}{p}")   