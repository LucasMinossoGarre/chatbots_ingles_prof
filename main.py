import tkinter as tk
from tkinter import scrolledtext
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import os
import threading


model = OllamaLLM(model='llama3.2-vision')  # ou outro modelo

BACKUP_PATH_INGLES = "./backup/ingles.txt"

# Configuração da janela principal
root = tk.Tk()
root.minsize(500, 300)
root.maxsize(500, 300)
root.title('Sra. Sexta')
root.config(background='#1C1C1C')

#////////////////////////////////////////////////////////////////////////////////////////////////

def enviar_mensagem_prof_ingles():   
    global context,chain 
    # Pega a mensagem do usuário
    mensagem = entrada.get()
    entrada.delete(0, tk.END)
    
    if mensagem.strip():
        # Exibe a mensagem do usuário
        chat_log.config(state=tk.NORMAL)
        chat_log.insert(tk.END, f"Você: {mensagem}\n")
        
        chat_log.insert(tk.END, f"\n")
        chat_log.insert(tk.END, f"Gerando sua Resposta..\n")
        chat_log.config(state=tk.DISABLED)
        
        # Processa a mensagem com o chatbot
        try:            
            result = chain.invoke({'context': context, 'question': mensagem})
            resposta = result  # Extrai a resposta do chatbot
            context += f"\nVocê: {mensagem}\nIA: {resposta}"  # Atualiza o contexto
            salvar_contexto_ingles(context)
            
            # Exibe a resposta do chatbot
            chat_log.config(state=tk.NORMAL)
            chat_log.insert(tk.END, f"\n")
            chat_log.insert(tk.END, f"Sexta: {resposta}\n")
            chat_log.insert(tk.END, f"\n")
            chat_log.config(state=tk.DISABLED)
        except Exception as e:
            chat_log.config(state=tk.NORMAL)
            chat_log.insert(tk.END, f"Erro ao processar a mensagem: {str(e)}\n")
            chat_log.config(state=tk.DISABLED)

def salvar_contexto_ingles(context):
    """Salva o contexto do professor de inglês no arquivo de backup."""
    os.makedirs(os.path.dirname(BACKUP_PATH_INGLES), exist_ok=True)
    with open(BACKUP_PATH_INGLES, "w", encoding="utf-8") as f:
        f.write(context)

def carregar_contexto_ingles():
    """Carrega o contexto do professor de inglês do arquivo de backup, se existir."""
    if os.path.exists(BACKUP_PATH_INGLES):
        with open(BACKUP_PATH_INGLES, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def start_prof_ingles():
    global context,chain
    
    template = """
        Seguinte, você deverá agir como um professor de inglês. Seu objetivo é melhorar minha conversa em inglês
        Então nossa metodologia será: Uma conversa entre duas pessoas normalmente.
        
        obs: lembre-se de explicar sua frase e traduzir ela para que eu possa responder ela e você dar continuidade a nossa conversa
        
        Aqui está o histórico da conversa para apenas voce saber onde estamos para continuar aparti dela: {context}
        
        Pergunta: {question}
        
       obs: sempre traduza a minha pergunta e tente ver onde eu errei ou oque eu poderia ter falado.
          
    """
    # Variável para armazenar o histórico da conversa
    context = carregar_contexto_ingles()
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    threading.Thread(target=enviar_mensagem_prof_ingles).start()

def prof_ingles():
    # Atualiza o título
    title = tk.Label(root, text='Professor de Inglês', font=("Arial", 16), fg="white", bg="#1C1C1C")
    title.pack(pady=5)
    

    # Área de mensagens (com scrollbar)
    global chat_log
    chat_log = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, height=10, width=50, bg="#262626", fg="white", font=("Arial", 10))
    chat_log.pack(pady=(10, 5))
    
    # Campo de entrada de texto
    global entrada
    entrada = tk.Entry(root, width=40, bg="#333333", fg="white", font=("Arial", 10))
    entrada.pack(pady=5)
    
    # Botão para enviar mensagem
    botao_enviar = tk.Button(root, text="Enviar", command=start_prof_ingles, bg="#333333", fg="white", font=("Arial", 10))
    botao_enviar.pack(padx=5)


if __name__ == '__main__':
    prof_ingles()
    root.mainloop()