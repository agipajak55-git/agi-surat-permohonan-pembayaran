# -*- coding: utf-8 -*-
{
    'name': 'Surat Permohonan Pembayaran Sales Order (AGI)',
    'version': '16.0.1.3.0',
    'category': 'Sales/Sales',
    'summary': 'Cetak Surat Permohonan Pembayaran PT. Aston Graphindo Indonesia dari Sales Order (Odoo 16 Community)',
    'description': """
Module Konversi Generator Surat Permohonan Pembayaran ke Odoo 16 Community - PT. Aston Graphindo Indonesia
==========================================================================================================
Revisi 16.0.1.3.0:
- Hapus field 'Pakai Meterai', ruang tanda tangan dibuat default 20mm.
- Hapus field duplikat 'Penanda Tangan', disatukan ke field bawaan Odoo 'Ditandatangani Oleh' (who_sign).
- Jabatan penandatangan otomatis diambil dari menu Employee (hr.employee) dengan singkatan departemen standar:
  * Anton Wijaya -> Direktur
  * Danar Susilo -> Manager HR & GA
  * Agung Jayadi -> Staff Finance & Accounting
  * Anwar Wijaya -> Manager SC, Prod & IT
  * Hary Purwoko / Edy Poerwanto -> Supervisor SC, Prod & IT
  * Tim SCM lain -> Staff SC, Prod & IT
  * Tim HRD lain -> Staff HR & GA
  * Tim Sales -> Staff Sales & Marketing
- Penomoran otomatis format: [nomor SO]/Perm.Bayar-FA/AGI/[bulan romawi]/[tahun]
- Tanggal surat dapat disesuaikan lewat field 'Tanggal Print' (fallback ke tanggal hari ini).
- Lampiran Faktur Pajak bersifat opsional via checkbox 'Lampirkan Faktur Pajak'.
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
