import meteva
import numpy as np
import datetime
import copy
import matplotlib.pyplot as plt
import time
import pandas as pd
import math
import matplotlib as mpl
import os

para_example= {
    "day_num":7,
    "end_time":datetime.datetime.now(),
    "station_file":meteva.base.station_国家站,
    "interp": meteva.base.interp_gs_nearest,
    "defalut_value":999999,
    "hdf_file_name":"week.h5",
    "ob_data":{
        "hdf_dir":r"O:\data\hdf\SURFACE\QC_BY_FSOL\TMP_ALL_STATION",
        "dir_ob": r"O:\data\sta\SURFACE\QC_BY_FSOL\TMP_ALL_STATION\YYYYMMDD\YYYYMMDDHH0000.000",
        "read_method":meteva.base.io.read_stadata_from_gdsfile,
        "read_para":{},
        "operation":None,
        "operation_para":{}
    },
    "fo_data":{
        "SCMOC":{
            "hdf_dir": r"O:\data\hdf\NWFD_SCMOC\TMP\2M_ABOVE_GROUND",
            "dir_fo": r"O:\data\grid\NWFD_SCMOC\TMP\2M_ABOVE_GROUND\YYYYMMDD\YYMMDDHH.TTT.nc",
            "read_method": meteva.base.io.read_griddata_from_nc,
            "read_para": {},
            "operation": None,
            "operation_para_dict":{}
        },
        "GRAPES": {
            "hdf_dir": r"O:\data\hdf\GRAPES_GFS\TMP\2M_ABOVE_GROUND",
            "dir_fo": r"O:\data\grid\GRAPES_GFS\TMP\2M_ABOVE_GROUND\YYYYMMDD\YYMMDDHH.TTT.nc",
            "read_method": meteva.base.io.read_griddata_from_nc,
            "read_para": {},
            "operation": None,
            "operation_para_dict": {}
        },
        "ECMWF":{
            "hdf_dir": r"O:\data\hdf\ECMWF_HR\TMP_2M",
            "dir_fo": r"O:\data\grid\ECMWF_HR\TMP_2M\YYYYMMDD\YYMMDDHH.TTT.nc",
            "read_method": meteva.base.io.read_griddata_from_nc,
            "read_para": {},
            "operation": None,
            "operation_para_dict":{}
        }
    },
    "output_dir":r"O:\data\hdf\combined\temp_2m"
}


def prepare_dataset(para):
    '''

    :param para: 根据配置参数从站点和网格数据中读取数据插值到指定站表上，在存储成hdf格式文件，然后从hdf格式文件中读取相应的文件合并成检验要的数据集合文件
    :return:
    '''

    # 全局参数预处理，站点列表的读取
    station = meteva.base.read_station(para["station_file"])
    station.iloc[:,-1] = para["defalut_value"]
    para["station"] = station

    #全局参数预处理，起止日期的处理
    day_num = para["day_num"]
    end_time = para["end_time"]
    if end_time is None:
        end_time = datetime.datetime.now()
    end_date = datetime.datetime(end_time.year, end_time.month, end_time.day, 0, 0)
    start_date = end_date - datetime.timedelta(days=day_num)
    end_date = end_date + datetime.timedelta(days=1)
    para["start_date"] = start_date
    para["end_date"] = end_date


    hdf_path = para["ob_data"]["hdf_dir"] + "/" + para["hdf_file_name"]
    hdf_file_list = [hdf_path]
    para["ob_data"]["hdf_path"] = hdf_path
    creat_ob_dataset(para)
    models = para["fo_data"].keys()
    for model in models:
        hdf_path = para["fo_data"][model]["hdf_dir"] + "/" + para["hdf_file_name"]
        para["fo_data"][model]["hdf_path"] = hdf_path
        hdf_file_list.append(hdf_path)
        creat_fo_dataset(model,para)

    output_file = para["output_dir"] + "/" + para["hdf_file_name"]
    meteva.base.path_tools.creat_path(output_file)
    combine_ob_fos_dataset(output_file,hdf_file_list)


