import os
import streamlit as st
from streamlit_option_menu import option_menu
from src.utils.locales import en, es
from src.utils.conversation import llama_conversation
from src.utils.helpers import show_chat_buttons, show_text_input
from src.utils.rag import load_indexes, generate_indexes
from scraper.helpers import Topics
from scraper.run_scrapers import run_all_scrapers

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

with st.sidebar:
    selected_lang = option_menu(
        menu_title=None,
        options=[LANG_ES, LANG_EN, ],
        icons=["globe2", "globe"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal"
    )


@st.cache_resource
def initialize_scrapers():
    documents_path = os.path.join(PATH, "scraper", "documents")
    if not os.path.exists(documents_path):
        run_all_scrapers()


@st.cache_resource
def initialize_rag():
    index_path = os.path.join(PATH, "storage")
    if not os.path.exists(index_path):
        generate_indexes()


def main() -> None:
    with st.sidebar:
        selected_role = option_menu(
            menu_title=st.session_state.locale.select_placeholder,
            options=st.session_state.locale.ai_role_options,
            icons=["car-front-fill", "globe", "circle"],
            menu_icon="cast",
            default_index=0,
            orientation="vertical",
            styles={
                "nav-link": {"--hover-color": "#eee"},
            }
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

    st.markdown(
        f"<h1 style='text-align: center;'>{st.session_state.locale.title} {selected_role}</h1>",
        unsafe_allow_html=True)

    index = load_indexes(st.session_state.selected_role)

    llama_conversation(st.session_state.selected_role, index)
    st.session_state.user_text = ""
    show_text_input()
    show_chat_buttons()


if __name__ == "__main__":
    initialize_scrapers()
    initialize_rag()

    match selected_lang:
        case "En":
            st.session_state.locale = en
        case "Es":
            st.session_state.locale = es
        case _:
            st.session_state.locale = en
    main()
