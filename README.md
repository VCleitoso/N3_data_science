# N3_data_science

Alunos: Amarildo Junior, Fernando Paludo, Júlio Spezzia, Kamila Klein e Kauê Otto

## Trabalho N3 da disciplina de ciência de dados

O presente repositório trata-se da avaliação N3 da disciplina de ciência de dados

## Como funciona

A aplicação lê um csv de dados da netflix (o python tinha dificuldadem em ler um dataset tão grande quanto o que o professor requisitou)

É gerada uma aplicação flask que apresenta um formulário html ao usuário, o texto inserido é traduzido para o inglês (o dataset está em inglês), onde é então feita uma análise de similaridades, sendo que as 10 linhas do dataset com maior similaridade são retornadas.

As linhas são convertidas para string e adicionadas junto da mensagem original à um prompt para uma LLM do groq.

A LLM é então instruida à dar uma recomendação com base nos dados recebidos.
