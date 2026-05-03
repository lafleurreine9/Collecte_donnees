from flask import Flask, render_template_string, request, session
import os
import math
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'eco_prix_key_2024'
FILE = "donnees.csv"

HTML = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <title>Eco-Prix Yaoundé - Gestion des Sessions</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,600;14..32,700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            position: relative;
            overflow-x: hidden;
        }

        /* Effet de particules animées */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: radial-gradient(circle at 20% 40%, rgba(255,255,255,0.1) 1px, transparent 1px);
            background-size: 30px 30px;
            pointer-events: none;
            animation: float 20s linear infinite;
        }

        @keyframes float {
            0% { transform: translateY(0px) rotate(0deg); }
            100% { transform: translateY(-50px) rotate(360deg); }
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            position: relative;
            z-index: 1;
        }

        /* Animations d'entrée */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes slideInLeft {
            from {
                opacity: 0;
                transform: translateX(-50px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        @keyframes slideInRight {
            from {
                opacity: 0;
                transform: translateX(50px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }

        .card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 24px;
            padding: 28px;
            margin-bottom: 24px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.15);
            transition: all 0.3s ease;
            animation: fadeInUp 0.6s ease-out;
            border: 1px solid rgba(255,255,255,0.2);
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 30px 70px rgba(0,0,0,0.2);
        }

        /* Cartes avec délais d'animation différents */
        .card:nth-child(1) { animation-delay: 0.1s; }
        .card:nth-child(2) { animation-delay: 0.2s; }
        .card:nth-child(3) { animation-delay: 0.3s; }
        .card:nth-child(4) { animation-delay: 0.4s; }

        /* Header premium */
        .hero-card {
            background: linear-gradient(135deg, #1a472a 0%, #2e7d32 100%);
            color: white;
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        .hero-card::before {
            content: '🛒';
            position: absolute;
            font-size: 200px;
            opacity: 0.1;
            bottom: -30px;
            right: -30px;
            transform: rotate(-15deg);
        }

        .hero-card h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            font-weight: 700;
            letter-spacing: -0.5px;
        }

        .hero-card p {
            font-size: 1rem;
            opacity: 0.9;
            margin-bottom: 20px;
        }

        .session-badge {
            display: inline-flex;
            align-items: center;
            gap: 15px;
            background: rgba(255,255,255,0.2);
            padding: 10px 25px;
            border-radius: 50px;
            backdrop-filter: blur(5px);
        }

        .session-badge span {
            font-weight: 600;
        }

        /* Formulaire moderne */
        .form-group {
            margin-bottom: 20px;
        }

        .form-row {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }

        .form-row input {
            flex: 1;
        }

        input, select {
            width: 100%;
            padding: 14px 18px;
            border: 2px solid #e0e0e0;
            border-radius: 14px;
            font-size: 15px;
            font-family: 'Inter', sans-serif;
            transition: all 0.3s ease;
            background: white;
        }

        input:focus {
            outline: none;
            border-color: #2e7d32;
            box-shadow: 0 0 0 3px rgba(46,125,50,0.1);
            transform: translateY(-2px);
        }

        /* Boutons stylisés */
        .btn {
            padding: 14px 28px;
            border: none;
            border-radius: 14px;
            font-size: 15px;
            font-weight: 600;
            font-family: 'Inter', sans-serif;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            text-decoration: none;
        }

        .btn-primary {
            background: linear-gradient(135deg, #2e7d32, #1b5e20);
            color: white;
            box-shadow: 0 4px 15px rgba(46,125,50,0.3);
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(46,125,50,0.4);
        }

        .btn-secondary {
            background: linear-gradient(135deg, #ff9800, #f57c00);
            color: white;
        }

        .btn-danger {
            background: linear-gradient(135deg, #f44336, #d32f2f);
            color: white;
        }

        .btn-outline {
            background: transparent;
            border: 2px solid #2e7d32;
            color: #2e7d32;
        }

        .btn-outline:hover {
            background: #2e7d32;
            color: white;
        }

        .btn-sm {
            padding: 8px 16px;
            font-size: 13px;
        }

        .btn-group {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            margin-top: 15px;
        }

        /* Table moderne */
        .table-container {
            overflow-x: auto;
            border-radius: 16px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        th {
            background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
            padding: 15px;
            text-align: left;
            font-weight: 600;
            color: #1b5e20;
        }

        td {
            padding: 12px 15px;
            border-bottom: 1px solid #f0f0f0;
        }

        tr:hover {
            background: #f5f5f5;
        }

        /* Grille de statistiques */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 25px;
        }

        .stat-card {
            background: linear-gradient(135deg, #f8fff8, #e8f5e9);
            padding: 20px;
            border-radius: 20px;
            text-align: center;
            transition: all 0.3s ease;
            border: 1px solid rgba(46,125,50,0.2);
        }

        .stat-card:hover {
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }

        .stat-icon {
            font-size: 35px;
            color: #2e7d32;
            margin-bottom: 10px;
        }

        .stat-value {
            font-size: 28px;
            font-weight: 800;
            color: #1b5e20;
        }

        .stat-label {
            font-size: 13px;
            color: #666;
            margin-top: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* Badges et alertes */
        .alert-success {
            background: linear-gradient(135deg, #d4edda, #c3e6cb);
            color: #155724;
            padding: 15px 20px;
            border-radius: 14px;
            margin-bottom: 20px;
            border-left: 4px solid #2e7d32;
            animation: slideInLeft 0.5s ease-out;
        }

        .alert-info {
            background: linear-gradient(135deg, #d1ecf1, #bee5eb);
            color: #0c5460;
            padding: 15px 20px;
            border-radius: 14px;
            margin-bottom: 20px;
        }

        /* Produit vide */
        .empty-state {
            text-align: center;
            padding: 50px;
            color: #999;
        }

        .empty-state i {
            font-size: 60px;
            margin-bottom: 15px;
            opacity: 0.5;
        }

        /* Responsive */
        @media (max-width: 768px) {
            body {
                padding: 12px;
            }
            .card {
                padding: 18px;
            }
            .hero-card h1 {
                font-size: 1.8rem;
            }
            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
                gap: 12px;
            }
            .stat-value {
                font-size: 22px;
            }
            .btn-group {
                justify-content: center;
            }
        }
    </style>
</head>
<body>
<div class="container">
    <!-- En-tête Hero -->
    <div class="card hero-card">
        <h1><i class="fas fa-store"></i> Eco-Prix Yaoundé</h1>
        <p>Gestion intelligente des sessions d'achats | Analyse statistique en temps réel</p>
        <div class="session-badge">
            <span><i class="fas fa-calendar-alt"></i> Session active :</span>
            <strong>{{ session_id }}</strong>
            <span class="badge-count"><i class="fas fa-boxes"></i> {{ session_count }} produits</span>
        </div>
    </div>

    <!-- Formulaire d'ajout -->
    <div class="card">
        <h2 style="margin-bottom: 20px; display: flex; align-items: center; gap: 10px;">
            <i class="fas fa-plus-circle" style="color: #2e7d32;"></i> Ajouter un produit
        </h2>
        <form method="POST" action="{{ url_for('add_product') }}">
            <div class="form-row">
                <input type="text" name="product" placeholder="🏷️ Nom du produit" required>
                <input type="number" name="price" placeholder="💰 Prix (FCFA)" step="any" required>
                <button type="submit" class="btn btn-primary">
                    <i class="fas fa-save"></i> Enregistrer
                </button>
            </div>
        </form>
        <div class="btn-group">
            <form method="POST" action="{{ url_for('new_session') }}">
                <button type="submit" class="btn btn-secondary">
                    <i class="fas fa-plus"></i> Nouvelle session
                </button>
            </form>
            <form method="POST" action="{{ url_for('end_session') }}" onsubmit="return confirm('🏁 Terminer cette session ? Les données seront sauvegardées.')">
                <button type="submit" class="btn btn-danger">
                    <i class="fas fa-flag-checkered"></i> Terminer la session
                </button>
            </form>
        </div>
    </div>

    <!-- Liste des produits -->
    <div class="card">
        <h2 style="margin-bottom: 20px;"><i class="fas fa-list-ul"></i> Produits enregistrés</h2>
        {% if session_products %}
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th><i class="fas fa-tag"></i> Produit</th>
                        <th><i class="fas fa-money-bill-wave"></i> Prix (FCFA)</th>
                        <th><i class="fas fa-cogs"></i> Action</th>
                    </tr>
                </thead>
                <tbody>
                    {% for p in session_products %}
                    <tr>
                        <td>{{ loop.index }}</td>
                        <td><strong>{{ p.name }}</strong></td>
                        <td style="color: #2e7d32; font-weight: 600;">{{ "%.0f"|format(p.price) }} FCFA</td>
                        <td>
                            <form method="POST" action="{{ url_for('remove_product') }}" style="display:inline;">
                                <input type="hidden" name="index" value="{{ loop.index0 }}">
                                <button type="submit" class="btn btn-sm btn-danger" style="padding: 6px 12px;">
                                    <i class="fas fa-trash"></i>
                                </button>
                            </form>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        {% else %}
        <div class="empty-state">
            <i class="fas fa-shopping-cart"></i>
            <p>Aucun produit dans cette session</p>
            <p style="font-size: 14px; color: #aaa;">Ajoutez votre premier produit ci-dessus ✨</p>
        </div>
        {% endif %}
    </div>

    <!-- Statistiques détaillées -->
    <div class="card">
        <h2 style="margin-bottom: 20px;"><i class="fas fa-chart-line"></i> Analyse descriptive</h2>
        {% if session_stats %}
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-cubes"></i></div>
                <div class="stat-value">{{ session_stats.count }}</div>
                <div class="stat-label">Articles</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-coins"></i></div>
                <div class="stat-value">{{ "%.0f"|format(session_stats.sum) }}</div>
                <div class="stat-label">Total (FCFA)</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-chart-simple"></i></div>
                <div class="stat-value">{{ "%.0f"|format(session_stats.mean) }}</div>
                <div class="stat-label">Moyenne</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-chart-bar"></i></div>
                <div class="stat-value">{{ "%.2f"|format(session_stats.variance) }}</div>
                <div class="stat-label">Variance</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-arrow-down"></i></div>
                <div class="stat-value">{{ "%.0f"|format(session_stats.min) }}</div>
                <div class="stat-label">Minimum</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-arrow-up"></i></div>
                <div class="stat-value">{{ "%.0f"|format(session_stats.max) }}</div>
                <div class="stat-label">Maximum</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-chart-pie"></i></div>
                <div class="stat-value">{{ "%.0f"|format(session_stats.median) }}</div>
                <div class="stat-label">Médiane</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-waveform"></i></div>
                <div class="stat-value">{{ "%.2f"|format(session_stats.std_dev) }}</div>
                <div class="stat-label">Écart-type</div>
            </div>
        </div>
        {% if session_stats.trend %}
        <div class="alert-info" style="margin-top: 15px;">
            <h4 style="margin-bottom: 10px;"><i class="fas fa-chart-line"></i> Régression linéaire (évolution des prix)</h4>
            <div class="stats-grid" style="grid-template-columns: repeat(3, 1fr);">
                <div class="stat-card" style="background: #e3f2fd;">
                    <div class="stat-label">Direction</div>
                    <div class="stat-value" style="font-size: 20px;">
                        {% if session_stats.trend.slope > 0 %}📈 Hausse
                        {% elif session_stats.trend.slope < 0 %}📉 Baisse
                        {% else %}➡️ Stable
                        {% endif %}
                    </div>
                </div>
                <div class="stat-card" style="background: #e3f2fd;">
                    <div class="stat-label">Pente</div>
                    <div class="stat-value" style="font-size: 20px;">{{ "%.2f"|format(session_stats.trend.slope) }}</div>
                </div>
                <div class="stat-card" style="background: #e3f2fd;">
                    <div class="stat-label">R² (corrélation)</div>
                    <div class="stat-value" style="font-size: 20px;">{{ "%.3f"|format(session_stats.trend.r2) }}</div>
                </div>
            </div>
        </div>
        {% endif %}
        {% else %}
        <div class="empty-state">
            <i class="fas fa-chart-line"></i>
            <p>Ajoutez des produits pour voir les statistiques</p>
        </div>
        {% endif %}
    </div>

    <!-- Historique -->
    <div class="card">
        <h2 style="margin-bottom: 20px;"><i class="fas fa-history"></i> Historique des sessions</h2>
        {% if history %}
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>Session</th>
                        <th>Date</th>
                        <th>Articles</th>
                        <th>Total</th>
                        <th>Moyenne</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {% for h in history %}
                    <tr>
                        <td><strong>{{ h.session_id }}</strong></td>
                        <td>{{ h.timestamp }}</td>
                        <td>{{ h.count }}</td>
                        <td>{{ "%.0f"|format(h.total) }} FCFA</td>
                        <td>{{ "%.0f"|format(h.mean) }} FCFA</td>
                        <td>
                            <form method="POST" action="{{ url_for('load_session') }}" style="display:inline;">
                                <input type="hidden" name="session_id" value="{{ h.session_id }}">
                                <button type="submit" class="btn btn-sm btn-outline">
                                    <i class="fas fa-folder-open"></i> Charger
                                </button>
                            </form>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        {% else %}
        <div class="empty-state">
            <i class="fas fa-clock"></i>
            <p>Aucune session sauvegardée</p>
            <p style="font-size: 14px;">Terminez une session pour l'archiver</p>
        </div>
        {% endif %}
    </div>
</div>
</body>
</html>
"""

# ============ FONCTIONS STATISTIQUES ============
def calculate_variance(values):
    if len(values) < 2:
        return 0
    mean = sum(values) / len(values)
    return sum((x - mean) ** 2 for x in values) / len(values)

def calculate_median(values):
    if not values:
        return 0
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    if n % 2 == 0:
        return (sorted_vals[n//2 - 1] + sorted_vals[n//2]) / 2
    return sorted_vals[n//2]

def linear_regression(values):
    n = len(values)
    if n < 2:
        return None
    x = list(range(1, n + 1))
    y = values
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    denominator = sum((x[i] - mean_x) ** 2 for i in range(n))
    if denominator == 0:
        return None
    slope = numerator / denominator
    intercept = mean_y - slope * mean_x
    ss_res = sum((y[i] - (slope * x[i] + intercept)) ** 2 for i in range(n))
    ss_tot = sum((y[i] - mean_y) ** 2 for i in range(n))
    r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
    return {'slope': slope, 'r2': r2}

# ============ GESTION FICHIER ============
def save_session_to_file(session_id, products, timestamp):
    with open(FILE, "a", encoding='utf-8') as f:
        for p in products:
            f.write(f"{session_id}|{timestamp}|{p['name']}|{p['price']}\n")

def load_history_from_file():
    history = []
    sessions_data = {}
    if os.path.exists(FILE):
        with open(FILE, "r", encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 4:
                        session_id, timestamp, name, price = parts
                        price = float(price)
                        if session_id not in sessions_data:
                            sessions_data[session_id] = {'timestamp': timestamp, 'products': [], 'prices': []}
                        sessions_data[session_id]['products'].append({'name': name, 'price': price})
                        sessions_data[session_id]['prices'].append(price)
    for session_id, data in sessions_data.items():
        prices = data['prices']
        history.append({
            'session_id': session_id,
            'timestamp': data['timestamp'],
            'count': len(prices),
            'total': sum(prices),
            'mean': sum(prices) / len(prices) if prices else 0,
            'products': data['products']
        })
    history.sort(key=lambda x: x['timestamp'], reverse=True)
    return history

# ============ ROUTES FLASK ============
@app.route('/')
def home():
    if 'current_session' not in session:
        session['current_session'] = 'SESSION_001'
    if 'session_products' not in session:
        session['session_products'] = []
    if 'session_counter' not in session:
        session['session_counter'] = 1

    session_id = session['current_session']
    session_products = session.get('session_products', [])
    session_stats = None

    if session_products:
        prices = [p['price'] for p in session_products]
        stats = {
            'count': len(prices),
            'sum': sum(prices),
            'mean': sum(prices) / len(prices),
            'variance': calculate_variance(prices),
            'min': min(prices),
            'max': max(prices),
            'median': calculate_median(prices),
            'std_dev': math.sqrt(calculate_variance(prices))
        }
        if len(prices) >= 2:
            stats['trend'] = linear_regression(prices)
        session_stats = stats

    history = load_history_from_file()
    return render_template_string(HTML,
                                  session_id=session_id,
                                  session_count=len(session_products),
                                  session_products=session_products,
                                  session_stats=session_stats,
                                  history=history)

@app.route('/add', methods=['POST'])
def add_product():
    product_name = request.form.get('product', '').strip()
    price = request.form.get('price', '')
    if product_name and price:
        try:
            price = float(price)
            session.setdefault('session_products', []).append({'name': product_name, 'price': price})
            session.modified = True
        except ValueError:
            pass
    return home()

@app.route('/remove', methods=['POST'])
def remove_product():
    index = request.form.get('index')
    if index is not None:
        try:
            index = int(index)
            if 'session_products' in session and 0 <= index < len(session['session_products']):
                session['session_products'].pop(index)
                session.modified = True
        except ValueError:
            pass
    return home()

@app.route('/new_session', methods=['POST'])
def new_session():
    if session.get('session_products'):
        save_session_to_file(session['current_session'], session['session_products'], datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    session['session_counter'] = session.get('session_counter', 1) + 1
    session['current_session'] = f'SESSION_{session["session_counter"]:03d}'
    session['session_products'] = []
    session.modified = True
    return home()

@app.route('/end_session', methods=['POST'])
def end_session():
    if session.get('session_products'):
        save_session_to_file(session['current_session'], session['session_products'], datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    session['session_products'] = []
    session.modified = True
    return home()

@app.route('/load_session', methods=['POST'])
def load_session():
    session_id = request.form.get('session_id')
    for h in load_history_from_file():
        if h['session_id'] == session_id:
            session['current_session'] = session_id
            session['session_products'] = h['products']
            session.modified = True
            break
    return home()
# ==================== NOUVELLES FONCTIONNALITÉS ====================
import json
import hashlib
from datetime import datetime

# ---------- Gestion des utilisateurs ----------
USERS_FILE = "users.json"
ALERTS_FILE = "alerts.json"

def init_users():
    if not os.path.exists(USERS_FILE):
        users = {
            "admin": hashlib.sha256("admin123".encode()).hexdigest(),
            "demo": hashlib.sha256("demo".encode()).hexdigest()
        }
        with open(USERS_FILE, "w") as f:
            json.dump(users, f)

def check_user(username, password):
    if not os.path.exists(USERS_FILE):
        init_users()
    with open(USERS_FILE, "r") as f:
        users = json.load(f)
    return username in users and users[username] == hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    if not os.path.exists(USERS_FILE):
        users = {}
    else:
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
    if username in users:
        return False
    users[username] = hashlib.sha256(password.encode()).hexdigest()
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)
    return True

# ---------- Gestion des alertes ----------
def save_alert(username, product_name, max_price):
    alerts = {}
    if os.path.exists(ALERTS_FILE):
        with open(ALERTS_FILE, "r") as f:
            alerts = json.load(f)
    if username not in alerts:
        alerts[username] = []
    alerts[username].append({
        "product": product_name,
        "max_price": float(max_price),
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    with open(ALERTS_FILE, "w") as f:
        json.dump(alerts, f)

def get_alerts(username):
    if os.path.exists(ALERTS_FILE):
        with open(ALERTS_FILE, "r") as f:
            alerts = json.load(f)
        return alerts.get(username, [])
    return []

def check_alerts(username, product_name, price):
    alerts = get_alerts(username)
    triggered = []
    for alert in alerts:
        if alert["product"].lower() == product_name.lower() and price <= alert["max_price"]:
            triggered.append(alert)
    return triggered

# ---------- Recherche et filtrage ----------
def search_products(username, keyword=None, min_price=None, max_price=None):
    results = []
    if os.path.exists(FILE):
        with open(FILE, "r", encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) >= 4:
                        session_id, timestamp, name, price = parts[:4]
                        user = parts[4] if len(parts) > 4 else "unknown"
                        if user != username:
                            continue
                        price = float(price)
                        match = True
                        if keyword and keyword.lower() not in name.lower():
                            match = False
                        if min_price and price < float(min_price):
                            match = False
                        if max_price and price > float(max_price):
                            match = False
                        if match:
                            results.append({
                                'session_id': session_id,
                                'timestamp': timestamp,
                                'name': name,
                                'price': price
                            })
    return results

# ---------- Comparaison de sessions ----------
def compare_sessions(session_ids, username):
    sessions_data = []
    if os.path.exists(FILE):
        data = {}
        with open(FILE, "r", encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) >= 4:
                        sid, ts, name, price = parts[:4]
                        user = parts[4] if len(parts) > 4 else "unknown"
                        if user != username or sid not in session_ids:
                            continue
                        price = float(price)
                        if sid not in data:
                            data[sid] = {'prices': [], 'timestamp': ts, 'products': []}
                        data[sid]['prices'].append(price)
                        data[sid]['products'].append({'name': name, 'price': price})
        for sid in session_ids:
            if sid in data:
                d = data[sid]
                sessions_data.append({
                    'session_id': sid,
                    'timestamp': d['timestamp'],
                    'count': len(d['prices']),
                    'total': sum(d['prices']),
                    'mean': sum(d['prices']) / len(d['prices']) if d['prices'] else 0,
                    'products': d['products']
                })
    return sessions_data

# ---------- Routes supplémentaires ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_user(username, password):
            session['username'] = username
            session['current_session'] = f"{username}_SESSION_{int(datetime.now().timestamp())}"
            session['session_products'] = []
            return redirect(url_for('home'))
        return render_template_string(HTML_LOGIN, error="Identifiants incorrects")
    return render_template_string(HTML_LOGIN)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']
        if password != confirm:
            return render_template_string(HTML_REGISTER, error="Mots de passe différents")
        if register_user(username, password):
            return render_template_string(HTML_REGISTER, success="Inscription réussie ! Connectez-vous.")
        return render_template_string(HTML_REGISTER, error="Utilisateur existe déjà")
    return render_template_string(HTML_REGISTER)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/create_alert', methods=['POST'])
def create_alert():
    if 'username' not in session:
        return redirect(url_for('login'))
    product = request.form['product']
    max_price = request.form['max_price']
    save_alert(session['username'], product, max_price)
    return redirect(url_for('home'))

@app.route('/search_view')
def search_view():
    if 'username' not in session:
        return redirect(url_for('login'))
    keyword = request.args.get('keyword', '')
    min_price = request.args.get('min_price', '')
    max_price = request.args.get('max_price', '')
    results = search_products(session['username'], keyword, min_price, max_price)
    return render_template_string(HTML_SEARCH, results=results, keyword=keyword, min_price=min_price, max_price=max_price)

@app.route('/compare_view')
def compare_view():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template_string(HTML_COMPARE)

@app.route('/compare_sessions', methods=['POST'])
def compare_sessions_route():
    if 'username' not in session:
        return redirect(url_for('login'))
    session1 = request.form['session1']
    session2 = request.form['session2']
    comparison = compare_sessions([session1, session2], session['username'])
    return render_template_string(HTML_COMPARE, comparison=comparison, session1=session1, session2=session2)

# ---------- Templates HTML supplémentaires ----------
HTML_LOGIN = """
<!DOCTYPE html>
<html>
<head><meta name="viewport" content="width=device-width, initial-scale=1"><title>Connexion</title>
<style>
body{font-family:sans-serif;background:linear-gradient(135deg,#667eea,#764ba2);display:flex;align-items:center;justify-content:center;min-height:100vh}
.login{background:white;padding:40px;border-radius:20px;width:300px}
input{width:100%;padding:10px;margin:10px 0;border-radius:8px;border:1px solid #ddd}
button{width:100%;padding:10px;background:#2e7d32;color:white;border:none;border-radius:8px;cursor:pointer}
.error{color:red;margin:10px 0}
</style>
</head>
<body>
<div class=login>
<h2>🔐 Eco-Prix</h2>
{% if error %}<div class=error>{{ error }}</div>{% endif %}
<form method=POST>
<input type=text name=username placeholder="Nom d'utilisateur" required>
<input type=password name=password placeholder="Mot de passe" required>
<button type=submit>Connexion</button>
</form>
<p style=margin-top:15px><a href=/register>Créer un compte</a> | demo/demo</p>
</div>
</body>
</html>
"""

HTML_REGISTER = """
<!DOCTYPE html>
<html>
<head><meta name="viewport" content="width=device-width, initial-scale=1"><title>Inscription</title>
<style>
body{font-family:sans-serif;background:linear-gradient(135deg,#667eea,#764ba2);display:flex;align-items:center;justify-content:center;min-height:100vh}
.register{background:white;padding:40px;border-radius:20px;width:300px}
input{width:100%;padding:10px;margin:10px 0;border-radius:8px;border:1px solid #ddd}
button{width:100%;padding:10px;background:#2e7d32;color:white;border:none;border-radius:8px;cursor:pointer}
.error{color:red}.success{color:green}
</style>
</head>
<body>
<div class=register>
<h2>📝 Inscription</h2>
{% if error %}<div class=error>{{ error }}</div>{% endif %}
{% if success %}<div class=success>{{ success }}</div>{% endif %}
<form method=POST>
<input type=text name=username placeholder="Nom d'utilisateur" required>
<input type=password name=password placeholder="Mot de passe" required>
<input type=password name=confirm placeholder="Confirmer" required>
<button type=submit>S'inscrire</button>
</form>
<p><a href=/login>Déjà inscrit ? Se connecter</a></p>
</div>
</body>
</html>
"""

HTML_SEARCH = """
<!DOCTYPE html>
<html>
<head><meta name="viewport" content="width=device-width, initial-scale=1"><title>Recherche</title>
<style>
body{font-family:sans-serif;background:#f4f4f4;padding:20px}
.card{background:white;border-radius:15px;padding:20px;margin-bottom:20px}
input,button{padding:10px;margin:5px;border-radius:8px}
table{width:100%;border-collapse:collapse}
th,td{padding:10px;text-align:left;border-bottom:1px solid #ddd}
</style>
</head>
<body>
<div class=card>
<h2>🔍 Recherche de produits</h2>
<form method=GET>
<input type=text name=keyword placeholder="Nom du produit" value="{{ keyword }}">
<input type=number name=min_price placeholder="Prix min" value="{{ min_price }}">
<input type=number name=max_price placeholder="Prix max" value="{{ max_price }}">
<button type=submit>Rechercher</button>
<a href="/"><button type=button>Retour</button></a>
</form>
</div>
{% if results %}
<div class=card>
<h3>Résultats ({{ results|length }})</h3>
<table>
<tr><th>Produit</th><th>Prix</th><th>Session</th><th>Date</th></tr>
{% for r in results %}
<tr><td>{{ r.name }}</td><td>{{ "%.0f"|format(r.price) }} FCFA</td><td>{{ r.session_id }}</td><td>{{ r.timestamp }}</td></tr>
{% endfor %}
</table>
</div>
{% endif %}
</body>
</html>
"""

HTML_COMPARE = """
<!DOCTYPE html>
<html>
<head><meta name="viewport" content="width=device-width, initial-scale=1"><title>Comparaison</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
body{font-family:sans-serif;background:#f4f4f4;padding:20px}
.card{background:white;border-radius:15px;padding:20px;margin-bottom:20px}
select,button{padding:10px;margin:5px;border-radius:8px}
canvas{max-width:100%}
</style>
</head>
<body>
<div class=card>
<h2>📊 Comparer deux sessions</h2>
<form method=POST action="/compare_sessions">
<select name="session1" required>
<option value="">Session 1</option>
{% for h in history %}
<option value="{{ h.session_id }}">{{ h.session_id }} - {{ h.timestamp[:10] }}</option>
{% endfor %}
</select>
<select name="session2" required>
<option value="">Session 2</option>
{% for h in history %}
<option value="{{ h.session_id }}">{{ h.session_id }} - {{ h.timestamp[:10] }}</option>
{% endfor %}
</select>
<button type=submit>Comparer</button>
<a href="/"><button type=button>Retour</button></a>
</form>
</div>
{% if comparison %}
<div class=card>
<h3>Comparaison: {{ session1 }} vs {{ session2 }}</h3>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">
<div style="background:#e8f5e9;padding:20px;border-radius:10px">
<h4>{{ session1 }}</h4>
<p>Articles: {{ comparison[0].count }}</p>
<p>Total: {{ "%.0f"|format(comparison[0].total) }} FCFA</p>
<p>Moyenne: {{ "%.0f"|format(comparison[0].mean) }} FCFA</p>
</div>
<div style="background:#fff3e0;padding:20px;border-radius:10px">
<h4>{{ session2 }}</h4>
<p>Articles: {{ comparison[1].count }}</p>
<p>Total: {{ "%.0f"|format(comparison[1].total) }} FCFA</p>
<p>Moyenne: {{ "%.0f"|format(comparison[1].mean) }} FCFA</p>
</div>
</div>
<canvas id="compareChart" style="margin-top:20px"></canvas>
</div>
<script>
new Chart(document.getElementById('compareChart'), {
    type: 'bar',
    data: {
        labels: ['{{ session1 }}', '{{ session2 }}'],
        datasets: [{
            label: 'Prix moyen (FCFA)',
            data: [{{ comparison[0].mean }}, {{ comparison[1].mean }}],
            backgroundColor: ['#2e7d32', '#ff9800']
        }]
    }
});
</script>
{% endif %}
</body>
</html>
"""

# Modifier la route home pour inclure les nouvelles fonctionnalités
@app.route('/')
def home_enhanced():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    
    if request.method == 'POST' and 'p' in request.form:
        with open(FILE, "a") as f:
            f.write(f"{session.get('current_session', 'default')}|{datetime.now()}|{request.form['p']}|{request.form['v']}|{username}\n")
    
    info = "<i>Aucune donnée enregistrée.</i>"
    session_products = []
    
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 4 and parts[4] == username and parts[0] == session.get('current_session', ''):
                    session_products.append({'name': parts[2], 'price': float(parts[3])})
    
    if session_products:
        prix = [p['price'] for p in session_products]
        moyenne = sum(prix) / len(prix)
        variance = sum((x - moyenne) ** 2 for x in prix) / len(prix)
        info = f"""
        <b>Articles :</b> {len(prix)}<br>
        <b>Moyenne :</b> {moyenne:.0f} FCFA<br>
        <b>Max :</b> {max(prix):.0f} FCFA<br>
        <b>Variance :</b> {variance:.2f}
        """
    
    history = load_history_from_file(username)
    alerts = get_alerts(username)
    
    # Ajouter les liens vers les nouvelles pages
    extra_links = """
    <div style="margin-top:15px; display:flex; gap:10px; flex-wrap:wrap;">
        <a href="/search_view" style="background:#2196f3; color:white; padding:8px 15px; border-radius:8px; text-decoration:none;">🔍 Rechercher</a>
        <a href="/compare_view" style="background:#ff9800; color:white; padding:8px 15px; border-radius:8px; text-decoration:none;">📊 Comparer sessions</a>
        <a href="/logout" style="background:#f44336; color:white; padding:8px 15px; border-radius:8px; text-decoration:none;">🚪 Déconnexion</a>
    </div>
    """
    
    return render_template_string(HTML.replace('</body>', extra_links + '</body>'), info=info)

# Initialiser les utilisateurs
init_users()

print("✅ Nouvelles fonctionnalités ajoutées !")
print("📝 Comptes par défaut : admin/admin123 | demo/demo")
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
