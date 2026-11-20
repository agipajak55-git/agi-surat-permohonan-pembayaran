# -*- coding: utf-8 -*-
{
    'name': 'Surat Permohonan Pembayaran Sales Order (AGI)',
    'version': '16.0.1.2.0',
    'category': 'Sales/Sales',
    'summary': 'Cetak Surat Permohonan Pembayaran PT. Aston Graphindo Indonesia dari Sales Order (Odoo 16 Community)',
    'description': """
Module Konversi Generator Surat Permohonan Pembayaran ke Odoo 16 Community - PT. Aston Graphindo Indonesia
==========================================================================================================
Revisi 16.0.1.2.0:
- Penyesuaian nama Bank Mandiri - KCP Solo Pasar Legi menggunakan karakter strip standar (-) agar tidak menjadi simbol tidak terbaca (â€“).
- Pilihan penandatangan surat & jabatan dinamis pada Sales Order:
  * Anton Wijaya - Direktur
  * Agung Jayadi - Finance
  * Pilihan Custom: dapat mengisi nama & jabatan penandatangan lain secara manual.
- Mengambil tanggal surat & nomor surat (bulan romawi & tahun) dari field 'Tanggal Print' (tanggal_print).
  Jika tanggal_print kosong, otomatis fallback ke tanggal hari ini.
- Lampiran Faktur Pajak bersifat opsional via checkbox 'Lampirkan Faktur Pajak' pada Sales Order:
  * Dicentang: 4 berkas (Invoice, Kuitansi, Faktur Pajak, Salinan dasar) & baris potongan pajak dimunculkan.
  * Tidak dicentang: 3 berkas (tanpa Faktur Pajak) & baris potongan pajak disembunyikan.
- Checkbox 'Pakai Meterai': mengatur jarak tanda tangan 30mm (pakai meterai) atau 10mm (tanpa meterai).
- Penomoran otomatis format: [nomor SO]/Perm.Bayar-FA/AGI/[bulan romawi]/[tahun]
- Terbilang otomatis Bahasa Indonesia (Rupiah).
    """,
    'author': 'PT. Aston Graphindo Indonesia',
    'website': 'https://www.astongraphindo.com',
    'license': 'LGPL-3',
    'depends': [
        'sale',
        'account',
    ],
    'data': [
        'views/sale_order_views.xml',
        'report/report_surat_permohonan_pembayaran.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
