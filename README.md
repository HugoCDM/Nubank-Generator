# Nubank Invoice Generator App(in development)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

<p> A Tkinter-based application for analyzing Nubank CSV files and generating invoices through interactive graphs and charts and text from Excel.</p>




## 📥 Installation
1. Clone the repository and navigate into the directory
   ```bash
   git clone https://github.com/HugoCDM/Nubank-Generator.git
   cd Nubank-Generator
   ```
2. Create and activate a virtual environment(optional)
   ```bash
   python -m venv your_venv_name
   .\venv\Scripts\activate
   ```
3. Install the dependencies -requirements
   ```bash
   pip install -r requirements.txt 
   ```
If you have trouble with .\venv\Scripts\activate, run Windows PowerShell on your search bar as an administrator and write:
```bash
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser # Then type Y and press Enter. Go to step 2
```
## 🖱 Usage
### 1. Directory Selection
- User must provide the file path where Nubank CSV files are stored.
### 2. Period Selection
- The application supports some time periods:
  - A single month(e.g. ***01*** referring to January).
  - A range between two months(e.g. ***04-09*** referring to April to September).
  - All months(***all***).

### 3. Buttons and Functionalities
#### 3.1 Graph Button
- Calls the graph() function.
- Recognize your screen resolution and opens a fullscreen window displaying charts and graphs.

#### 3.2 Generate Button
- Calls the invoice_generate() function.
- Generates an invoice based on selected CSV data.
- The file extension created is .xlsx(Excel).

## ƒ Functions
### nubank_app()
- The main window.

### update_graph()
- Updates the graph whenever a new invoice is generated or an existing one is selected.

### open_folder()
- Allows you to open existing files already created.
- Only Excel files allowed.


## 🌅 Image section


![nubank_imgs](https://github.com/user-attachments/assets/66eba00a-4507-486e-af9e-16c06a397350)


![nubank february graphs](https://github.com/user-attachments/assets/5d391c60-3712-421e-9d9a-2aa23e037517)


### *Made by [Hugo Mello](https://github.com/HugoCDM)*







