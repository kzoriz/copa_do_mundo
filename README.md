# ⚽ Copa do Mundo 2026 - App de Palpites

Aplicativo mobile para gerenciamento de palpites da Copa do Mundo FIFA 2026, permitindo que usuários acompanhem partidas, registrem palpites, disputem rankings e participem de grupos privados.

---

# 📖 Sobre o Projeto

O projeto foi desenvolvido para oferecer uma experiência completa de bolão da Copa do Mundo 2026, contemplando o novo formato da competição com:

* 48 seleções
* 12 grupos
* 104 partidas
* Classificação dos 8 melhores terceiros colocados
* Mata-mata completo (16 avos até a Final)

O sistema realiza automaticamente a classificação dos grupos, geração do chaveamento oficial da FIFA e atualização das fases eliminatórias conforme os resultados são registrados.

---

# ✨ Funcionalidades

## 👤 Usuários

* Cadastro de usuários
* Login com autenticação JWT
* Persistência de sessão
* Perfil do participante

---

## 🎯 Palpites

* Registro de palpites para todas as partidas
* Apenas um palpite por jogo
* Bloqueio automático após o horário limite
* Bloqueio após divulgação do resultado oficial
* Histórico completo de palpites

---

## 📊 Ranking

### Ranking Geral

Classificação de todos os participantes.

Critérios de desempate:

1. Pontuação total
2. Quantidade de placares exatos
3. Quantidade de vencedores corretos

---

### Grupos Privados

Os usuários podem:

* Criar grupos de ranking
* Compartilhar código de convite
* Entrar em grupos existentes
* Sair de grupos
* Visualizar rankings exclusivos

---

## 🏆 Copa do Mundo 2026

### Fase de Grupos

* Classificação automática
* Critérios oficiais da FIFA
* Confronto direto em casos de empate

### Melhores Terceiros

Seleção automática dos 8 melhores terceiros colocados.

Critérios:

1. Pontos
2. Saldo de gols
3. Gols marcados

---

### Mata-Mata

Fases:

* 16 Avos de Final
* Oitavas de Final
* Quartas de Final
* Semifinais
* Disputa de 3º Lugar
* Final

Chaveamento gerado automaticamente conforme o modelo oficial da FIFA.

---

### Pênaltis

Nas fases eliminatórias:

* Empates são decididos por pênaltis
* O vencedor é utilizado automaticamente para atualização do chaveamento

---

# 🛠️ Painel Administrativo

O sistema possui um painel administrativo para gerenciamento da competição.

Funcionalidades:

* Cadastro de seleções
* Upload de bandeiras
* Gestão de grupos
* Gestão de fases
* Gestão de partidas
* Registro de resultados oficiais
* Controle de pênaltis
* Ajuste manual da classificação dos grupos
* Definição manual de classificados em casos excepcionais

---

# 📱 Aplicativo Mobile

Principais telas:

* Login
* Cadastro
* Dashboard
* Fases
* Jogos
* Palpites
* Meus Palpites
* Ranking Geral
* Rankings de Grupo

---

# ⚙️ Tecnologias Utilizadas

## Backend

* Python 3.12
* Django
* Django Ninja
* JWT Authentication
* SQLite (desenvolvimento)
* PostgreSQL (produção)

## Frontend

* React Native
* Expo SDK 56
* Expo Router
* AsyncStorage

## Infraestrutura

* Ubuntu Server
* Gunicorn
* Nginx
* VPS Linux

---

# 🚀 Instalação

## Backend

```bash
git clone <repositorio>
cd backend

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver
```

---

## Frontend

```bash
cd mobile/my-app

npm install

npx expo start
```

---

# 📂 Estrutura do Projeto

```text
backend/
├── core/
├── media/
├── static/
├── manage.py

mobile/
└── my-app/
    ├── App.js
    ├── assets/
    ├── components/
    └── package.json
```

---

# 🔐 Regras de Negócio

## Palpites

* Um único palpite por usuário em cada partida.
* Não é permitido editar palpites.
* O prazo para palpitar encerra antes do início da partida.
* Não é possível palpitar após existir resultado oficial.

---

## Classificação dos Grupos

Critérios FIFA:

1. Pontos
2. Saldo de gols
3. Gols marcados
4. Confronto direto

---

## Classificação Manual

Quando houver empate não resolvido automaticamente (fair play, cartões ou decisão oficial da FIFA), o administrador pode definir manualmente a ordem dos classificados.

A classificação manual altera apenas a posição dos times.

As estatísticas permanecem preservadas.

---

# 📈 Status do Projeto

✅ Cadastro e Login

✅ Palpites

✅ Ranking Geral

✅ Grupos Privados

✅ Classificação Automática

✅ Classificação Manual

✅ Melhor Terceiro Colocado

✅ Chaveamento FIFA 2026

✅ Pênaltis

✅ Painel Administrativo

✅ Aplicativo Mobile

---

# 👨‍💻 Autor

**Boris Oliveira**

Graduando em Ciência da Computação - UERN

Projeto desenvolvido para estudo, prática de desenvolvimento full stack e acompanhamento da Copa do Mundo FIFA 2026.
