from flask import Flask, request, jsonify
import sqlite3
import os
from datetime import datetime, timedelta

app = Flask(__name__)
DATABASE = '/tmp/grocery.db'

def init_db():
    if os.path.exists(DATABASE):
        return
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('CREATE TABLE supermarkets (id INTEGER PRIMARY KEY, nombre TEXT)')
    c.execute('CREATE TABLE productos (id INTEGER PRIMARY KEY, nombre TEXT UNIQUE, cantidad TEXT)')
    c.execute('CREATE TABLE precios (id INTEGER PRIMARY KEY, supermercado_id INTEGER, producto_id INTEGER, precio REAL, precio_promo REAL, promo_vence TEXT, fecha_scraping TEXT)')
    c.execute("INSERT INTO supermarkets VALUES (1, 'Coto')")
    c.execute("INSERT INTO supermarkets VALUES (2, 'Jumbo')")
    c.execute("INSERT INTO supermarkets VALUES (3, 'Disco')")
    productos = [
        (1,'Leche Entera','1L'),(2,'Yogur Natural','200g'),(3,'Naranjas','1kg'),
        (4,'Huevos','12 unidades'),(5,'Queso Cremoso','1kg'),(6,'Manteca','200g'),
        (7,'Pan Lactal','500g'),(8,'Arroz','1kg'),(9,'Fideos Secos','500g'),
        (10,'Aceite de Girasol','1.5L'),(11,'Azúcar','1kg'),(12,'Harina','1kg'),
        (13,'Galletitas Dulces','300g'),(14,'Gaseosa Cola','2.25L'),(15,'Agua Mineral','2L'),
        (16,'Papel Higiénico','4 rollos'),(17,'Detergente','750ml'),(18,'Jabón en Polvo','800g'),
        (19,'Pollo Entero','1kg'),(20,'Carne Picada','1kg'),(21,'Banana','1kg'),
        (22,'Tomate','1kg'),(23,'Papa','1kg'),(24,'Cebolla','1kg'),
    ]
    for p in productos:
        c.execute('INSERT INTO productos VALUES (?, ?, ?)', p)
    hoy = datetime.now().strftime('%Y-%m-%d')
    pv1 = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    pv2 = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
    precios = [
        (1,1,1,1250,1100,pv1,hoy),(2,2,1,1240,None,None,hoy),(3,3,1,1230,1150,pv2,hoy),
        (4,1,2,890,None,None,hoy),(5,2,2,850,790,pv1,hoy),(6,3,2,920,None,None,hoy),
        (7,1,3,1500,1350,pv1,hoy),(8,2,3,1420,None,None,hoy),(9,3,3,1380,None,None,hoy),
        (10,1,4,2300,None,None,hoy),(11,2,4,2190,1990,pv2,hoy),(12,3,4,2410,None,None,hoy),
        (13,1,5,4200,None,None,hoy),(14,2,5,4100,3800,pv1,hoy),(15,3,5,4350,None,None,hoy),
        (16,1,6,1800,None,None,hoy),(17,2,6,1750,None,None,hoy),(18,3,6,1900,1700,pv1,hoy),
        (19,1,7,1600,1400,pv1,hoy),(20,2,7,1550,None,None,hoy),(21,3,7,1580,None,None,hoy),
        (22,1,8,1100,None,None,hoy),(23,2,8,1050,950,pv2,hoy),(24,3,8,1150,None,None,hoy),
        (25,1,9,750,None,None,hoy),(26,2,9,720,None,None,hoy),(27,3,9,780,690,pv1,hoy),
        (28,1,10,2200,1990,pv1,hoy),(29,2,10,2150,None,None,hoy),(30,3,10,2300,None,None,hoy),
        (31,1,11,950,None,None,hoy),(32,2,11,920,None,None,hoy),(33,3,11,980,850,pv2,hoy),
        (34,1,12,650,None,None,hoy),(35,2,12,630,550,pv1,hoy),(36,3,12,680,None,None,hoy),
        (37,1,13,1200,None,None,hoy),(38,2,13,1150,None,None,hoy),(39,3,13,1250,1100,pv1,hoy),
        (40,1,14,1800,1600,pv2,hoy),(41,2,14,1750,None,None,hoy),(42,3,14,1850,None,None,hoy),
        (43,1,15,800,None,None,hoy),(44,2,15,780,None,None,hoy),(45,3,15,820,700,pv1,hoy),
        (46,1,16,1500,None,None,hoy),(47,2,16,1450,1300,pv1,hoy),(48,3,16,1550,None,None,hoy),
        (49,1,17,950,None,None,hoy),(50,2,17,920,None,None,hoy),(51,3,17,980,880,pv2,hoy),
        (52,1,18,2100,1900,pv1,hoy),(53,2,18,2050,None,None,hoy),(54,3,18,2200,None,None,hoy),
        (55,1,19,2800,None,None,hoy),(56,2,19,2700,2500,pv1,hoy),(57,3,19,2900,None,None,hoy),
        (58,1,20,4500,None,None,hoy),(59,2,20,4400,None,None,hoy),(60,3,20,4600,4200,pv2,hoy),
        (61,1,21,1200,1050,pv1,hoy),(62,2,21,1150,None,None,hoy),(63,3,21,1250,None,None,hoy),
        (64,1,22,1800,None,None,hoy),(65,2,22,1750,1600,pv1,hoy),(66,3,22,1850,None,None,hoy),
        (67,1,23,900,None,None,hoy),(68,2,23,850,None,None,hoy),(69,3,23,950,800,pv1,hoy),
        (70,1,24,800,700,pv2,hoy),(71,2,24,780,None,None,hoy),(72,3,24,820,None,None,hoy),
    ]
    for p in precios:
        c.execute('INSERT INTO precios VALUES (?, ?, ?, ?, ?, ?, ?)', p)
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GroceryFinder - Mejores precios en Buenos Aires</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Inter', sans-serif; background: #f0f4f8; min-height: 100vh; padding: 20px 16px; }
        .top-bar { max-width: 750px; margin: 0 auto 14px; display: flex; justify-content: space-between; align-items: center; padding: 0 4px; }
        .top-bar .logo { font-size: 20px; font-weight: 700; color: #0d9488; letter-spacing: -0.5px; }
        .top-bar .logo span { color: #334155; }
        .top-bar .right { display: flex; align-items: center; gap: 12px; }
        .top-bar .tagline { font-size: 11px; color: #94a3b8; font-weight: 500; }
        .lang-toggle { display: flex; border: 1.5px solid #e2e8f0; border-radius: 8px; overflow: hidden; }
        .lang-btn { padding: 4px 10px; font-size: 12px; font-weight: 600; cursor: pointer; border: none; background: white; color: #64748b; font-family: 'Inter', sans-serif; transition: all 0.2s; }
        .lang-btn.active { background: #0d9488; color: white; }
        .container { background: white; border-radius: 16px; padding: 28px; max-width: 750px; width: 100%; margin: 0 auto; box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 8px 30px rgba(0,0,0,0.04); border: 1px solid #e2e8f0; }
        .header { text-align: center; margin-bottom: 24px; }
        .header h1 { color: #1e293b; font-size: 26px; margin-bottom: 4px; font-weight: 700; letter-spacing: -0.5px; }
        .header p { color: #94a3b8; font-size: 14px; }
        .coupons-section { margin-bottom: 22px; }
        .coupons-scroll { display: flex; gap: 12px; overflow-x: auto; padding-bottom: 8px; scrollbar-width: thin; }
        .coupons-scroll::-webkit-scrollbar { height: 4px; }
        .coupons-scroll::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
        .coupon { min-width: 220px; border-radius: 12px; padding: 16px; position: relative; overflow: hidden; cursor: pointer; transition: transform 0.2s; flex-shrink: 0; }
        .coupon:hover { transform: translateY(-2px); }
        .coupon-coto { background: linear-gradient(135deg, #dc2626, #ef4444); color: white; }
        .coupon-jumbo { background: linear-gradient(135deg, #059669, #10b981); color: white; }
        .coupon-disco { background: linear-gradient(135deg, #7c3aed, #8b5cf6); color: white; }
        .coupon .discount { font-size: 28px; font-weight: 700; line-height: 1; }
        .coupon .coupon-desc { font-size: 12px; margin-top: 4px; opacity: 0.9; }
        .coupon .coupon-code { display: inline-block; background: rgba(255,255,255,0.25); padding: 3px 10px; border-radius: 6px; font-size: 11px; font-weight: 600; margin-top: 8px; letter-spacing: 1px; }
        .coupon .coupon-exp { font-size: 10px; opacity: 0.7; margin-top: 6px; }
        .coupon .store-name { font-size: 14px; font-weight: 600; margin-bottom: 6px; opacity: 0.9; }
        .coupon-circle { position: absolute; right: -15px; top: -15px; width: 70px; height: 70px; border-radius: 50%; background: rgba(255,255,255,0.1); }
        .coupon-circle2 { position: absolute; right: 20px; bottom: -20px; width: 50px; height: 50px; border-radius: 50%; background: rgba(255,255,255,0.08); }
        .coupon-copied { position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%); background: #1e293b; color: white; padding: 10px 20px; border-radius: 10px; font-size: 13px; font-weight: 600; z-index: 200; display: none; animation: fadeUp 0.3s ease-out; }
        @keyframes fadeUp { from { opacity: 0; transform: translateX(-50%) translateY(10px); } to { opacity: 1; transform: translateX(-50%) translateY(0); } }
        .search-box { position: relative; display: flex; gap: 10px; margin-bottom: 20px; }
        .search-box input { flex: 1; padding: 13px 16px; border: 1.5px solid #e2e8f0; border-radius: 10px; font-size: 15px; outline: none; transition: all 0.2s; background: #f8fafc; font-family: 'Inter', sans-serif; }
        .search-box input:focus { border-color: #0d9488; background: white; box-shadow: 0 0 0 3px rgba(13,148,136,0.1); }
        .search-box button { padding: 13px 24px; background: #0d9488; color: white; border: none; border-radius: 10px; cursor: pointer; font-weight: 600; font-size: 14px; transition: all 0.2s; font-family: 'Inter', sans-serif; }
        .search-box button:hover { background: #0f766e; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(13,148,136,0.25); }
        .autocomplete-list { position: absolute; top: 100%; left: 0; right: 80px; background: white; border: 1px solid #e2e8f0; border-top: none; border-radius: 0 0 10px 10px; max-height: 200px; overflow-y: auto; z-index: 10; display: none; box-shadow: 0 8px 20px rgba(0,0,0,0.08); }
        .autocomplete-item { padding: 10px 16px; cursor: pointer; font-size: 14px; border-bottom: 1px solid #f1f5f9; }
        .autocomplete-item:hover { background: #f0fdfa; }
        .autocomplete-item .cantidad { color: #94a3b8; font-size: 12px; margin-left: 5px; }
        .categories { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 22px; }
        .cat-btn { padding: 7px 16px; border: 1.5px solid #e2e8f0; border-radius: 25px; background: white; cursor: pointer; font-size: 13px; transition: all 0.2s; font-family: 'Inter', sans-serif; font-weight: 500; color: #64748b; }
        .cat-btn:hover { border-color: #0d9488; color: #0d9488; background: #f0fdfa; }
        .cat-btn.active { background: #0d9488; color: white; border-color: #0d9488; }
        .section-title { font-size: 13px; color: #94a3b8; margin-bottom: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }
        .results { margin-top: 10px; }
        .product { margin-bottom: 16px; padding: 18px; border-left: 4px solid #0d9488; background: #f8fafc; border-radius: 0 12px 12px 0; }
        .product h3 { color: #1e293b; margin-bottom: 3px; font-size: 17px; font-weight: 600; }
        .product .cantidad-label { color: #94a3b8; font-size: 13px; margin-bottom: 10px; }
        .price-item { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid #e2e8f0; cursor: pointer; transition: all 0.15s; }
        .price-item:last-child { border-bottom: none; }
        .price-item:hover { opacity: 0.8; }
        .supermarket { display: flex; align-items: center; gap: 6px; font-size: 14px; color: #475569; font-weight: 500; }
        .price-info { text-align: right; }
        .price { font-weight: 700; color: #0d9488; font-size: 16px; }
        .price-promo { font-size: 13px; }
        .price-original { text-decoration: line-through; color: #cbd5e1; margin-right: 8px; }
        .price-oferta { color: #dc2626; font-weight: 700; }
        .promo-vence { font-size: 11px; color: #dc2626; display: block; margin-top: 2px; }
        .cheapest { background: #f0fdfa; padding: 10px; border-radius: 8px; border: 1px solid #ccfbf1; }
        .cheapest .price { color: #059669; }
        .badge { background: #059669; color: white; padding: 3px 10px; border-radius: 20px; font-size: 10px; margin-left: 8px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.3px; }
        .badge-promo { background: #dc2626; color: white; padding: 3px 10px; border-radius: 20px; font-size: 10px; margin-left: 8px; font-weight: 600; text-transform: uppercase; }
        .popular-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(155px, 1fr)); gap: 12px; margin-bottom: 20px; }
        .popular-item { background: white; border-radius: 12px; padding: 16px 12px; text-align: center; cursor: pointer; transition: all 0.25s; border: 1.5px solid #e2e8f0; }
        .popular-item:hover { border-color: #0d9488; transform: translateY(-3px); box-shadow: 0 8px 20px rgba(13,148,136,0.1); }
        .popular-item .emoji { font-size: 32px; display: block; margin-bottom: 8px; }
        .popular-item .name { font-size: 13px; color: #1e293b; font-weight: 600; display: block; }
        .popular-item .qty { font-size: 11px; color: #94a3b8; display: block; margin-top: 2px; }
        .popular-item .desde { font-size: 13px; color: #0d9488; font-weight: 700; margin-top: 6px; display: block; }
        .no-results { text-align: center; padding: 40px; color: #94a3b8; }
        .no-results .emoji-big { font-size: 48px; display: block; margin-bottom: 10px; }
        .scrape-date { text-align: center; font-size: 11px; color: #94a3b8; margin-top: 15px; }
        .modal-overlay { display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(15,23,42,0.4); backdrop-filter: blur(4px); z-index: 100; justify-content: center; align-items: center; padding: 20px; }
        .modal-overlay.active { display: flex; }
        .modal { background: white; border-radius: 16px; padding: 28px; max-width: 420px; width: 100%; box-shadow: 0 20px 60px rgba(0,0,0,0.12); position: relative; animation: modalIn 0.25s ease-out; }
        @keyframes modalIn { from { transform: scale(0.95) translateY(10px); opacity: 0; } to { transform: scale(1) translateY(0); opacity: 1; } }
        .modal-close { position: absolute; top: 14px; right: 16px; background: #f1f5f9; border: none; font-size: 16px; cursor: pointer; color: #64748b; width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; transition: all 0.15s; }
        .modal-close:hover { background: #e2e8f0; color: #1e293b; }
        .modal h3 { font-size: 18px; color: #1e293b; margin-bottom: 5px; font-weight: 700; }
        .modal .modal-subtitle { font-size: 13px; color: #94a3b8; margin-bottom: 18px; }
        .modal-row { display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid #f1f5f9; font-size: 14px; }
        .modal-row:last-child { border-bottom: none; }
        .modal-label { color: #64748b; }
        .modal-value { color: #1e293b; font-weight: 600; }
        .modal-value.promo { color: #dc2626; }
        .modal-value.mejor { color: #059669; }
        .modal-source { margin-top: 18px; padding: 14px; background: #f8fafc; border-radius: 10px; font-size: 12px; color: #64748b; border: 1px solid #e2e8f0; line-height: 1.6; }
        .modal-source strong { color: #1e293b; display: block; margin-bottom: 4px; }
        @media (max-width: 500px) {
            .container { padding: 20px 15px; }
            .header h1 { font-size: 22px; }
            .popular-grid { grid-template-columns: repeat(3, 1fr); gap: 8px; }
            .popular-item { padding: 10px 6px; }
            .popular-item .emoji { font-size: 26px; }
            .coupon { min-width: 190px; }
        }
    </style>
</head>
<body>
    <div class="top-bar">
        <div class="logo"><span>Grocery</span>Finder</div>
        <div class="right">
            <div class="tagline">Buenos Aires, Argentina</div>
            <div class="lang-toggle">
                <button class="lang-btn active" id="btn-es" onclick="setLang('es')">ES</button>
                <button class="lang-btn" id="btn-en" onclick="setLang('en')">EN</button>
            </div>
        </div>
    </div>
    <div class="container">
        <div class="header">
            <h1 data-es="Compará precios al instante" data-en="Compare prices instantly" class="i18n"></h1>
            <p data-es="Encontrá el mejor precio entre Coto, Jumbo y Disco" data-en="Find the best price across Coto, Jumbo and Disco" class="i18n"></p>
        </div>

        <div class="coupons-section">
            <p class="section-title i18n" data-es="Cupones disponibles" data-en="Available coupons" id="coupons-title"></p>
            <div class="coupons-scroll" id="coupons-scroll"></div>
        </div>

        <div class="search-box">
            <input type="text" id="search" data-es-placeholder="¿Qué producto buscás?" data-en-placeholder="What product are you looking for?" autocomplete="off" />
            <div class="autocomplete-list" id="autocomplete"></div>
            <button onclick="buscar()" class="i18n-btn" data-es="Buscar" data-en="Search" id="search-btn"></button>
        </div>

        <div class="categories" id="categories">
            <button class="cat-btn active" onclick="filtrarCategoria('todos')" data-es="Todos" data-en="All" class="i18n-cat"></button>
            <button class="cat-btn" onclick="filtrarCategoria('lácteos')">🥛 <span data-es="Lácteos" data-en="Dairy" class="i18n"></span></button>
            <button class="cat-btn" onclick="filtrarCategoria('frutas')">🍎 <span data-es="Frutas y Verduras" data-en="Fruits & Vegetables" class="i18n"></span></button>
            <button class="cat-btn" onclick="filtrarCategoria('carnes')">🥩 <span data-es="Carnes" data-en="Meats" class="i18n"></span></button>
            <button class="cat-btn" onclick="filtrarCategoria('almacén')">🏪 <span data-es="Almacén" data-en="Pantry" class="i18n"></span></button>
            <button class="cat-btn" onclick="filtrarCategoria('bebidas')">🥤 <span data-es="Bebidas" data-en="Drinks" class="i18n"></span></button>
            <button class="cat-btn" onclick="filtrarCategoria('limpieza')">🧹 <span data-es="Limpieza" data-en="Cleaning" class="i18n"></span></button>
        </div>

        <div id="home-section">
            <p class="section-title i18n" data-es="Productos disponibles" data-en="Available products" id="products-title"></p>
            <div class="popular-grid" id="popular-grid"></div>
        </div>
        <div id="results" class="results"></div>
        <div class="scrape-date" id="scrape-date"></div>
    </div>

    <div class="modal-overlay" id="modal-overlay" onclick="cerrarModal(event)">
        <div class="modal" id="modal">
            <button class="modal-close" onclick="cerrarModal()">&times;</button>
            <div id="modal-content"></div>
        </div>
    </div>
    <div class="coupon-copied" id="coupon-copied"></div>

    <script>
        let allProducts = [];
        let lang = 'es';

        const T = {
            es: {
                desde: 'Desde', search_placeholder: '¿Qué producto buscás?', search_btn: 'Buscar',
                no_results_1: 'No encontramos', no_results_2: 'Probá con otro término o elegí un producto de la lista',
                no_autocomplete: 'No hay resultados para', updated: 'Precios actualizados',
                regular_price: 'Precio regular', promo_price: 'Precio promocional', savings: 'Ahorro',
                promo_expires: 'Promo vence', days: 'días', expired: 'Vencida', verdict: 'Veredicto',
                best_price: 'Mejor precio disponible', scrape_title: 'Datos del scraping',
                source: 'Fuente', extraction_date: 'Fecha de extracción', method: 'Método',
                auto_scraping: 'Scraping automático del sitio web', product: 'Producto',
                not_available: 'No disponible', cheapest: 'MÁS BARATO', offer: 'OFERTA',
                expires: 'Vence', coupon_copied: 'Cupón copiado',
                coupons_title: 'Cupones disponibles', products_title: 'Productos disponibles',
                coupon_off: 'OFF', coupon_in: 'en', coupon_valid: 'Válido hasta',
                coupon_min: 'Compra mínima', coupon_tap: 'Tocá para copiar el código',
                online: 'Online',
            },
            en: {
                desde: 'From', search_placeholder: 'What product are you looking for?', search_btn: 'Search',
                no_results_1: 'We couldn\\'t find', no_results_2: 'Try another term or pick a product from the list',
                no_autocomplete: 'No results for', updated: 'Prices updated',
                regular_price: 'Regular price', promo_price: 'Promotional price', savings: 'Savings',
                promo_expires: 'Promo expires', days: 'days', expired: 'Expired', verdict: 'Verdict',
                best_price: 'Best price available', scrape_title: 'Scraping data',
                source: 'Source', extraction_date: 'Extraction date', method: 'Method',
                auto_scraping: 'Automatic website scraping', product: 'Product',
                not_available: 'Not available', cheapest: 'CHEAPEST', offer: 'SALE',
                expires: 'Expires', coupon_copied: 'Coupon copied',
                coupons_title: 'Available coupons', products_title: 'Available products',
                coupon_off: 'OFF', coupon_in: 'at', coupon_valid: 'Valid until',
                coupon_min: 'Minimum purchase', coupon_tap: 'Tap to copy code',
                online: 'Online',
            }
        };
        function t(key) { return T[lang][key] || key; }

        const coupons = [
            { store: 'Coto', cls: 'coupon-coto', discount: '15%', desc_es: 'en Lácteos y Quesos', desc_en: 'on Dairy & Cheese', code: 'COTO15LACTEOS', min_es: '$5.000', min_en: '$5,000 ARS', exp: 7 },
            { store: 'Jumbo', cls: 'coupon-jumbo', discount: '20%', desc_es: 'en Frutas y Verduras', desc_en: 'on Fruits & Vegetables', code: 'JUMBO20FRESH', min_es: '$3.000', min_en: '$3,000 ARS', exp: 5 },
            { store: 'Disco', cls: 'coupon-disco', discount: '10%', desc_es: 'en toda tu compra', desc_en: 'on your entire purchase', code: 'DISCO10TODO', min_es: '$8.000', min_en: '$8,000 ARS', exp: 10 },
            { store: 'Coto', cls: 'coupon-coto', discount: '25%', desc_es: 'en Bebidas', desc_en: 'on Beverages', code: 'COTO25BEBIDAS', min_es: '$2.000', min_en: '$2,000 ARS', exp: 3 },
            { store: 'Jumbo', cls: 'coupon-jumbo', discount: '2x1', desc_es: 'en Limpieza', desc_en: 'on Cleaning products', code: 'JUMBO2X1CLEAN', min_es: '$4.000', min_en: '$4,000 ARS', exp: 12 },
        ];

        function renderCoupons() {
            const scroll = document.getElementById('coupons-scroll');
            const now = new Date();
            scroll.innerHTML = coupons.map(c => {
                const exp = new Date(now.getTime() + c.exp * 24*60*60*1000);
                const expStr = exp.toLocaleDateString(lang === 'es' ? 'es-AR' : 'en-US', {day:'numeric',month:'short'});
                const desc = lang === 'es' ? c.desc_es : c.desc_en;
                const min = lang === 'es' ? c.min_es : c.min_en;
                return `<div class="coupon ${c.cls}" onclick="copyCoupon('${c.code}')">
                    <div class="coupon-circle"></div><div class="coupon-circle2"></div>
                    <div class="store-name">${c.store}</div>
                    <div class="discount">${c.discount} ${t('coupon_off')}</div>
                    <div class="coupon-desc">${desc}</div>
                    <div class="coupon-code">${c.code}</div>
                    <div class="coupon-exp">${t('coupon_valid')} ${expStr} · ${t('coupon_min')} ${min}</div>
                </div>`;
            }).join('');
        }

        function copyCoupon(code) {
            navigator.clipboard.writeText(code).then(() => {
                const el = document.getElementById('coupon-copied');
                el.textContent = '✅ ' + t('coupon_copied') + ': ' + code;
                el.style.display = 'block';
                setTimeout(() => { el.style.display = 'none'; }, 2000);
            });
        }

        function setLang(l) {
            lang = l;
            document.getElementById('btn-es').classList.toggle('active', l === 'es');
            document.getElementById('btn-en').classList.toggle('active', l === 'en');
            document.querySelectorAll('.i18n').forEach(el => {
                if (el.dataset[l]) el.textContent = el.dataset[l];
            });
            document.getElementById('search').placeholder = t('search_placeholder');
            document.getElementById('search-btn').textContent = t('search_btn');
            document.getElementById('coupons-title').textContent = t('coupons_title');
            document.getElementById('products-title').textContent = t('products_title');
            renderCoupons();
            if (allProducts.length) mostrarPopulares(allProducts);
        }

        async function cargarProductos() {
            try {
                const response = await fetch('/api/products');
                allProducts = await response.json();
                mostrarPopulares(allProducts);
            } catch (error) { console.error('Error:', error); }
        }

        function mostrarPopulares(productos) {
            const emojis = {'Leche Entera':'🥛','Yogur Natural':'🥛','Naranjas':'🍊','Huevos':'🥚','Queso Cremoso':'🧀','Manteca':'🧈','Pan Lactal':'🍞','Arroz':'🍚','Fideos Secos':'🍝','Aceite de Girasol':'🫒','Azúcar':'🍬','Harina':'🌾','Galletitas Dulces':'🍪','Gaseosa Cola':'🥤','Agua Mineral':'💧','Papel Higiénico':'🧻','Detergente':'🧴','Jabón en Polvo':'🧼','Pollo Entero':'🍗','Carne Picada':'🥩','Banana':'🍌','Tomate':'🍅','Papa':'🥔','Cebolla':'🧅'};
            document.getElementById('popular-grid').innerHTML = productos.map(p => `
                <div class="popular-item" onclick="buscarProducto('${p.nombre}')">
                    <span class="emoji">${emojis[p.nombre]||'🛒'}</span>
                    <span class="name">${p.nombre}</span>
                    <span class="qty">${p.cantidad}</span>
                    <span class="desde">${t('desde')} $${p.precio_min}</span>
                </div>`).join('');
        }

        function buscarProducto(nombre) { document.getElementById('search').value = nombre; buscar(); }

        function filtrarCategoria(cat) {
            document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
            event.target.closest('.cat-btn').classList.add('active');
            const cats = {'lácteos':['Leche Entera','Yogur Natural','Queso Cremoso','Manteca'],'frutas':['Naranjas','Banana','Tomate','Papa','Cebolla'],'carnes':['Pollo Entero','Carne Picada','Huevos'],'almacén':['Pan Lactal','Arroz','Fideos Secos','Aceite de Girasol','Azúcar','Harina','Galletitas Dulces'],'bebidas':['Gaseosa Cola','Agua Mineral'],'limpieza':['Papel Higiénico','Detergente','Jabón en Polvo']};
            mostrarPopulares(cat === 'todos' ? allProducts : allProducts.filter(p => cats[cat]?.includes(p.nombre)));
            document.getElementById('home-section').style.display = 'block';
            document.getElementById('results').innerHTML = '';
        }

        const searchInput = document.getElementById('search');
        const autocompleteList = document.getElementById('autocomplete');
        searchInput.addEventListener('input', function() {
            const q = this.value.toLowerCase().trim();
            if (q.length < 1) { autocompleteList.style.display = 'none'; return; }
            const matches = allProducts.filter(p => p.nombre.toLowerCase().includes(q));
            if (matches.length === 0) { autocompleteList.innerHTML = '<div class="autocomplete-item" style="color:#94a3b8;">' + t('no_autocomplete') + ' "' + q + '"</div>'; autocompleteList.style.display = 'block'; return; }
            autocompleteList.innerHTML = matches.map(p => `<div class="autocomplete-item" onclick="buscarProducto('${p.nombre}')">${p.nombre} <span class="cantidad">${p.cantidad}</span></div>`).join('');
            autocompleteList.style.display = 'block';
        });
        document.addEventListener('click', function(e) { if (!e.target.closest('.search-box')) autocompleteList.style.display = 'none'; });

        async function buscar() {
            autocompleteList.style.display = 'none';
            const q = document.getElementById("search").value.trim();
            if (!q) return;
            document.getElementById('home-section').style.display = 'none';
            try {
                const response = await fetch(`/api/search?q=${encodeURIComponent(q)}`);
                const data = await response.json();
                let html = "", fechaScraping = "";
                if (Object.keys(data).length === 0) {
                    html = `<div class="no-results"><span class="emoji-big">🔍</span><p>${t('no_results_1')} "<strong>${q}</strong>"</p><p style="margin-top:8px;font-size:13px;">${t('no_results_2')}</p></div>`;
                    document.getElementById('home-section').style.display = 'block';
                }
                for (const [producto, info] of Object.entries(data)) {
                    const precios = info.precios;
                    const mejorPrecio = Math.min(...precios.map(p => p.precio_final));
                    html += `<div class="product"><h3>${producto}</h3><div class="cantidad-label">${info.cantidad}</div>`;
                    for (const precio of precios) {
                        const esMejor = precio.precio_final === mejorPrecio;
                        const clase = esMejor ? "cheapest" : "";
                        const md = encodeURIComponent(JSON.stringify({producto,cantidad:info.cantidad,supermarket:precio.supermarket,precio:precio.precio,precio_promo:precio.precio_promo,precio_final:precio.precio_final,promo_vence:precio.promo_vence,fecha_scraping:precio.fecha_scraping,esMejor}));
                        let ph = "";
                        if (precio.precio_promo) {
                            ph = `<span class="price-promo"><span class="price-original">$${precio.precio}</span><span class="price-oferta">$${precio.precio_promo}</span><span class="badge-promo">${t('offer')}</span></span>`;
                            if (precio.promo_vence) ph += `<span class="promo-vence">${t('expires')}: ${formatDate(precio.promo_vence)}</span>`;
                        } else { ph = `<span class="price">$${precio.precio}</span>`; }
                        html += `<div class="price-item ${clase}" onclick="abrirModal('${md}')"><span class="supermarket">🏪 ${precio.supermarket}</span><div class="price-info">${ph}${esMejor?'<span class="badge">'+t('cheapest')+'</span>':''}</div></div>`;
                        if (precio.fecha_scraping) fechaScraping = precio.fecha_scraping;
                    }
                    html += `</div>`;
                }
                document.getElementById("results").innerHTML = html;
                if (fechaScraping) document.getElementById("scrape-date").innerHTML = `${t('updated')}: ${formatDate(fechaScraping)}`;
            } catch (error) { document.getElementById("results").innerHTML = "<p>Error</p>"; }
        }

        function formatDate(dateStr) { const d = new Date(dateStr+'T00:00:00'); return d.toLocaleDateString(lang==='es'?'es-AR':'en-US',{day:'numeric',month:'long',year:'numeric'}); }
        searchInput.addEventListener("keypress", (e) => { if (e.key === "Enter") buscar(); });

        function abrirModal(encodedData) {
            const d = JSON.parse(decodeURIComponent(encodedData));
            let html = `<h3>🏪 ${d.supermarket}</h3><div class="modal-subtitle">${d.producto} — ${d.cantidad}</div><div class="modal-row"><span class="modal-label">${t('regular_price')}</span><span class="modal-value">$${d.precio}</span></div>`;
            if (d.precio_promo) {
                html += `<div class="modal-row"><span class="modal-label">${t('promo_price')}</span><span class="modal-value promo">$${d.precio_promo}</span></div><div class="modal-row"><span class="modal-label">${t('savings')}</span><span class="modal-value promo">-$${d.precio-d.precio_promo} (${Math.round((1-d.precio_promo/d.precio)*100)}%)</span></div>`;
                if (d.promo_vence) { const dias = Math.ceil((new Date(d.promo_vence+'T00:00:00')-new Date())/(1000*60*60*24)); html += `<div class="modal-row"><span class="modal-label">${t('promo_expires')}</span><span class="modal-value promo">${formatDate(d.promo_vence)} (${dias>0?dias+' '+t('days'):t('expired')})</span></div>`; }
            }
            if (d.esMejor) html += `<div class="modal-row"><span class="modal-label">${t('verdict')}</span><span class="modal-value mejor">✅ ${t('best_price')}</span></div>`;
            html += `<div class="modal-source"><strong>📊 ${t('scrape_title')}</strong>${t('source')}: ${d.supermarket} ${t('online')}<br>${t('extraction_date')}: ${d.fecha_scraping?formatDate(d.fecha_scraping):t('not_available')}<br>${t('method')}: ${t('auto_scraping')}<br>${t('product')}: ${d.producto} (${d.cantidad})</div>`;
            document.getElementById('modal-content').innerHTML = html;
            document.getElementById('modal-overlay').classList.add('active');
        }

        function cerrarModal(event) { if (!event||event.target===document.getElementById('modal-overlay')||event.target.classList.contains('modal-close')) document.getElementById('modal-overlay').classList.remove('active'); }
        document.addEventListener('keydown', (e) => { if (e.key==='Escape') cerrarModal(); });

        // Init
        setLang('es');
        cargarProductos();
        renderCoupons();
    </script>
</body>
</html>'''

@app.route('/api/products')
def products():
    init_db()
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT p.nombre, p.cantidad, MIN(CASE WHEN pr.precio_promo IS NOT NULL THEN pr.precio_promo ELSE pr.precio END) as precio_min FROM productos p JOIN precios pr ON p.id = pr.producto_id GROUP BY p.id ORDER BY p.nombre')
    results = c.fetchall()
    conn.close()
    return jsonify([{'nombre': r['nombre'], 'cantidad': r['cantidad'], 'precio_min': r['precio_min']} for r in results])

@app.route('/api/search')
def search():
    init_db()
    q = request.args.get('q', '').lower()
    if not q: return jsonify({})
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT p.nombre, p.cantidad, s.nombre as supermarket, pr.precio, pr.precio_promo, pr.promo_vence, pr.fecha_scraping FROM precios pr JOIN productos p ON pr.producto_id = p.id JOIN supermarkets s ON pr.supermercado_id = s.id WHERE LOWER(p.nombre) LIKE ? ORDER BY p.nombre, pr.precio', (f'%{q}%',))
    results = c.fetchall()
    conn.close()
    grouped = {}
    for row in results:
        prod = row['nombre']
        if prod not in grouped: grouped[prod] = {'cantidad': row['cantidad'], 'precios': []}
        pf = row['precio_promo'] if row['precio_promo'] else row['precio']
        grouped[prod]['precios'].append({'supermarket': row['supermarket'], 'precio': row['precio'], 'precio_promo': row['precio_promo'], 'precio_final': pf, 'promo_vence': row['promo_vence'], 'fecha_scraping': row['fecha_scraping']})
    return jsonify(grouped)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
