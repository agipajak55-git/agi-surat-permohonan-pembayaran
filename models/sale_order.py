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

    tanggal_print = fields.Date(
        string='Tanggal Print',
        help='Tanggal yang digunakan pada Surat Permohonan Pembayaran. Jika kosong, otomatis memakai tanggal hari ini.'
    )

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

    lampirkan_faktur_pajak = fields.Boolean(
        string='Lampirkan Faktur Pajak',
        default=True,
        help='Centang jika surat permohonan pembayaran menyertakan lampiran Faktur Pajak dan rincian potongan.'
    )

    pakai_meterai = fields.Boolean(
        string='Pakai Meterai',
        default=True,
        help='Centang jika surat memerlukan ruang tempel meterai (30mm). Jika tidak, ruang tanda tangan 10mm.'
    )

    def _default_penandatangan_surat(self):
        user = self.env.user
        if user and user.name and "anton" in user.name.lower():
            return 'anton'
        return 'agung'

    def _default_nama_penandatangan(self):
        user = self.env.user
        if user and user.name and "anton" in user.name.lower():
            return 'Anton Wijaya'
        return 'Agung Jayadi'

    def _default_jabatan_penandatangan(self):
        user = self.env.user
        if user and user.name and "anton" in user.name.lower():
            return 'Direktur'
        return 'Finance'

    penandatangan_surat = fields.Selection([
        ('agung', 'Agung Jayadi - Finance'),
        ('anton', 'Anton Wijaya - Direktur'),
        ('custom', 'Nama & Jabatan Lain (Custom)'),
    ], string='Penanda Tangan', default=_default_penandatangan_surat,
       help='Pilih penandatangan untuk Surat Permohonan Pembayaran.')

    nama_penandatangan = fields.Char(
        string='Nama Penanda Tangan',
        default=_default_nama_penandatangan,
        help='Nama yang akan tercetak pada tanda tangan surat.'
    )

    jabatan_penandatangan = fields.Char(
        string='Jabatan Penanda Tangan',
        default=_default_jabatan_penandatangan,
        help='Jabatan yang akan tercetak di bawah nama penandatangan.'
    )

    @api.onchange('penandatangan_surat')
    def _onchange_penandatangan_surat(self):
        if self.penandatangan_surat == 'anton':
            self.nama_penandatangan = "Anton Wijaya"
            self.jabatan_penandatangan = "Direktur"
        elif self.penandatangan_surat == 'agung':
            self.nama_penandatangan = "Agung Jayadi"
            self.jabatan_penandatangan = "Finance"
        elif self.penandatangan_surat == 'custom':
            if not self.nama_penandatangan or self.nama_penandatangan in ["Agung Jayadi", "Anton Wijaya"]:
                self.nama_penandatangan = ""
                self.jabatan_penandatangan = ""

    @api.onchange('user_id')
    def _onchange_user_id_penandatangan(self):
        if self.user_id and self.user_id.name:
            user_name_lower = self.user_id.name.lower()
            if 'anton' in user_name_lower:
                self.penandatangan_surat = 'anton'
                self.nama_penandatangan = "Anton Wijaya"
                self.jabatan_penandatangan = "Direktur"
            elif 'agung' in user_name_lower:
                self.penandatangan_surat = 'agung'
                self.nama_penandatangan = "Agung Jayadi"
                self.jabatan_penandatangan = "Finance"

    @api.onchange('amount_total')
    def _onchange_amount_total_faktur_pajak(self):
        """Otomatis memberi saran centang Faktur Pajak jika > 2jt, tetap dapat diubah manual kapan saja."""
        if self.amount_total:
            self.lampirkan_faktur_pajak = (self.amount_total > 2000000)

    def _get_effective_surat_date(self):
        """Mengambil tanggal surat: menggunakan tanggal_print jika diisi, jika kosong memakai hari ini."""
        self.ensure_one()
        d = self.tanggal_print
        if not d:
            return date.today()
        if isinstance(d, str):
            return fields.Date.from_string(d)
        if isinstance(d, datetime):
            return d.date()
        return d

    def get_terbilang_total(self):
        """Mengembalikan teks terbilang dari amount_total dalam format Rupiah."""
        self.ensure_one()
        terbilang_str = _terbilang_id(self.amount_total)
        return f"{terbilang_str} Rupiah"

    def get_nomor_surat_permohonan(self):
        """
        Format nomor surat AGI: [nomor SO]/Perm.Bayar-FA/AGI/[bulan romawi]/[tahun]
        Bulan romawi dan tahun mengikuti field Tanggal Print (atau hari ini).
        """
        self.ensure_one()
        dt = self._get_effective_surat_date()
        bulan_romawi = ROMAN_MONTHS[dt.month - 1]
        tahun = dt.year
        nomor_bersih = (self.name or "SO").replace("/", "-")
        return f"{nomor_bersih}/Perm.Bayar-FA/AGI/{bulan_romawi}/{tahun}"

    def get_tanggal_surat_panjang(self):
        """Format tanggal surat cetak: e.g. '19 November 2026'."""
        self.ensure_one()
        dt = self._get_effective_surat_date()
        return f"{dt.day} {BULAN_ID[dt.month - 1]} {dt.year}"

    def get_kota_surat(self):
        """Mengembalikan kota perusahaan atau default Karanganyar."""
        self.ensure_one()
        return self.company_id.city or self.company_id.partner_id.city or "Karanganyar"

    def get_jabatan_penerima(self):
        """Mengembalikan jabatan penerima dari opsi_penerima atau kontak partner."""
        self.ensure_one()
        if hasattr(self, 'opsi_penerima') and self.opsi_penerima:
            map_opsi = {
                'kuasa': 'Kuasa Pengguna Anggaran',
                'bendahara': 'Bendahara Pengeluaran',
                'pejabat': 'Pejabat Pembuat Komitmen',
            }
            if self.opsi_penerima in map_opsi:
                return map_opsi[self.opsi_penerima]
        p = self.partner_id
        if p.function:
            return p.function
        elif p.title and p.title.name:
            return p.title.name
        return "Pejabat Pembuat Komitmen / Bendahara"

    def get_nama_instansi(self):
        """Mengembalikan nama instansi / satuan kerja pelanggan."""
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
        dt = self.tgl_dasar_pekerjaan or (self.date_order and self.date_order.date()) or date.today()
        tanggal = f"{dt.day} {BULAN_ID[dt.month - 1]} {dt.year}"
        return {
            'jenis': jenis,
            'nomor': nomor,
            'tanggal': tanggal
        }

    def get_bank_info(self):
        """Mengambil rekening bank AGI dengan fallback default Mandiri - KCP Solo Pasar Legi."""
        self.ensure_one()
        company = self.company_id
        bank_accounts = company.partner_id.bank_ids or self.env['res.partner.bank'].search([
            ('company_id', '=', company.id)
        ], limit=1)

        if bank_accounts:
            acc = bank_accounts[0]
            nama_bank = acc.bank_id.name if acc.bank_id else (acc.bank_name or "Mandiri")
            nama_bank = (nama_bank or "").replace("–", "-").replace("—", "-").replace("â€“", "-").replace("â€”", "-")
            atas_nama = acc.acc_holder_name or company.name or "PT. Aston Graphindo Indonesia"
            atas_nama = (atas_nama or "").replace("–", "-").replace("—", "-").replace("â€“", "-").replace("â€”", "-")
            return {
                'nama_bank': nama_bank,
                'no_rek': acc.acc_number or "-",
                'atas_nama': atas_nama
            }
        return {
            'nama_bank': "Mandiri - KCP Solo Pasar Legi",
            'no_rek': "138 00 0790783 0",
            'atas_nama': company.name or "PT. Aston Graphindo Indonesia"
        }

    def get_penandatangan(self):
        """
        Mengambil data penandatangan dan jabatannya:
        - Anton Wijaya -> Direktur
        - Agung Jayadi -> Finance
        - Custom -> nama & jabatan sesuai inputan manual
        - Fallback: who_sign / user_id
        """
        self.ensure_one()
        nama = ""
        jabatan = ""

        if self.penandatangan_surat == 'anton':
            nama = self.nama_penandatangan or "Anton Wijaya"
            jabatan = self.jabatan_penandatangan or "Direktur"
        elif self.penandatangan_surat == 'agung':
            nama = self.nama_penandatangan or "Agung Jayadi"
            jabatan = self.jabatan_penandatangan or "Finance"
        elif self.penandatangan_surat == 'custom':
            nama = self.nama_penandatangan or ""
            jabatan = self.jabatan_penandatangan or ""
        else:
            if self.nama_penandatangan:
                nama = self.nama_penandatangan
                jabatan = self.jabatan_penandatangan
            else:
                sign_user = getattr(self, 'who_sign', False)
                if sign_user and hasattr(sign_user, 'name') and sign_user.name:
                    nama = sign_user.name
                elif self.user_id and self.user_id.name:
                    nama = self.user_id.name
                else:
                    nama = "Agung Jayadi"

        # Deteksi pintar jabatan jika belum terisi
        if not jabatan:
            nama_lower = (nama or "").lower()
            if "anton" in nama_lower:
                jabatan = "Direktur"
            elif "agung" in nama_lower:
                jabatan = "Finance"
            else:
                job = False
                if hasattr(self, 'user_id') and self.user_id and hasattr(self.user_id, 'partner_id') and self.user_id.partner_id and self.user_id.partner_id.function:
                    job = self.user_id.partner_id.function
                jabatan = job or "Finance"

        if not nama:
            nama = "Agung Jayadi"
            if not jabatan:
                jabatan = "Finance"

        return {
            'who_sign': nama,
            'nama': nama,
            'jabatan': jabatan
        }

    def get_lampiran_info(self):
        """
        Menentukan daftar lampiran dan jumlah total berkas berdasarkan checkbox lampirkan_faktur_pajak.
        Jika dicentang: 4 (empat) berkas (termasuk Faktur Pajak).
        Jika tidak dicentang: 3 (tiga) berkas (tanpa Faktur Pajak).
        """
        self.ensure_one()
        if self.lampirkan_faktur_pajak:
            items = [
                "Invoice",
                "Kuitansi",
                "Faktur Pajak",
                "Salinan dasar pekerjaan (Purchase Order/SPK/Kontrak)"
            ]
            count_text = "4 (empat)"
        else:
            items = [
                "Invoice",
                "Kuitansi",
                "Salinan dasar pekerjaan (Purchase Order/SPK/Kontrak)"
            ]
            count_text = "3 (tiga)"
        return {
            'items': items,
            'count_text': count_text
        }
