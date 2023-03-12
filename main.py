import tkinter
import tkinter.messagebox
import customtkinter
import cx_Oracle
from random import randint

connection = cx_Oracle.connect("bd149/bd149@bd-dc.cs.tuiasi.ro:1539/orcl")

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

root = customtkinter.CTk()
root.geometry("700x400")
root.title("R&RKickz")
root.iconbitmap("sneakers.ico")


def insert():
    id = e_id.get()
    name = e_name.get()
    size = e_size.get()
    qty = e_qty.get()

    con = cx_Oracle.connect("bd149/bd149@bd-dc.cs.tuiasi.ro:1539/orcl")
    cursor = con.cursor()
    cursor.execute("select * from snkrs")
    rows = cursor.fetchall()
    for row in rows:
        #print(name,row[1],size,row[2])
        if str(name) == str(row[1]) and str(size) == str(row[2]):
            tkinter.messagebox.showinfo("Insert Status", "Duplicate product")
            return
    if id == "" or name == "" or size == "" or qty == "":
        tkinter.messagebox.showinfo("Insert Status", "All fields are required")
    if int(qty) < 0:
        tkinter.messagebox.showinfo("Insert Status", "Quantity must be greater or equal to 0")

    else:
        cursor.execute("insert into snkrs values('" + id + "','" + name + "','" + size + " ','" + qty + "')")
        cursor.execute("commit")

        e_id.delete(0, 'end')
        e_name.delete(0, 'end')
        e_size.delete(0, 'end')
        e_qty.delete(0, 'end')
        show()
        tkinter.messagebox.showinfo("Insert Status", "Inserted successfully")
        con.close()


def delete():
    if e_id.get() == "":
        tkinter.messagebox.showinfo("Delete Status", "ID is mandatory for deletion")
    else:
        con = cx_Oracle.connect("bd149/bd149@bd-dc.cs.tuiasi.ro:1539/orcl")
        cursor = con.cursor()
        cursor.execute("delete from snkrs where s_id='" + e_id.get() + "'")
        cursor.execute("commit")

        e_id.delete(0, 'end')
        e_name.delete(0, 'end')
        e_size.delete(0, 'end')
        e_qty.delete(0, 'end')
        show()
        tkinter.messagebox.showinfo("Delete Status", "Deleted successfully")
        con.close()


def update():
    id = e_id.get()
    name = e_name.get()
    size = e_size.get()
    qty = e_qty.get()

    if id == "" or name == "" or size == "" or qty == "":
        tkinter.messagebox.showinfo("Update Status", "All fields are required")
    if int(qty) < 0:
        tkinter.messagebox.showinfo("Insert Status", "Quantity must be greater or equal to 0")
    else:
        con = cx_Oracle.connect("bd149/bd149@bd-dc.cs.tuiasi.ro:1539/orcl")
        cursor = con.cursor()
        cursor.execute("update snkrs set nume='" + name + "', s_size ='" + size + "', qty = '" + qty + "'where s_id = '" + id + "'")
        cursor.execute("commit")

        e_id.delete(0, 'end')
        e_name.delete(0, 'end')
        e_size.delete(0, 'end')
        e_qty.delete(0, 'end')
        show()
        tkinter.messagebox.showinfo("Insert Status", "Inserted successfully")
        con.close()


def get():
    if e_id.get() == "":
        tkinter.messagebox.showinfo("Delete Status", "ID is mandatory for get")
    else:
        con = cx_Oracle.connect("bd149/bd149@bd-dc.cs.tuiasi.ro:1539/orcl")
        cursor = con.cursor()
        cursor.execute("select * from snkrs where s_id='" + e_id.get() + "'")
        rows = cursor.fetchall()
        e_name.delete(0, 'end')
        e_size.delete(0, 'end')
        e_qty.delete(0, 'end')
        for row in rows:
            e_name.insert(0, row[1])
            e_size.insert(0, row[2])
            e_qty.insert(0, row[3])
        show()
        con.close()


def show():
    con = cx_Oracle.connect("bd149/bd149@bd-dc.cs.tuiasi.ro:1539/orcl")
    cursor = con.cursor()
    cursor.execute("select * from snkrs")
    rows = cursor.fetchall()
    list.delete(0, list.size())

    for row in rows:
        insertData = str(row[0]) + " - model " + row[1] + ", marime " + str(row[2]) + ", bucati in stoc: " + str(row[3])
        list.insert(list.size() + 1, insertData)
    con.close()


con = cx_Oracle.connect("bd149/bd149@bd-dc.cs.tuiasi.ro:1539/orcl")
cursor = con.cursor()
cursor.execute("select id from orderss")
rows = cursor.fetchall()
print(rows)
if(rows == []):
    ctr=1
else:
    ctr=max(rows[-1])+1
