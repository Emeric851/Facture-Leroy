from pathlib import Path
from datetime import datetime
import re
import time

DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)

class InvoiceService:

    def __init__(self, page, log_callback=None):
        self.page = page
        self.log = log_callback or print
        self.results = []

    def sanitize(self, text):
        return re.sub(r'[\\/*?:"<>|]', "_", text)

    def download_invoices(self, year="2025"):

        self.log(f"Recherche des factures {year}...")

        self.page.goto(
            "https://www.leroymerlin.fr/espace-client/commandes"
        )

        time.sleep(5)

        visited = set()

        while True:

            buttons = self.page.locator(
                "text=/Facture|Télécharger|PDF/i"
            )

            count = buttons.count()

            self.log(f"{count} éléments détectés")

            for i in range(count):

                try:
                    btn = buttons.nth(i)
                    text = btn.inner_text(timeout=2000)

                    if text in visited:
                        continue

                    visited.add(text)

                    with self.page.expect_download(timeout=15000) as dl:
                        btn.click()

                    download = dl.value

                    filename = self.sanitize(
                        download.suggested_filename
                    )

                    path = DOWNLOAD_DIR / filename

                    download.save_as(path)

                    self.results.append({
                        "filename": filename,
                        "path": str(path),
                        "date": datetime.now().isoformat()
                    })

                    self.log(f"Téléchargé : {filename}")

                    time.sleep(1)

                except Exception as e:
                    self.log(f"Erreur : {e}")

            next_button = self.page.locator(
                "text=/Suivant|Next/i"
            )

            if next_button.count() > 0:
                try:
                    next_button.first.click()
                    self.page.wait_for_load_state("networkidle")
                    time.sleep(2)
                except:
                    break
            else:
                break

        return self.results
