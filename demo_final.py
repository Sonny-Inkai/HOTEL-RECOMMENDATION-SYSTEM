import streamlit as st
from streamlit_searchbar import streamlit_searchbar
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd
import numpy as np 
import re
import pickle
from PIL import Image
import underthesea
from underthesea import word_tokenize
#
user_rating_matrix = pickle.load(open(r"C:\Users\THANG\source\repos\PythonApplication1\pkl_file\ensemble_model.pkl", "rb"))
hotel = pickle.load(open(r"C:\Users\THANG\source\repos\PythonApplication1\pkl_file\hotel.pkl", "rb"))
item_infor = hotel.drop_duplicates(subset=['HotelID']).sort_values(by=['HotelID'])
userid = pd.DataFrame(hotel['UserID'].values, columns=['UserID']).drop_duplicates().sort_values(by='UserID')
def get_img(itemid):
    path = 'C:\\Users\\THANG\\source\\repos\\PythonApplication1\\image\\img\\'
    if itemid <= 1000: 
        return path + str(itemid) + '.jpeg'
    elif 1000 < itemid <=2000:
        return path + str(itemid-1000) + '.jpeg'
    elif 2000 < itemid <=3000:
        return path + str(itemid-2000) + '.jpeg'
    elif 3000 < itemid <=4000:
        return path + str(itemid-3000) + '.jpeg'
    elif 4000 < itemid <=5000:
        return path + str(itemid-4000) + '.jpeg'
def get_hotel_name(item_infor, itemid):
    return item_infor[item_infor['HotelID'] == itemid]['Name Hotel'].values[0]


def get_address(item_infor, itemid):
    return item_infor[item_infor['HotelID'] == itemid]['Address'].values[0]


def get_description(item_infor, itemid):
    return item_infor[item_infor['HotelID'] == itemid]['Descriptions'].values[0]


def get_url(item_infor, itemid):
    return item_infor[item_infor['HotelID'] == itemid]['URL Hotel'].values[0]
def get_infor_item(item_infor, itemid):
    infor = []
    infor.append(get_img(itemid))
    infor.append(get_hotel_name(item_infor, itemid))
    infor.append(get_address(item_infor, itemid))
    infor.append(get_description(item_infor, itemid))
    infor.append(get_url(item_infor, itemid))
    return infor
def get_recommendation_4user(user_rating_matrix, usersid, topk, item_infor):
    rating_list = list(enumerate(user_rating_matrix[usersid, :]))
    sorted_rating = sorted(rating_list, key=lambda x: x[1], reverse=True)
    list_item = [item[0] for item in sorted_rating[:topk]]

    list_item_infor = []
    for itemid in list_item:
        list_item_infor.append(get_infor_item(item_infor, itemid))
    return list_item_infor
def show_recommendations(user_rating_matrix, userid, topk, item_infor):
    if userid < user_rating_matrix.shape[0]:
        list_item_infor = get_recommendation_4user(user_rating_matrix, userid, topk, item_infor)
    else:
        st.error("UserID không hợp lệ.")
        return []

    for item_infor in list_item_infor:
        col1,col2 = st.columns([0.6,0.4], gap='small')

        with col1:
            path = item_infor[0]
            image = Image.open(path)
            st.image(image, caption = '', output_format='JPEG', use_column_width=True)
        
        with col2:
            st.markdown(f'<p class="name">{item_infor[1]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="address">{item_infor[2]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="description">{item_infor[3][:300]}...</p>', unsafe_allow_html=True)
            st.markdown(f'[Go to Website]({item_infor[4]})', unsafe_allow_html=True)
            st.markdown('------------')
def main():
    #Widget nhập tên người dùng và mật khẩu
    username = st.sidebar.text_input("User")
    #
    password = st.sidebar.text_input("Password", type="password")

    # Widget button để xử lý đăng nhập
    if st.sidebar.button("Sign in"):
        userid_ = int(username)
        if is_user_authenticated(userid_, userid_):
            st.success("Sign in successfully!")
            st.text("Hotels you might like")
            # Thực hiện các hành động sau khi đăng nhập thành công
            show_recommendations(user_rating_matrix, userid_,10, item_infor)
        else:
            st.error("Unknown user name or bad password")
def is_user_authenticated(username, password):
    # Kiểm tra đăng nhập, bạn cần thay thế kiểm tra này bằng hệ thống đăng nhập thực tế của bạn
    return (username in userid["UserID"].values)
#
def convert_it(a):
  return int(re.sub('[^\w\s]', '', str(list(a.keys()))))
