#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy import signal
# from astropy.stats import LombScargle
from astropy.timeseries import LombScargle
import numpy as np
import math


plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


# 信息熵
def IFMT_En(RRI):
    x = list(set(RRI))
    x.sort()
    y = [0]*len(x)
    for rr in RRI:
        y[x.index(rr)] += 1
    y1 = [round(i/sum(y), 5) for i in y]
    xns = round(sum([(-p)*np.log2(p) for p in y1]), 2)
    return xns

# 样本熵：
def SampEn(RRI, m=2, r=0.15):
    RRI = np.array(RRI)
    d = r*RRI.std()
    def _maxdist(x_i, x_j):
        return max([abs(ua - va) for ua, va in zip(x_i, x_j)])
    def _phi(m):
        x = [[RRI[j] for j in range(i, i + m - 1 + 1)] for i in range(N - m + 1)]
        B = [(len([1 for x_j in x if _maxdist(x_i, x_j) <= d]) - 1.0) / (N - m) for x_i in x]
        return (N - m + 1.0)**(-1) * sum(B)
    N = len(RRI)
    try:
        SE = round(-np.log(_phi(m+1) / _phi(m)), 2)
    except:
        SE = 0
    return SE

# 基本尺度熵
def Fundamental_scale_entropy(RRI, m=4, a=0.1):
    RRI = np.array(RRI)
    N = len(RRI)
    Xi = np.array([[list(RRI)*2][0][i:i+m] for i in range(N-m+1)])
    SX = []
    for i in range(len(Xi)):
        X = Xi[i]
        BS = round(np.sqrt(sum([(RRI[i]-RRI[i-1])**2 for i in range(1, len(RRI))])/(m-1)), 2)
        mn = round(RRI.mean(), 2)
        zhi = []
        for k in range(m):
            Xk = X[k]
            if Xk > mn+a*BS:
                s = 1
            elif Xk > mn:
                s = 0
            elif Xk > mn-a*BS:
                s = 2
            else:
                s = 3
            zhi.append(s)
        S = [int('1'+'0'*(i-1)) for i in range(1, m+1)]
        S.reverse()
        SXi = sum(np.array(S)*np.array(zhi))
        SX.append(SXi)
    x = list(set(SX))
    x.sort()
    H = round(-sum([p*np.log2(p) for p in [round(SX.count(i)/(N-m+1), 2) for i in x]]), 2)
    return H

# Lorenz散点图统计参数
def Lorenz(RRI):
    dic = {}
    x = RRI[0:-1]
    y = RRI[1:]
    SD1 = round(np.array([y[i]-x[i] for i in range(len(x))]).std(), 5)/np.sqrt(2)
    SD2 = round(np.array([x[i]+y[i] for i in range(len(x))]).std(), 5)/np.sqrt(2)
    dic['SD1'] = round(SD1, 2)
    dic['SD2'] = round(SD2, 2)
    return dic

# 时域分析（The time domain analysis）
def HRV1(RRI):
    HRV = {}
    N = len(RRI)
    HRV['MAX'] = max(RRI)
    HRV['MIN'] = min(RRI)
    mn = round(np.array(RRI).mean(), 2)
    HRV['MEAN'] = mn
    RRS = [abs(RRI[i] - RRI[i-1]) for i in range(1,N)]
    SDNN = round(np.sqrt(sum([(rr-mn)**2 for rr in RRI])/len(RRI)), 2)
    if np.isnan(SDNN):
        SDNN = 0
    HRV['SDNN'] = SDNN
    HRV['RMSSD'] = round(np.sqrt(np.sum([rrs ** 2 for rrs in RRS]).sum() / (N - 1)), 2)
    HRV['SDSD'] = round(np.sqrt(np.array([(RRSi - np.mean(RRS)) ** 2 for RRSi in RRS]).sum() / (N - 1)), 2)
    NN50 = len([rrs for rrs in RRS if rrs > 50])
    HRV['NN50'] = NN50
    HRV['PNN50'] = round(NN50 / N * 100, 2)
    # HRV['SE'] = round(SampEn(RR), 3)
    return HRV

