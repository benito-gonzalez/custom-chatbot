import streamlit as st
from streamlit_chat import message as custom_message
from io import BytesIO
from gtts import gTTS, gTTSError
from llama_index.core.memory import ChatMemoryBuffer
from src.helpers import show_chat_buttons, show_text_input, ChatInterface


def get_chat_engine(topic, index, streaming=True):
    memory = ChatMemoryBuffer.from_defaults(token_limit=5000)
    return index.as_chat_engine(
        chat_mode="context",
        memory=memory,
        system_prompt=(
            f"{st.session_state.locale.ai_role_prefix} {topic.value} {st.session_state.locale.ai_role_postfix}"
        ),
        streaming=streaming
    )


def traditional_chat(topic, index):
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):

        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            chat_engine = get_chat_engine(topic, index, streaming=True)
            if prompt:
                response = chat_engine.stream_chat(prompt, chat_history=st.session_state.chat_history)
                response = st.write_stream(response.response_gen)
                st.session_state.messages.append({"role": "assistant", "content": response})


def modern_chat(topic, index):
    chat_engine = get_chat_engine(topic, index, streaming=False)

    # Use the chat method
    if st.session_state.user_text and st.session_state.user_text != '':
        response = chat_engine.chat(st.session_state.user_text, chat_history=st.session_state.chat_history)

        st.session_state.messages.append({"role": "user", "content": st.session_state.user_text})
        st.session_state.messages.append({"role": "assistant", "content": response.response})

    chat_placeholder = st.empty()

    with chat_placeholder.container():
        for idx, message in enumerate(st.session_state.messages):
            if message.get('role') == "user":
                custom_message(message.get('content'), is_user=True, key=f"{idx}_user", avatar_style="micah")
            else:
                custom_message(message.get('content'), key=f"{idx}")


def show_chat(chat_interface, topic, index):
    if chat_interface == ChatInterface.TRADITIONAL:
        traditional_chat(topic, index)
        show_audio_checkbox()

    else:
        modern_chat(topic, index)
        show_audio_checkbox()
        show_text_input()
        show_chat_buttons()


def show_audio_checkbox():
    st.divider()
    if st.session_state.messages:
        if st.checkbox(st.session_state.locale.audio_player_checkbox):
            show_audio_player(st.session_state.messages[-1].get('content'))


def show_audio_player(ai_content: str) -> None:
    """
    Generate and display an audio player for AI-generated content.

    This function converts AI-generated content into speech using the gTTS library,
    writes the speech to a BytesIO object, and then displays an audio player using Streamlit.

    :param ai_content: The AI-generated content to be converted to speech.
    :type ai_content: str

    :return: None
    """
    sound_file = BytesIO()
    try:
        tts = gTTS(text=ai_content, lang=st.session_state.locale.lang_code)
        tts.write_to_fp(sound_file)
        st.write(st.session_state.locale.stt_placeholder)
        st.audio(sound_file)
    except gTTSError as err:
        st.error(err)
