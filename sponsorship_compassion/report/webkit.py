import tempfile
import os
import time
import subprocess

from openerp.addons.report_webkit import webkit_report
from openerp.osv import fields, orm
from openerp.tools.translate import _

import logging
logger = logging.getLogger(__name__)

class HeaderHTML(orm.Model):
    """HTML Header allows you to define HTML CSS and Page format"""
    _inherit = "ir.header_webkit"
    
    _columns = {
        'page_width': fields.float('Page width (mm)'),
        'page_height': fields.float('Page height (mm)'),
        'format': fields.selection(
            [
            ('A0' ,'A0  5   841 x 1189 mm'),
            ('A1' ,'A1  6   594 x 841 mm'),
            ('A2' ,'A2  7   420 x 594 mm'),
            ('A3' ,'A3  8   297 x 420 mm'),
            ('A4' ,'A4  0   210 x 297 mm, 8.26 x 11.69 inches'),
            ('A5' ,'A5  9   148 x 210 mm'),
            ('A6' ,'A6  10  105 x 148 mm'),
            ('A7' ,'A7  11  74 x 105 mm'),
            ('A8' ,'A8  12  52 x 74 mm'),
            ('A9' ,'A9  13  37 x 52 mm'),
            ('B0' ,'B0  14  1000 x 1414 mm'),
            ('B1' ,'B1  15  707 x 1000 mm'),
            ('B2' ,'B2  17  500 x 707 mm'),
            ('B3' ,'B3  18  353 x 500 mm'),
            ('B4' ,'B4  19  250 x 353 mm'),
            ('B5' ,'B5  1   176 x 250 mm, 6.93 x 9.84 inches'),
            ('B6' ,'B6  20  125 x 176 mm'),
            ('B7' ,'B7  21  88 x 125 mm'),
            ('B8' ,'B8  22  62 x 88 mm'),
            ('B9' ,'B9  23  33 x 62 mm'),
            ('B10',':B10    16  31 x 44 mm'),
            ('C5E','C5E 24  163 x 229 mm'),
            ('Comm10E','Comm10E 25  105 x 241 mm, U.S. Common 10 Envelope'),
            ('DLE', 'DLE 26 110 x 220 mm'),
            ('Executive','Executive 4   7.5 x 10 inches, 190.5 x 254 mm'),
            ('Folio','Folio 27  210 x 330 mm'),
            ('Ledger', 'Ledger  28  431.8 x 279.4 mm'),
            ('Legal', 'Legal    3   8.5 x 14 inches, 215.9 x 355.6 mm'),
            ('Letter','Letter 2 8.5 x 11 inches, 215.9 x 279.4 mm'),
            ('Tabloid', 'Tabloid 29 279.4 x 431.8 mm'),
            ],
            'Paper size',
            required=False,
            help="Select Proper Paper size"
            ),
        }

def generate_pdf(self, comm_path, report_xml, header, footer, html_list, webkit_header=False):
    """Call webkit in order to generate pdf"""
    if not webkit_header:
        webkit_header = report_xml.webkit_header
    tmp_dir = tempfile.gettempdir()
    out_filename = tempfile.mktemp(suffix=".pdf", prefix="webkit.tmp.")
    file_to_del = [out_filename]
    if comm_path:
        command = [comm_path]
    else:
        command = ['wkhtmltopdf']

    command.append('--quiet')
    # default to UTF-8 encoding.  Use <meta charset="latin-1"> to override.
    command.extend(['--encoding', 'utf-8'])
    if header :
        head_file = file( os.path.join(
                              tmp_dir,
                              str(time.time()) + '.head.html'
                             ),
                            'w'
                        )
        head_file.write(self._sanitize_html(header))
        head_file.close()
        file_to_del.append(head_file.name)
        command.extend(['--header-html', head_file.name])
    if footer :
        foot_file = file(  os.path.join(
                              tmp_dir,
                              str(time.time()) + '.foot.html'
                             ),
                            'w'
                        )
        foot_file.write(self._sanitize_html(footer))
        foot_file.close()
        file_to_del.append(foot_file.name)
        command.extend(['--footer-html', foot_file.name])

    if webkit_header.margin_top :
        command.extend(['--margin-top', str(webkit_header.margin_top).replace(',', '.')])
    if webkit_header.margin_bottom :
        command.extend(['--margin-bottom', str(webkit_header.margin_bottom).replace(',', '.')])
    if webkit_header.margin_left :
        command.extend(['--margin-left', str(webkit_header.margin_left).replace(',', '.')])
    if webkit_header.margin_right :
        command.extend(['--margin-right', str(webkit_header.margin_right).replace(',', '.')])
    if webkit_header.orientation :
        command.extend(['--orientation', str(webkit_header.orientation).replace(',', '.')])
    if webkit_header.format :
        command.extend(['--page-size', str(webkit_header.format).replace(',', '.')])
    if webkit_header.page_width :
        command.extend(['--page-width', str(webkit_header.page_width).replace(',', '.')])
    if webkit_header.page_height :
        command.extend(['--page-height', str(webkit_header.page_height).replace(',', '.')])
    count = 0
    for html in html_list :
        html_file = file(os.path.join(tmp_dir, str(time.time()) + str(count) +'.body.html'), 'w')
        count += 1
        html_file.write(self._sanitize_html(html))
        html_file.close()
        file_to_del.append(html_file.name)
        command.append(html_file.name)
    command.append(out_filename)
    stderr_fd, stderr_path = tempfile.mkstemp(text=True)
    file_to_del.append(stderr_path)
    
    logger.info("Command: %s" % command)
    try:
        status = subprocess.call(command, stderr=stderr_fd)
        os.close(stderr_fd) # ensure flush before reading
        stderr_fd = None # avoid closing again in finally block
        fobj = open(stderr_path, 'r')
        error_message = fobj.read()
        fobj.close()
        if not error_message:
            error_message = _('No diagnosis message was provided')
        else:
            error_message = _('The following diagnosis message was provided:\n') + error_message
        if status :
            raise except_osv(_('Webkit error' ),
                             _("The command 'wkhtmltopdf' failed with error code = %s. Message: %s") % (status, error_message))
        pdf_file = open(out_filename, 'rb')
        pdf = pdf_file.read()
        pdf_file.close()
    finally:
        if stderr_fd is not None:
            os.close(stderr_fd)
        for f_to_del in file_to_del:
            try:
                os.unlink(f_to_del)
            except (OSError, IOError), exc:
                logger.error('cannot remove file %s: %s', f_to_del, exc)
    return pdf

webkit_report.WebKitParser.generate_pdf = generate_pdf
