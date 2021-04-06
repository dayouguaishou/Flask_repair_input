from flask import Flask, jsonify, render_template, request
import SimplifyuseMySQL.SimplifyuseMySQL as mysql
import json
import time

app = Flask(__name__)#实例化app对象

@app.route("/repair_input_yq")
def test():
    return render_template("repair_input_yq.html")

@app.route('/repair_input')
def repair_input():
    user_name = ''
    user_projects = ''
    input_tm = ''
    if request.args.get('input_phone', 0, type=str) == '' or request.args.get('accident_place', 0, type=str) == '' or request.args.get('accident_reason', 0, type=str) == '' :
        stat = 1 
    else:
        SQL_phone = "SELECT user_name,projects FROM input_personnel WHERE phone = '{input_phone}'".format(input_phone = request.args.get('input_phone', 0, type=str))
        user_info = mysql.select_MYSQL(SQL_phone)
        if len(user_info) != 1:
            stat = 2
        else:
            user_name = mysql.select_datas_column(user_info,0)[0]
            user_projects = mysql.select_datas_column(user_info,1)[0]
            now = request.args.get('now', 0, type=float)
            input_tm = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now/1000))
            json_val_list = []
            json_name_list =['server_sitename','accident_place','accident_reason','treatment_method','start_tm','end_tm','stop_tms','stop_area']
            for i in range(len(json_name_list)):
                json_val_list.append(request.args.get(json_name_list[i], 0, type=str))
            json_val_str = "'" + user_projects +"','" + request.args.get('input_phone', 0, type=str) +"','" + input_tm + "','" + "','".join(json_val_list) + "'"
            json_name_str = 'projects,input_phone,input_tm,' + ','.join(json_name_list)
            SQL_input = "INSERT INTO input_table ({json_name_str}) VALUES ({json_val_str})".format(json_name_str = json_name_str , json_val_str = json_val_str)
            mysql.execute_to_mysql(SQL_input)
            stat = 0
    return jsonify(result = [stat,user_projects,user_name,input_tm])


if __name__ == '__main__':
   app.run(host = "0.0.0.0", port = 5050,threaded=True)



