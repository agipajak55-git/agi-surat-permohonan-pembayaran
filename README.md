# Module Surat Permohonan Pembayaran (Odoo 16 Community)

Module ini mengonversi fungsionalitas dan tata letak dari **Generator Surat Permohonan Pembayaran** ke dalam modul Odoo 16 Community.

## Fitur Utama
1. **Menu Sales Order > Print > "Surat Permohonan Pembayaran"**:
   - Menambahkan opsi cetak surat permohonan pembayaran resmi dalam format PDF langsung dari dokumen Sales Order (`sale.order`).
2. **Tanpa Mengubah / Menambah Kolom Baru Database**:
   - Memetakan field standard Odoo secara dinamis:
     - **Nomor Surat**: `<SO_NAME>/Perm.Bayar-FA/AGI/<BULAN_ROMAWI>/<TAHUN>`
     - **Tujuan Surat**: `partner_id.name`, `partner_id.parent_id`, `partner_id.function`
     - **Dasar Pekerjaan**: `client_order_ref` (Customer Reference / PO No) & `date_order`
     - **Uraian Pekerjaan**: Deskripsi dari `order_line` / `product_id`
     - **Nilai & Terbilang**: `amount_total` dihitung otomatis ke kalimat terbilang Rupiah
     - **Rekening Pembayaran**: Master data `res.partner.bank` pada profil Company
     - **Penandatangan**: Data Salesperson (`user_id.name`) & Jabatan
3. **Format Layout Presisi**:
   - Dilengkapi ruang kop surat (25-27mm) untuk kertas berkop instansi/perusahaan.
   - Aturan baris potongan pajak otomatis (aktif untuk nilai di atas Rp 2.000.000,-).

## Cara Pasang (Install)
1. Salin folder `surat_permohonan_pembayaran` ke direktori `addons` Odoo 16 Anda (misal: `/opt/odoo/custom-addons/`).
2. Restart service Odoo:
   ```bash
   sudo systemctl restart odoo
   ```
3. Buka browser, aktifkan **Developer Mode** di Odoo (Settings > Activate the developer mode).
4. Masuk ke menu **Apps** > klik tombol **Update Apps List**.
5. Cari `Surat Permohonan Pembayaran` atau `surat_permohonan_pembayaran`, lalu klik **Install / Pasang**.
6. Masuk ke menu **Sales** > buka salah satu dokumen **Sales Order** > klik tombol **Print** > pilih **"Surat Permohonan Pembayaran"**.
