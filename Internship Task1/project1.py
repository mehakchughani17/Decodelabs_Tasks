import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime
import threading
import time

# ── Rule-based responses ───────────────────────────────────────────────────
RESPONSES = {
   "hello": "Hi, I'm DecodeBot!, Your chatbot:) How can I help you today?",
    "hi": "Hello! I'm here to assist you.",
    "hey": "Heyy! I'm here for you.",
    "bye": "Goodbye! Have a great day.",
    "how are you": "I'm just a bot, but I'm doing great! Thanks for asking.",
    "i need help": "I would love to help but only can I respond to greetings, simple questions, and exit commands.",
    "who are you": "I'm a simple AI chatbot created for Project 1.",
    "i need information": "I only can give information about ai",
    "ok give me information about ai": "Sure! ask what do you wanna know about Ai",
    
    # AI related responses
    "are you ai": "Yes, I am an AI chatbot, My name is DecodeBot and designed to interact with you.",
    "what is ai": "AI means Artificial Intelligence — machines that can simulate human-like thinking and decision-making.",
    "how does ai work": "AI works by using rules, logic, and sometimes learning from data to solve problems or answer questions.",
    "examples of ai": "Examples of AI include chatbots, self-driving cars, recommendation systems, and voice assistants like Siri or Alexa.",
    "benefits of ai": "AI helps in automating tasks, analyzing large data, improving healthcare, enhancing customer service, and making technology smarter.",
    "future of ai": "The future of AI includes more advanced learning systems, ethical guardrails, and integration into everyday life to assist humans."
 }

# TKINTER  GUI 
# ── Colors & fonts 
BG          = "#0d1117"
CARD        = "#161b22"
BORDER      = "#30363d"
GREEN       = "#3fb950"
BLUE        = "#1f6feb"
FG          = "#e6edf3"
MUTED       = "#8b949e"
USER_BUBBLE = "#1f6feb"
BOT_BUBBLE  = "#21262d"
INPUT_BG    = "#21262d"

FONT_UI   = ("Segoe UI", 12)
FONT_BOLD = ("Segoe UI", 12, "bold")
FONT_MSG  = ("Consolas", 12)
FONT_SMALL= ("Segoe UI", 10)
FONT_TITLE= ("Segoe UI", 14, "bold")


