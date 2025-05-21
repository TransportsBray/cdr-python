import socket
import time
from datetime import datetime

HOST = "localhost"
PORT = 3000  # Doit correspondre au port écouté par callvitesse_listener.py

def generate_cdr_line(call_id_suffix):
    """
    Génère une ligne CDR texte conforme au format attendu par le serveur.
    Format : "dd/mm/yy HH:MM:SS, status, caller, callee, duration, ..., Chain: ... "
    On simplifie avec les champs essentiels pour le test.
    """
    now = datetime.now()
    date_str = now.strftime("%d/%m/%y %H:%M:%S")
    status = "TerminatedBySrc"
    caller = f"Ext.{100 + call_id_suffix}"
    callee = f"Ext.{200 + call_id_suffix}"
    duration = 60 + call_id_suffix * 10  # durée en secondes (exemple)
    
    # Pour simplifier on remplit certains champs par défaut avec des virgules (comme dans ton exemple)
    # et on ajoute un champ Chain avec des valeurs fictives.
    chain = f"Ext.{caller}; Ext.{callee};A"
    
    # Ligne formatée CSV + chain
    line = f"{date_str}, {status}, {caller}, {callee}, {duration},,,,,,,,,,,Chain: {chain}\n"
    return line

def send_cdr_line(line):
    """Envoie une ligne texte CDR au serveur via socket."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(line.encode())
            print(f"📤 Ligne CDR envoyée : {line.strip()}")
    except ConnectionRefusedError:
        print("❌ Impossible de se connecter au serveur, vérifier que le listener est lancé.")
    except Exception as e:
        print(f"❌ Erreur lors de l’envoi de la ligne CDR : {e}")

if __name__ == "__main__":
    nombre_envois = 5
    for i in range(1, nombre_envois + 1):
        line = generate_cdr_line(i)
        send_cdr_line(line)
        time.sleep(1)  # Pause 1 seconde entre chaque envoi
