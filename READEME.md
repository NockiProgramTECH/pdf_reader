# 🎧 Lecteur PDF Vocal Professionnel

Application de lecture vocale de fichiers PDF avec interface graphique moderne et **système hybride intelligent** (en ligne/hors ligne).

## 📋 Fonctionnalités

### ✨ Principales
- **🌐 Mode hybride intelligent** : Détection automatique de la connexion Internet
  - **En ligne** : Utilise Google TTS (qualité supérieure, voix naturelles)
  - **Hors ligne** : Bascule automatiquement sur pyttsx3 (fonctionne sans Internet)
- **Lecture vocale intelligente** : Synthèse vocale naturelle avec respect de la ponctuation
- **Contrôle des pages** : Sélection de la page de début et de fin
- **Interface moderne** : Design professionnel avec CustomTkinter
- **Contrôles avancés** :
  - Vitesse de lecture ajustable (0.5x à 2.0x)
  - Volume ajustable (0% à 100%)
  - Pause/Reprise
  - Arrêt immédiat
- **Barre de progression** : Suivi en temps réel de la lecture
- **Indicateurs de statut** : Affichage du mode actif et de la qualité audio

### 🎯 Respect de la ponctuation
Le programme lit le texte comme un humain en respectant :
- **Points (.)** : Pause longue et ton descendant
- **Points d'interrogation (?)** : Ton interrogatif avec légère montée
- **Points d'exclamation (!)** : Ton exclamatif avec emphase
- **Virgules (,)** : Pause courte (300ms)
- **Deux-points (:)** : Pause moyenne (400ms)
- **Points-virgules (;)** : Pause moyenne (500ms)

### 🌐 Système hybride intelligent

#### Mode EN LIGNE (prioritaire)
Lorsqu'une connexion Internet est détectée :
- ✅ **Utilise Google Text-to-Speech (gTTS)**
- ✅ Qualité vocale supérieure
- ✅ Voix naturelles et expressives
- ✅ Détection automatique de la langue (français/anglais)
- ✅ Meilleure prononciation
- ✅ Intonation plus naturelle

#### Mode HORS LIGNE (fallback automatique)
Sans connexion Internet ou si gTTS échoue :
- 🔄 **Bascule automatiquement sur pyttsx3**
- 📴 Fonctionne complètement hors ligne
- 🔊 Utilise les voix système
- ⚡ Pas de dépendance réseau
- 💾 Pas de fichiers temporaires

**Le programme détecte automatiquement le meilleur mode et affiche l'état actuel dans l'interface.**

## 📦 Installation

### Prérequis
- Python 3.7 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner ou télécharger le projet**
```bash
git clone [URL_DU_PROJET]
cd lecteur-pdf-vocal
```

2. **Créer un environnement virtuel (recommandé)**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

### Dépendances système

#### Windows
- **Mode hors ligne** : Aucune installation supplémentaire (SAPI5 intégré)
- **Mode en ligne** : Connexion Internet uniquement

#### Linux (Ubuntu/Debian)
```bash
# Pour le mode hors ligne (pyttsx3)
sudo apt-get update
sudo apt-get install espeak espeak-data libespeak-dev

# Pour le mode en ligne (pygame pour lecture audio)
sudo apt-get install python3-pygame
```

#### macOS
- **Mode hors ligne** : Aucune installation supplémentaire (NSSpeechSynthesizer natif)
- **Mode en ligne** : `brew install portaudio` (si problème avec pygame)

## 🚀 Utilisation

### Lancement de l'application
```bash
python main.py
```

Le programme affiche automatiquement le mode actif :
- **🌐 En ligne** : Utilise Google TTS (qualité haute)
- **📴 Hors ligne** : Utilise pyttsx3 (qualité standard)

### Guide d'utilisation

