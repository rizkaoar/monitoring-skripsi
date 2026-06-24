import streamlit as st
import pandas as pd
import os

# ==================================================
# KONFIGURASI
# ==================================================

file_excel = "data_skripsi.xlsx"
folder_file = "file_skripsi"

if not os.path.exists(folder_file):
    os.makedirs(folder_file)

# ==================================================
# MEMBUAT FILE EXCEL JIKA BELUM ADA
# ==================================================

if not os.path.exists(file_excel):

    data_awal = pd.DataFrame(columns=[
        "Nama",
        "NIM",
        "No Hp",
        "Pembimbing Akademik",
        "Pembimbing Skripsi",
        "Penguji",
        "Judul Skripsi",


        "Skripsi Bab 1",
        "Skripsi Bab 2",
        "Skripsi Bab 3",
        "Skripsi Bab 4",
        "Skripsi Bab 5",

        "Progres"
    ])

    data_awal.to_excel(file_excel, index=False)

# ==================================================
# MEMBACA DATA
# ==================================================

data = pd.read_excel(file_excel, dtype=str).fillna("")

st.title("SISTEM MONITORING MAHASISWA SKRIPSI")

# ==================================================
# FUNGSI SIMPAN FILE
# ==================================================

def simpan_file(file_obj, nim, jenis):

    if file_obj is None:
        return ""

    nama_file = f"{nim}_{jenis}_{file_obj.name}"

    lokasi = os.path.join(
        folder_file,
        nama_file
    )

    with open(lokasi, "wb") as f:
        f.write(file_obj.getbuffer())

    return nama_file

# ==================================================
# CARI DATA
# ==================================================

st.subheader("Cari Nama / NIM")

cari = st.text_input("Cari nama atau NIM")

if cari != "":

    hasil = data[
        data["Nama"].str.lower().str.contains(cari.lower(), na=False)
        |
        data["NIM"].str.lower().str.contains(cari.lower(), na=False)
    ]

    if len(hasil) == 0:

        st.warning("Data tidak ditemukan")

    else:

        for i, row in hasil.iterrows():

            st.write("## Data Mahasiswa")

            st.write("Nama :", row["Nama"])
            st.write("NIM :", row["NIM"])
            st.write("No HP :", row["No Hp"])
            st.write("Pembimbing Akademik :", row["Pembimbing Akademik"])
            st.write("Pembimbing Skripsi :", row["Pembimbing Skripsi"])
            st.write("Penguji :", row["Penguji"])
            st.write("Judul Skripsi :", row["Judul Skripsi"])
            st.write("Progres :", row["Progres"])

            st.write("### Dokumen Skripsi")

            dokumen = [
                "Skripsi Bab 1",
                "Skripsi Bab 2",
                "Skripsi Bab 3",
                "Skripsi Bab 4",
                "Skripsi Bab 5"
            ]

            for dok in dokumen:

                nama_file = row[dok]

                if nama_file != "":

                    path_file = os.path.join(
                        folder_file,
                        nama_file
                    )

                    if os.path.exists(path_file):

                        st.success(f"✓ {dok} tersedia")

                        with open(path_file, "rb") as file:

                            st.download_button(
                                label=f"Download {dok}",
                                data=file,
                                file_name=nama_file,
                                key=f"download_{dok}_{row['NIM']}"
                            )

                    else:

                        st.error(f"{dok} tidak ditemukan")

                else:

                    st.warning(f"{dok} belum diupload")

            progres_baru = st.selectbox(
                "Update Progres",
                [
                    "Pengajuan Judul",
                    "Skripsi Bab 1",
                    "Skripsi Bab 2",
                    "Skripsi Bab 3",
                    "Seminar Proposal",
                    "Skripsi Bab 4",
                    "Skripsi Bab 5",
                    "Seminar Hasil",
                    "Sidang",
                    "Revisi",
                    "Lulus"
                ],
                key="progres_" + str(row["NIM"])
            )

            if st.button(
                "Update Progres",
                key="update_" + str(row["NIM"])
            ):

                data.loc[
                    data["NIM"] == row["NIM"],
                    "Progres"
                ] = progres_baru

                data.to_excel(
                    file_excel,
                    index=False
                )

                st.success(
                    "Progres berhasil diupdate"
                )

                st.rerun()

            if st.button(
                "Hapus Data Ini",
                key="hapus_" + str(row["NIM"])
            ):

                data = data[
                    data["NIM"] != row["NIM"]
                ]

                data.to_excel(
                    file_excel,
                    index=False
                )

                st.success(
                    "Data berhasil dihapus"
                )

                st.rerun()

            st.write("---")
            
