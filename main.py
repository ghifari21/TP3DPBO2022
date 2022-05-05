from tkinter import *
import mysql.connector
from PIL import Image, ImageTk

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="db_praktikum"
)

dbcursor = mydb.cursor()

root = Tk()
root.title("Praktikum DPBO")


# Fungsi untuk mengambil data
def getMhs():
    global mydb
    global dbcursor

    dbcursor.execute("SELECT * FROM mahasiswa")
    result = dbcursor.fetchall()

    return result


# Window Input Data
def inputs():
    # Hide root window
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Input")
    dframe = LabelFrame(top, text="Input Data Mahasiswa", padx=10, pady=10)
    dframe.pack(padx=10, pady=10)
    # Input 1
    label1 = Label(dframe, text="Nama Mahasiswa").grid(row=0, column=0, sticky="w")
    input_nama = Entry(dframe, width=30)
    input_nama.grid(row=0, column=1, padx=20, pady=10, sticky="w")
    # Input 2
    label2 = Label(dframe, text="NIM").grid(row=1, column=0, sticky="w")
    input_nim = Entry(dframe, width=30)
    input_nim.grid(row=1, column=1, padx=20, pady=10, sticky="w")
    # Input 3
    options = ["Filsafat Meme", "Sastra Mesin", "Teknik Kedokteran", "Pendidikan Gaming"]
    input_jurusan = StringVar(root)
    input_jurusan.set(options[0])
    label3 = Label(dframe, text="Jurusan").grid(row=2, column=0, sticky="w")
    input3 = OptionMenu(dframe, input_jurusan, *options)
    input3.grid(row=2, column=1, padx=20, pady=10, sticky='w')
    # Input 4
    input_gender = StringVar(root)
    label4 = Label(dframe, text="Jenis Kelamin").grid(row=3, column=0, sticky="w")
    gender_laki_laki = Radiobutton(dframe, text="Laki-Laki", variable=input_gender, value="Laki-laki").grid(row=3, column=1, padx=20, pady=10, sticky="w")
    gender_perempuan = Radiobutton(dframe, text="Perempuan", variable=input_gender, value="Perempuan").grid(row=3, column=1, padx=100, pady=10, sticky="w")
    # Input 5
    def checkboxValue():
        hobby = []
        if input_hobby1.get() is True:
            hobby.append("Turu")
        if input_hobby2.get() is True:
            hobby.append("Gaming")
        if input_hobby3.get() is True:
            hobby.append("Rebahan")
        return hobby

    input_hobby1 = BooleanVar(root)
    input_hobby2 = BooleanVar(root)
    input_hobby3 = BooleanVar(root)
    label5 = Label(dframe, text="Hobi").grid(row=4, column=0, sticky="w")
    check_box = Checkbutton(dframe, text="Turu", variable=input_hobby1, onvalue=True, offvalue=False).grid(row=4, column=1, padx=20, pady=10, sticky="w")
    check_box = Checkbutton(dframe, text="Gaming", variable=input_hobby2, onvalue=True, offvalue=False).grid(row=4, column=1, padx=100, pady=10, sticky="w")
    check_box = Checkbutton(dframe, text="Rebahan", variable=input_hobby3, onvalue=True, offvalue=False).grid(row=4, column=1, padx=180, pady=10, sticky="w")


    # Button Frame
    frame2 = LabelFrame(dframe, borderwidth=0)
    frame2.grid(columnspan=2, column=0, row=10, pady=10)

    # Submit Button
    btn_submit = Button(frame2, text="Submit Data", anchor="s", command=lambda:[insertData(top, input_nama, input_nim, input_jurusan, input_gender, checkboxValue()), top.withdraw()])
    btn_submit.grid(row=3, column=0, padx=10)

    # Cancel Button
    btn_cancel = Button(frame2, text="Gak jadi / Kembali", anchor="s", command=lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row=3, column=1, padx=10)

