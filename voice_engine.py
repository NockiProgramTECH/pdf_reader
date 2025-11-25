"""
Moteur de synthèse vocale hybride (en ligne et hors ligne)
Détection automatique de la connexion Internet
"""

import pyttsx3
import re
import time
import os
import tempfile
from pathlib import Path

class VoiceEngine:
    """Classe pour la synthèse vocale hybride"""
    
    def __init__(self):
        """Initialisation du moteur de synthèse vocale"""
        # Détection de la connexion Internet
        self.is_online = self._check_internet_connection()
        
        # Variables d'état
        self.is_paused = False
        self.should_stop = False
        self.current_engine = None
        
        # Initialisation des moteurs
        if self.is_online:
            self._init_online_engine()
        else:
            self._init_offline_engine()
            
    def _check_internet_connection(self):
        """
        Vérifie si une connexion Internet est disponible
        
        Returns:
            bool: True si connecté, False sinon
        """
        try:
            import socket
            import urllib.request
            
            # Test de connexion à Google DNS
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            
            # Tentative de connexion à Google (backup)
            try:
                urllib.request.urlopen('http://www.google.com', timeout=2)
                return True
            except:
                return True  # DNS fonctionne, considéré comme en ligne
                
        except (socket.error, OSError):
            return False
            
    def _init_online_engine(self):
        """Initialisation du moteur en ligne (gTTS)"""
        try:
            from gtts import gTTS
            import pygame
            
            # Test de fonctionnement
            test_text = "test"
            tts = gTTS(text=test_text, lang='fr', slow=False)
            
            self.current_engine = "online"
            self.gtts_available = True
            
            # Initialisation de pygame pour la lecture audio
            pygame.mixer.init()
            
            print("✓ Moteur en ligne activé (gTTS)")
            
        except ImportError:
            print("⚠ gTTS ou pygame non disponible, passage en mode hors ligne")
            self._init_offline_engine()
        except Exception as e:
            print(f"⚠ Erreur moteur en ligne: {e}, passage en mode hors ligne")
            self._init_offline_engine()
            
    def _init_offline_engine(self):
        """Initialisation du moteur hors ligne (pyttsx3)"""
        try:
            self.engine = pyttsx3.init()
            self.current_engine = "offline"
            self.gtts_available = False
            
            # Configuration par défaut
            self._setup_default_voice()
            
            print("✓ Moteur hors ligne activé (pyttsx3)")
            
        except Exception as e:
            raise Exception(f"Impossible d'initialiser le moteur vocal: {e}")
            
    def _setup_default_voice(self):
        """Configuration de la voix par défaut (pyttsx3)"""
        voices = self.engine.getProperty('voices')
        
        # Recherche d'une voix française si disponible
        french_voice = None
        for voice in voices:
            if 'french' in voice.name.lower() or 'fr' in voice.id.lower():
                french_voice = voice
                break
                
        # Utilisation de la voix française si trouvée
        if french_voice:
            self.engine.setProperty('voice', french_voice.id)
        
        # Configuration de base
        self.engine.setProperty('rate', 150)  # Vitesse normale
        self.engine.setProperty('volume', 0.8)  # Volume à 80%
        
    def read_text(self, text, speed=1.0, volume=0.8, progress_callback=None):
        """
        Lit un texte à haute voix avec gestion de la ponctuation
        
        Args:
            text (str): Texte à lire
            speed (float): Vitesse de lecture (0.5 à 2.0)
            volume (float): Volume (0.0 à 1.0)
            progress_callback (callable): Fonction de rappel pour la progression
        """
        self.should_stop = False
        self.is_paused = False
        
        # Application des paramètres
        self.set_speed(speed)
        self.set_volume(volume)
        
        # Découpage du texte en phrases
        sentences = self._split_into_sentences(text)
        total_sentences = len(sentences)
        
        if self.current_engine == "online":
            self._read_text_online(sentences, total_sentences, progress_callback)
        else:
            self._read_text_offline(sentences, total_sentences, progress_callback)
            
    def _read_text_online(self, sentences, total_sentences, progress_callback):
        """
        Lecture avec moteur en ligne (gTTS)
        
        Args:
            sentences (list): Liste des phrases
            total_sentences (int): Nombre total de phrases
            progress_callback (callable): Fonction de rappel
        """
        from gtts import gTTS
        import pygame
        
        temp_dir = tempfile.gettempdir()
        
        for i, sentence in enumerate(sentences):
            if self.should_stop:
                break
                
            # Gestion de la pause
            while self.is_paused and not self.should_stop:
                time.sleep(0.1)
                
            if self.should_stop:
                break
                
            try:
                # Détection de la langue (simplifiée)
                lang = self._detect_sentence_language(sentence)
                
                # Génération audio avec gTTS
                tts = gTTS(text=sentence, lang=lang, slow=False)
                
                # Fichier temporaire
                temp_file = os.path.join(temp_dir, f"tts_temp_{i}.mp3")
                tts.save(temp_file)
                
                # Lecture du fichier audio
                pygame.mixer.music.load(temp_file)
                pygame.mixer.music.play()
                
                # Attente de la fin de la lecture
                while pygame.mixer.music.get_busy():
                    if self.should_stop:
                        pygame.mixer.music.stop()
                        break
                    while self.is_paused and not self.should_stop:
                        pygame.mixer.music.pause()
                        time.sleep(0.1)
                        if not self.is_paused:
                            pygame.mixer.music.unpause()
                    time.sleep(0.1)
                
                # Suppression du fichier temporaire
                try:
                    os.remove(temp_file)
                except:
                    pass
                    
                # Mise à jour de la progression
                if progress_callback:
                    progress = (i + 1) / total_sentences
                    progress_callback(progress)
                    
            except Exception as e:
                print(f"Erreur lecture en ligne: {e}")
                # Fallback vers le mode hors ligne
                self._init_offline_engine()
                remaining_sentences = sentences[i:]
                self._read_text_offline(
                    remaining_sentences, 
                    len(remaining_sentences),
                    progress_callback
                )
                break
                
    def _read_text_offline(self, sentences, total_sentences, progress_callback):
        """
        Lecture avec moteur hors ligne (pyttsx3)
        
        Args:
            sentences (list): Liste des phrases
            total_sentences (int): Nombre total de phrases
            progress_callback (callable): Fonction de rappel
        """
        for i, sentence in enumerate(sentences):
            if self.should_stop:
                break
                
            # Gestion de la pause
            while self.is_paused and not self.should_stop:
                time.sleep(0.1)
                
            if self.should_stop:
                break
                
            # Lecture de la phrase
            self._read_sentence_offline(sentence)
            
            # Mise à jour de la progression
            if progress_callback:
                progress = (i + 1) / total_sentences
                progress_callback(progress)
                
    def _split_into_sentences(self, text):
        """
        Découpe le texte en phrases en respectant la ponctuation
        
        Args:
            text (str): Texte à découper
            
        Returns:
            list: Liste des phrases
        """
        # Découpage sur les points, points d'exclamation et d'interrogation
        sentences = re.split(r'([.!?]+)', text)
        
        # Reconstruction des phrases avec leur ponctuation
        result = []
        for i in range(0, len(sentences) - 1, 2):
            if sentences[i].strip():
                sentence = sentences[i].strip()
                if i + 1 < len(sentences):
                    sentence += sentences[i + 1]
                result.append(sentence)
                
        return [s for s in result if s.strip()]
        
    def _read_sentence_offline(self, sentence):
        """
        Lit une phrase avec pyttsx3
        
        Args:
            sentence (str): Phrase à lire
        """
        # Ajout de pauses pour les virgules et autres ponctuations
        sentence_with_pauses = sentence.replace(',', ', ')
        sentence_with_pauses = sentence_with_pauses.replace(';', '; ')
        sentence_with_pauses = sentence_with_pauses.replace(':', ': ')
        
        # Détection du ton basé sur la ponctuation finale
        if sentence.strip().endswith('?'):
            self._adjust_pitch_offline(1.1)
        elif sentence.strip().endswith('!'):
            self._adjust_pitch_offline(1.05)
        else:
            self._adjust_pitch_offline(1.0)
            
        # Lecture de la phrase
        self.engine.say(sentence_with_pauses)
        self.engine.runAndWait()
        
    def _adjust_pitch_offline(self, factor):
        """
        Ajuste la hauteur de la voix pour pyttsx3
        
        Args:
            factor (float): Facteur de hauteur
        """
        # pyttsx3 ne supporte pas directement le pitch
        # Cette fonction est un placeholder
        pass
        
    def _detect_sentence_language(self, sentence):
        """
        Détecte la langue d'une phrase (pour gTTS)
        
        Args:
            sentence (str): Phrase à analyser
            
        Returns:
            str: Code de langue ('fr', 'en', etc.)
        """
        sentence_lower = sentence.lower()
        
        # Mots français courants
        french_words = ['le', 'la', 'les', 'de', 'des', 'un', 'une', 'et', 
                        'est', 'dans', 'pour', 'que', 'qui', 'par', 'avec']
        # Mots anglais courants
        english_words = ['the', 'and', 'of', 'to', 'in', 'is', 'that', 
                         'for', 'it', 'with', 'as', 'was', 'on', 'are']
        
        # Comptage des occurrences
        french_count = sum(1 for word in french_words if f' {word} ' in f' {sentence_lower} ')
        english_count = sum(1 for word in english_words if f' {word} ' in f' {sentence_lower} ')
        
        # Retour de la langue dominante
        if french_count > english_count:
            return 'fr'
        elif english_count > french_count:
            return 'en'
        else:
            return 'fr'  # Par défaut
            
    def pause(self):
        """Met en pause la lecture"""
        self.is_paused = True
        
    def resume(self):
        """Reprend la lecture"""
        self.is_paused = False
        
    def stop(self):
        """Arrête la lecture"""
        self.should_stop = True
        self.is_paused = False
        
        if self.current_engine == "online":
            try:
                import pygame
                pygame.mixer.music.stop()
            except:
                pass
        else:
            try:
                self.engine.stop()
            except:
                pass
                
    def set_speed(self, speed):
        """
        Définit la vitesse de lecture
        
        Args:
            speed (float): Vitesse (0.5 à 2.0, normal = 1.0)
        """
        if self.current_engine == "offline":
            base_rate = 150
            rate = int(base_rate * speed)
            rate = max(50, min(rate, 300))
            self.engine.setProperty('rate', rate)
        # Pour gTTS, la vitesse est gérée différemment (slow parameter)
        
    def set_volume(self, volume):
        """
        Définit le volume
        
        Args:
            volume (float): Volume (0.0 à 1.0)
        """
        volume = max(0.0, min(volume, 1.0))
        
        if self.current_engine == "offline":
            self.engine.setProperty('volume', volume)
        else:
            try:
                import pygame
                pygame.mixer.music.set_volume(volume)
            except:
                pass
                
    def get_engine_status(self):
        """
        Obtient le statut du moteur actuel
        
        Returns:
            dict: Informations sur le moteur
        """
        return {
            'engine': self.current_engine,
            'is_online': self.is_online,
            'quality': 'Haute (Google TTS)' if self.current_engine == 'online' else 'Standard (pyttsx3)'
        }
        
    def get_available_voices(self):
        """
        Obtient la liste des voix disponibles (pyttsx3 uniquement)
        
        Returns:
            list: Liste des voix disponibles
        """
        if self.current_engine == "offline":
            return self.engine.getProperty('voices')
        return []
        
    def set_voice(self, voice_id):
        """
        Définit la voix à utiliser (pyttsx3 uniquement)
        
        Args:
            voice_id (str): ID de la voix
        """
        if self.current_engine == "offline":
            self.engine.setProperty('voice', voice_id)