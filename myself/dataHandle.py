import pymysql

# uid, name, lng, lat, address, telephone, keyword


class DataHandle:
    def __init__(self):
        # 将成数据保存到MariaDB
        self.conn = pymysql.connect(
            host="193.112.42.136", port=3306,
            user="dbadministrator", password="ljw591992561",
            database="baidumap", charset="utf8mb4"
        )
        self.cursor = self.conn.cursor()

    def save_data(self, datas):
        try:
            for a in datas:
                sql = "INSERT INTO baidumap.address(uid, aname, lng, lat, address, telephone, keyword) VALUES('%s','%s',%s,%s,'%s','%s','%s');" % (
                    a[0], a[1], str(a[2]), str(a[3]), a[4], a[5], a[6])
                self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            with open("./run.log", mode="a") as file:
                file.write(e+"\n")


if __name__ == '__main__':
    # 初始化连接
    test = DataHandle()

    # 测试 MariaDB
    test.cursor.execute("SELECT * FROM baidumap.usertable;")
    ret = test.cursor.fetchall()
    print(ret)
