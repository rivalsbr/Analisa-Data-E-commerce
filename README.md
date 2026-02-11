\# E-Commerce Data Analysis Dashboard ✨



\## Deskripsi

Dashboard ini dibuat untuk menganalisis performa penjualan dan tingkat kepuasan pelanggan pada platform E-Commerce. Fokus utama analisis meliputi tren pendapatan, kategori produk unggulan, pengaruh ketepatan waktu pengiriman terhadap ulasan, serta segmentasi pelanggan menggunakan teknik RFM (Recency, Frequency, Monetary).



\## Struktur Proyek

\- `/dashboard`: Berisi file `e-commerce\_dashboard.py` dan dataset yang sudah dibersihkan (`product\_sales.csv` \& `delivery\_reviews.csv`).

\- `/data`: Berisi raw data.

\- `notebook.ipynb`: File analisis data dari awal hingga akhir.

\- `requirements.txt`: Daftar library yang dibutuhkan.



\## Setup Environment - Anaconda

```

conda create --name main-ds python=3.9

conda activate main-ds

pip install -r requirements.txt

```



\## Setup Environment - Shell/Terminal

```

mkdir proyek\_analisis\_data

cd proyek\_analisis\_data

pipenv install

pipenv shell

pip install -r requirements.txt

```



\## Run Streamlit App

```

streamlit run e-commerce\_dashboard.py

```