def creat_fo_dataset(model,para):

    station = para["station"]
    interp = para["interp"]
    end_date = para["end_date"]
    start_date = para["start_date"]
    day_num = para["day_num"] + 1
    para_model = para["fo_data"][model]
    hdf_path = para_model["hdf_path"]
    dir_fo  =para_model["dir_fo"]
    read_method = para_model["read_method"]
    read_para =para_model["read_para"]
    if read_para is None:
        read_para = {}
    operation = para_model["operation"]
    operation_para =para_model["operation_para"]
    if operation_para is None:
        operation_para = {}
    move_fo_time = para_model["move_fo_time"]

    data0 = None
    if os.path.exists(hdf_path):
        data0 = pd.read_hdf(hdf_path, "df")

    hours = None
    if para_model["hour"] is not None:
        hours = np.arange(para_model["hour"][0],para_model["hour"][1]+1,para_model["hour"][2]).tolist()


    dtimes = None
    if para_model["dtime"] is not None:
        dtimes = np.arange(para_model["dtime"][0],para_model["dtime"][1]+1,para_model["dtime"][2]).tolist()

    sta_list = [] #用于收集所有数据
    exist_dtimes = {}
    if data0 is None:
        if hours is None:
            hours = np.arange(0, 24, 1).tolist()
        if dtimes is None:
            dtimes = np.arange(0, 721, 1).tolist()
    else:
        data_left = meteva.base.sele_by_para(data0, time_range=[start_date, end_date])
        meteva.base.set_stadata_names(data_left,model)
        sta_list.append(data_left)
        id0 = station["id"].values[0]
        data_id0 = meteva.base.sele_by_para(data0, id=id0)
        print(data_id0)
        times = data_id0.loc[:, "time"].values.tolist()
        times = list(set(times))
        times.sort()
        exist_time_list = []
        for i in range(len(times)):
            time1 = meteva.base.time_tools.all_type_time_to_datetime(times[i])
            exist_time_list.append(time1)
            data_id0_time0 = meteva.base.sele_by_para(data_id0, time=time1)
            ehours = data_id0_time0.loc[:, "dtime"].values.tolist()
            exist_dtimes[time1] = ehours

        if hours is None:
            hours = []
            for time1 in exist_time_list:
                hours.append(time1.hour)
            hours = list(set(hours))
            hours.sort()
        if dtimes is None:
            dtimes = data_id0.loc[:, "dtime"].values.tolist()
            dtimes = list(set(dtimes))
            dtimes.sort()

    print(exist_dtimes)
    for dd in range(day_num):
        for hh in range(len(hours)):
            hour = hours[hh]
            time1 = end_date - datetime.timedelta(days=dd) + datetime.timedelta(hours=hour)
            for dt in dtimes:
                if time1 in exist_dtimes.keys():
                    exist_dtime = exist_dtimes[time1]
                    if dt in exist_dtime:
                        continue
                path = meteva.base.get_path(dir_fo, time1, dt)
                if os.path.exists(path):
                    try:
                        dat = read_method(path,**read_para)
                        if dat is not None:
                            if not isinstance(dat, pd.DataFrame):
                                dat = interp(dat, station)
                            meteva.base.set_stadata_coords(dat,time = time1,dtime = dt)
                            meteva.base.set_stadata_names(dat,model)
                            sta_list.append(dat)
                            print("success read data from " + path)
                        else:
                            print("fail read data from " + path)
                    except:
                        print("fail read data from " + path)
                else:
                    print(path +" does not exist")

    if(len(sta_list) == 0):
        print("there is not file data in " + dir_fo)
        return
    sta_all = pd.concat(sta_list, axis=0)
    if operation is not None:
        sta_all = operation(sta_all,**operation_para)
    if move_fo_time !=0:
        sta_all = meteva.base.move_fo_time(sta_all,move_fo_time)
    print(hdf_path)
    meteva.base.creat_path(hdf_path)
    sta_all.to_hdf(hdf_path, "df")

