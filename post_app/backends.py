# post_app/email_backends.py
import smtplib
import ssl
import certifi
from django.core.mail.backends.smtp import EmailBackend as DjangoEmailBackend


class CustomEmailBackend(DjangoEmailBackend):
    def open(self):
        if self.connection:
            return False
        try:
            # 创建SMTP连接
            self.connection = smtplib.SMTP(self.host, self.port, timeout=self.timeout)
            self.connection.ehlo()

            if self.use_tls:
                # 使用certifi提供的证书包创建SSL上下文
                context = ssl.create_default_context(cafile=certifi.where())
                # 如果还是有问题，可以降低安全级别
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE

                self.connection.starttls(context=context)
                self.connection.ehlo()

            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except Exception as e:
            print(f"邮件连接失败: {e}")
            if not self.fail_silently:
                raise
            return False