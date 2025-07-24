# 🍔 Py-Delivery Frontend

Este é um frontend simples em **Flask** para consumir uma API RESTful de delivery.

✅ **Principais funcionalidades:**
- Tela de **Login** e **Cadastro** de usuário.
- Tela **Home** com listagem de produtos vinda da API.
- Função de **Criar Pedido** escolhendo quantidades de produtos.
- Tela de **Pedidos** do usuário, com possibilidade de avaliar cada pedido.
- Tela de **Criar Produto** com pré-visualização de imagem antes de salvar.

---

## 🚀 Tecnologias utilizadas

- **Python 3.13**
- **Flask** (framework web)
- **HTML5 / CSS3**
- **Jinja2** (templates dinâmicos)
- Conexão com API RESTful usando **requests**

---

## 📦 Como rodar o projeto

1. **Clone o repositório**
```bash
git clone https://github.com/jefim9413/py-delivery.git
cd seuprojeto
```

2. **Crie um ambiente virtual e instale dependências**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate   # Windows

pip install flask requests
```

3. **Configure a URL da API**
> Edite o arquivo `app.py` e defina a variável `API_BASE` com o endereço da sua API.
```python
API_BASE = "https://delivery-api-i9pg.onrender.com"
```

4. **Execute o servidor**
```bash
python app.py
```
> Por padrão, ele rodará em: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🖼️ Estrutura de pastas

```
py-delivery/
│
├── app.py                # Lógica Flask
├── requirements.txt      # Dependências (opcional)
└── templates/            # Templates HTML
    ├── login.html
    ├── cadastro.html
    ├── home.html
    ├── pedidos.html
    └── criar_produto.html
```

---

## ✨ Funcionalidades detalhadas

### 🔑 Login & Cadastro
- Usuário pode se cadastrar.
- Após cadastro, pode logar e receber um token de sessão.

### 🏠 Home
- Lista produtos da API.
- Permite escolher quantidade e enviar pedido (rota `create orders`).

### 📋 Pedidos
- Lista pedidos do usuário.
- Permite avaliar pedido pendente.
- Mostra nota/comentário se já avaliado.

### ➕ Criar Produto
- Formulário para criar um novo produto via POST na API.
- Pré‑visualização da imagem ao digitar o link.

---

## 📌 Observações
- Ajuste a URL da API (`API_BASE`) conforme necessário.
- Alguns endpoints podem requerer token de autenticação; o app está preparado para usar `session['token']`.

---

