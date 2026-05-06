import customtkinter as ctk
import threading

from ui.theme import *
from services.browser_service import BrowserService
from services.invoice_service import InvoiceService
from services.csv_service import CsvService

class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Leroy Merlin Factures")
        self.geometry("900x650")

        self.browser = BrowserService()
        self.browser.start()

        self.build_ui()

    def build_ui(self):

        title = ctk.CTkLabel(
            self,
            text="Leroy Merlin Factures Downloader",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=20)

        self.year_var = ctk.StringVar(value="2025")

        year_frame = ctk.CTkFrame(self)
        year_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            year_frame,
            text="Année"
        ).pack(side="left", padx=10)

        self.year_entry = ctk.CTkEntry(
            year_frame,
            textvariable=self.year_var,
            width=120
        )
        self.year_entry.pack(side="left", padx=10)

        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(fill="x", padx=20, pady=10)

        self.login_btn = ctk.CTkButton(
            btn_frame,
            text="Ouvrir Leroy Merlin",
            command=self.open_login
        )
        self.login_btn.pack(side="left", padx=10, pady=10)

        self.download_btn = ctk.CTkButton(
            btn_frame,
            text="Télécharger les factures",
            command=self.start_download
        )
        self.download_btn.pack(side="left", padx=10)

        self.progress = ctk.CTkProgressBar(self)
        self.progress.pack(fill="x", padx=20, pady=10)
        self.progress.set(0)

        self.logs = ctk.CTkTextbox(self)
        self.logs.pack(fill="both", expand=True, padx=20, pady=20)

    def log(self, message):
        self.logs.insert("end", message + "\n")
        self.logs.see("end")
        self.update()

    def open_login(self):
        self.browser.open_login()
        self.log("Navigateur ouvert")
        self.log("Connecte-toi manuellement")

    def start_download(self):
        thread = threading.Thread(target=self.download)
        thread.start()

    def download(self):

        self.progress.set(0.2)

        service = InvoiceService(
            self.browser.page,
            log_callback=self.log
        )

        data = service.download_invoices(
            self.year_var.get()
        )

        self.progress.set(0.8)

        csv_path = CsvService.export(data)

        self.progress.set(1)

        self.log(f"CSV exporté : {csv_path}")
        self.log("Téléchargement terminé")