def csr_to_list(csr_matrix):
  l_list = []
  num = len(csr_matrix.data)
  for i in range(num):
    l_list.append({'index': csr_matrix.indices[i],'values': csr_matrix.data[i]})
  return l_list
def hotel_by_location(location, num_of_rec):
  location = word_tokenize(location, format = 'text')
  for i in range(len(list_loc)):
    temp = word_tokenize(list_loc[i], format = 'text')
    if(location == temp):
      rec_list = []
      hotel_list = hotel[hotel['Location'] == list_loc[i]]
      mean_rating = hotel_list.groupby('HotelID')['Rating'].mean()
      mean_rating = mean_rating.sort_values(ascending = False)
      list_Id = mean_rating[:num_of_rec]
      list_Id = list_Id.index.tolist()
      for j in range(num_of_rec):
        rec_list.append({list_Id[j]: mapping_1[mapping_3[list_Id[j]]]})
      return rec_list
def loc_search_hotel(location, search, num):
  location = word_tokenize(location, format = 'text')
  for i in range(len(list_loc)):
    temp = word_tokenize(list_loc[i], format = 'text')
    if(location == temp):
      list_for_rec = []
      list_score = []
      search = search.lower()
      search = re.sub('[^\w\s]', ' ', str(search))
      search = word_tokenize(search, format = 'text')
      df_for_vectorizing = hotel_new_1[hotel_new_1['Location'] == list_loc[i]]
      mapping_4 = pd.Series(df_for_vectorizing['Name Hotel'], df_for_vectorizing.index)
      mapping_5 = pd.Series(df_for_vectorizing['HotelID'], df_for_vectorizing.index)
      df_for_vectorizing = df_for_vectorizing.reset_index(drop = True)
      mapping_6 = pd.Series(hotel_new_1[hotel_new_1['Location'] == list_loc[i]].index, df_for_vectorizing.index)
      df_for_vectorizing_temp = df_for_vectorizing['tags']
      df_for_vectorizing_temp.loc[len(df_for_vectorizing)] = search + ' ' + location
      vectorizer = TfidfVectorizer()
      tags_matrix = vectorizer.fit_transform(df_for_vectorizing_temp)
      similarities = linear_kernel(tags_matrix, tags_matrix, dense_output = False)
      ind = (len(df_for_vectorizing_temp) - 1)
      list_dict = similarities[ind]
      list_dict = csr_to_list(list_dict)
      list_dict = sorted(list_dict, key = lambda x: x['values'], reverse = True)[1:num + 1]
      for j in range(len(list_dict)):
        list_dict[j]['index'] = list_dict[j]['index'].astype(np.int64)
      for i in range(len(list_dict)):
        list_for_rec.append({mapping_5[mapping_6[list_dict[i]['index']]]: mapping_4[mapping_6[list_dict[i]['index']]]})
        list_score.append(list_dict[i]['values'])
      return list_for_rec, list_score
def rec_by_clicked(hotel_clicked_id):
      location = hotel_new_1[hotel_new_1['HotelID'] == hotel_clicked_id]['Location'].values[0]
      list_for_rec = []
      df_for_vectorizing = hotel_new_1[hotel_new_1['Location'] == location]
      mapping_4 = pd.Series(df_for_vectorizing['Name Hotel'], df_for_vectorizing.index)
      mapping_5 = pd.Series(df_for_vectorizing['HotelID'], df_for_vectorizing.index)
      mapping_51 = pd.Series(df_for_vectorizing.index, df_for_vectorizing['HotelID'])
      df_for_vectorizing = df_for_vectorizing.reset_index(drop = True)
      mapping_6 = pd.Series(hotel_new_1[hotel_new_1['Location'] == location].index, df_for_vectorizing.index)
      df_for_vectorizing_temp = df_for_vectorizing['tags']
      vectorizer = TfidfVectorizer()
      tags_matrix = vectorizer.fit_transform(df_for_vectorizing_temp)
      similarities = linear_kernel(tags_matrix, tags_matrix, dense_output = False)
      ind = mapping_51[hotel_clicked_id]  
      list_dict = similarities[ind]
      list_dict = csr_to_list(list_dict)
      list_dict = sorted(list_dict, key = lambda x: x['values'], reverse = True)[:5]
      for j in range(len(list_dict)):
        list_dict[j]['index'] = list_dict[j]['index'].astype(np.int64) 
      for i in range(len(list_dict)):
        list_for_rec.append({mapping_5[mapping_6[list_dict[i]['index']]]: mapping_4[mapping_6[list_dict[i]['index']]]})
      return list_for_rec
