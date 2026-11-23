import re


def check_message(text):
    if not text or len(text.strip()) < 5:
        return "Safe", 0.0

    msg = text.lower()

    # --- LAYER 1: THE "IMMOVABLE" SAFE LIST (100% SAFE) ---
    # These keywords represent official Indian academic & career communications.
    trusted_entities = [
        'nptel', 'iitm', 'swayam', 'infosys', 'hackwithinfy',
        'tcs', 'otp', 'exam', 'hall ticket', 'admit card',
        'placement office', 'placement cell', 'verification code'
    ]

    if any(entity in msg for entity in trusted_entities):
        return "Safe", 0.0  # Force 0% Spam

    # --- LAYER 2: THE "DEFINITIVE" SPAM SIGNALS (100% SPAM) ---
    # We look for the "DNA" of a mass-marketing blast.

    # 1. Marketing Intent (Subjects/Promos)
    has_marketing_subject = bool(
        re.search(r'(mba|internship|career|brochure|offer|prize|bonus|3\.0|4\.0|omni|fidelity|redefining)', msg))

    # 2. Call to Action (Links/Buttons)
    has_cta = bool(
        re.search(r'(try now|try \w+|know more|download|click here|join the|register|forms\.gle|bit\.ly)', msg))

    # 3. Bulk Signatures (The "To: Everyone" Footer)
    is_bulk = bool(re.search(r'(creators|users|community|team|best, the|unsubscribe|opt-out|mailing list)', msg))

    # --- FINAL LOGIC ---
    # If it looks like a Product Launch (Hype + Link) OR Bulk Marketing (Unsubscribe + Link)
    if (has_marketing_subject and has_cta) or (is_bulk and has_cta):
        return "Spam", 100.0

    # If it has a suspicious external form link but didn't match the Whitelist
    if re.search(r'forms\.gle', msg):
        return "Spam", 100.0

    # Default Fallback: If it doesn't match a Spam Rule, it's Safe.
    return "Safe", 0.0