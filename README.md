![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white) ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white) ![IF Baiano](https://img.shields.io/badge/IF%20Baiano-Campus%20Guanambi-green?style=for-the-badge)

# Sistema de Denúncia Anônima para Mulheres no Ambiente Escolar

> Uma plataforma web em Django para o registro sigiloso de denúncias de violência de gênero no ambiente escolar.

## Sumário 📒

- [Sobre o projeto 🔍](#sobre-o-projeto-)
- [Funcionalidades ✨](#funcionalidades-)
- [Perfis e permissões 🔐](#perfis-e-permissões-)
- [Tecnologias utilizadas ⚒️](#tecnologias-utilizadas-)
- [Estrutura do projeto 🗂️](#estrutura-do-projeto-)
- [Requisitos 📄](#requisitos-)
- [Configuração ⚙️](#configuração-)
- [Execução ▶️](#execução-)
- [Status do projeto 🚧](#status-do-projeto-)
- [Contribuições ➕](#contribuições-)
- [Licença 📃](#licença-)
- [Autoras e orientação 👥](#autoras-e-orientação-)

## Sobre o projeto 🔍

Aplicação web desenvolvida por alunas do curso Técnico Integrado em Informática para Internet do IF Baiano – Campus Guanambi, em 2026, para as disciplinas de **Projeto de Conclusão de Curso (PCC)** e **Programação de Sistemas Web (PSW)**.

A plataforma permite que mulheres, mediante cadastro e login, registrem denúncias de violência sofrida no ambiente escolar, com a **identidade preservada perante as demais usuárias**. O Conselho de Acompanhamento Escolar (CAE) possui permissões para consultar e acompanhar as denúncias, responder às ocorrências e atualizar seus status. O sistema também oferece **conteúdos educativos** e **canais de apoio**, como Ligue 180 e 190.

> ℹ️ O sistema não oferece anonimato absoluto: a denunciante precisa estar identificada para registrar e acompanhar sua denúncia. A identidade não é exibida às demais denunciantes. O cadastro solicita nome de usuário, e-mail, **CPF, RG e endereço**. As telas de gerenciamento de usuárias são protegidas por permissões atribuídas ao CAE. O CPF passa por validação de formato e dos dígitos verificadores. Essa validação não consulta a Receita Federal nem confirma a titularidade do documento. O tratamento dos dados deve observar as diretrizes da **LGPD** (Lei nº 13.709/2018).

## Funcionalidades ✨

- Cadastro, login e logout de usuárias.
- Cadastro com nome de usuário, e-mail, CPF, RG e endereço.
- Validação do CPF no cadastro e na edição dos dados, incluindo formato e dígitos verificadores.
- Registro de denúncias com tipo de violência e descrição.
- Anexo de evidências em imagem: até 5 por denúncia, com tamanho máximo de 5 MB cada, nos formatos JPG, PNG ou WEBP.
- Geração automática de protocolo único com 12 caracteres.
- Área **Minhas denúncias**, na qual a denunciante pode visualizar, editar e excluir suas próprias denúncias e acompanhar seus status.
- Respostas da CAE vinculadas às denúncias, com identificação do autor e data de envio.
- Histórico de alterações de status, registrando o status anterior, o novo status, o responsável pela alteração e a data.
- Notificações internas para a denunciante quando a CAE envia uma nova resposta.
- Painel da CAE com listagem de denúncias e filtros por status.
- Conteúdos educativos sobre Direitos, Prevenção e Impactos psicológicos, filtráveis por categoria.
- Canais de apoio, com cadastro, edição e exclusão pelo CAE.
- Gerenciamento de usuárias pelo CAE.

## Perfis e permissões 🔐

Os grupos **CAE** e **Denunciante** são criados por migrações de dados. Durante o cadastro, a usuária é adicionada ao grupo Denunciante.

| Ação | Visitante | Denunciante | CAE |
|---|:---:|:---:|:---:|
| Receber notificações sobre as próprias denúncias | ❌ | ✅ | ❌ |
| Consultar o histórico de alterações de status das denúncias que pode acessar | ❌ | ✅ | ✅ |
| Ver conteúdos e canais de apoio | ✅ | ✅ | ✅ |
| Registrar, visualizar, editar e excluir as próprias denúncias | ❌ | ✅ | ❌ |
| Ver as respostas do CAE às próprias denúncias | ❌ | ✅ | ✅ |
| Ver todas as denúncias | ❌ | ❌ | ✅ |
| Alterar status e responder denúncias | ❌ | ❌ | ✅ |
| Gerenciar conteúdos e canais de apoio | ❌ | ❌ | ✅ |
| Listar, editar e excluir usuárias | ❌ | ❌ | ✅ |

A regra de acesso às denúncias está definida em `denuncias/regras.py`. Uma usuária pode visualizar apenas as próprias denúncias, enquanto o CAE possui permissão para consultar todas. Não é possível excluir uma usuária que tenha denúncias registradas, nem excluir a própria conta pela funcionalidade de gerenciamento.

## Tecnologias utilizadas ⚒️

- Python e Django, com views baseadas em funções.
- Autenticação com `django.contrib.auth` (login, logout, grupos, permissões e decorators `login_required` e `permission_required`).
- SQLite.
- Pillow, para validação e armazenamento das imagens de evidência.
- HTML com templates do Django e CSS próprio.
- Git.

## Estrutura do projeto 🗂️

```text
administracao/      # Grupos CAE e Denunciante e permissões (migrações de dados)
conteudos/          # Conteúdos educativos e canais de apoio
denuncia_anonima/   # Configurações do projeto (settings, urls) e página inicial
denuncias/          # Denúncias, tipos de violência, evidências e regras de acesso
respostas/          # Respostas do CAE e notificações
usuarios/           # Cadastro, login e gestão de usuárias
templates/          # Layouts base e página inicial
static/             # CSS e imagens estáticas
diagramas/          # Diagrama de classes
manage.py
requirements.txt
```

## Requisitos 📄

- Python 3.12 ou superior.
- pip e Git.

As dependências do projeto, incluindo Django e Pillow, estão especificadas em `requirements.txt`.

## Configuração ⚙️

### 1. Clone e acesse o projeto

```bash
git clone https://github.com/Letty15/Sistema-de-den-ncia-an-nima-.git
cd Sistema-de-den-ncia-an-nima-
```

### 2. Crie e ative um ambiente virtual

**Windows:**

```powershell
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**

```shell
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências e aplique as migrações

```bash
pip install -r requirements.txt
python manage.py migrate
```

### 4. Crie um superusuário

```bash
python manage.py createsuperuser
```

### 5. Configure pelo `/admin`

- Cadastre ao menos um **Tipo de violência**. Sem isso, o formulário de denúncia ficará sem opções.
- Para criar um membro do CAE, crie o usuário e adicione-o ao grupo **CAE**.
- Cadastre também os **canais de apoio** e os **conteúdos educativos**, ou faça isso pelo próprio sistema, com uma conta que tenha as permissões do CAE.

## Execução ▶️

Inicie o servidor de desenvolvimento:

```bash
python manage.py runserver
```

Acesse [http://127.0.0.1:8000/](http://127.0.0.1:8000/). A página inicial reúne os atalhos para registrar denúncias, consultar conteúdos educativos, acessar canais de apoio, entrar e cadastrar-se.

Para executar os testes automatizados:

```bash
python manage.py test
```

Em produção, configure as variáveis `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False` e `DJANGO_ALLOWED_HOSTS` (com os hosts separados por vírgula). Com `DEBUG=False`, o Django não serve diretamente os arquivos de `media/`, onde ficam armazenadas as evidências. O servidor web precisa ser configurado para disponibilizá-los de forma adequada e segura.

## Status do projeto 🚧

Em desenvolvimento, com finalização do protótipo prevista para **dezembro de 2026**. A validação realizada até o momento, com 11 participantes, utilizou imagens das telas, e não a plataforma em funcionamento.

Próximos passos:

- [ ] Ampliar os materiais educativos.
- [ ] Melhorar o contraste de cores e a acessibilidade visual.
- [ ] Realizar testes em ambiente controlado, incluindo controle de acesso e proteção de dados (LGPD).
- [ ] Incluir local, data aproximada e opção de retorno no formulário de denúncia.
- [ ] Implementar notificações para a denunciante quando o status de uma denúncia for alterado.

## Contribuições ➕

Por se tratar de um projeto escolar, o projeto não aceita contribuições externas.

## Licença 📃

Este projeto é de uso educacional. Todos os direitos reservados às autoras.

## Autoras e orientação 👥

- Eloany R. Carvalho - [@eloany15](https://github.com/eloany15)
- Lara M. Rodrigues - [@lararg0910](https://github.com/lararg0910)
- Letícia B. Silva - [@Letty15](https://github.com/Letty15)
- Profª. Sara Monicky (orientadora)
- Profª. Jamile da Silva Ramos - [@jamile-ramos](https://github.com/jamile-ramos)
- Prof. Dr. Carlos Anderson