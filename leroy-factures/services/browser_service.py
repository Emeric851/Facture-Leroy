from playwright.sync_api import sync_playwright
from pathlib import Path

SESSION_DIR = Path("browser/session")
SESSION_DIR.mkdir(parents=True, exist_ok=True)

class BrowserService:

    def __init__(self):
        self.playwright = None
        self.context = None
        self.page = None

    def start(self):
        self.playwright = sync_playwright().start()

        self.context = self.playwright.chromium.launch_persistent_context(
            user_data_dir=str(SESSION_DIR),
            headless=False,
            accept_downloads=True,
            slow_mo=200
        )

        self.page = self.context.new_page()

    def open_login(self):
        self.page.goto("https://www.leroymerlin.fr/")

    def close(self):
        if self.context:
            self.context.close()

        if self.playwright:
            self.playwright.stop()
