from config import MOCK_MODE
from utils.logger import logger

# Adresse I2C par défaut du module LCD avec PCF8574 (souvent 0x27 ou 0x3F)
LCD_I2C_ADDRESS = 0x27
LCD_PORT        = 1       # I2C bus 1 sur Raspberry Pi
LCD_COLS        = 16      # Nombre de colonnes
LCD_ROWS        = 2       # Nombre de lignes


class Lcd:
    """
    Écran LCD 16x2 piloté via I2C avec la librairie RPLCD.
    Compatible avec les modules basés sur PCF8574 (adresse 0x27 ou 0x3F).

    En mode MOCK, les messages sont simplement affichés dans les logs.
    """

    def __init__(self, address=LCD_I2C_ADDRESS, port=LCD_PORT):
        self.address = address
        self.port = port
        self._lcd = None

        if not MOCK_MODE:
            self._init_lcd()

    # ------------------------------------------------------------------
    # Initialisation
    # ------------------------------------------------------------------

    def _init_lcd(self):
        """Initialise l'écran LCD via RPLCD en mode I2C."""
        try:
            from RPLCD.i2c import CharLCD
            self._lcd = CharLCD(
                i2c_expander='PCF8574',
                address=self.address,
                port=self.port,
                cols=LCD_COLS,
                rows=LCD_ROWS,
                dotsize=8,
                charmap='A02',
                auto_linebreaks=False,
                backlight_enabled=True,
            )
            self._lcd.clear()
            logger.info(f"Actuator [LCD]: Écran initialisé (adresse={hex(self.address)}, {LCD_COLS}x{LCD_ROWS})")
        except Exception as e:
            logger.error(f"Actuator [LCD]: Impossible d'initialiser l'écran: {e}")
            self._lcd = None

    # ------------------------------------------------------------------
    # API publique
    # ------------------------------------------------------------------

    def display(self, line1: str, line2: str = ""):
        """
        Affiche deux lignes de texte sur l'écran LCD.
        Chaque ligne est tronquée / complétée à exactement LCD_COLS caractères.

        :param line1: Texte de la première ligne.
        :param line2: Texte de la deuxième ligne (optionnel).
        """
        l1 = self._format_line(line1)
        l2 = self._format_line(line2)

        # Toujours logger en mode mock ET en mode réel (pour le débogage)
        logger.info(f"Actuator [LCD]:\n  +{'-'*LCD_COLS}+\n  |{l1}|\n  |{l2}|\n  +{'-'*LCD_COLS}+")

        if not MOCK_MODE:
            self._write(l1, l2)

    def scroll(self, text: str, delay: float = 1.5):
        """
        Affiche un texte long en faisant défiler page par page (16 caractères / ligne).
        Utile pour les messages qui dépassent 16 caractères.

        :param text: Texte complet à afficher.
        :param delay: Durée d'affichage de chaque page (secondes).

        Exemple :
            lcd.scroll("Bonjour Manuel Comment tu vas toi moi je vais bien")
        """
        import time
        words  = text.split()
        line1  = ""
        line2  = ""

        def flush():
            self.display(line1, line2)
            time.sleep(delay)

        for word in words:
            # Essaie de placer le mot sur line1
            candidate = (line1 + " " + word).strip() if line1 else word
            if len(candidate) <= LCD_COLS:
                line1 = candidate
            else:
                # line1 est pleine, tente line2
                candidate2 = (line2 + " " + word).strip() if line2 else word
                if len(candidate2) <= LCD_COLS:
                    line2 = candidate2
                else:
                    # Les deux lignes sont pleines : affiche et réinitialise
                    flush()
                    line1 = word
                    line2 = ""

        # Affiche le reste
        if line1 or line2:
            flush()

        self.clear()

    def clear(self):
        """Efface l'écran LCD."""
        logger.debug("Actuator [LCD]: Effacement de l'écran.")
        if not MOCK_MODE and self._lcd:
            try:
                self._lcd.clear()
            except Exception as e:
                logger.error(f"Actuator [LCD]: Erreur lors de l'effacement: {e}")

    def backlight(self, enabled: bool):
        """Active ou désactive le rétroéclairage."""
        state = "ON" if enabled else "OFF"
        logger.debug(f"Actuator [LCD]: Rétroéclairage {state}.")
        if not MOCK_MODE and self._lcd:
            try:
                self._lcd.backlight_enabled = enabled
            except Exception as e:
                logger.error(f"Actuator [LCD]: Erreur rétroéclairage: {e}")

    def close(self):
        """Ferme proprement la connexion LCD."""
        if not MOCK_MODE and self._lcd:
            try:
                self._lcd.clear()
                self._lcd.close(clear=True)
                logger.info("Actuator [LCD]: Connexion fermée.")
            except Exception as e:
                logger.error(f"Actuator [LCD]: Erreur lors de la fermeture: {e}")

    # ------------------------------------------------------------------
    # Méthodes privées
    # ------------------------------------------------------------------

    def _format_line(self, text: str) -> str:
        """Formate une chaîne pour qu'elle fasse exactement LCD_COLS caractères."""
        return f"{str(text)[:LCD_COLS]:<{LCD_COLS}}"

    def _write(self, line1: str, line2: str):
        """Écrit les deux lignes sur l'écran physique."""
        if not self._lcd:
            logger.warning("Actuator [LCD]: Écran non initialisé, écriture ignorée.")
            return
        try:
            self._lcd.home()
            self._lcd.write_string(line1)
            self._lcd.cursor_pos = (1, 0)
            self._lcd.write_string(line2)
        except Exception as e:
            logger.error(f"Actuator [LCD]: Erreur d'écriture: {e}")
