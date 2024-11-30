from flask import Flask, render_template, request
from deep_translator import GoogleTranslator
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from groq import Groq

app = Flask(__name__)
client = Groq(api_key="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")

@app.route("/", methods=["GET", "POST"])
def index():
    resposta = ""
    
    if request.method == "POST":
        
        netflix = pd.read_csv("titulos.netflix.csv")
        netflix['tipo'] = netflix['tipo'].fillna("")
        netflix['titulo'] = netflix['titulo'].fillna("")
        netflix['diretor'] = netflix['diretor'].fillna("")
        netflix['atores'] = netflix['atores'].fillna("")
        netflix['descrição'] = netflix['descrição'].fillna("")
        netflix['país'] = netflix['país'].fillna("")
        netflix['classificação_indicativa'] = netflix['classificação_indicativa'].fillna("")
        netflix['ano_lançamento'] = netflix['ano_lançamento'].fillna("") 

        netflix['texto_completo'] = (
            netflix['tipo'] + " " + 
            netflix['titulo'] + " " + 
            netflix['diretor'] + " " + 
            netflix['atores'] + " " + 
            netflix['descrição'] + " " + 
            netflix['país'] + " " + 
            netflix['ano_lançamento'].astype(str) + " " +  
            netflix['classificação_indicativa'].astype(str)
        )
        
        mensagem = request.form["mensagem"]
        
        traducao = GoogleTranslator(source='pt', target='en').translate(mensagem)
        mensagem_em_ingles = traducao if traducao else ""  # Garante que o valor não seja None
        
        corpus = [mensagem_em_ingles] + netflix['texto_completo'].tolist()
     
        vectorizer = TfidfVectorizer(stop_words='english')
        X = vectorizer.fit_transform(corpus)
        
        cosine_similarities = cosine_similarity(X[0:1], X[1:]).flatten() 
                
        indices_similares = cosine_similarities.argsort()[-10:][::-1] 
        top_10_similares = netflix.iloc[indices_similares]
        
        top_10_similares['similarity'] = cosine_similarities[indices_similares] 
                
        similares = top_10_similares[['show_id', 'tipo', 'titulo', 'diretor', 'atores', 'país', 
                                      'ano_lançamento', 'classificação_indicativa', 'descrição', 'similarity']]
                
        mensagem_enriquecida = mensagem + " Favor fazer sua resposta baseada no contexto adicional do CSV com dados da Netflix: " + similares.to_string(index=False)
        
        messages = [{"role": "user", "content": mensagem_enriquecida}]           

        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )
                
        for chunk in completion:
            resposta += chunk.choices[0].delta.content or ""
    
    return render_template("index.html", resposta=resposta)

if __name__ == "__main__":
    app.run(debug=True)
