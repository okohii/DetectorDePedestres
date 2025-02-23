import speech_recognition as sr  # Biblioteca para reconhecimento de fala
import pyttsx3  # Biblioteca para síntese de fala
import os  # Biblioteca para interagir com o sistema operacional
import time  # Biblioteca para manipulação de tempo
import random  # Biblioteca para gerar números aleatórios
import requests  # Biblioteca para fazer requisições HTTP

# Inicializa o reconhecedor de fala e o motor de síntese de fala
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Configuração da API do Google AI Gemini
GEMINI_API_KEY = 'AIzaSyBzb9LfZWMcM_KJ0h5mXu4Ml8CiylwG4gk'  # Chave da API do Google AI Gemini
GEMINI_API_URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}'  # URL da API do Google AI Gemini

def configurar_voz(language):
    """
    Configura a voz do assistente de acordo com o idioma selecionado.
    """
    voices = engine.getProperty('voices')  # Obtém as vozes disponíveis
    if language == 'pt-BR':
        for voice in voices:
            if 'brazil' in voice.name.lower():
                engine.setProperty('voice', voice.id)  # Configura a voz para português do Brasil
                break
    elif language == 'en-US':
        for voice in voices:
            if 'english' in voice.name.lower():
                engine.setProperty('voice', voice.id)  # Configura a voz para inglês
                break
    engine.setProperty('rate', 210)  # Configura a velocidade da fala

def ouvir_comando(language='pt-BR'):
    """
    Captura o comando de voz do usuário e o reconhece usando a API do Google.
    """
    with sr.Microphone() as source:
        print("Ouvindo...")  # Indica que o assistente está ouvindo
        audio = recognizer.listen(source)  # Captura o áudio do microfone
        comando = ""
        try:
            comando = recognizer.recognize_google(audio, language=language)  # Reconhece o comando de voz
            print(f"Você disse: {comando}" if language == 'pt-BR' else f"You said: {comando}")  # Exibe o comando reconhecido
        except sr.UnknownValueError:
            print("Não entendi o que você disse." if language == 'pt-BR' else "I didn't understand what you said.")  # Mensagem de erro se não entender o comando
        except sr.RequestError:
            print("Erro ao se conectar ao serviço de reconhecimento de fala." if language == 'pt-BR' else "Error connecting to the speech recognition service.")  # Mensagem de erro se não conseguir conectar ao serviço de reconhecimento de fala
        
        return comando.lower()  # Retorna o comando em letras minúsculas

def falar(texto):
    """
    Converte o texto em fala e o executa.
    """
    engine.say(texto)  # Converte o texto em fala
    engine.runAndWait()  # Executa a fala

def verificar_comando(comando, palavras_chave):
    """
    Verifica se alguma palavra-chave está presente no comando.
    """
    return any(palavra in comando for palavra in palavras_chave)

def responder_com_gemini(comando, language='pt-BR'):
    """
    Faz uma requisição para a API do Google AI Gemini e retorna a resposta.
    """
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "contents": [{
            "parts": [{"text": comando}]
        }]
    }
    response = requests.post(GEMINI_API_URL, headers=headers, json=data)  # Faz uma requisição POST para a API do Google AI Gemini
    if response.status_code == 200:
        try:
            response_json = response.json()  # Converte a resposta para JSON
            resposta_texto = response_json['candidates'][0]['content']['parts'][0]['text'].strip()  # Extrai o texto da resposta
            resposta_texto = resposta_texto.replace('*', '').replace('\n', ' ')  # Remove caracteres indesejados
            return resposta_texto  # Retorna a resposta
        except KeyError as e:
            return "Desculpe, houve um erro ao processar sua solicitação."  # Mensagem de erro se não conseguir acessar a chave
    else:
        return "Desculpe, houve um erro ao processar sua solicitação."  # Mensagem de erro se a requisição falhar

