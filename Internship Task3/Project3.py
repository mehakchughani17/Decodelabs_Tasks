import tkinter as tk
from tkinter import scrolledtext, messagebox
import math
from collections import Counter
from datetime import datetime

# ── Job role database ──────────────────────────────────────────────────────
JOB_ROLES = {
    "Software Engineer": [
        "python", "java", "c++", "algorithms", "data structures",
        "git", "problem solving", "oop", "debugging", "testing"
    ],
    "Data Scientist": [
        "python", "machine learning", "statistics", "pandas", "numpy",
        "data analysis", "visualization", "sql", "tensorflow", "research"
    ],
    "Machine Learning Engineer": [
        "python", "machine learning", "deep learning", "tensorflow",
        "pytorch", "neural networks", "algorithms", "mathematics", "data", "ai"
    ],
    "DevOps Engineer": [
        "cloud computing", "automation", "python", "linux", "docker",
        "kubernetes", "ci/cd", "scripting", "networking", "monitoring"
    ],
    "Cloud Architect": [
        "cloud computing", "aws", "azure", "networking", "security",
        "automation", "infrastructure", "docker", "kubernetes", "system design"
    ],
    "System Administrator": [
        "linux", "networking", "automation", "scripting", "cloud computing",
        "security", "monitoring", "troubleshooting", "servers", "python"
    ],
    "Web Developer": [
        "html", "css", "javascript", "react", "nodejs",
        "python", "sql", "git", "api", "responsive design"
    ],
    "Cybersecurity Analyst": [
        "networking", "security", "linux", "ethical hacking", "python",
        "cryptography", "firewalls", "vulnerability assessment", "monitoring", "forensics"
    ],
    "Data Engineer": [
        "python", "sql", "data",
        "cloud computing",  "data warehousing", "automation"
    ],
    "AI Research Scientist": [
        "machine learning", "deep learning", "mathematics", "research",
        "python", "neural networks", "statistics", "nlp", "computer vision", "ai"
    ],
    "Mobile App Developer": [
        "java", "kotlin",  "react", "flutter",
        "api",  "oop", "debugging", "ui/ux"
    ],
    "Database Administrator": [
        "sql", "database design", "oracle", "mysql", "postgresql",
        "data modeling", "backup",  "security", "python"
    ],
    "Network Engineer": [
        "networking", "switching", "security",
        "linux", "troubleshooting", "cloud computing", "firewalls", "monitoring"
    ],
    "UI/UX Designer": [
        "ui/ux", "figma", "design", "prototyping", "user research",
        "css", "html", "wireframing", "accessibility", "responsive design"
    ],
    "Business Intelligence Analyst": [
        "sql", "data analysis", "visualization", "statistics", "excel",
        "power bi", "tableau", "reporting", "python", "business"
    ],
}

# ── TF-IDF + Cosine Similarity ─────────────────────────────────────────────
def build_tfidf(job_roles):
    N = len(job_roles)
    doc_freq = Counter()
    for skills in job_roles.values():
        for skill in set(skills):
            doc_freq[skill] += 1
    return {skill: math.log(N / freq) for skill, freq in doc_freq.items()}

def vectorize(skills, idf):
    tf = Counter(skills)
    total = len(skills)
    return {skill: (count / total) * idf.get(skill, 0) for skill, count in tf.items()}

def cosine_similarity(vec_a, vec_b):
    common = set(vec_a) & set(vec_b)
    dot = sum(vec_a[k] * vec_b[k] for k in common)
    mag_a = math.sqrt(sum(v ** 2 for v in vec_a.values()))
    mag_b = math.sqrt(sum(v ** 2 for v in vec_b.values()))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)

def recommend(user_skills, top_n=5):
    idf = build_tfidf(JOB_ROLES)
    user_clean = [s.lower().strip() for s in user_skills if s.strip()]
    user_vec = vectorize(user_clean, idf)
    results = []
    for role, role_skills in JOB_ROLES.items():
        role_vec = vectorize(role_skills, idf)
        score = cosine_similarity(user_vec, role_vec)
        matched = [s for s in user_clean if s in role_skills]
        results.append((role, score, matched))
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_n]


