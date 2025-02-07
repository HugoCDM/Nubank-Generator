from tkinter import *
import os
import pandas as pd
import re
from custom_hovertip import CustomTooltipLabel
from tkinter import filedialog as fd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

months_of_the_year = {
    '01': 'January',
    '02': 'February',
    '03': 'March',
    '04': 'April',
    '05': 'May',
    '06': 'June',
    '07': 'July',
    '08': 'August',
    '09': 'September',
    '10': 'October',
    '11': 'November',
    '12': 'December'
}


def nubank_app():
    global entry_dir, entry_period, label_doc, window

    window = Tk()
    window.geometry('320x205')
    window.title('Nubank Invoices')
    window.resizable(False, False)
    window.config(bg='#820ad2')

    # Labels
    label_top = Label(text=' Nubank Invoice Generator  ', bg='#820ad2', fg='white', font=(
        'Gill Sans', 14, 'bold'), borderwidth=10, highlightthickness=2)
    label_top.place(relx=0.5, rely=0.2, anchor='c')

    label_dir = Label(text='Directory:', bg='#820ad2',
                      fg='white', font=('Arial', 12), height=3)
    label_dir.place(relx=0.05, rely=0.28)

    label_period = Label(text='Period:', bg='#820ad2',
                         fg='white', font=('Arial', 12))
    label_period.place(relx=0.08, rely=0.51)

    label_doc = Label(text='', font=('Arial', 12),
                      fg='lightgray', bg='#820ad2')
    label_doc.place(relx=0.22, rely=0.84)

    # Entrys
    entry_dir = Entry(width=34)
    entry_dir.place(relx=0.29, rely=0.385)
    entry_dir.focus()

    entry_period = Entry(width=34)
    entry_period.place(relx=0.29, rely=0.525)

    # Buttons
    button_generate = Button(window, text='Generate', width=10,
                             command=invoice_generate, relief='flat')
    button_generate.place(relx=0.692, rely=0.66)

    button_graph = Button(window, text='Graph',
                          width=10, command=graph, relief='flat')
    button_graph.place(relx=0.29, rely=0.66)

    # Tooltips
    CustomTooltipLabel(entry_dir, text=' The path where you can find \n the Nubank csv docs ',
                       hover_delay=100, foreground='#820ad2', width=26, background='lightgray')
    CustomTooltipLabel(entry_period, text=' Examples for the period: \n 01: January\n 01-10: From January to October \n all: Filter all months ',
                       hover_delay=100, foreground='#820ad2', background='lightgray', width=26)

    return window.mainloop()


def graph():
    global top
    global new_df

    # Screen attrs
    height = window.winfo_screenheight()
    width = window.winfo_screenwidth()
    top = Toplevel()
    # top.state('zoomed')
    top.resizable(False, False)
    top.geometry(f'{width}x{height}')
    top.title('Invoices Graph')
    top.configure(bg='white')

    try:
        new_invoices = new_invoice.replace('Nubank ', '').replace(
            ' invoice', '').replace('.xlsx', '').replace(' Invoice', '')
        label_title = Label(top, text=f'{new_invoices} Invoice Graph',
                            bg='white', font=('Arial', 30, 'bold'))
        label_title.place(relx=0.5, rely=0.04, anchor='c')

    except:
        label_title = Label(top, text='Invoice Graph',
                            bg='white', font=('Arial', 30, 'bold'))
        label_title.place(relx=0.5, rely=0.04, anchor='c')

    # Buttons
    btn_new_invoice = Button(top, text='Select a new invoice', font=(
        'Arial', 12), command=open_folder, width=20, bg='lightgray')
    btn_new_invoice.place(relx=0.04, rely=0.062)

    # DF
    new_df = pd.read_excel(new_invoice)
    attr_changed_description = new_df['Description'].value_counts()
    attr_changed_status = new_df['Status'].value_counts()

    # Charts' section

    # Pie
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    ax1.set_title('Values categorized by transaction')
    canvas = FigureCanvasTkAgg(fig1, master=top)
    canvas.get_tk_widget().place(relx=0.07, rely=0.1)
    ax1.pie(attr_changed_description, autopct='%1.1f%%')
    ax1.legend(new_df.Description.unique(),
               loc='upper left', bbox_to_anchor=(-0.7, 0.9))
    canvas.draw()

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.set_title('Values categorized by status')
    canvas = FigureCanvasTkAgg(fig2, master=top)
    canvas.get_tk_widget().place(relx=0.46, rely=0.1)
    ax2.pie(attr_changed_status, autopct='%1.1f%%')
    ax2.legend(new_df.Status.unique(), loc='best', bbox_to_anchor=(0.9, 0.9))
    canvas.draw()
    canvas.get_tk_widget().place()

    fig3, ax3 = plt.subplots(figsize=(10, 5))
    ax3.set_title('Values categorized by status')
    ax3.set_xlabel('Date')
    ax3.set_ylabel('Value')
    canvas = FigureCanvasTkAgg(fig3, master=top)
    canvas.get_tk_widget().place(relx=0.49, rely=0.48)
    ax3.plot(new_df.Date, new_df.Value)
    ax3.legend()
    canvas.draw()
    canvas.get_tk_widget().place()

    fig4, ax4 = plt.subplots(figsize=(10, 5))
    ax4.set_title('Values categorized by status')
    ax4.set_xlabel('Date')
    ax4.set_ylabel('Value')
    canvas = FigureCanvasTkAgg(fig4, master=top)
    canvas.get_tk_widget().place(relx=0.001, rely=0.48)
    ax4.scatter(new_df.Date, new_df.Value)
    ax4.legend(new_df.Status)
    canvas.draw()
    canvas.get_tk_widget().place()


