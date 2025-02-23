import speech_recognition as sr
import pyttsx3
import os
import time
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
    engine.setProperty('rate', 220)

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

def verificar_comando(comando, palavras_chave):
    return any(palavra in comando for palavra in palavras_chave)

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
            resposta_texto = response_json['candidates'][0]['content']['parts'][0]['text'].strip()
            resposta_texto = resposta_texto.replace('*', '').replace('\n', ' ')
            return resposta_texto
        except KeyError as e:
            return "Desculpe, houve um erro ao processar sua solicitação."
    else:
        return "Desculpe, houve um erro ao processar sua solicitação."

def executar_tarefa(comando, language='pt-BR'):
    if verificar_comando(comando, ['olá', 'oi', 'hello', 'hi', 'hey', 'e aí', 'e ai', 'tudo bem', 'tá bem', 'como vai', 'como está', 'how are you', 'how are you doing', 'how do you do']):
        falar("Olá! Tudo bem?" if language == 'pt-BR' else "Hello! How are you?")
    elif verificar_comando(comando, ['quem é você', 'quem você é', 'what is your name', 'what are you', 'who are you', 'who you are']):
        falar("Eu sou um assistente virtual criado por um gostosão chamado Gustavo." if language == 'pt-BR' else "I am a virtual assistant created by a hottie named Gustavo.")
    elif verificar_comando(comando, ['navegador', 'browser']):
        falar("Abrindo o navegador" if language == 'pt-BR' else "Opening the browser")
        os.system("start opera")
    elif verificar_comando(comando, ['que horas são', 'whats the time', 'what the time', "what's time", "what's the time", 'what is time', 'what time']):
        from datetime import datetime
        agora = datetime.now().strftime("%H:%M")
        falar(f"Agora são {agora}" if language == 'pt-BR' else f"The time is {agora}")
    elif verificar_comando(comando, ['preparar', 'área de trabalho', 'workspace']):
        falar("Preparando a área de trabalho" if language == 'pt-BR' else "Preparing the workspace")
        os.system("start opera")
        os.system("start code")
        os.system("start C:\\Users\\okohi\\AppData\\Local\\Postman\\Postman.exe")
        os.system("explorer")
    elif verificar_comando(comando, ['descansar', 'ir embora', 'soneca', 'rest', 'nap', 'comes e bebes', 'comes e bebe', 'bye', 'tchau', 'adeus', 'até mais', 'até depois', 'até logo', 'até breve', 'até a próxima', 'até a próxima vez', 'até a próxima vez']):
        falar("Beleza, vou tirar uma soneca. Até depois moral!" if language == 'pt-BR' else "Alright, I'm going to take a nap. See you later!")
        exit()
    else:
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
