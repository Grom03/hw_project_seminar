import imaplib
import email
import email.message
import sys


def get_mail_server(login, password):
    try:
        mail = imaplib.IMAP4_SSL('imap.yandex.ru', 993)
        mail.login(login, password)
        mail.select('INBOX')
        return mail
    except imaplib.IMAP4_SSL.error as e:
        print("There's IMAP error " + e)
        return None


def get_unseen_emails_for_last_x_days(mail_server, sent_since, mails_number):
    filter = f'UNSEEN SENTSINCE {sent_since}'
    _, data = mail_server.search(None, filter)

    ids = data[0]
    id_list = ids.split()

    if len(id_list) < mails_number:
        mails_number = len(id_list)

    for i in range(1, mails_number + 1):
        _, data = mail_server.fetch(id_list[-i], "(RFC822)")
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)

        print("From: {}".format(email_message['From']))
        print("Subject: {}".format(email_message['Subject']))
        print("Date: {}".format(email_message['Date']))

        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == 'text/plain':
                    print(part.get_payload(decode=True).decode('utf-8'))
        else:
            print(email_message.get_payload(decode=True).decode('utf-8'))
        print('-' * 50)

if __name__ == '__main__':
    if len(sys.argv) < 5:
        raise RuntimeError("Unexpected: less than 4 arguments")
    login = sys.argv[1]
    password = sys.argv[2]
    sent_since = sys.argv[3]
    mails_number = sys.argv[4]

    mail_server = get_mail_server(login, password)
    get_unseen_emails_for_last_x_days(mail_server, sent_since, mails_number)