# Untuk memasukan data
def insertData(parent, nama, nim, jurusan, gender, raw_hobbies):
    top = Toplevel()
    # Get data
    nama = nama.get()
    nim = nim.get()
    jurusan = jurusan.get()
    gender = gender.get()
    hobbies = ", ".join(raw_hobbies)

    error_msg = ""
    if nama == "":
        error_msg += "Field Nama tidak boleh kosong!\n"
    if nim == "":
        error_msg += "Field NIM tidak boleh kosong!\n"
    if jurusan == "":
        error_msg += "Field Jurusan tidak boleh kosong!\n"
    if gender == "":
        error_msg += "Field Gender tidak boleh kosong!\n"
    if hobbies == "":
        error_msg += "Field Hobi tidak boleh kosong!\n"

    if error_msg == "":
        global mydb
        global dbcursor
        query = "INSERT INTO mahasiswa VALUES (null, %s, %s, %s, %s, %s)"
        val = (nim, nama, jurusan, gender, hobbies)
        dbcursor.execute(query, val)
        mydb.commit()

        success_label = Label(top, text="Telah berhasil menambahkan data!").grid(row=0, column=0, padx=20, pady=10, sticky="w")
        # Input data disini
        btn_ok = Button(top, text="Syap!", anchor="s", command=lambda:[top.destroy(), parent.deiconify()])
        btn_ok.pack(padx=10, pady=10)
    else:
        error_label = Label(top, text=error_msg).grid(row=0, column=0, padx=20, pady=10, sticky="w")
        # Input data disini
        btn_ok = Button(top, text="Syap!", anchor="s", command=lambda:[top.destroy(), parent.deiconify()])
        btn_ok.pack(padx=10, pady=10)

  
