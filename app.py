import requests
import streamlit as st

# Konfigurasi halaman web
st.set_page_config(
    page_title="Web Al-Qur'an Digital", page_icon="📖", layout="wide"
)

# Judul Utama
st.title("📖 Web Al-Qur'an Digital Indonesia")
st.markdown(
    "Aplikasi web sederhana dibuat menggunakan **Python (Streamlit)** & **API"
    " EQuran.id**"
)
st.markdown("---")


# Fungsi untuk mengambil daftar surat dari API
@st.cache_data
def get_daftar_surat():
  url = "https://equran.id/api/v2/surat"
  response = requests.get(url)
  if response.status_code == 200:
    return response.json().get("data", [])
  return []


# Fungsi untuk mengambil detail surat dan ayat
def get_detail_surat(nomor):
  url = f"https://equran.id/api/v2/surat/{nomor}"
  response = requests.get(url)
  if response.status_code == 200:
    return response.json().get("data", {})
  return {}


# Sidebar untuk Navigasi Surat
st.sidebar.header("📌 Navigasi Surat")
daftar_surat = get_daftar_surat()

if daftar_surat:
  # Membuat pilihan dropdown surat
  pilihan_surat = {
      f"{surat['nomor']}. {surat['namaLatin']} ({surat['nama']})": surat[
          "nomor"
      ]
      for surat in daftar_surat
  }

  selected_label = st.sidebar.selectbox(
      "Pilih Surat Al-Qur'an:", list(pilihan_surat.keys())
  )
  selected_nomor = pilihan_surat[selected_label]

  # Ambil data detail surat yang dipilih
  surat_detail = get_detail_surat(selected_nomor)

  if surat_detail:
    # Tampilkan Informasi Surat
    st.header(
        f"Surat {surat_detail.get('namaLatin')} ({surat_detail.get('nama')})"
    )
    st.info(
        f"Arti: **{surat_detail.get('arti')}** | "
        f"Jumlah Ayat: **{surat_detail.get('jumlahAyat')}** | "
        f"Tempat Turun: **{surat_detail.get('tempatTurun')}**"
    )

    # Pemutar Audio Full Surat (Qari Misyari Rasyid Al-Afasi)
    audio_url = surat_detail.get("audioFull", {}).get("05")
    if audio_url:
      st.audio(audio_url, format="audio/mp3")

    st.markdown("---")

    # Menampilkan Daftar Ayat
    ayat_list = surat_detail.get("ayat", [])
    for ayat in ayat_list:
      nomor_ayat = ayat.get("nomorAyat")
      teks_arab = ayat.get("teksArab")
      teks_latin = ayat.get("teksLatin")
      teks_indo = ayat.get("teksIndonesia")

      # Format Tampilan Ayat
      st.markdown(
          f"### `{nomor_ayat}`. &nbsp;&nbsp;&nbsp; **{teks_arab}**",
          unsafe_allow_html=True,
      )
      st.markdown(f"*{teks_latin}*")
      st.markdown(f"**Artinya:** {teks_indo}")

      # Tombol Audio per Ayat
      audio_ayat = ayat.get("audio", {}).get("05")
      if audio_ayat:
        with st.expander(f"Dengarkan Audio Ayat {nomor_ayat}"):
          st.audio(audio_ayat, format="audio/mp3")

      st.markdown("---")
else:
  st.error("Gagal memuat data dari server. Periksa koneksi internet Anda.")
  