# ── Pastel palette ─────────────────────────────────────────────────────────
BG          = "#fdf6ff"        # soft lavender white
CARD        = "#ffffff"
CARD2       = "#f8f0ff"        # light lavender card
BORDER      = "#e8d5f5"        # lavender border
LAVENDER    = "#c084fc"        # main accent
LAVENDER_DK = "#a855f7"        # darker lavender for hover
MINT        = "#6ee7b7"        # mint green
PEACH       = "#fdba74"        # peach
PINK        = "#f9a8d4"        # soft pink
BLUE_SOFT   = "#93c5fd"        # soft blue
FG          = "#4a3f6b"        # deep purple-grey text
MUTED       = "#a89bbf"        # muted purple
ERROR       = "#f87171"        # soft red
INPUT_BG    = "#fdf4ff"
INPUT_BD    = "#ddd6fe"

# Role card accent colors cycling
ROLE_COLORS = ["#c084fc", "#6ee7b7", "#fdba74", "#f9a8d4", "#93c5fd",
               "#a5f3fc", "#fde68a", "#d9f99d", "#fca5a5", "#c4b5fd"]

FONT_UI    = ("Segoe UI", 10)
FONT_BOLD  = ("Segoe UI", 10, "bold")
FONT_MONO  = ("Consolas", 10)
FONT_SMALL = ("Segoe UI", 8)
FONT_TITLE = ("Segoe UI", 15, "bold")
FONT_H2    = ("Segoe UI", 11, "bold")
FONT_EMOJI = ("Segoe UI Emoji", 13)


# ── Rounded button helper ──────────────────────────────────────────────────
def styled_btn(parent, text, command, bg, fg, font=FONT_BOLD, pady=9):
    return tk.Button(
        parent, text=text, command=command,
        bg=bg, fg=fg, font=font,
        relief="flat", bd=0, cursor="hand2",
        activebackground=bg, activeforeground=fg,
        pady=pady, padx=14
    )


