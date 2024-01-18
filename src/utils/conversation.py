import streamlit as st
from streamlit_chat import message
from io import BytesIO
from gtts import gTTS, gTTSError
from llama_index.llms.base import ChatMessage
from llama_index.memory import ChatMemoryBuffer


def show_chat_formatted(past, generated) -> None:
    chat_placeholder = st.empty()

    with chat_placeholder.container():
        for i in range(len(generated)):
            message(past[i], is_user=True, key=f"{i}_user", avatar_style="micah")
            message(generated[i].response, key=f"{i}")


def llama_conversation(index):
    memory = ChatMemoryBuffer.from_defaults(token_limit=10000)

    chat_engine = index.as_chat_engine(
        chat_mode="context",
        memory=memory,
        system_prompt=(
            "You are a chatbot, able to have normal interactions, as well as talk"
            " about an essay discussing Paul Grahams life."
        ),
    )
    # Use the chat method
    if st.session_state.user_text and st.session_state.user_text != '':
        chat_message = ChatMessage(role="user", content=st.session_state.user_text)
        response = chat_engine.chat(st.session_state.user_text, chat_history=st.session_state.chat_messages)
        st.session_state.chat_messages.append(chat_message)

        st.session_state.messages.append({"role": "user", "content": st.session_state.user_text})
        st.session_state.messages.append({"role": "system", "content": response})

        st.session_state.past.append(st.session_state.user_text)
        st.session_state.generated.append(response)

    show_chat_formatted(st.session_state.past, st.session_state.generated)
    st.divider()


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
