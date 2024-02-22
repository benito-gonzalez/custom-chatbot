from dataclasses import dataclass
from typing import List


@dataclass
class Locale:
    ai_role_options: List[str]
    ai_role_prefix: str
    ai_role_postfix: str
    title: str
    language: str
    lang_code: str
    chat_placeholder: str
    chat_run_btn: str
    chat_clear_btn: str
    chat_save_btn: str
    select_placeholder: str
    select_chat_interface: str
    interface1: str
    interface2: str
    stt_placeholder: str
    audio_player_checkbox: str


AI_ROLE_OPTIONS_EN = [
    "F1",
    "NBA",
    "Football",
    "Tennis"
]

AI_ROLE_OPTIONS_ES = [
    "F1",
    "NBA",
    "Futbol",
    "Tenis"
]

en = Locale(
    ai_role_options=AI_ROLE_OPTIONS_EN,
    ai_role_prefix="You are a chatbot, able to have normal interactions, as well as an expert in ",
    ai_role_postfix="Answer as concisely as possible.",
    title="Welcome to your expert in ",
    language="English",
    lang_code="en",
    chat_placeholder="Start Your Conversation With AI:",
    chat_run_btn="Ask",
    chat_clear_btn="Clear",
    chat_save_btn="Save",
    select_placeholder="Select your expert",
    select_chat_interface="Select the chat interface",
    interface1="Traditional",
    interface2="Modern",
    stt_placeholder="To Hear The Voice Of AI Press Play",
    audio_player_checkbox="Show audio player"
)

es = Locale(
    ai_role_options=AI_ROLE_OPTIONS_ES,
    ai_role_prefix="Eres un chatbot capacitado para tener conversaciones normales y experto en ",
    ai_role_postfix="Responde de la manera más concisa posible.",
    title="Bienvenido a tu experto en ",
    language="Español",
    lang_code="es",
    chat_placeholder="Inicia tu conversación con la IA:",
    chat_run_btn="Preguntar",
    chat_clear_btn="Limpiar",
    chat_save_btn="Guardar",
    select_placeholder="Selecciona a tu experto",
    select_chat_interface="Selecciona la interface del chat",
    interface1="Tradicional",
    interface2="Moderna",
    stt_placeholder="Para escuchar la voz de la IA, presiona Reproducir",
    audio_player_checkbox="Mostrar reproductor de audio"

)