print(ctr)
con.close()


def insert_order():
    global ctr
    qty = order_e_qty.get()
    name = combobox1.get()
    size = combobox2.get()
    if name == "" or size == "" or qty == "":
        tkinter.messagebox.showinfo("Insert Status", "All fields are required")
    if int(qty) <= 0:
        tkinter.messagebox.showinfo("Insert Status", "Order quantity must be greater than 0")
    else:
        con = cx_Oracle.connect("bd149/bd149@bd-dc.cs.tuiasi.ro:1539/orcl")
        cursor = con.cursor()
        cursor.execute("insert into orderss values('" + str(ctr) + "','" + name + "','" + size + " ','" + qty + "')")
        cursor.execute("commit")
        ctr+=1
        order_e_qty.delete(0, 'end')
        showorders()
        tkinter.messagebox.showinfo("Insert Status", "Order placed")
        con.close()


def my_upd(*args):
    combobox2.set('')
    my_list2 = []
    con = cx_Oracle.connect("bd149/bd149@bd-dc.cs.tuiasi.ro:1539/orcl")
    cursor = con.cursor()
    cursor.execute("select distinct s_size from snkrs where nume = '" + sel.get() + "'")
    rows = cursor.fetchall()
    for row in rows:
        my_list2.append(row[0])
    con.close()
    stri=""

    for it in my_list2:
        stri+=str(it)+" "
    combobox2.configure(values=stri.split())
    my_list2.clear()


def showorders():
    con = cx_Oracle.connect("bd149/bd149@bd-dc.cs.tuiasi.ro:1539/orcl")
    cursor = con.cursor()
    cursor.execute("select * from orderss")
    rows = cursor.fetchall()
    list2.delete(0, list2.size())

    for row in rows:
        insertData = str(row[0])+" " + row[1] + ", marime " + str(row[2]) + ", " + str(row[3]) + " bucati"
        list2.insert(list2.size() + 1, insertData)
    con.close()


def ship_order():
    con = cx_Oracle.connect("bd149/bd149@bd-dc.cs.tuiasi.ro:1539/orcl")
    cursor = con.cursor()
    cursor.execute("select * from orderss")
    rows1 = cursor.fetchall()
    print(rows1)
    cursor.execute("select * from snkrs")
    rows2 = cursor.fetchall()
    cursor.execute("select * from shipmentss")
    rows3= cursor.fetchall()
    ship_id=[]

    for row3 in rows3:
        ship_id.append(row3[0])
    print(ship_id)
    if rows3 == []:
        for row1 in rows1:
            for row2 in rows2:
                if str(row1[1]) == str(row2[1]) and str(row1[2]) == str(row2[2]):
                    if int(row1[3]) <= int(row2[3]):
                        cursor.execute("update snkrs set qty = qty - '" + str(row1[3]) + "' where nume = '"
                                           + str(row1[1]) + "' and s_size = '" + str(row1[2]) + "'")
                        cursor.execute("commit")
                        print(row2[0])
                        cursor.execute("insert into shipmentss values('" + str(row1[0]) + "','" + "shipped" + "','" + str(
                                row2[0]) + "')")
                        cursor.execute("commit")
    else:
            for row1 in rows1:
                for row2 in rows2:
                    if str(row1[1]) == str(row2[1]) and str(row1[2]) == str(row2[2]) and row1[0] not in ship_id:
                        if int(row1[3]) <= int(row2[3]):
                            cursor.execute("update snkrs set qty = qty - '" + str(row1[3]) + "' where nume = '"
                                           + str(row1[1]) + "' and s_size = '" + str(row1[2]) + "'")
                            cursor.execute("commit")
                            print(row2[0])
                            cursor.execute("insert into shipmentss values('" + str(row1[0]) + "','" + "shipped" + "','" + str(
                                row2[0]) + "')")
                            cursor.execute("commit")
                        else:
                            tkinter.messagebox.showinfo("Insert Status", "Not enough shoes in stock")

    con.close()


def show_shipped():
    con = cx_Oracle.connect("bd149/bd149@bd-dc.cs.tuiasi.ro:1539/orcl")
    cursor = con.cursor()
    cursor.execute("select * from shipmentss")
    rows = cursor.fetchall()
    list3.delete(0, list3.size())

    for row in rows:
        insertData = str(row[0]) + ", status " + str(row[1]) + ", marca produs " + str(row[2])
        list3.insert(list3.size() + 1, insertData)
    con.close()


frame = customtkinter.CTkFrame(master=root)
frame.pack(fill="both", expand=True)

tabview = customtkinter.CTkTabview(frame, width=600, height=300)
tabview.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
tabview.add("Stock")
tabview.add("Order")
tabview.add("Shipments")

id = customtkinter.CTkLabel(tabview.tab("Stock"), text='Enter ID', font=('bold', 15))
id.place(x=30, y=20)

