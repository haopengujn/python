#-*- coding: utf-8 -*-
#Filename add_device_data.py

import os
import re
import shutil
import MySQLdb

baseDir="/root/jucheng"
apacheDir="/usr/local/apache/htdocs/images/"
categoryDirs=os.listdir(baseDir)
imageHref="http://115.28.210.97/"

def addCategory(category, cursor):
    ifExistSql="select ID from DEVICE_CATEGORY where NAME='%s'"
    cursor.execute(ifExistSql, category)
    rows=cursor.fetchall()
    if rows and rows[0]:
        return rows[0][0]
    addCategorySql="insert into DEVICE_CATEGORY(NAME) values('%s')"
    cursor.execute(addCategorySql, category)
    categoryId=cursor.lastrowid
    return categoryId

def addDevice(device, catgoryId, categoryDir, cursor):
    deviceDir=categoryDir+"/"+device
    files=os.listdir(deviceDir)
    desc=""
    picUrl=""
    for fileName in files:
        fileDir=deviceDir+"/"+fileName
        if "txt" in fileName:
            try:
                f=open(fileDir)
                desc=f.read()
                desc=re.compile("\\n|\\r|(\\r\\n)|(\u0085)|(\u2028)|(\u2029)",re.IGNORECASE).sub("<br/>", desc)
            finally:
                f.close()
        else:
            apachePath=apacheDir+fileName
            if not os.path .isfile(apachePath):
                os.mknod(apachePath)
            shutil.copyfile(fileDir, apachePath)
            picUrl=imageHref+fileName
    addDeviceSql="insert into DEVICE() values(DEVICE_CATEGORY_ID, PIC, NAME, IS_HOT, DESCRIPTION, CREATED_DATE) values(%s, %s, %s, %s, %s, now())"
    cursor.execute(addDeviceSql, (catgoryId, picUrl, device, 1, desc))
    print "add device name :%s"%device


def main():
    conn=MySQLdb.connect(host = "10.144.151.155", user = "root", passwd = "helloworld", db = "jucheng", charset="utf8")
    try:
        cursor=conn.cursor()
        for category in categoryDirs:
            catgoryId=addCategory(category, cursor)
            categoryDir=baseDir+"/"+category
            deviceDirs=os.listdir(categoryDir)
            for device in deviceDirs:
                addDevice(device, catgoryId, categoryDir, cursor)
        conn.commit()
        cursor.close()
    except Exception, ex:
        raise ex
    finally:
        conn.close()


if __name__=='__main__':
    main()