def creat_ob_dataset(para):
    station = para["station"]
    data_name ="ob"
    day_num = para["day_num"] + 1
    end_date = para["end_date"]
    start_date = para["start_date"]
    hdf_path = para["ob_data"]["hdf_path"]
    dir_ob =para["ob_data"]["dir_ob"]
    read_method = para["ob_data"]["read_method"]
    read_para = para["ob_data"]["read_para"]
    if read_para is None:
        read_para = {}
    reasonable_value = para["ob_data"]["reasonable_value"]
    operation = para["ob_data"]["operation"]
    operation_para = para["ob_data"]["operation_para"]
    if operation_para is None:
        operation_para = {}

    hours = None
    if para["ob_data"]["hour"] is not None:
        hours = np.arange(para["ob_data"]["hour"][0],para["ob_data"]["hour"][1]+1,para["ob_data"]["hour"][2]).tolist()

    exist_time_list = []
    sta_list = []
    data0 = None
    if os.path.exists(hdf_path):
        data0 = pd.read_hdf(hdf_path, "df")
    if data0 is None:
        if hours is None:
            hours = np.arange(0, 24, 1).tolist()
    else:
        data_left = meteva.base.sele_by_para(data0, time_range=[start_date, end_date])
        meteva.base.set_stadata_names(data_left, data_name)
        sta_list.append(data_left)
        id0 = station["id"].values[0]
        data_id0 = meteva.base.sele_by_para(data0, id=id0)
        times = data_id0.loc[:, "time"].values.tolist()
        times = list(set(times))
        times.sort()

        for i in range(len(times)):
            time1 = meteva.base.time_tools.all_type_time_to_datetime(times[i])
            exist_time_list.append(time1)
        if hours is None:
            hours = []
            for time1 in exist_time_list:
                hours.append(time1.hour)
            hours = list(set(hours))
            hours.sort()


    for dd in range(day_num):
        for hh in range(len(hours)):
            hour = hours[hh]
            time1 = end_date - datetime.timedelta(days=dd) + datetime.timedelta(hours=hour)
            if time1 in exist_time_list:
                continue
            path = meteva.base.get_path(dir_ob, time1)
            if os.path.exists(path):
                try:
                    dat = read_method(path,**read_para)
                    if dat is not None:
                        dat = meteva.base.fun.comp.put_stadata_on_station(dat,station)
                        if not isinstance(dat,pd.DataFrame):
                            interp = para["interp"]
                            dat = interp(dat,station)
                        if reasonable_value is not None:
                            dat = meteva.base.sele_by_para(dat,value=reasonable_value)
                        meteva.base.set_stadata_names(dat,data_name)
                        meteva.base.set_stadata_coords(dat,time = time1)
                        sta_list.append(dat)
                    else:
                        print("fail read data from " + path)
                except:
                    print("fail read data from " + path)
            else:
                print(path +  "does not exist")
    sta_all = pd.concat(sta_list, axis=0)
    if operation is not None:
        sta_all = operation(sta_all,**operation_para)
    meteva.base.creat_path(hdf_path)
    print(hdf_path)
    sta_all.to_hdf(hdf_path, "df")

def load_ob_fos_dataset(ob_fos_path_list,ob_fos_name_list = None,reset_level = True):
    sta_all_list = []
    level_ob =0
    for i in range(len(ob_fos_path_list)):
        sta_all = pd.read_hdf(ob_fos_path_list[i],"df")
        if ob_fos_name_list is not None:
            meteva.base.set_stadata_names(sta_all,[ob_fos_name_list[i]])
        if reset_level and i==0:
            level_ob = sta_all.iloc[0,0]
        if np.isnan(level_ob):
            level_ob = 0
            meteva.base.set_stadata_coords(sta_all, level=level_ob)
        else:
            if reset_level and i !=0:
                meteva.base.set_stadata_coords(sta_all,level = level_ob)
        sta_all_list.append(sta_all)
        print(sta_all)
    sta_all_merged = meteva.base.combine_on_obTime_id(sta_all_list[0],sta_all_list[1:])
    return sta_all_merged

def combine_ob_fos_dataset(output_path,ob_fos_path_list,ob_fos_name_list = None,reset_level = True):
    sta_all_merged = load_ob_fos_dataset(ob_fos_path_list, ob_fos_name_list=ob_fos_name_list,reset_level= reset_level)
    sta_all_merged.to_hdf(output_path, "df")
    print("success combined data to " + output_path)


