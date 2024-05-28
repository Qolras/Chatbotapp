import tkinter as tk
from tkinter import messagebox, Text, ttk, filedialog
import os
import requests
import webbrowser

# Configuration
CONFIG = {
    'api_key': 'APIKEY',
    'api_url': 'https://api.openai.com/v1/chat/completions'
}

class ChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat with AI")
        self.root.geometry("700x600")
        self.setup_gui()

    def setup_gui(self):
        style = ttk.Style()
        style.theme_use("clam")  # Modern theme

        # Frame for chat history
        self.frame_chat_history = ttk.Frame(self.root, padding="10")
        self.frame_chat_history.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.chat_history = Text(self.frame_chat_history, state=tk.DISABLED, wrap=tk.WORD, font=("Helvetica", 10))
        self.chat_history.pack(fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.chat_history, command=self.chat_history.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_history['yscrollcommand'] = self.scrollbar.set

        # Frame for user input and buttons
        self.frame_input = ttk.Frame(self.root, padding="10")
        self.frame_input.pack(fill=tk.X, padx=10, pady=5)

        self.text_input = Text(self.frame_input, height=3, wrap=tk.WORD, font=("Helvetica", 10))
        self.text_input.pack(fill=tk.X, side=tk.LEFT, padx=(0, 5), pady=5, expand=True)

        self.send_button = ttk.Button(self.frame_input, text="Send", command=self.submit_text, width=10)
        self.send_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.clear_button = ttk.Button(self.frame_input, text="Clear Chat", command=self.clear_chat_history, width=10)
        self.clear_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.save_button = ttk.Button(self.frame_input, text="Save Chat", command=self.save_chat_history, width=10)
        self.save_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.browse_button = ttk.Button(self.frame_input, text="Browse Folder", command=self.browse_folder, width=15)
        self.browse_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # PanedWindow for collapsible section
        self.paned_window = ttk.PanedWindow(self.root, orient=tk.VERTICAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Frame for treeview inside the PanedWindow
        self.frame_treeview = ttk.Frame(self.paned_window)
        self.paned_window.add(self.frame_treeview, weight=1)

        # Treeview for folder and file selection
        self.treeview = ttk.Treeview(self.frame_treeview, show="tree")
        self.treeview.pack(fill=tk.BOTH, expand=True)
        self.treeview.bind("<<TreeviewSelect>>", self.folder_or_file_selected)

        # Adjust the sash position after the window has been fully rendered
        self.root.after(100, lambda: self.paned_window.sashpos(0, 450))

        # Initialize conversation state
        self.reset_chatbot()

    def populate_treeview(self, folder_path):
        self.treeview.delete(*self.treeview.get_children())
        folder_id = self.treeview.insert("", "end", text=folder_path, open=True)
        self.add_items(folder_id, folder_path)

    def add_items(self, parent, folder_path):
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                folder_id = self.treeview.insert(parent, "end", text=item, values=(item_path,), open=False)
                # Populate the folder with a dummy item to show the expand icon
                self.treeview.insert(folder_id, "end", text="dummy")
            else:
                self.treeview.insert(parent, "end", text=item, values=(item_path,))

    def on_open_folder(self, event):
        selected_item = self.treeview.focus()
        item_path = self.treeview.item(selected_item, "values")[0]
        if os.path.isdir(item_path):
            self.treeview.delete(*self.treeview.get_children(selected_item))
            self.add_items(selected_item, item_path)

    def send_to_openai(self, text):
        headers = {
            'Authorization': f'Bearer {CONFIG["api_key"]}',
            'Content-Type': 'application/json'
        }
        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'user', 'content': text}],
            'max_tokens': 150
        }
        try:
            response = requests.post(CONFIG['api_url'], headers=headers, json=data)
            response_json = response.json()
            if response.status_code == 200:
                return response_json['choices'][0]['message']['content']
            else:
                return f"Error: {response_json.get('error', {}).get('message', 'Unknown error')}"
        except Exception as e:
            return f"Exception: {str(e)}"

    def submit_text(self):
        user_input = self.text_input.get("1.0", "end-1c").strip().lower()
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, f"You: {user_input}\n")

        if self.conversation_state['state'] == 'initial':
            response = self.send_to_openai(user_input)
            self.chat_history.insert(tk.END, f"AI: {response}\n")
        elif self.conversation_state['state'] == 'folder_selected':
            folder_choice = user_input
            if os.path.exists(folder_choice):
                self.populate_treeview(folder_choice)
            else:
                self.chat_history.insert(tk.END, "AI: Invalid folder path. Please choose a valid folder.\n")

        self.chat_history.config(state=tk.DISABLED)
        self.text_input.delete("1.0", "end")

    def folder_or_file_selected(self, event):
        selected_item = self.treeview.selection()[0]
        item_path = self.treeview.item(selected_item, "values")[0]
        if os.path.isdir(item_path):
            self.populate_treeview(item_path)
        else:
            self.open_file(item_path)

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.conversation_state['state'] = 'folder_selected'
            self.populate_treeview(folder_path)

    def open_file(self, file_path):
        try:
            if file_path.lower().endswith(".pdf"):
                webbrowser.open(f"file:///{file_path.replace('\\', '/')}")
                os.startfile(file_path)
            else:
                os.startfile(file_path)
            self.chat_history.config(state=tk.NORMAL)
            self.chat_history.insert(tk.END, f"AI: Opened file: {file_path}\n")
            self.chat_history.config(state=tk.DISABLED)
        except Exception as e:
            self.chat_history.config(state=tk.NORMAL)
            self.chat_history.insert(tk.END, f"AI: Unable to open the file: {str(e)}\n")
            self.chat_history.config(state=tk.DISABLED)

    def clear_chat_history(self):
        if messagebox.askyesno("Clear Chat", "Are you sure you want to clear the chat history?"):
            self.chat_history.config(state=tk.NORMAL)
            self.chat_history.delete("1.0", tk.END)
            self.chat_history.config(state=tk.DISABLED)
            self.reset_chatbot()

    def save_chat_history(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.chat_history.get("1.0", tk.END))
            messagebox.showinfo("Save Chat History", "Chat history saved successfully.")

    def reset_chatbot(self):
        self.conversation_state = {
            'state': 'initial',
            'folder_mapping': {},
            'current_folder': None,
            'files_in_folder': []
        }

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotApp(root)
    root.mainloop()
