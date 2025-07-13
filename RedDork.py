import tkinter as tk
from tkinter import messagebox
import webbrowser

DORKS = {
    "🔐 Login Pages": [
        "site:{domain} inurl:login",
        "site:{domain} inurl:signin",
        "site:{domain} intitle:'Login'"
    ],
    "🧪 Test Environments": [
        "site:{domain} inurl:test",
        "site:{domain} inurl:staging",
        "site:{domain} inurl:dev"
    ],
    "📄 Sensitive Documents": [
        "site:{domain} ext:doc OR ext:docx OR ext:pdf",
        "site:{domain} ext:xls OR ext:xlsx OR ext:csv"
    ],
    "🧷 Sensitive Parameters": [
        "site:{domain} inurl:password",
        "site:{domain} inurl:token",
        "site:{domain} inurl:apikey"
    ],
    "🧃 Juicy Extensions": [
        "site:{domain} ext:bak",
        "site:{domain} ext:old",
        "site:{domain} ext:backup"
    ],
    "🧩 PHP Extension with Parameters": [
        "site:{domain} inurl:.php?id=",
        "site:{domain} inurl:.php?page=",
        "site:{domain} inurl:.php?cat="
    ],
    "🔌 API Endpoints": [
        "site:{domain} inurl:/api/",
        "site:{domain} inurl:/v1/",
        "site:{domain} inurl:/v2/"
    ],
    "📊 High % inurl keywords": [
        "site:{domain} inurl:redirect",
        "site:{domain} inurl:url",
        "site:{domain} inurl:return"
    ],
    "🚨 Server Errors": [
        "site:{domain} intext:'Internal Server Error'",
        "site:{domain} intext:'502 Bad Gateway'",
        "site:{domain} intext:'403 Forbidden'"
    ],
    "💥 XSS Prone Parameters": [
        "site:{domain} inurl:q=",
        "site:{domain} inurl:s=",
        "site:{domain} inurl:search=",
        "site:{domain} inurl:query="
    ],
    "💉 SQLi Prone Parameters": [
        "site:{domain} inurl=id=",
        "site:{domain} inurl=catid=",
        "site:{domain} inurl=item="
    ],
    "🔀 Open Redirect": [
        "site:{domain} inurl=redirect=",
        "site:{domain} inurl=next="
    ],
    "🌐 SSRF Prone": [
        "site:{domain} inurl=url=",
        "site:{domain} inurl=dest="
    ],
    "🗂️ LFI Prone": [
        "site:{domain} inurl:file=",
        "site:{domain} inurl:include="
    ],
    "⚙️ RCE Prone": [
        "site:{domain} inurl=cmd=",
        "site:{domain} inurl:exec="
    ],
    "📤 File Upload": [
        "site:{domain} inurl:upload",
        "site:{domain} inurl:fileupload"
    ],
    "📚 API Docs": [
        "site:{domain} inurl:swagger",
        "site:{domain} inurl:api-docs"
    ],
    "🏢 Adobe Experience Manager (AEM)": [
        "site:{domain} inurl:/content",
        "site:{domain} inurl:/libs/granite"
    ],
    "🔓 Code Leaks": [
        "site:github.com {domain}",
        "site:gitlab.com {domain}"
    ],
    "📘 Code Sharing Platforms": [
        "site:jsfiddle.net {domain}",
        "site:codepen.io {domain}",
        "site:codebeautify.org {domain}"
    ],
    "☁️ Cloud Storage": [
        "site:storage.googleapis.com {domain}",
        "site:s3.amazonaws.com {domain}"
    ],
    "🧪 JFrog / Firebase": [
        "site:{domain} inurl:artifactory",
        "site:firebaseio.com intext:{domain}"
    ]
}

class DorkFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Google Dork Finder")
        self.root.geometry("980x700")
        self.root.configure(bg="#121212")

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self.root, text="Google Dork Finder", font=("Segoe UI", 20, "bold"),
                         bg="#121212", fg="red")
        title.pack(pady=12)

        input_frame = tk.Frame(self.root, bg="#121212")
        input_frame.pack(pady=5)

        tk.Label(input_frame, text="Target Domain:", font=("Segoe UI", 12),
                 fg="#cccccc", bg="#121212").pack(side="left", padx=5)

        self.domain_entry = tk.Entry(input_frame, font=("Segoe UI", 12), width=40)
        self.domain_entry.pack(side="left", padx=8)
        self.domain_entry.bind("<Return>", lambda e: self.generate_dorks())
        self.root.bind("<Return>", lambda e: self.generate_dorks())

        tk.Button(input_frame, text="Generate", command=self.generate_dorks,
                  font=("Segoe UI", 11, "bold"), bg="black", fg="red").pack(side="left", padx=5)

        self.canvas = tk.Canvas(self.root, bg="#1b1b1b", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.dork_frame = tk.Frame(self.canvas, bg="#1b1b1b")
        self.canvas.create_window((0, 0), window=self.dork_frame, anchor="nw")

        self.dork_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        if event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")

    def generate_dorks(self):
        for widget in self.dork_frame.winfo_children():
            widget.destroy()

        domain = self.domain_entry.get().strip()
        if not domain:
            messagebox.showerror("Missing Input", "Please enter a domain.")
            return

        for category, dorks in DORKS.items():
            cat_label = tk.Label(self.dork_frame, text=category,
                                 font=("Segoe UI", 13, "bold"), bg="#1b1b1b", fg="red")
            cat_label.pack(anchor="w", pady=(10, 0), padx=10)

            for dork in dorks:
                full_query = dork.replace("{domain}", domain)
                dork_label = tk.Label(self.dork_frame, text=full_query,
                                      font=("Consolas", 10), fg="#00ddff", bg="#1b1b1b", cursor="hand2")
                dork_label.pack(anchor="w", padx=25)
                dork_label.bind("<Button-1>", lambda e, q=full_query: self.open_google_search(q))

    def open_google_search(self, query):
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)

if __name__ == "__main__":
    root = tk.Tk()
    app = DorkFinderApp(root)
    root.mainloop()
