import os
import streamlit as st
from streamlit_option_menu import option_menu
from src.locales import en, es
from src.conversation import llama_conversation
from src.helpers import show_chat_buttons, show_text_input
from src.index_generator import load_indexes
from scraper.helpers import Topics

PAGE_TITLE: str = "AI Talks"
PAGE_ICON: str = "🤖"
LANG_EN: str = "En"
LANG_ES: str = "Es"

PATH = os.path.abspath(os.path.dirname(__file__))

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

# remove streamlit menu
hide_streamlit_style = """
            <style>
            [data-testid="stToolbar"] {visibility: hidden !important;}
            footer {visibility: hidden !important;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

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
    st.session_state.selected_role = Topics.F1
if "selected_text_model" not in st.session_state:
    st.session_state.selected_text_model = "gpt-3.5-turbo"

with st.sidebar:
    selected_lang = option_menu(
        menu_title=None,
        options=[LANG_ES, LANG_EN, ],
        icons=["globe2", "globe"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={"nav-link": {"--hover-color": "#eee"}}
    )


def show_selected_text_model():
    with st.sidebar:
        option_menu(
            menu_title="LLM",
            options=["gpt-3.5-turbo"],
            icons=["robot", "robot"],
            menu_icon="wrench-adjustable",
            default_index=0,
            orientation="horizontal",
            styles={"nav-link": {"--hover-color": "#eee"}}
        )


def get_selected_role():
    with st.sidebar:
        selected_role = option_menu(
            menu_title=st.session_state.locale.select_placeholder,
            options=st.session_state.locale.ai_role_options,
            icons=["car-front-fill", "globe", "circle"],
            menu_icon="person-lines-fill",
            default_index=0,
            orientation="vertical",
            styles={"nav-link": {"--hover-color": "#eee"}}
        )
    match selected_role:
        case "F1":
            st.session_state.selected_role = Topics.F1
        case "NBA":
            st.session_state.selected_role = Topics.NBA
        case "Football" | "Futbol":
            st.session_state.selected_role = Topics.FOOTBALL
        case "Tennis" | "Tenis":
            st.session_state.selected_role = Topics.TENNIS
        case _:
            st.session_state.selected_role = Topics.F1

    return selected_role


def display_title(selected_role):
    st.markdown(
        f"<h1 style='text-align: center;'>{st.session_state.locale.title} {selected_role}</h1>",
        unsafe_allow_html=True)


def main() -> None:
    show_selected_text_model()
    selected_role = get_selected_role()
    display_title(selected_role)

    index = load_indexes(st.session_state.selected_role)
    llama_conversation(st.session_state.selected_role, index)
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
