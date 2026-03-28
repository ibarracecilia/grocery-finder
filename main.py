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
<title>GroceryFinder</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
<style>
:root{
--bg:#fafaf8;--card:#fff;--card2:#f5f3ef;--border:#e8e5df;--text:#1a1a18;--text2:#6b6960;--text3:#9e9a90;
--accent:#0d9488;--accent2:#06b6a4;--accent-bg:#e6faf7;--accent-glow:rgba(13,148,136,0.12);
--red:#e8553a;--red-bg:#fef0ec;--green:#1a9e6f;--green-bg:#e8f8f0;
--shadow-sm:0 1px 2px rgba(26,26,24,0.04);--shadow-md:0 4px 20px rgba(26,26,24,0.06);--shadow-lg:0 12px 40px rgba(26,26,24,0.08);
--shadow-glow:0 0 40px rgba(13,148,136,0.08);--radius:16px;
}
[data-theme="dark"]{
--bg:#111110;--card:#1c1c1a;--card2:#242422;--border:#333330;--text:#f0ede6;--text2:#a09d94;--text3:#6b6960;
--accent:#2dd4bf;--accent2:#5eead4;--accent-bg:#0d2d28;--accent-glow:rgba(45,212,191,0.15);
--red:#f87171;--red-bg:#3b1515;--green:#34d399;--green-bg:#0d3320;
--shadow-sm:0 1px 2px rgba(0,0,0,0.2);--shadow-md:0 4px 20px rgba(0,0,0,0.3);--shadow-lg:0 12px 40px rgba(0,0,0,0.4);
--shadow-glow:0 0 40px rgba(45,212,191,0.1);
}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'DM Sans',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;transition:background .4s,color .4s}
@keyframes fadeUp{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}
@keyframes slideIn{from{opacity:0;transform:translateX(-12px)}to{opacity:1;transform:translateX(0)}}
@keyframes scaleIn{from{transform:scale(.95);opacity:0}to{transform:scale(1);opacity:1}}
@keyframes pulseNode{0%,100%{opacity:.2;r:2.5}50%{opacity:.8;r:3.5}}
@keyframes glowCore{0%,100%{opacity:.5}50%{opacity:1}}
@keyframes pulsePin{0%,100%{opacity:.4}50%{opacity:.8}}
.logo-node{animation:pulseNode 2.5s ease-in-out infinite}
.logo-node:nth-child(2){animation-delay:.4s}.logo-node:nth-child(3){animation-delay:.8s}
.logo-node:nth-child(4){animation-delay:1.2s}.logo-node:nth-child(5){animation-delay:1.6s}
.logo-core{animation:glowCore 3s ease-in-out infinite}
.logo-pin{animation:pulsePin 2s ease-in-out infinite}
.logo-pin:nth-child(odd){animation-delay:.3s}
.logo-svg:hover .logo-node{animation-duration:1s}
.logo-svg:hover .logo-core{opacity:1;animation-duration:1s}
nav{max-width:800px;margin:0 auto;padding:16px 20px;display:flex;justify-content:space-between;align-items:center}
nav .logo svg{height:72px;width:auto}
nav .controls{display:flex;align-items:center;gap:8px}
.pill-toggle{display:flex;background:var(--card2);border-radius:10px;padding:3px;border:1px solid var(--border)}
.pill-btn{padding:5px 12px;border:none;border-radius:8px;font-size:12px;font-weight:600;cursor:pointer;background:transparent;color:var(--text3);font-family:'DM Sans',sans-serif;transition:all .2s}
.pill-btn.active{background:var(--accent);color:#fff;box-shadow:0 2px 8px rgba(13,148,136,.3)}
.theme-btn{width:36px;height:36px;border-radius:10px;border:1px solid var(--border);background:var(--card2);cursor:pointer;font-size:15px;display:flex;align-items:center;justify-content:center;transition:all .2s}
.theme-btn:hover{border-color:var(--accent);background:var(--accent-bg)}
.nav-cur{padding:5px 8px;border:1px solid var(--border);border-radius:10px;background:var(--card2);color:var(--accent);font-family:'Space Grotesk',sans-serif;font-size:12px;font-weight:700;outline:none;cursor:pointer;transition:all .2s}
.nav-cur:focus{border-color:var(--accent)}
.cur-eq{font-size:11px;color:var(--accent);font-weight:600;opacity:.7;display:block;margin-top:1px}
.cur-eq-i{font-size:11px;color:var(--accent);font-weight:600;opacity:.7;margin-left:4px}
.hero{max-width:800px;margin:0 auto;padding:0 20px 24px;animation:fadeUp .6s ease-out}
.hero h1{font-family:'Space Grotesk',sans-serif;font-size:clamp(28px,5vw,38px);font-weight:700;letter-spacing:-1.5px;line-height:1.1;margin-bottom:8px}
.hero h1 em{font-style:normal;color:var(--accent);position:relative}
.hero p{color:var(--text2);font-size:16px;max-width:480px}
.main{max-width:800px;margin:0 auto;padding:0 20px 40px}
.search-wrap{position:relative;margin-bottom:24px;animation:fadeUp .6s ease-out .1s both}
.search-wrap input{width:100%;padding:16px 20px 16px 48px;border:2px solid var(--border);border-radius:14px;font-size:16px;background:var(--card);color:var(--text);font-family:'DM Sans',sans-serif;outline:none;transition:all .25s;box-shadow:var(--shadow-sm)}
.search-wrap input:focus{border-color:var(--accent);box-shadow:var(--shadow-glow),0 0 0 4px var(--accent-glow)}
.search-wrap input::placeholder{color:var(--text3)}
.search-wrap .search-icon{position:absolute;left:16px;top:50%;transform:translateY(-50%);width:20px;height:20px;color:var(--text3)}
.autocomplete-list{position:absolute;top:100%;left:0;right:0;background:var(--card);border:1px solid var(--border);border-radius:0 0 14px 14px;max-height:220px;overflow-y:auto;z-index:10;display:none;box-shadow:var(--shadow-lg)}
.autocomplete-item{padding:12px 20px;cursor:pointer;font-size:14px;border-bottom:1px solid var(--border);color:var(--text);transition:background .15s}
.autocomplete-item:hover{background:var(--accent-bg)}
.autocomplete-item .qty{color:var(--text3);font-size:12px;margin-left:6px}
.cur-eq{font-size:11px;color:var(--text3);font-weight:500;display:block;margin-top:2px}
.cur-eq-i{font-size:11px;color:var(--text3);font-weight:500;margin-left:5px}
.modal-cur{margin-top:14px;padding:14px;background:var(--card2);border-radius:12px;border:1px solid var(--border)}
.modal-cur-title{font-size:12px;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:1px;margin-bottom:8px}
.modal-cur-row{display:flex;align-items:center;gap:8px}
.modal-cur-sel{padding:6px 10px;border:1px solid var(--border);border-radius:8px;background:var(--card);color:var(--text);font-family:'DM Sans',sans-serif;font-size:13px;font-weight:600;outline:none;cursor:pointer}
.modal-cur-val{font-family:'Space Grotesk',sans-serif;font-size:16px;font-weight:700;color:var(--accent)}
.coupons{margin-bottom:28px;animation:fadeUp .6s ease-out .2s both}
.coupons-title{font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;color:var(--text3);margin-bottom:12px}
.coupons-scroll{display:flex;gap:14px;overflow-x:auto;padding-bottom:8px;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch}
.coupons-scroll::-webkit-scrollbar{height:0}
.coupon{min-width:240px;border-radius:16px;padding:20px;position:relative;overflow:hidden;cursor:pointer;transition:transform .25s;flex-shrink:0;scroll-snap-align:start}
.coupon:hover{transform:translateY(-4px) scale(1.01)}
.coupon:active{transform:scale(.98)}
.coupon-coto{background:linear-gradient(135deg,#e8553a,#f97358)}
.coupon-jumbo{background:linear-gradient(135deg,#059669,#34d399)}
.coupon-disco{background:linear-gradient(135deg,#7c3aed,#a78bfa)}
.coupon *{color:#fff}
.coupon .store{font-size:13px;font-weight:600;opacity:.85;margin-bottom:6px}
.coupon .disc{font-family:'Space Grotesk',sans-serif;font-size:32px;font-weight:700;line-height:1}
.coupon .cdesc{font-size:13px;margin-top:4px;opacity:.85}
.coupon .ccode{display:inline-block;background:rgba(255,255,255,.22);backdrop-filter:blur(4px);padding:4px 12px;border-radius:8px;font-size:11px;font-weight:700;margin-top:10px;letter-spacing:1.5px}
.coupon .cexp{font-size:10px;opacity:.6;margin-top:6px}
.coupon .blob{position:absolute;border-radius:50%;background:rgba(255,255,255,.1)}
.coupon .blob1{width:80px;height:80px;right:-20px;top:-20px}
.coupon .blob2{width:60px;height:60px;right:30px;bottom:-25px;background:rgba(255,255,255,.06)}
.cats{display:flex;gap:8px;overflow-x:auto;margin-bottom:24px;padding-bottom:4px;animation:fadeUp .6s ease-out .25s both;-webkit-overflow-scrolling:touch}
.cats::-webkit-scrollbar{height:0}
.cat{padding:9px 18px;border:1.5px solid var(--border);border-radius:28px;background:var(--card);cursor:pointer;font-size:14px;font-weight:600;color:var(--text2);white-space:nowrap;transition:all .2s;font-family:'DM Sans',sans-serif}
.cat:hover{border-color:var(--accent);color:var(--accent);background:var(--accent-bg)}
.cat.active{background:var(--accent);color:#fff;border-color:var(--accent);box-shadow:0 4px 14px rgba(13,148,136,.25)}
.sec-title{font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;color:var(--text3);margin-bottom:16px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:14px;margin-bottom:24px}
.item{background:var(--card);border-radius:var(--radius);padding:20px 14px;text-align:center;cursor:pointer;border:1.5px solid var(--border);transition:all .3s;position:relative;overflow:hidden}
.item:hover{border-color:var(--accent);transform:translateY(-6px);box-shadow:var(--shadow-lg),var(--shadow-glow)}
.item:active{transform:scale(.97)}
.item .emo{font-size:42px;display:block;margin-bottom:10px;transition:transform .3s}
.item:hover .emo{transform:scale(1.15) rotate(-5deg)}
.item .nm{font-size:14px;font-weight:700;color:var(--text);display:block;letter-spacing:-.2px}
.item .qt{font-size:12px;color:var(--text3);display:block;margin-top:3px}
.item .pr{font-family:'Space Grotesk',sans-serif;font-size:16px;color:var(--accent);font-weight:700;margin-top:8px;display:block}
.results{animation:fadeUp .4s ease-out}
.product{margin-bottom:18px;padding:22px;background:var(--card);border-radius:var(--radius);border:1.5px solid var(--border);box-shadow:var(--shadow-sm);animation:scaleIn .3s ease-out;transition:box-shadow .3s}
.product:hover{box-shadow:var(--shadow-md)}
.product h3{font-family:'Space Grotesk',sans-serif;font-size:20px;font-weight:700;letter-spacing:-.5px;margin-bottom:2px}
.product .qlabel{color:var(--text3);font-size:13px;margin-bottom:14px;font-weight:500}
.price-row{display:flex;justify-content:space-between;align-items:center;padding:12px 14px;margin:4px 0;border-radius:12px;cursor:pointer;transition:all .2s;background:var(--card2);border:1px solid transparent}
.price-row:hover{border-color:var(--accent);background:var(--accent-bg)}
.price-row.best{background:var(--green-bg);border:1.5px solid var(--green)}
.sm-name{font-size:15px;font-weight:600;color:var(--text)}
.pr-info{text-align:right}
.pr-val{font-family:'Space Grotesk',sans-serif;font-weight:700;color:var(--accent);font-size:18px}
.pr-promo{font-size:13px}
.pr-old{text-decoration:line-through;color:var(--text3);margin-right:8px}
.pr-sale{color:var(--red);font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:16px}
.tag{display:inline-block;padding:3px 10px;border-radius:20px;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;margin-left:8px}
.tag-best{background:var(--green);color:#fff}
.tag-sale{background:var(--red);color:#fff}
.promo-exp{font-size:11px;color:var(--red);display:block;margin-top:3px}
.no-results{text-align:center;padding:50px 20px;color:var(--text3)}
.no-results .big{font-size:56px;display:block;margin-bottom:12px}
.scrape-info{text-align:center;font-size:11px;color:var(--text3);margin-top:16px}
.loc-hero{max-width:800px;margin:0 auto 20px;padding:0 20px;animation:fadeUp .5s ease-out .1s both}
.loc-box{background:var(--card);border:1.5px solid var(--border);border-radius:20px;padding:24px;box-shadow:var(--shadow-md);position:relative;overflow:hidden}
.loc-box::before{content:'';position:absolute;right:-30px;top:-30px;width:160px;height:160px;border-radius:50%;background:var(--accent-glow);pointer-events:none}
.loc-box::after{content:'';position:absolute;right:40px;bottom:-40px;width:100px;height:100px;border-radius:50%;background:var(--accent-glow);pointer-events:none}
.loc-header{display:flex;align-items:center;gap:12px;margin-bottom:16px}
.loc-pin-icon{width:44px;height:44px;border-radius:12px;background:var(--accent);display:flex;align-items:center;justify-content:center;flex-shrink:0}
.loc-pin-icon svg{width:22px;height:22px;color:#fff}
.loc-title{font-family:'Space Grotesk',sans-serif;font-size:18px;font-weight:700;color:var(--text);letter-spacing:-.3px}
.loc-subtitle{font-size:13px;color:var(--text3);margin-top:2px}
.loc-input-wrap{position:relative;margin-bottom:16px}
.loc-input{width:100%;padding:14px 18px 14px 44px;border:1.5px solid var(--border);border-radius:14px;font-size:15px;background:var(--card2);color:var(--text);font-family:'DM Sans',sans-serif;outline:none;transition:all .25s}
.loc-input:focus{border-color:var(--accent);background:var(--card);box-shadow:0 0 0 3px var(--accent-glow)}
.loc-input::placeholder{color:var(--text3)}
.loc-input-wrap svg{position:absolute;left:14px;top:50%;transform:translateY(-50%);width:18px;height:18px;color:var(--text3)}
.loc-suggestions{position:absolute;top:100%;left:0;right:0;background:var(--card);border:1px solid var(--border);border-radius:0 0 14px 14px;max-height:200px;overflow-y:auto;z-index:10;display:none;box-shadow:var(--shadow-lg)}
.loc-sug-item{padding:12px 18px;cursor:pointer;font-size:14px;border-bottom:1px solid var(--border);color:var(--text);transition:background .15s}
.loc-sug-item:hover{background:var(--accent-bg)}
.loc-sug-item .loc-zone{color:var(--text3);font-size:11px;display:block;margin-top:2px}
.loc-results{display:grid;gap:12px}
.loc-card{background:var(--card2);border:1.5px solid var(--border);border-radius:14px;padding:16px;display:flex;gap:14px;align-items:flex-start;transition:all .25s;animation:scaleIn .3s ease-out;cursor:pointer}
.loc-card:hover{border-color:var(--accent);background:var(--accent-bg);transform:translateX(4px)}
.loc-icon{width:48px;height:48px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:800;color:#fff;flex-shrink:0;font-family:'Space Grotesk',sans-serif}
.loc-icon.coto{background:linear-gradient(135deg,#e8553a,#f97358)}
.loc-icon.jumbo{background:linear-gradient(135deg,#059669,#34d399)}
.loc-icon.disco{background:linear-gradient(135deg,#7c3aed,#a78bfa)}
.loc-info{flex:1}
.loc-name{font-family:'Space Grotesk',sans-serif;font-size:15px;font-weight:700;color:var(--text);margin-bottom:2px}
.loc-addr{font-size:12px;color:var(--text2);margin-bottom:8px}
.loc-meta{display:flex;gap:8px;flex-wrap:wrap}
.loc-tag{font-size:11px;padding:3px 10px;border-radius:20px;font-weight:600}
.loc-tag.open{background:var(--green-bg);color:var(--green)}
.loc-tag.closed{background:var(--red-bg);color:var(--red)}
.loc-tag.dist{background:var(--card);color:var(--text2);border:1px solid var(--border)}
.loc-tag.hours{background:var(--accent-bg);color:var(--accent)}
.modal-bg{display:none;position:fixed;inset:0;background:rgba(0,0,0,.45);backdrop-filter:blur(6px);z-index:100;justify-content:center;align-items:center;padding:20px}
.modal-bg.on{display:flex}
.modal{background:var(--card);border-radius:20px;padding:30px;max-width:440px;width:100%;box-shadow:var(--shadow-lg);position:relative;animation:scaleIn .25s ease-out;border:1px solid var(--border)}
.modal .mx{position:absolute;top:14px;right:16px;width:34px;height:34px;border-radius:10px;border:1px solid var(--border);background:var(--card2);cursor:pointer;font-size:16px;display:flex;align-items:center;justify-content:center;color:var(--text3);transition:all .15s}
.modal .mx:hover{background:var(--border);color:var(--text)}
.modal h3{font-family:'Space Grotesk',sans-serif;font-size:20px;font-weight:700;margin-bottom:4px}
.modal .msub{font-size:13px;color:var(--text3);margin-bottom:18px}
.mrow{display:flex;justify-content:space-between;padding:12px 0;border-bottom:1px solid var(--border);font-size:14px}
.mrow:last-child{border-bottom:none}
.mlbl{color:var(--text2)}.mval{font-weight:700;color:var(--text)}
.mval.promo{color:var(--red)}.mval.best{color:var(--green)}
.msrc{margin-top:18px;padding:16px;background:var(--card2);border-radius:12px;font-size:12px;color:var(--text2);line-height:1.7;border:1px solid var(--border)}
.msrc strong{color:var(--text);display:block;margin-bottom:4px;font-size:13px}
.toast{position:fixed;bottom:30px;left:50%;transform:translateX(-50%);background:var(--text);color:var(--bg);padding:12px 24px;border-radius:12px;font-size:13px;font-weight:600;z-index:200;display:none;animation:fadeUp .3s ease-out}
.add-btn{padding:6px 14px;border:1.5px solid var(--accent);border-radius:10px;background:var(--accent-bg);color:var(--accent);font-family:'DM Sans',sans-serif;font-size:12px;font-weight:700;cursor:pointer;transition:all .2s;margin-top:8px}
.add-btn:hover{background:var(--accent);color:#fff}
.add-btn.added{background:var(--green);color:#fff;border-color:var(--green)}
.cart-bar{position:fixed;bottom:0;left:0;right:0;background:var(--card);border-top:1.5px solid var(--border);padding:14px 20px;box-shadow:0 -4px 20px rgba(0,0,0,.1);z-index:50;transform:translateY(100%);transition:transform .35s ease-out;display:flex;flex-direction:column;align-items:center;gap:10px}
.cart-bar.show{transform:translateY(0)}
.cart-summary{display:flex;gap:14px;flex-wrap:wrap;justify-content:center;width:100%;max-width:800px}
.cart-store{flex:1;min-width:140px;padding:12px 16px;border-radius:14px;border:1.5px solid var(--border);background:var(--card2);text-align:center;transition:all .2s}
.cart-store.best-store{border-color:var(--green);background:var(--green-bg)}
.cart-store-name{font-size:13px;font-weight:700;color:var(--text);margin-bottom:4px}
.cart-store-total{font-family:'Space Grotesk',sans-serif;font-size:22px;font-weight:700;color:var(--text)}
.cart-store.best-store .cart-store-total{color:var(--green)}
.cart-store-tag{font-size:10px;font-weight:700;text-transform:uppercase;color:var(--green);margin-top:4px;letter-spacing:.5px}
.cart-header{display:flex;align-items:center;justify-content:space-between;width:100%;max-width:800px}
.cart-title{font-family:'Space Grotesk',sans-serif;font-size:16px;font-weight:700;color:var(--text)}
.cart-count{font-size:13px;color:var(--text3)}
.cart-clear{padding:5px 12px;border:1px solid var(--border);border-radius:8px;background:var(--card2);color:var(--red);font-family:'DM Sans',sans-serif;font-size:11px;font-weight:600;cursor:pointer;transition:all .2s}
.cart-clear:hover{background:var(--red-bg);border-color:var(--red)}
.cart-items{display:flex;gap:6px;flex-wrap:wrap;justify-content:center;width:100%;max-width:800px}
.cart-item-pill{padding:4px 10px;border-radius:8px;background:var(--card2);border:1px solid var(--border);font-size:12px;color:var(--text2);display:flex;align-items:center;gap:4px}
.cart-item-pill .cart-x{cursor:pointer;color:var(--text3);font-weight:700;transition:color .15s}
.cart-item-pill .cart-x:hover{color:var(--red)}
@media(max-width:600px){
nav{padding:12px 16px}.hero h1{font-size:28px}.main{padding:0 16px 30px}
.grid{grid-template-columns:repeat(3,1fr);gap:10px}.item{padding:14px 8px}.item .emo{font-size:32px}
.coupon{min-width:200px;padding:16px}.cart-store{min-width:100px;padding:10px}.cart-store-total{font-size:18px}
}
</style>
</head>
<body>
<nav>
  <div class="logo">
    <svg class="logo-svg" viewBox="0 0 420 140" xmlns="http://www.w3.org/2000/svg">
      <line x1="8" y1="30" x2="28" y2="45" stroke="var(--accent)" stroke-width="1.5" opacity=".3"/>
      <line x1="4" y1="72" x2="24" y2="62" stroke="var(--accent)" stroke-width="1.5" opacity=".25"/>
      <line x1="10" y1="105" x2="28" y2="92" stroke="var(--accent)" stroke-width="1.5" opacity=".3"/>
      <line x1="100" y1="10" x2="85" y2="26" stroke="var(--accent)" stroke-width="1.5" opacity=".2"/>
      <line x1="108" y1="45" x2="98" y2="52" stroke="var(--accent)" stroke-width="1.5" opacity=".25"/>
      <circle class="logo-node" cx="8" cy="30" r="2.5" fill="var(--accent)"/>
      <circle class="logo-node" cx="4" cy="72" r="2.5" fill="var(--accent)"/>
      <circle class="logo-node" cx="10" cy="105" r="2.5" fill="var(--accent)"/>
      <circle class="logo-node" cx="100" cy="10" r="2.5" fill="var(--accent)"/>
      <circle class="logo-node" cx="108" cy="45" r="2.5" fill="var(--accent)"/>
      <path d="M62 8A52 52 0 1 0 62 114" fill="none" stroke="var(--accent)" stroke-width="9" stroke-linecap="round"/>
      <line x1="62" y1="61" x2="40" y2="61" stroke="var(--accent)" stroke-width="9" stroke-linecap="round"/>
      <path d="M60 59L100 59 94 96 48 96Z" fill="none" stroke="var(--accent)" stroke-width="3.5" stroke-linejoin="round"/>
      <circle cx="59" cy="108" r="6" fill="none" stroke="var(--accent)" stroke-width="2.5"/>
      <circle cx="86" cy="108" r="6" fill="none" stroke="var(--accent)" stroke-width="2.5"/>
      <rect x="64" y="69" width="17" height="17" rx="2.5" fill="none" stroke="var(--accent)" stroke-width="1.5" opacity=".8"/>
      <line class="logo-pin" x1="70" y1="69" x2="70" y2="65" stroke="var(--accent)" stroke-width="1.2" opacity=".5"/>
      <line class="logo-pin" x1="77" y1="69" x2="77" y2="65" stroke="var(--accent)" stroke-width="1.2" opacity=".5"/>
      <line class="logo-pin" x1="64" y1="76" x2="60" y2="76" stroke="var(--accent)" stroke-width="1.2" opacity=".5"/>
      <line class="logo-pin" x1="64" y1="81" x2="60" y2="81" stroke="var(--accent)" stroke-width="1.2" opacity=".5"/>
      <line class="logo-pin" x1="81" y1="76" x2="85" y2="76" stroke="var(--accent)" stroke-width="1.2" opacity=".5"/>
      <line class="logo-pin" x1="81" y1="81" x2="85" y2="81" stroke="var(--accent)" stroke-width="1.2" opacity=".5"/>
      <line class="logo-pin" x1="70" y1="86" x2="70" y2="90" stroke="var(--accent)" stroke-width="1.2" opacity=".5"/>
      <line class="logo-pin" x1="77" y1="86" x2="77" y2="90" stroke="var(--accent)" stroke-width="1.2" opacity=".5"/>
      <circle class="logo-core" cx="73" cy="78" r="3" fill="var(--accent)" opacity=".7"/>
      <text x="125" y="55" style="font-family:'Space Grotesk',sans-serif;font-size:30px;font-weight:700;letter-spacing:-1px" fill="var(--text)">Grocery</text>
      <text x="262" y="55" style="font-family:'Space Grotesk',sans-serif;font-size:30px;font-weight:700;letter-spacing:-1px" fill="var(--accent)">Finder</text>
      <text x="125" y="76" style="font-family:'DM Sans',sans-serif;font-size:10px;font-weight:700;letter-spacing:2px" fill="var(--accent)" opacity=".6">AI-POWERED PRICE COMPARISON</text>
      <text x="125" y="96" style="font-family:'DM Sans',sans-serif;font-size:11px" fill="var(--text3)">Buenos Aires, Argentina</text>
    </svg>
  </div>
  <div class="controls">
    <select class="nav-cur" id="nav-cur" onchange="changeCur(this.value)">
      <option value="">ARS $</option>
      <option value="USD">+ USD</option><option value="EUR">+ EUR</option><option value="BRL">+ BRL</option>
      <option value="GBP">+ GBP</option><option value="CLP">+ CLP</option><option value="UYU">+ UYU</option>
      <option value="MXN">+ MXN</option><option value="JPY">+ JPY</option><option value="CNY">+ CNY</option>
    </select>
    <div class="pill-toggle">
      <button class="pill-btn active" id="btn-es" onclick="setLang('es')">ES</button>
      <button class="pill-btn" id="btn-en" onclick="setLang('en')">EN</button>
    </div>
    <button class="theme-btn" id="theme-btn" onclick="toggleTheme()">☀️</button>
  </div>
</nav>
<div class="hero">
  <h1 data-es="Encontrá el <em>mejor precio</em> para tu compra" data-en="Find the <em>best price</em> for your groceries" class="i18n-html" id="hero-title"></h1>
  <p data-es="Compará Coto, Jumbo y Disco al instante" data-en="Compare Coto, Jumbo and Disco instantly" class="i18n"></p>
</div>
<div class="loc-hero">
  <div class="loc-box">
    <div class="loc-header">
      <div class="loc-pin-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/><circle cx="12" cy="9" r="2.5"/></svg></div>
      <div>
        <div class="loc-title i18n" data-es="Supermercados cerca tuyo" data-en="Supermarkets near you" id="loc-title-text"></div>
        <div class="loc-subtitle i18n" data-es="Escribí tu barrio y encontrá la sucursal más cercana" data-en="Type your neighborhood to find the nearest store"></div>
      </div>
    </div>
    <div class="loc-input-wrap">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><line x1="16.5" y1="16.5" x2="21" y2="21"/></svg>
      <input class="loc-input" type="text" id="loc-input" autocomplete="off"/>
      <div class="loc-suggestions" id="loc-sug"></div>
    </div>
    <div class="loc-results" id="loc-results"></div>
  </div>
</div>
<div class="main">
  <div class="search-wrap">
    <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><line x1="16.5" y1="16.5" x2="21" y2="21"/></svg>
    <input type="text" id="search" autocomplete="off"/>
    <div class="autocomplete-list" id="autocomplete"></div>
  </div>
  <div class="coupons">
    <div class="coupons-title i18n" data-es="Cupones disponibles" data-en="Available coupons" id="coup-title"></div>
    <div class="coupons-scroll" id="coup-scroll"></div>
  </div>
  <div class="cats" id="cats">
    <button class="cat active" onclick="filtrarCat('todos')" data-es="Todos" data-en="All" class="i18n"></button>
    <button class="cat" onclick="filtrarCat('lácteos')"><span data-es="🥛 Lácteos" data-en="🥛 Dairy" class="i18n"></span></button>
    <button class="cat" onclick="filtrarCat('frutas')"><span data-es="🍎 Frutas" data-en="🍎 Fruits" class="i18n"></span></button>
    <button class="cat" onclick="filtrarCat('carnes')"><span data-es="🥩 Carnes" data-en="🥩 Meats" class="i18n"></span></button>
    <button class="cat" onclick="filtrarCat('almacén')"><span data-es="🏪 Almacén" data-en="🏪 Pantry" class="i18n"></span></button>
    <button class="cat" onclick="filtrarCat('bebidas')"><span data-es="🥤 Bebidas" data-en="🥤 Drinks" class="i18n"></span></button>
    <button class="cat" onclick="filtrarCat('limpieza')"><span data-es="🧹 Limpieza" data-en="🧹 Cleaning" class="i18n"></span></button>
  </div>
  <div id="home">
    <div class="sec-title i18n" data-es="Productos disponibles" data-en="Available products" id="prod-title"></div>
    <div class="grid" id="grid"></div>
  </div>
  <div id="results" class="results"></div>
  <div class="scrape-info" id="scrape-info"></div>
</div>
<div class="modal-bg" id="modal-bg" onclick="closeModal(event)">
  <div class="modal"><button class="mx" onclick="closeModal()">&times;</button><div id="modal-c"></div></div>
</div>
<div class="cart-bar" id="cart-bar">
  <div class="cart-header">
    <div><span class="cart-title" id="cart-title"></span> <span class="cart-count" id="cart-count"></span></div>
    <button class="cart-clear" onclick="clearCart()" id="cart-clear-btn"></button>
  </div>
  <div class="cart-items" id="cart-items"></div>
  <div class="cart-summary" id="cart-summary"></div>
</div>
<div class="toast" id="toast"></div>
<script>
let AP=[],lang='es',dark=false,selCur='',cart=[];
const XR={USD:{r:1200,s:'US$'},EUR:{r:1300,s:'€'},BRL:{r:230,s:'R$'},GBP:{r:1520,s:'£'},CLP:{r:1.28,s:'CL$'},UYU:{r:28,s:'UY$'},MXN:{r:70,s:'MX$'},JPY:{r:7.8,s:'¥'},CNY:{r:165,s:'¥'}};
function cv(a){if(!selCur)return '';const c=XR[selCur];return `<span class="cur-eq">${c.s}${(a/c.r).toFixed(2)}</span>`}
function cvi(a){if(!selCur)return '';const c=XR[selCur];return `<span class="cur-eq-i">(${c.s}${(a/c.r).toFixed(2)})</span>`}
function cvModal(a){if(!selCur)return 'ARS $'+a;const c=XR[selCur];return `${c.s}${(a/c.r).toFixed(2)} ${selCur}`}
function changeCur(v){selCur=v;if(AP.length)showPop(AP);const q=document.getElementById('search').value.trim();if(q)buscar()}
const T={
es:{desde:'Desde',ph:'¿Qué producto buscás?',nr1:'No encontramos',nr2:'Probá con otro término',na:'No hay resultados para',upd:'Precios actualizados',rp:'Precio regular',pp:'Precio promocional',sav:'Ahorro',pe:'Promo vence',days:'días',exp:'Vencida',verd:'Veredicto',bp:'Mejor precio disponible',st:'Datos del scraping',src:'Fuente',ed:'Fecha de extracción',meth:'Método',as:'Scraping automático',prod:'Producto',nd:'No disponible',cheap:'MÁS BARATO',offer:'OFERTA',expires:'Vence',cc:'Cupón copiado',ct:'Cupones disponibles',pt:'Productos disponibles',off:'OFF',vu:'Válido hasta',cm:'Compra mín.',onl:'Online'},
en:{desde:'From',ph:'What are you looking for?',nr1:'We couldn\\'t find',nr2:'Try another term',na:'No results for',upd:'Prices updated',rp:'Regular price',pp:'Promo price',sav:'Savings',pe:'Promo expires',days:'days',exp:'Expired',verd:'Verdict',bp:'Best price available',st:'Scraping data',src:'Source',ed:'Extraction date',meth:'Method',as:'Auto website scraping',prod:'Product',nd:'Not available',cheap:'CHEAPEST',offer:'SALE',expires:'Expires',cc:'Coupon copied',ct:'Available coupons',pt:'Available products',off:'OFF',vu:'Valid until',cm:'Min. purchase',onl:'Online'}
};
function t(k){return T[lang][k]||k}
function toggleTheme(){dark=!dark;document.documentElement.setAttribute('data-theme',dark?'dark':'');document.getElementById('theme-btn').textContent=dark?'🌙':'☀️'}
const coups=[
{store:'Coto',cls:'coupon-coto',disc:'15%',des:'en Lácteos',den:'on Dairy',code:'COTO15LAC',min:'$5.000',exp:7},
{store:'Jumbo',cls:'coupon-jumbo',disc:'20%',des:'en Frutas',den:'on Fruits',code:'JUMBO20FRU',min:'$3.000',exp:5},
{store:'Disco',cls:'coupon-disco',disc:'10%',des:'en todo',den:'on everything',code:'DISCO10ALL',min:'$8.000',exp:10},
{store:'Coto',cls:'coupon-coto',disc:'25%',des:'en Bebidas',den:'on Drinks',code:'COTO25BEB',min:'$2.000',exp:3},
{store:'Jumbo',cls:'coupon-jumbo',disc:'2x1',des:'en Limpieza',den:'on Cleaning',code:'JUMBO2X1CL',min:'$4.000',exp:12}
];
function renderCoups(){const s=document.getElementById('coup-scroll'),now=new Date();s.innerHTML=coups.map(c=>{const e=new Date(now.getTime()+c.exp*864e5).toLocaleDateString(lang==='es'?'es-AR':'en-US',{day:'numeric',month:'short'});return `<div class="coupon ${c.cls}" onclick="copyCoup('${c.code}')"><div class="blob blob1"></div><div class="blob blob2"></div><div class="store">${c.store}</div><div class="disc">${c.disc} ${t('off')}</div><div class="cdesc">${lang==='es'?c.des:c.den}</div><div class="ccode">${c.code}</div><div class="cexp">${t('vu')} ${e} · ${t('cm')} ${c.min}</div></div>`}).join('')}
function copyCoup(c){navigator.clipboard.writeText(c).then(()=>{const e=document.getElementById('toast');e.textContent='✅ '+t('cc')+': '+c;e.style.display='block';setTimeout(()=>e.style.display='none',2e3)})}
function setLang(l){lang=l;document.getElementById('btn-es').classList.toggle('active',l==='es');document.getElementById('btn-en').classList.toggle('active',l==='en');document.querySelectorAll('.i18n').forEach(e=>{if(e.dataset[l])e.textContent=e.dataset[l]});document.querySelectorAll('.i18n-html').forEach(e=>{if(e.dataset[l])e.innerHTML=e.dataset[l]});document.getElementById('search').placeholder=t('ph');document.getElementById('coup-title').textContent=t('ct');document.getElementById('prod-title').textContent=t('pt');const cct=document.getElementById('cur-chip-text');if(cct)cct.textContent=cct.dataset[l];renderCoups();if(AP.length)showPop(AP)}
async function loadProds(){try{const r=await fetch('/api/products');AP=await r.json();showPop(AP)}catch(e){console.error(e)}}
const EM={'Leche Entera':'🥛','Yogur Natural':'🥛','Naranjas':'🍊','Huevos':'🥚','Queso Cremoso':'🧀','Manteca':'🧈','Pan Lactal':'🍞','Arroz':'🍚','Fideos Secos':'🍝','Aceite de Girasol':'🫒','Azúcar':'🍬','Harina':'🌾','Galletitas Dulces':'🍪','Gaseosa Cola':'🥤','Agua Mineral':'💧','Papel Higiénico':'🧻','Detergente':'🧴','Jabón en Polvo':'🧼','Pollo Entero':'🍗','Carne Picada':'🥩','Banana':'🍌','Tomate':'🍅','Papa':'🥔','Cebolla':'🧅'};
function showPop(ps){document.getElementById('grid').innerHTML=ps.map((p,i)=>{const inCart=cart.includes(p.nombre);return `<div class="item" style="animation-delay:${i*40}ms;animation:fadeUp .4s ease-out ${i*40}ms both"><span class="emo" onclick="pickProd('${p.nombre}')">${EM[p.nombre]||'🛒'}</span><span class="nm" onclick="pickProd('${p.nombre}')">${p.nombre}</span><span class="qt">${p.cantidad}</span><span class="pr">${t('desde')} $${p.precio_min}${cvi(p.precio_min)}</span><button class="add-btn ${inCart?'added':''}" id="add-${p.nombre.replace(/\\s/g,'_')}" onclick="event.stopPropagation();addToCart('${p.nombre}')">${inCart?'✓':'+'}</button></div>`}).join('')}
function pickProd(n){document.getElementById('search').value=n;buscar()}
function filtrarCat(c){document.querySelectorAll('.cat').forEach(b=>b.classList.remove('active'));event.target.closest('.cat').classList.add('active');const cs={'lácteos':['Leche Entera','Yogur Natural','Queso Cremoso','Manteca'],'frutas':['Naranjas','Banana','Tomate','Papa','Cebolla'],'carnes':['Pollo Entero','Carne Picada','Huevos'],'almacén':['Pan Lactal','Arroz','Fideos Secos','Aceite de Girasol','Azúcar','Harina','Galletitas Dulces'],'bebidas':['Gaseosa Cola','Agua Mineral'],'limpieza':['Papel Higiénico','Detergente','Jabón en Polvo']};showPop(c==='todos'?AP:AP.filter(p=>cs[c]?.includes(p.nombre)));document.getElementById('home').style.display='block';document.getElementById('results').innerHTML=''}
const si=document.getElementById('search'),al=document.getElementById('autocomplete');
si.addEventListener('input',function(){const q=this.value.toLowerCase().trim();if(q.length<1){al.style.display='none';return}const m=AP.filter(p=>p.nombre.toLowerCase().includes(q));if(!m.length){al.innerHTML=`<div class="autocomplete-item" style="color:var(--text3)">${t('na')} "${q}"</div>`;al.style.display='block';return}al.innerHTML=m.map(p=>`<div class="autocomplete-item" onclick="pickProd('${p.nombre}')">${p.nombre} <span class="qty">${p.cantidad}</span></div>`).join('');al.style.display='block'});
document.addEventListener('click',e=>{if(!e.target.closest('.search-wrap'))al.style.display='none'});
async function buscar(){al.style.display='none';const q=si.value.trim();if(!q)return;document.getElementById('home').style.display='none';try{const r=await fetch(`/api/search?q=${encodeURIComponent(q)}`);const data=await r.json();let h='',fs='';if(!Object.keys(data).length){h=`<div class="no-results"><span class="big">🔍</span><p><strong>${t('nr1')}</strong> "${q}"</p><p style="margin-top:8px;font-size:14px;color:var(--text3)">${t('nr2')}</p></div>`;document.getElementById('home').style.display='block'}for(const[prod,info]of Object.entries(data)){const ps=info.precios,best=Math.min(...ps.map(p=>p.precio_final));h+=`<div class="product"><h3>${prod}</h3><div class="qlabel">${info.cantidad}</div>`;for(const p of ps){const ib=p.precio_final===best,cls=ib?'best':'';const md=encodeURIComponent(JSON.stringify({producto:prod,cantidad:info.cantidad,supermarket:p.supermarket,precio:p.precio,precio_promo:p.precio_promo,precio_final:p.precio_final,promo_vence:p.promo_vence,fecha_scraping:p.fecha_scraping,esMejor:ib}));let ph='';if(p.precio_promo){ph=`<span class="pr-promo"><span class="pr-old">$${p.precio}</span><span class="pr-sale">$${p.precio_promo}</span><span class="tag tag-sale">${t('offer')}</span></span>${cv(p.precio_promo)}`;if(p.promo_vence)ph+=`<span class="promo-exp">${t('expires')}: ${fmtD(p.promo_vence)}</span>`}else{ph=`<span class="pr-val">$${p.precio}</span>${cv(p.precio)}`}h+=`<div class="price-row ${cls}" onclick="openModal('${md}')"><span class="sm-name">🏪 ${p.supermarket}</span><div class="pr-info">${ph}${ib?`<span class="tag tag-best">${t('cheap')}</span>`:''}</div></div>`;if(p.fecha_scraping)fs=p.fecha_scraping}h+=`</div>`}document.getElementById('results').innerHTML=h;if(fs)document.getElementById('scrape-info').innerHTML=`${t('upd')}: ${fmtD(fs)}`}catch(e){document.getElementById('results').innerHTML='<p>Error</p>'}}
function fmtD(d){return new Date(d+'T00:00:00').toLocaleDateString(lang==='es'?'es-AR':'en-US',{day:'numeric',month:'long',year:'numeric'})}
si.addEventListener('keypress',e=>{if(e.key==='Enter')buscar()});
function openModal(ed){const d=JSON.parse(decodeURIComponent(ed));const pF=d.precio_promo||d.precio;let h=`<h3>🏪 ${d.supermarket}</h3><div class="msub">${d.producto} — ${d.cantidad}</div><div class="mrow"><span class="mlbl">${t('rp')}</span><span class="mval">$${d.precio}</span></div>`;if(d.precio_promo){h+=`<div class="mrow"><span class="mlbl">${t('pp')}</span><span class="mval promo">$${d.precio_promo}</span></div><div class="mrow"><span class="mlbl">${t('sav')}</span><span class="mval promo">-$${d.precio-d.precio_promo} (${Math.round((1-d.precio_promo/d.precio)*100)}%)</span></div>`;if(d.promo_vence){const dias=Math.ceil((new Date(d.promo_vence+'T00:00:00')-new Date())/864e5);h+=`<div class="mrow"><span class="mlbl">${t('pe')}</span><span class="mval promo">${fmtD(d.promo_vence)} (${dias>0?dias+' '+t('days'):t('exp')})</span></div>`}}if(d.esMejor)h+=`<div class="mrow"><span class="mlbl">${t('verd')}</span><span class="mval best">✅ ${t('bp')}</span></div>`;h+=`<div class="modal-cur"><div class="modal-cur-title">${lang==='es'?'Equivalencia en otra moneda':'Currency equivalent'}</div><div class="modal-cur-row"><select class="modal-cur-sel" onchange="selCur=this.value;document.getElementById('mcv').textContent=cvModal(${pF})"><option value="USD">USD $</option><option value="EUR">EUR €</option><option value="BRL">BRL R$</option><option value="GBP">GBP £</option><option value="CLP">CLP</option><option value="UYU">UYU</option><option value="MXN">MXN</option><option value="JPY">JPY ¥</option><option value="CNY">CNY ¥</option></select><span class="modal-cur-val" id="mcv">${cvModal(pF)}</span></div></div>`;h+=`<div class="msrc"><strong>📊 ${t('st')}</strong>${t('src')}: ${d.supermarket} ${t('onl')}<br>${t('ed')}: ${d.fecha_scraping?fmtD(d.fecha_scraping):t('nd')}<br>${t('meth')}: ${t('as')}<br>${t('prod')}: ${d.producto} (${d.cantidad})</div>`;document.getElementById('modal-c').innerHTML=h;document.getElementById('modal-bg').classList.add('on')}
function closeModal(e){if(!e||e.target===document.getElementById('modal-bg')||e.target.classList.contains('mx'))document.getElementById('modal-bg').classList.remove('on')}
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeModal()});
function addToCart(nombre){if(cart.includes(nombre))return;cart.push(nombre);updateCart();const btn=document.getElementById('add-'+nombre.replace(/\s/g,'_'));if(btn){btn.textContent='✓';btn.classList.add('added')}}
function removeFromCart(nombre){cart=cart.filter(n=>n!==nombre);updateCart();const btn=document.getElementById('add-'+nombre.replace(/\s/g,'_'));if(btn){btn.textContent='+';btn.classList.remove('added')}}
function clearCart(){cart=[];updateCart();document.querySelectorAll('.add-btn.added').forEach(b=>{b.textContent='+';b.classList.remove('added')})}
function updateCart(){const bar=document.getElementById('cart-bar');if(!cart.length){bar.classList.remove('show');return}bar.classList.add('show');document.getElementById('cart-title').textContent=lang==='es'?'Tu lista':'Your list';document.getElementById('cart-count').textContent=`(${cart.length} ${lang==='es'?'productos':'items'})`;document.getElementById('cart-clear-btn').textContent=lang==='es'?'Vaciar':'Clear';document.getElementById('cart-items').innerHTML=cart.map(n=>`<div class="cart-item-pill">${n} <span class="cart-x" onclick="removeFromCart('${n}')">✕</span></div>`).join('');calcCartTotals()}
function calcCartTotals(){const stores={Coto:0,Jumbo:0,Disco:0};cart.forEach(nombre=>{const p=AP.find(x=>x.nombre===nombre);if(!p)return;fetch(`/api/search?q=${encodeURIComponent(nombre)}`).then(r=>r.json()).then(data=>{for(const[prod,info]of Object.entries(data)){for(const pr of info.precios){const pf=pr.precio_promo||pr.precio;if(stores[pr.supermarket]!==undefined)stores[pr.supermarket]+=pf}}renderCartTotals(stores)})});if(!cart.length)renderCartTotals(stores)}
function renderCartTotals(stores){const best=Math.min(...Object.values(stores).filter(v=>v>0));const sum=document.getElementById('cart-summary');sum.innerHTML=Object.entries(stores).map(([name,total])=>{const isBest=total===best&&total>0;return `<div class="cart-store ${isBest?'best-store':''}"><div class="cart-store-name">🏪 ${name}</div><div class="cart-store-total">$${total.toLocaleString('es-AR')}</div>${isBest?`<div class="cart-store-tag">${lang==='es'?'Mejor opción':'Best option'}</div>`:''}</div>`}).join('')}
setLang('es');loadProds();renderCoups();

const STORES=[
{name:'Coto',cls:'coto',letter:'C',stores:[
{addr:'Av. Cabildo 2571, Belgrano',barrios:['Belgrano','Nuñez','Colegiales'],hours:'8:00 - 22:00',dist:'0.4 km'},
{addr:'Av. Rivadavia 5150, Caballito',barrios:['Caballito','Flores','Almagro'],hours:'8:00 - 22:00',dist:'0.6 km'},
{addr:'Av. Corrientes 3247, Abasto',barrios:['Balvanera','Abasto','Once','Almagro'],hours:'8:00 - 22:00',dist:'0.5 km'},
{addr:'Av. Directorio 2820, Parque Chacabuco',barrios:['Parque Chacabuco','Boedo','Caballito'],hours:'8:00 - 21:30',dist:'0.7 km'},
{addr:'Av. Córdoba 5650, Palermo',barrios:['Palermo','Villa Crespo','Chacarita'],hours:'8:00 - 22:00',dist:'0.3 km'},
{addr:'Av. Juan B. Justo 3563, Villa Crespo',barrios:['Villa Crespo','Palermo','Chacarita'],hours:'8:00 - 22:00',dist:'0.5 km'},
]},
{name:'Jumbo',cls:'jumbo',letter:'J',stores:[
{addr:'Av. Bullrich 345, Palermo',barrios:['Palermo','Recoleta','Belgrano'],hours:'9:00 - 21:30',dist:'0.8 km'},
{addr:'Av. Rivadavia 7550, Flores',barrios:['Flores','Floresta','Caballito'],hours:'9:00 - 21:00',dist:'1.2 km'},
{addr:'Av. Santa Fe 1860, Recoleta',barrios:['Recoleta','Barrio Norte','Retiro'],hours:'9:00 - 21:30',dist:'0.6 km'},
{addr:'Av. Corrientes 5559, Villa Crespo',barrios:['Villa Crespo','Chacarita','Almagro'],hours:'9:00 - 21:00',dist:'0.9 km'},
]},
{name:'Disco',cls:'disco',letter:'D',stores:[
{addr:'Av. Libertador 2475, Recoleta',barrios:['Recoleta','Palermo','Retiro','Barrio Norte'],hours:'8:30 - 21:00',dist:'0.5 km'},
{addr:'Av. Cabildo 1550, Belgrano',barrios:['Belgrano','Nuñez','Colegiales'],hours:'8:30 - 21:00',dist:'0.7 km'},
{addr:'Av. Acoyte 440, Caballito',barrios:['Caballito','Almagro','Boedo'],hours:'8:30 - 21:00',dist:'0.4 km'},
{addr:'Av. Scalabrini Ortiz 3178, Palermo',barrios:['Palermo','Villa Crespo'],hours:'8:30 - 21:00',dist:'0.6 km'},
]}
];

const BARRIOS=['Belgrano','Nuñez','Colegiales','Palermo','Recoleta','Barrio Norte','Retiro','Caballito','Flores','Floresta','Almagro','Balvanera','Abasto','Once','Boedo','Parque Chacabuco','Villa Crespo','Chacarita','San Telmo','La Boca','Monserrat','San Nicolás','Puerto Madero','Devoto','Villa Urquiza','Saavedra','Liniers','Mataderos','Villa Lugano','Pompeya'];

document.getElementById('loc-input').placeholder=lang==='es'?'Escribí tu barrio...':'Type your neighborhood...';

const locInput=document.getElementById('loc-input'),locSug=document.getElementById('loc-sug');
locInput.addEventListener('input',function(){const q=this.value.toLowerCase().trim();if(q.length<2){locSug.style.display='none';return}const m=BARRIOS.filter(b=>b.toLowerCase().includes(q));if(!m.length){locSug.innerHTML=`<div class="loc-sug-item" style="color:var(--text3)">${lang==='es'?'No encontramos ese barrio':'Neighborhood not found'}</div>`;locSug.style.display='block';return}locSug.innerHTML=m.map(b=>`<div class="loc-sug-item" onclick="selectBarrio('${b}')">${b}<span class="loc-zone">Buenos Aires, CABA</span></div>`).join('');locSug.style.display='block'});
document.addEventListener('click',e=>{if(!e.target.closest('.loc-input-wrap'))locSug.style.display='none'});

function selectBarrio(b){locInput.value=b;locSug.style.display='none';const results=[];STORES.forEach(s=>{s.stores.forEach(st=>{if(st.barrios.some(br=>br.toLowerCase()===b.toLowerCase())){results.push({name:s.name,cls:s.cls,letter:s.letter,addr:st.addr,hours:st.hours,dist:st.dist})}})});results.sort((a,b)=>parseFloat(a.dist)-parseFloat(b.dist));const now=new Date().getHours();const lr=document.getElementById('loc-results');if(!results.length){lr.innerHTML=`<div style="text-align:center;padding:20px;color:var(--text3)">${lang==='es'?'No hay sucursales cercanas en '+b:'No nearby stores in '+b}</div>`;return}lr.innerHTML=results.map(r=>{const open=now>=8&&now<21;return `<div class="loc-card"><div class="loc-icon ${r.cls}">${r.letter}</div><div class="loc-info"><div class="loc-name">${r.name}</div><div class="loc-addr">${r.addr}</div><div class="loc-meta"><span class="loc-tag ${open?'open':'closed'}">${open?(lang==='es'?'Abierto':'Open'):(lang==='es'?'Cerrado':'Closed')}</span><span class="loc-tag hours">${r.hours}</span><span class="loc-tag dist">${r.dist}</span></div></div></div>`}).join('')}
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
