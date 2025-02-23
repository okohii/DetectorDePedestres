import speech_recognition as sr
import pyttsx3
import os
import random
import requests

recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Configuração da API do Google AI Gemini
GEMINI_API_KEY = 'AIzaSyBzb9LfZWMcM_KJ0h5mXu4Ml8CiylwG4gk'
GEMINI_API_URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}'

def configurar_voz(language):
    voices = engine.getProperty('voices')
    if language == 'pt-BR':
        for voice in voices:
            if 'brazil' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
    elif language == 'en-US':
        for voice in voices:
            if 'english' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
    engine.setProperty('rate', 220)  # Aumentar a velocidade da fala

def ouvir_comando(language='pt-BR'):
    with sr.Microphone() as source:
        print("Ouvindo...")
        audio = recognizer.listen(source)
        comando = ""
        try:
            comando = recognizer.recognize_google(audio, language=language)
            print(f"Você disse: {comando}" if language == 'pt-BR' else f"You said: {comando}")
        except sr.UnknownValueError:
            print("Não entendi o que você disse." if language == 'pt-BR' else "I didn't understand what you said.")
        except sr.RequestError:
            print("Erro ao se conectar ao serviço de reconhecimento de fala." if language == 'pt-BR' else "Error connecting to the speech recognition service.")
        
        return comando.lower()

def falar(texto):
    engine.say(texto)
    engine.runAndWait()

def responder_com_gemini(comando, language='pt-BR'):
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "contents": [{
            "parts": [{"text": comando}]
        }]
    }
    response = requests.post(GEMINI_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        try:
            response_json = response.json()
            print("Resposta completa da API:", response_json)
            resposta_texto = response_json['candidates'][0]['content']['parts'][0]['text'].strip()
            resposta_texto = resposta_texto.replace('*', '').replace('\n', ' ')
            return resposta_texto
        except KeyError as e:
            print(f"Erro ao acessar a chave: {e}")
            return "Desculpe, houve um erro ao processar sua solicitação."
    else:
        print("Erro na resposta da API:", response.status_code, response.text)
        return "Desculpe, houve um erro ao processar sua solicitação."

def executar_tarefa(comando, language='pt-BR'):
    # Adicionar lógica para abrir programas com base no comando antes de chamar a API
    if 'abrir navegador' in comando or 'abrir o navegador' in comando:
        falar("Abrindo o navegador.")
        os.system("start chrome")  # Exemplo de abrir o Google Chrome
        return
    elif 'abrir bloco de notas' in comando:
        falar("Abrindo o Bloco de Notas.")
        os.system("start notepad")  # Exemplo de abrir o Bloco de Notas
        return
    elif 'abrir calculadora' in comando:
        falar("Abrindo a Calculadora.")
        os.system("start calc")  # Exemplo de abrir a Calculadora
        return

    # Caso contrário, chame a API do Gemini
    resposta = responder_com_gemini(comando, language)
    falar(resposta)

if __name__ == "__main__":
    falar("Português ou, or English?")
    language = 'pt-BR'
    while True:
        escolha = ouvir_comando('pt-BR')
        if 'português' in escolha or 'portugues' in escolha or 'portuguese' in escolha:
            language = 'pt-BR'
            configurar_voz(language)
            falar("Você escolheu português. Como posso ajudar você hoje?")
            break
        elif 'english' in escolha or 'inglês' in escolha or 'ingles' in escolha:
            language = 'en-US'
            configurar_voz(language)
            falar("You chose English. How can I help you today?")
            break
        else:
            falar("Português ou, or English?")

    while True:
        comando = ouvir_comando(language)
        if comando:
            executar_tarefa(comando, language)
