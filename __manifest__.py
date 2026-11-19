# -*- coding: utf-8 -*-
{
    'name': 'Surat Permohonan Pembayaran Sales Order (AGI)',
    'version': '16.0.1.1.0',
    'category': 'Sales/Sales',
    'summary': 'Cetak Surat Permohonan Pembayaran PT. Aston Graphindo Indonesia dari Sales Order (Odoo 16 Community)',
    'description': """
Module Konversi Generator Surat Permohonan Pembayaran ke Odoo 16 Community - PT. Aston Graphindo Indonesia
==========================================================================================================
Revisi:
- Mengambil tanggal surat & nomor surat (bulan romawi & tahun) dari field 'Tanggal Print' (tanggal_print).
  Jika tanggal_print kosong, otomatis fallback ke tanggal hari ini.
- Lampiran Faktur Pajak bersifat opsional via checkbox 'Lampirkan Faktur Pajak' pada Sales Order:
  * Dicentang: 4 berkas (Invoice, Kuitansi, Faktur Pajak, Salinan dasar) & baris potongan pajak dimunculkan.
  * Tidak dicentang: 3 berkas (tanpa Faktur Pajak) & baris potongan pajak disembunyikan.
- Checkbox 'Pakai Meterai': mengatur jarak tanda tangan 30mm (pakai meterai) atau 10mm (tanpa meterai).
- Penomoran otomatis format: [nomor SO]/Perm.Bayar-FA/AGI/[bulan romawi]/[tahun]
- Terbilang otomatis Bahasa Indonesia (Rupiah).
- Rincian Bank Mandiri KCP Solo Pasar Legi AGI, tata letak presisi sesuai kop surat & generator HTML.
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
