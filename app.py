from flask import Flask, render_template, request
from groq import Groq
import pandas as pd

app = Flask(__name__)

# Instanciando o cliente Groq com a chave de API
client = Groq(api_key="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")

@app.route("/", methods=["GET", "POST"])
def index():
    resposta = ""
    
    if request.method == "POST":
        # Lendo os arquivos CSV
        netflix = pd.read_csv("titulos.netflix.csv")

        # Obtendo uma amostra dos dados do CSV para evitar exceder o limite de tamanho da solicitação
        sample_data = netflix.sample(n=10)  # Amostra de 10 linhas aleatórias
        sample_data_str = sample_data.to_string(index=False)

        mensagem = request.form["mensagem"]  # Obtendo a mensagem do formulário
        
        # Enriquecendo a mensagem com a amostra dos dados do CSV
        mensagem_enriquecida = mensagem + " Favor fazer sua resposta baseada no contexto adicional do CSV com dados da netflix: " + sample_data_str

        # Configurando a mensagem para a API
        messages = [{"role": "user", "content": mensagem_enriquecida}]
        
        # Fazendo a requisição à API
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )
        
        # Processando a resposta da API e exibindo
        for chunk in completion:
            resposta += chunk.choices[0].delta.content or ""
    
    return render_template("index.html", resposta=resposta)

if __name__ == "__main__":
    app.run(debug=True)
