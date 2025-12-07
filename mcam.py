import cv2
import tkinter as tk
from PIL import Image, ImageTk

class FloatingCamera:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Floating Camera")
        
        # 1. Setup Frameless Window
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", 1)
        self.root.geometry("320x240+100+100")
        
        # 2. Setup Webcam
        self.cap = cv2.VideoCapture(0)

        # 3. Setup Video Label
        self.label = tk.Label(self.root, bg="black")
        self.label.pack(fill="both", expand=True)
        
        # 4. Bind Mouse Events to the VIDEO itself (No separate grip widget)
        self.label.bind("<ButtonPress-1>", self.on_click)
        self.label.bind("<ButtonRelease-1>", self.on_release)
        self.label.bind("<B1-Motion>", self.on_drag)
        self.label.bind("<Motion>", self.on_hover) # For changing cursor style
        
        # Right click to exit
        self.label.bind("<Button-3>", lambda e: self.root.quit())
        self.root.bind("<Escape>", lambda e: self.root.quit())

        # State variables
        self.drag_mode = None  # "move" or "resize"
        self.start_x = 0
        self.start_y = 0
        self.win_w = 0
        self.win_h = 0
        
        # Size of the invisible resize area (bottom right corner)
        self.resize_margin = 20 

        self.update_frame()
        self.root.mainloop()

    def on_hover(self, event):
        """Change cursor to let user know they can resize"""
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        
        # Check if mouse is in the bottom-right corner
        if (event.x > width - self.resize_margin) and (event.y > height - self.resize_margin):
            self.root.config(cursor="crosshair") # or "resize" depending on OS
        else:
            self.root.config(cursor="arrow")

    def on_click(self, event):
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        
        self.start_x = event.x
        self.start_y = event.y
        
        # Check if click is in the bottom-right corner
        if (event.x > width - self.resize_margin) and (event.y > height - self.resize_margin):
            self.drag_mode = "resize"
            self.win_w = width
            self.win_h = height
        else:
            self.drag_mode = "move"

    def on_release(self, event):
        self.drag_mode = None

    def on_drag(self, event):
        if self.drag_mode == "move":
            # Move the Window
            deltax = event.x - self.start_x
            deltay = event.y - self.start_y
            x = self.root.winfo_x() + deltax
            y = self.root.winfo_y() + deltay
            self.root.geometry(f"+{x}+{y}")
            
        elif self.drag_mode == "resize":
            # Resize the Window
            delta_w = event.x - self.start_x
            delta_h = event.y - self.start_y
            new_w = self.win_w + delta_w
            new_h = self.win_h + delta_h
            
            if new_w > 50 and new_h > 50:
                self.root.geometry(f"{new_w}x{new_h}")
                # Update stored dimensions so continuous dragging works smooth
                self.win_w = new_w
                self.win_h = new_h
                self.start_x = event.x
                self.start_y = event.y

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            win_w = self.root.winfo_width()
            win_h = self.root.winfo_height()

            if win_w > 1 and win_h > 1:
                # --- ASPECT FILL LOGIC ---
                h_img, w_img = frame.shape[:2]
                scale = max(win_w / w_img, win_h / h_img)
                
                new_w = int(w_img * scale)
                new_h = int(h_img * scale)
                frame = cv2.resize(frame, (new_w, new_h))
                
                x_center = new_w // 2
                y_center = new_h // 2
                x1 = max(0, int(x_center - win_w / 2))
                y1 = max(0, int(y_center - win_h / 2))
                
                frame = frame[y1:y1+win_h, x1:x1+win_w]
                
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=img)
                self.label.imgtk = imgtk
                self.label.configure(image=imgtk)
            
        self.label.after(10, self.update_frame)

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()

if __name__ == "__main__":
    FloatingCamera()