# ==================================================
# TAMBAH DATA
# ==================================================

st.subheader("TAMBAH DATA MAHASISWA")

nama = st.text_input("Nama")
nim = st.text_input("NIM")
no_hp = st.text_input("No Hp")

pa = st.text_input(
    "Pembimbing Akademik"
)

ps = st.text_input(
    "Pembimbing Skripsi"
)

penguji = st.text_input(
    "Penguji"
)

judul = st.text_area(
    "Judul Skripsi"
)

progres = st.selectbox(
    "Progres",
    [
        "Pengajuan Judul",
        "Skripsi Bab 1",
        "Skripsi Bab 2",
        "Skripsi Bab 3",
         "Seminar Proposal",
        "Skripsi Bab 4",
        "Skripsi Bab 5",
        "Seminar Hasil",
        "Sidang",
        "Revisi",
        "Lulus"
    ]
)


# ==================================================
# UPLOAD SKRIPSI
# ==================================================

st.subheader("Upload File Skripsi")

skripsi_bab1 = st.file_uploader(
    "Skripsi Bab 1",
    type=["pdf", "docx"]
)

skripsi_bab2 = st.file_uploader(
    "Skripsi Bab 2",
    type=["pdf", "docx"]
)

skripsi_bab3 = st.file_uploader(
    "Skripsi Bab 3",
    type=["pdf", "docx"]
)

skripsi_bab4 = st.file_uploader(
    "Skripsi Bab 4",
    type=["pdf", "docx"]
)

skripsi_bab5 = st.file_uploader(
    "Skripsi Bab 5",
    type=["pdf", "docx"]
)

# ==================================================
# SIMPAN DATA
# ==================================================

if st.button("Simpan Data"):

    if nama == "" or nim == "":

        st.warning(
            "Nama dan NIM wajib diisi"
        )

    elif nim in data["NIM"].values:

        st.error(
            "NIM sudah ada"
        )

    else:

        file_skr1 = simpan_file(
            skripsi_bab1,
            nim,
            "SkripsiBab1"
        )

        file_skr2 = simpan_file(
            skripsi_bab2,
            nim,
            "SkripsiBab2"
        )

        file_skr3 = simpan_file(
            skripsi_bab3,
            nim,
            "SkripsiBab3"
        )

        file_skr4 = simpan_file(
            skripsi_bab4,
            nim,
            "SkripsiBab4"
        )

        file_skr5 = simpan_file(
            skripsi_bab5,
            nim,
            "SkripsiBab5"
        )

        data_baru = pd.DataFrame({

            "Nama": [nama],
            "NIM": [nim],
            "No Hp": [no_hp],

            "Pembimbing Akademik": [pa],
            "Pembimbing Skripsi": [ps],
            "Penguji": [penguji],

            "Judul Skripsi": [judul],


            "Skripsi Bab 1": [file_skr1],
            "Skripsi Bab 2": [file_skr2],
            "Skripsi Bab 3": [file_skr3],
            "Skripsi Bab 4": [file_skr4],
            "Skripsi Bab 5": [file_skr5],

            "Progres": [progres]
        })

        data = pd.concat(
            [data, data_baru],
            ignore_index=True
        )

        data.to_excel(
            file_excel,
            index=False
        )

        st.success(
            "Data berhasil disimpan"
        )

        st.rerun()
