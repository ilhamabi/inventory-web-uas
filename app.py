from flask import Flask, render_template, request, redirect, url_for, Response
import sqlite3
import logging
from logging.handlers import RotatingFileHandler
import os
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Monitoring
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Inventory Web App Info', version='1.0.0')

# Logging ke file + stdout
log_dir = os.environ.get('LOG_DIR', '/tmp/app')
log_file = os.path.join(log_dir, 'app.log')

if not os.path.exists(log_dir):
    os.makedirs(log_dir)


# Rotating File Handler
file_handler = RotatingFileHandler(log_file, maxBytes=1000000, backupCount=3)
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
file_handler.setFormatter(file_formatter)

# StreamHandler (stdout) → tetap bisa dilihat di docker logs
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(file_formatter)

# Logger setup
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# Database setup
def init_db():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    logger.info("Akses halaman utama /")
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('SELECT * FROM items')
    items = c.fetchall()
    conn.close()
    return render_template('index.html', items=items)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute('INSERT INTO items (name, quantity) VALUES (?, ?)', (name, quantity))
        conn.commit()
        conn.close()
        logger.info(f"Item ditambahkan: {name}, Jumlah: {quantity}")
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        c.execute('UPDATE items SET name=?, quantity=? WHERE id=?', (name, quantity, id))
        conn.commit()
        conn.close()
        logger.info(f"Item diubah (ID: {id}): {name}, Jumlah: {quantity}")
        return redirect(url_for('index'))
    else:
        c.execute('SELECT * FROM items WHERE id=?', (id,))
        item = c.fetchone()
        conn.close()
        return render_template('edit.html', item=item)

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('DELETE FROM items WHERE id=?', (id,))
    conn.commit()
    conn.close()
    logger.warning(f"Item dihapus (ID: {id})")
    return redirect(url_for('index'))

@app.route('/metrics')
def metrics_custom():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route('/simulate-log')
def simulate_log():
    logger.info("Simulasi log berhasil.")
    logger.warning("Simulasi peringatan log.")
    logger.error("Simulasi error log.")
    return "Log berhasil disimulasikan!"

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', debug=True, port=5000)
