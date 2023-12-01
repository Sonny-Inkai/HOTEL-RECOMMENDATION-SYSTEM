import streamlit as st
import pandas as pd
from PIL import Image
import pickle
#tải user rating prediction 
with open('C:\\Users\\Theba\\OneDrive\\Documents\\Recommendation System\\demo_project\\model\\ensemble_model.pkl', 'rb') as file:
    user_rating_matrix = pickle.load(file)

#user_rating_matrix

#tải thông tin của item
import pandas as pd
infor_matrix = pd.read_csv('C:\\Users\\Theba\\OneDrive\\Documents\\Recommendation System\\demo_project\\data\hotels_users_ratings.csv')
item_infor = infor_matrix.drop_duplicates(subset=['HotelID']).sort_values(by=['HotelID'])

#thông tin id của user
userid = pd.DataFrame(infor_matrix['UserID'].values, columns=['UserID']).drop_duplicates().sort_values(by='UserID')

def get_img(itemid):
    path = 'C:\\Users\\Theba\\OneDrive\\Documents\\Recommendation System\\demo_project\\img\\'
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
    
#------------------------------------------------------------------------------------------------------------------------
# Giả sử bạn có một dữ liệu người dùng và dữ liệu khuyến nghị
# Bạn cần thay thế dữ liệu thực tế của mình tại đây
st.markdown(
    """
    <style>
        #sidebar {
            background-color: #2a2a2a;
            padding: 20px;
            border-radius: 10px;
            color: #fff;
        }
        #sidebar .stButton {
            background-color: #007bff;
            color: #fff;
            border-radius: 5px;
            padding: 8px 12px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        #sidebar .stButton:hover {
            background-color: #0056b3;
        }
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    st.title("Trang web khuyến nghị")

    
    #Widget nhập tên người dùng và mật khẩu
    username = st.sidebar.text_input("Tên người dùng")
    #
    password = st.sidebar.text_input("Mật khẩu", type="password")

    # Widget button để xử lý đăng nhập
    if st.sidebar.button("Đăng nhập"):
        userid_ = int(username)
        if is_user_authenticated(userid_, userid_):
            st.success("Đăng nhập thành công!")
            # Thực hiện các hành động sau khi đăng nhập thành công
            show_recommendations(user_rating_matrix, userid_,10, item_infor)
        else:
            st.error("Tên người dùng hoặc mật khẩu không đúng.")



def is_user_authenticated(username, password):
    # Kiểm tra đăng nhập, bạn cần thay thế kiểm tra này bằng hệ thống đăng nhập thực tế của bạn
    return (username in userid["UserID"].values)

def login(username, password):
    if is_user_authenticated(username, password):
        st.sidebar.success("Đăng nhập thành công!")
        show_recommendations(user_rating_matrix, username, 10, item_infor)
    else:
        st.sidebar.error("Tên người dùng hoặc mật khẩu không đúng.")

def show_recommendations(user_rating_matrix, userid, topk, item_infor):
    # Thay đổi màu sắc và font chữ
    st.markdown("""
        <style>
            .name { color: #00ccff; font-weight: bold; }
            .address { color: #ff6600; }
            .description { color:  #ffffff; }
        </style>
    """, unsafe_allow_html=True)

    hover_css = """
    img:hover {
        transform: scale(1.05);
        transition: transform 0.3s ease-in-out;
        filter: brightness(80%);
    }
    """
    st.markdown(f"""<style>{hover_css}</style>""", unsafe_allow_html=True)

    # Thêm CSS để vát góc của hình ảnh
    st.markdown(
        f"""
        <style>
            .rounded-image {{
                border-radius: 15px; /* Điều chỉnh giá trị này để thay đổi độ cong góc */
                overflow: hidden;
            }}
        </style>
        """
    , unsafe_allow_html=True)

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


if __name__ == "__main__":
    main()
