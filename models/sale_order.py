# -*- coding: utf-8 -*-
import math
from datetime import datetime, date
from odoo import models, fields, api, _

ROMAN_MONTHS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
BULAN_ID = [
    "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember"
]
SATUAN = [
    "", "satu", "dua", "tiga", "empat", "lima", "enam", "tujuh", "delapan", "sembilan",
    "sepuluh", "sebelas", "dua belas", "tiga belas", "empat belas", "lima belas", "enam belas",
    "tujuh belas", "delapan belas", "sembilan belas"
]


def _tiga_angka(n):
    n = int(math.floor(n))
    s = ""
    if n >= 100:
        r = n // 100
        s += ("seratus" if r == 1 else SATUAN[r] + " ratus") + " "
        n %= 100
    if n > 0:
        if n < 20:
            s += SATUAN[n]
        else:
            puluh = n // 10
            sisa = n % 10
            s += SATUAN[puluh] + " puluh" + (" " + SATUAN[sisa] if sisa > 0 else "")
    return s.strip()


def _terbilang_id(num):
    num = int(math.floor(abs(num or 0)))
    if num == 0:
        return "Nol"
    units = [
        (1000000000000, "triliun"),
        (1000000000, "miliar"),
        (1000000, "juta"),
        (1000, "ribu"),
    ]
    sisa = num
    parts = []
    for val, label in units:
        count = sisa // val
        if count > 0:
            if label == "ribu" and count == 1:
                parts.append("seribu")
            else:
                parts.append(_tiga_angka(count) + " " + label)
            sisa %= val
    if sisa > 0:
        parts.append(_tiga_angka(sisa))
    result = " ".join(parts).strip()
    return result.title()


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    dasar_pekerjaan = fields.Selection([
        ('Purchase Order', 'Purchase Order'),
        ('SPK', 'SPK'),
        ('Kontrak', 'Kontrak'),
        ('Surat Pesanan', 'Surat Pesanan'),
    ], string='Dasar Pekerjaan', default='Purchase Order')

    nomor_dasar_pekerjaan = fields.Char(
        string='Nomor Dasar Pekerjaan',
        help='Nomor dokumen dasar seperti nomor PO, SPK, atau Kontrak'
    )

    tgl_dasar_pekerjaan = fields.Date(string='Tanggal Dasar Pekerjaan')

    jenis_pekerjaan = fields.Char(
        string='Uraian / Jenis Pekerjaan',
        help='misal: Pengadaan Computer Supplies (Cartridge Printer)'
    )

    def get_terbilang_total(self):
        """Mengembalikan teks terbilang dari amount_total dalam format Rupiah."""
        self.ensure_one()
        terbilang_str = _terbilang_id(self.amount_total)
        return f"{terbilang_str} Rupiah"

    def get_nomor_surat_permohonan(self):
        """
        Format nomor surat: [nomor SO]/Perm.Bayar-FA/AGI/[bulan tanggal_print]/[tahun tanggal_print]
        Berdasarkan tanggal cetak/print (datetime.today()).
        """
        self.ensure_one()
        dt = datetime.today()
        bulan_romawi = ROMAN_MONTHS[dt.month - 1]
        tahun = dt.year
        nomor_bersih = (self.name or "SO").replace("/", "-")
        return f"{nomor_bersih}/Perm.Bayar-FA/AGI/{bulan_romawi}/{tahun}"

    def get_tanggal_surat_panjang(self):
        """Format tanggal surat cetak: e.g. '8 September 2026'."""
        self.ensure_one()
        dt = datetime.today()
        return f"{dt.day} {BULAN_ID[dt.month - 1]} {dt.year}"

    def get_kota_surat(self):
        """Mengembalikan kota perusahaan atau default Karanganyar."""
        self.ensure_one()
        return self.company_id.city or self.company_id.partner_id.city or "Karanganyar"

    def get_jabatan_penerima(self):
        """Mengembalikan jabatan penerima dari kontak partner."""
        self.ensure_one()
        p = self.partner_id
        if p.function:
            return p.function
        elif p.title and p.title.name:
            return p.title.name
        return "Pejabat Pembuat Komitmen / Bendahara"

    def get_nama_instansi(self):
        """Mengembalikan nama instansi / perusahaan pelanggan."""
        self.ensure_one()
        p = self.partner_id
        if p.parent_id and p.parent_id.name:
            return p.parent_id.name
        elif p.commercial_partner_id and p.commercial_partner_id.name:
            return p.commercial_partner_id.name
        return p.name or "-"

    def get_uraian_pekerjaan(self):
        """Mengambil uraian pekerjaan dari field jenis_pekerjaan, order line, atau note."""
        self.ensure_one()
        if self.jenis_pekerjaan:
            return self.jenis_pekerjaan
        lines = self.order_line.filtered(lambda l: not l.display_type)
        if lines:
            line_names = [l.name.split('\n')[0].strip() for l in lines if l.name]
            return ", ".join(line_names)
        return self.note or "Pengadaan Barang / Jasa"

    def get_dasar_pekerjaan(self):
        """
        Mengembalikan informasi dasar pekerjaan (Jenis dokumen, Nomor, Tanggal)
        dari field dasar_pekerjaan, nomor_dasar_pekerjaan, client_order_ref, & tgl_dasar_pekerjaan.
        """
        self.ensure_one()
        jenis = self.dasar_pekerjaan or "Purchase Order"
        nomor = self.nomor_dasar_pekerjaan or self.client_order_ref or self.origin or self.name or "-"
        dt = self.tgl_dasar_pekerjaan or self.date_order or date.today()
        tanggal = f"{dt.day} {BULAN_ID[dt.month - 1]} {dt.year}"
        return {
            'jenis': jenis,
            'nomor': nomor,
            'tanggal': tanggal
        }

    def get_bank_info(self):
        """Mengambil rekening bank perusahaan dengan strip normal."""
        self.ensure_one()
        company = self.company_id
        bank_accounts = company.partner_id.bank_ids or self.env['res.partner.bank'].search([
            ('company_id', '=', company.id)
        ], limit=1)

        if bank_accounts:
            acc = bank_accounts[0]
            nama_bank = acc.bank_id.name if acc.bank_id else (acc.bank_name or "Mandiri")
            nama_bank = nama_bank.replace("–", "-").replace("—", "-")
            return {
                'nama_bank': nama_bank,
                'no_rek': acc.acc_number or "-",
                'atas_nama': acc.acc_holder_name or company.name or "-"
            }
        return {
            'nama_bank': "Mandiri - KCP Solo Pasar Legi",
            'no_rek': "138 00 0790783 0",
            'atas_nama': company.name or "PT. Aston Graphindo Indonesia"
        }

    def get_penandatangan(self):
        """Mengambil data penandatangan langsung dari field many2one 'who_sign' yang sudah ada di database."""
        self.ensure_one()
        # Mengambil nama dari record res.users relasi many2one field who_sign
        sign_user = getattr(self, 'who_sign', False)
        if sign_user:
            nama = sign_user.name
        else:
            nama = (self.user_id and self.user_id.name) or "Agung Jayadi"
        
        return {
            'who_sign': nama,
            'nama': nama,
            'jabatan': "Finance"
        }

    def get_lampiran_info(self):
        """
        Menentukan daftar lampiran dan jumlah total berkas berdasarkan nilai SO.
        Jika amount_total <= 2,000,000 (tidak kena Faktur Pajak), lampiran 3 berkas.
        Jika > 2,000,000, lampiran 4 berkas.
        """
        self.ensure_one()
        total = self.amount_total or 0
        if total <= 2000000:
            items = [
                "Invoice",
                "Kuitansi",
                "Salinan dasar pekerjaan (Purchase Order/SPK/Kontrak)"
            ]
            count_text = "3 (tiga)"
        else:
            items = [
                "Invoice",
                "Kuitansi",
                "Faktur Pajak",
                "Salinan dasar pekerjaan (Purchase Order/SPK/Kontrak)"
            ]
            count_text = "4 (empat)"
        return {
            'items': items,
            'count_text': count_text
        }
