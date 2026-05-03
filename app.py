from flask import Flask, render_template_string, request, session, redirect, url_for
import os
import math
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'eco_prix_key_2024'
FILE = "donnees.csv"

CATEGORIES = [
    {"id": "alimentaire",  "label": "Denrees alimentaires",     "emoji": "🍎", "color": "#22c55e"},
    {"id": "construction", "label": "Materiaux construction",   "emoji": "🧱", "color": "#f59e0b"},
    {"id": "hygiene",      "label": "Hygiene et beaute",        "emoji": "🧴", "color": "#3b82f6"},
    {"id": "electronique", "label": "Electronique",             "emoji": "📱", "color": "#8b5cf6"},
    {"id": "habillement",  "label": "Habillement textile",      "emoji": "👗", "color": "#ec4899"},
    {"id": "agriculture",  "label": "Agriculture jardinage",    "emoji": "🌾", "color": "#84cc16"},
    {"id": "sante",        "label": "Sante pharmacie",          "emoji": "💊", "color": "#ef4444"},
    {"id": "education",    "label": "Education fournitures",    "emoji": "📚", "color": "#06b6d4"},
    {"id": "transport",    "label": "Transport carburant",      "emoji": "🚗", "color": "#f97316"},
    {"id": "autre",        "label": "Autre",                    "emoji": "📦", "color": "#6b7280"},
]
CAT_MAP = {c["id"]: c for c in CATEGORIES}

