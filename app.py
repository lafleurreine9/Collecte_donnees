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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