# 频域分析指标（Frequency domain analysis）
def Fda(RRI):
    dic = {}
    a, b = plt.psd(RRI)
    x1 = b
    y1 = [round(math.log(i, 2)*3, 5) for i in a]
    lis_LF = []
    lis_HF = []
    lis_TP = []
    lis_VLF = []
    for i in range(len(x1)):
        if 0.4>=x1[i]>0.15:
            lis_HF.append(y1[i])
        elif 0.15>=x1[i]>0.04:
            lis_LF.append(y1[i])
        elif 0.04> x1[i]:
            lis_VLF.append(y1[i])
        if 0.4>=x1[i]>0.0033:
            lis_TP.append(y1[i])
    LF = round(sum(lis_LF), 2)
    dic['LF'] = LF
    HF = round(sum(lis_HF), 2)
    dic['HF'] = HF
    dic['TP'] = round(sum(lis_TP), 2)
    dic['VLF'] = round(sum(lis_VLF), 2)
    dic['LF_norm'] = round(LF/(LF+HF)*100, 2)
    dic['HF_norm'] = round(HF/(LF+HF)*100, 2)
    dic['LF_HF'] = round(LF/HF, 2)
    return dic

# PSD分析

# PSD分析

# 不同频段的命名元组
VlfBand = (0.0033, 0.04)
LfBand = (0.04, 0.15)
HfBand = (0.15, 0.40)


# 创建时间信息
def _create_time_info(RRI):
    # 转换为秒
    RRI_tmstp = np.cumsum(RRI) / 1000

    # 强制从0开始
    return RRI_tmstp - RRI_tmstp[0]

# 指定采样频率并创建插值时间
def _create_interpolation_time(RRI, sampling_frequency=7):
    time_rri = _create_time_info(RRI)
    # 为插值创建时间戳
    rri_interpolation_tmstp = np.arange(0, time_rri[-1], 1 / float(sampling_frequency))
    return rri_interpolation_tmstp

# 从RR间期数据中获取频率和功率谱密度值
def _get_freq_psd_from_nn_intervals(RRI, method="welch", sampling_frequency=7, interpolation_method="linear", vlf_band=VlfBand, hf_band=HfBand):
    timestamps = _create_time_info(RRI)

    if method == "welch":
        # ---------- 插值的信号 ---------- #
        funct = interpolate.interp1d(x=timestamps, y=RRI, kind=interpolation_method)

        timestamps_interpolation = _create_interpolation_time(RRI, sampling_frequency)
        nni_interpolation = funct(timestamps_interpolation)

        # ---------- 去除直流分量 ---------- #
        nni_normalized = nni_interpolation - np.mean(nni_interpolation)

        #  ----------  计算功率谱密度  ---------- #
        freq, psd = signal.welch(x=nni_normalized, fs=sampling_frequency, window='hann',
                                 nfft=4096)

    elif method == "lomb":
        freq, psd = LombScargle(timestamps, RRI,
                                normalization='psd').autopower(minimum_frequency=vlf_band[0],
                                                               maximum_frequency=hf_band[1])
    else:
        raise ValueError("Not a valid method. Choose between 'lomb' and 'welch'")

    return (freq, psd)

# 从功率谱密度中获取特征
def _get_features_from_psd(freq, psd, vlf_band=VlfBand, lf_band=LfBand, hf_band=HfBand):
    # 期望频带间指数的计算
    vlf_indexes = np.logical_and(freq >= vlf_band[0], freq < vlf_band[1])
    lf_indexes = np.logical_and(freq >= lf_band[0], freq < lf_band[1])
    hf_indexes = np.logical_and(freq >= hf_band[0], freq < hf_band[1])

    PeakVLF = round(freq[vlf_indexes][list(psd[vlf_indexes]).index(max(psd[vlf_indexes]))], 2)
    PeakLF = round(freq[lf_indexes][list(psd[lf_indexes]).index(max(psd[lf_indexes]))], 2)
    PeakHF = round(freq[hf_indexes][list(psd[vlf_indexes]).index(max(psd[vlf_indexes]))], 2)

    # 标准

    # 利用复合梯形规则进行积分
    vlf = np.trapz(y=psd[vlf_indexes], x=freq[vlf_indexes])
    lf = np.trapz(y=psd[lf_indexes], x=freq[lf_indexes])
    hf = np.trapz(y=psd[hf_indexes], x=freq[hf_indexes])

    # 总功率:功能经常用于“长期记录”分析
    tp = vlf + lf + hf

    LF_HF = lf / hf
    lfnu = (lf / (lf + hf)) * 100
    hfnu = (hf / (lf + hf)) * 100

    dic = {}
    dic['VLF'] = {'Peak': PeakVLF, 'Power1': round(vlf, 2), 'Power2': round(vlf / tp * 100, 2),
                  'LF_HF': round(LF_HF, 2)}
    dic['LF'] = {'Peak': PeakLF, 'Power1': round(lf, 2), 'Power2': round(lf / tp * 100, 2), 'Power3': round(lfnu, 2)}
    dic['HF'] = {'Peak': PeakHF, 'Power1': round(hf, 2), 'Power2': round(hf / tp * 100, 2), 'Power3': round(hfnu, 2)}

    return dic

