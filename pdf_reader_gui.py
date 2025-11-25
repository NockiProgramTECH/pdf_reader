"""
Interface graphique du lecteur PDF
Gestion de l'UI avec CustomTkinter
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from pdf_processor import PDFProcessor
from voice_engine import VoiceEngine

class PDFReaderGUI(ctk.CTk):
    """Classe principale de l'interface graphique"""
    
    def __init__(self):
        super().__init__()
        
        # Configuration de la fenêtre principale
        self.title("Lecteur PDF Vocal Professionnel")
        self.geometry("1000x700")
        self.minsize(800, 600)
        
        # Couleurs professionnelles
        self.colors = {
            "primary": "#1a1a2e",
            "secondary": "#16213e",
            "accent": "#0f3460",
            "highlight": "#533483",
            "text": "#e8e8e8",
            "success": "#2ecc71",
            "warning": "#f39c12",
            "danger": "#e74c3c"
        }
        
        # Initialisation des modules
        self.pdf_processor = PDFProcessor()
        self.voice_engine = VoiceEngine()
        
        # Variables d'état
        self.current_pdf_path = None
        self.is_reading = False
        self.reading_thread = None
        
        # Construction de l'interface
        self._build_ui()
        
    def _build_ui(self):
        """Construction de l'interface utilisateur"""
        
        # Configuration de la grille principale
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Panneau latéral gauche (contrôles)
        self._create_sidebar()
        
        # Panneau principal (affichage du texte)
        self._create_main_panel()
        
        # Barre de statut
        self._create_status_bar()
        
    def _create_sidebar(self):
        """Création du panneau latéral de contrôle"""
        sidebar = ctk.CTkFrame(self, width=300, corner_radius=0)
        sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=0, pady=0)
        sidebar.grid_rowconfigure(10, weight=1)
        
        # Titre
        title_label = ctk.CTkLabel(
            sidebar,
            text="🎧 Lecteur PDF Vocal",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Bouton de sélection de fichier
        self.btn_select_file = ctk.CTkButton(
            sidebar,
            text="📁 Ouvrir un PDF",
            command=self._select_pdf_file,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.colors["highlight"],
            hover_color=self.colors["accent"]
        )
        self.btn_select_file.grid(row=1, column=0, padx=20, pady=10)
        
        # Nom du fichier
        self.lbl_filename = ctk.CTkLabel(
            sidebar,
            text="Aucun fichier sélectionné",
            wraplength=260,
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.lbl_filename.grid(row=2, column=0, padx=20, pady=(0, 20))
        
        # Séparateur
        separator1 = ctk.CTkFrame(sidebar, height=2, fg_color="gray30")
        separator1.grid(row=3, column=0, sticky="ew", padx=20, pady=10)
        
        # Section des pages
        page_label = ctk.CTkLabel(
            sidebar,
            text="Configuration de lecture",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        page_label.grid(row=4, column=0, padx=20, pady=(10, 5))
        
        # Page de début
        start_page_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        start_page_frame.grid(row=5, column=0, padx=20, pady=5, sticky="ew")
        
        ctk.CTkLabel(
            start_page_frame,
            text="Page de début:",
            font=ctk.CTkFont(size=12)
        ).pack(side="left", padx=(0, 10))
        
        self.entry_start_page = ctk.CTkEntry(
            start_page_frame,
            width=60,
            placeholder_text="1"
        )
        self.entry_start_page.pack(side="left")
        self.entry_start_page.insert(0, "1")
        
        # Page de fin (optionnelle)
        end_page_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        end_page_frame.grid(row=6, column=0, padx=20, pady=5, sticky="ew")
        
        ctk.CTkLabel(
            end_page_frame,
            text="Page de fin:",
            font=ctk.CTkFont(size=12)
        ).pack(side="left", padx=(0, 10))
        
        self.entry_end_page = ctk.CTkEntry(
            end_page_frame,
            width=60,
            placeholder_text="Fin"
        )
        self.entry_end_page.pack(side="left")
        
        # Vitesse de lecture
        speed_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        speed_frame.grid(row=7, column=0, padx=20, pady=10, sticky="ew")
        
        ctk.CTkLabel(
            speed_frame,
            text="Vitesse:",
            font=ctk.CTkFont(size=12)
        ).pack(side="left", padx=(0, 10))
        
        self.slider_speed = ctk.CTkSlider(
            speed_frame,
            from_=0.5,
            to=2.0,
            number_of_steps=15,
            command=self._update_speed
        )
        self.slider_speed.pack(side="left", fill="x", expand=True)
        self.slider_speed.set(1.0)
        
        self.lbl_speed = ctk.CTkLabel(speed_frame, text="1.0x", width=40)
        self.lbl_speed.pack(side="left", padx=(5, 0))
        
        # Volume
        volume_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        volume_frame.grid(row=8, column=0, padx=20, pady=10, sticky="ew")
        
        ctk.CTkLabel(
            volume_frame,
            text="Volume:",
            font=ctk.CTkFont(size=12)
        ).pack(side="left", padx=(0, 10))
        
        self.slider_volume = ctk.CTkSlider(
            volume_frame,
            from_=0.0,
            to=1.0,
            number_of_steps=10,
            command=self._update_volume
        )
        self.slider_volume.pack(side="left", fill="x", expand=True)
        self.slider_volume.set(0.8)
        
        self.lbl_volume = ctk.CTkLabel(volume_frame, text="80%", width=40)
        self.lbl_volume.pack(side="left", padx=(5, 0))
        
        # Séparateur
        separator2 = ctk.CTkFrame(sidebar, height=2, fg_color="gray30")
        separator2.grid(row=9, column=0, sticky="ew", padx=20, pady=15)
        
        # Boutons de contrôle
        control_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        control_frame.grid(row=11, column=0, padx=20, pady=(0, 20))
        
        self.btn_play = ctk.CTkButton(
            control_frame,
            text="▶️ Lire",
            command=self._start_reading,
            width=120,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.colors["success"],
            hover_color="#27ae60"
        )
        self.btn_play.grid(row=0, column=0, padx=5, pady=5)
        
        self.btn_pause = ctk.CTkButton(
            control_frame,
            text="⏸️ Pause",
            command=self._pause_reading,
            width=120,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.colors["warning"],
            hover_color="#e67e22",
            state="disabled"
        )
        self.btn_pause.grid(row=0, column=1, padx=5, pady=5)
        
        self.btn_stop = ctk.CTkButton(
            control_frame,
            text="⏹️ Arrêter",
            command=self._stop_reading,
            width=120,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.colors["danger"],
            hover_color="#c0392b",
            state="disabled"
        )
        self.btn_stop.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
    def _create_main_panel(self):
        """Création du panneau principal d'affichage"""
        main_frame = ctk.CTkFrame(self, corner_radius=10)
        main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Titre du panneau
        header = ctk.CTkLabel(
            main_frame,
            text="Contenu du PDF",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        header.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # Zone de texte avec scrollbar
        self.text_display = ctk.CTkTextbox(
            main_frame,
            font=ctk.CTkFont(size=13),
            wrap="word",
            activate_scrollbars=True
        )
        self.text_display.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
    def _create_status_bar(self):
        """Création de la barre de statut"""
        status_frame = ctk.CTkFrame(self, height=40, corner_radius=0)
        status_frame.grid(row=1, column=1, sticky="ew", padx=0, pady=0)
        
        self.lbl_status = ctk.CTkLabel(
            status_frame,
            text="Prêt",
            font=ctk.CTkFont(size=11),
            anchor="w"
        )
        self.lbl_status.pack(side="left", padx=20, pady=10)
        
        self.progress_bar = ctk.CTkProgressBar(status_frame, width=200)
        self.progress_bar.pack(side="right", padx=20, pady=10)
        self.progress_bar.set(0)
        
    def _select_pdf_file(self):
        """Sélection d'un fichier PDF"""
        filename = filedialog.askopenfilename(
            title="Sélectionner un fichier PDF",
            filetypes=[("Fichiers PDF", "*.pdf"), ("Tous les fichiers", "*.*")]
        )
        
        if filename:
            self.current_pdf_path = filename
            # Afficher uniquement le nom du fichier
            import os
            file_display = os.path.basename(filename)
            self.lbl_filename.configure(text=file_display, text_color=self.colors["text"])
            
            # Charger et afficher le PDF
            self._load_pdf()
            
    def _load_pdf(self):
        """Chargement et affichage du contenu PDF"""
        if not self.current_pdf_path:
            return
            
        try:
            self.lbl_status.configure(text="Chargement du PDF...")
            self.text_display.delete("1.0", "end")
            
            # Extraction du texte
            text = self.pdf_processor.extract_text(self.current_pdf_path)
            
            if text:
                self.text_display.insert("1.0", text)
                total_pages = self.pdf_processor.get_page_count(self.current_pdf_path)
                self.lbl_status.configure(
                    text=f"PDF chargé - {total_pages} page(s)"
                )
            else:
                messagebox.showwarning(
                    "Avertissement",
                    "Aucun texte n'a pu être extrait de ce PDF."
                )
                self.lbl_status.configure(text="Échec du chargement")
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement: {str(e)}")
            self.lbl_status.configure(text="Erreur")
            
    def _start_reading(self):
        """Démarrage de la lecture vocale"""
        if not self.current_pdf_path:
            messagebox.showwarning(
                "Avertissement",
                "Veuillez d'abord sélectionner un fichier PDF."
            )
            return
            
        try:
            start_page = int(self.entry_start_page.get() or 1)
            end_page_text = self.entry_end_page.get()
            end_page = int(end_page_text) if end_page_text else None
            
            # Extraction du texte pour les pages spécifiées
            text = self.pdf_processor.extract_text(
                self.current_pdf_path,
                start_page,
                end_page
            )
            
            if not text:
                messagebox.showwarning(
                    "Avertissement",
                    "Aucun texte à lire dans les pages spécifiées."
                )
                return
                
            # Mise à jour de l'interface
            self.is_reading = True
            self.btn_play.configure(state="disabled")
            self.btn_pause.configure(state="normal")
            self.btn_stop.configure(state="normal")
            self.btn_select_file.configure(state="disabled")
            
            # Démarrage de la lecture dans un thread séparé
            self.reading_thread = threading.Thread(
                target=self._read_text_thread,
                args=(text,),
                daemon=True
            )
            self.reading_thread.start()
            
            self.lbl_status.configure(text="Lecture en cours...")
            
        except ValueError:
            messagebox.showerror(
                "Erreur",
                "Veuillez entrer des numéros de page valides."
            )
            
    def _read_text_thread(self, text):
        """Thread de lecture vocale"""
        try:
            self.voice_engine.read_text(
                text,
                speed=self.slider_speed.get(),
                volume=self.slider_volume.get(),
                progress_callback=self._update_progress
            )
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Erreur", str(e)))
        finally:
            self.after(0, self._reading_finished)
            
    def _pause_reading(self):
        """Pause de la lecture"""
        if self.is_reading:
            self.voice_engine.pause()
            self.btn_pause.configure(text="▶️ Reprendre")
            self.lbl_status.configure(text="En pause")
        else:
            self.voice_engine.resume()
            self.btn_pause.configure(text="⏸️ Pause")
            self.lbl_status.configure(text="Lecture en cours...")
            
        self.is_reading = not self.is_reading
        
    def _stop_reading(self):
        """Arrêt de la lecture"""
        self.voice_engine.stop()
        self._reading_finished()
        
    def _reading_finished(self):
        """Appelé lorsque la lecture est terminée"""
        self.is_reading = False
        self.btn_play.configure(state="normal")
        self.btn_pause.configure(state="disabled", text="⏸️ Pause")
        self.btn_stop.configure(state="disabled")
        self.btn_select_file.configure(state="normal")
        self.lbl_status.configure(text="Lecture terminée")
        self.progress_bar.set(0)
        
    def _update_progress(self, progress):
        """Mise à jour de la barre de progression"""
        self.after(0, lambda: self.progress_bar.set(progress))
        
    def _update_speed(self, value):
        """Mise à jour de la vitesse de lecture"""
        self.lbl_speed.configure(text=f"{value:.1f}x")
        if self.is_reading:
            self.voice_engine.set_speed(value)
            
    def _update_volume(self, value):
        """Mise à jour du volume"""
        self.lbl_volume.configure(text=f"{int(value * 100)}%")
        if self.is_reading:
            self.voice_engine.set_volume(value)