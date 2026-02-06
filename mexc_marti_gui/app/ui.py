import tkinter as tk
from tkinter import messagebox

from app.logger import get_logger
from app.mexc_api import MexcClient


def run_app() -> None:
    logger = get_logger("ui")
    logger.info("UI started")

    root = tk.Tk()
    root.title("MEXC Спотовый Мартингейл-бот")

    form_frame = tk.Frame(root)
    form_frame.pack(padx=20, pady=10, fill=tk.X)

    tk.Label(form_frame, text="API Key").grid(row=0, column=0, sticky=tk.W, pady=4)
    api_key_entry = tk.Entry(form_frame, width=40)
    api_key_entry.grid(row=0, column=1, pady=4, sticky=tk.W)

    tk.Label(form_frame, text="API Secret").grid(row=1, column=0, sticky=tk.W, pady=4)
    api_secret_entry = tk.Entry(form_frame, width=40, show="*")
    api_secret_entry.grid(row=1, column=1, pady=4, sticky=tk.W)

    tk.Label(form_frame, text="Base URL").grid(row=2, column=0, sticky=tk.W, pady=4)
    base_url_entry = tk.Entry(form_frame, width=40)
    base_url_entry.insert(0, "https://api.mexc.com")
    base_url_entry.grid(row=2, column=1, pady=4, sticky=tk.W)

    status_label = tk.Label(root, text="Шаг 0: каркас готов")
    status_label.pack(padx=20, pady=5)

    def handle_check_connection() -> None:
        api_key = api_key_entry.get().strip()
        api_secret = api_secret_entry.get().strip()
        base_url = base_url_entry.get().strip()

        logger.info("Checking MEXC connection")
        client = MexcClient(api_key=api_key, api_secret=api_secret, base_url=base_url)
        success, message = client.check_connection()
        if success:
            logger.info("MEXC connection успешна")
            messagebox.showinfo("Успех", "Подключение к MEXC успешно")
        else:
            logger.error("MEXC connection ошибка: %s", message)
            messagebox.showerror("Ошибка", message)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    check_button = tk.Button(button_frame, text="Проверить подключение", command=handle_check_connection)
    check_button.pack(side=tk.LEFT, padx=5)

    exit_button = tk.Button(button_frame, text="Выход", command=root.destroy)
    exit_button.pack(side=tk.LEFT, padx=5)

    root.mainloop()