# 获取频域特征
def get_frequency_domain_features(RRI, method="welch", sampling_frequency=7, interpolation_method="linear", vlf_band=VlfBand, lf_band=LfBand, hf_band=HfBand):
    # ----------  计算频率与功率的信号  ---------- #
    freq, psd = _get_freq_psd_from_nn_intervals(RRI=RRI, method=method,
                                                sampling_frequency=sampling_frequency,
                                                interpolation_method=interpolation_method,
                                                vlf_band=vlf_band, hf_band=hf_band)

    # ---------- 特性计算 ---------- #
    freqency_domain_features = _get_features_from_psd(freq=freq, psd=psd,
                                                      vlf_band=vlf_band,
                                                      lf_band=lf_band,
                                                      hf_band=hf_band)

    return freqency_domain_features

# 时域分析
def TimeDomain(RRI):
    dic = {}
    N = len(RRI)
    dic['MAX'] = max(RRI)
    dic['MIN'] = min(RRI)
    mn = round(np.array(RRI).mean(), 2)
    dic['MEAN'] = mn
    RRS = [abs(RRI[i] - RRI[i-1]) for i in range(1,N)]
    SDNN = round(np.sqrt(sum([(rr-mn)**2 for rr in RRI])/len(RRI)), 2)
    if np.isnan(SDNN):
        SDNN = 0
    dic['SDNN'] = SDNN
    dic['RMSSD'] = round(np.sqrt(np.sum([rrs ** 2 for rrs in RRS]).sum() / (N - 1)), 2)
    dic['SDSD'] = round(np.sqrt(np.array([(RRSi - np.mean(RRS)) ** 2 for RRSi in RRS]).sum() / (N - 1)), 2)
    NN50 = len([rrs for rrs in RRS if rrs > 50])
    dic['NN50'] = NN50
    dic['PNN50'] = round(NN50 / N * 100, 2)
    return dic
# 频域分析
def FreqDomain(RRI):
    dic = {}
    dic['WelckPSD'] = get_frequency_domain_features(RRI, method='welch')
    #dic['BurgPSD'] = BurgPSD(RR)
    dic['LombScarglePSD'] = get_frequency_domain_features(RRI, method='lomb')
    return dic
# 散点图分析
def Poincare(RRI):
    dic = {}
    x = RRI[0:-1]
    y = RRI[1:]
    SD1 = round(np.array([y[i]-x[i] for i in range(len(x))]).std(), 5)/np.sqrt(2)
    SD2 = round(np.array([x[i]+y[i] for i in range(len(x))]).std(), 5)/np.sqrt(2)
    dic['SD1'] = round(SD1, 2)
    dic['SD2'] = round(SD2, 2)
    return dic
# 非线性分析
def Nonlinear(RRI):
    dic = {}
    dic['IE'] = IFMT_En(RRI)
    dic['SE'] = SampEn(RRI, m=2, r=0.15)
    dic['BE'] = Fundamental_scale_entropy(RRI, m=4, a=0.1)
    return dic
# 时间频域分析
def TimeFreq(RRI):
    dic = {}

    #Welck = WelckPSD(RR)
    #Burg = BurgPSD(RR)
    #LombScargle = LombScarglePSD(RR)
    #Welck['LF']['LF_HF'] = 0.682
    #Burg['LF']['LF_HF'] = 0.500
    #LombScargle['LF']['LF_HF'] = 3.770

    #dic['WelckPSD'] = Welck
    #dic['BurgPSD'] = Burg
    #dic['LombScarglePSD'] = LombScargle
    return dic

def GetHRV(RRI, Domain = None):
    dic = {}
    dic['TimeDomain'] = TimeDomain(RRI)          # 完成
    dic['FreqDomain'] = FreqDomain(RRI)          # 完成
    dic['Poincare'] = Poincare(RRI)              # 完成
    dic['Nonlinear'] = Nonlinear(RRI)            # 完成
    #dic['TimeFreq'] = TimeFreq(RR)

    if Domain==None:
        return dic
    elif Domain == 'TimeDomain':
        return dic['TimeDomain']
    elif Domain == 'FreqDomain':
        return dic['FreqDomain']
    elif Domain == 'Poincare':
        return dic['Poincare']
    elif Domain == 'Nonlinear':
        return dic['Nonlinear']
    else:
        return {'暂无该领域的分析方法。'}