1. **Vérifier le statut de connexion**
   - En haut à gauche : indicateur "🌐 En ligne" ou "📴 Hors ligne"
   - En bas : "Qualité: Haute (Google TTS)" ou "Qualité: Standard (pyttsx3)"

2. **Ouvrir un PDF**
   - Cliquez sur "📁 Ouvrir un PDF"
   - Sélectionnez votre fichier PDF
   - Le contenu s'affiche automatiquement

2. **Configurer la lecture**
   - **Page de début** : Entrez le numéro de la première page à lire (défaut : 1)
   - **Page de fin** : Entrez le numéro de la dernière page (optionnel, défaut : dernière page)
   - **Vitesse** : Ajustez avec le curseur (0.5x à 2.0x)
   - **Volume** : Ajustez avec le curseur (0% à 100%)

3. **Contrôler la lecture**
   - **▶️ Lire** : Démarre la lecture
   - **⏸️ Pause** : Met en pause (devient "▶️ Reprendre")
   - **⏹️ Arrêter** : Arrête complètement la lecture

4. **Suivre la progression**
   - La barre de progression en bas indique l'avancement
   - Le statut affiche l'état actuel (Lecture en cours, En pause, etc.)

### Basculement automatique en cas de perte de connexion

Si vous perdez votre connexion Internet pendant la lecture :
- Le programme détecte automatiquement l'erreur
- Bascule sur le moteur hors ligne (pyttsx3)
- Continue la lecture sans interruption
- Met à jour l'indicateur de statut

## 📁 Structure du projet

```
lecteur-pdf-vocal/
│
├── main.py                 # Point d'entrée de l'application
├── pdf_reader_gui.py       # Interface graphique (CustomTkinter)
├── pdf_processor.py        # Traitement et extraction des PDF
├── voice_engine.py         # Moteur de synthèse vocale
├── requirements.txt        # Dépendances du projet
└── README.md              # Documentation (ce fichier)
```

## 🔧 Architecture

### main.py
- Point d'entrée principal
- Configuration du thème CustomTkinter
- Initialisation de l'application

### pdf_reader_gui.py
- Interface utilisateur complète
- Gestion des événements
- Coordination des modules
- **Composants** :
  - Panneau latéral de contrôle
  - Zone d'affichage du texte
  - Barre de statut avec progression

### pdf_processor.py
- Extraction du texte des PDF (PyPDF2)
- Nettoyage et formatage du texte
- Détection basique de la langue
- Gestion des pages spécifiques

### voice_engine.py
- Moteur de synthèse vocale **hybride**
- **Détection automatique** de la connexion Internet
- **Mode en ligne** : gTTS (Google Text-to-Speech)
  - Génération de fichiers audio MP3 temporaires
  - Lecture avec pygame
  - Détection automatique de la langue
- **Mode hors ligne** : pyttsx3
  - Utilisation des voix système
  - Pas de fichiers temporaires
- **Fallback automatique** : bascule du mode en ligne vers hors ligne en cas d'erreur
- Gestion de la ponctuation identique pour les deux modes
- Contrôle de la vitesse et du volume
- Système de pause/reprise
- Threading pour lecture non-bloquante

## 🎨 Personnalisation

### Couleurs
Les couleurs sont définies dans `pdf_reader_gui.py` :
```python
self.colors = {
    "primary": "#1a1a2e",      # Arrière-plan principal
    "secondary": "#16213e",    # Arrière-plan secondaire
    "accent": "#0f3460",       # Accent
    "highlight": "#533483",    # Surbrillance
    "text": "#e8e8e8",        # Texte
    "success": "#2ecc71",     # Succès (bouton Lire)
    "warning": "#f39c12",     # Avertissement (bouton Pause)
    "danger": "#e74c3c"       # Danger (bouton Arrêter)
}
```

### Voix
Pour changer la voix par défaut, modifiez `_setup_default_voice()` dans `voice_engine.py`.

