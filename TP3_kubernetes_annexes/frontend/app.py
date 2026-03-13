from flask import Flask, render_template_string
import requests

app = Flask(__name__)

# C'est ici la magie K8s : on va utiliser le nom du futur Service Kubernetes !
BACKEND_URL = "http://backend-service:5000/api/message"

@app.route('/')
def home():
    try:
        # Le frontend (côté serveur) appelle le backend
        reponse = requests.get(BACKEND_URL, timeout=5)
        data = reponse.json()
        message = data.get("message", "Message introuvable")
    except Exception as e:
        message = f"Erreur de connexion au backend : {e}"

    # On affiche une jolie petite page HTML
    html = f"""
    <html>
        <head><title>Frontend TP3</title></head>
        <body style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h1>Interface Frontend 🌐</h1>
            <div style="padding: 20px; background-color: #e0f7fa; display: inline-block; border-radius: 10px; border: 2px solid #00acc1;">
                <h2>Message du backend : <br><span style="color: #00695c;">{message}</span></h2>
            </div>
        </body>
    </html>
    """
    return render_template_string(html)

if __name__ == '__main__':
    # Le frontend tournera sur le port 8080
    app.run(host='0.0.0.0', port=8080)