"""
Module de traitement des fichiers PDF
Extraction et traitement du texte
"""

import PyPDF2
import re

class PDFProcessor:
    """Classe pour le traitement des fichiers PDF"""
    
    def __init__(self):
        """Initialisation du processeur PDF"""
        pass
        
    def extract_text(self, pdf_path, start_page=None, end_page=None):
        """
        Extrait le texte d'un fichier PDF
        
        Args:
            pdf_path (str): Chemin vers le fichier PDF
            start_page (int, optional): Page de début (1-indexed)
            end_page (int, optional): Page de fin (1-indexed)
            
        Returns:
            str: Texte extrait du PDF
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                
                # Gestion des pages par défaut
                if start_page is None:
                    start_page = 1
                if end_page is None:
                    end_page = total_pages
                    
                # Validation des numéros de pages
                start_page = max(1, min(start_page, total_pages))
                end_page = max(start_page, min(end_page, total_pages))
                
                # Extraction du texte
                text = ""
                for page_num in range(start_page - 1, end_page):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    
                    if page_text:
                        # Nettoyage du texte
                        cleaned_text = self._clean_text(page_text)
                        text += cleaned_text + "\n\n"
                        
                return text.strip()
                
        except Exception as e:
            raise Exception(f"Erreur lors de l'extraction du PDF: {str(e)}")
            
    def get_page_count(self, pdf_path):
        """
        Obtient le nombre total de pages d'un PDF
        
        Args:
            pdf_path (str): Chemin vers le fichier PDF
            
        Returns:
            int: Nombre de pages
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                return len(pdf_reader.pages)
        except Exception as e:
            raise Exception(f"Erreur lors de la lecture du PDF: {str(e)}")
            
    def _clean_text(self, text):
        """
        Nettoie le texte extrait du PDF
        
        Args:
            text (str): Texte brut
            
        Returns:
            str: Texte nettoyé
        """
        # Suppression des sauts de ligne excessifs
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Correction des mots coupés en fin de ligne
        text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)
        
        # Remplacement des sauts de ligne simples par des espaces
        # sauf s'ils sont suivis d'une majuscule (nouveau paragraphe)
        lines = text.split('\n')
        cleaned_lines = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                cleaned_lines.append('')
                continue
                
            # Si la ligne se termine par un signe de ponctuation
            # et la suivante commence par une majuscule, on garde le saut
            if i < len(lines) - 1:
                next_line = lines[i + 1].strip()
                if line and next_line:
                    # Fin de phrase détectée
                    if line[-1] in '.!?:' or next_line[0].isupper():
                        cleaned_lines.append(line)
                    else:
                        # Concaténation avec la ligne suivante
                        cleaned_lines.append(line + ' ')
                else:
                    cleaned_lines.append(line)
            else:
                cleaned_lines.append(line)
                
        text = ''.join(cleaned_lines)
        
        # Nettoyage des espaces multiples
        text = re.sub(r' {2,}', ' ', text)
        
        return text
        
    def detect_language(self, text):
        """
        Détecte la langue du texte (fonction basique)
        
        Args:
            text (str): Texte à analyser
            
        Returns:
            str: Code de langue ('fr', 'en', etc.)
        """
        # Détection simple basée sur des mots courants
        text_lower = text.lower()
        
        # Mots français courants
        french_words = ['le', 'la', 'les', 'de', 'des', 'un', 'une', 'et', 
                        'est', 'dans', 'pour', 'que', 'qui', 'par']
        # Mots anglais courants
        english_words = ['the', 'and', 'of', 'to', 'in', 'is', 'that', 
                         'for', 'it', 'with', 'as', 'was', 'on']
        
        # Comptage des occurrences
        french_count = sum(1 for word in french_words if f' {word} ' in text_lower)
        english_count = sum(1 for word in english_words if f' {word} ' in text_lower)
        
        # Retour de la langue dominante
        if french_count > english_count:
            return 'fr'
        elif english_count > french_count:
            return 'en'
        else:
            return 'fr'  # Par défaut