def executar_tarefa(comando, language='pt-BR'):
    """
    Executa a tarefa correspondente ao comando de voz reconhecido.
    """
    if verificar_comando(comando, ['olá', 'oi', 'hello', 'hi', 'hey', 'e aí', 'e ai', 'tudo bem', 'tá bem', 'como vai', 'como está', 'how are you', 'how are you doing', 'how do you do']):
        resposta = "Olá! Tudo bem?" if language == 'pt-BR' else "Hello! How are you?"
        print(resposta)  # Exibe a resposta no terminal
        falar(resposta)  # Converte a resposta em fala
    elif verificar_comando(comando, ['quem é você', 'quem você é', 'what is your name', 'what are you', 'who are you', 'who you are']):
        resposta = "Eu sou um assistente virtual criado por um gostosão chamado Gustavo." if language == 'pt-BR' else "I am a virtual assistant created by a delicious man named Gustavo."
        print(resposta)  # Exibe a resposta no terminal
        falar(resposta)  # Converte a resposta em fala
    elif verificar_comando(comando, ['me fala sobre o jp', 'JP', 'quem é o jp', 'jp', 'seu criador jp']):
        resposta = "O JP, ou João Pedro Mori Noce é um dos colaboradores que ajudou a me desenvolver, é um cara alegre, proativo e interessado, um ótimo desenvolvedor. Porém, não comente nada sobre os anos entre 1933 e 1945 na Alemanha, ele pode ficar desconfortável." if language == 'pt-BR' else "JP, or João Pedro Mori Noce is one of the employees who helped develop me, is a cheerful, proactive and interested guy, a great developer. However, it does not comment on the years between 1933 and 1945 in Germany, it can be uncomfortable."
        print(resposta)  # Exibe a resposta no terminal
        falar(resposta)  # Converte a resposta em fala
    elif verificar_comando(comando, ['navegador', 'browser']):
        resposta = "Abrindo o navegador" if language == 'pt-BR' else "Opening the browser"
        print(resposta)  # Exibe a resposta no terminal
        falar(resposta)  # Converte a resposta em fala
        os.system("start opera")  # Abre o navegador
    elif verificar_comando(comando, ['que horas são', 'whats the time', 'what the time', "what's time", "what's the time", 'what is time', 'what time']):
        from datetime import datetime
        agora = datetime.now().strftime("%H:%M")  # Obtém a hora atual
        resposta = f"Agora são {agora}" if language == 'pt-BR' else f"The time is {agora}"
        print(resposta)  # Exibe a resposta no terminal
        falar(resposta)  # Converte a resposta em fala
    elif verificar_comando(comando, ['preparar', 'área de trabalho', 'workspace']):
        resposta = "Preparando a área de trabalho" if language == 'pt-BR' else "Preparing the workspace"
        print(resposta)  # Exibe a resposta no terminal
        falar(resposta)  # Converte a resposta em fala
        os.system("start opera")  # Abre o navegador
        os.system("start code")  # Abre o Visual Studio Code
        os.system("start C:\\Users\\okohi\\AppData\\Local\\Postman\\Postman.exe")  # Abre o Postman
        os.system("explorer")  # Abre o explorador de arquivos
    elif verificar_comando(comando, ['descansar', 'ir embora', 'soneca', 'rest', 'nap', 'comes e bebes', 'comes e bebe', 'bye', 'tchau', 'adeus', 'até mais', 'até depois', 'até logo', 'até breve', 'até a próxima', 'até a próxima vez', 'até a próxima vez']):
        resposta = "Beleza, vou tirar uma soneca. Até depois moral!" if language == 'pt-BR' else "Alright, I'm going to take a nap. See you later!"
        print(resposta)  # Exibe a resposta no terminal
        falar(resposta)  # Converte a resposta em fala
        exit()  # Encerra o assistente
    else:
        resposta = responder_com_gemini(comando, language)  # Obtém a resposta da API do Google AI Gemini
        print(resposta)  # Exibe a resposta no terminal
        falar(resposta)  # Converte a resposta em fala


# Deixa esse bloco por último, se não quebra tudo!!!!!
if __name__ == "__main__":
    print("Português ou, or English?")
    falar("Português ou, or English?")  # Pergunta ao usuário em qual língua ele gostaria de se comunicar
    language = 'pt-BR'
    while True:
        escolha = ouvir_comando('pt-BR')
        if 'português' in escolha or 'portugues' in escolha or 'portuguese' in escolha:
            language = 'pt-BR'
            configurar_voz(language)
            falar("Você escolheu português. Como posso ajudar você hoje?")  # Responde em português
            break
        elif 'english' in escolha or 'inglês' in escolha or 'ingles' in escolha:
            language = 'en-US'
            configurar_voz(language)
            falar("You chose English. How can I help you today?")  # Responde em inglês
            break
        else:
            print("Português ou, or English?")
            falar("Português ou, or English?")  # Repete a pergunta se não entender a escolha

    while True:
        comando = ouvir_comando(language)  # Captura o comando de voz do usuário
        if comando:
            executar_tarefa(comando, language)  # Executa a tarefa correspondente ao comando