#pickle file loading objects
hotel_info = pickle.load(open(r"C:\Users\THANG\source\repos\PythonApplication1\pkl_file\hotel_info.pkl", "rb"))
mapping_1 = pickle.load(open(r"C:\Users\THANG\source\repos\PythonApplication1\pkl_file\mapping_1.pkl", "rb"))
mapping_2 = pickle.load(open(r"C:\Users\THANG\source\repos\PythonApplication1\pkl_file\mapping_2.pkl", "rb"))
mapping_3 = pd.Series(hotel_info.index, hotel_info['HotelID'])
hotel_new_1 = pickle.load(open(r"C:\Users\THANG\source\repos\PythonApplication1\pkl_file\hotel_new_1.pkl", "rb"))
hotel_new = pickle.load(open(r"C:\Users\THANG\source\repos\PythonApplication1\pkl_file\hotel_new.pkl", "rb"))
list_loc = pickle.load(open(r"C:\Users\THANG\source\repos\PythonApplication1\pkl_file\list_loc.pkl", "rb"))
df_for_vectorizing = hotel_new['tags']
list_hotel = hotel.drop(columns = ['Location', 'UserID', 'User', 'Rating', 'tags'])
list_hotel = list_hotel.drop_duplicates()
list_hotel = list_hotel.drop_duplicates(subset='Name Hotel')
list_hotel = list_hotel.reset_index(drop = True)
st.header("Hotel recommender systems")
all_selections = list_loc
all_selections.loc[len(all_selections)] = '(None)'
selected_loc = st.selectbox("Select location:", all_selections)
searched_query = st.text_input('Type the query and press Enter:')
st.write('Result for: ',searched_query)
hotel_name, score = loc_search_hotel(selected_loc, searched_query, 10)
#
def displaying_process(hotel_name1):
    list_testtt = []
    for i in range(len(hotel_name1)):
        list_testtt.append(convert_it(hotel_name1[i]))
    rec_list = []
    for i in range(len(list_testtt)):
        row = []
        for j in range(len(list_testtt)):
            row.append(0)
        rec_list.append(row)
    for i in range(len(list_testtt)):
        a = str(list_hotel[list_hotel['HotelID'] == list_testtt[i]]['Name Hotel'].values).strip('[]\'\\')
        b = str(list_hotel[list_hotel['HotelID'] == list_testtt[i]]['Descriptions'].values).strip('[]\'\\')
        c = str(list_hotel[list_hotel['HotelID'] == list_testtt[i]]['Address'].values).strip('[]\'\\')
        d = str(list_hotel[list_hotel['HotelID'] == list_testtt[i]]['URL Hotel'].values).strip('[]\'\\')
        rec_list[i] = (a, b, c, d)
    return list_testtt, rec_list
