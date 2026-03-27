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
        (1, 'Leche Entera', '1L'),
        (2, 'Yogur Natural', '200g'),
        (3, 'Naranjas', '1kg'),
        (4, 'Huevos', '12 unidades'),
        (5, 'Queso Cremoso', '1kg'),
        (6, 'Manteca', '200g'),
        (7, 'Pan Lactal', '500g'),
        (8, 'Arroz', '1kg'),
        (9, 'Fideos Secos', '500g'),
        (10, 'Aceite de Girasol', '1.5L'),
        (11, 'Azúcar', '1kg'),
        (12, 'Harina', '1kg'),
        (13, 'Galletitas Dulces', '300g'),
        (14, 'Gaseosa Cola', '2.25L'),
        (15, 'Agua Mineral', '2L'),
        (16, 'Papel Higiénico', '4 rollos'),
        (17, 'Detergente', '750ml'),
        (18, 'Jabón en Polvo', '800g'),
        (19, 'Pollo Entero', '1kg'),
        (20, 'Carne Picada', '1kg'),
        (21, 'Banana', '1kg'),
        (22, 'Tomate', '1kg'),
        (23, 'Papa', '1kg'),
        (24, 'Cebolla', '1kg'),
    ]
    for p in productos:
        c.execute('INSERT INTO productos VALUES (?, ?, ?)', p)
    
    hoy = datetime.now().strftime('%Y-%m-%d')
    promo_vence = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    promo_vence2 = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
    
    precios = [
        # Leche Entera
        (1, 1, 1, 1250, 1100, promo_vence, hoy),
        (2, 2, 1, 1240, None, None, hoy),
        (3, 3, 1, 1230, 1150, promo_vence2, hoy),
        # Yogur Natural
        (4, 1, 2, 890, None, None, hoy),
        (5, 2, 2, 850, 790, promo_vence, hoy),
        (6, 3, 2, 920, None, None, hoy),
        # Naranjas
        (7, 1, 3, 1500, 1350, promo_vence, hoy),
        (8, 2, 3, 1420, None, None, hoy),
        (9, 3, 3, 1380, None, None, hoy),
        # Huevos
        (10, 1, 4, 2300, None, None, hoy),
        (11, 2, 4, 2190, 1990, promo_vence2, hoy),
        (12, 3, 4, 2410, None, None, hoy),
        # Queso Cremoso
        (13, 1, 5, 4200, None, None, hoy),
        (14, 2, 5, 4100, 3800, promo_vence, hoy),
        (15, 3, 5, 4350, None, None, hoy),
        # Manteca
        (16, 1, 6, 1800, None, None, hoy),
        (17, 2, 6, 1750, None, None, hoy),
        (18, 3, 6, 1900, 1700, promo_vence, hoy),
        # Pan Lactal
        (19, 1, 7, 1600, 1400, promo_vence, hoy),
        (20, 2, 7, 1550, None, None, hoy),
        (21, 3, 7, 1580, None, None, hoy),
        # Arroz
        (22, 1, 8, 1100, None, None, hoy),
        (23, 2, 8, 1050, 950, promo_vence2, hoy),
        (24, 3, 8, 1150, None, None, hoy),
        # Fideos Secos
        (25, 1, 9, 750, None, None, hoy),
        (26, 2, 9, 720, None, None, hoy),
        (27, 3, 9, 780, 690, promo_vence, hoy),
        # Aceite de Girasol
        (28, 1, 10, 2200, 1990, promo_vence, hoy),
        (29, 2, 10, 2150, None, None, hoy),
        (30, 3, 10, 2300, None, None, hoy),
        # Azúcar
        (31, 1, 11, 950, None, None, hoy),
        (32, 2, 11, 920, None, None, hoy),
        (33, 3, 11, 980, 850, promo_vence2, hoy),
        # Harina
        (34, 1, 12, 650, None, None, hoy),
        (35, 2, 12, 630, 550, promo_vence, hoy),
        (36, 3, 12, 680, None, None, hoy),
        # Galletitas Dulces
        (37, 1, 13, 1200, None, None, hoy),
        (38, 2, 13, 1150, None, None, hoy),
        (39, 3, 13, 1250, 1100, promo_vence, hoy),
        # Gaseosa Cola
        (40, 1, 14, 1800, 1600, promo_vence2, hoy),
        (41, 2, 14, 1750, None, None, hoy),
        (42, 3, 14, 1850, None, None, hoy),
        # Agua Mineral
        (43, 1, 15, 800, None, None, hoy),
        (44, 2, 15, 780, None, None, hoy),
        (45, 3, 15, 820, 700, promo_vence, hoy),
        # Papel Higiénico
        (46, 1, 16, 1500, None, None, hoy),
        (47, 2, 16, 1450, 1300, promo_vence, hoy),
        (48, 3, 16, 1550, None, None, hoy),
        # Detergente
        (49, 1, 17, 950, None, None, hoy),
        (50, 2, 17, 920, None, None, hoy),
        (51, 3, 17, 980, 880, promo_vence2, hoy),
        # Jabón en Polvo
        (52, 1, 18, 2100, 1900, promo_vence, hoy),
        (53, 2, 18, 2050, None, None, hoy),
        (54, 3, 18, 2200, None, None, hoy),
        # Pollo Entero
        (55, 1, 19, 2800, None, None, hoy),
        (56, 2, 19, 2700, 2500, promo_vence, hoy),
        (57, 3, 19, 2900, None, None, hoy),
        # Carne Picada
        (58, 1, 20, 4500, None, None, hoy),
        (59, 2, 20, 4400, None, None, hoy),
        (60, 3, 20, 4600, 4200, promo_vence2, hoy),
        # Banana
        (61, 1, 21, 1200, 1050, promo_vence, hoy),
        (62, 2, 21, 1150, None, None, hoy),
        (63, 3, 21, 1250, None, None, hoy),
        # Tomate
        (64, 1, 22, 1800, None, None, hoy),
        (65, 2, 22, 1750, 1600, promo_vence, hoy),
        (66, 3, 22, 1850, None, None, hoy),
        # Papa
        (67, 1, 23, 900, None, None, hoy),
        (68, 2, 23, 850, None, None, hoy),
        (69, 3, 23, 950, 800, promo_vence, hoy),
        # Cebolla
        (70, 1, 24, 800, 700, promo_vence2, hoy),
        (71, 2, 24, 780, None, None, hoy),
        (72, 3, 24, 820, None, None, hoy),
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
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .container { background: white; border-radius: 15px; padding: 30px; max-width: 700px; width: 100%; margin: 0 auto; box-shadow: 0 10px 40px rgba(0,0,0,0.2); }
        .header { text-align: center; margin-bottom: 25px; }
        .header h1 { color: #333; font-size: 28px; margin-bottom: 5px; }
        .header p { color: #666; font-size: 14px; }
        .search-box { position: relative; display: flex; gap: 10px; margin-bottom: 20px; }
        .search-box input { flex: 1; padding: 12px 15px; border: 2px solid #ddd; border-radius: 8px; font-size: 15px; outline: none; transition: border 0.3s; }
        .search-box input:focus { border-color: #667eea; }
        .search-box button { padding: 12px 25px; background: #4caf50; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; font-size: 14px; transition: background 0.3s; }
        .search-box button:hover { background: #45a049; }
        .autocomplete-list { position: absolute; top: 100%; left: 0; right: 70px; background: white; border: 1px solid #ddd; border-top: none; border-radius: 0 0 8px 8px; max-height: 200px; overflow-y: auto; z-index: 10; display: none; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        .autocomplete-item { padding: 10px 15px; cursor: pointer; font-size: 14px; border-bottom: 1px solid #f0f0f0; }
        .autocomplete-item:hover { background: #f0f4ff; }
        .autocomplete-item .cantidad { color: #999; font-size: 12px; margin-left: 5px; }
        .info-bar { background: #f0f4ff; border-radius: 8px; padding: 12px 15px; margin-bottom: 20px; font-size: 13px; color: #555; display: flex; justify-content: space-between; align-items: center; }
        .info-bar .fecha { color: #667eea; font-weight: 600; }
        .categories { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 20px; }
        .cat-btn { padding: 6px 14px; border: 1px solid #ddd; border-radius: 20px; background: white; cursor: pointer; font-size: 13px; transition: all 0.3s; }
        .cat-btn:hover, .cat-btn.active { background: #667eea; color: white; border-color: #667eea; }
        .section-title { font-size: 16px; color: #333; margin-bottom: 12px; font-weight: 600; }
        .results { margin-top: 10px; }
        .product { margin-bottom: 15px; padding: 15px; border-left: 4px solid #667eea; background: #f9f9f9; border-radius: 0 8px 8px 0; }
        .product h3 { color: #333; margin-bottom: 3px; font-size: 17px; }
        .product .cantidad-label { color: #888; font-size: 13px; margin-bottom: 10px; }
        .price-item { display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #eee; }
        .price-item:last-child { border-bottom: none; }
        .supermarket { display: flex; align-items: center; gap: 5px; font-size: 14px; }
        .price-info { text-align: right; }
        .price { font-weight: bold; color: #667eea; font-size: 15px; }
        .price-promo { font-size: 13px; }
        .price-original { text-decoration: line-through; color: #999; margin-right: 8px; }
        .price-oferta { color: #e53e3e; font-weight: bold; }
        .promo-vence { font-size: 11px; color: #e53e3e; display: block; margin-top: 2px; }
        .cheapest { background: #d4edda; padding: 8px; border-radius: 4px; }
        .cheapest .price { color: #28a745; }
        .badge { background: #28a745; color: white; padding: 2px 8px; border-radius: 3px; font-size: 11px; margin-left: 8px; }
        .badge-promo { background: #e53e3e; color: white; padding: 2px 8px; border-radius: 3px; font-size: 11px; margin-left: 8px; }
        .popular-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 10px; margin-bottom: 20px; }
        .popular-item { background: #f9f9f9; border-radius: 8px; padding: 12px; text-align: center; cursor: pointer; transition: all 0.3s; border: 1px solid #eee; }
        .popular-item:hover { background: #f0f4ff; border-color: #667eea; transform: translateY(-2px); }
        .popular-item .emoji { font-size: 28px; display: block; margin-bottom: 5px; }
        .popular-item .name { font-size: 13px; color: #333; font-weight: 600; }
        .popular-item .qty { font-size: 11px; color: #888; }
        .popular-item .desde { font-size: 12px; color: #667eea; font-weight: 600; margin-top: 4px; }
        .no-results { text-align: center; padding: 30px; color: #888; }
        .no-results .emoji-big { font-size: 48px; display: block; margin-bottom: 10px; }
        .scrape-date { text-align: center; font-size: 11px; color: #aaa; margin-top: 15px; }
        @media (max-width: 500px) {
            .container { padding: 20px 15px; }
            .header h1 { font-size: 24px; }
            .popular-grid { grid-template-columns: repeat(3, 1fr); gap: 8px; }
            .popular-item { padding: 10px 6px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛒 GroceryFinder</h1>
            <p>Compará precios en supermercados de Buenos Aires</p>
        </div>
        
        <div class="search-box">
            <input type="text" id="search" placeholder="¿Qué producto buscás?" autocomplete="off" />
            <div class="autocomplete-list" id="autocomplete"></div>
            <button onclick="buscar()">BUSCAR</button>
        </div>

        <div class="categories" id="categories">
            <button class="cat-btn active" onclick="filtrarCategoria('todos')">Todos</button>
            <button class="cat-btn" onclick="filtrarCategoria('lácteos')">🥛 Lácteos</button>
            <button class="cat-btn" onclick="filtrarCategoria('frutas')">🍎 Frutas y Verduras</button>
            <button class="cat-btn" onclick="filtrarCategoria('carnes')">🥩 Carnes</button>
            <button class="cat-btn" onclick="filtrarCategoria('almacén')">🏪 Almacén</button>
            <button class="cat-btn" onclick="filtrarCategoria('bebidas')">🥤 Bebidas</button>
            <button class="cat-btn" onclick="filtrarCategoria('limpieza')">🧹 Limpieza</button>
        </div>

        <div id="home-section">
            <p class="section-title">🔥 Productos populares</p>
            <div class="popular-grid" id="popular-grid"></div>
        </div>

        <div id="results" class="results"></div>
        <div class="scrape-date" id="scrape-date"></div>
    </div>

    <script>
        let allProducts = [];
        
        async function cargarProductos() {
            try {
                const response = await fetch('/api/products');
                allProducts = await response.json();
                mostrarPopulares(allProducts);
            } catch (error) {
                console.error('Error cargando productos:', error);
            }
        }
        
        function mostrarPopulares(productos) {
            const emojis = {
                'Leche Entera': '🥛', 'Yogur Natural': '🥛', 'Naranjas': '🍊',
                'Huevos': '🥚', 'Queso Cremoso': '🧀', 'Manteca': '🧈',
                'Pan Lactal': '🍞', 'Arroz': '🍚', 'Fideos Secos': '🍝',
                'Aceite de Girasol': '🫒', 'Azúcar': '🍬', 'Harina': '🌾',
                'Galletitas Dulces': '🍪', 'Gaseosa Cola': '🥤', 'Agua Mineral': '💧',
                'Papel Higiénico': '🧻', 'Detergente': '🧴', 'Jabón en Polvo': '🧼',
                'Pollo Entero': '🍗', 'Carne Picada': '🥩', 'Banana': '🍌',
                'Tomate': '🍅', 'Papa': '🥔', 'Cebolla': '🧅'
            };
            const grid = document.getElementById('popular-grid');
            grid.innerHTML = productos.map(p => `
                <div class="popular-item" onclick="buscarProducto('${p.nombre}')">
                    <span class="emoji">${emojis[p.nombre] || '🛒'}</span>
                    <span class="name">${p.nombre}</span>
                    <span class="qty">${p.cantidad}</span>
                    <span class="desde">Desde $${p.precio_min}</span>
                </div>
            `).join('');
        }
        
        function buscarProducto(nombre) {
            document.getElementById('search').value = nombre;
            buscar();
        }
        
        function filtrarCategoria(cat) {
            document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
            event.target.classList.add('active');
            
            const categorias = {
                'lácteos': ['Leche Entera', 'Yogur Natural', 'Queso Cremoso', 'Manteca'],
                'frutas': ['Naranjas', 'Banana', 'Tomate', 'Papa', 'Cebolla'],
                'carnes': ['Pollo Entero', 'Carne Picada', 'Huevos'],
                'almacén': ['Pan Lactal', 'Arroz', 'Fideos Secos', 'Aceite de Girasol', 'Azúcar', 'Harina', 'Galletitas Dulces'],
                'bebidas': ['Gaseosa Cola', 'Agua Mineral'],
                'limpieza': ['Papel Higiénico', 'Detergente', 'Jabón en Polvo']
            };
            
            if (cat === 'todos') {
                mostrarPopulares(allProducts);
            } else {
                const filtrados = allProducts.filter(p => categorias[cat]?.includes(p.nombre));
                mostrarPopulares(filtrados);
            }
            
            document.getElementById('home-section').style.display = 'block';
            document.getElementById('results').innerHTML = '';
        }

        // Autocompletado
        const searchInput = document.getElementById('search');
        const autocompleteList = document.getElementById('autocomplete');
        
        searchInput.addEventListener('input', function() {
            const q = this.value.toLowerCase().trim();
            if (q.length < 1) {
                autocompleteList.style.display = 'none';
                return;
            }
            const matches = allProducts.filter(p => 
                p.nombre.toLowerCase().includes(q)
            );
            if (matches.length === 0) {
                autocompleteList.innerHTML = '<div class="autocomplete-item" style="color:#999;">No hay resultados para "' + q + '"</div>';
                autocompleteList.style.display = 'block';
                return;
            }
            autocompleteList.innerHTML = matches.map(p => 
                `<div class="autocomplete-item" onclick="buscarProducto('${p.nombre}')">
                    ${p.nombre} <span class="cantidad">${p.cantidad}</span>
                </div>`
            ).join('');
            autocompleteList.style.display = 'block';
        });
        
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.search-box')) {
                autocompleteList.style.display = 'none';
            }
        });

        async function buscar() {
            autocompleteList.style.display = 'none';
            const q = document.getElementById("search").value.trim();
            if (!q) return;
            
            document.getElementById('home-section').style.display = 'none';
            
            try {
                const response = await fetch(`/api/search?q=${encodeURIComponent(q)}`);
                const data = await response.json();
                let html = "";
                let fechaScraping = "";
                
                if (Object.keys(data).length === 0) {
                    html = `<div class="no-results">
                        <span class="emoji-big">🔍</span>
                        <p>No encontramos "<strong>${q}</strong>"</p>
                        <p style="margin-top:8px; font-size:13px;">Probá con otro término o elegí un producto de la lista</p>
                    </div>`;
                    document.getElementById('home-section').style.display = 'block';
                }
                
                for (const [producto, info] of Object.entries(data)) {
                    const precios = info.precios;
                    const mejorPrecio = Math.min(...precios.map(p => p.precio_final));
                    
                    html += `<div class="product"><h3>${producto}</h3>`;
                    html += `<div class="cantidad-label">${info.cantidad}</div>`;
                    
                    for (const precio of precios) {
                        const esMejor = precio.precio_final === mejorPrecio;
                        const clase = esMejor ? "cheapest" : "";
                        
                        let precioHtml = "";
                        if (precio.precio_promo) {
                            precioHtml = `<span class="price-promo">
                                <span class="price-original">$${precio.precio}</span>
                                <span class="price-oferta">$${precio.precio_promo}</span>
                                <span class="badge-promo">OFERTA</span>
                            </span>`;
                            if (precio.promo_vence) {
                                precioHtml += `<span class="promo-vence">Vence: ${formatDate(precio.promo_vence)}</span>`;
                            }
                        } else {
                            precioHtml = `<span class="price">$${precio.precio}</span>`;
                        }
                        
                        html += `<div class="price-item ${clase}">
                            <span class="supermarket">🏪 ${precio.supermarket}</span>
                            <div class="price-info">
                                ${precioHtml}
                                ${esMejor ? '<span class="badge">MÁS BARATO</span>' : ''}
                            </div>
                        </div>`;
                        
                        if (precio.fecha_scraping) fechaScraping = precio.fecha_scraping;
                    }
                    html += `</div>`;
                }
                
                document.getElementById("results").innerHTML = html;
                
                if (fechaScraping) {
                    document.getElementById("scrape-date").innerHTML = 
                        `📅 Precios actualizados: ${formatDate(fechaScraping)}`;
                }
            } catch (error) {
                document.getElementById("results").innerHTML = "<p>Error en la búsqueda</p>";
            }
        }
        
        function formatDate(dateStr) {
            const d = new Date(dateStr + 'T00:00:00');
            const opciones = { day: 'numeric', month: 'long', year: 'numeric' };
            return d.toLocaleDateString('es-AR', opciones);
        }
        
        searchInput.addEventListener("keypress", (e) => { if (e.key === "Enter") buscar(); });
        
        // Cargar productos al inicio
        cargarProductos();
    </script>
</body>
</html>'''

@app.route('/api/products')
def products():
    init_db()
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''
        SELECT p.nombre, p.cantidad, MIN(
            CASE WHEN pr.precio_promo IS NOT NULL THEN pr.precio_promo ELSE pr.precio END
        ) as precio_min
        FROM productos p
        JOIN precios pr ON p.id = pr.producto_id
        GROUP BY p.id
        ORDER BY p.nombre
    ''')
    results = c.fetchall()
    conn.close()
    return jsonify([{'nombre': r['nombre'], 'cantidad': r['cantidad'], 'precio_min': r['precio_min']} for r in results])

@app.route('/api/search')
def search():
    init_db()
    q = request.args.get('q', '').lower()
    if not q:
        return jsonify({})
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''
        SELECT p.nombre, p.cantidad, s.nombre as supermarket, 
               pr.precio, pr.precio_promo, pr.promo_vence, pr.fecha_scraping
        FROM precios pr
        JOIN productos p ON pr.producto_id = p.id
        JOIN supermarkets s ON pr.supermercado_id = s.id
        WHERE LOWER(p.nombre) LIKE ?
        ORDER BY p.nombre, pr.precio
    ''', (f'%{q}%',))
    results = c.fetchall()
    conn.close()
    grouped = {}
    for row in results:
        prod = row['nombre']
        if prod not in grouped:
            grouped[prod] = {
                'cantidad': row['cantidad'],
                'precios': []
            }
        precio_final = row['precio_promo'] if row['precio_promo'] else row['precio']
        grouped[prod]['precios'].append({
            'supermarket': row['supermarket'],
            'precio': row['precio'],
            'precio_promo': row['precio_promo'],
            'precio_final': precio_final,
            'promo_vence': row['promo_vence'],
            'fecha_scraping': row['fecha_scraping']
        })
    return jsonify(grouped)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
