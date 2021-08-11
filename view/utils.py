import smtplib
from email.mime.text import MIMEText


def send_mail(user_email, temp_password):
    print(user_email)
    sendEmail = "ggulgguk.official@gmail.com"
    recvEmail = user_email
    password = "123ggulgguk123"

    smtpName = "smtp.gmail.com" #smtp 서버 주소
    smtpPort = 587 #smtp 포트 번호


    text = temp_password
    msg = MIMEText(text) #MIMEText(text , _charset = "utf8")

    msg['Subject'] = "[꿀꺽] 임시 비밀번호 안내"
    msg['From'] = sendEmail
    msg['To'] = recvEmail
    print(msg.as_string())

    s=smtplib.SMTP( smtpName , smtpPort ) #메일 서버 연결
    s.starttls() #TLS 보안 처리
    s.login( sendEmail , password ) #로그인
    s.sendmail( sendEmail, recvEmail, msg.as_string() ) #메일 전송, 문자열로 변환해야 합니다.
    s.close() #smtp 서버 연결을 종료합니다.