#   
#
list_testtt, rec_list = displaying_process(hotel_name)
#
st.markdown(
    """
    <style>
    button[kind="primary"] {
        background: none!important;
        border: none;
        padding: 0!important;
        color: black !important;
        text-decoration: none;
        cursor: pointer;
        border: none !important;
    }
    button[kind="primary"]:hover {
        text-decoration: none;
        color: black !important;
    }
    button[kind="primary"]:focus {
        outline: none !important;
        box-shadow: none !important;
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
#########
hotel_clicked_id = 0
if st.button("Enter"):
    num_for_rand = 0;
    for i in range(len(score)):
        col_1, col_2 = st.columns(2)
        with col_1:
            path_1 = f'C:\\Users\\THANG\\source\\repos\\PythonApplication1\\image\\img\\{random.randint(num_for_rand, num_for_rand + 99)}.jpeg'
            st.image(Image.open(path_1), caption = '', output_format='JPEG', use_column_width=True)
        with col_2:
            st.markdown(f'**Hotel ID**: {list_testtt[i]}')
            st.markdown(f'**Name Hotel**: {rec_list[i][0]}')
            st.markdown(f'**Hotel Description**: {rec_list[i][1][:300]}...')
            st.markdown(f'**Hotel Address**: {rec_list[i][2]}')
            st.markdown(f'**Sim Score**: {score[i]}')
            if st.link_button("Go to website", rec_list[i][3]):    
                pass
        num_for_rand = num_for_rand + 99
#if st.button('Home'):
#    hotel_clicked_id =  pickle.load(open(r"C:\Users\THANG\source\repos\PythonApplication1\pkl_file\hotel_clicked_id.pkl", "rb"))
#    hotel_clicked_id
#    if(hotel_clicked_id != 0):
#        clicked_loc = hotel_new_1[hotel_new_1['HotelID'] == hotel_clicked_id]['Location'].values[0]
#        st.markdown(f'<h1 style="font-size:30px;text-align:center;">Hotel in {clicked_loc}</h1>', unsafe_allow_html=True)
#        clicked_rec = rec_by_clicked(hotel_clicked_id)
#        num_for_rand = 0;
#        list_testt, rec_listt = displaying_process(clicked_rec)
#        col_c1, col_c2, col_c3, col_c4, col_c5  = st.columns(5)
#        with col_c1:
#            col_c11, col_c12 = st.columns(2)
#            with col_c11:
#                path = f'C:\\Users\\THANG\\source\\repos\\PythonApplication1\\image\\img\\{random.randint(num_for_rand, num_for_rand + 99)}.jpeg'
#                st.image(Image.open(path), caption = '', output_format='JPEG', use_column_width=True)
#            with col_c12:
#                st.markdown(f'**Hotel ID**: {list_testt[0]}')
#                st.markdown(f'**Name Hotel**: {rec_listt[0][0]}')
#                st.markdown(f'**Hotel Address**: {rec_listt[0][2]}')
#                if st.link_button("Go to website", rec_listt[0][3]):
#                    hotel_clicked_id = list_testt[0]
#                    pass
#        num_for_rand = num_for_rand + 99;
#        with col_c2:
#            col_c21, col_c22 = st.columns(2)
#            with col_c21:
#                path = f'C:\\Users\\THANG\\source\\repos\\PythonApplication1\\image\\img\\{random.randint(num_for_rand, num_for_rand + 99)}.jpeg'
##                st.image(Image.open(path), caption = '', output_format='JPEG', use_column_width=True)
#           with col_c22:
#                st.markdown(f'**Hotel ID**: {list_testt[1]}')
#                st.markdown(f'**Name Hotel**: {rec_listt[1][0]}')
#                st.markdown(f'**Hotel Address**: {rec_listt[1][2]}')
#                if st.link_button("Go to website", rec_listt[1][3]):
#                    hotel_clicked_id = list_testt[1]
#                    pass
#        num_for_rand = num_for_rand + 99;
#        with col_c3:
#            col_c31, col_c32 = st.columns(2)
#            with col_c11:
#                path = f'C:\\Users\\THANG\\source\\repos\\PythonApplication1\\image\\img\\{random.randint(num_for_rand, num_for_rand + 99)}.jpeg'
#                st.image(Image.open(path), caption = '', output_format='JPEG', use_column_width=True)
##            with col_c12:
#               st.markdown(f'**Hotel ID**: {list_testt[2]}')
#                st.markdown(f'**Name Hotel**: {rec_listt[2][0]}')
#                st.markdown(f'**Hotel Address**: {rec_listt[2][2]}')
#                if st.link_button("Go to website", rec_listt[2][3]):
#                    hotel_clicked_id = list_testt[2]
#                    pass
#        num_for_rand = num_for_rand + 99;
#        with col_c4:
#            col_c41, col_c42 = st.columns(2)
#            with col_c11:
#                path = f'C:\\Users\\THANG\\source\\repos\\PythonApplication1\\image\\img\\{random.randint(num_for_rand, num_for_rand + 99)}.jpeg'
#                st.image(Image.open(path), caption = '', output_format='JPEG', use_column_width=True)
#            with col_c12:
#                st.markdown(f'**Hotel ID**: {list_testt[3]}')
#                st.markdown(f'**Name Hotel**: {rec_listt[3][0]}')
#                st.markdown(f'**Hotel Address**: {rec_listt[3][2]}')
#                if st.link_button("Go to website", rec_listt[3][3]):
#                    hotel_clicked_id = list_testt[3]
#                    pass
#        num_for_rand = num_for_rand + 99;
#        with col_c5:
#            col_c51, col_c52 = st.columns(2)
#            with col_c11:
#                path = f'C:\\Users\\THANG\\source\\repos\\PythonApplication1\\image\\img\\{random.randint(num_for_rand, num_for_rand + 99)}.jpeg'
#                st.image(Image.open(path), caption = '', output_format='JPEG', use_column_width=True)
#            with col_c12:
#                st.markdown(f'**Hotel ID**: {list_testt[4]}')
#                st.markdown(f'**Name Hotel**: {rec_listt[4][0]}')
#                st.markdown(f'**Hotel Address**: {rec_listt[4][2]}')
#                if st.link_button("Go to website", rec_listt[4][3]):
#                    hotel_clicked_id = list_testt[4]
#                    pass
#        num_for_rand = num_for_rand + 99;
if __name__ == "__main__":
    main()