name = customtkinter.CTkLabel(tabview.tab("Stock"), text='Enter Name', font=('bold', 15))
name.place(x=30, y=70)

size = customtkinter.CTkLabel(tabview.tab("Stock"), text='Enter Size', font=('bold', 15))
size.place(x=30, y=120)

qty = customtkinter.CTkLabel(tabview.tab("Stock"), text='Enter Quantity', font=('bold', 15))
qty.place(x=30, y=170)

e_id = customtkinter.CTkEntry(master=tabview.tab("Stock"))
e_id.place(x=160, y=20)

e_name = customtkinter.CTkEntry(master=tabview.tab("Stock"))
e_name.place(x=160, y=70)

e_size = customtkinter.CTkEntry(master=tabview.tab("Stock"))
e_size.place(x=160, y=120)

e_qty = customtkinter.CTkEntry(master=tabview.tab("Stock"))
e_qty.place(x=160, y=170)

insertb = customtkinter.CTkButton(tabview.tab("Stock"), text="Insert", font=("italic", 10), command=insert)
insertb.grid(row=0, column=0, padx=(0, 0), pady=(220, 0), sticky="nsew")

deleteb = customtkinter.CTkButton(tabview.tab("Stock"), text="Delete", font=("italic", 10), command=delete)
deleteb.grid(row=0, column=1, padx=(20, 0), pady=(220, 0), sticky="nsew")

updateb = customtkinter.CTkButton(tabview.tab("Stock"), text="Update", font=("italic", 10), command=update)
updateb.grid(row=0, column=2, padx=(20, 0), pady=(220, 0), sticky="nsew")

getb = customtkinter.CTkButton(tabview.tab("Stock"), text="Get", font=("italic", 10), command=get)
getb.grid(row=0, column=3, padx=(20, 0), pady=(220, 0), sticky="nsew")

list = tkinter.Listbox(tabview.tab("Stock"), height=10, width=35)
list.place(x=450, y=30)

listname = customtkinter.CTkLabel(tabview.tab("Stock"), text='Current Stock', font=('bold', 15))
listname.place(x=400, y=0)

name_values = []
con = cx_Oracle.connect("bd149/bd149@bd-dc.cs.tuiasi.ro:1539/orcl")
cursor = con.cursor()
cursor.execute("select distinct nume from snkrs")
rows = cursor.fetchall()
for row in rows:
    name_values.append(row[0])

sel = customtkinter.StringVar()

combobox1 = customtkinter.CTkComboBox(tabview.tab("Order"),
                                     values=name_values,
                                     command=my_upd,
                                     variable=sel)
combobox1.place(x=160, y=20)

sel2 = customtkinter.StringVar()

combobox2 = customtkinter.CTkComboBox(tabview.tab("Order"), variable=sel2)
combobox2.place(x=160, y=70)

combo1 = customtkinter.CTkLabel(tabview.tab("Order"), text='Enter Model', font=('bold', 15))
combo1.place(x=30, y=20)

combo2 = customtkinter.CTkLabel(tabview.tab("Order"), text='Enter Size', font=('bold', 15))
combo2.place(x=30, y=70)

order_e_qty = customtkinter.CTkEntry(master=tabview.tab("Order"))
order_e_qty.place(x=160, y=120)

orderqty = customtkinter.CTkLabel(tabview.tab("Order"), text='Enter Quantity', font=('bold', 15))
orderqty.place(x=30, y=120)

orderb = customtkinter.CTkButton(tabview.tab("Order"), text="Place Order", font=("italic", 10), command=insert_order)
orderb.place(x=20, y=180)

show_orders = customtkinter.CTkButton(tabview.tab("Order"), text="Show Orders", font=("italic", 10), command=showorders)
show_orders.place(x=180, y=180)

list2 = tkinter.Listbox(tabview.tab("Order"), height=10, width=35)
list2.place(x=450, y=30)

listname2 = customtkinter.CTkLabel(tabview.tab("Order"), text='Your Orders', font=('bold', 15))
listname2.place(x=400, y=0)

list3 = tkinter.Listbox(tabview.tab("Shipments"), height=10, width=35)
list3.place(x=250, y=30)

listname3 = customtkinter.CTkLabel(tabview.tab("Shipments"), text='Ongoing Shipments', font=('bold', 15))
listname3.place(x=220, y=0)

shipmentb = customtkinter.CTkButton(tabview.tab("Shipments"), text="Show", font=("italic", 10), command=show_shipped)
shipmentb.place(x=150, y=220)

shipmentb2 = customtkinter.CTkButton(tabview.tab("Shipments"), text="Ship Orders", font=("italic", 10), command=ship_order)
shipmentb2.place(x=300, y=220)

root.mainloop()