def invoice_generate(event=None):
    global new_invoice, df

    try:
        # Focus on directory's entry
        entry_dir.focus()

        # Clear label
        label_doc.configure(text='')

        # List
        nubank = []

        # Selecionar filtro
        months = entry_period.get().split('-')

        # Directory
        directory = entry_dir.get()

        # All folders
        files = os.listdir(directory)

        # Regex pattern
        pattern = re.compile(r'Agência: \w+ Conta: \w+-\d')

        for file in files:
            try:
                if file.endswith('.csv'):

                    df = pd.read_csv(f'{directory}/{file}')

                    for index, archive in df.iterrows():

                        # Regex search
                        regex_description = re.search(pattern, archive.iloc[3])

                        # Date
                        date = archive.iloc[0]

                        # Changing description
                        new_description = str(
                            archive.iloc[3]).split(' - ')[0]

                        if new_description == 'Aplicação RDB':
                            new_description = 'Caixinha Nubank'

                        # Negative value
                        if archive.iloc[1] < 0:
                            status = 'Sent'
                            new_value = float(
                                str(archive.iloc[1]).replace('-', ''))

                        else:
                            status = 'Received'
                            new_value = float(archive.iloc[1])

                        # '-' splits when it gets more than 1 term
                        if '-' in archive.iloc[3]:
                            name = str(
                                archive.iloc[3]).split(' - ')[1]

                        else:
                            name = ' '

                        if regex_description:
                            ag_c = regex_description.group().replace(
                                'Agência', 'Ag').replace('Conta', '- C')

                        else:
                            ag_c = ' '

                        nubank.append([date, new_description, status,
                                       new_value, name, ag_c])

            except KeyError:
                pass

        df = pd.DataFrame(nubank, columns=[
            'Date', 'Description', 'Status', 'Value', 'Name', 'Ag/C'])
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

        try:
            if len(months) == 1 and months[0] == '02':
                beginning = f'2024-{months[0]}-01'
                fim = f'2024-{months[0]}-28'
                new_invoice = f'Nubank February invoice.xlsx'

                try:
                    df = df[(df['Date'] >= pd.to_datetime(beginning))
                            & (df['Date'] <= pd.to_datetime(fim))]
                except:
                    df = df[(df['Date'] >= pd.to_datetime(beginning)) & (
                        df['Date'] <= pd.to_datetime(f'2024-{months[0]}-29'))]

            elif len(months) == 1 and months[0] in months_of_the_year:
                beginning = f'2024-{months[0]}-01'
                fim = f'2024-{months[0]}-31'
                new_invoice = f'Nubank {
                    months_of_the_year[months[0]]} invoice.xlsx'

                try:
                    df = df[(df['Date'] >= pd.to_datetime(beginning))
                            & (df['Date'] <= pd.to_datetime(fim))]
                except:
                    df = df[(df['Date'] >= pd.to_datetime(beginning)) & (
                        df['Date'] <= pd.to_datetime(f'2024-{months[0]}-30'))]

            elif len(months) == 2 and months[0] < months[1] and (months[0] and months[1] in months_of_the_year):
                beginning = f'2024-{months[0]}-01'
                fim = f'2024-{months[1]}-31'
                new_invoice = f'Nubank {
                    months_of_the_year[months[0]]}-{months_of_the_year[months[1]]} invoice .xlsx'

                try:
                    df = df[(df['Date'] >= pd.to_datetime(beginning))
                            & (df['Date'] <= pd.to_datetime(fim))]
                except:
                    df = df[(df['Date'] >= pd.to_datetime(beginning)) & (
                        df['Date'] <= pd.to_datetime(f'2024-{months[1]}-30'))]

            elif len(months) == 2 and months[0] > months[1] and (months[0] and months[1] in months_of_the_year):
                beginning = f'2024-{months[1]}-01'
                fim = f'2024-{months[0]}-31'
                new_invoice = f'Nubank {
                    months_of_the_year[months[1]]}-{months_of_the_year[months[0]]} invoice .xlsx'

                try:
                    df = df[(df['Date'] >= pd.to_datetime(beginning))
                            & (df['Date'] <= pd.to_datetime(fim))]
                except:
                    df = df[(df['Date'] >= pd.to_datetime(beginning)) & (
                        df['Date'] <= pd.to_datetime(f'2024-{months[0]}-30'))]

            elif months[0] == 'all':
                df['Date'] = df['Date']
                new_invoice = 'Nubank General Invoice.xlsx'

            else:
                entry_period.delete(0, END)
                label_doc.configure(text='Incorrect Period', padx=103)

            df = df.sort_values(by='Date')

            df.to_excel(new_invoice, index=False)

            label_doc.configure(text='Document created successfully', padx=0)
            entry_dir.delete(0, END)
            entry_period.delete(0, END)
            label_doc.after(2500, lambda: label_doc.configure(text=''))

        except PermissionError:
            label_doc.configure(
                text='File already created. Close the Excel!', padx=0)
            pass

    except FileNotFoundError:
        entry_dir.delete(0, END)
        entry_period.delete(0, END)
        label_doc.configure(text='Incorrect directory', padx=97)
        pass

    except UnboundLocalError:
        pass


