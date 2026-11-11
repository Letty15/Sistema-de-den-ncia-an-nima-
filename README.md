![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white) ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white) ![IF Baiano](https://img.shields.io/badge/IF%20Baiano-Campus%20Guanambi-green?style=for-the-badge)

# Sistema de Denúncia Anônima para Mulheres no Ambiente Escolar
> Uma plataforma web em Django para o registro sigiloso de denúncias de violência de gênero no ambiente escolar.

## Sumário 📒
[Sobre o projeto 🔍](#sobre-o-projeto-)  
[Funcionalidades ✨](#funcionalidades-)  
[Perfis e permissões 🔐](#perfis-e-permissões-)  
[Tecnologias utilizadas ⚒️](#tecnologias-utilizadas-️)  
[Estrutura do projeto 🗂️](#estrutura-do-projeto-️)  
[Requisitos 📄](#requisitos-)  
[Configuração ⚙️](#configuração-️)  
[Execução ▶️](#execução-️)  
[Status do projeto 🚧](#status-do-projeto-)  
[Contribuições ➕](#contribuições-)  
[Licença 📃](#licença-)  
[Autoras e orientação 👥](#autoras-e-orientação-)

## Sobre o projeto 🔍
Aplicação web desenvolvida por alunas do curso Técnico Integrado em Informática para Internet do IF Baiano – Campus Guanambi, em 2026, para as disciplinas de **Projeto de Conclusão de Curso (PCC)** e **Programação de Sistemas Web (PSW)**.

A plataforma permite que mulheres, mediante cadastro e login, registrem denúncias de qualquer forma de violência sofrida na escola, com a **identidade preservada perante as demais usuárias**. Os dados identificadores ficam acessíveis apenas ao **Conselho de Acompanhamento Escolar (CAE)**, que analisa, responde e encaminha as ocorrências. Também oferece **conteúdos educativos** e **canais de apoio** (como Ligue 180 e 190).

> ℹ️ O sistema não oferece anonimato absoluto: a denunciante é identificada para que o CAE possa acolhê-la e acompanhar o caso, sem exposição a colegas, professores ou agressores. O tratamento de dados segue as diretrizes da **LGPD** (Lei nº 13.709/2018).

## Funcionalidades ✨
* Cadastro e login de usuárias
* Registro de denúncias com tipo de violência e descrição
* Protocolo único gerado automaticamente (12 caracteres)
* Acompanhamento em "Minhas denúncias" com status: Pendente, Em análise, Encaminhada ao CAE e Concluída
* Respostas do CAE vinculadas ao protocolo
* Painel do CAE para ver todas as denúncias, alterar status e responder
* Conteúdos educativos (Direitos, Prevenção e Impactos psicológicos) e canais de apoio
* Gerenciamento de usuárias pelo CAE

## Perfis e permissões 🔐
Os grupos **CAE** e **Denunciante** são criados automaticamente por *data migration*. Usuárias que se cadastram entram no grupo Denunciante.

| Ação | Visitante | Denunciante | CAE |
|---|:---:|:---:|:---:|
| Ver conteúdos e canais de apoio | ✅ | ✅ | ✅ |
| Registrar, ver, editar e excluir **as próprias** denúncias | ❌ | ✅ | ❌ |
| Ver **todas** as denúncias (somente leitura) | ❌ | ❌ | ✅ |
| Alterar status e responder denúncias | ❌ | ❌ | ✅ |
| Gerenciar conteúdos, canais de apoio e usuárias | ❌ | ❌ | ✅ |

A regra de acesso a cada denúncia está em `denuncias/regras.py`.

## Tecnologias utilizadas ⚒️
* Python e Django (views baseadas em funções)
* SQLite
* Pillow
* HTML com *templates* do Django
* Git

## Estrutura do projeto 🗂️
```
administracao/      # Grupos CAE e Denunciante e permissões
conteudos/          # Conteúdos educativos e canais de apoio
denuncia_anonima/   # Configurações do projeto (settings, urls)
denuncias/          # Denúncias, tipos de violência, evidências e regras de acesso
respostas/          # Respostas do CAE às denúncias
usuarios/           # Cadastro, login e gestão de usuárias
templates/          # Layout base
diagramas/          # Diagrama de classes
initial_data.json
manage.py
requirements.txt
```

## Requisitos 📄
* Python 3.12 ou superior
* pip e Git

## Configuração ⚙️
### 1. Clone e acesse o projeto
```
git clone <URL_DO_REPOSITORIO>
cd Sistema-de-denuncia-anonima
```

### 2. Crie e ative um ambiente virtual
```powershell
# Windows
python -m venv venv
venv\Scripts\activate
```
```shell
# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências e aplique as migrações
```
pip install -r requirements.txt
python manage.py migrate
```

### 4. Crie um superusuário
```
python manage.py createsuperuser
```

### 5. Configure pelo `/admin`
* Cadastre ao menos um **Tipo de violência** (sem isso o formulário de denúncia fica vazio)
* Para criar um membro do CAE, crie o usuário e adicione-o ao grupo **CAE**

## Execução ▶️
```
python manage.py runserver
```
Acesse `http://127.0.0.1:8000/` (a página inicial mostra os conteúdos educativos). Para rodar os testes: `python manage.py test`.

Em produção, defina as variáveis `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False` e `DJANGO_ALLOWED_HOSTS` (hosts separados por vírgula).

## Status do projeto 🚧
Em desenvolvimento, com finalização do protótipo prevista para **dezembro de 2026**. A validação feita até aqui (11 participantes) usou apenas imagens das telas, não a plataforma em funcionamento.

Próximos passos:
- [ ] Ampliar os materiais educativos
- [ ] Melhorar contraste de cores e acessibilidade visual
- [ ] Testes em ambiente controlado, incluindo controle de acesso e proteção de dados (LGPD)
- [ ] Anexar evidências visuais à denúncia (o modelo `Imagem` já existe)
- [ ] Incluir local, data aproximada e opção de retorno no formulário de denúncia

## Contribuições ➕
Por se tratar de um projeto escolar, o projeto não aceita contribuições.

## Licença 📃
Este projeto é de uso educacional. Todos os direitos reservados às autoras.

## Autoras e orientação 👥
- Eloany R. Carvalho - [@eloany15](https://github.com/eloany15)
- Lara M. Rodrigues - [@lararg0910](https://github.com/lararg0910)
- Letícia B. Silva - [@Letty15](https://github.com/Letty15)
- Profª. Sara Monicky (orientadora) - [@](https://github.com/)
- Profª. Jamile da Silva Ramos - [@jamile-ramos](https://github.com/jamile-ramos)
- Prof. Dr. Carlos Anderson - [@](https://github.com/)