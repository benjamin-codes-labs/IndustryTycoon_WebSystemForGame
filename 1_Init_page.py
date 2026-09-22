import streamlit as st
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False
    st.session_state.placeholder = 'Enter your name:'

if 'player_name_list' not in st.session_state:
    st.session_state.player_name_list = [None, "", "", "", ""]
    
st.title('輸入你的名稱和角色！')
st.subheader('警告：不能有重複名稱')

if 'char_idx_tuple' not in st.session_state:
    st.session_state.char_idx_tuple = (0, 0, 0, 0)
    




player1_name = st.text_input(
        "玩家一名稱:👇",
        value=st.session_state.player_name_list[1],
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
        placeholder=st.session_state.placeholder,
    )

option1 = st.selectbox(
        "玩家一角色",
        ('爱迪生', '特斯拉', '慈禧', '尼古拉斯二世', '袁隆平', '成吉思汗', '秦始皇', '明治天皇', '罗斯福', '刘秀', '奥本海默', '腓特烈二世'),
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
    )


player2_name = st.text_input(
        "玩家二名稱: 👇",
        value=st.session_state.player_name_list[2],
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
        placeholder=st.session_state.placeholder,
    )

option2 = st.selectbox(
        "玩家二角色",
        ('爱迪生', '特斯拉', '慈禧', '尼古拉斯二世', '袁隆平', '成吉思汗', '秦始皇', '明治天皇', '罗斯福', '刘秀', '奥本海默', '腓特烈二世'),
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
    )


player3_name = st.text_input(
        "玩家三名字: 👇",
        value=st.session_state.player_name_list[3],
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
        placeholder=st.session_state.placeholder,
    )

option3 = st.selectbox(
        "玩家三角色",
        ('爱迪生', '特斯拉', '慈禧', '尼古拉斯二世', '袁隆平', '成吉思汗', '秦始皇', '明治天皇', '罗斯福', '刘秀', '奥本海默', '腓特烈二世'),
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
    )


player4_name = st.text_input(
    "玩家四名稱: 👇",
    value=st.session_state.player_name_list[4],
    label_visibility=st.session_state.visibility,
    disabled=st.session_state.disabled,
    placeholder=st.session_state.placeholder,
)

option4 = st.selectbox(
        "玩家四角色",
        ('爱迪生', '特斯拉', '慈禧', '尼古拉斯二世', '袁隆平', '成吉思汗', '秦始皇', '明治天皇', '罗斯福', '刘秀', '奥本海默', '腓特烈二世'),
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
    )

char_list = ('爱迪生', '特斯拉', '慈禧', '尼古拉斯二世', '袁隆平', '成吉思汗', '秦始皇', '明治天皇', '罗斯福', '刘秀', '奥本海默', '腓特烈二世')

option1_idx = char_list.index(option1)
option2_idx = char_list.index(option2)
option3_idx = char_list.index(option3)
option4_idx = char_list.index(option4)


st.session_state.char_idx_tuple = (option1_idx, option2_idx, option3_idx, option4_idx)

st.session_state.player_name_list[1] = player1_name
st.session_state.player_name_list[2] = player2_name
st.session_state.player_name_list[3] = player3_name
st.session_state.player_name_list[4] = player4_name