# ============ TEMPLATE HTML PRINCIPAL ============
HTML = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <title>Eco-Prix Yaoundé – Gestion des Sessions</title>
    <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
    <style>
        :root {
            --primary:   #0f4c2a;
            --accent:    #22c55e;
            --accent2:   #f59e0b;
            --accent3:   #3b82f6;
            --danger:    #ef4444;
            --surface:   #ffffff;
            --surface2:  #f0fdf4;
            --text:      #111827;
            --muted:     #6b7280;
            --border:    rgba(34,197,94,0.18);
            --shadow:    0 8px 32px rgba(15,76,42,0.10);
            --radius:    20px;
        }

        *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'DM Sans', sans-serif;
            background: #0b1f14;
            min-height: 100vh;
            color: var(--text);
        }

        /* ===== SIDEBAR NAV ===== */
        .sidebar {
            position: fixed;
            left: 0; top: 0;
            width: 240px; height: 100vh;
            background: linear-gradient(180deg, #0f4c2a 0%, #0a3320 100%);
            display: flex;
            flex-direction: column;
            padding: 30px 20px;
            z-index: 100;
            box-shadow: 4px 0 24px rgba(0,0,0,0.3);
        }

        .sidebar-logo {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 40px;
        }

        .sidebar-logo .logo-icon {
            width: 46px; height: 46px;
            background: var(--accent);
            border-radius: 14px;
            display: flex; align-items: center; justify-content: center;
            font-size: 22px;
            flex-shrink: 0;
        }

        .sidebar-logo h2 {
            font-family: 'Syne', sans-serif;
            font-size: 1.1rem;
            color: white;
            font-weight: 700;
            line-height: 1.2;
        }

        .sidebar-logo span {
            font-size: 0.72rem;
            color: rgba(255,255,255,0.5);
            font-weight: 400;
        }

        .nav-label {
            font-size: 0.68rem;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: rgba(255,255,255,0.3);
            margin-bottom: 10px;
            padding-left: 12px;
        }

        .nav-links { list-style: none; margin-bottom: 30px; }

        .nav-links a {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 16px;
            border-radius: 12px;
            color: rgba(255,255,255,0.65);
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: 500;
            transition: all 0.2s;
            margin-bottom: 4px;
        }

        .nav-links a:hover,
        .nav-links a.active {
            background: rgba(34,197,94,0.18);
            color: var(--accent);
        }

        .nav-links a i { width: 18px; text-align: center; }

        .session-pill {
            margin-top: auto;
            background: rgba(34,197,94,0.12);
            border: 1px solid rgba(34,197,94,0.25);
            border-radius: 14px;
            padding: 16px;
            color: white;
        }

        .session-pill .s-label { font-size: 0.72rem; color: rgba(255,255,255,0.5); margin-bottom: 4px; }
        .session-pill .s-id { font-family: 'Syne', sans-serif; font-size: 1rem; font-weight: 700; color: var(--accent); }
        .session-pill .s-count { font-size: 0.8rem; color: rgba(255,255,255,0.6); margin-top: 4px; }

        /* ===== MAIN CONTENT ===== */
        .main {
            margin-left: 240px;
            min-height: 100vh;
            background: #f7faf8;
        }

        /* ===== PAGE SECTIONS (tab-based) ===== */
        .page { display: none; }
        .page.active { display: block; }

        /* ===== HERO DASHBOARD ===== */
        .hero-banner {
            background: linear-gradient(135deg, #0f4c2a 0%, #166534 60%, #16a34a 100%);
            padding: 48px 40px 40px;
            position: relative;
            overflow: hidden;
        }

        .hero-banner::after {
            content: '🛒';
            position: absolute;
            font-size: 180px;
            opacity: 0.07;
            right: 40px;
            bottom: -20px;
            transform: rotate(-10deg);
        }

        .hero-banner h1 {
            font-family: 'Syne', sans-serif;
            font-size: 2.4rem;
            font-weight: 800;
            color: white;
            margin-bottom: 8px;
        }

        .hero-banner p {
            color: rgba(255,255,255,0.7);
            font-size: 1rem;
            margin-bottom: 28px;
        }

        .hero-kpis {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
            gap: 16px;
        }

        .kpi-box {
            background: rgba(255,255,255,0.12);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 16px;
            padding: 20px;
            color: white;
            transition: transform 0.2s;
        }

        .kpi-box:hover { transform: translateY(-3px); }

        .kpi-box .kpi-icon { font-size: 24px; margin-bottom: 10px; }
        .kpi-box .kpi-val {
            font-family: 'Syne', sans-serif;
            font-size: 1.7rem;
            font-weight: 800;
        }
        .kpi-box .kpi-lbl { font-size: 0.78rem; opacity: 0.7; margin-top: 2px; }

        /* ===== CONTENT AREA ===== */
        .content-area { padding: 32px 40px; }

        /* ===== CARDS ===== */
        .card {
            background: var(--surface);
            border-radius: var(--radius);
            padding: 28px;
            margin-bottom: 24px;
            box-shadow: var(--shadow);
            border: 1px solid rgba(0,0,0,0.04);
            animation: fadeUp 0.4s ease both;
        }

        @keyframes fadeUp {
            from { opacity: 0; transform: translateY(18px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        .card-title {
            font-family: 'Syne', sans-serif;
            font-size: 1.15rem;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .card-title i { color: var(--accent); }

        /* ===== CHARTS GRID ===== */
        .charts-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        .chart-box {
            background: var(--surface);
            border-radius: var(--radius);
            padding: 24px;
            box-shadow: var(--shadow);
            border: 1px solid rgba(0,0,0,0.04);
        }

        .chart-box h3 {
            font-family: 'Syne', sans-serif;
            font-size: 0.95rem;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 16px;
            display: flex; align-items: center; gap: 8px;
        }

        /* ===== STATS GRID ===== */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 14px;
        }

        .stat-card {
            background: var(--surface2);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 18px;
            text-align: center;
            transition: all 0.25s;
        }

        .stat-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(34,197,94,0.15);
        }

        .stat-icon { font-size: 28px; color: var(--accent); margin-bottom: 8px; }
        .stat-val  { font-family: 'Syne', sans-serif; font-size: 1.5rem; font-weight: 800; color: var(--primary); }
        .stat-lbl  { font-size: 0.72rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px; }

        /* ===== FORM ===== */
        .form-row { display: flex; gap: 12px; flex-wrap: wrap; }
        .form-row input { flex: 1; min-width: 150px; }

        input, select {
            width: 100%;
            padding: 13px 16px;
            border: 2px solid #e5e7eb;
            border-radius: 12px;
            font-size: 14px;
            font-family: 'DM Sans', sans-serif;
            transition: all 0.2s;
            background: white;
            color: var(--text);
        }

        input:focus, select:focus {
            outline: none;
            border-color: var(--accent);
            box-shadow: 0 0 0 3px rgba(34,197,94,0.12);
        }

        /* ===== BUTTONS ===== */
        .btn {
            padding: 12px 22px;
            border: none;
            border-radius: 12px;
            font-size: 14px;
            font-weight: 600;
            font-family: 'DM Sans', sans-serif;
            cursor: pointer;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            text-decoration: none;
            white-space: nowrap;
        }

        .btn-primary { background: linear-gradient(135deg, #16a34a, #15803d); color: white; box-shadow: 0 4px 14px rgba(22,163,74,0.3); }
        .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(22,163,74,0.4); }

        .btn-amber  { background: linear-gradient(135deg, #f59e0b, #d97706); color: white; }
        .btn-danger { background: linear-gradient(135deg, #ef4444, #dc2626); color: white; }
        .btn-outline { background: transparent; border: 2px solid var(--accent); color: var(--accent); }
        .btn-outline:hover { background: var(--accent); color: white; }

        .btn-sm { padding: 7px 14px; font-size: 13px; border-radius: 10px; }

        .btn-group { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 14px; }

        /* ===== TABLE ===== */
        .table-wrap { overflow-x: auto; border-radius: 14px; border: 1px solid #e5e7eb; }

        table { width: 100%; border-collapse: collapse; }

        th {
            background: var(--surface2);
            padding: 13px 16px;
            text-align: left;
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--primary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        td { padding: 12px 16px; border-bottom: 1px solid #f3f4f6; font-size: 0.9rem; }

        tr:last-child td { border-bottom: none; }
        tr:hover td { background: #f9fafb; }

        /* ===== EMPTY STATE ===== */
        .empty-state { text-align: center; padding: 48px 20px; color: var(--muted); }
        .empty-state i { font-size: 52px; opacity: 0.3; display: block; margin-bottom: 12px; }

        /* ===== TREND BADGE ===== */
        .trend-box {
            background: linear-gradient(135deg, #eff6ff, #dbeafe);
            border: 1px solid #bfdbfe;
            border-radius: 14px;
            padding: 18px 20px;
            margin-top: 18px;
        }

        .trend-box h4 { font-family: 'Syne', sans-serif; font-size: 0.95rem; margin-bottom: 12px; color: #1d4ed8; }

        /* ===== UML DIAGRAM ===== */
        .uml-container {
            overflow-x: auto;
            padding: 10px 0;
        }

        .uml-diagram {
            display: flex;
            gap: 30px;
            align-items: flex-start;
            justify-content: center;
            flex-wrap: wrap;
            min-width: 700px;
        }

        .uml-class {
            border: 2px solid var(--primary);
            border-radius: 10px;
            overflow: hidden;
            min-width: 200px;
            font-size: 0.85rem;
            box-shadow: 0 4px 16px rgba(15,76,42,0.12);
        }

        .uml-header {
            background: var(--primary);
            color: white;
            padding: 10px 16px;
            font-family: 'Syne', sans-serif;
            font-weight: 700;
            text-align: center;
            font-size: 0.95rem;
        }

        .uml-section {
            padding: 10px 16px;
            border-bottom: 1px solid #d1fae5;
            background: white;
        }

        .uml-section:last-child { border-bottom: none; }

        .uml-section-title {
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--accent);
            font-weight: 700;
            margin-bottom: 6px;
        }

        .uml-item {
            padding: 3px 0;
            color: var(--text);
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .uml-item .vis { color: var(--accent); font-weight: 700; font-size: 0.8rem; }
        .uml-item .type { color: var(--accent3); font-size: 0.78rem; }

        .uml-arrow {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 4px;
            padding-top: 60px;
            color: var(--muted);
            font-size: 0.75rem;
            text-align: center;
        }

        .uml-arrow .line {
            width: 2px;
            height: 60px;
            background: repeating-linear-gradient(to bottom, var(--accent) 0, var(--accent) 5px, transparent 5px, transparent 10px);
        }

        /* ===== ALERT ===== */
        .alert { border-radius: 12px; padding: 12px 18px; margin-bottom: 18px; font-size: 0.9rem; }
        .alert-success { background: #dcfce7; color: #166534; border-left: 4px solid var(--accent); }
        .alert-info    { background: #eff6ff; color: #1d4ed8; border-left: 4px solid var(--accent3); }

        /* ===== RESPONSIVE ===== */
        @media (max-width: 900px) {
            .sidebar { display: none; }
            .main { margin-left: 0; }
            .charts-grid { grid-template-columns: 1fr; }
            .content-area { padding: 20px; }
            .hero-banner { padding: 28px 20px; }
            .hero-banner h1 { font-size: 1.6rem; }

            .mobile-nav {
                display: flex !important;
                position: fixed;
                bottom: 0; left: 0; right: 0;
                background: var(--primary);
                z-index: 200;
                justify-content: space-around;
                padding: 10px 0;
            }
        }

        .mobile-nav { display: none; }

        .mobile-nav a {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
            color: rgba(255,255,255,0.6);
            text-decoration: none;
            font-size: 0.68rem;
            padding: 6px 12px;
        }

        .mobile-nav a.active, .mobile-nav a:hover { color: var(--accent); }
        .mobile-nav a i { font-size: 20px; }
    </style>
</head>
<body>

<!-- ====== SIDEBAR ====== -->
<nav class="sidebar">
    <div class="sidebar-logo">
        <div class="logo-icon">🛒</div>
        <div>
            <h2>Eco-Prix<br><span>Yaoundé</span></h2>
        </div>
    </div>

    <div class="nav-label">Navigation</div>
    <ul class="nav-links">
        <li><a href="#" onclick="showPage('dashboard')" id="nav-dashboard" class="active"><i class="fas fa-th-large"></i> Tableau de bord</a></li>
        <li><a href="#" onclick="showPage('session')" id="nav-session"><i class="fas fa-shopping-cart"></i> Session active</a></li>
        <li><a href="#" onclick="showPage('stats')" id="nav-stats"><i class="fas fa-chart-line"></i> Statistiques</a></li>
        <li><a href="#" onclick="showPage('history')" id="nav-history"><i class="fas fa-history"></i> Historique</a></li>
        <li><a href="#" onclick="showPage('popular')" id="nav-popular"><i class="fas fa-fire"></i> Produits populaires</a></li>
        <li><a href="#" onclick="showPage('categories')" id="nav-categories"><i class="fas fa-tags"></i> Par catégorie</a></li>
        <li><a href="#" onclick="showPage('about')" id="nav-about"><i class="fas fa-info-circle"></i> À propos / UML</a></li>
    </ul>

    <div class="session-pill">
        <div class="s-label">Session active</div>
        <div class="s-id">{{ session_id }}</div>
        <div class="s-count"><i class="fas fa-boxes"></i> {{ session_count }} produit(s)</div>
    </div>
</nav>

<!-- ====== MOBILE NAV ====== -->
<nav class="mobile-nav">
    <a href="#" onclick="showPage('dashboard')" id="mnav-dashboard" class="active"><i class="fas fa-th-large"></i> Accueil</a>
    <a href="#" onclick="showPage('session')" id="mnav-session"><i class="fas fa-cart-plus"></i> Session</a>
    <a href="#" onclick="showPage('stats')" id="mnav-stats"><i class="fas fa-chart-bar"></i> Stats</a>
    <a href="#" onclick="showPage('history')" id="mnav-history"><i class="fas fa-history"></i> Historique</a>
    <a href="#" onclick="showPage('popular')" id="mnav-popular"><i class="fas fa-fire"></i> Populaires</a>
    <a href="#" onclick="showPage('categories')" id="mnav-categories"><i class="fas fa-tags"></i> Catégories</a>
    <a href="#" onclick="showPage('about')" id="mnav-about"><i class="fas fa-sitemap"></i> UML</a>
</nav>

<!-- ====== MAIN ====== -->
<div class="main">

    <!-- ============ PAGE: DASHBOARD ============ -->
    <div id="page-dashboard" class="page active">
        <div class="hero-banner">
            <h1><i class="fas fa-store"></i> Eco-Prix Yaoundé</h1>
            <p>Tableau de bord intelligent – analyse statistique en temps réel</p>
            <div class="hero-kpis">
                <div class="kpi-box">
                    <div class="kpi-icon">🛍️</div>
                    <div class="kpi-val">{{ session_count }}</div>
                    <div class="kpi-lbl">Produits session</div>
                </div>
                {% if session_stats %}
                <div class="kpi-box">
                    <div class="kpi-icon">💰</div>
                    <div class="kpi-val">{{ "%.0f"|format(session_stats.sum) }}</div>
                    <div class="kpi-lbl">Total FCFA</div>
                </div>
                <div class="kpi-box">
                    <div class="kpi-icon">📊</div>
                    <div class="kpi-val">{{ "%.0f"|format(session_stats.mean) }}</div>
                    <div class="kpi-lbl">Prix moyen</div>
                </div>
                <div class="kpi-box">
                    <div class="kpi-icon">📉</div>
                    <div class="kpi-val">{{ "%.0f"|format(session_stats.min) }}</div>
                    <div class="kpi-lbl">Prix min</div>
                </div>
                <div class="kpi-box">
                    <div class="kpi-icon">📈</div>
                    <div class="kpi-val">{{ "%.0f"|format(session_stats.max) }}</div>
                    <div class="kpi-lbl">Prix max</div>
                </div>
                {% else %}
                <div class="kpi-box">
                    <div class="kpi-icon">💡</div>
                    <div class="kpi-val">–</div>
                    <div class="kpi-lbl">Ajoutez des produits</div>
                </div>
                {% endif %}
                <div class="kpi-box">
                    <div class="kpi-icon">📁</div>
                    <div class="kpi-val">{{ history|length }}</div>
                    <div class="kpi-lbl">Sessions archivées</div>
                </div>
            </div>
        </div>

        <div class="content-area">
            {% if session_products %}
            <div class="charts-grid">
                <!-- Graphique barres -->
                <div class="chart-box">
                    <h3><i class="fas fa-chart-bar" style="color:var(--accent)"></i> Prix par produit</h3>
                    <canvas id="barChart" height="220"></canvas>
                </div>
                <!-- Graphique camembert -->
                <div class="chart-box">
                    <h3><i class="fas fa-chart-pie" style="color:var(--accent2)"></i> Répartition des dépenses</h3>
                    <canvas id="pieChart" height="220"></canvas>
                </div>
                <!-- Courbe d'évolution -->
                <div class="chart-box" style="grid-column: 1 / -1;">
                    <h3><i class="fas fa-chart-line" style="color:var(--accent3)"></i> Évolution des prix (ordre d'entrée)</h3>
                    <canvas id="lineChart" height="140"></canvas>
                </div>
            </div>
            {% else %}
            <div class="card">
                <div class="empty-state">
                    <i class="fas fa-chart-area"></i>
                    <p style="font-size:1.05rem; margin-bottom:8px;">Aucun produit enregistré</p>
                    <p style="font-size:0.85rem;">Rendez-vous dans <strong>Session active</strong> pour ajouter des produits et voir les graphiques ici.</p>
                    <button class="btn btn-primary" style="margin-top:18px;" onclick="showPage('session')">
                        <i class="fas fa-plus"></i> Ajouter un produit
                    </button>
                </div>
            </div>
            {% endif %}

            {% if history %}
            <div class="card">
                <div class="card-title"><i class="fas fa-history"></i> Résumé des sessions archivées</div>
                <div class="chart-box" style="box-shadow:none; border:none; padding:0;">
                    <canvas id="historyChart" height="120"></canvas>
                </div>
            </div>
            {% endif %}
        </div>
    </div>

    <!-- ============ PAGE: SESSION ============ -->
    <div id="page-session" class="page">
        <div class="hero-banner">
            <h1><i class="fas fa-shopping-cart"></i> Session active</h1>
            <p>Ajoutez et gérez les produits de votre session courante</p>
        </div>
        <div class="content-area">
            <!-- Formulaire ajout -->
            <div class="card">
                <div class="card-title"><i class="fas fa-plus-circle"></i> Ajouter un produit</div>
                <form method="POST" action="{{ url_for('add_product') }}">
                    <div class="form-row" style="margin-bottom:12px;">
                        <input type="text" name="product" placeholder="🏷️ Nom du produit" required>
                        <input type="number" name="price" placeholder="💰 Prix (FCFA)" step="any" required>
                    </div>
                    <div class="form-row">
                        <select name="category" required style="flex:2;">
                            <option value="" disabled selected>📂 Choisir une catégorie</option>
                            {% for cat in categories %}
                            <option value="{{ cat.id }}">{{ cat.emoji }} {{ cat.label }}</option>
                            {% endfor %}
                        </select>
                        <button type="submit" class="btn btn-primary" style="flex:1;">
                            <i class="fas fa-save"></i> Enregistrer
                        </button>
                    </div>
                </form>
                <div class="btn-group">
                    <form method="POST" action="{{ url_for('new_session') }}">
                        <button type="submit" class="btn btn-amber">
                            <i class="fas fa-plus"></i> Nouvelle session
                        </button>
                    </form>
                    <form method="POST" action="{{ url_for('end_session') }}" onsubmit="return confirm('Terminer cette session ? Les données seront sauvegardées.')">
                        <button type="submit" class="btn btn-danger">
                            <i class="fas fa-flag-checkered"></i> Terminer la session
                        </button>
                    </form>
                </div>
            </div>

            <!-- Liste produits -->
            <div class="card">
                <div class="card-title"><i class="fas fa-list-ul"></i> Produits enregistrés</div>
                {% if session_products %}
                <div class="table-wrap">
                    <table>
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Produit</th>
                                <th>Catégorie</th>
                                <th>Prix (FCFA)</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for p in session_products %}
                            <tr>
                                <td>{{ loop.index }}</td>
                                <td><strong>{{ p.name }}</strong></td>
                                <td>
                                    {% set cat = cat_map.get(p.get('category','autre'), cat_map['autre']) %}
                                    <span style="background:{{ cat.color }}22; color:{{ cat.color }}; border:1px solid {{ cat.color }}55; padding:3px 10px; border-radius:20px; font-size:0.8rem; font-weight:600; white-space:nowrap;">
                                        {{ cat.emoji }} {{ cat.label }}
                                    </span>
                                </td>
                                <td style="color: #16a34a; font-weight: 600;">{{ "%.0f"|format(p.price) }} FCFA</td>
                                <td>
                                    <form method="POST" action="{{ url_for('remove_product') }}" style="display:inline;">
                                        <input type="hidden" name="index" value="{{ loop.index0 }}">
                                        <button type="submit" class="btn btn-sm btn-danger">
                                            <i class="fas fa-trash"></i> Supprimer
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
                    <p style="font-size:0.82rem; margin-top:6px;">Ajoutez votre premier produit ci-dessus ✨</p>
                </div>
                {% endif %}
            </div>
        </div>
    </div>

    <!-- ============ PAGE: STATISTIQUES ============ -->
    <div id="page-stats" class="page">
        <div class="hero-banner">
            <h1><i class="fas fa-chart-line"></i> Analyse statistique</h1>
            <p>Statistiques descriptives et régression linéaire de la session courante</p>
        </div>
        <div class="content-area">
            {% if session_stats %}
            <div class="card">
                <div class="card-title"><i class="fas fa-calculator"></i> Statistiques descriptives</div>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-icon"><i class="fas fa-cubes"></i></div>
                        <div class="stat-val">{{ session_stats.count }}</div>
                        <div class="stat-lbl">Articles</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon"><i class="fas fa-coins"></i></div>
                        <div class="stat-val">{{ "%.0f"|format(session_stats.sum) }}</div>
                        <div class="stat-lbl">Total (FCFA)</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon"><i class="fas fa-chart-simple"></i></div>
                        <div class="stat-val">{{ "%.0f"|format(session_stats.mean) }}</div>
                        <div class="stat-lbl">Moyenne</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon"><i class="fas fa-chart-bar"></i></div>
                        <div class="stat-val">{{ "%.2f"|format(session_stats.variance) }}</div>
                        <div class="stat-lbl">Variance</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon"><i class="fas fa-arrow-down"></i></div>
                        <div class="stat-val">{{ "%.0f"|format(session_stats.min) }}</div>
                        <div class="stat-lbl">Minimum</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon"><i class="fas fa-arrow-up"></i></div>
                        <div class="stat-val">{{ "%.0f"|format(session_stats.max) }}</div>
                        <div class="stat-lbl">Maximum</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon"><i class="fas fa-chart-pie"></i></div>
                        <div class="stat-val">{{ "%.0f"|format(session_stats.median) }}</div>
                        <div class="stat-lbl">Médiane</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon"><i class="fas fa-wave-square"></i></div>
                        <div class="stat-val">{{ "%.2f"|format(session_stats.std_dev) }}</div>
                        <div class="stat-lbl">Écart-type</div>
                    </div>
                </div>

                {% if session_stats.trend %}
                <div class="trend-box">
                    <h4><i class="fas fa-chart-line"></i> Régression linéaire (évolution des prix)</h4>
                    <div class="stats-grid" style="grid-template-columns: repeat(3, 1fr);">
                        <div class="stat-card" style="background:#eff6ff;">
                            <div class="stat-lbl">Direction</div>
                            <div class="stat-val" style="font-size:1.3rem;">
                                {% if session_stats.trend.slope > 0 %}📈 Hausse
                                {% elif session_stats.trend.slope < 0 %}📉 Baisse
                                {% else %}➡️ Stable
                                {% endif %}
                            </div>
                        </div>
                        <div class="stat-card" style="background:#eff6ff;">
                            <div class="stat-lbl">Pente</div>
                            <div class="stat-val" style="font-size:1.3rem;">{{ "%.2f"|format(session_stats.trend.slope) }}</div>
                        </div>
                        <div class="stat-card" style="background:#eff6ff;">
                            <div class="stat-lbl">R² (corrélation)</div>
                            <div class="stat-val" style="font-size:1.3rem;">{{ "%.3f"|format(session_stats.trend.r2) }}</div>
                        </div>
                    </div>
                </div>
                {% endif %}
            </div>

            <!-- Graphiques stats avancés -->
            <div class="charts-grid">
                <div class="chart-box">
                    <h3><i class="fas fa-chart-bar" style="color:var(--accent)"></i> Comparaison des prix</h3>
                    <canvas id="statsBarChart" height="240"></canvas>
                </div>
                <div class="chart-box">
                    <h3><i class="fas fa-chart-area" style="color:var(--accent3)"></i> Distribution des prix</h3>
                    <canvas id="statsLineChart" height="240"></canvas>
                </div>
            </div>

            {% else %}
            <div class="card">
                <div class="empty-state">
                    <i class="fas fa-chart-line"></i>
                    <p>Ajoutez des produits pour voir les statistiques</p>
                </div>
            </div>
            {% endif %}
        </div>
    </div>

    <!-- ============ PAGE: HISTORIQUE ============ -->
    <div id="page-history" class="page">
        <div class="hero-banner">
            <h1><i class="fas fa-history"></i> Historique des sessions</h1>
            <p>Consultez et rechargez vos anciennes sessions d'achats</p>
        </div>
        <div class="content-area">
            <div class="card">
                <div class="card-title"><i class="fas fa-archive"></i> Sessions archivées</div>
                {% if history %}
                <div class="table-wrap">
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
                                <td><strong style="color:var(--primary);">{{ h.session_id }}</strong></td>
                                <td style="color:var(--muted);">{{ h.timestamp }}</td>
                                <td>{{ h.count }}</td>
                                <td style="color:#16a34a; font-weight:600;">{{ "%.0f"|format(h.total) }} FCFA</td>
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
                    <p style="font-size:0.82rem; margin-top:6px;">Terminez une session pour l'archiver automatiquement</p>
                </div>
                {% endif %}
            </div>
        </div>
    </div>

    <!-- ============ PAGE: À PROPOS / UML ============ -->
    <div id="page-about" class="page">
        <div class="hero-banner">
            <h1><i class="fas fa-sitemap"></i> À propos & Diagramme de classes</h1>
            <p>Architecture du système Eco-Prix Yaoundé – TP INF232</p>
        </div>
        <div class="content-area">

            <!-- Description projet -->
            <div class="card">
                <div class="card-title"><i class="fas fa-info-circle"></i> Description du projet</div>
                <p style="color:var(--muted); line-height:1.7; margin-bottom: 16px;">
                    <strong>Eco-Prix Yaoundé</strong> est une application web Flask de gestion intelligente des sessions d'achats.
                    Elle permet d'enregistrer des produits et leurs prix, de calculer des statistiques descriptives avancées
                    (moyenne, variance, médiane, régression linéaire) et de visualiser les données graphiquement.
                </p>
                <div style="display:flex; gap:12px; flex-wrap:wrap;">
                    <span style="background:#dcfce7; color:#166534; padding:6px 14px; border-radius:20px; font-size:0.82rem; font-weight:600;"><i class="fab fa-python"></i> Python 3</span>
                    <span style="background:#dbeafe; color:#1d4ed8; padding:6px 14px; border-radius:20px; font-size:0.82rem; font-weight:600;"><i class="fas fa-flask"></i> Flask</span>
                    <span style="background:#fef3c7; color:#92400e; padding:6px 14px; border-radius:20px; font-size:0.82rem; font-weight:600;"><i class="fas fa-chart-bar"></i> Chart.js</span>
                    <span style="background:#ede9fe; color:#5b21b6; padding:6px 14px; border-radius:20px; font-size:0.82rem; font-weight:600;"><i class="fas fa-database"></i> CSV</span>
                </div>
            </div>

            <!-- Diagramme de classes UML -->
            <div class="card">
                <div class="card-title"><i class="fas fa-diagram-project"></i> Diagramme de classes UML</div>
                <div class="uml-container">
                    <div class="uml-diagram">

                        <!-- Classe Application -->
                        <div class="uml-class">
                            <div class="uml-header">🌐 Application (Flask)</div>
                            <div class="uml-section">
                                <div class="uml-section-title">Attributs</div>
                                <div class="uml-item"><span class="vis">+</span> secret_key <span class="type">: str</span></div>
                                <div class="uml-item"><span class="vis">+</span> FILE <span class="type">: str</span></div>
                            </div>
                            <div class="uml-section">
                                <div class="uml-section-title">Routes (méthodes)</div>
                                <div class="uml-item"><span class="vis">+</span> home() <span class="type">: Response</span></div>
                                <div class="uml-item"><span class="vis">+</span> add_product() <span class="type">: Response</span></div>
                                <div class="uml-item"><span class="vis">+</span> remove_product() <span class="type">: Response</span></div>
                                <div class="uml-item"><span class="vis">+</span> new_session() <span class="type">: Response</span></div>
                                <div class="uml-item"><span class="vis">+</span> end_session() <span class="type">: Response</span></div>
                                <div class="uml-item"><span class="vis">+</span> load_session() <span class="type">: Response</span></div>
                            </div>
                        </div>

                        <!-- Flèche -->
                        <div class="uml-arrow">
                            <div class="line"></div>
                            <span>utilise</span>
                            <i class="fas fa-arrow-right"></i>
                        </div>

                        <!-- Classe Session -->
                        <div class="uml-class">
                            <div class="uml-header">📦 Session</div>
                            <div class="uml-section">
                                <div class="uml-section-title">Attributs</div>
                                <div class="uml-item"><span class="vis">+</span> session_id <span class="type">: str</span></div>
                                <div class="uml-item"><span class="vis">+</span> products <span class="type">: list[Produit]</span></div>
                                <div class="uml-item"><span class="vis">+</span> counter <span class="type">: int</span></div>
                                <div class="uml-item"><span class="vis">+</span> timestamp <span class="type">: datetime</span></div>
                            </div>
                            <div class="uml-section">
                                <div class="uml-section-title">Méthodes</div>
                                <div class="uml-item"><span class="vis">+</span> add(p: Produit) <span class="type">: void</span></div>
                                <div class="uml-item"><span class="vis">+</span> remove(i: int) <span class="type">: void</span></div>
                                <div class="uml-item"><span class="vis">+</span> get_prices() <span class="type">: list[float]</span></div>
                                <div class="uml-item"><span class="vis">+</span> save() <span class="type">: void</span></div>
                            </div>
                        </div>

                        <!-- Flèche -->
                        <div class="uml-arrow">
                            <div class="line"></div>
                            <span>contient</span>
                            <i class="fas fa-arrow-right"></i>
                        </div>

                        <!-- Classe Produit -->
                        <div class="uml-class">
                            <div class="uml-header">🏷️ Produit</div>
                            <div class="uml-section">
                                <div class="uml-section-title">Attributs</div>
                                <div class="uml-item"><span class="vis">+</span> name <span class="type">: str</span></div>
                                <div class="uml-item"><span class="vis">+</span> price <span class="type">: float</span></div>
                            </div>
                            <div class="uml-section">
                                <div class="uml-section-title">Méthodes</div>
                                <div class="uml-item"><span class="vis">+</span> to_dict() <span class="type">: dict</span></div>
                                <div class="uml-item"><span class="vis">+</span> __str__() <span class="type">: str</span></div>
                            </div>
                        </div>

                    </div>

                    <!-- Deuxième rang -->
                    <div class="uml-diagram" style="margin-top: 30px;">

                        <!-- Classe Statistiques -->
                        <div class="uml-class">
                            <div class="uml-header">📊 Statistiques</div>
                            <div class="uml-section">
                                <div class="uml-section-title">Attributs</div>
                                <div class="uml-item"><span class="vis">+</span> values <span class="type">: list[float]</span></div>
                            </div>
                            <div class="uml-section">
                                <div class="uml-section-title">Méthodes</div>
                                <div class="uml-item"><span class="vis">+</span> calculate_variance() <span class="type">: float</span></div>
                                <div class="uml-item"><span class="vis">+</span> calculate_median() <span class="type">: float</span></div>
                                <div class="uml-item"><span class="vis">+</span> linear_regression() <span class="type">: dict</span></div>
                                <div class="uml-item"><span class="vis">+</span> std_dev() <span class="type">: float</span></div>
                                <div class="uml-item"><span class="vis">+</span> summary() <span class="type">: dict</span></div>
                            </div>
                        </div>

                        <div class="uml-arrow">
                            <div class="line"></div>
                            <span>calcule</span>
                            <i class="fas fa-arrow-right"></i>
                        </div>

                        <!-- Classe Fichier CSV -->
                        <div class="uml-class">
                            <div class="uml-header">💾 FichierCSV</div>
                            <div class="uml-section">
                                <div class="uml-section-title">Attributs</div>
                                <div class="uml-item"><span class="vis">-</span> path <span class="type">: str</span></div>
                                <div class="uml-item"><span class="vis">-</span> separator <span class="type">: str = '|'</span></div>
                            </div>
                            <div class="uml-section">
                                <div class="uml-section-title">Méthodes</div>
                                <div class="uml-item"><span class="vis">+</span> save_session() <span class="type">: void</span></div>
                                <div class="uml-item"><span class="vis">+</span> load_history() <span class="type">: list</span></div>
                                <div class="uml-item"><span class="vis">+</span> exists() <span class="type">: bool</span></div>
                            </div>
                        </div>

                        <div class="uml-arrow">
                            <div class="line"></div>
                            <span>fournit données</span>
                            <i class="fas fa-arrow-right"></i>
                        </div>

                        <!-- Classe Historique -->
                        <div class="uml-class">
                            <div class="uml-header">📋 Historique</div>
                            <div class="uml-section">
                                <div class="uml-section-title">Attributs</div>
                                <div class="uml-item"><span class="vis">+</span> sessions <span class="type">: list[Session]</span></div>
                            </div>
                            <div class="uml-section">
                                <div class="uml-section-title">Méthodes</div>
                                <div class="uml-item"><span class="vis">+</span> get_all() <span class="type">: list</span></div>
                                <div class="uml-item"><span class="vis">+</span> get_by_id() <span class="type">: Session</span></div>
                                <div class="uml-item"><span class="vis">+</span> sort_by_date() <span class="type">: list</span></div>
                            </div>
                        </div>

                    </div>
                </div>

                <!-- Légende UML -->
                <div style="display:flex; gap:20px; flex-wrap:wrap; margin-top:20px; padding-top:16px; border-top:1px solid #e5e7eb;">
                    <span style="font-size:0.8rem; color:var(--muted);"><span style="color:var(--accent); font-weight:700;">+</span> Public</span>
                    <span style="font-size:0.8rem; color:var(--muted);"><span style="color:var(--danger); font-weight:700;">-</span> Privé</span>
                    <span style="font-size:0.8rem; color:var(--muted);"><span style="color:var(--accent3); font-weight:700;">#</span> Protégé</span>
                    <span style="font-size:0.8rem; color:var(--muted);">- - → Association / Dépendance</span>
                    <span style="font-size:0.8rem; color:var(--muted);">──→ Composition / Agrégation</span>
                </div>
            </div>

            <!-- Membres -->
            <div class="card">
                <div class="card-title"><i class="fas fa-users"></i> Membres du groupe</div>
                <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:16px;">
                    <div style="background:var(--surface2); border-radius:14px; padding:18px; text-align:center; border:1px solid var(--border);">
                        <div style="font-size:2rem; margin-bottom:8px;">👤</div>
                        <div style="font-family:'Syne',sans-serif; font-weight:700; color:var(--primary);">Membre 1</div>
                        <div style="font-size:0.8rem; color:var(--muted); margin-top:4px;">Matricule : —</div>
                    </div>
                    <div style="background:var(--surface2); border-radius:14px; padding:18px; text-align:center; border:1px solid var(--border);">
                        <div style="font-size:2rem; margin-bottom:8px;">👤</div>
                        <div style="font-family:'Syne',sans-serif; font-weight:700; color:var(--primary);">Membre 2</div>
                        <div style="font-size:0.8rem; color:var(--muted); margin-top:4px;">Matricule : —</div>
                    </div>
                    <div style="background:var(--surface2); border-radius:14px; padding:18px; text-align:center; border:1px solid var(--border);">
                        <div style="font-size:2rem; margin-bottom:8px;">👤</div>
                        <div style="font-family:'Syne',sans-serif; font-weight:700; color:var(--primary);">Membre 3</div>
                        <div style="font-size:0.8rem; color:var(--muted); margin-top:4px;">Matricule : —</div>
                    </div>
                </div>
                <div style="margin-top:16px; padding-top:16px; border-top:1px solid #e5e7eb; font-size:0.85rem; color:var(--muted);">
                    <i class="fas fa-university"></i> Cours : INF232 – Année académique 2024/2025
                </div>
            </div>

        </div>
    </div>

    <!-- ============ PAGE: PRODUITS POPULAIRES ============ -->
    <div id="page-popular" class="page">
        <div class="hero-banner">
            <h1><i class="fas fa-fire"></i> Produits populaires</h1>
            <p>Classement des produits par fréquence d'achat et montant total dépensé (toutes sessions)</p>
        </div>
        <div class="content-area">
            {% if popular_products %}

            <!-- KPIs populaires -->
            <div class="hero-kpis" style="margin-bottom:24px;">
                <div class="kpi-box" style="background:rgba(245,158,11,0.15); border:1px solid rgba(245,158,11,0.3);">
                    <div class="kpi-icon">🏆</div>
                    <div class="kpi-val" style="color:#92400e;">{{ popular_products[0].name[:12] }}</div>
                    <div class="kpi-lbl">Produit n°1</div>
                </div>
                <div class="kpi-box" style="background:rgba(34,197,94,0.15); border:1px solid rgba(34,197,94,0.3);">
                    <div class="kpi-icon">🔢</div>
                    <div class="kpi-val" style="color:#166534;">{{ popular_products[0].count }}</div>
                    <div class="kpi-lbl">Fois acheté (top)</div>
                </div>
                <div class="kpi-box" style="background:rgba(59,130,246,0.15); border:1px solid rgba(59,130,246,0.3);">
                    <div class="kpi-icon">💰</div>
                    <div class="kpi-val" style="color:#1d4ed8;">{{ "%.0f"|format(popular_products[0].total) }}</div>
                    <div class="kpi-lbl">FCFA dépensé (top)</div>
                </div>
                <div class="kpi-box" style="background:rgba(139,92,246,0.15); border:1px solid rgba(139,92,246,0.3);">
                    <div class="kpi-icon">📦</div>
                    <div class="kpi-val" style="color:#5b21b6;">{{ popular_products|length }}</div>
                    <div class="kpi-lbl">Produits distincts</div>
                </div>
            </div>

            <!-- Deux camemberts côte à côte -->
            <div class="charts-grid">
                <div class="chart-box">
                    <h3><i class="fas fa-chart-pie" style="color:var(--accent2)"></i> Parts de marché – Fréquence d'achat</h3>
                    <canvas id="popFreqPie" height="260"></canvas>
                </div>
                <div class="chart-box">
                    <h3><i class="fas fa-chart-pie" style="color:var(--accent3)"></i> Parts de marché – Montant total dépensé</h3>
                    <canvas id="popTotalPie" height="260"></canvas>
                </div>
            </div>

            <!-- Tableau classement -->
            <div class="card" style="margin-top:24px;">
                <div class="card-title"><i class="fas fa-trophy"></i> Classement combiné des produits</div>
                <div class="table-wrap">
                    <table>
                        <thead>
                            <tr>
                                <th>Rang</th>
                                <th>Produit</th>
                                <th>Fois acheté</th>
                                <th>Prix moyen (FCFA)</th>
                                <th>Total dépensé (FCFA)</th>
                                <th>Score popularité</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for p in popular_products %}
                            <tr>
                                <td>
                                    {% if loop.index == 1 %}🥇
                                    {% elif loop.index == 2 %}🥈
                                    {% elif loop.index == 3 %}🥉
                                    {% else %}#{{ loop.index }}
                                    {% endif %}
                                </td>
                                <td><strong>{{ p.name }}</strong></td>
                                <td>
                                    <span style="background:#dcfce7; color:#166534; padding:3px 10px; border-radius:20px; font-size:0.82rem; font-weight:600;">
                                        {{ p.count }}×
                                    </span>
                                </td>
                                <td>{{ "%.0f"|format(p.avg) }} FCFA</td>
                                <td style="color:#16a34a; font-weight:600;">{{ "%.0f"|format(p.total) }} FCFA</td>
                                <td>
                                    <div style="display:flex; align-items:center; gap:8px;">
                                        <div style="flex:1; background:#e5e7eb; border-radius:8px; height:8px; overflow:hidden;">
                                            <div style="width:{{ p.score_pct }}%; background:linear-gradient(90deg,#22c55e,#16a34a); height:100%; border-radius:8px;"></div>
                                        </div>
                                        <span style="font-size:0.8rem; color:var(--muted); min-width:36px;">{{ "%.0f"|format(p.score_pct) }}%</span>
                                    </div>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>

            {% else %}
            <div class="card">
                <div class="empty-state">
                    <i class="fas fa-fire"></i>
                    <p style="font-size:1.05rem; margin-bottom:8px;">Aucune donnée disponible</p>
                    <p style="font-size:0.85rem;">Terminez au moins une session pour voir les produits populaires sur l'ensemble de l'historique.</p>
                    <button class="btn btn-primary" style="margin-top:18px;" onclick="showPage('session')">
                        <i class="fas fa-cart-plus"></i> Aller à la session active
                    </button>
                </div>
            </div>
            {% endif %}
        </div>
    </div>

    <!-- ============ PAGE: PAR CATÉGORIE ============ -->
    <div id="page-categories" class="page">
        <div class="hero-banner">
            <h1><i class="fas fa-tags"></i> Produits par catégorie</h1>
            <p>Visualisation et analyse des dépenses regroupées par catégorie</p>
        </div>
        <div class="content-area">
            {% if cat_stats %}

            <!-- KPIs catégories -->
            <div class="hero-kpis" style="margin-bottom:24px;">
                <div class="kpi-box" style="background:rgba(34,197,94,0.15); border:1px solid rgba(34,197,94,0.3);">
                    <div class="kpi-icon">🗂️</div>
                    <div class="kpi-val" style="color:#166534;">{{ cat_stats|length }}</div>
                    <div class="kpi-lbl">Catégories utilisées</div>
                </div>
                {% set top_cat = cat_stats[0] %}
                <div class="kpi-box" style="background:rgba(245,158,11,0.15); border:1px solid rgba(245,158,11,0.3);">
                    <div class="kpi-icon">{{ top_cat.emoji }}</div>
                    <div class="kpi-val" style="color:#92400e; font-size:1.1rem;">{{ top_cat.label[:14] }}</div>
                    <div class="kpi-lbl">Catégorie dominante</div>
                </div>
                <div class="kpi-box" style="background:rgba(59,130,246,0.15); border:1px solid rgba(59,130,246,0.3);">
                    <div class="kpi-icon">💰</div>
                    <div class="kpi-val" style="color:#1d4ed8;">{{ "%.0f"|format(top_cat.total) }}</div>
                    <div class="kpi-lbl">FCFA (top catégorie)</div>
                </div>
                <div class="kpi-box" style="background:rgba(139,92,246,0.15); border:1px solid rgba(139,92,246,0.3);">
                    <div class="kpi-icon">🛍️</div>
                    <div class="kpi-val" style="color:#5b21b6;">{{ cat_stats | sum(attribute='count') }}</div>
                    <div class="kpi-lbl">Produits total (historique)</div>
                </div>
            </div>

            <!-- Camembert + Barres côte à côte -->
            <div class="charts-grid">
                <div class="chart-box">
                    <h3><i class="fas fa-chart-pie" style="color:var(--accent2)"></i> Répartition par catégorie (montant)</h3>
                    <canvas id="catPieChart" height="280"></canvas>
                </div>
                <div class="chart-box">
                    <h3><i class="fas fa-chart-bar" style="color:var(--accent3)"></i> Nombre d'articles par catégorie</h3>
                    <canvas id="catBarChart" height="280"></canvas>
                </div>
            </div>

            <!-- Cartes catégories détaillées -->
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px,1fr)); gap:16px; margin-top:24px;">
                {% for cs in cat_stats %}
                <div style="background:white; border-radius:18px; padding:20px; box-shadow:var(--shadow); border-left:5px solid {{ cs.color }};">
                    <div style="display:flex; align-items:center; gap:12px; margin-bottom:14px;">
                        <div style="font-size:2rem;">{{ cs.emoji }}</div>
                        <div>
                            <div style="font-family:'Syne',sans-serif; font-weight:700; font-size:0.95rem; color:var(--primary);">{{ cs.label }}</div>
                            <div style="font-size:0.78rem; color:var(--muted);">{{ cs.count }} article(s)</div>
                        </div>
                        <div style="margin-left:auto; font-family:'Syne',sans-serif; font-weight:800; font-size:1.1rem; color:{{ cs.color }};">
                            {{ "%.0f"|format(cs.total) }} F
                        </div>
                    </div>
                    <!-- Barre de progression -->
                    <div style="background:#f3f4f6; border-radius:8px; height:8px; margin-bottom:10px; overflow:hidden;">
                        <div style="width:{{ cs.pct_total }}%; background:{{ cs.color }}; height:100%; border-radius:8px; transition:width 0.6s ease;"></div>
                    </div>
                    <div style="display:flex; justify-content:space-between; font-size:0.78rem; color:var(--muted);">
                        <span>Moy. : <strong style="color:var(--text);">{{ "%.0f"|format(cs.avg) }} FCFA</strong></span>
                        <span>Min : <strong>{{ "%.0f"|format(cs.min) }}</strong> | Max : <strong>{{ "%.0f"|format(cs.max) }}</strong></span>
                    </div>
                    <!-- Liste des produits de cette catégorie -->
                    <details style="margin-top:12px;">
                        <summary style="cursor:pointer; font-size:0.82rem; color:{{ cs.color }}; font-weight:600;">
                            Voir les produits ({{ cs.products|length }})
                        </summary>
                        <ul style="list-style:none; margin-top:8px;">
                            {% for prod in cs.products[:8] %}
                            <li style="display:flex; justify-content:space-between; padding:4px 0; border-bottom:1px solid #f3f4f6; font-size:0.82rem;">
                                <span>{{ prod.name }}</span>
                                <span style="font-weight:600; color:{{ cs.color }};">{{ "%.0f"|format(prod.price) }} F</span>
                            </li>
                            {% endfor %}
                            {% if cs.products|length > 8 %}
                            <li style="font-size:0.78rem; color:var(--muted); padding-top:4px;">… et {{ cs.products|length - 8 }} autre(s)</li>
                            {% endif %}
                        </ul>
                    </details>
                </div>
                {% endfor %}
            </div>

            <!-- Tableau récapitulatif -->
            <div class="card" style="margin-top:24px;">
                <div class="card-title"><i class="fas fa-table"></i> Tableau récapitulatif par catégorie</div>
                <div class="table-wrap">
                    <table>
                        <thead>
                            <tr>
                                <th>Catégorie</th>
                                <th>Articles</th>
                                <th>Total (FCFA)</th>
                                <th>Moyenne</th>
                                <th>Min</th>
                                <th>Max</th>
                                <th>Part du budget</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for cs in cat_stats %}
                            <tr>
                                <td>
                                    <span style="display:flex; align-items:center; gap:8px;">
                                        <span style="width:12px; height:12px; border-radius:50%; background:{{ cs.color }}; display:inline-block; flex-shrink:0;"></span>
                                        {{ cs.emoji }} {{ cs.label }}
                                    </span>
                                </td>
                                <td>{{ cs.count }}</td>
                                <td style="font-weight:600; color:#16a34a;">{{ "%.0f"|format(cs.total) }} FCFA</td>
                                <td>{{ "%.0f"|format(cs.avg) }}</td>
                                <td>{{ "%.0f"|format(cs.min) }}</td>
                                <td>{{ "%.0f"|format(cs.max) }}</td>
                                <td>
                                    <div style="display:flex; align-items:center; gap:8px;">
                                        <div style="flex:1; background:#e5e7eb; border-radius:6px; height:7px; overflow:hidden;">
                                            <div style="width:{{ cs.pct_total }}%; background:{{ cs.color }}; height:100%; border-radius:6px;"></div>
                                        </div>
                                        <span style="font-size:0.8rem; min-width:36px;">{{ "%.1f"|format(cs.pct_total) }}%</span>
                                    </div>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>

            {% else %}
            <div class="card">
                <div class="empty-state">
                    <i class="fas fa-tags"></i>
                    <p style="font-size:1.05rem; margin-bottom:8px;">Aucune donnée par catégorie</p>
                    <p style="font-size:0.85rem;">Ajoutez des produits avec une catégorie dans la session active, puis terminez la session pour voir les statistiques ici.</p>
                    <button class="btn btn-primary" style="margin-top:18px;" onclick="showPage('session')">
                        <i class="fas fa-cart-plus"></i> Aller à la session active
                    </button>
                </div>
            </div>
            {% endif %}
        </div>
    </div>

</div><!-- /.main -->

<!-- ====== SCRIPTS ====== -->
<script>
// ---- Navigation entre pages ----
function showPage(name) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.nav-links a, .mobile-nav a').forEach(a => a.classList.remove('active'));
    document.getElementById('page-' + name).classList.add('active');
    const navEl = document.getElementById('nav-' + name);
    const mnavEl = document.getElementById('mnav-' + name);
    if (navEl)  navEl.classList.add('active');
    if (mnavEl) mnavEl.classList.add('active');
    return false;
}

// ---- Données produits depuis Flask ----
const products = {{ session_products | tojson }};
const labels   = products.map(p => p.name);
const prices   = products.map(p => p.price);

const PALETTE = [
    '#22c55e','#3b82f6','#f59e0b','#ef4444','#8b5cf6',
    '#06b6d4','#ec4899','#84cc16','#f97316','#14b8a6'
];

// ---- Bar Chart ----
if (products.length > 0 && document.getElementById('barChart')) {
    new Chart(document.getElementById('barChart'), {
        type: 'bar',
        data: {
            labels,
            datasets: [{
                label: 'Prix (FCFA)',
                data: prices,
                backgroundColor: labels.map((_, i) => PALETTE[i % PALETTE.length] + 'cc'),
                borderColor:     labels.map((_, i) => PALETTE[i % PALETTE.length]),
                borderWidth: 2,
                borderRadius: 8,
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true, grid: { color: '#f0f0f0' } }, x: { grid: { display: false } } }
        }
    });
}

// ---- Pie Chart ----
if (products.length > 0 && document.getElementById('pieChart')) {
    new Chart(document.getElementById('pieChart'), {
        type: 'doughnut',
        data: {
            labels,
            datasets: [{
                data: prices,
                backgroundColor: labels.map((_, i) => PALETTE[i % PALETTE.length] + 'cc'),
                borderColor: '#fff',
                borderWidth: 3,
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'right', labels: { boxWidth: 14, font: { size: 12 } } }
            }
        }
    });
}

// ---- Line Chart (évolution) ----
if (products.length > 0 && document.getElementById('lineChart')) {
    new Chart(document.getElementById('lineChart'), {
        type: 'line',
        data: {
            labels,
            datasets: [{
                label: 'Prix (FCFA)',
                data: prices,
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59,130,246,0.08)',
                tension: 0.4,
                fill: true,
                pointBackgroundColor: '#3b82f6',
                pointRadius: 5,
                pointHoverRadius: 8,
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: false, grid: { color: '#f0f0f0' } }, x: { grid: { display: false } } }
        }
    });
}

// ---- Stats Bar Chart (page stats) ----
if (products.length > 0 && document.getElementById('statsBarChart')) {
    new Chart(document.getElementById('statsBarChart'), {
        type: 'bar',
        data: {
            labels,
            datasets: [{
                label: 'Prix (FCFA)',
                data: prices,
                backgroundColor: labels.map((_, i) => PALETTE[i % PALETTE.length] + 'bb'),
                borderColor:     labels.map((_, i) => PALETTE[i % PALETTE.length]),
                borderWidth: 2,
                borderRadius: 8,
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true } }
        }
    });
}

// ---- Stats Line Chart ----
if (products.length > 0 && document.getElementById('statsLineChart')) {
    new Chart(document.getElementById('statsLineChart'), {
        type: 'line',
        data: {
            labels,
            datasets: [{
                label: 'Prix',
                data: prices,
                borderColor: '#22c55e',
                backgroundColor: 'rgba(34,197,94,0.1)',
                tension: 0.4,
                fill: true,
                pointBackgroundColor: '#22c55e',
                pointRadius: 5,
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: false } }
        }
    });
}

// ---- History Chart (totaux par session) ----
const history = {{ history | tojson }};
if (history.length > 0 && document.getElementById('historyChart')) {
    const hLabels = history.map(h => h.session_id);
    const hTotals = history.map(h => h.total);
    new Chart(document.getElementById('historyChart'), {
        type: 'bar',
        data: {
            labels: hLabels,
            datasets: [{
                label: 'Total FCFA',
                data: hTotals,
                backgroundColor: hLabels.map((_, i) => PALETTE[i % PALETTE.length] + 'cc'),
                borderColor:     hLabels.map((_, i) => PALETTE[i % PALETTE.length]),
                borderWidth: 2,
                borderRadius: 8,
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true }, x: { grid: { display: false } } }
        }
    });
}

// ---- Popular Products Pie Charts ----
const popularProducts = {{ popular_products | tojson }};

if (popularProducts.length > 0 && document.getElementById('popFreqPie')) {
    const popLabels = popularProducts.map(p => p.name);
    const popCounts = popularProducts.map(p => p.count);
    new Chart(document.getElementById('popFreqPie'), {
        type: 'doughnut',
        data: {
            labels: popLabels,
            datasets: [{
                data: popCounts,
                backgroundColor: popLabels.map((_, i) => PALETTE[i % PALETTE.length] + 'cc'),
                borderColor: '#fff',
                borderWidth: 3,
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'bottom', labels: { boxWidth: 14, font: { size: 12 }, padding: 16 } },
                tooltip: {
                    callbacks: {
                        label: ctx => ` ${ctx.label} : ${ctx.parsed} achat(s) (${((ctx.parsed / popCounts.reduce((a,b)=>a+b,0))*100).toFixed(1)}%)`
                    }
                }
            }
        }
    });
}

if (popularProducts.length > 0 && document.getElementById('popTotalPie')) {
    const popLabels = popularProducts.map(p => p.name);
    const popTotals = popularProducts.map(p => p.total);
    new Chart(document.getElementById('popTotalPie'), {
        type: 'doughnut',
        data: {
            labels: popLabels,
            datasets: [{
                data: popTotals,
                backgroundColor: popLabels.map((_, i) => PALETTE[i % PALETTE.length] + 'aa'),
                borderColor: '#fff',
                borderWidth: 3,
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'bottom', labels: { boxWidth: 14, font: { size: 12 }, padding: 16 } },
                tooltip: {
                    callbacks: {
                        label: ctx => ` ${ctx.label} : ${ctx.parsed.toFixed(0)} FCFA (${((ctx.parsed / popTotals.reduce((a,b)=>a+b,0))*100).toFixed(1)}%)`
                    }
                }
            }
        }
    });
}
// ---- Category Charts ----
const catStats = {{ cat_stats | tojson }};

if (catStats.length > 0 && document.getElementById('catPieChart')) {
    const catLabels = catStats.map(c => c.emoji + ' ' + c.label);
    const catTotals = catStats.map(c => c.total);
    const catColors = catStats.map(c => c.color + 'cc');
    new Chart(document.getElementById('catPieChart'), {
        type: 'doughnut',
        data: {
            labels: catLabels,
            datasets: [{
                data: catTotals,
                backgroundColor: catColors,
                borderColor: '#fff',
                borderWidth: 3,
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'bottom', labels: { boxWidth: 14, font: { size: 11 }, padding: 12 } },
                tooltip: {
                    callbacks: {
                        label: ctx => ` ${ctx.label} : ${ctx.parsed.toFixed(0)} FCFA (${((ctx.parsed / catTotals.reduce((a,b)=>a+b,0))*100).toFixed(1)}%)`
                    }
                }
            }
        }
    });
}

if (catStats.length > 0 && document.getElementById('catBarChart')) {
    const catLabels2 = catStats.map(c => c.emoji + ' ' + c.label);
    const catCounts  = catStats.map(c => c.count);
    const catColors2 = catStats.map(c => c.color + 'cc');
    new Chart(document.getElementById('catBarChart'), {
        type: 'bar',
        data: {
            labels: catLabels2,
            datasets: [{
                label: "Nombre d'articles",
                data: catCounts,
                backgroundColor: catColors2,
                borderColor: catStats.map(c => c.color),
                borderWidth: 2,
                borderRadius: 8,
            }]
        },
        options: {
            responsive: true,
            indexAxis: 'y',
            plugins: { legend: { display: false } },
            scales: {
                x: { beginAtZero: true, grid: { color: '#f0f0f0' } },
                y: { grid: { display: false }, ticks: { font: { size: 11 } } }
            }
        }
    });
}
</script>
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
    numerator   = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    denominator = sum((x[i] - mean_x) ** 2 for i in range(n))
    if denominator == 0:
        return None
    slope     = numerator / denominator
    intercept = mean_y - slope * mean_x
    ss_res = sum((y[i] - (slope * x[i] + intercept)) ** 2 for i in range(n))
    ss_tot = sum((y[i] - mean_y) ** 2 for i in range(n))
    r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
    return {'slope': slope, 'r2': r2}

# ============ PRODUITS POPULAIRES ============
def get_popular_products():
    prod_map = {}
    if os.path.exists(FILE):
        with open(FILE, "r", encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) >= 4:
                        name, price = parts[2], float(parts[3])
                        name_key = name.strip().lower()
                        if name_key not in prod_map:
                            prod_map[name_key] = {'name': name.strip(), 'count': 0, 'total': 0.0}
                        prod_map[name_key]['count'] += 1
                        prod_map[name_key]['total'] += price
    if not prod_map:
        return []
    products = list(prod_map.values())
    for p in products:
        p['avg'] = p['total'] / p['count']
    max_count = max(p['count'] for p in products)
    max_total = max(p['total'] for p in products)
    for p in products:
        p['score']     = (p['count']/max_count * 0.5 + p['total']/max_total * 0.5)
        p['score_pct'] = p['score'] * 100
    products.sort(key=lambda x: x['score'], reverse=True)
    return products


def get_cat_stats():
    """Agrège les dépenses par catégorie sur toutes les sessions archivées."""
    cat_map_data = {}
    if os.path.exists(FILE):
        with open(FILE, "r", encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) >= 4:
                        name  = parts[2]
                        price = float(parts[3])
                        cat_id = parts[4].strip() if len(parts) >= 5 else 'autre'
                        if cat_id not in CAT_MAP:
                            cat_id = 'autre'
                        if cat_id not in cat_map_data:
                            cat_map_data[cat_id] = {'products': [], 'prices': []}
                        cat_map_data[cat_id]['products'].append({'name': name, 'price': price})
                        cat_map_data[cat_id]['prices'].append(price)

    if not cat_map_data:
        return []

    grand_total = sum(sum(v['prices']) for v in cat_map_data.values())
    result = []
    for cat_id, data in cat_map_data.items():
        prices = data['prices']
        total  = sum(prices)
        info   = CAT_MAP.get(cat_id, CAT_MAP['autre'])
        result.append({
            'id':       cat_id,
            'label':    info['label'],
            'emoji':    info['emoji'],
            'color':    info['color'],
            'count':    len(prices),
            'total':    total,
            'avg':      total / len(prices),
            'min':      min(prices),
            'max':      max(prices),
            'pct_total': (total / grand_total * 100) if grand_total else 0,
            'products': data['products'],
        })
    result.sort(key=lambda x: x['total'], reverse=True)
    return result


def save_session_to_file(session_id, products, timestamp):
    with open(FILE, "a", encoding='utf-8') as f:
        for p in products:
            cat = p.get('category', 'autre')
            f.write(f"{session_id}|{timestamp}|{p['name']}|{p['price']}|{cat}\n")

def load_history_from_file():
    history = []
    sessions_data = {}
    if os.path.exists(FILE):
        with open(FILE, "r", encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) >= 4:
                        session_id, timestamp, name, price = parts[0], parts[1], parts[2], parts[3]
                        category = parts[4] if len(parts) >= 5 else 'autre'
                        price = float(price)
                        if session_id not in sessions_data:
                            sessions_data[session_id] = {'timestamp': timestamp, 'products': [], 'prices': []}
                        sessions_data[session_id]['products'].append({'name': name, 'price': price, 'category': category})
                        sessions_data[session_id]['prices'].append(price)
    for session_id, data in sessions_data.items():
        prices = data['prices']
        history.append({
            'session_id':  session_id,
            'timestamp':   data['timestamp'],
            'count':       len(prices),
            'total':       sum(prices),
            'mean':        sum(prices) / len(prices) if prices else 0,
            'products':    data['products']
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

    session_id       = session['current_session']
    session_products = session.get('session_products', [])
    session_stats    = None

    if session_products:
        prices = [p['price'] for p in session_products]
        stats  = {
            'count':   len(prices),
            'sum':     sum(prices),
            'mean':    sum(prices) / len(prices),
            'variance': calculate_variance(prices),
            'min':     min(prices),
            'max':     max(prices),
            'median':  calculate_median(prices),
            'std_dev': math.sqrt(calculate_variance(prices))
        }
        if len(prices) >= 2:
            stats['trend'] = linear_regression(prices)
        session_stats = stats

    history = load_history_from_file()
    popular_products = get_popular_products()
    cat_stats_data   = get_cat_stats()
    return render_template_string(HTML,
        session_id=session_id,
        session_count=len(session_products),
        session_products=session_products,
        session_stats=session_stats,
        history=history,
        popular_products=popular_products,
        categories=CATEGORIES,
        cat_map=CAT_MAP,
        cat_stats=cat_stats_data,
    )

@app.route('/add', methods=['POST'])
def add_product():
    product_name = request.form.get('product', '').strip()
    price        = request.form.get('price', '')
    category     = request.form.get('category', 'autre').strip()
    if category not in CAT_MAP:
        category = 'autre'
    if product_name and price:
        try:
            price = float(price)
            session.setdefault('session_products', []).append({
                'name': product_name, 'price': price, 'category': category
            })
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
        save_session_to_file(
            session['current_session'],
            session['session_products'],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    session['session_counter']  = session.get('session_counter', 1) + 1
    session['current_session']  = f'SESSION_{session["session_counter"]:03d}'
    session['session_products'] = []
    session.modified = True
    return home()

@app.route('/end_session', methods=['POST'])
def end_session():
    if session.get('session_products'):
        save_session_to_file(
            session['current_session'],
            session['session_products'],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    session['session_products'] = []
    session.modified = True
    return home()

@app.route('/load_session', methods=['POST'])
def load_session():
    session_id = request.form.get('session_id')
    for h in load_history_from_file():
        if h['session_id'] == session_id:
            session['current_session']  = session_id
            session['session_products'] = h['products']
            session.modified = True
            break
    return home()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
