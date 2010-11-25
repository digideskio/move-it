
from childcount.reports.statistics import form_reporting, matching_message_stats
from childcount.reports.report_framework import PrintedReport

class Report(PrintedReport):
    title = 'Form C Entered by Day'
    filename = 'form_c_entered'
    formats = ['pdf','xls','html']
    argvs = []

    def generate(self, rformat, **kwargs):
        return form_reporting(
            rformat,
            u'Form C (Follow-Up) Per Day',
            matching_message_stats(\
                ' `text` LIKE "%%+U %%" OR \
                  `text` LIKE "%%+S %%" OR \
                  `text` LIKE "%%+P %%" OR \
                  `text` LIKE "%%+N %%" OR \
                  `text` LIKE "%%+T %%" OR \
                  `text` LIKE "%%+M %%" OR \
                  `text` LIKE "%%+F %%" OR \
                  `text` LIKE "%%+G %%" OR \
                  `text` LIKE "%%+R %%" AND \
                `text` LIKE "%%Successfully processed: [%%%%" AND \
                `backend` = "debackend" '),
            self.get_filepath(rformat))