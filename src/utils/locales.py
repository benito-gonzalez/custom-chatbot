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
    select_placeholder1: str
    select_placeholder2: str
    select_placeholder3: str
    radio_placeholder: str
    radio_text1: str
    radio_text2: str
    stt_placeholder: str


AI_ROLE_OPTIONS_EN = [
    "helpful assistant",
    "code assistant",
    "code reviewer",
    "text improver",
    "cinema expert",
    "sports expert",
]

AI_ROLE_OPTIONS_ES = [
    "asistente útil",
    "asistente de código",
    "revisor de código",
    "mejorador de texto",
    "experto en cine",
    "experto en deportes",
]

en = Locale(
    ai_role_options=AI_ROLE_OPTIONS_EN,
    ai_role_prefix="You are a female",
    ai_role_postfix="Answer as concisely as possible.",
    title="AI Talks",
    language="English",
    lang_code="en",
    chat_placeholder="Start Your Conversation With AI:",
    chat_run_btn="Ask",
    chat_clear_btn="Clear",
    chat_save_btn="Save",
    select_placeholder1="Select Model",
    select_placeholder2="Select Role",
    select_placeholder3="Create Role",
    radio_placeholder="Role Interaction",
    radio_text1="Select",
    radio_text2="Create",
    stt_placeholder="To Hear The Voice Of AI Press Play",
)

es = Locale(
    ai_role_options=AI_ROLE_OPTIONS_ES,
    ai_role_prefix="Eres una mujer",
    ai_role_postfix="Responde de la manera más concisa posible.",
    title="Bienvenido a tu experto en F1",
    language="Español",
    lang_code="es",
    chat_placeholder="Inicia tu conversación con la IA:",
    chat_run_btn="Preguntar",
    chat_clear_btn="Limpiar",
    chat_save_btn="Guardar",
    select_placeholder1="Seleccionar Modelo",
    select_placeholder2="Seleccionar Rol",
    select_placeholder3="Crear Rol",
    radio_placeholder="Interacción de Rol",
    radio_text1="Seleccionar",
    radio_text2="Crear",
    stt_placeholder="Para escuchar la voz de la IA, presiona Reproducir",
)
