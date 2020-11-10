import Multiversion as MV
import SimpleLock as SL
import OCC as OCC

if __name__ == "__main__":
    print("Selamat datang pada simulasi Concurrency Control G8-K2!")
    method_input = 0
    while (method_input < 1 or method_input > 3):
        method_input = int(input("Pilih metode Concurreny Control yang ingin digunakan!\n1. Simple Locking\n2. OCC\n3. Multiversion\n"))

    file_input = input("Ketik nama file yang ingin digunakan sebagai test case (Pastikan ada dalam folder 'test'): ")

    if method_input == 1:
        SL.execute_SL(file_input)
    elif method_input == 2:
        print("OCC")
    else:
        print("Multiversion")

    print("\nTerima kasih telah mencoba program kami!")
    print("Creators:\n1. Michael Hans\n2. Muh. Muslim Al Mujahid\n3. Ananda Yulizar\n4. M. Rizki Nahasrudin\n5. Fatkhan Matsuri")
    print("Kelompok 08 Kelas 02")
    print("Teknik Informatika 2018 Institut Teknologi Bandung")