Liste des voix disponibles :
```python
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    print(f"ID: {voice.id}")
    print(f"Nom: {voice.name}")
    print(f"Langues: {voice.languages}")
    print("---")
```

## 🌐 Mode en ligne (optionnel)

Pour utiliser Google Text-to-Speech (nécessite Internet) :

1. Installer gTTS :
```bash
pip install gtts playsound
```

2. Créer `voice_engine_online.py` (voir extension dans la documentation avancée)

## 🐛 Dépannage

### Problème : Pas de son
- **Windows** : Vérifiez que les pilotes audio sont installés
- **Linux** : Installez `espeak` et ses dépendances
- **Mac** : Vérifiez les paramètres de sortie audio
- **En ligne** : Vérifiez que pygame est correctement installé

### Problème : Mode hors ligne uniquement (alors que connecté)
```bash
# Vérifier l'installation de gTTS et pygame
pip install gTTS pygame --upgrade

# Tester manuellement
python -c "from gtts import gTTS; print('gTTS OK')"
python -c "import pygame; print('pygame OK')"
```

### Problème : Erreur "No module named 'gTTS'" ou "'pygame'"
```bash
pip install -r requirements.txt --upgrade
```

### Problème : Voix robot/métallique (mode hors ligne)
- Installez des voix supplémentaires pour votre système
- Windows : Paramètres > Voix > Ajouter des voix
- Linux : `sudo apt-get install mbrola mbrola-fr1`
- **Solution** : Le mode en ligne (gTTS) offre une bien meilleure qualité

### Problème : PDF vide après chargement
- Le PDF peut contenir des images au lieu de texte
- Utilisez un OCR pour extraire le texte (non inclus dans cette version)

### Problème : Erreur "No module named..."
```bash
pip install -r requirements.txt --upgrade
```

### Problème : Programme lent en mode en ligne
- Normal : gTTS génère des fichiers audio pour chaque phrase
- La première phrase peut prendre 1-2 secondes
- Les phrases suivantes sont plus rapides
- **Avantage** : Meilleure qualité vocale

### Problème : Fichiers temporaires non supprimés
- Normalement supprimés automatiquement après lecture
- Emplacement : dossier temporaire système
- Nettoyage manuel : supprimez les fichiers `tts_temp_*.mp3` du dossier temp

## 🔮 Améliorations futures

- [ ] Support de l'OCR pour les PDF scannés
- [ ] Sélection manuelle du mode (en ligne/hors ligne)
- [ ] Sélection de différentes voix depuis l'interface
- [ ] Sauvegarde des préférences utilisateur
- [ ] Export audio (MP3/WAV)
- [ ] Cache intelligent pour gTTS (éviter régénération)
- [ ] Support de langues supplémentaires
- [ ] Surlignage du texte en cours de lecture
- [ ] Gestion des signets PDF
- [ ] Mode sombre/clair personnalisable
- [ ] Support multi-langues de l'interface
- [ ] Vitesse ajustable pour gTTS
- [ ] Visualiseur d'ondes audio

## 📄 Licence

Ce projet est libre d'utilisation pour un usage personnel et éducatif.

## 👤 Auteur

Créé avec ❤️ par l'Assistant Claude

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Soumettre des pull requests

## 📞 Support

Pour toute question ou problème :
1. Consultez la section Dépannage
2. Vérifiez que toutes les dépendances sont installées
3. Assurez-vous d'utiliser Python 3.7+

---

**💡 Astuce** : Pour une meilleure qualité vocale, assurez-vous d'avoir une connexion Internet active. Le programme utilisera automatiquement Google TTS qui offre des voix beaucoup plus naturelles que les voix système.

**🔐 Confidentialité** : En mode en ligne, le texte est envoyé à l'API Google TTS. En mode hors ligne, tout reste local sur votre machine.

**Note** : Ce programme lit uniquement le texte extractible des PDF. Pour les PDF scannés (images), un module OCR serait nécessaire.