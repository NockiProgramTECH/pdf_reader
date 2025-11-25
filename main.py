"""
Lecteur PDF avec synthèse vocale
Application principale
Auteur: Assistant Claude
"""

import customtkinter as ctk
from pdf_reader_gui import PDFReaderGUI

def main():
    """Point d'entrée principal de l'application"""
    # Configuration du thème
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Création et lancement de l'application
    app = PDFReaderGUI()
    app.mainloop()

if __name__ == "__main__":
    main()