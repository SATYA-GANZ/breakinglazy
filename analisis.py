import pandas as pd
import numpy as np
from banner import random_art
import os
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import preprocessing
import joblib
from time import strftime

# Path default untuk menyimpan file dan model
PATH = "/storage/emulated/0/otomatis/"

def main_menu():
    """Menampilkan menu utama dan meminta pilihan pengguna."""
    print(random_art())
    print("\n=== Automato CLI ===")
    print("1. Preprocessing Data (Bersihkan Data)")
    print("2. Analisis Data dengan Machine Learning")
    print("3. Developer Option (Train Model)")
    choice = int(input("Pilih opsi (1/2/3): "))
    
    match(choice):
     case 1:
    		proper_data()
     case 2:
        print("Pilih periode untuk analisis : ")
        print("1. Harian")
        print("2. Mingguan")
        print("3. Bulanan")
        choice = input("Pilih opsi (1/2/3): ").strip()
    
        period_map = {"1": "harian", "2": "mingguan", "3": "bulanan"}
        period = period_map.get(choice)
        choice2 = input("masukkan file csv : ")
        if not period:
          print("Opsi tidak valid.")
          return
            
        analyze_data("model_harian_09_May_2058.joblib", period, choice2)
     case 3:
    		train_model_menu()

def proper_data():
    """Fungsi untuk preprocessing data: membaca, membersihkan, dan menyimpan summary."""
    try:
        print("\n--- Preprocessing Data ---")
        file_exist = input("Masukkan nama file CSV log: ").strip()
        if not file_exist or not os.path.exists(file_exist):
            print("File tidak ditemukan atau nama file kosong.")
            return
        
        df = pd.read_csv(file_exist)
        df["waktu awal"] = pd.to_datetime(df['waktu awal'], errors='coerce')
        df["waktu akhir"] = pd.to_datetime(df['waktu akhir'], errors='coerce')
        
        if df["waktu awal"].isnull().any() or df["waktu akhir"].isnull().any():
            print("Ada data waktu yang tidak valid. Periksa formatnya.")
            return
        
        df['durasi kerja'] = (df["waktu akhir"] - df["waktu awal"]).dt.total_seconds() / 3600
        df['tanggal'] = df['waktu awal'].dt.date
        df['minggu'] = df['waktu awal'].dt.isocalendar().week
        df['bulan'] = df['waktu awal'].dt.month
        
        harian = df.groupby('tanggal')['durasi kerja'].sum()
        mingguan = df.groupby('minggu')['durasi kerja'].sum()
        bulanan = df.groupby('bulan')['durasi kerja'].sum()
        
        label_harian = np.where(harian >= 12, 'hard work', 
                                np.where(harian <=7, 'biasa', 'pemalas'))
        label_mingguan = np.where(mingguan >= 84, 'hard work', 
                                  np.where(mingguan <= 80, 'biasa', 'pemalas'))
        label_bulanan = np.where(bulanan >= 372, 'hard work', 
                                 np.where(bulanan >= 300, 'sedang', 
                                          np.where(bulanan >= 250, 'malas', 'biasa')))
        
        df_daily = pd.DataFrame({'total_jam': harian, 'kategori': label_harian})
        df_weekly = pd.DataFrame({'total_jam': mingguan, 'kategori': label_mingguan})
        df_monthly = pd.DataFrame({'total_jam': bulanan, 'kategori': label_bulanan})
        
        label_encoder = preprocessing.LabelEncoder()
        df['agenda_encode'] = label_encoder.fit_transform(df['agenda'])
        
        print("\nData Awal (5 baris):")
        print(df[['tanggal', 'waktu awal', 'waktu akhir', 'durasi kerja', 'agenda']].head())
        
        input_file = input("\nMasukkan nama file untuk data yang sudah bersih: ").strip()
        if input_file:
            df_processed = df[['tanggal', 'waktu awal', 'waktu akhir', 'agenda', 'durasi kerja', 'agenda_encode']]
            df_processed.to_csv(os.path.join(PATH, input_file), index=False)
            print("Data yang sudah diproses berhasil disimpan!")
        
        print("\nSimpan summary per periode:")
        save_summary(df_daily, "harian")
        save_summary(df_weekly, "mingguan")
        save_summary(df_monthly, "bulanan")
        
        flowAnalyze = input("\nLanjut ke training model? (y/n): ").lower()
        if flowAnalyze == "y":
            train_model_menu()
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def save_summary(df_summary, period):
    """Simpan summary data ke file CSV dengan timestamp."""
    file_name = input(f"Masukkan nama file untuk summary {period}: ").strip()
    if file_name:
        df_summary.to_csv(os.path.join(PATH, f"{file_name}_{strftime('%d_%b')}.csv"))
        print(f"Summary {period} berhasil disimpan!")

def train_model_menu():
    """Menu untuk memilih periode dan melatih model."""
    print("\n--- Training Model ---")
    print("Pilih periode untuk training:")
    print("1. Harian")
    print("2. Mingguan")
    print("3. Bulanan")
    choice = input("Pilih opsi (1/2/3): ").strip()
    
    period_map = {"1": "harian", "2": "mingguan", "3": "bulanan"}
    period = period_map.get(choice)
    if not period:
        print("Opsi tidak valid.")
        return
    
    file_summary = input(f"Masukkan nama file summary {period}: ").strip()
    file_path = os.path.join(PATH, file_summary)
    if not os.path.exists(file_path):
        print("File summary tidak ditemukan.")
        return
    
    # Training model dan simpan
    training_data(file_path, period)

def training_data(file, period):
    """Fungsi untuk melatih model Decision Tree berdasarkan file summary dan menyimpan model."""
    try:
        df = pd.read_csv(file)
        X = df[['total_jam']]
        y = df['kategori']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = DecisionTreeClassifier()
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"\nAkurasi model untuk {period}: {accuracy:.2f}")
        
        # Simpan model ke file
        model_filename = f"model_{period}_{strftime('%d_%b_%H%M')}.joblib"
        joblib.dump(model, os.path.join(PATH, model_filename))
        print(f"Model disimpan sebagai {model_filename}")
        
        flow_analisis = input("\nMau lanjut analisis? (y/n): ").lower()
        if flow_analisis == "y":
            analyze_data(model_filename, period)
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def analyze_data(model_file, period,total_work):
    """Fungsi untuk memprediksi kategori berdasarkan input total jam baru menggunakan model yang dimuat."""
    try:
        # Muat model dari file
        model = joblib.load(os.path.join(PATH, model_file))
        df = pd.read_csv(total_work)
        total_jam_sum = df['total_jam'].sum()
        print(f"current total sum : {total_jam_sum}")
        total_jam = float(input(f"Masukkan total jam belajar ({period}): "))
        prediksi = model.predict([[total_jam]])[0]
        print(f"\nPrediksi kategori untuk {total_jam} jam ({period}): {prediksi}")
    except ValueError:
        print("Input tidak valid. Harap masukkan angka.")
    except FileNotFoundError:
        print("Model file tidak ditemukan. Harap latih model terlebih dahulu.")

