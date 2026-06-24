import customtkinter as ctk
import math
import os
import sys

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class ShreeMarutiApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Shree Maruti Rate Calculator")
        self.geometry("480x650")
        self.resizable(False, False)
        self.after(100, self.load_icon)

        self.colors = {
            "maruti": "#D32F2F",
            "bg": "#F0F2F5",
            "card": "#FFFFFF",
            "text_main": "#111827",
            "text_sub": "#6B7280",
            "input_bg": "#F3F4F6",
            "input_border": "#E5E7EB"
        }
        self.logo_img = None
        self.setup_ui()

    def load_icon(self):
        try:
            icon_path = resource_path("icon.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception:
            pass

    def setup_ui(self):
        main_frame = ctk.CTkFrame(self, fg_color=self.colors["bg"])
        main_frame.pack(fill="both", expand=True)
        main_frame.grid_columnconfigure(0, weight=1)

        # Header
        header_card = ctk.CTkFrame(main_frame, fg_color=self.colors["card"], corner_radius=0, border_width=0)
        header_card.grid(row=0, column=0, sticky="ew")

        logo_frame = ctk.CTkFrame(header_card, fg_color="transparent", height=100)
        logo_frame.pack(fill="x")
        logo_frame.pack_propagate(False)

        try:
            if HAS_PIL:
                img_path = resource_path("maruti_logo.png")
                if os.path.exists(img_path):
                    img = Image.open(img_path)
                    width_percent = (220 / float(img.size[0]))
                    hsize = int(float(img.size[1]) * width_percent)
                    img = img.resize((220, hsize), Image.Resampling.LANCZOS)
                    self.logo_img = ctk.CTkImage(light_image=img, size=(220, hsize))
                    ctk.CTkLabel(logo_frame, image=self.logo_img, text="").pack(pady=(10, 0))
                else:
                    raise FileNotFoundError
        except Exception:
            ctk.CTkLabel(logo_frame, text="SHREE MARUTI", font=ctk.CTkFont(size=24, weight="bold"),
                         text_color=self.colors["maruti"]).pack(pady=(15, 0))

        ctk.CTkLabel(logo_frame, text="Integrated Logistics", font=ctk.CTkFont(size=10),
                     text_color=self.colors["text_sub"]).pack(pady=(2, 5))

        # Content
        content_card = ctk.CTkFrame(main_frame, fg_color=self.colors["card"], corner_radius=0, border_width=0)
        content_card.grid(row=1, column=0, sticky="ew")

        self.add_title(content_card, "Shipment Details")

        # Zone
        self.zone_var = ctk.StringVar(value="MP")
        self.create_input_row(content_card, "Zone", is_menu=True, values=["MP", "ROI", "NE"])

        # Weight
        self.weight_entry = self.create_input_row(content_card, "Weight (Kg)", is_entry=True, placeholder="Enter weight")
        self.weight_entry.bind("<Return>", lambda e: self.calculate())

        # Button
        self.calc_btn = ctk.CTkButton(content_card, text="CALCULATE RATE 📦",
                                      command=self.calculate, corner_radius=10, height=45,
                                      fg_color=self.colors["maruti"], hover_color="#B71C1C",
                                      font=ctk.CTkFont(size=14, weight="bold"))
        self.calc_btn.pack(fill="x", padx=20, pady=(5, 15))

        # Result
        self.result_card = ctk.CTkFrame(content_card, fg_color="#FFF3F3", corner_radius=12, border_width=1, border_color="#EF9A9A")
        self.result_card.pack(fill="x", padx=20, pady=(0, 15))

        ctk.CTkLabel(self.result_card, text="TOTAL AMOUNT", font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=self.colors["text_sub"]).pack(pady=(8, 0))

        self.amount_label = ctk.CTkLabel(self.result_card, text="₹0", font=ctk.CTkFont(size=32, weight="bold"),
                                         text_color=self.colors["maruti"])
        self.amount_label.pack(pady=(2, 2))

        self.detail_label = ctk.CTkLabel(self.result_card, text="Select zone & enter weight",
                                         font=ctk.CTkFont(size=11), text_color=self.colors["text_sub"])
        self.detail_label.pack(pady=(0, 8))

    def add_title(self, parent, text):
        ctk.CTkLabel(parent, text=text, font=ctk.CTkFont(size=14, weight="bold"),
                     text_color=self.colors["text_main"], anchor="w").pack(fill="x", padx=20, pady=(15, 10))

    def create_input_row(self, parent, label_text, is_menu=False, is_entry=False, values=None, placeholder=""):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=(0, 8))

        ctk.CTkLabel(frame, text=label_text, font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=self.colors["text_main"], anchor="w").pack(fill="x", pady=(0, 4))

        if is_entry:
            entry = ctk.CTkEntry(frame, placeholder_text=placeholder,
                                 fg_color=self.colors["input_bg"], border_color=self.colors["input_border"],
                                 border_width=1, corner_radius=10, height=40,
                                 font=ctk.CTkFont(size=13), text_color=self.colors["text_main"],
                                 placeholder_text_color="#9CA3AF")
            entry.pack(fill="x")
            return entry
        else:
            menu = ctk.CTkOptionMenu(frame, variable=self.zone_var, values=values,
                                     fg_color=self.colors["input_bg"], button_color=self.colors["input_bg"],
                                     button_hover_color="#E5E7EB", corner_radius=10, height=40,
                                     font=ctk.CTkFont(size=13, weight="bold"), text_color=self.colors["text_main"],
                                     dropdown_text_color=self.colors["text_main"],
                                     dropdown_fg_color=self.colors["card"],
                                     dropdown_hover_color=self.colors["input_bg"])
            menu.pack(fill="x")
            return menu

    def calculate(self):
        try:
            wt_text = self.weight_entry.get().strip()
            if not wt_text:
                self.show_error("Please enter weight")
                return
            w = float(wt_text)
            if w <= 0:
                self.show_error("Weight must be greater than 0")
                return
        except ValueError:
            self.show_error("Please enter a valid number")
            return

        zone = self.zone_var.get().lower()

        # Shree Maruti DOX Rates (base from rate chart)
        rates = {
            "mp":  {"base_500": 17, "addl_500": 17},
            "roi": {"base_500": 45, "addl_500": 42},
            "ne":  {"base_500": 55, "addl_500": 52}
        }

        r = rates[zone]
        slabs = math.ceil(w / 0.5)  # Each 500gm = 1 slab

        if slabs == 1:
            base = r["base_500"]
            detail = f"1 slab (500gm) @ ₹{base}"
        else:
            base = r["base_500"] + ((slabs - 1) * r["addl_500"])
            detail = f"{slabs} slabs: 1st @ ₹{r['base_500']} + {slabs-1} addl @ ₹{r['addl_500']}"

        # Cost chain: Docket ₹5 → Fuel 25% → GST 18% → Bus ₹10 → Profit 50%
        subtotal = base + 5  # Docket
        subtotal = subtotal * 1.25  # Fuel
        subtotal = subtotal * 1.18  # GST
        subtotal = subtotal + 10  # Bus
        final = math.ceil(subtotal * 1.5)  # 50% profit

        self.show_result(final, detail)

    def show_result(self, amount, detail):
        self.amount_label.configure(text=f"₹{amount}")
        self.detail_label.configure(text=detail)

    def show_error(self, message):
        self.amount_label.configure(text="⚠️", text_color="#F44336")
        self.detail_label.configure(text=message)
        self.result_card.configure(fg_color="#FFEBEE")

if __name__ == "__main__":
    app = ShreeMarutiApp()
    app.mainloop()