# Window Semua Mahasiswa
def viewAll():
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Semua Mahasiswa")
    frame = LabelFrame(top, borderwidth=0)
    frame.pack()
    # Cancel Button
    btn_cancel = Button(frame, text="Kembali", anchor="w", command=lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    # Head title
    head = Label(frame, text="Data Mahasiswa")
    head.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    tableFrame = LabelFrame(frame)
    tableFrame.grid(row=1, column = 0, columnspan=2)

    # Get All Data
    result = getMhs()

    # Title
    title1 = Label(tableFrame, text="No.", borderwidth=1, relief="solid", width=3, padx=5).grid(row=0, column=0)
    title2 = Label(tableFrame, text="NIM", borderwidth=1, relief="solid", width=15, padx=5).grid(row=0, column=1)
    title3 = Label(tableFrame, text="Nama", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=2)
    title4 = Label(tableFrame, text="Jurusan", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=3)
    title5 = Label(tableFrame, text="Jenis Kelamin", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=4)
    title6 = Label(tableFrame, text="Hobi", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=5)

    # Print content
    i = 0
    for data in result:
        label1 = Label(tableFrame, text=str(i+1), borderwidth=1, relief="solid", height=2, width=3, padx=5).grid(row=i+1, column=0)
        label2 = Label(tableFrame, text=data[1], borderwidth=1, relief="solid", height=2, width=15, padx=5).grid(row=i+1, column=1)
        label3 = Label(tableFrame, text=data[2], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=2)
        label4 = Label(tableFrame, text=data[3], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=3)
        label5 = Label(tableFrame, text=data[4], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=4)
        label6 = Label(tableFrame, text=data[5], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=5)
        i += 1

# Dialog konfirmasi hapus semua data
def clearAll():
    top = Toplevel()
    lbl = Label(top, text="Yakin mau hapus semua data?")
    lbl.pack(padx=20, pady=20)
    btnframe = LabelFrame(top, borderwidth=0)
    btnframe.pack(padx=20, pady=20)
    # Yes
    btn_yes = Button(btnframe, text="Gass", bg="green", fg="white", command=lambda:[top.destroy(), delAll()])
    btn_yes.grid(row=0, column=0, padx=10)
    # No
    btn_no = Button(btnframe, text="Tapi boong", bg="red", fg="white", command=top.destroy)
    btn_no.grid(row=0, column=1, padx=10)

# Dialog konfirmasi keluar GUI
def exitDialog():
    global root
    root.withdraw()
    top = Toplevel()
    lbl = Label(top, text="Yakin mau keluar?")
    lbl.pack(padx=20, pady=20)
    btnframe = LabelFrame(top, borderwidth=0)
    btnframe.pack(padx=20, pady=20)
    # Yes
    btn_yes = Button(btnframe, text="Gass", bg="green", fg="white", command=lambda:[top.destroy(), root.destroy()])
    btn_yes.grid(row=0, column=0, padx=10)
    # No
    btn_no = Button(btnframe, text="Tapi boong", bg="red", fg="white", command=lambda:[top.destroy(), root.deiconify()])
    btn_no.grid(row=0, column=1, padx=10)

def delAll():
    top = Toplevel()
    # Delete data disini
    global mydb
    global dbcursor
    query = "DELETE FROM mahasiswa"
    dbcursor.execute(query)
    mydb.commit()
    btn_ok = Button(top, text="Zeeb", command=top.destroy)
    btn_ok.pack(pady=20)

def viewFacility():
    global root
    root.withdraw()
    top = Toplevel()
    top.title("Semua Fasilitas Kampus")
    frame = LabelFrame(top, borderwidth=0)
    frame.pack()

    # Cancel Button
    btn_cancel = Button(frame, text="Kembali", anchor="w", command=lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    # Head title
    head = Label(frame, text="Fasilitas Kampus")
    head.grid(row=0, column=1, columnspan=4, padx=10, pady=10, sticky="w")

    tableFrame = LabelFrame(frame)
    tableFrame.grid(row=1, column = 0, columnspan=2)

    current_value = IntVar(root)

    # titles
    titles = ["Lab Komputer", "Musholla", "Perpustakaan", "Ruang Kelas"]

    # images path
    images = ["project/labkomputer.jpg", "project/musholla.jpg", "project/perpustakaan.jpg", "project/ruangkelas.jpg"]


    def imageSlider():
        index = current_value.get()
        title = Label(frame, text=titles[index-1]).grid(row=2, column=0, columnspan=5)
        img = Image.open(images[index-1])
        img = img.resize((500, 500))
        img = ImageTk.PhotoImage(img)

        img_frame = Label(frame, image=img).grid(row=3, column=0, columnspan=5)
        img_frame.image = img

        horizontal = Scale(frame, from_=1, to=4, orient=HORIZONTAL, variable=current_value).grid(row=4, column=0, columnspan=5)
        confirm_btn = Button(frame, text="Ganti Fasilitas", command=imageSlider).grid(row=5, column=0, columnspan=5)

    horizontal = Scale(frame, from_=1, to=4, orient=HORIZONTAL, variable=current_value).grid(row=4, column=0, columnspan=5)
    confirm_btn = Button(frame, text="Ganti Fasilitas", command=imageSlider).grid(row=5, column=0, columnspan=5)

    title = Label(frame, text=titles[0]).grid(row=2, column=0, columnspan=5)
    img = Image.open(images[0])
    img = img.resize((500, 500))
    img = ImageTk.PhotoImage(img)

    img_frame = Label(frame, image=img).grid(row=3, column=0, columnspan=5)
    img_frame.image = img


# Title Frame
frame = LabelFrame(root, text="Praktikum DPBO", padx=10, pady=10)
frame.pack(padx=10, pady=10)

# ButtonGroup Frame
buttonGroup = LabelFrame(root, padx=10, pady=10)
buttonGroup.pack(padx=10, pady=10)

# Title
label1 = Label(frame, text="Data Mahasiswa", font=(30))
label1.pack()

# Description
label2 = Label(frame, text="Ceritanya ini database mahasiswa ngab")
label2.pack()

# Input btn
b_add = Button(buttonGroup, text="Input Data Mahasiswa", command=inputs, width=30)
b_add.grid(row=0, column=0, pady=5)

# All data btn
b_add = Button(buttonGroup, text="Semua Data Mahasiswa", command=viewAll, width=30)
b_add.grid(row=1, column=0, pady=5)

# View facility btn
b_facility = Button(buttonGroup, text="Semua Fasilitas Kampus", command=viewFacility, width=30)
b_facility.grid(row=2, column=0, pady=5)

# Clear all btn
b_clear = Button(buttonGroup, text="Hapus Semua Data Mahasiswa", command=clearAll, width=30)
b_clear.grid(row=3, column=0, pady=5)

# Exit btn
b_exit = Button(buttonGroup, text="Exit", command=exitDialog, width=30)
b_exit.grid(row=4, column=0, pady=5)

root.mainloop()