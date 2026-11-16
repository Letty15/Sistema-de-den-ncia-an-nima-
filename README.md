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

> ℹ️ O sistema não oferece anonimato absoluto: a denunciante é identificada para que o CAE possa acolhê-la e acompanhar o caso, sem exposição a colegas, professores ou agressores. No cadastro são coletados nome de usuário, e-mail, **CPF, RG e endereço**, visíveis apenas ao CAE. O tratamento de dados segue as diretrizes da **LGPD** (Lei nº 13.709/2018).

## Funcionalidades ✨
* Cadastro e login de usuárias (com CPF, RG e endereço) e logout
* Registro de denúncias com tipo de violência e descrição
* Anexo de **evidências em imagem** (até 5 por denúncia, de até 5 MB cada, nos formatos JPG, PNG ou WEBP)
* Protocolo único gerado automaticamente (12 caracteres)
* "Minhas denúncias": a denunciante vê, edita (inclusive as evidências) e exclui as próprias denúncias e acompanha o status: Pendente, Em análise, Encaminhada ao CAE e Concluída
* Respostas do CAE vinculadas ao protocolo, visíveis à denunciante dona da denúncia
* Painel do CAE com totais e denúncias recentes na página inicial, lista de todas as denúncias com filtro por status, alteração de status e respostas
* Conteúdos educativos (Direitos, Prevenção e Impactos psicológicos, filtráveis por categoria) e canais de apoio, com cadastro, edição e exclusão pelo CAE
* Gerenciamento de usuárias pelo CAE (listar, detalhar, editar e excluir)

## Perfis e permissões 🔐
Os grupos **CAE** e **Denunciante** são criados automaticamente por *data migration*. Usuárias que se cadastram entram no grupo Denunciante.

| Ação | Visitante | Denunciante | CAE |
|---|:---:|:---:|:---:|
| Ver conteúdos e canais de apoio | ✅ | ✅ | ✅ |
| Registrar, ver, editar e excluir **as próprias** denúncias | ❌ | ✅ | ❌ |
| Ver as respostas do CAE às **próprias** denúncias | ❌ | ✅ | ✅ |
| Ver **todas** as denúncias (somente leitura) | ❌ | ❌ | ✅ |
| Alterar status e responder denúncias | ❌ | ❌ | ✅ |
| Gerenciar conteúdos e canais de apoio | ❌ | ❌ | ✅ |
| Listar, editar e excluir usuárias | ❌ | ❌ | ✅ |

A regra de acesso a cada denúncia está em `denuncias/regras.py`. Não é possível excluir uma usuária que tenha denúncias registradas, nem a própria conta.

## Tecnologias utilizadas ⚒️
* Python e Django (views baseadas em funções)
* Autenticação com `django.contrib.auth` (login, logout, grupos, permissões e decorators `login_required`/`permission_required`)
* SQLite
* Pillow (validação e armazenamento das imagens de evidência)
* HTML com *templates* do Django e CSS próprio
* Git

## Estrutura do projeto 🗂️
```
administracao/      # Grupos CAE e Denunciante e permissões (data migrations)
conteudos/          # Conteúdos educativos e canais de apoio
denuncia_anonima/   # Configurações do projeto (settings, urls) e página inicial
denuncias/          # Denúncias, tipos de violência, evidências e regras de acesso
respostas/          # Respostas do CAE às denúncias
usuarios/           # Cadastro, login e gestão de usuárias
templates/          # Layouts base e página inicial
static/             # CSS e imagens estáticas
diagramas/          # Diagrama de classes
manage.py
requirements.txt
```

## Requisitos 📄
* Python 3.12 ou superior
* pip e Git

As dependências (Django 6.1, Pillow, entre outras) estão em `requirements.txt`.

## Configuração ⚙️
### 1. Clone e acesse o projeto
```
git clone https://github.com/Letty15/Sistema-de-den-ncia-an-nima-.git
cd Sistema-de-den-ncia-an-nima-
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
* Cadastre também os **canais de apoio** e os **conteúdos educativos** (ou faça isso pelo próprio sistema, logada como CAE)

## Execução ▶️
```
python manage.py runserver
```
Acesse `http://127.0.0.1:8000/` (a página inicial reúne os atalhos para registrar denúncia, ver conteúdos, canais de apoio, entrar e cadastrar-se). Para rodar os testes: `python manage.py test`.

Em produção, defina as variáveis `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False` e `DJANGO_ALLOWED_HOSTS` (hosts separados por vírgula). Com `DEBUG=False`, o Django não serve os arquivos de `media/` (evidências); o servidor web precisa ser configurado para isso.

## Status do projeto 🚧
Em desenvolvimento, com finalização do protótipo prevista para **dezembro de 2026**. A validação feita até aqui (11 participantes) usou apenas imagens das telas, não a plataforma em funcionamento.

Próximos passos:
- [ ] Ampliar os materiais educativos
- [ ] Melhorar contraste de cores e acessibilidade visual
- [ ] Testes em ambiente controlado, incluindo controle de acesso e proteção de dados (LGPD)
- [ ] Incluir local, data aproximada e opção de retorno no formulário de denúncia

## Contribuições ➕
Por se tratar de um projeto escolar, o projeto não aceita contribuições.

## Licença 📃
Este projeto é de uso educacional. Todos os direitos reservados às autoras.

## Autoras e orientação 👥
- Eloany R. Carvalho - [@eloany15](https://github.com/eloany15)
- Lara M. Rodrigues - [@lararg0910](https://github.com/lararg0910)
- Letícia B. Silva - [@Letty15](https://github.com/Letty15)
- Profª. Sara Monicky (orientadora)
- Profª. Jamile da Silva Ramos - [@jamile-ramos](https://github.com/jamile-ramos)
- Prof. Dr. Carlos Anderson