# ── Main application ───────────────────────────────────────────────────────
class DecodeBotApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("DecodeBot")
        self.root.geometry("700x600")
        self.root.minsize(520, 460)
        self.root.configure(bg=BG)

        self.user_name: str | None = None
        self.typing = False

        self._build_ui()
        self._post_bot_message("Hi, I'm DecodeBot! 🤖 How can I help you today?")

    # ── UI construction ────────────────────────────────────────────────────
    def _build_ui(self):
        # ── Title bar ──────────────────────────────────────────────────────
        title_bar = tk.Frame(self.root, bg=BG, pady=8)
        title_bar.pack(fill="x", padx=16)

        tk.Label(title_bar, text="🤖  DecodeBot", font=FONT_TITLE,
                 bg=BG, fg=GREEN).pack(side="left")

        self.clock_label = tk.Label(title_bar, text="", font=FONT_SMALL,
                                    bg=BG, fg=MUTED, justify="right")
        self.clock_label.pack(side="right")
        self._update_clock()

        # ── Tab bar ────────────────────────────────────────────────────────
        tab_bar = tk.Frame(self.root, bg=CARD, pady=0)
        tab_bar.pack(fill="x")

        self.active_tab = tk.StringVar(value="chat")
        for tab_name in ("Chat", "Help", "About"):
            btn = tk.Button(
                tab_bar, text=tab_name, font=FONT_UI,
                bg=CARD, fg=MUTED, relief="flat", bd=0,
                activebackground=CARD, activeforeground=GREEN,
                cursor="hand2", padx=18, pady=8,
                command=lambda t=tab_name.lower(): self._switch_tab(t)
            )
            btn.pack(side="left")
            setattr(self, f"tab_{tab_name.lower()}", btn)

        # Clear button on the right
        tk.Button(
            tab_bar, text="🗑  Clear", font=FONT_SMALL,
            bg=CARD, fg=MUTED, relief="flat", bd=0,
            activebackground="#2d1515", activeforeground="#f85149",
            cursor="hand2", padx=12, pady=8,
            command=self._clear_chat
        ).pack(side="right", padx=4)

        separator = tk.Frame(self.root, bg=BORDER, height=1)
        separator.pack(fill="x")

        # ── Content area ───────────────────────────────────────────────────
        self.content_frame = tk.Frame(self.root, bg=BG)
        self.content_frame.pack(fill="both", expand=True)

        self._build_chat_panel()
        self._build_help_panel()
        self._build_about_panel()

        self._switch_tab("chat")

    def _switch_tab(self, tab: str):
        self.active_tab.set(tab)
        for name in ("chat", "help", "about"):
            frame = getattr(self, f"panel_{name}")
            frame.pack_forget()
            btn   = getattr(self, f"tab_{name}")
            btn.config(fg=GREEN if name == tab else MUTED)

        getattr(self, f"panel_{tab}").pack(fill="both", expand=True)

        if tab == "chat":
            self.input_box.focus_set()

    # ── Chat panel ─────────────────────────────────────────────────────────
    def _build_chat_panel(self):
        self.panel_chat = tk.Frame(self.content_frame, bg=BG)

        # Message area
        msg_frame = tk.Frame(self.panel_chat, bg=BG)
        msg_frame.pack(fill="both", expand=True, padx=12, pady=(10, 0))

        self.chat_display = scrolledtext.ScrolledText(
            msg_frame, bg=BG, fg=FG, font=FONT_MSG,
            relief="flat", bd=0, wrap="word",
            state="disabled", cursor="arrow",
            selectbackground=BLUE, selectforeground=FG
        )
        self.chat_display.pack(fill="both", expand=True)

        # Tag styles
        self.chat_display.tag_config("bot_name",  foreground=GREEN, font=("Segoe UI", 8, "bold"))
        self.chat_display.tag_config("user_name", foreground=BLUE,  font=("Segoe UI", 8, "bold"))
        self.chat_display.tag_config("bot_msg",   foreground=FG,    font=FONT_MSG, lmargin1=16, lmargin2=16)
        self.chat_display.tag_config("user_msg",  foreground=FG,    font=FONT_MSG, lmargin1=16, lmargin2=16)
        self.chat_display.tag_config("time_tag",  foreground=MUTED, font=("Segoe UI", 7))
        self.chat_display.tag_config("typing",    foreground=MUTED, font=("Segoe UI", 9, "italic"))
        self.chat_display.tag_config("divider",   foreground=BORDER)

        # Input bar
        input_frame = tk.Frame(self.panel_chat, bg=INPUT_BG,
                                highlightthickness=1, highlightbackground=BORDER,
                                highlightcolor=GREEN)
        input_frame.pack(fill="x", padx=12, pady=12)

        self.input_box = tk.Entry(
            input_frame, bg=INPUT_BG, fg=FG, insertbackground=GREEN,
            font=("Consolas", 10), relief="flat", bd=8,
        )
        self.input_box.pack(side="left", fill="x", expand=True)
        self.input_box.bind("<Return>", self._on_send)
        self.input_box.insert(0, "")

        send_btn = tk.Button(
            input_frame, text="Send ➤", font=FONT_BOLD,
            bg=GREEN, fg="#0d1117", relief="flat", bd=0,
            activebackground="#2ea043", activeforeground="#0d1117",
            cursor="hand2", padx=14, pady=6,
            command=self._on_send
        )
        send_btn.pack(side="right", padx=(0, 2), pady=2)

        hint = tk.Label(
            self.panel_chat,
            text='Press Enter to send  ·  Try: "hello",',
            font=FONT_SMALL, bg=BG, fg=MUTED
        )
        hint.pack(pady=(0, 6))

    # ── Help panel ─────────────────────────────────────────────────────────
    def _build_help_panel(self):
        self.panel_help = tk.Frame(self.content_frame, bg=BG)

        tk.Label(self.panel_help, text="Help & Commands",
                 font=FONT_TITLE, bg=BG, fg=GREEN).pack(pady=(20, 4))
        tk.Label(self.panel_help,
                 text="Type any phrase below exactly to get a response.",
                 font=FONT_SMALL, bg=BG, fg=MUTED).pack(pady=(0, 12))

        commands = [
            ("hello / hi / hey",          "Greeting responses"),
            ("how are you",               "Check how the bot is doing"),
            ("who are you",               "Learn about DecodeBot"),
            ("what is ai",                "AI definition"),
            ("how does ai work",          "How AI functions"),
            ("examples of ai",            "Real-world AI examples"),
            ("benefits of ai",            "Advantages of AI"),
            ("future of ai",              "AI future insights"),
            ("i need information",        "Request AI info"),
            ("ok give me information about ai", "Get AI info"),
            ("i am [your name]",          "Introduce yourself"),
            ("thanks / thank you",        "Express gratitude"),
            ("bye / exit",                "End the conversation"),
        ]

        list_frame = tk.Frame(self.panel_help, bg=BG)
        list_frame.pack(fill="both", expand=True, padx=24, pady=4)

        for cmd, desc in commands:
            row = tk.Frame(list_frame, bg=CARD,
                           highlightthickness=1, highlightbackground=BORDER)
            row.pack(fill="x", pady=3, ipady=6, ipadx=10)

            tk.Label(row, text=cmd, font=("Consolas", 9, "bold"),
                     bg=CARD, fg=GREEN, anchor="w", width=34).pack(side="left", padx=(10, 0))
            tk.Label(row, text=desc, font=FONT_SMALL,
                     bg=CARD, fg=MUTED, anchor="w").pack(side="left", padx=8)

    # ── About panel ────────────────────────────────────────────────────────
    def _build_about_panel(self):
        self.panel_about = tk.Frame(self.content_frame, bg=BG)

        tk.Label(self.panel_about, text="🤖", font=("Segoe UI", 40),
                 bg=BG).pack(pady=(30, 4))
        tk.Label(self.panel_about, text="DecodeBot",
                 font=("Segoe UI", 16, "bold"), bg=BG, fg=GREEN).pack()
        tk.Label(self.panel_about, text="Rule-Based AI Chatbot · Project 1",
                 font=FONT_SMALL, bg=BG, fg=MUTED).pack(pady=(2, 20))

        info = [
            ("Goal",             "Create a simple rule-based chatbot that responds to predefined user inputs."),
            ("Key Requirements", "Handle greetings and exit commands, use if-else logic for responses."),
            ("Key Skills",       "Control flow, decision-making logic, and basic AI concepts."),
            ("Technology",       "Python · Tkinter GUI"),
           
        ]

        for label, value in info:
            card = tk.Frame(self.panel_about, bg=CARD,
                            highlightthickness=1, highlightbackground=BORDER)
            card.pack(fill="x", padx=48, pady=4, ipady=8, ipadx=12)

            tk.Label(card, text=label, font=FONT_BOLD,
                     bg=CARD, fg=GREEN, anchor="w").pack(anchor="w", padx=10, pady=(6, 0))
            tk.Label(card, text=value, font=FONT_SMALL,
                     bg=CARD, fg=MUTED, anchor="w", wraplength=480, justify="left").pack(
                anchor="w", padx=10, pady=(2, 6))

    # ── Logic ──────────────────────────────────────────────────────────────
    def _on_send(self, event=None):
        text = self.input_box.get().strip()
        if not text or self.typing:
            return
        self.input_box.delete(0, "end")
        self._post_user_message(text)
        threading.Thread(target=self._get_reply, args=(text,), daemon=True).start()

    def _get_reply(self, text: str):
        self.typing = True
        self._show_typing()
        time.sleep(0.8 + (hash(text) % 5) * 0.1)   # simulated delay
        self._hide_typing()

        clean = text.lower().strip()

        # Name detection
        name_prefixes = ["i am ", "i'm ", "my name is ", "hi i am ", "hi i'm "]
        for prefix in name_prefixes:
            if clean.startswith(prefix):
                name = text[len(prefix):].strip().title()
                self.user_name = name
                self._post_bot_message(f"Nice to meet you, {name}! 😊")
                self.typing = False
                return

        # Personalised thanks
        if clean in ("thanks", "thank you") and self.user_name:
            self._post_bot_message(f"You're welcome, {self.user_name}! 😊")
            self.typing = False
            return

        reply = RESPONSES.get(clean, "I don't understand that. Please go to help to see stored commands. THANK YOU :)")
        self._post_bot_message(reply)
        self.typing = False

    def _post_bot_message(self, msg: str):
        ts = datetime.now().strftime("%I:%M %p")
        self.chat_display.config(state="normal")
        self.chat_display.insert("end", "DecodeBot  ", "bot_name")
        self.chat_display.insert("end", f"{ts}\n", "time_tag")
        self.chat_display.insert("end", f"  {msg}\n\n", "bot_msg")
        self.chat_display.config(state="disabled")
        self.chat_display.see("end")

    def _post_user_message(self, msg: str):
        ts  = datetime.now().strftime("%I:%M %p")
        name = self.user_name or "You"
        self.chat_display.config(state="normal")
        self.chat_display.insert("end", f"{name}  ", "user_name")
        self.chat_display.insert("end", f"{ts}\n", "time_tag")
        self.chat_display.insert("end", f"  {msg}\n\n", "user_msg")
        self.chat_display.config(state="disabled")
        self.chat_display.see("end")

    def _show_typing(self):
        self.chat_display.config(state="normal")
        self.chat_display.insert("end", "DecodeBot is typing...\n", "typing")
        self.chat_display.config(state="disabled")
        self.chat_display.see("end")
        self._typing_mark = self.chat_display.index("end-2l")

    def _hide_typing(self):
        self.chat_display.config(state="normal")
        # Remove the typing line
        try:
            self.chat_display.delete(self._typing_mark, f"{self._typing_mark} lineend+1c")
        except Exception:
            pass
        self.chat_display.config(state="disabled")

    def _clear_chat(self):
        if messagebox.askyesno("Clear Chat", "Clear all messages?", parent=self.root):
            self.chat_display.config(state="normal")
            self.chat_display.delete("1.0", "end")
            self.chat_display.config(state="disabled")
            self.user_name = None
            self._post_bot_message("Chat cleared! Hi again, I'm DecodeBot. How can I help?")

    def _update_clock(self):
        now = datetime.now().strftime("%A, %b %d %Y   %I:%M:%S %p")
        self.clock_label.config(text=now)
        self.root.after(1000, self._update_clock)


# ── Entry point ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = DecodeBotApp(root)
    root.mainloop()