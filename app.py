import os
from flask import Flask, request, render_template_string
import redis

app = Flask(__name__)


redis_host = os.environ.get('REDIS_HOST', 'redis')
redis_port = int(os.environ.get('REDIS_PORT', 6379))

redis_password = None
redis_password_file_path = os.environ.get('REDIS_PASSWORD_FILE')

if redis_password_file_path:

    with open(redis_password_file_path, 'r') as f:
        redis_password = f.read().strip()
else:
 
    redis_password = os.environ.get('REDIS_PASSWORD')


try:
    r = redis.Redis(host=redis_host, port=redis_port, password=redis_password, db=0, decode_responses=True)
    
    r.ping()
    redis_status = "Tersambung ke Redis"
except Exception as e:
    r = None
    redis_status = f"Gagal tersambung ke Redis: {e}"


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ALIF DOCKER SECRET</title>
    <style>
        /* --- General Setup & Background --- */
        body {
            background-color: #000;
            color: #0f0;
            font-family: 'Courier New', Courier, monospace;
            margin: 0;
            padding: 0;
            overflow: hidden; /* Sembunyikan scrollbar */
        }
        canvas#matrix-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1; /* Letakkan di paling belakang */
        }
        /* --- Main Content Box (Terminal Window) --- */
        .container {
            max-width: 700px;
            margin: 5vh auto;
            padding: 25px;
            background: rgba(0, 20, 0, 0.85); /* Latar belakang semi-transparan */
            border: 2px solid #0f0;
            box-shadow: 0 0 15px #0f0;
            border-radius: 5px;
            position: relative;
            z-index: 1;
            animation: fadeIn 1s ease-in-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        /* --- Typography & Links --- */
        h2, h3 {
            color: #0f0;
            text-shadow: 0 0 5px #0f0;
            border-bottom: 1px solid #0a0;
            padding-bottom: 10px;
            letter-spacing: 2px;
        }
        h2::before {
            content: 'root@docker:~$ ';
        }
        p {
            line-height: 1.6;
        }
        /* --- Connection Status --- */
        .status {
            font-weight: bold;
            padding: 3px 8px;
            border-radius: 3px;
        }
        .status.ok {
            color: #0f0;
            background-color: rgba(0, 255, 0, 0.1);
        }
        .status.error {
            color: #f00;
            background-color: rgba(255, 0, 0, 0.2);
            text-shadow: 0 0 5px #f00;
        }
        /* --- Form Elements --- */
        form {
            margin-top: 20px;
        }
        input[type=text] {
            background: transparent;
            border: 1px solid #0f0;
            color: #0f0;
            padding: 10px;
            width: calc(100% - 115px); /* Lebar input dikurangi lebar tombol */
            font-family: 'Courier New', Courier, monospace;
            font-size: 1em;
            margin-right: 10px;
            caret-color: #0f0; /* Warna kursor ketik */
            transition: box-shadow 0.3s;
        }
        input[type=text]:focus {
            outline: none;
            box-shadow: 0 0 8px #0f0;
        }
        input[type=submit] {
            background-color: #0f0;
            border: 1px solid #0f0;
            color: #000;
            padding: 10px 15px;
            font-family: 'Courier New', Courier, monospace;
            font-size: 1em;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: bold;
        }
        input[type=submit]:hover {
            background-color: #000;
            color: #0f0;
            box-shadow: 0 0 10px #0f0;
        }
        /* --- Message List --- */
        ul {
            list-style-type: none;
            padding: 0;
            margin-top: 20px;
            max-height: 300px;
            overflow-y: auto;
            border: 1px solid #0a0;
            padding: 10px;
        }
        /* Custom scrollbar untuk message list */
        ul::-webkit-scrollbar {
            width: 8px;
        }
        ul::-webkit-scrollbar-track {
            background: rgba(0, 20, 0, 0.85);
        }
        ul::-webkit-scrollbar-thumb {
            background-color: #0f0;
            border-radius: 4px;
        }
        li {
            padding: 8px;
            border-bottom: 1px dashed #0a0;
            word-wrap: break-word; /* Agar teks panjang tidak merusak layout */
        }
        li:last-child {
            border-bottom: none;
        }
        li::before {
            content: '> ';
            color: #0c0;
        }
    </style>
</head>
<body>

    <canvas id="matrix-bg"></canvas>

    <div class="container">
        <h2>Alif Secure Web App wt Docker Secret</h2>
        <p>
            Status Koneksi: <span class="status {{ 'ok' if 'Tersambung' in redis_status else 'error' }}">{{ redis_status }}</span>
        </p>

        <h3>Kirim Pesan Baru ke Redis:</h3>
        <form method="post">
            <input type="text" name="pesan" placeholder="SISTEM.INPUT_BARU " required autocomplete="off">
            <input type="submit" value="[ Submit ]">
        </form>

        <h3>Log Pesan yang Tersimpan:</h3>
        {% if messages %}
            <ul>
            {% for msg in messages %}
                <li>{{ msg }}</li>
            {% endfor %}
            </ul>
        {% else %}
            <p>> LOG KOSONG... MENUNGGU INPUT BARU...</p>
        {% endif %}
    </div>

    <script>
        const canvas = document.getElementById('matrix-bg');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        const katakana = 'アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴッン';
        const latin = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        const nums = '0123456789';
        const alphabet = katakana + latin + nums;
        const fontSize = 16;
        const columns = canvas.width / fontSize;
        const rainDrops = [];
        for (let x = 0; x < columns; x++) {
            rainDrops[x] = 1;
        }
        const draw = () => {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#0f0';
            ctx.font = fontSize + 'px monospace';
            for (let i = 0; i < rainDrops.length; i++) {
                const text = alphabet.charAt(Math.floor(Math.random() * alphabet.length));
                ctx.fillText(text, i * fontSize, rainDrops[i] * fontSize);
                if (rainDrops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                    rainDrops[i] = 0;
                }
                rainDrops[i]++;
            }
        };
        setInterval(draw, 33);
        window.addEventListener('resize', () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        });
    </script>

</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if r:
        if request.method == 'POST':
            pesan = request.form.get('pesan')
            if pesan:
              
                r.lpush('messages', pesan)
       
        messages = r.lrange('messages', 0, 9)
    else:
        messages = []
    return render_template_string(HTML_TEMPLATE, messages=messages, redis_status=redis_status)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)