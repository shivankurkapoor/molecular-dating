import os
import MySQLdb


def DB_connect():
    db = MySQLdb.connect(host='mool', user='miseq', passwd='norris', db='dating')
    return db


def get_list(tablename, conditions='', columns=''):
    if columns == '':
        line = "SELECT * "
    else:
        line = "SELECT " + columns + " "
    line = line + "from " + tablename
    if conditions != '':
        line = line + " where " + conditions

    db = DB_connect()
    c = db.cursor()
    c.execute(line)
    row = c.fetchone()
    result = []
    while row != None:
        result.append(row)
        row = c.fetchone()

    c.close()
    db.close()
    return result


def add_record(tablename, values, columns=''):
    line = "INSERT INTO " + tablename
    if columns != '':
        line = line + " (" + columns + ") "
    line = line + "VALUES (%s)"

    db = DB_connect()
    c = db.cursor()
    c.execute(line % values)

    db.commit()
    c.close()
    db.close()
    return


def update_record(tablename, values, conditions=''):
    line = "UPDATE " + tablename
    line = line + " SET " + values
    if conditions != '':
        line = line + " WHERE " + conditions

    db = DB_connect()
    c = db.cursor()
    c.execute(line)

    db.commit()
    c.close()
    db.close()
    return


def submit_job_into_queue(name, requestid, pset, starttime=''):
    if starttime == '':
        add_record('queue', "'%s','%s','%s'" % (name, requestid, pset) + ",0",
                   "queue_type,requestID,parameter,processed")
    else:
        add_record('queue', "'%s','%s','%s','%s'" % (name, requestid, pset, starttime) + ",0",
                   "queue_type,requestID,parameter,assign_time,processed")
    current_dir = os.getcwd()
    os.chdir('/home/spark/queue_operation')
    if name == 'single':
        os.system("/usr/bin/qsub -e log -o log script/qsingle")
    if name == 'pipeline':
        os.system("/usr/bin/qsub -e log -o log script/qpipe")
    if name == 'taxonomy':
        os.system("/usr/bin/qsub -e log -o log script/qtaxo")
    if name == 'graph':
        os.system("/usr/bin/qsub -e log -o log script/qgraph")
    if name == 'upload':
        os.system("/usr/bin/qsub -e log -o log script/qup")
    os.chdir(current_dir)
    return


def check_if_all_samples_finished(requestID, stage='taxonomy', option=''):
    check_list = get_list("queue", "sid=%s and %s!=%d" % (requestID, stage, 2), "rid")
    if len(check_list) >= 1:
        return False
    if option == 'update_status':
        update_record("simulation", stage + '=2', "sid=%s" % requestID)
    return True
