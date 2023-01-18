import datetime
import re
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .constan_service import ConstantService


class MailUtilities(object):
    @staticmethod
    def send_success_notification(emails, download_link, start_dt):
        raw_body = '''
        <body style="font-family:arial;">
                      Dear <span>friends</span>,<br><br>

                    <table style="text-align:left;width:100%;font-family:arial">
                         <tr>
                            <td style="padding-bottom:10px;">{head_message}</td>
                         </tr>
        				 <tr>
                            <td style="padding-bottom:10px;">Status: {status}</td>
                         </tr>
                         <tr>
                            <td style="padding-bottom:10px;">Download Link: {download_link}</td>
                         </tr>
        				 <tr>
                            <td>Start Date/Time : {dt}</td>
                         </tr>
                         <tr>
                            <td>End Date/Time : {dtt}</td>
                         </tr>

                    </table>
                        <br><br><br><br><br><br><br>
        				Regards,
                        <br><span style="color:#0073A5"> Employee Ms</span>
                        <br><span style="color:#0073A5">(Employee Ms-Platform)</span>
                </html>
        '''
        now = datetime.datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        # head_message = "Xignite {type} process has been started."
        head_message = "Execution successfully Completed"

        status = "Completed"

        to = emails
        cc = ConstantService.cc_mail_id()
        subject = " Employee Ms Notification - Success"

        head_message.format(type="Quarterly")
        body = raw_body.format(head_message=head_message, status=status, download_link=download_link,
                               dt=start_dt, dtt=dt_string)

        sent_mail = MailUtilities.sendHtmlMail(to, cc, subject, body)
        if sent_mail is True:
            return "Email has been sent"

    @staticmethod
    def send_failed_notification(emails, error_log, start_dt):
        raw_body = '''
        <body style="font-family:arial;">
                      Dear <span>friends</span>,<br><br>

                    <table style="text-align:left;width:100%;font-family:arial">
                         <tr>
                            <td style="padding-bottom:10px;">{head_message}</td>
                         </tr>
        				 <tr>
                            <td style="padding-bottom:10px;">Status: {status}</td>
                         </tr>
                         <tr>
                            <td>Start Date/Time : {dt}</td>
                         </tr>
                         <tr>
                            <td>End Date/Time : {dtt}</td>
                         </tr>
                         <tr>
                            <td style="padding-bottom:10px;"><br>Error Log: {error_log}</td>
                         </tr>


                    </table>
                        <br><br><br><br><br><br><br>
                        
        				Regards,
                        <br><span style="color:#0073A5"> Employee Ms</span>
                        <br><span style="color:#0073A5">(Employee Ms-Platform)</span>
                </html>
        '''
        now = datetime.datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        # head_message = "Xignite {type} process has been started."
        head_message = " Execution failed."
        status = "Failed"
        to = emails
        cc = ConstantService.cc_mail_id()
        subject = "  Execution failed - Failed"
        head_message.format(type="Quarterly")
        body = raw_body.format(head_message=head_message, status=status,
                               dt=start_dt, dtt=dt_string, download_link=error_log)
        MailUtilities.sendHtmlMail(to, cc, subject, body)

    @staticmethod
    def sendPlainMail(to=None, cc=None, subject=None, body=None):

        status = False

        frm = "subham.thakurela@gmail.com"
        all_add = cc.split(',') + [to]
        msg = MIMEMultipart()
        msg['From'] = frm
        msg['To'] = to
        msg['Cc'] = cc
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))
        text = msg.as_string()
        try:
            s_mail = smtplib.SMTP("smtp.gmail.com", 587)
            s_mail.set_debuglevel(2)
            s_mail.ehlo()
            s_mail.starttls()
            s_mail.ehlo()
            s_mail.login("subham.thakurela@gmail.com", "milslaixmobfcmpa")
            time.sleep(3)
            s_mail.sendmail(frm, all_add, text)
            status = True
            print("Email has been sent")
            '''logger.logg(debug_msg='Error while sending mail.',
                        info_msg='Mail has been sent',
                        warning_msg=None,
                        error_msg='Module = ' + "mailer.py",
                        critical_msg=None)'''
        except Exception as e:
            ''' logger.logg(debug_msg='Error while sending mail.',
                         info_msg='Mail could not be sent',
                         warning_msg='Error in sending mail',
                         error_msg='Module = ' + "mailer.py",
                         critical_msg=str(e))'''

        return status

    @staticmethod
    def sendHtmlMail(to=None, cc=None, subject=None, body=None):

        status = False
        # logger = Logger()

        frm = "subham.thakurela@gmail.com"
        all_add = cc.split(',') + [to]
        msg = MIMEMultipart()
        msg['From'] = frm
        msg['To'] = to
        msg['Cc'] = cc
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'html'))
        text = msg.as_string()
        try:
            s_mail = smtplib.SMTP("smtp.gmail.com", 587)
            s_mail.set_debuglevel(2)
            s_mail.ehlo()
            s_mail.starttls()
            s_mail.ehlo()
            s_mail.login("subham.thakurela@gmail.com", "milslaixmobfcmpa")
            time.sleep(5)
            s_mail.sendmail(frm, all_add, text)
            status = True
            print("Email has been sent")
            '''logger.logg(debug_msg='None.',
                        info_msg='Mail has been sent',
                        warning_msg="None",
                        error_msg='Module = ' + "mailer.py",
                        critical_msg="None")'''
        except Exception as e:
            pass
            """logger.logg(debug_msg='Error while sending mail.',
                        info_msg='Mail could not be sent',
                        warning_msg='Error in sending mail',
                        error_msg='Module = ' + "mailer.py",
                        critical_msg=str(e))"""

        return status

    @staticmethod
    def validate_email(input_email):
        reg = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if re.fullmatch(reg, input_email):
            return True
        else:
            return False

    @staticmethod
    def send_success_noti(emails, dt_start, insertfile):
        raw_body = '''
            <body style="font-family:arial;">
                          Dear <span>friends</span>,<br><br>

                        <table style="text-align:left;width:100%;font-family:arial">
                             <tr>
                                <td style="padding-bottom:10px;">{head_message}</td>
                             </tr>
            				 <tr>
                                <td style="padding-bottom:10px;">Status: {status}</td>
                             </tr>
                             <tr>
                                <td style="padding-bottom:10px;">inserted_file: {insertfile}</td>
                             </tr>
            				<tr>
                            <td>Start Date/Time : {dt}</td>
                         </tr>
                         <tr>
                            <td>End Date/Time : {dtt}</td>
                         </tr>

                        </table>
                            <br><br><br><br><br><br><br>
            				Regards,
                            <br><span style="color:#0073A5"> Employee Ms</span>
                            <br><span style="color:#0073A5">(Employee Ms-Platform)</span>
                    </html>
            '''
        now = datetime.datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        # head_message = "Xignite {type} process has been started."
        head_message = "Execution successfully Completed"
        status = "Completed"
        to = emails
        cc = ConstantService.cc_mail_id()
        subject = " Employee Ms Notification - Success"
        head_message.format(type="Quarterly")
        body = raw_body.format(head_message=head_message, status=status, insertfile=insertfile,
                               dt=dt_start, dtt=dt_string)
        sent_mail = MailUtilities.sendHtmlMail(to, cc, subject, body)
        if sent_mail is True:
            return "Email has been sent"
