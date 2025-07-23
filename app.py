from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests

app = Flask(__name__)
app.secret_key = "sua_chave_secreta_aqui"  # necessário para usar session

API_BASE = "https://delivery-api-i9pg.onrender.com"

# -----------------------
# Tela de Login
# -----------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        # Faz login na API
        r = requests.post(f"{API_BASE}/sessions", json={"email": email, "password": password})
        if r.status_code == 200:
            token = r.json().get("token")
            session["token"] = token
            return redirect(url_for("home"))
        else:
            flash("Login inválido. Tente novamente.")
    return render_template("login.html")


# -----------------------
# Tela de Cadastro
# -----------------------
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        password = request.form["password"]
        r = requests.post(f"{API_BASE}/users", json={"name": nome, "email": email, "password": password})
        if r.status_code == 201:
            flash("Cadastro realizado! Faça login.")
            return redirect(url_for("login"))
        else:
            flash("Erro ao cadastrar.")
    return render_template("cadastro.html")


# -----------------------
# Tela Home (lista produtos)
# -----------------------
@app.route("/home")
def home():
    token = session.get("token")
    if not token:
        return redirect(url_for("login"))

    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{API_BASE}/products", headers=headers)
    produtos = []
    if r.status_code == 200:
        dados = r.json()
        produtos = dados.get("products", []) 
    return render_template("home.html", produtos=produtos)


@app.route("/criar_pedido", methods=["POST"])
def criar_pedido():
    token = session.get("token")
    if not token:
        flash("Você precisa fazer login.")
        return redirect(url_for("login"))

    # Montar lista de items
    items = []
    for key, value in request.form.items():
        if key.startswith("quantidade_"):
            product_id = key.replace("quantidade_", "")
            quantidade = int(value)
            if quantidade > 0:
                items.append({
                    "productId": product_id,
                    "quantity": quantidade
                })

    if not items:
        flash("Nenhum produto selecionado.")
        return redirect(url_for("home"))

    payload = {
        "status": "Pendente",
        "items": items
    }

    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(f"{API_BASE}/orders", json=payload, headers=headers)

    if r.status_code in (200, 201):
        flash("Pedido criado com sucesso! 🎉")
    else:
        flash(f"Erro ao criar pedido: {r.status_code} - {r.text}")

    return redirect(url_for("home"))

@app.route("/pedidos")
def pedidos():
    token = session.get("token")
    if not token:
        flash("Você precisa fazer login.")
        return redirect(url_for("login"))

    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{API_BASE}/orders", headers=headers)

    pedidos = []
    if r.status_code == 200:
        pedidos = r.json().get("orders", []) if isinstance(r.json(), dict) else r.json()

    return render_template("pedidos.html", pedidos=pedidos)


@app.route("/avaliar_pedido/<order_id>", methods=["POST"])
def avaliar_pedido(order_id):
    token = session.get("token")
    if not token:
        flash("Você precisa fazer login.")
        return redirect(url_for("login"))

    nota = int(request.form.get("nota", 0))
    comentario = request.form.get("comentario", "")

    payload = {
        "rating": nota,
        "ratingComment": comentario
    }

    headers = {"Authorization": f"Bearer {token}"}
    r = requests.patch(f"{API_BASE}/orders/{order_id}/rating", json=payload, headers=headers)

    if r.status_code in (200, 201):
        flash("Avaliação enviada com sucesso! ✅")
    else:
        flash(f"Erro ao avaliar pedido: {r.status_code} - {r.text}")

    return redirect(url_for("pedidos"))

@app.route("/criar_produto", methods=["GET", "POST"])
def criar_produto():
    token = session.get("token")  
    if not token:
        flash("Você precisa fazer login primeiro.")
        return redirect(url_for("login"))

    if request.method == "POST":
        # Captura os dados do formulário
        nome = request.form.get("name")
        descricao = request.form.get("description")
        preco = request.form.get("price")
        imagem = request.form.get("imageUrl")

        payload = {
            "name": nome,
            "description": descricao,
            "price": float(preco),
            "imageUrl": imagem
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"  # se necessário
        }

        # Faz o POST na sua API
        url = f"{API_BASE}/products"
        r = requests.post(url, json=payload, headers=headers)

        if r.status_code in (200, 201):
            flash("✅ Produto criado com sucesso!")
            return redirect(url_for("home"))
        else:
            flash(f"❌ Erro ao criar produto: {r.status_code} - {r.text}")
            return redirect(url_for("criar_produto"))

    # Se método GET apenas exibe o formulário
    return render_template("criar_produto.html")


# -----------------------
# Logout
# -----------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
