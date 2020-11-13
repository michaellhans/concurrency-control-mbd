# Concurrency Protocol Database Management

## Deskripsi Tugas
Dalam tugas besar Manajemen Basis Data kali ini, kami mengimplementasikan protokol concurrency control dalam bentuk simulasi terhadap kumpulan proses dalam suatu schedule. Berikut ini adalah daftar Concurrency Control Protocol yang kami implementasikan pada tugas besar ini, yaitu:
1. Simple Locking (Exclusive Only)
2. Serial Optimistic Concurrency Control (Validation Based Protocol)
3. Multiversion Timestamp Ordering Concurrency Control (MVCC)

## How to Run Program
1. Untuk menjalankan program, masukkan command berikut dengan kondisi terminal sudah pada directory ./src
```python Main.py```
1. Masukkan pilihan mode protocol yang ingin disimulasikan
2. Masukkan nama file yang berisi kumpulan transaksi yang ingin dijalankan.
3. Format penulisan pada file text yang berisi kumpulan transaksi adalah sebagai berikut.
```
3               # banyak transaksi yang terlibat
X Y             # data-data yang dimainkan pada schedule
R1(X)           # T1 melakukan Read terhadap X
W2(X)           # T2 melakukan Write terhadap X
W2(Y)           # T2 melakukan Write terhadap Y
W3(Y)           # T3 melakukan Write terhadap Y
W1(Y)           # T1 melakukan Write terhadap Y
C1              # T1 melakukan Commit
C2              # T2 melakukan Commit
C3              # T3 melakukan Commit
```

## Built With

- [Python](https://www.python.org/)

## Authors

**Kelompok 08 Kelas 02**
1. **13518052 - Muhamad Rizki Nasharudin**
2. **13518053 - Fatkhan Masruri**
3. **13518054 - Muh. Muslim Al Mujahid**
4. **13518056 - Michael Hans**
5. **13518088 - Ananda Yulizar Muhammad**

## Acknowledgments

- Dosen IF3140 K1 - Tricya Esterina Widagdo
- Dosen IF3140 K2 - Fazat Nur Azizah
- Dosen IF3140 K2 - Ardian Umam
- Dosen IF3140 K3 - Latifa Dwiyanti
- IF3140 Manajemen Basis Data Tahun Ajaran 2020-2021
- Asisten Laboratorium Basis Data Tahun Ajaran 2020-2021