def update_graph():
    global label_title

    try:
        if label_title:
            label_title.destroy()
    except:
        pass

    try:
        new_invoices = new_invoice.replace('Nubank ', '').replace(
            ' invoice', '').replace('.xlsx', '').replace(' Invoice', '')
        label_title = Label(top, text=f'{new_invoices} Invoice Graph',
                            bg='white', font=('Arial', 30, 'bold'))
        label_title.place(relx=0.5, rely=0.04, anchor='c')

    except:
        label_title = Label(top, text='Invoice Graph',
                            bg='white', font=('Arial', 30, 'bold'))
        label_title.place(relx=0.5, rely=0.04, anchor='c')

    attr_changed_description = new_df['Description'].value_counts()
    attr_changed_status = new_df['Status'].value_counts()

    # Charts' section

    # Pie
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    ax1.set_title('Values categorized by transaction')
    canvas = FigureCanvasTkAgg(fig1, master=top)
    canvas.get_tk_widget().place(relx=0.07, rely=0.1)
    ax1.pie(attr_changed_description, autopct='%1.1f%%')
    ax1.legend(new_df.Description.unique(), loc='upper left',
               bbox_to_anchor=(-0.7, 0.87))
    canvas.draw()

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.set_title('Values categorized by status')
    canvas = FigureCanvasTkAgg(fig2, master=top)
    canvas.get_tk_widget().place(relx=0.46, rely=0.1)
    ax2.pie(attr_changed_status, autopct='%1.1f%%')
    ax2.legend(new_df.Status.unique(), loc='best', bbox_to_anchor=(0.9, 0.9))
    canvas.draw()
    canvas.get_tk_widget().place()

    fig3, ax3 = plt.subplots(figsize=(10, 5))
    ax3.set_title('Values categorized by status')
    ax3.set_xlabel('Date')
    ax3.set_ylabel('Value')
    canvas = FigureCanvasTkAgg(fig3, master=top)
    canvas.get_tk_widget().place(relx=0.49, rely=0.48)
    ax3.plot(new_df.Date, new_df.Value)
    ax3.legend()
    # ax3.legend(['Enviado', 'Recebido'], loc='best', bbox_to_anchor=(0.9, 0.9))
    canvas.draw()
    canvas.get_tk_widget().place()

    fig4, ax4 = plt.subplots(figsize=(10, 5))
    ax4.set_title('Values categorized by status')
    ax4.set_xlabel('Date')
    ax4.set_ylabel('Value')
    canvas = FigureCanvasTkAgg(fig4, master=top)
    canvas.get_tk_widget().place(relx=0.001, rely=0.48)
    ax4.scatter(new_df.Date, new_df.Value)
    ax4.legend(new_df.Status)
    # print(type(df_p.Status))
    # ax3.legend(['Enviado', 'Recebido'], loc='best', bbox_to_anchor=(0.9, 0.9))
    canvas.draw()
    canvas.get_tk_widget().place()


def open_folder():
    global new_invoice, new_df

    new_invoice = fd.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])

    if new_invoice:
        new_invoice = os.path.basename(new_invoice)
        new_df = pd.read_excel(new_invoice)
        update_graph()


if __name__ == '__main__':
    nubank_app()
