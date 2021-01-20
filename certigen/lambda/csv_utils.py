import csv


class CSV_Utils:

    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.data = dict()

        self.extract_data()

    def extract_data(self):

        with open(self.csv_file_path) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')

            self.raw_data = list()
            self.names = list()
            self.emails = list()

            for row in csv_reader:
                self.raw_data.append(row)
                self.names.append(row['Name'])
                self.emails.append(row['Email'])

    def emails_as_chunks(self, recipients_at_a_time=10):
        emails = self.emails
        email_list_chucks = [emails[i:i + recipients_at_a_time]
                             for i in range(0, len(emails), recipients_at_a_time)]

        return email_list_chucks    
