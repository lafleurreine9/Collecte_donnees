from flask import Flask, render_template_string, request
import os

app = Flask(__name__)
FILE = "donnees.csv"

HTML = """
<!DOCTYPE html>
<html>
<head><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="font-family:sans-serif; padding:15px; background:#f4f4f4;">
    <div style="background:white; padding:15px; border-radius:10px; box-shadow:0 2px 5px rgba(0,0,0,0.1);">
        <h2 style="color:green;">🛒 Eco-Prix Yaoundé</h2>
        <form method="POST">
            Produit: <input type="text" name="p" required style="width:100%; padding:8px;"><br><br>
            Prix (FCFA): <input type="number" name="v" required style="width:100%; padding:8px;"><br><br>
            <button type="submit" style="width:100%; background:green; color:white; padding:10px; border:none; border-radius:5px;">Enregistrer</button>
        </form>
    </div>
    <div style="margin-top:20px; background:#e8f5e9; padding:15px; border-radius:10px; border-left:5px solid green;">
        <h3>📊 Analyse Descriptive</h3>
        {{ info | safe }}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        with open(FILE, "a") as f:
            f.write(f"{request.form['p']},{request.form['v']}\n")
    
    info = "<i>Aucune donnée enregistrée.</i>"
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            lignes = [l.strip() for l in f.readlines() if l.strip()]
            if lignes:
                prix = [float(l.split(',')[1]) for l in lignes]
                moyenne = sum(prix) / len(prix)
                info = f"<b>Nombre d'articles :</b> {len(prix)}<br><b>Prix Moyen :</b> {moyenne:.0f} FCFA<br><b>Prix Max :</b> {max(prix):.0f} FCFA"
    
    return render_template_string(HTML, info=info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


