# Nubank Invoice Generator App(in development)]


### A Tkinter-based application for analyzing Nubank CSV files and generating invoices through interactive graphs and charts and text from Excel


![nubank](https://github.com/user-attachments/assets/64402dda-e9bb-4b6a-be23-a5dc9bea1a1c)

### Built with
![68747470733a2f2f696d672e736869656c64732e696f2f62616467652f707974686f6e2d3336373041303f7374796c653d666c6174266c6f676f3d707974686f6e266c6f676f436f6c6f723d666664643534](https://github.com/user-attachments/assets/78a19a49-1893-43a5-9ffc-8d6d49d068c5)

## Usage
### 1. Directory Selection
- User must provide the file path where Nubank CSV files are stored
### 2. Period Selection
- The application supports some time periods:
  - A single month(e.g ***01*** referring to January)
  - A range between two months(eg ***04-09*** referring to April to September)
  - All months(***all***)

### 3. Buttons and Functionalities
#### 3.1 Graph Button
- Calls the graph() function
- Recognize your screen resolution and opens a fullscreen window displaying charts and graphs

#### 3.2 Generate Button
- Calls the invoice_generate() function
- Generates an invoice based on selected CSV data
- The file extension is .xlsx(Excel)

## Functions
### nubank_app()
- The main window(first image)

### update_graph()
- Updates the graph whenever a new invoice is generated or an existing one is selected

### open_folder()
- Allows you to open existing files already created
- Only Excel files allowed


## Image section


![nubank_imgs](https://github.com/user-attachments/assets/66eba00a-4507-486e-af9e-16c06a397350)


![nubank february graphs](https://github.com/user-attachments/assets/5d391c60-3712-421e-9d9a-2aa23e037517)










