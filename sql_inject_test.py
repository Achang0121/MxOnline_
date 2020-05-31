import MySQLdb

username = "' OR 1=1 #"
password = 'pbkdf2_sha256$150000$HFCwyGGv8dNv$hAAxveNLJSKUKWH52/XkxYFoeu9SdvwdDsLS4iBx+cU='

conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='mxonline')
cursor = conn.cursor()

sql = "select * from users_userprofile where username='{}' and password='{}'".format(username, password)
print(sql)
# cursor.execute(sql)
# for row in cursor.fetchall():
#     print(row)
