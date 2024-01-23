import streamlit as st
from streamlit_option_menu import option_menu
from src.utils.locales import en, es
from src.utils.conversation import llama_conversation
from src.utils.helpers import show_chat_buttons, show_text_input
from src.utils.rag import load_indexes
from scraper.helpers import Topics

PAGE_TITLE: str = "AI Talks"
PAGE_ICON: str = "🤖"
LANG_EN: str = "En"
LANG_ES: str = "Es"

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

# Store the content
if "locale" not in st.session_state:
    st.session_state.locale = en
if "generated" not in st.session_state:
    st.session_state.generated = []
if "past" not in st.session_state:
    st.session_state.past = []
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_text" not in st.session_state:
    st.session_state.user_text = ""
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "selected_role" not in st.session_state:
    st.session_state.selected_role = "f1"

with st.sidebar:
    selected_lang = option_menu(
        menu_title=None,
        options=[LANG_ES, LANG_EN, ],
        icons=["globe2", "globe"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal"
    )


def main() -> None:
    print("Entramos en main")

    with st.sidebar:
        selected_role = st.selectbox(label=st.session_state.locale.select_placeholder,
                                     key="role",
                                     options=st.session_state.locale.ai_role_options)
    match selected_role:
        case "F1":
            st.session_state.selected_role = Topics.F1
        case "NBA":
            st.session_state.selected_role = Topics.NBA
        case "Football" | "Futbol":
            st.session_state.selected_role = Topics.FOOTBALL
        case _:
            st.session_state.selected_role = Topics.F1

    st.markdown(
        f"<h1 style='text-align: center;'>{st.session_state.locale.title} {selected_role}</h1>",
        unsafe_allow_html=True)

    index = load_indexes(st.session_state.selected_role)

    llama_conversation(index)
    st.session_state.user_text = ""
    show_text_input()
    show_chat_buttons()


if __name__ == "__main__":
    match selected_lang:
        case "En":
            st.session_state.locale = en
        case "Es":
            st.session_state.locale = es
        case _:
            st.session_state.locale = en
    main()
