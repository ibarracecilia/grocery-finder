from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DATABASE = '/tmp/grocery.db'

def init_db():
    if os.path.exists(DATABASE):
        return
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('CREATE TABLE supermarkets (id INTEGER PRIMARY KEY, nombre TEXT)')
    c.execute('CREATE TABLE productos (id INTEGER PRIMARY KEY, nombre TEXT UNIQUE)')
    c.execute('CREATE TABLE precios (id INTEGER PRIMARY KEY, supermercado_id INTEGER, producto_id INTEGER, precio REAL)')
    c.execute("INSERT INTO supermarkets VALUES (1, 'Coto')")
    c.execute("INSERT INTO supermarkets VALUES (2, 'Jumbo')")
    c.execute("INSERT INTO supermarkets VALUES (3, 'Disco')")
    c.execute("INSERT INTO productos VALUES (1, 'Leche')")
    c.execute("INSERT INTO productos VALUES (2, 'Yogur')")
    c.execute("INSERT INTO productos VALUES (3, 'Naranjas')")
    c.execute("INSERT INTO productos VALUES (4, 'Huevos')")
    c.execute("INSERT INTO productos VALUES (5, 'Queso')")
    c.execute("INSERT INTO productos VALUES (6, 'Manteca')")
    for sm, prod, price in [
        (1,1,250),(2,1,240),(3,1,230),
        (1,2,240),(2,2,230),(3,2,250),
        (1,3,250),(2,3,220),(3,3,220),
        (1,4,300),(2,4,290),(3,4,310),
        (1,5,320),(2,5,310),(3,5,330),
        (1,6,280),(2,6,270),(3,6,290)
    ]:
        c.execute('INSERT INTO precios (supermercado_id, producto_id, precio) VALUES (?, ?, ?)', (sm, prod, price))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GroceryFinder</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; justify-content: center; align-items: center; padding: 20px; }
        .container { background: white; border-radius: 15px; padding: 40px; max-width: 600px; width: 100%; box-shadow: 0 10px 40px rgba(0,0,0,0.2); }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { color: #333; font-size: 32px; margin-bottom: 10px; }
        .header p { color: #666; font-size: 14px; }
        .search-box { display: flex; gap: 10px; margin-bottom: 30px; }
        .search-box input { flex: 1; padding: 12px; border: 2px solid #ddd; border-radius: 8px; font-size: 14px; }
        .search-box button { padding: 12px 30px; background: #4caf50; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; transition: background 0.3s; }
        .search-box button:hover { background: #45a049; }
        .results { margin-top: 20px; }
        .product { margin-bottom: 20px; padding: 15px; border-left: 4px solid #667eea; background: #f9f9f9; border-radius: 5px; }
        .product h3 { color: #333; margin-bottom: 10px; font-size: 18px; }
        .price-item { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee; }
        .price-item:last-child { border-bottom: none; }
        .supermarket { display: flex; align-items: center; gap: 5px; }
        .price { font-weight: bold; color: #667eea; }
        .cheapest { background: #d4edda; padding: 8px; border-radius: 4px; }
        .cheapest .price { color: #28a745; }
        .badge { background: #28a745; color: white; padding: 2px 8px; border-radius: 3px; font-size: 12px; margin-left: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛒 GroceryFinder</h1>
            <p>Encontrá los mejores precios en Buenos Aires</p>
        </div>
        <div class="search-box">
            <input type="text" id="search" placeholder="Busca un producto..." />
            <button onclick="buscar()">BUSCAR</button>
        </div>
        <div id="results" class="results"></div>
    </div>
    <script>
        async function buscar() {
            const q = document.getElementById("search").value.toLowerCase();
            if (!q) return;
            try {
                const response = await fetch(`/api/search?q=${encodeURIComponent(q)}`);
                const data = await response.json();
                let html = "";
                for (const [producto, precios] of Object.entries(data)) {
                    const precioMinimo = Math.min(...precios.map((p) => p.price));
                    html += `<div class="product"><h3>${producto}</h3>`;
                    for (const precio of precios) {
                        const esMinimo = precio.price === precioMinimo;
                        const clase = esMinimo ? "cheapest" : "";
                        html += `<div class="price-item ${clase}"><span class="supermarket">🏪 ${precio.supermarket}</span><span class="price">$${precio.price}${esMinimo ? '<span class="badge">MÁS BARATO</span>' : ""}</span></div>`;
                    }
                    html += `</div>`;
                }
                document.getElementById("results").innerHTML = html || "<p>No encontrado</p>";
            } catch (error) {
                document.getElementById("results").innerHTML = "<p>Error en la búsqueda</p>";
            }
        }
        document.getElementById("search").addEventListener("keypress", (e) => { if (e.key === "Enter") buscar(); });
    </script>
</body>
</html>'''

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
        SELECT p.nombre, s.nombre as supermarket, pr.precio
        FROM precios pr
        JOIN productos p ON pr.producto_id = p.id
        JOIN supermarkets s ON pr.supermercado_id = s.id
        WHERE LOWER(p.nombre) LIKE ?
    ''', (f'%{q}%',))
    results = c.fetchall()
    conn.close()
    grouped = {}
    for row in results:
        prod = row['nombre']
        if prod not in grouped:
            grouped[prod] = []
        grouped[prod].append({'supermarket': row['supermarket'], 'price': row['precio']})
    return jsonify(grouped)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
