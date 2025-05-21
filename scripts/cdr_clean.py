import re
from datetime import datetime

def clean_chain(chain: str) -> str:
    """
    Nettoie le champ 'chain' en supprimant les répétitions inutiles comme 'Ext.Ext.101'.
    """
    if not isinstance(chain, str):
        return chain
    # Nettoyer les doublons de 'Ext.' et espaces
    chain = re.sub(r'\bExt\.Ext\.', 'Ext.', chain)
    chain = re.sub(r'\s*;\s*', '; ', chain.strip())
    return chain


def clean_timestamp(timestamp_str: str) -> str | None:
    """
    Valide et nettoie un timestamp, retourne au format MySQL (YYYY-MM-DD HH:MM:SS).
    """
    try:
        dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        return None


def clean_duration(duration) -> int | None:
    """
    Nettoie la durée et la convertit en entier. Retourne None si invalide.
    """
    try:
        return int(duration)
    except (ValueError, TypeError):
        return None


def clean_cdr(raw_cdr: dict) -> dict:
    """
    Nettoie un dictionnaire de type CDR avant insertion ou traitement.
    """
    cdr = dict(raw_cdr)  # copie pour ne pas modifier l'original

    # Nettoyage des champs spécifiques
    cdr['chain'] = clean_chain(cdr.get('chain', ''))
    cdr['call_start'] = clean_timestamp(cdr.get('call_start'))
    cdr['call_end'] = clean_timestamp(cdr.get('call_end'))
    cdr['duration'] = clean_duration(cdr.get('duration'))

    return cdr
