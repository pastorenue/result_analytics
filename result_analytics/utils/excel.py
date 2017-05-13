from django.db import models
from django.db.models import fields
import csv, xlwt
from datetime import date, datetime
from itertools import groupby
from xlwt import Workbook, easyxf

class CsvReport(object):
    def __init__(self, data, fields=[]):
        self.data = data
        self.fields = fields

    @property
    def headers(self):
        """Get the header row for this report."""
        return [fld_name.replace('_', ' ').title() for fld_name in self.fields]

    def get_row_values(self, item):
        """Return a list of values for a row of data."""
        return [getattr(item, name, '') for name in self.fields]

    def write(self, outfile):
        writer = csv.writer(outfile)
        writer.writerow(self.get_headers())
        for item in self.data:
            writer.writerow(self.get_row_values(item))

styles = {
    'header': easyxf(
        'font: name Trebuchet MS, bold True, color black, height 240;'
        'borders: bottom 6, bottom_color black;'
        ),
    'subheader': easyxf(
        'font: name Trebuchet MS, bold True, color black, height 220;'
        ),
    'data': easyxf(
        'font: name Trebuchet MS, color gray80;'
        'borders: bottom 1, bottom_color gray25;'
        ),
    'date': easyxf(
        'font: name Trebuchet MS, color gray80;'
        'borders: bottom 1, bottom_color gray25;',
        num_format_str='D MMM YYYY'
        )
    }

class ExcelReport(CsvReport):
    def __init__(self, data, fields=[], groupby=None):
        super(ExcelReport, self).__init__(data, fields)
        if groupby and groupby not in self.fields:
            raise ValueError('%s is not a valid field for grouping.' % groupby)
        self.groupby = groupby
        
    def write_cell_data(self, sheet, pos, val):
        """Writes the data at the specified position."""
        row, col = pos
        if isinstance(val, (date, datetime)):
            sheet.write(row, col, label=val, style=styles['date'])
        else:
            sheet.write(row, col, label=val, style=styles['data'])

    def export_qs(self, sheet):
        """Export a Queryset to excel."""
        opts = self.data.model._meta
        row = 4
        for item in self.data:
            col = 0
            for name in self.fields:
                val = getattr(item, name, '')
                self.write_cell_data(sheet, (row, col), val)
                col += 1
            row += 1

    def export_list(self, sheet):
        """Export a list of items to excel, optionally grouping by `groupby`."""
        if self.groupby:
            idx = self.fields.index(self.groupby)
            groups = []
            uniquekeys = []
            queryset = sorted(self.data, key=lambda x: x[idx])
            for key, group in groupby(queryset, key=lambda x: x[idx]):
                groups.append(list(group))
                uniquekeys.append(key)
            row = 1
            for grouper, group in zip(uniquekeys, groups):
                sheet.write(row, 0, u'', styles['data'])
                sheet.write(row + 1, 0, grouper, styles['subheader'])
                row += 2
                for line in group:
                    col = 0
                    for val in line:
                        self.write_cell_data(sheet, (row, col), val)
                        col += 1
                    row += 1
        else:
            row = 1
            for line in self.data:
                col = 0
                for val in line:
                    self.write_cell_data(sheet, (row, col), val)
                    col += 1
                row += 1

    def write(self, outfile):
        wbook = Workbook(encoding='ascii')
        sheet = wbook.add_sheet('Report')
        
        for idx, header in enumerate(self.headers):
            if sheet.col(idx).width < int(256 * (len(header) + 5)):
                sheet.col(idx).width = int(256 * (len(header) + 5))
            sheet.write(0, idx, header, styles['header'])
            
        if hasattr(self.data, 'model') and issubclass(self.data.model, models.Model):
            # `data` is a Django Queryset:
            self.export_qs(sheet)
        else:
            # `data` is a list or other iterable:
            self.export_list(sheet)
            
        wbook.save(outfile)

