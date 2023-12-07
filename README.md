# BancoNeo4j
Part 2 do Trabalho de Banco 2 
Instalação do FastAPI:

* Indico de rodar a aplicação dentro de um ambiente virtual que rode as instalações em um ambiente diferente aos programas do computador.

-> python -m venv venv
-> para ativar é source {nome_venv}/bin/activate
-> para desativar: deactivate

* Em seguida rode: pip install "fastapi[all]"
Caso não instale o uvicorn rode: pip install "uvicorn[standard]"

Para rodar o banco indico baixar o Neo4j verção desktop. 
https://neo4j.com/download/

Essas são as bibliotecas importadas no projeto.
Em seguida rode: uvicorn main:app --reload
Tem um pequeno dump da db junto ao arquivos.

A senha do banco no trabalho está como 12345678. Caso seja diferente, mude no config.py.
A porta do banco usada é a padrão do neo4j.

A porta padrão é localhost:8000 e sua docs ficam em localhost:8000/docs

Instalação  do Frontend em VUE:

rode: npm install vue
na pasta do frontend/banco rode: npm install e npm run dev

porta padrão é 5173 sendo: localhost:5173

não foi importado bibliotecas externas.

Dumb da db:
Foi fornecido um dumb da db o qual pode ser rodado em neo4j.






