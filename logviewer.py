import os
import json
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, colorchooser
import locale
import sys
import urllib.request
import webbrowser
import threading
from datetime import datetime

# Für das Taskleisten-Icon unter Windows
try:
    import ctypes
except ImportError:
    ctypes = None

class LogViewerApp:
    APP_VERSION = "0.4.0"  # Manuell gepflegte Anwendungsversion
    SETTINGS_FILE = "log_viewer_settings.json"
    ICON_FILE = "icon.ico"

    def __init__(self, root):
        self.root = root
        
        # Lokalisierung (Fest im Code integriert, keine externen Files)
        self.translations = {
            "de": {
                "title": "Log Viewer",
                "file": "Datei",
                "open_file": "Datei öffnen...",
                "open_folder": "Ordner öffnen...",
                "open_app_dir": "Programm-Verzeichnis öffnen",
                "settings": "Einstellungen",
                "exit": "Beenden",
                "help": "Hilfe",
                "info": "Info",
                "search": "Suchen:",
                "btn_search": "Suchen",
                "live_view": "Live View",
                "auto_scroll": "Auto-Scroll",
                "word_wrap": "Zeilenumbruch",
                "highlights": "Hervorhebungen",
                "file_filter": "Datei-Filter & Sortierung",
                "filename": "Dateiname:",
                "sorting": "Sortierung:",
                "types": "Typen:",
                "select": "Auswählen...",
                "no_ext": "(keine Endung)",
                "tab_general": "Allgemein",
                "tab_highlights": "Hervorhebungen",
                "path_structure": "Pfad & Struktur",
                "size": "Größe",
                "lines": "Zeilen",
                "modified": "Geändert",
                "scan_subdirs": "Unterverzeichnisse durchsuchen",
                "auto_refresh": "Struktur automatisch aktualisieren",
                "language": "Sprache:",
                "manage_ext": "Dateiendungen verwalten",
                "add_ext": "Endung hinzufügen",
                "delete": "Löschen",
                "save_close": "Speichern & Schließen",
                "rules_priority": "Hervorhebungs-Regeln (Reihenfolge = Priorität)",
                "new": "Neu",
                "edit": "Bearbeiten",
                "rule_editor": "Regel-Editor",
                "name": "Name:",
                "terms": "Begriffe (kommagetrennt):",
                "text_color": "Text",
                "bg_color": "Hintergrund",
                "save": "Speichern",
                "cancel": "Abbrechen",
                "error": "Fehler",
                "warning": "Warnung",
                "delete_confirm": "Regel wirklich löschen?",
                "no_ext_warn": "Die Option '(keine Endung)' ist ein fester Bestandteil und kann nicht gelöscht werden.",
                "copyright": "Copyright © Dominik Scharrer",
                "help_text": "Bedienung:\n\n1. Baumansicht: Filtert und sortiert Logdateien.\n2. Einstellungen: Verwalten Sie Dateiendungen und farbliche Regeln.\n3. Priorität: Obere Regeln in der Liste haben Vorrang.\n4. Live View: Echtzeit-Analyse mit manuellem Scroll-Stopp.\n5. Auto-Scroll: Pausiert automatisch beim Hochscrollen.",
                "update_title": "Update verfügbar",
                "update_available": "Eine neue Version ({version}) ist verfügbar!\n\nMöchten Sie die Download-Seite öffnen?",
                "check_for_updates": "Auf Updates prüfen...",
                "no_update_title": "Kein Update",
                "no_update_available": "Sie verwenden bereits die aktuellste Version.",
                "update_check_failed": "Die Update-Prüfung ist fehlgeschlagen.\nBitte prüfen Sie Ihre Internetverbindung.",
                "tab_updates": "Updates",
                "check_updates_on_startup": "Beim Start automatisch auf Updates prüfen",
                "line": "Zeile",
                "column": "Spalte",
                "time_ago": "vor",
                "second": "Sekunde",
                "seconds": "Sekunden",
                "minute": "Minute",
                "minutes": "Minuten",
                "hour": "Stunde",
                "hours": "Stunden",
                "day": "Tag",
                "days": "Tagen",
                "month": "Monat",
                "months": "Monaten",
                "year": "Jahr",
                "years": "Jahren",
                "manual": "ausgewählt",
                "detected": "erkannt"
            },
            "en": {
                "title": "Log Viewer",
                "file": "File",
                "open_file": "Open File...",
                "open_folder": "Open Folder...",
                "open_app_dir": "Open App Directory",
                "settings": "Settings",
                "exit": "Exit",
                "help": "Help",
                "info": "Info",
                "search": "Search:",
                "btn_search": "Search",
                "live_view": "Live View",
                "auto_scroll": "Auto-Scroll",
                "word_wrap": "Word Wrap",
                "highlights": "Highlights",
                "file_filter": "File Filter & Sorting",
                "filename": "Filename:",
                "sorting": "Sorting:",
                "types": "Types:",
                "select": "Select...",
                "no_ext": "(no extension)",
                "tab_general": "General",
                "tab_highlights": "Highlights",
                "path_structure": "Path & Structure",
                "size": "Size",
                "lines": "Lines",
                "modified": "Modified",
                "scan_subdirs": "Search subdirectories",
                "auto_refresh": "Automatically refresh structure",
                "language": "Language:",
                "manage_ext": "Manage Extensions",
                "add_ext": "Add Extension",
                "delete": "Delete",
                "save_close": "Save & Close",
                "rules_priority": "Highlighting Rules (Order = Priority)",
                "new": "New",
                "edit": "Edit",
                "rule_editor": "Rule Editor",
                "name": "Name:",
                "terms": "Terms (comma separated):",
                "text_color": "Text",
                "bg_color": "Background",
                "save": "Save",
                "cancel": "Cancel",
                "error": "Error",
                "warning": "Warning",
                "delete_confirm": "Delete this rule?",
                "no_ext_warn": "The option '(no extension)' is a permanent feature and cannot be deleted.",
                "copyright": "Copyright © Dominik Scharrer",
                "help_text": "Operation:\n\n1. Tree View: Filter and sort log files.\n2. Settings: Manage extensions and color rules.\n3. Priority: Rules at the top of the list take precedence.\n4. Live View: Real-time analysis with manual scroll stop.\n5. Auto-Scroll: Pauses automatically when scrolling up.",
                "update_title": "Update Available",
                "update_available": "A new version ({version}) is available!\nDo you want to open the download page?",
                "check_for_updates": "Check for Updates...",
                "no_update_title": "No Update",
                "no_update_available": "You are already using the latest version.",
                "update_check_failed": "The update check failed.\nPlease check your internet connection.",
                "tab_updates": "Updates",
                "check_updates_on_startup": "Automatically check for updates on startup",
                "line": "Line",
                "column": "Column",
                "time_ago": "ago",
                "second": "second",
                "seconds": "seconds",
                "minute": "minute",
                "minutes": "minutes",
                "hour": "hour",
                "hours": "hours",
                "day": "day",
                "days": "days",
                "month": "month",
                "months": "months",
                "year": "year",
                "years": "years",
                "manual": "selected",
                "detected": "detected"
            }
        }

        # Standard-Konfiguration
        self.default_config = [
            {"name": "ERROR", "fg": "white", "bg": "red", "aliases": ["ERROR", "ERR", "FAILURE", "FAILED", "CRITICAL", "FATAL", "EXCEPTION", "SEVERE"]},
            {"name": "WARNING", "fg": "black", "bg": "orange", "aliases": ["WARNING", "WARN", "ATTENTION", "CAUTION", "VORSICHT"]},
            {"name": "INFO", "fg": "white", "bg": "blue", "aliases": ["INFO", "INFORMATION", "LOG", "MSG", "MESSAGE", "HINWEIS"]},
            {"name": "SUCCESS", "fg": "white", "bg": "green", "aliases": ["SUCCESS", "OK", "DONE", "COMPLETED", "FINISHED", "PASSED", "ERFOLG"]},
            {"name": "DEBUG", "fg": "black", "bg": "gray", "aliases": ["DEBUG", "TRACE", "VERBOSE"]}
        ]

        # Statusvariablen
        self.live_view_active = tk.BooleanVar(value=False)
        self.auto_scroll_active = tk.BooleanVar(value=False)
        self.word_wrap_active = tk.BooleanVar(value=False)
        self.current_file = None
        self.last_mtime = 0
        self.tree_structure_cache = None
        self.settings_modified = False
        self.current_file_encoding = None
        self.current_file_mtime = None
        self.last_detected_encoding = None

        # Filter & Sortierung Variablen
        self.file_search_var = tk.StringVar()
        self.file_search_var.trace_add("write", lambda *args: self.refresh_file_tree())
        self.sort_var = tk.StringVar()
        
        # Initiale Sprache bestimmen
        try:
            locale.setlocale(locale.LC_ALL, "")
            sys_lang = locale.getlocale()[0]
        except:
            sys_lang = "en"
        self.lang = "de" if sys_lang and sys_lang.lower().startswith(("de", "german")) else "en"

        # Einstellungen laden
        self.load_settings()
        
        self.root.title(f"{self.tr('title')} v{self.APP_VERSION}")
        self.root.geometry("1200x800")
        
        # Icon setzen
        self.set_app_icon()

        self.setup_menu()
        self.setup_ui()
        self.refresh_file_tree()
        
        self.check_for_file_updates()
        self.check_for_tree_updates()
        if self.check_updates_on_startup_var.get():
            self.check_for_new_release()

        self.update_relative_time()
        self.update_cursor_position_display()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def tr(self, key):
        """Hilfsfunktion für Übersetzungen."""
        lang_dict = self.translations.get(self.lang, self.translations["en"])
        return lang_dict.get(key, key)

    def get_resource_path(self, relative_path):
        """Gibt den Pfad zu einer Ressource zurück (funktioniert für Skript und EXE)."""
        if hasattr(sys, '_MEIPASS'):
            # PyInstaller entpackt Dateien in diesen temporären Ordner
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    def get_app_dir(self):
        """Gibt das Verzeichnis zurück, in dem die EXE/das Skript liegt (für JSON)."""
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        return os.path.dirname(os.path.abspath(__file__))

    def set_app_icon(self):
        """Lädt das Icon aus dem PyInstaller-Speicher."""
        icon_path = self.get_resource_path(self.ICON_FILE)
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
                if sys.platform == "win32" and ctypes:
                    app_id = f"dominikscharrer.logviewer.v1"
                    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
            except:
                pass

    def load_settings(self):
        """Lädt Einstellungen aus der JSON neben der EXE."""
        app_dir = self.get_app_dir()
        defaults = {
            "log_rules": self.default_config,
            "filter_states": {item["name"]: False for item in self.default_config},
            "scan_subdirs": True,
            "auto_refresh_tree": True,
            "sidebar_width": 300,
            "current_scan_path": app_dir,
            "allowed_extensions": [".log", ".txt", ""],
            "active_extensions": [".log", ".txt", ""],
            "sort_mode": "Name (A-Z)",
            "language": self.lang,
            "word_wrap": False,
            "check_for_updates_on_startup": True
        }

        settings_path = os.path.join(app_dir, self.SETTINGS_FILE)
        loaded_data = {}
        if os.path.exists(settings_path):
            try:
                with open(settings_path, "r", encoding="utf-8") as f:
                    loaded_data = json.load(f)
            except Exception: # Bei korrupter Datei werden Defaults verwendet
                pass

        self.log_rules = loaded_data.get("log_rules", defaults["log_rules"])
        saved_filters = loaded_data.get("filter_states", {})
        self.scan_subdirs = tk.BooleanVar(value=loaded_data.get("scan_subdirs", defaults["scan_subdirs"]))
        self.auto_refresh_tree = tk.BooleanVar(value=loaded_data.get("auto_refresh_tree", defaults["auto_refresh_tree"]))
        self.sidebar_width = loaded_data.get("sidebar_width", defaults["sidebar_width"])
        self.current_scan_path = loaded_data.get("current_scan_path", defaults["current_scan_path"])
        self.allowed_extensions = loaded_data.get("allowed_extensions", defaults["allowed_extensions"])
        self.active_extensions = loaded_data.get("active_extensions", defaults["active_extensions"])
        self.sort_var.set(loaded_data.get("sort_mode", defaults["sort_mode"]))
        self.lang = loaded_data.get("language", defaults["language"])
        self.word_wrap_active.set(loaded_data.get("word_wrap", defaults["word_wrap"]))
        self.check_updates_on_startup_var = tk.BooleanVar(value=loaded_data.get("check_for_updates_on_startup", defaults["check_for_updates_on_startup"]))

        if "" not in self.allowed_extensions:
            self.allowed_extensions.append("")

        if not os.path.exists(self.current_scan_path):
            self.current_scan_path = app_dir

        self.filter_vars = {rule["name"]: tk.BooleanVar(value=saved_filters.get(rule["name"], False)) for rule in self.log_rules}
        self.ext_vars = {ext: tk.BooleanVar(value=(ext in self.active_extensions)) for ext in self.allowed_extensions}
        self.settings_modified = False

    def save_settings(self, force=False):
        current_width = self.sidebar_frame.winfo_width()
        if current_width > 1 and current_width != self.sidebar_width:
            self.sidebar_width = current_width
            self.settings_modified = True

        if not self.settings_modified and not force:
            return

        data = {
            "log_rules": self.log_rules,
            "filter_states": {name: var.get() for name, var in self.filter_vars.items()},
            "scan_subdirs": self.scan_subdirs.get(),
            "auto_refresh_tree": self.auto_refresh_tree.get(),
            "sidebar_width": self.sidebar_width,
            "current_scan_path": self.current_scan_path,
            "allowed_extensions": self.allowed_extensions,
            "active_extensions": [ext for ext, var in self.ext_vars.items() if var.get()],
            "sort_mode": self.sort_var.get(),
            "language": self.lang,
            "word_wrap": self.word_wrap_active.get(),
            "check_for_updates_on_startup": self.check_updates_on_startup_var.get()
        }
        try:
            settings_path = os.path.join(self.get_app_dir(), self.SETTINGS_FILE)
            with open(settings_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            self.settings_modified = False
        except Exception as e:
            print(f"Error saving settings: {e}")

    def on_closing(self):
        self.save_settings()
        self.root.destroy()

    def setup_menu(self):
        self.menubar = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label=self.tr("open_file"), command=self.open_manual_file)
        self.file_menu.add_command(label=self.tr("open_folder"), command=self.open_manual_folder)
        self.file_menu.add_command(label=self.tr("open_app_dir"), command=self.reset_to_app_path)
        self.file_menu.add_separator()
        self.file_menu.add_command(label=self.tr("settings"), command=self.open_settings)
        self.file_menu.add_separator()
        self.file_menu.add_command(label=self.tr("exit"), command=self.on_closing)
        self.menubar.add_cascade(label=self.tr("file"), menu=self.file_menu)
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.help_menu.add_command(label=self.tr("help"), command=self.show_help)
        self.help_menu.add_command(label=self.tr("check_for_updates"), command=lambda: self.check_for_new_release(manual_check=True))
        self.help_menu.add_separator()
        self.help_menu.add_command(label=self.tr("info"), command=self.show_info)
        self.menubar.add_cascade(label=self.tr("help"), menu=self.help_menu)
        self.root.config(menu=self.menubar)

    def setup_ui(self):
        self.paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned.pack(fill=tk.BOTH, expand=True)
        self.sidebar_frame = ttk.Frame(self.paned, width=self.sidebar_width)
        self.paned.add(self.sidebar_frame, weight=0)
        self.file_filter_frame = ttk.LabelFrame(self.sidebar_frame, text=self.tr("file_filter"), padding=5)
        self.file_filter_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        ttk.Label(self.file_filter_frame, text=self.tr("filename")).pack(anchor="w")
        ttk.Entry(self.file_filter_frame, textvariable=self.file_search_var).pack(fill=tk.X, pady=(0, 10))
        dropdown_row = ttk.Frame(self.file_filter_frame); dropdown_row.pack(fill=tk.X, pady=(0, 5))
        sort_col = ttk.Frame(dropdown_row); sort_col.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(sort_col, text=self.tr("sorting")).pack(anchor="w")
        sort_options = ["Name (A-Z)", "Name (Z-A)", "Datum (Neu zuerst)", "Datum (Alt zuerst)"]
        self.sort_dropdown = ttk.OptionMenu(sort_col, self.sort_var, self.sort_var.get(), *sort_options, command=self.on_sort_change)
        self.sort_dropdown.pack(fill=tk.X, padx=(0, 5))
        type_col = ttk.Frame(dropdown_row); type_col.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(type_col, text=self.tr("types")).pack(anchor="w")
        self.ext_menubutton = ttk.Menubutton(type_col, text=self.tr("select")); self.ext_menubutton.pack(fill=tk.X)
        self.ext_menu = tk.Menu(self.ext_menubutton, tearoff=0); self.ext_menubutton["menu"] = self.ext_menu
        self.rebuild_extension_checkboxes()
        self.tree = ttk.Treeview(self.sidebar_frame, selectmode="browse", show="tree")
        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        tree_scroll = ttk.Scrollbar(self.sidebar_frame, orient=tk.VERTICAL, command=self.tree.yview)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y); self.tree.configure(yscrollcommand=tree_scroll.set)
        self.tree.bind("<<TreeviewSelect>>", self.on_file_select)
        self.main_frame = ttk.Frame(self.paned); self.paned.add(self.main_frame, weight=1)
        self.toolbar = ttk.Frame(self.main_frame, padding=5); self.toolbar.pack(side=tk.TOP, fill=tk.X)
        ttk.Label(self.toolbar, text=self.tr("search")).pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar(); self.search_entry = ttk.Entry(self.toolbar, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, padx=5); self.search_entry.bind("<Return>", lambda e: self.perform_search())
        ttk.Button(self.toolbar, text=self.tr("btn_search"), command=self.perform_search).pack(side=tk.LEFT, padx=2)
        self.live_btn_ui = ttk.Checkbutton(self.toolbar, text=self.tr("live_view"), variable=self.live_view_active, command=self.on_live_view_toggle)
        self.live_btn_ui.pack(side=tk.LEFT, padx=15)
        self.scroll_btn_ui = ttk.Checkbutton(self.toolbar, text=self.tr("auto_scroll"), variable=self.auto_scroll_active)
        self.scroll_btn_ui.pack(side=tk.LEFT, padx=5)
        self.wrap_btn_ui = ttk.Checkbutton(self.toolbar, text=self.tr("word_wrap"), variable=self.word_wrap_active, command=self.toggle_word_wrap)
        self.wrap_btn_ui.pack(side=tk.LEFT, padx=15)

        self.filter_bar = ttk.LabelFrame(self.main_frame, text=self.tr("highlights"), padding=5); self.filter_bar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)
        self.rebuild_filter_buttons()

        initial_wrap = tk.WORD if self.word_wrap_active.get() else tk.NONE
        self.text_area = scrolledtext.ScrolledText(self.main_frame, wrap=initial_wrap, undo=True, font=("Consolas", 10))
        self.text_area.pack(fill=tk.BOTH, expand=True); self.update_text_tags()
        self.text_area.tag_configure("search_match", background="yellow", foreground="black")
        self.text_area.bind("<MouseWheel>", self.detect_manual_scroll)
        self.text_area.bind("<Button-4>", self.detect_manual_scroll); self.text_area.bind("<Button-5>", self.detect_manual_scroll)
        self.text_area.bind("<KeyRelease>", self.update_cursor_position_display)
        self.text_area.bind("<ButtonRelease-1>", self.update_cursor_position_display)
        self.text_area.bind("<FocusIn>", self.update_cursor_position_display)
        self.text_area.bind("<FocusOut>", self.clear_cursor_position_display)

        # Statusleiste
        self.status_bar = ttk.Frame(self.main_frame, padding=2, relief="sunken")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Widgets erstellen, aber nicht packen. Das macht update_status_bar.
        self.status_mtime_label = ttk.Label(self.status_bar, text="", anchor="e")
        self.mtime_sep = ttk.Separator(self.status_bar, orient=tk.VERTICAL)
        self.status_cursor_label = ttk.Label(self.status_bar, text="", anchor="e")
        self.cursor_sep = ttk.Separator(self.status_bar, orient=tk.VERTICAL)
        self.status_lines_label = ttk.Label(self.status_bar, text="", anchor="e")
        self.lines_sep = ttk.Separator(self.status_bar, orient=tk.VERTICAL)
        self.status_size_label = ttk.Label(self.status_bar, text="", anchor="e")
        self.size_sep = ttk.Separator(self.status_bar, orient=tk.VERTICAL)
        self.encoding_menubutton = ttk.Menubutton(self.status_bar, text="", style="Toolbutton", direction="above")
        self.encoding_menu = tk.Menu(self.encoding_menubutton, tearoff=0)
        self.encoding_menubutton["menu"] = self.encoding_menu
        self.build_encoding_menu()

        # Initialen Status der Statusleiste setzen
        self.update_status_bar()

    def on_sort_change(self, _):
        self.settings_modified = True; self.refresh_file_tree()

    def build_encoding_menu(self):
        self.encoding_menu.delete(0, tk.END)
        # Liste gängiger Encodings
        # Enthält die von Windows Notepad bekannten Formate sowie weitere Standards.
        encodings_to_offer = [
            'utf-8',       # Standard ohne BOM
            'utf-8-sig',   # UTF-8 mit BOM
            'utf-16-le',   # UTF-16 Little Endian (Windows Standard)
            'utf-16-be',   # UTF-16 Big Endian
            'cp1252',      # West-Europa (Windows "ANSI")
            'iso-8859-15', # Latin-9 (mit Euro-Zeichen)
            locale.getpreferredencoding(False)
        ]
        # Duplikate entfernen und sortieren
        unique_encodings = sorted(list(set(enc for enc in encodings_to_offer if enc)))
        for enc in unique_encodings:
            display_label = enc.upper()
            if self.last_detected_encoding and enc.lower() == self.last_detected_encoding.lower():
                display_label += f" ({self.tr('detected')})"
            self.encoding_menu.add_command(label=display_label, command=lambda e=enc: self.force_reload_with_encoding(e))

    def force_reload_with_encoding(self, encoding):
        if self.current_file: self.load_file(self.current_file, scroll_to_end=False, force_encoding=encoding)

    def clear_cursor_position_display(self, event=None):
        self.status_cursor_label.config(text="")

    def update_cursor_position_display(self, event=None):
        if not self.current_file:
            self.status_cursor_label.config(text="")
            return
        try:
            line, col = self.text_area.index(tk.INSERT).split('.')
            self.status_cursor_label.config(text=f"{self.tr('line')}: {line}, {self.tr('column')}: {int(col) + 1}")
        except Exception:
            self.status_cursor_label.config(text="")

    def update_relative_time(self):
        if self.current_file_mtime:
            absolute_time = datetime.fromtimestamp(self.current_file_mtime).strftime('%d.%m.%Y %H:%M:%S')
            relative_time = self.get_relative_time_string(self.current_file_mtime)
            mtime_str = f"{absolute_time} ({relative_time})"
            self.status_mtime_label.config(text=f"{self.tr('modified')}: {mtime_str}")
        
        self.root.after(1000, self.update_relative_time)

    def rebuild_extension_checkboxes(self):
        self.ext_menu.delete(0, tk.END)
        for ext in sorted(self.allowed_extensions):
            if ext not in self.ext_vars: self.ext_vars[ext] = tk.BooleanVar(value=True)
            display_name = ext if ext != "" else self.tr("no_ext")
            self.ext_menu.add_checkbutton(label=display_name, variable=self.ext_vars[ext], command=self.on_extension_filter_change)

    def on_extension_filter_change(self):
        self.settings_modified = True; self.refresh_file_tree()

    def on_live_view_toggle(self):
        self.auto_scroll_active.set(self.live_view_active.get())

    def toggle_word_wrap(self):
        self.settings_modified = True
        if self.word_wrap_active.get():
            self.text_area.config(wrap=tk.WORD)
        else:
            self.text_area.config(wrap=tk.NONE)

    def detect_manual_scroll(self, event):
        if self.auto_scroll_active.get():
            is_up = False
            if hasattr(event, 'delta'):
                if event.delta > 0: is_up = True
            elif event.num == 4: is_up = True
            if is_up: self.auto_scroll_active.set(False)

    def rebuild_filter_buttons(self):
        for widget in self.filter_bar.winfo_children(): widget.destroy()
        for rule in self.log_rules:
            name = rule["name"]
            cb = tk.Checkbutton(self.filter_bar, text=name, variable=self.filter_vars[name], command=self.on_filter_toggle, bg=rule["bg"], fg=rule["fg"], selectcolor=rule["bg"], activebackground=rule["bg"], activeforeground=rule["fg"], padx=5)
            cb.pack(side=tk.LEFT, padx=3)

    def update_text_tags(self):
        for tag in self.text_area.tag_names():
            if tag not in ["search_match", "sel"]: self.text_area.tag_delete(tag)
        for rule in self.log_rules: self.text_area.tag_configure(rule["name"], foreground=rule["fg"], background=rule["bg"])

    def on_filter_toggle(self):
        self.settings_modified = True; self.save_settings(); self.apply_log_highlighting()

    def open_settings(self):
        settings_win = tk.Toplevel(self.root); settings_win.title(self.tr("settings")); settings_win.geometry("700x600"); settings_win.transient(self.root); settings_win.grab_set()
        nb = ttk.Notebook(settings_win); nb.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        gen_tab = ttk.Frame(nb); nb.add(gen_tab, text=self.tr("tab_general"))
        opt_frame = ttk.LabelFrame(gen_tab, text=self.tr("path_structure"), padding=10); opt_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Checkbutton(opt_frame, text=self.tr("scan_subdirs"), variable=self.scan_subdirs).pack(anchor="w")
        ttk.Checkbutton(opt_frame, text=self.tr("auto_refresh"), variable=self.auto_refresh_tree).pack(anchor="w")
        lang_frame = ttk.Frame(opt_frame); lang_frame.pack(fill=tk.X, pady=5)
        ttk.Label(lang_frame, text=self.tr("language")).pack(side=tk.LEFT)
        lang_var = tk.StringVar(value=self.lang); lang_options = ["de", "en"]
        lang_menu = ttk.OptionMenu(lang_frame, lang_var, self.lang, *lang_options); lang_menu.pack(side=tk.LEFT, padx=10)
        def change_lang(new_l):
            if new_l != self.lang: self.lang = new_l; self.settings_modified = True; messagebox.showinfo(self.tr("title"), "Programm neu starten / Please restart.")
        lang_var.trace_add("write", lambda *args: change_lang(lang_var.get()))
        ext_mgmt_frame = ttk.LabelFrame(gen_tab, text=self.tr("manage_ext"), padding=10); ext_mgmt_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.ext_lb = tk.Listbox(ext_mgmt_frame); self.ext_lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        for e in sorted(self.allowed_extensions): self.ext_lb.insert(tk.END, e if e != "" else self.tr("no_ext"))
        ext_ctrl = ttk.Frame(ext_mgmt_frame); ext_ctrl.pack(side=tk.LEFT, padx=5, fill=tk.Y)
        self.new_ext_entry = ttk.Entry(ext_ctrl, width=15); self.new_ext_entry.pack(pady=2)
        ttk.Button(ext_ctrl, text=self.tr("add_ext"), command=self.add_extension).pack(fill=tk.X)
        ttk.Button(ext_ctrl, text=self.tr("delete"), command=self.remove_extension).pack(fill=tk.X, pady=5)
        rules_tab = ttk.Frame(nb); nb.add(rules_tab, text=self.tr("tab_highlights"))
        rules_frame = ttk.Frame(rules_tab, padding=10); rules_frame.pack(fill=tk.BOTH, expand=True)
        self.rules_listbox = tk.Listbox(rules_frame, font=("Segoe UI", 10)); self.rules_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        for r in self.log_rules: self.rules_listbox.insert(tk.END, r["name"])
        
        btn_list_frame = ttk.Frame(rules_frame); btn_list_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        ttk.Button(btn_list_frame, text="↑", width=3, command=lambda: self.move_rule(-1)).pack(pady=2)
        ttk.Button(btn_list_frame, text="↓", width=3, command=lambda: self.move_rule(1)).pack(pady=2)
        ttk.Button(btn_list_frame, text=self.tr("new"), command=lambda: self.open_rule_editor(settings_win)).pack(pady=10)
        ttk.Button(btn_list_frame, text=self.tr("edit"), command=lambda: self.open_rule_editor(settings_win, True)).pack(pady=2)
        ttk.Button(btn_list_frame, text=self.tr("delete"), command=self.delete_rule).pack(pady=2)
        
        # Tab 3: Updates
        updates_tab = ttk.Frame(nb); nb.add(updates_tab, text=self.tr("tab_updates"))
        update_frame = ttk.LabelFrame(updates_tab, text=self.tr("tab_updates"), padding=10); update_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Checkbutton(update_frame, text=self.tr("check_updates_on_startup"), variable=self.check_updates_on_startup_var).pack(anchor="w", pady=(0, 10))
        ttk.Button(update_frame, text=self.tr("check_for_updates"), command=lambda: self.check_for_new_release(manual_check=True)).pack(anchor="w")
        
        footer = ttk.Frame(settings_win, padding=10); footer.pack(fill=tk.X)
        def save_and_close(): self.settings_modified = True; self.save_settings(); settings_win.destroy()
        ttk.Button(footer, text=self.tr("save_close"), command=save_and_close).pack(side=tk.RIGHT)

    def add_extension(self):
        new_e = self.new_ext_entry.get().strip().lower()
        if not new_e or new_e == ".": return
        if not new_e.startswith("."): new_e = "." + new_e
        if new_e not in self.allowed_extensions:
            self.allowed_extensions.append(new_e); self.settings_modified = True; self.refresh_ext_listbox(); self.rebuild_extension_checkboxes()

    def refresh_ext_listbox(self):
        self.ext_lb.delete(0, tk.END)
        for e in sorted(self.allowed_extensions): self.ext_lb.insert(tk.END, e if e != "" else self.tr("no_ext"))

    def remove_extension(self):
        sel = self.ext_lb.curselection()
        if sel:
            display = self.ext_lb.get(sel)
            if display == self.tr("no_ext"): messagebox.showwarning(self.tr("warning"), self.tr("no_ext_warn")); return
            if display in self.allowed_extensions:
                self.allowed_extensions.remove(display); self.settings_modified = True; self.refresh_ext_listbox()
                if display in self.ext_vars: del self.ext_vars[display]
                self.rebuild_extension_checkboxes()

    def open_rule_editor(self, parent, edit=False):
        selection = self.rules_listbox.curselection()
        if edit and not selection: return
        idx = selection[0] if edit else None
        rule_data = self.log_rules[idx].copy() if edit else {"name": "", "fg": "black", "bg": "white", "aliases": []}
        editor_win = tk.Toplevel(parent); editor_win.title(self.tr("rule_editor")); editor_win.geometry("450x400"); editor_win.grab_set()
        content = ttk.Frame(editor_win, padding=15); content.pack(fill=tk.BOTH, expand=True)
        ttk.Label(content, text=self.tr("name")).pack(anchor="w"); name_entry = ttk.Entry(content)
        name_entry.pack(fill=tk.X, pady=(0, 10)); name_entry.insert(0, rule_data["name"])
        ttk.Label(content, text=self.tr("terms")).pack(anchor="w"); alias_entry = ttk.Entry(content)
        alias_entry.pack(fill=tk.X, pady=(0, 10)); alias_entry.insert(0, ", ".join(rule_data["aliases"]))
        fg_c, bg_c = rule_data["fg"], rule_data["bg"]
        def pick(m):
            nonlocal fg_c, bg_c
            c = colorchooser.askcolor(initialcolor=(fg_c if m == "fg" else bg_c))[1]
            if c:
                if m == "fg": fg_c = c; fg_p.config(bg=c)
                else: bg_c = c; bg_p.config(bg=c)
        f_frame = ttk.Frame(content); f_frame.pack(fill=tk.X, pady=10)
        fg_col = ttk.Frame(f_frame); fg_col.pack(side=tk.LEFT, expand=True)
        ttk.Label(fg_col, text=self.tr("text_color")).pack(); fg_p = tk.Label(fg_col, width=12, bg=fg_c, relief="ridge"); fg_p.pack(pady=2); ttk.Button(fg_col, text="...", command=lambda: pick("fg")).pack()
        bg_col = ttk.Frame(f_frame); bg_col.pack(side=tk.LEFT, expand=True)
        ttk.Label(bg_col, text=self.tr("bg_color")).pack(); bg_p = tk.Label(bg_col, width=12, bg=bg_c, relief="ridge"); bg_p.pack(pady=2); ttk.Button(bg_col, text="...", command=lambda: pick("bg")).pack()
        def save():
            name = name_entry.get().strip()
            if not name: return
            new_r = {"name": name, "fg": fg_c, "bg": bg_c, "aliases": [a.strip().upper() for a in alias_entry.get().split(",") if a.strip()]}
            if edit: self.log_rules[idx] = new_r
            else: self.log_rules.append(new_r)
            self.settings_modified = True; self.refresh_settings_ui(); editor_win.destroy()
        btn_f = ttk.Frame(content); btn_f.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        ttk.Button(btn_f, text=self.tr("cancel"), command=editor_win.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_f, text=self.tr("save"), command=save).pack(side=tk.RIGHT)

    def refresh_settings_ui(self):
        self.rules_listbox.delete(0, tk.END)
        for r in self.log_rules: self.rules_listbox.insert(tk.END, r["name"])

        # Filter-Variablen neu erstellen, um neue/gelöschte Regeln zu berücksichtigen
        saved_states = {name: var.get() for name, var in self.filter_vars.items()}
        self.filter_vars = {rule["name"]: tk.BooleanVar(value=saved_states.get(rule["name"], False)) for rule in self.log_rules}

        self.save_settings()
        self.rebuild_filter_buttons()
        self.update_text_tags()
        self.apply_log_highlighting()

    def move_rule(self, d):
        sel = self.rules_listbox.curselection()
        if sel:
            idx = sel[0]; n_idx = idx + d
            if 0 <= n_idx < len(self.log_rules): self.log_rules[idx], self.log_rules[n_idx] = self.log_rules[n_idx], self.log_rules[idx]; self.settings_modified = True; self.refresh_settings_ui(); self.rules_listbox.selection_set(n_idx)

    def delete_rule(self):
        sel = self.rules_listbox.curselection()
        if sel and messagebox.askyesno(self.tr("warning"), self.tr("delete_confirm")): self.log_rules.pop(sel[0]); self.settings_modified = True; self.refresh_settings_ui()

    def open_manual_file(self):
        p = filedialog.askopenfilename(filetypes=[("Log & Text", "*.log *.txt"), ("All", "*.*")])
        if p: self.current_file = p; self.last_mtime = os.path.getmtime(p); self.load_file(p)

    def open_manual_folder(self):
        p = filedialog.askdirectory()
        if p: self.current_scan_path = p; self.settings_modified = True; self.refresh_file_tree(); self.save_settings()

    def reset_to_app_path(self):
        self.current_scan_path = self.get_app_dir(); self.settings_modified = True; self.refresh_file_tree(); self.save_settings()

    def show_info(self): messagebox.showinfo(self.tr("info"), f"{self.tr('title')} v{self.APP_VERSION}\n\n{self.tr('copyright')}")
    def show_help(self): messagebox.showinfo(self.tr("help"), self.tr("help_text"))

    def refresh_file_tree(self):
        start_path = self.current_scan_path
        if not os.path.exists(start_path): return
        active_exts = [ext for ext, var in self.ext_vars.items() if var.get()]
        name_filter = self.file_search_var.get().lower()
        all_items = []
        if self.scan_subdirs.get():
            for root_dir, dirs, files in os.walk(start_path):
                for f in files:
                    ext = os.path.splitext(f)[1].lower()
                    if ext in active_exts and name_filter in f.lower():
                        full_p = os.path.join(root_dir, f); all_items.append({"path": full_p, "name": f, "rel": os.path.relpath(full_p, start_path), "mtime": os.path.getmtime(full_p)})
        else:
            for f in os.listdir(start_path):
                full_p = os.path.join(start_path, f)
                if os.path.isfile(full_p):
                    ext = os.path.splitext(f)[1].lower()
                    if ext in active_exts and name_filter in f.lower(): all_items.append({"path": full_p, "name": f, "rel": f, "mtime": os.path.getmtime(full_p)})
        cache_key = (tuple(active_exts), name_filter, self.sort_var.get(), len(all_items))
        if cache_key == self.tree_structure_cache: return
        self.tree_structure_cache = cache_key
        s_mode = self.sort_var.get()
        if s_mode == "Name (A-Z)": all_items.sort(key=lambda x: x["name"].lower())
        elif s_mode == "Name (Z-A)": all_items.sort(key=lambda x: x["name"].lower(), reverse=True)
        elif s_mode == "Datum (Neu zuerst)": all_items.sort(key=lambda x: x["mtime"], reverse=True)
        elif s_mode == "Datum (Alt zuerst)": all_items.sort(key=lambda x: x["mtime"])
        open_items = self.get_open_nodes(self.tree.get_children("")); sel_path = self.get_selected_path(); self.tree.delete(*self.tree.get_children())
        root_node = self.tree.insert("", "end", text=os.path.basename(start_path) or start_path, open=True)
        for item in all_items:
            parts = item["rel"].split(os.sep); curr_parent = root_node
            for i, part in enumerate(parts):
                if i == len(parts) - 1: self.tree.insert(curr_parent, "end", text=part, values=(item["path"],))
                else:
                    found = False
                    for child in self.tree.get_children(curr_parent):
                        if self.tree.item(child, "text") == part and not self.tree.item(child, "values"): curr_parent = child; found = True; break
                    if not found: curr_parent = self.tree.insert(curr_parent, "end", text=part, open=False)
        self.restore_open_nodes(self.tree.get_children(""), open_items)
        if sel_path: self.select_path_in_tree(self.tree.get_children(""), sel_path)

    def get_open_nodes(self, nodes):
        lst = []
        for n in nodes:
            if self.tree.item(n, "open"): lst.append(self.tree.item(n, "text")); lst.extend(self.get_open_nodes(self.tree.get_children(n)))
        return lst

    def restore_open_nodes(self, nodes, lst):
        for n in nodes:
            if self.tree.item(n, "text") in lst: self.tree.item(n, open=True); self.restore_open_nodes(self.tree.get_children(n), lst)

    def get_selected_path(self):
        sel = self.tree.selection(); return self.tree.item(sel[0], "values")[0] if sel and self.tree.item(sel[0], "values") else None

    def select_path_in_tree(self, nodes, target):
        for n in nodes:
            v = self.tree.item(n, "values")
            if v and v[0] == target: self.tree.selection_set(n); self.tree.see(n); return True
            if self.select_path_in_tree(self.tree.get_children(n), target): return True
        return False

    def on_file_select(self, event):
        sel = self.tree.selection()
        if sel:
            v = self.tree.item(sel[0], "values")
            if v and self.current_file != v[0]: self.current_file = v[0]; self.last_mtime = os.path.getmtime(v[0]); self.load_file(v[0])

    def load_file(self, path, scroll_to_end=False, force_encoding=None, is_recovery_load=False):
        content = ""
        file_info = {"encoding": "N/A", "size": None, "lines": None, "mtime": None}

        try:
            # Wenn der Benutzer die ursprünglich erkannte Kodierung erneut auswählt,
            # behandeln wir dies wie eine automatische Erkennung, um den "(ausgewählt)"-Zusatz zu entfernen.
            if force_encoding and self.last_detected_encoding and force_encoding.lower() == self.last_detected_encoding.lower():
                force_encoding = None

            file_info["size"] = os.path.getsize(path)
            file_info["mtime"] = os.path.getmtime(path)
            display_str = "N/A"
            actual_encoding = None

            if force_encoding:
                actual_encoding = force_encoding
                display_name = force_encoding.upper()
                if display_name == 'CP1252':
                    display_name = 'CP1252 (ANSI)'
                display_str = f"{display_name} ({self.tr('manual')})"
                with open(path, 'r', encoding=actual_encoding, errors='replace') as f:
                    content = f.read()
            else:
                # Automatische Erkennung
                with open(path, 'rb') as f: bom = f.read(4)
                
                detected_bom_encoding = None
                if bom.startswith(b'\xff\xfe'): detected_bom_encoding = 'utf-16-le'
                elif bom.startswith(b'\xfe\xff'): detected_bom_encoding = 'utf-16-be'
                elif bom.startswith(b'\xef\xbb\xbf'): detected_bom_encoding = 'utf-8-sig'
    
                if detected_bom_encoding:
                    actual_encoding = detected_bom_encoding
                    display_str = actual_encoding.upper()
                    with open(path, 'r', encoding=actual_encoding, errors='replace') as f:
                        content = f.read()
                else:
                    try:
                        with open(path, 'r', encoding='utf-8') as f: content = f.read()
                        actual_encoding = 'utf-8'
                        display_str = 'UTF-8'
                    except UnicodeDecodeError:
                        system_encoding = locale.getpreferredencoding(False)
                        with open(path, 'r', encoding=system_encoding, errors='replace') as f: content = f.read()
                        actual_encoding = system_encoding
                        display_str = system_encoding.upper()
                        if display_str == 'CP1252':
                            display_str = 'CP1252 (ANSI)'
                
                self.last_detected_encoding = actual_encoding
            
            file_info["encoding"] = display_str
            file_info["lines"] = len(content.splitlines())

            # --- UI aktualisieren ---
            curr_y = self.text_area.yview()[0]
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, content)
            self.apply_log_highlighting()

            self.build_encoding_menu()
            self.update_status_bar(**file_info)

            if scroll_to_end or self.auto_scroll_active.get(): self.text_area.see(tk.END)
            else: self.text_area.yview_moveto(curr_y)

            # Wenn der Ladevorgang erfolgreich war, speichern wir die verwendete Kodierung.
            # Dies überschreiben wir nicht bei einem Wiederherstellungs-Laden.
            if not is_recovery_load:
                self.current_file_encoding = actual_encoding

        except Exception as e:
            # Fehler dem Benutzer anzeigen
            if not scroll_to_end: messagebox.showerror(self.tr("error"), str(e))

            # Wenn ein manueller Ladeversuch fehlschlug, versuchen wir, mit der letzten
            # funktionierenden Kodierung wiederherzustellen.
            if force_encoding and not is_recovery_load and self.current_file_encoding:
                self.load_file(path, scroll_to_end=False, force_encoding=self.current_file_encoding, is_recovery_load=True)
            else:
                # Wenn die Wiederherstellung fehlschlägt oder nicht anwendbar ist, UI zurücksetzen.
                self.last_detected_encoding = None; self.build_encoding_menu()
                self.update_status_bar()
                self.text_area.delete("1.0", tk.END)

    def check_for_file_updates(self):
        if self.current_file and self.live_view_active.get():
            try:
                m = os.path.getmtime(self.current_file)
                if m > self.last_mtime:
                    self.last_mtime = m; self.load_file(self.current_file, True)
            except OSError: pass
        self.root.after(500, self.check_for_file_updates)

    def get_relative_time_string(self, timestamp):
        """Erzeugt einen relativen Zeit-String (z.B. 'vor 5 Minuten')."""
        now = datetime.now()
        dt_object = datetime.fromtimestamp(timestamp)
        delta = now - dt_object
        seconds = delta.total_seconds()

        # Deutsche Grammatik: "vor 5 Tagen"
        if self.lang == 'de':
            if seconds < 60: val = int(seconds); unit = self.tr("second") if val == 1 else self.tr("seconds"); return f"{self.tr('time_ago')} {val} {unit}"
            elif seconds < 3600: val = int(seconds / 60); unit = self.tr("minute") if val == 1 else self.tr("minutes"); return f"{self.tr('time_ago')} {val} {unit}"
            elif seconds < 86400: val = int(seconds / 3600); unit = self.tr("hour") if val == 1 else self.tr("hours"); return f"{self.tr('time_ago')} {val} {unit}"
            elif seconds < 2592000: val = int(seconds / 86400); unit = self.tr("day") if val == 1 else self.tr("days"); return f"{self.tr('time_ago')} {val} {unit}"
            elif seconds < 31536000: val = int(seconds / 2592000); unit = self.tr("month") if val == 1 else self.tr("months"); return f"{self.tr('time_ago')} {val} {unit}"
            else: val = int(seconds / 31536000); unit = self.tr("year") if val == 1 else self.tr("years"); return f"{self.tr('time_ago')} {val} {unit}"
        # Englische Grammatik: "5 days ago"
        else:
            if seconds < 60: val = int(seconds); unit = self.tr("second") if val == 1 else self.tr("seconds"); return f"{val} {unit} {self.tr('time_ago')}"
            elif seconds < 3600: val = int(seconds / 60); unit = self.tr("minute") if val == 1 else self.tr("minutes"); return f"{val} {unit} {self.tr('time_ago')}"
            elif seconds < 86400: val = int(seconds / 3600); unit = self.tr("hour") if val == 1 else self.tr("hours"); return f"{val} {unit} {self.tr('time_ago')}"
            elif seconds < 2592000: val = int(seconds / 86400); unit = self.tr("day") if val == 1 else self.tr("days"); return f"{val} {unit} {self.tr('time_ago')}"
            elif seconds < 31536000: val = int(seconds / 2592000); unit = self.tr("month") if val == 1 else self.tr("months"); return f"{val} {unit} {self.tr('time_ago')}"
            else: val = int(seconds / 31536000); unit = self.tr("year") if val == 1 else self.tr("years"); return f"{val} {unit} {self.tr('time_ago')}"

    def update_status_bar(self, encoding=None, size=None, lines=None, mtime=None):
        """Aktualisiert die Statusleiste dynamisch. Leere Felder werden ausgeblendet."""
        self.current_file_mtime = mtime

        # Alle Widgets der Statusleiste entfernen, um sie neu aufzubauen
        for widget in self.status_bar.winfo_children():
            widget.pack_forget()

        # --- Linke Seite ---
        if encoding:
            self.encoding_menubutton.config(text=f"{encoding} ▲", state=tk.NORMAL)
            self.encoding_menubutton.pack(side=tk.LEFT, padx=(5, 5))

        # --- Rechte Seite (von rechts nach links packen) ---
        is_right_side_visible = False

        # Zeitstempel
        if mtime is not None:
            self.status_mtime_label.pack(side=tk.RIGHT, padx=(5, 10))
            is_right_side_visible = True

        # Cursor-Position
        if lines is not None:
            if is_right_side_visible: self.mtime_sep.pack(side=tk.RIGHT, fill='y', padx=5)
            self.status_cursor_label.pack(side=tk.RIGHT, padx=5)
            is_right_side_visible = True

        # Zeilenanzahl
        if lines is not None:
            if is_right_side_visible: self.cursor_sep.pack(side=tk.RIGHT, fill='y', padx=5)
            self.status_lines_label.config(text=f"{self.tr('lines')}: {f'{lines:,}'.replace(',', '.')}")
            self.status_lines_label.pack(side=tk.RIGHT, padx=5)
            is_right_side_visible = True

        # Dateigröße
        if size is not None:
            if is_right_side_visible: self.lines_sep.pack(side=tk.RIGHT, fill='y', padx=5)
            if size < 1024: size_str = f"{size} B"
            elif size < 1024**2: size_str = f"{size/1024:.1f} KB"
            else: size_str = f"{size/1024**2:.2f} MB"
            self.status_size_label.config(text=f"{self.tr('size')}: {size_str}")
            self.status_size_label.pack(side=tk.RIGHT, padx=5)
            is_right_side_visible = True

        # Separator zwischen linker und rechter Seite
        if encoding and is_right_side_visible:
            self.size_sep.pack(side=tk.LEFT, fill='y', padx=5)

    def check_for_new_release(self, manual_check=False):
        """Starts a background thread to check for a new release on GitHub."""
        thread = threading.Thread(target=self._perform_update_check, args=(manual_check,), daemon=True)
        thread.start()

    def _is_newer_version(self, remote_version_str, local_version_str):
        """Compares two version strings (e.g., '1.0.0' vs '0.2.1')."""
        try:
            remote_parts = [int(p) for p in remote_version_str.split('.')]
            local_parts = [int(p) for p in local_version_str.split('.')]
            max_len = max(len(remote_parts), len(local_parts))
            remote_parts.extend([0] * (max_len - len(remote_parts)))
            local_parts.extend([0] * (max_len - len(local_parts)))
            return remote_parts > local_parts
        except (ValueError, IndexError):
            return False

    def _perform_update_check(self, manual_check=False):
        """Performs the actual network request and version comparison."""
        API_URL = "https://api.github.com/repos/hellodosi/Logfile-Viewer/releases/latest"
        try:
            with urllib.request.urlopen(API_URL, timeout=5) as response:
                if response.status == 200:
                    data = json.load(response)
                    latest_version_tag = data.get("tag_name", "v0.0.0")
                    release_url = data.get("html_url")
                    latest_version = latest_version_tag.lstrip('v')
                    if self._is_newer_version(latest_version, self.APP_VERSION):
                        message = self.tr("update_available").format(version=latest_version)
                        if messagebox.askyesno(self.tr("update_title"), message):
                            webbrowser.open_new_tab(release_url)
                    elif manual_check:
                        messagebox.showinfo(self.tr("no_update_title"), self.tr("no_update_available"))
        except Exception as e:
            # Bei manueller Prüfung eine Fehlermeldung anzeigen, ansonsten still ignorieren.
            if manual_check:
                messagebox.showerror(self.tr("error"), self.tr("update_check_failed"))
            else:
                pass # Automatische Prüfung wird still ignoriert

    def check_for_tree_updates(self):
        if self.auto_refresh_tree.get(): self.refresh_file_tree()
        self.root.after(5000, self.check_for_tree_updates)

    def apply_log_highlighting(self):
        for r in self.log_rules: self.text_area.tag_remove(r["name"], "1.0", tk.END)
        lines = self.text_area.get("1.0", tk.END).splitlines()
        for i, line in enumerate(lines):
            up = line.upper()
            for r in self.log_rules:
                if self.filter_vars.get(r["name"]) and self.filter_vars[r["name"]].get() and any(a in up for a in r["aliases"]): self.text_area.tag_add(r["name"], f"{i+1}.0", f"{i+1}.end"); break

    def perform_search(self):
        self.text_area.tag_remove("search_match", "1.0", tk.END); s = self.search_var.get()
        if not s: return
        start = "1.0"
        while True:
            start = self.text_area.search(s, start, tk.END, nocase=True)
            if not start: break
            end = f"{start}+{len(s)}c"; self.text_area.tag_add("search_match", start, end); start = end

if __name__ == "__main__":
    root = tk.Tk(); app = LogViewerApp(root); root.mainloop()