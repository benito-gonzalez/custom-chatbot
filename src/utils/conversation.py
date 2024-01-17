import streamlit as st
from openai import OpenAI

from openai import OpenAIError
from typing import List
from streamlit_chat import message
from sqlalchemy.exc import InvalidRequestError
from io import BytesIO
from gtts import gTTS, gTTSError


def create_gpt_completion(ai_model: str, messages: List[dict]):
    client = OpenAI(api_key=st.secrets.api_crendentials)
    completion = client.chat.completions.create(
        model=ai_model,
        messages=messages)
    return completion


def show_chat(ai_content: str, user_text: str) -> None:
    if ai_content not in st.session_state.generated and st.session_state.user_text != '':
        # store the ai content
        st.session_state.past.append(user_text)
        st.session_state.generated.append(ai_content)
    if st.session_state.generated:
        for idx, element in enumerate(st.session_state.generated):
            message(st.session_state.past[idx], is_user=True, key=str(idx) + "_user", avatar_style="micah")
            message("", key=str(idx))
            st.markdown(element)


def show_gpt_conversation() -> None:
    """
    Display a conversation with GPT model.

    This function attempts to generate a completion using the GPT model based on the current
    conversation messages. It then updates the conversation with the AI-generated content,
    displays the content in the chat, and shows an audio player if the content exists.

    Exceptions are caught and handled, including InvalidRequestError for context length exceeded,
    which results in removing the assistant's previous message.

    :return: None
    """
    try:
        completion = create_gpt_completion(st.session_state.model, st.session_state.messages)
        ai_content = completion.choices[0].message.content
        st.session_state.messages.append({'role': 'assistant', 'content': ai_content})
        if ai_content:
            show_chat(ai_content, st.session_state.user_text)
            st.divider()
            #show_audio_player(ai_content)
    except InvalidRequestError as err:
        if err.code == "context_length_excedeed":
            st.session_state.messages.pop(1)
            if len(st.session_state.messages) == 1:
                st.session_state.user_text = ""
            show_conversation()
        else:
            st.error(err)
    except (OpenAIError, UnboundLocalError) as err:
        st.error(err)


def show_conversation() -> None:
    """
    Update and display the conversation.

    This function checks if there are existing messages in the conversation.
    If messages exist, it appends the user's message to the conversation.
    If no messages exist, it initializes the conversation with a system message
    and the user's message. It then proceeds to show the GPT-generated conversation.

    :return: None
    """
    if st.session_state.messages:
        st.session_state.messages.append({'role': 'user', 'content': st.session_state.user_text})
    else:
        ai_role = f"{st.session_state.locale.ai_role_prefix} {st.session_state.role}. {st.session_state.locale.ai_role_postfix}"  # NOQA: E501
        st.session_state.messages = [
            {"role": "system", "content": ai_role},
            {"role": "user", "content": st.session_state.user_text},
        ]
    # if there is a previous conversation, show it
    if [message for message in st.session_state.messages if message['role'] == 'user' and message['content'] != '']:
        show_gpt_conversation()


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
