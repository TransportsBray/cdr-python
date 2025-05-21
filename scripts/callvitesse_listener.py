import socket
import logging
import threading
from pathlib import Path
from insert_cdr import insert_cdr_entry, init_db
from datetime import datetime, timedelta
from cdr_clean import clean_cdr  # ✅ import nettoyage

Path("logs").mkdir(exist_ok=True)

logging.basicConfig(
    filename="logs/cdr_listener.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8"
)

HOST = "0.0.0.0"
PORT = 3000

def parse_cdr_line(line):
    try:
        parts = line.strip().split(",")
        if len(parts) < 5:
            raise ValueError("Format CDR invalide (trop court)")

        dt_str = parts[0].strip()
        call_start = datetime.strptime(dt_str, "%d/%m/%y %H:%M:%S")

        status = parts[1].strip()
        caller = parts[2].strip()
        callee = parts[3].strip()

        duration_str = parts[4].strip()
        duration = int(duration_str) if duration_str.isdigit() else 0

        chain = ""
        if "Chain:" in line:
            chain = line.split("Chain:")[1].strip()

        cdr_dict = {
            "call_id": f"{caller}_{callee}_{int(call_start.timestamp())}",
            "caller": caller,
            "callee": callee,
            "call_start": call_start.strftime("%Y-%m-%d %H:%M:%S"),
            "call_end": (call_start + timedelta(seconds=duration)).strftime("%Y-%m-%d %H:%M:%S") if duration > 0 else None,
            "duration": duration,
            "call_type": status,
            "status": status,
            "chain": chain
        }
        return cdr_dict
    except Exception as e:
        logging.error(f"Erreur parsing CDR: {e} | Ligne: {line}")
        return None

def handle_client(conn, addr):
    with conn:
        logging.info(f"Connexion acceptée depuis {addr}")
        print(f"✅ Connexion acceptée depuis {addr}")
        buffer = ""
        while True:
            data = conn.recv(4096)
            if not data:
                logging.info(f"Connexion fermée par {addr}")
                print(f"⚠️ Connexion fermée par {addr}")
                break

            buffer += data.decode(errors='ignore')

            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                cdr = parse_cdr_line(line)
                if cdr:
                    try:
                        cleaned_cdr = clean_cdr(cdr)  # ✅ Nettoyage avant insertion
                        insert_cdr_entry(cleaned_cdr)
                        logging.info(f"CDR inséré : {cleaned_cdr}")
                        print(f"📥 CDR reçu : {cleaned_cdr}")
                    except Exception as e:
                        logging.error(f"Erreur insertion CDR : {e}")
                        print(f"❌ Erreur lors de l'insertion : {e}")

def main():
    init_db()
    print(f"🎧 Serveur en écoute sur le port {PORT}...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        logging.info(f"Serveur en écoute sur le port {PORT}")

        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()
            logging.info(f"Thread démarré pour {addr}")

if __name__ == "__main__":
    main()
