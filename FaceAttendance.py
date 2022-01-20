import cv2
import numpy as np
import face_recognition
import os
import tkinter as tk
from datetime import datetime

def IMAGES():
    path = 'DataWajah'
    images = []
    myList = os.listdir(path)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
    return images

def daftarNama():
    path = 'DataWajah'
    nama = []
    myList = os.listdir(path)
    for cl in myList:
        nama.append(os.path.splitext(cl)[0])
    return nama

def Classname():
    classNames = []
    for p in daftarNama():
        classNames.append(p.split(',')[0])
    return classNames

def latihWajah():
    def findEncodings(images):
        encodelist = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodelist.append(encode)
        return encodelist
    return findEncodings(IMAGES())
encodeListKnown = latihWajah()

def fix():
    def latih(baru):
        global encodeListKnown
        encodeListKnown = baru
    latih(latihWajah())
    intructions.config(text="Sistem telah siap untuk digunakan")
    terimakasih.config(text="")
    absen.config(text="")

def markAttendance(name):
    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            dayString = now.strftime('%A %d %B %Y')
            f.writelines(f'\n{name},{dayString},{dtString}')

def absensiWajah():
    cap = cv2.VideoCapture(0)
    angka = 1
    while True:
        succes, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        facesCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
        for encodeFace, (x, y, w, h) in zip(encodeCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)
            x, y, w, h = x * 4, y * 4, w * 4, h * 4
            cv2.rectangle(img, (h, x), (y, w), (0, 0, 255), 2)
            cv2.rectangle(img, (h, w - 35), (y, w), (0, 255, 0), cv2.FILLED)
            if matches[matchIndex]:
                name = Classname()[matchIndex]
                namaFile = daftarNama()[matchIndex]
                cv2.putText(img, name, (h + 6, w - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                angka += 1
        cv2.imshow('Face Recognition', img)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
        elif angka > 5:
            break
    markAttendance(namaFile)
    terimakasih.config(text = "Terimakasih")
    intructions.config(text = name.upper(), font= ("Roboto", 30,"bold"), fg= "#40F400")
    absen.config(text="Telah melakukan absensi")
    cap.release()
    cv2.destroyAllWindows()

root = tk.Tk()

def openNewWindow():
    win = tk.Tk()
    win.geometry("700x400")
    win.configure(background= "#013880")
    # for entry data nama
    entry1 = tk.Entry(win, font="Roboto", width= 30)
    entry1.place(x = 200, y = 120)
    label1 = tk.Label(win, text="Nama ", font="Roboto", fg="white", bg="#013880")
    label1.place(x = 80, y = 120)
    # for entry data nim
    entry2 = tk.Entry(win, font="Roboto", width= 20)
    entry2.place(x = 200, y = 160)
    label2 = tk.Label(win, text="NIM", font="Roboto", fg="white", bg="#013880")
    label2.place(x = 80, y = 160)
    # for entry data kelas
    entry3 = tk.Entry(win, font="Roboto", width= 20)
    entry3.place(x = 200, y = 200)
    label3 = tk.Label(win, text="Kelas", font="Roboto", fg="white", bg="#013880")
    label3.place(x = 80, y = 200)

    judulWajah = tk.Label(win, text="Rekam Data Wajah", font= ("Roboto", 30,"bold"), fg="white", bg="#013880")
    judulWajah.place(x=180, y= 30)

    global selesai
    selesai = tk.Label(win, text="Silahkan isi data dengan lengkap", font=("Roboto", 17), fg="white", bg="#013880")
    selesai.place(x=185, y=260)

    def rekamWajah():
        wajahDir = 'DataWajah'
        cap = cv2.VideoCapture(0)
        faceID = entry1.get()
        NRP = entry2.get()
        Kelas = entry3.get()
        ambilData = 1
        while True:
            succes, img = cap.read()
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
            facesCurFrame = face_recognition.face_locations(imgS)
            for (x, y, w, h) in facesCurFrame:
                namaFile = str(faceID) + ',' + str(NRP) + ',' + str(Kelas) + '.jpg'
                cv2.imwrite(wajahDir + '/' + namaFile, img)
                ambilData += 1
            cv2.imshow('Face Detection', img)
            k = cv2.waitKey(1) & 0xFF
            if k == 27 or k == ord('q'):
                break
            elif ambilData > 1:
                break
        cap.release()
        cv2.destroyAllWindows()
        fix()
        selesai.config(text="Perekaman data telah selesai")

    def clear():
        entry1.delete(0,'end')
        entry2.delete(0, 'end')
        entry3.delete(0, 'end')
        selesai.config(text="Silahkan isi data dengan lengkap")

    btnAmbil = tk.Button(win, text="Ambil Gambar", font="Roboto", bg="#F1C40F", fg="#0C446A", height=1, width=15, command= rekamWajah)
    btnAmbil.place(x = 465, y = 320)
    btnClear = tk.Button(win, text="Clear", font="Roboto", bg="red", fg="#0C446A", height=1, width=9, command= clear)
    btnClear.place(x=300, y=320)

# mengatur canvas (window tkinter)
canvas = tk.Canvas(root, width=700, height=400)
canvas.grid(columnspan=3, rowspan=8)
canvas.configure(bg="#013880")
# judul
judul = tk.Label(root, text="Sistem Absensi Wajah", font=("Roboto",33,"bold"),bg="#013880", fg="white")
canvas.create_window(350, 65, window=judul)
#credit
made = tk.Label(root, text="Made by Mohamad Hafidz Al Habib", font=("Roboto",10,"italic"), bg="#013880",fg="white")
canvas.create_window(570, 380, window=made)

global intructions
global terimakasih
global absen

terimakasih = tk.Label(root, text='', font=("Arial",20),fg="white",bg="#013880", wraplength= 500)
canvas.create_window(350, 130, window=terimakasih)

intructions = tk.Label(root, text='SELAMAT DATANG', font=("Roboto",25),fg="white",bg="#013880", wraplength= 500)
canvas.create_window(350, 195, window=intructions)

absen = tk.Label(root, text='', font=("Arial",20),fg="white",bg="#013880", wraplength= 500)
canvas.create_window(350, 260, window=absen)

Rekam_text = tk.StringVar()
Rekam_btn = tk.Button(root, textvariable=Rekam_text, font="Roboto", bg="#3FE917", fg="#0C446A", height=1, width=15, command=openNewWindow)
Rekam_text.set("Rekam Wajah")
Rekam_btn.place( x = 110,y = 320)
# tombol absensi dengan wajah
Rekam_text2 = tk.StringVar()
Rekam_btn2 = tk.Button(root, textvariable=Rekam_text2, font="Roboto", bg="#F1C40F", fg="#0C446A", height=1, width=15, command= absensiWajah)
Rekam_text2.set("Absensi")
Rekam_btn2.place(x = 415, y = 320)

root.mainloop()