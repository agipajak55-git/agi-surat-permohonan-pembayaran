# -*- coding: utf-8 -*-
{
    'name': 'Surat Permohonan Pembayaran Sales Order',
    'version': '16.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Cetak Surat Permohonan Pembayaran dari Sales Order (Odoo 16 Community)',
    'description': """
Module Konversi Generator Surat Permohonan Pembayaran ke Odoo 16 Community
==========================================================================
Fitur:
- Field Dasar Pekerjaan di tab Sales Order > Other Info.
- Menambahkan tombol print "Surat Permohonan Pembayaran" di menu Sales Order (sale.order).
- Penomoran otomatis format: [nomor SO]/Perm.Bayar-FA/AGI/[bulan print]/[tahun print]
- Otomatis menghitung Terbilang dalam Bahasa Indonesia.
- Format penomoran, layout surat, tabel rincian pembayaran, rekening bank, dan daftar lampiran presisi.
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

# Update: Add upgrade flag to force reload report action
