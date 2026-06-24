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
        self.geometry("500x700")
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
                else: raise FileNotFoundError
        except Exception:
            ctk.CTkLabel(logo_frame, text="SHREE MARUTI", font=ctk.CTkFont(size=22, weight="bold"),
                         text_color=self.colors["maruti"]).pack(pady=(15, 0))
        ctk.CTkLabel(logo_frame, text="Integrated Logistics", font=ctk.CTkFont(size=10),
                     text_color=self.colors["text_sub"]).pack(pady=(2, 5))

        # Content
        content_card = ctk.CTkFrame(main_frame, fg_color=self.colors["card"], corner_radius=0, border_width=0)
        content_card.grid(row=1, column=0, sticky="ew")

        # --- CATEGORY ---
        ctk.CTkLabel(content_card, text="Category", font=ctk.CTkFont(size=14, weight="bold"), text_color=self.colors["text_main"], anchor="w").pack(fill="x", padx=20, pady=(15, 5))
        self.cat_var = ctk.StringVar(value="Standard Dox")
        cat_menu = ctk.CTkOptionMenu(content_card, variable=self.cat_var, 
                                     values=["Standard Dox", "Standard Non-Dox", "Fast Track Dox", "Fast Track Non-Dox"],
                                     fg_color=self.colors["input_bg"], button_color=self.colors["input_bg"],
                                     button_hover_color="#E5E7EB", corner_radius=10, height=40, 
                                     font=ctk.CTkFont(size=13, weight="bold"), text_color=self.colors["text_main"])
        cat_menu.pack(fill="x", padx=20, pady=(0, 15))

        # --- ZONE ---
        ctk.CTkLabel(content_card, text="Zone", font=ctk.CTkFont(size=14, weight="bold"), text_color=self.colors["text_main"], anchor="w").pack(fill="x", padx=20, pady=(10, 5))
        self.zone_var = ctk.StringVar(value="State")
        zone_menu = ctk.CTkOptionMenu(content_card, variable=self.zone_var, 
                                      values=["State", "ROI", "SPL"],
                                      fg_color=self.colors["input_bg"], button_color=self.colors["input_bg"],
                                      button_hover_color="#E5E7EB", corner_radius=10, height=40, 
                                      font=ctk.CTkFont(size=13, weight="bold"), text_color=self.colors["text_main"])
        zone_menu.pack(fill="x", padx=20, pady=(0, 15))

        # --- WEIGHT ---
        ctk.CTkLabel(content_card, text="Weight (Kg)", font=ctk.CTkFont(size=14, weight="bold"), text_color=self.colors["text_main"], anchor="w").pack(fill="x", padx=20, pady=(10, 5))
        self.weight_entry = ctk.CTkEntry(content_card, placeholder_text="Enter weight (e.g. 2.5)",
                                         fg_color=self.colors["input_bg"], border_color=self.colors["input_border"],
                                         border_width=1, corner_radius=10, height=40,
                                         font=ctk.CTkFont(size=13), text_color=self.colors["text_main"],
                                         placeholder_text_color="#9CA3AF")
        self.weight_entry.pack(fill="x", padx=20, pady=(0, 15))
        self.weight_entry.bind("<Return>", lambda e: self.calculate())

        # --- BUTTON ---
        self.calc_btn = ctk.CTkButton(content_card, text="CALCULATE RATE 📦",
                                      command=self.calculate, corner_radius=10, height=45,
                                      fg_color=self.colors["maruti"], hover_color="#B71C1C",
                                      font=ctk.CTkFont(size=14, weight="bold"))
        self.calc_btn.pack(fill="x", padx=20, pady=(5, 15))

        # --- RESULT ---
        self.result_card = ctk.CTkFrame(content_card, fg_color="#FFF3F3", corner_radius=12, border_width=1, border_color="#EF9A9A")
        self.result_card.pack(fill="x", padx=20, pady=(0, 20))
        ctk.CTkLabel(self.result_card, text="TOTAL AMOUNT", font=ctk.CTkFont(size=11, weight="bold"), text_color=self.colors["text_sub"]).pack(pady=(10, 0))
        self.amount_label = ctk.CTkLabel(self.result_card, text="₹0", font=ctk.CTkFont(size=36, weight="bold"), text_color=self.colors["maruti"])
        self.amount_label.pack(pady=(2, 2))
        self.detail_label = ctk.CTkLabel(self.result_card, text="Select category & enter weight", font=ctk.CTkFont(size=12), text_color=self.colors["text_sub"])
        self.detail_label.pack(pady=(0, 10))

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

        cat = self.cat_var.get()
        zone = self.zone_var.get().lower()

        # Docket Charge: Standard ₹5, Fast Track ₹10
        docket_charge = 10 if "Fast Track" in cat else 5

        base_rate = 0
        detail = ""

        try:
            # --- 1. STANDARD DOX ---
            if cat == "Standard Dox":
                if zone == "state":
                    # Special Logic for State Dox
                    if w <= 0.5:
                        base_rate = 100
                        detail = "0-500gm @ ₹100"
                    elif w <= 1.0:
                        base_rate = 120
                        detail = "Up to 1kg @ ₹120"
                    else:
                        extra_slabs = math.ceil((w - 1.0) / 0.5)
                        base_rate = 120 + (extra_slabs * 60) # 1.5kg = 120 + 60 = 180
                        detail = f"1kg ₹120 + {extra_slabs} addl slab(s) @ ₹60"
                else:
                    # ROI & SPL (Normal Slab Logic)
                    rates = {
                        "roi": {"base": 150, "addl": 100},
                        "spl": {"base": 180, "addl": 100}
                    }
                    r = rates[zone]
                    slabs = math.ceil(w / 0.5)
                    if slabs == 1:
                        base_rate = r["base"]
                        detail = f"1 slab (500gm) @ ₹{r['base']}"
                    else:
                        base_rate = r["base"] + ((slabs - 1) * r["addl"])
                        detail = f"{slabs} slabs: ₹{r['base']} + {(slabs-1)} addl @ ₹{r['addl']}"

            # --- 2. STANDARD NON-DOX ---
            elif cat == "Standard Non-Dox":
                # Simple Per Kg Logic
                rates = {"state": 100, "roi": 160, "spl": 200}
                cw = math.ceil(w)
                rate = rates[zone]
                base_rate = rate * cw
                detail = f"Non-Dox: ₹{rate}/kg × {cw}kg"

            # --- 3. FAST TRACK DOX ---
            elif cat == "Fast Track Dox":
                # Normal Slab Logic
                rates = {
                    "state": {"base": 400, "addl": 160},
                    "roi": {"base": 500, "addl": 260},
                    "spl": {"base": 560, "addl": 340}
                }
                r = rates[zone]
                slabs = math.ceil(w / 0.5)
                if slabs == 1:
                    base_rate = r["base"]
                    detail = f"1 slab (500gm) @ ₹{r['base']}"
                else:
                    base_rate = r["base"] + ((slabs - 1) * r["addl"])
                    detail = f"{slabs} slabs: ₹{r['base']} + {(slabs-1)} addl @ ₹{r['addl']}"

            # --- 4. FAST TRACK NON-DOX ---
            elif cat == "Fast Track Non-Dox":
                # Simple Per Kg Logic
                rates = {"state": 350, "roi": 550, "spl": 610}
                cw = math.ceil(w)
                rate = rates[zone]
                base_rate = rate * cw
                detail = f"FT Non-Dox: ₹{rate}/kg × {cw}kg"

        except Exception as e:
            self.show_error("Error calculating rates")
            return

        # Cost Chain: Docket -> Fuel 25% -> GST 18% -> Bus 10/kg -> Co-loader 10/kg -> Profit 50%
        subtotal = base_rate + docket_charge  
        subtotal = subtotal * 1.25  # Fuel
        subtotal = subtotal * 1.18  # GST
        
        cw = math.ceil(w)
        subtotal = subtotal + (10 * cw)  # Bus
        subtotal = subtotal + (10 * cw)  # Co-loader
        
        final = math.ceil(subtotal * 1.5)  # Profit

        self.show_result(final, f"Docket: ₹{docket_charge} | {detail}")

    def show_result(self, amount, detail):
        self.amount_label.configure(text=f"₹{amount}", text_color=self.colors["maruti"])
        self.detail_label.configure(text=detail)
        self.result_card.configure(fg_color="#FFF3F3")

    def show_error(self, message):
        self.amount_label.configure(text="⚠️", text_color="#F44336")
        self.detail_label.configure(text=message)
        self.result_card.configure(fg_color="#FFEBEE")

if __name__ == "__main__":
    app = ShreeMarutiApp()
    app.mainloop()