# ── Main App ───────────────────────────────────────────────────────────────
class TechRecommenderApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("✨ Career Recommender")
        self.root.geometry("820x640")
        self.root.minsize(640, 520)
        self.root.configure(bg=BG)

        self.skill_entries = []
        self.top_n_var = tk.IntVar(value=5)
        self._build_ui()

    # ── UI shell ───────────────────────────────────────────────────────────
    def _build_ui(self):
        # ── Header ────────────────────────────────────────────────────────
        header = tk.Frame(self.root, bg=CARD,
                          highlightthickness=1, highlightbackground=BORDER)
        header.pack(fill="x")

        inner_h = tk.Frame(header, bg=CARD, pady=12)
        inner_h.pack(fill="x", padx=24)

        # Logo blob
        logo_frame = tk.Frame(inner_h, bg="#ede9fe", width=44, height=44)
        logo_frame.pack(side="left", padx=(0, 12))
        logo_frame.pack_propagate(False)
        tk.Label(logo_frame, text="✨", font=("Segoe UI Emoji", 20),
                 bg="#ede9fe").place(relx=0.5, rely=0.5, anchor="center")

        title_col = tk.Frame(inner_h, bg=CARD)
        title_col.pack(side="left")
        tk.Label(title_col, text="Career Recommender",
                 font=FONT_TITLE, bg=CARD, fg=FG).pack(anchor="w")
        tk.Label(title_col, text="AI-powered career path suggestions based on your skills",
                 font=FONT_SMALL, bg=CARD, fg=MUTED).pack(anchor="w")

        self.clock_lbl = tk.Label(inner_h, text="", font=FONT_SMALL,
                                  bg=CARD, fg=MUTED, justify="right")
        self.clock_lbl.pack(side="right")
        self._tick()

        # ── Tab bar ────────────────────────────────────────────────────────
        tab_bar = tk.Frame(self.root, bg=CARD2,
                           highlightthickness=1, highlightbackground=BORDER)
        tab_bar.pack(fill="x")

        for name, emoji in [("Explore", "🔍"), ("Help", "💡"), ("About", "🌸")]:
            btn = tk.Button(
                tab_bar, text=f"  {emoji}  {name}  ", font=FONT_UI,
                bg=CARD2, fg=MUTED, relief="flat", bd=0,
                activebackground=CARD2, activeforeground=LAVENDER,
                cursor="hand2", pady=10,
                command=lambda n=name.lower(): self._switch(n)
            )
            btn.pack(side="left")
            setattr(self, f"tab_{name.lower()}", btn)

        # Content
        self.content = tk.Frame(self.root, bg=BG)
        self.content.pack(fill="both", expand=True)

        self._build_explore()
        self._build_help()
        self._build_about()
        self._switch("explore")

    def _switch(self, tab: str):
        for name in ("explore", "help", "about"):
            getattr(self, f"panel_{name}").pack_forget()
            getattr(self, f"tab_{name}").config(
                fg=LAVENDER_DK if name == tab else MUTED,
                font=FONT_BOLD if name == tab else FONT_UI
            )
        getattr(self, f"panel_{tab}").pack(fill="both", expand=True)

    # ── Explore panel ──────────────────────────────────────────────────────
    def _build_explore(self):
        self.panel_explore = tk.Frame(self.content, bg=BG)

        # Two columns
        left = tk.Frame(self.panel_explore, bg=BG, width=310)
        left.pack(side="left", fill="y", padx=(18, 10), pady=18)
        left.pack_propagate(False)

        right = tk.Frame(self.panel_explore, bg=BG)
        right.pack(side="left", fill="both", expand=True, padx=(0, 18), pady=18)

        # ── LEFT: skill inputs ─────────────────────────────────────────────
        skill_card = tk.Frame(left, bg=CARD,
                              highlightthickness=1, highlightbackground=BORDER)
        skill_card.pack(fill="x")

        header_row = tk.Frame(skill_card, bg="#faf5ff", pady=10)
        header_row.pack(fill="x")
        tk.Label(header_row, text="🌿  Your Skills",
                 font=FONT_H2, bg="#faf5ff", fg=FG).pack(side="left", padx=14)

        tk.Frame(skill_card, bg=BORDER, height=1).pack(fill="x")

        hint = tk.Label(skill_card,
                        text="Enter at least 3 skills below",
                        font=FONT_SMALL, bg=CARD, fg=MUTED)
        hint.pack(anchor="w", padx=14, pady=(8, 4))

        self.entries_frame = tk.Frame(skill_card, bg=CARD)
        self.entries_frame.pack(fill="x", padx=14, pady=(0, 8))

        for _ in range(5):
            self._add_entry_row()

        # Add / Remove
        btn_row = tk.Frame(skill_card, bg=CARD, pady=8)
        btn_row.pack(fill="x", padx=14)

        styled_btn(btn_row, "＋ Add Skill", self._add_entry_row,
                   bg="#f3e8ff", fg=LAVENDER_DK, font=FONT_SMALL, pady=6
                   ).pack(side="left", padx=(0, 8))

        styled_btn(btn_row, "− Remove", self._remove_entry_row,
                   bg="#fff1f2", fg=ERROR, font=FONT_SMALL, pady=6
                   ).pack(side="left")

        # Top-N
        tk.Frame(skill_card, bg=BORDER, height=1).pack(fill="x")

        n_frame = tk.Frame(skill_card, bg=CARD, pady=10)
        n_frame.pack(fill="x", padx=14)

        n_header = tk.Frame(n_frame, bg=CARD)
        n_header.pack(fill="x")
        tk.Label(n_header, text="🎯  Top results",
                 font=FONT_BOLD, bg=CARD, fg=FG).pack(side="left")
        self.n_label = tk.Label(n_header, text="5",
                                font=FONT_BOLD, bg="#f3e8ff",
                                fg=LAVENDER_DK, width=3)
        self.n_label.pack(side="right")

        tk.Scale(n_frame, from_=1, to=10, orient="horizontal",
                 variable=self.top_n_var, bg=CARD, fg=FG,
                 troughcolor=INPUT_BD, highlightthickness=0,
                 activebackground=LAVENDER, sliderrelief="flat",
                 showvalue=False,
                 command=lambda v: self.n_label.config(text=v)
                 ).pack(fill="x", pady=(4, 0))

        # Action buttons
        tk.Frame(skill_card, bg=BORDER, height=1).pack(fill="x")

        actions = tk.Frame(skill_card, bg=CARD, pady=12)
        actions.pack(fill="x", padx=14)

        styled_btn(actions, "✨  Find My Path", self._run,
                   bg=LAVENDER, fg="white", pady=10
                   ).pack(fill="x")

        styled_btn(actions, "🗑  Clear All", self._clear,
                   bg="#fff7ed", fg=PEACH, font=FONT_SMALL, pady=7
                   ).pack(fill="x", pady=(8, 0))

        # Suggestion chips
        chips_card = tk.Frame(left, bg=CARD,
                              highlightthickness=1, highlightbackground=BORDER)
        chips_card.pack(fill="x", pady=(12, 0))

        tk.Label(chips_card, text="💫  Try these skills",
                 font=FONT_BOLD, bg=CARD, fg=FG).pack(anchor="w", padx=14, pady=(10, 4))

        chips = ["python", "sql", "machine learning", "docker",
                 "react", "networking", "linux", "deep learning",
                 "aws", "statistics", "git", "security"]

        chip_frame = tk.Frame(chips_card, bg=CARD)
        chip_frame.pack(fill="x", padx=10, pady=(0, 10))

        for i, chip in enumerate(chips):
            color_bg = ROLE_COLORS[i % len(ROLE_COLORS)]
            btn = tk.Button(
                chip_frame, text=chip, font=FONT_SMALL,
                bg=color_bg , fg=FG,
                relief="flat", bd=0, cursor="hand2",
                padx=8, pady=4,
                command=lambda s=chip: self._fill_chip(s)
            )
            btn.grid(row=i // 3, column=i % 3, padx=3, pady=3, sticky="ew")

        chip_frame.columnconfigure(0, weight=1)
        chip_frame.columnconfigure(1, weight=1)
        chip_frame.columnconfigure(2, weight=1)

        # ── RIGHT: results ─────────────────────────────────────────────────
        results_header = tk.Frame(right, bg=CARD,
                                  highlightthickness=1, highlightbackground=BORDER)
        results_header.pack(fill="x")

        rh_inner = tk.Frame(results_header, bg=CARD, pady=10)
        rh_inner.pack(fill="x", padx=14)
        tk.Label(rh_inner, text="🌟  Career Recommendations",
                 font=FONT_H2, bg=CARD, fg=FG).pack(side="left")

        tk.Frame(results_header, bg=BORDER, height=1).pack(fill="x")

        self.result_canvas_frame = tk.Frame(right, bg=BG)
        self.result_canvas_frame.pack(fill="both", expand=True)

        # Scrollable result area
        self.result_canvas = tk.Canvas(self.result_canvas_frame, bg=BG,
                                       highlightthickness=0, bd=0)
        scrollbar = tk.Scrollbar(self.result_canvas_frame,
                                 orient="vertical",
                                 command=self.result_canvas.yview)
        self.result_canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.result_canvas.pack(side="left", fill="both", expand=True)

        self.results_inner = tk.Frame(self.result_canvas, bg=BG)
        self.canvas_window = self.result_canvas.create_window(
            (0, 0), window=self.results_inner, anchor="nw"
        )

        self.results_inner.bind("<Configure>", self._on_frame_configure)
        self.result_canvas.bind("<Configure>", self._on_canvas_configure)
        self.result_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Placeholder
        self._show_placeholder()

    def _on_frame_configure(self, event):
        self.result_canvas.configure(
            scrollregion=self.result_canvas.bbox("all")
        )

    def _on_canvas_configure(self, event):
        self.result_canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        self.result_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _show_placeholder(self):
        for w in self.results_inner.winfo_children():
            w.destroy()
        ph = tk.Frame(self.results_inner, bg=BG)
        ph.pack(expand=True, pady=60)
        tk.Label(ph, text="🌸", font=("Segoe UI Emoji", 40), bg=BG).pack()
        tk.Label(ph, text="Enter your skills and click\n✨ Find My Path",
                 font=("Segoe UI", 11), bg=BG, fg=MUTED,
                 justify="center").pack(pady=8)

    def _fill_chip(self, skill: str):
        for entry in self.skill_entries:
            if not entry.get().strip():
                entry.insert(0, skill)
                return
        self._add_entry_row()
        self.skill_entries[-1].insert(0, skill)

    def _add_entry_row(self):
        idx = len(self.skill_entries) + 1
        row = tk.Frame(self.entries_frame, bg=CARD)
        row.pack(fill="x", pady=3)

        tk.Label(row, text=f"{idx}", font=FONT_SMALL,
                 bg="#ede9fe", fg=LAVENDER_DK, width=2,
                 pady=4).pack(side="left", padx=(0, 6))

        entry = tk.Entry(
            row, bg=INPUT_BG, fg=FG, insertbackground=LAVENDER,
            font=FONT_UI, relief="flat", bd=6,
            highlightthickness=1,
            highlightbackground=INPUT_BD,
            highlightcolor=LAVENDER
        )
        entry.pack(side="left", fill="x", expand=True)
        entry.bind("<Return>", lambda e: self._run())
        self.skill_entries.append(entry)

        if len(self.skill_entries) == 1:
            entry.focus_set()

    def _remove_entry_row(self):
        if len(self.skill_entries) <= 3:
            messagebox.showwarning("Oopsiiii! 🌸",
                                   "You need at least 3 skill fields.",
                                   parent=self.root)
            return
        entry = self.skill_entries.pop()
        entry.master.destroy()

    # ── Run recommendation ─────────────────────────────────────────────────
    def _run(self):
        skills = [e.get().strip() for e in self.skill_entries if e.get().strip()]

        for w in self.results_inner.winfo_children():
            w.destroy()

        if len(skills) < 3:
            err = tk.Frame(self.results_inner, bg=BG)
            err.pack(pady=60)
            tk.Label(err, text="⚠️", font=("Segoe UI Emoji", 36), bg=BG).pack()
            tk.Label(err, text="Please enter at least 3 skills!",
                     font=FONT_H2, bg=BG, fg=ERROR).pack(pady=6)
            return

        top_n = self.top_n_var.get()
        results = recommend(skills, top_n)
        ts = datetime.now().strftime("%b %d, %Y  •  %I:%M %p")

        # Summary strip
        summary = tk.Frame(self.results_inner, bg="#fdf4ff",
                           highlightthickness=1, highlightbackground=BORDER)
        summary.pack(fill="x", padx=4, pady=(8, 4))

        tk.Label(summary,
                 text=f"✨  Showing top {top_n} matches for:  {' · '.join(skills)}",
                 font=FONT_SMALL, bg="#fdf4ff", fg=MUTED,
                 wraplength=380, justify="left"
                 ).pack(side="left", padx=12, pady=8)

        tk.Label(summary, text=ts, font=FONT_SMALL,
                 bg="#fdf4ff", fg=MUTED).pack(side="right", padx=12)

        # Result cards
        medals = ["🥇", "🥈", "🥉"]

        for i, (role, score, matched) in enumerate(results):
            pct = int(score * 100)
            color = ROLE_COLORS[i % len(ROLE_COLORS)]
            medal = medals[i] if i < 3 else f"#{i+1}"

            card = tk.Frame(self.results_inner, bg=CARD,
                            highlightthickness=1, highlightbackground=BORDER)
            card.pack(fill="x", padx=4, pady=5)

            # Colored left accent strip
            accent = tk.Frame(card, bg=color, width=5)
            accent.pack(side="left", fill="y")

            body = tk.Frame(card, bg=CARD, pady=10)
            body.pack(side="left", fill="both", expand=True, padx=12)

            # Rank + role name
            top_row = tk.Frame(body, bg=CARD)
            top_row.pack(fill="x")

            tk.Label(top_row, text=f"{medal}",
                     font=("Segoe UI Emoji", 16), bg=CARD).pack(side="left", padx=(0, 8))

            tk.Label(top_row, text=role,
                     font=FONT_H2, bg=CARD, fg=FG).pack(side="left")

            # Score badge
            badge_bg = color,
            tk.Label(top_row, text=f"  {pct}% match  ",
                     font=("Segoe UI", 9, "bold"),
                     bg=badge_bg, fg=FG
                     ).pack(side="right", padx=8)

            # Progress bar
            bar_outer = tk.Frame(body, bg="#f3e8ff", height=6)
            bar_outer.pack(fill="x", pady=(6, 4))
            bar_outer.pack_propagate(False)

            fill_w = max(1, int(score * 300))
            bar_fill = tk.Frame(bar_outer, bg=color, width=fill_w, height=6)
            bar_fill.place(x=0, y=0, relheight=1)

            # Matched skills chips
            if matched:
                chips_row = tk.Frame(body, bg=CARD)
                chips_row.pack(fill="x", pady=(2, 0))

                tk.Label(chips_row, text="Matched: ",
                         font=FONT_SMALL, bg=CARD, fg=MUTED).pack(side="left")

                for skill in matched:
                    tk.Label(chips_row,
                             text=f" {skill} ",
                             font=("Segoe UI", 8),
                             bg=color, fg=FG,
                             padx=4, pady=2
                             ).pack(side="left", padx=2)
            else:
                tk.Label(body,
                         text="No direct matches — based on overall profile similarity",
                         font=FONT_SMALL, bg=CARD, fg=MUTED).pack(anchor="w")

        # Bottom padding
        tk.Frame(self.results_inner, bg=BG, height=16).pack()
        self.result_canvas.yview_moveto(0)

    def _clear(self):
        for entry in self.skill_entries:
            entry.delete(0, "end")
        self._show_placeholder()
        if self.skill_entries:
            self.skill_entries[0].focus_set()

    # ── Help panel ─────────────────────────────────────────────────────────
    def _build_help(self):
        self.panel_help = tk.Frame(self.content, bg=BG)

        tk.Label(self.panel_help, text="💡  Help & Usage",
                 font=FONT_TITLE, bg=BG, fg=FG).pack(pady=(24, 4))
        tk.Label(self.panel_help,
                 text="How to use the Tech Stack Recommender",
                 font=FONT_SMALL, bg=BG, fg=MUTED).pack(pady=(0, 18))

        steps = [
            ("🌿  Step 1 — Enter Skills",
             "Type at least 3 skills into the input fields. Use the chips to auto-fill common ones."),
            ("🎯  Step 2 — Set Top-N",
             "Drag the slider to choose how many career path results you want (1–10)."),
            ("✨  Step 3 — Find My Path",
             "Click the purple button or press Enter. Results appear as ranked cards on the right."),
            ("🌸  Step 4 — Read Results",
             "Each card shows a match percentage bar, medal ranking, and which skills matched."),
            ("🗑  Step 5 — Clear & Retry",
             "Use 'Clear All' to reset everything and try a different skill set."),
        ]

        for title, desc in steps:
            card = tk.Frame(self.panel_help, bg=CARD,
                            highlightthickness=1, highlightbackground=BORDER)
            card.pack(fill="x", padx=80, pady=5, ipady=8, ipadx=14)

            tk.Label(card, text=title, font=FONT_BOLD,
                     bg=CARD, fg=FG, anchor="w").pack(anchor="w", padx=14, pady=(8, 2))
            tk.Label(card, text=desc, font=FONT_SMALL,
                     bg=CARD, fg=MUTED, anchor="w", wraplength=520,
                     justify="left").pack(anchor="w", padx=14, pady=(0, 8))

    # ── About panel ────────────────────────────────────────────────────────
    def _build_about(self):
        self.panel_about = tk.Frame(self.content, bg=BG)

        tk.Label(self.panel_about, text="✨",
                 font=("Segoe UI Emoji", 48), bg=BG).pack(pady=(28, 4))
        tk.Label(self.panel_about, text="Tech Stack Recommender",
                 font=FONT_TITLE, bg=BG, fg=FG).pack()
        tk.Label(self.panel_about, text="AI Recommendation System.",
                 font=FONT_SMALL, bg=BG, fg=MUTED).pack(pady=(2, 22))

        info = [
            ("🌿  Goal",
             "Map user skills to career paths using AI-powered similarity logic."),
            ("🔬  How It Works",
             "TF-IDF vectorization converts skills into weighted vectors. Cosine Similarity ranks job roles by closeness to your profile."),
            
            ("🛠  Technology",
             "Python  ·  Tkinter GUI "),
          
        ]

        for label, value in info:
            card = tk.Frame(self.panel_about, bg=CARD,
                            highlightthickness=1, highlightbackground=BORDER)
            card.pack(fill="x", padx=80, pady=4, ipady=6, ipadx=14)

            tk.Label(card, text=label, font=FONT_BOLD,
                     bg=CARD, fg=FG, anchor="w").pack(anchor="w", padx=14, pady=(8, 2))
            tk.Label(card, text=value, font=FONT_SMALL,
                     bg=CARD, fg=MUTED, anchor="w", wraplength=520,
                     justify="left").pack(anchor="w", padx=14, pady=(0, 8))

    # ── Clock ──────────────────────────────────────────────────────────────
    def _tick(self):
        now = datetime.now().strftime("%A, %b %d  •  %I:%M:%S %p")
        self.clock_lbl.config(text=now)
        self.root.after(1000, self._tick)


# ── Entry point ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    TechRecommenderApp(root)
    root.mainloop()
