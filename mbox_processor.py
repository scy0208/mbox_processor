import mailbox
import csv

def mbox_to_csv(mbox_file_name, csv_file_name, limit=10):
    # Open the mbox file
    mbox = mailbox.mbox(mbox_file_name)

    # Open a CSV writer
    with open(csv_file_name, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write CSV headers
        writer.writerow(['Subject', 'From', 'To', 'Date', 'Body'])
        
        # Loop through limited number of messages in the mbox file
        for idx, message in enumerate(mbox):
            if idx >= limit:
                break

            subject = message['subject']
            from_address = message['from']
            to_address = message['to']
            date = message['date']
            body = message.get_payload(decode=True)
            
            if body:
                # Decode the body if it's bytes
                charset = message.get_content_charset()
                if charset:
                    try:
                        body = body.decode(charset)
                    except:
                        body = body.decode('utf-8', 'ignore')
            
            writer.writerow([subject, from_address, to_address, date, body])

if __name__ == '__main__':
    mbox_file = input('Enter the path to your mbox file: ')
    csv_file = input('Enter the desired output CSV file path: ')
    mbox_to_csv(mbox_file, csv_file)
