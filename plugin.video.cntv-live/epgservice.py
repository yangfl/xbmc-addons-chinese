# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon

import datetime
import re
import os
import traceback
import urllib2

try:
	import simplejson as jsonimpl
except ImportError:
	import json as jsonimpl


addon = xbmcaddon.Addon(id="plugin.video.cntv-live")
addon_path = xbmc.translatePath(addon.getAddonInfo("path"))


ZERO = datetime.timedelta(0)


class FixedOffset(datetime.tzinfo):
	"""Fixed offset in minutes east from UTC."""

	def __init__(self, offset, name):
		self.__offset = datetime.timedelta(minutes = offset)
		self.__name = name

	def utcoffset(self, dt):
		return self.__offset

	def tzname(self, dt):
		return self.__name

	def dst(self, dt):
		return ZERO


CST = FixedOffset(8 * 60, 'CST')


def updateChannel(fHandle, channelID, channelName):
	try:
		print("Updating channel " + channelID)

		dateInChina = datetime.datetime.now(CST)

		#Get data
		request = urllib2.Request("http://api.cntv.cn/epg/epginfo?serviceId=shiyi&d=" + dateInChina.strftime("%Y%m%d") + "&c=" + channelID)
		request.add_header("Referer", "http://tv.cntv.cn/epg")
		resp = urllib2.urlopen(request)
		data = resp.read().decode("utf-8")

		#Process data
		jsondata = jsonimpl.loads(data)
		programmes = jsondata[channelID]['program']

		#Write channel data
		fHandle.write('<channel id="{0}">\n'.format(channelID))
		fHandle.write('<display-name lang="cn">{0}</display-name>\n'.format(channelName))
		fHandle.write('</channel>\n'.format(channelID))

		#Write programme data
		for entry in programmes:
			#Convert to local time zone
			startTime = datetime.datetime.fromtimestamp(entry['st'], CST)
			stopTime = datetime.datetime.fromtimestamp(entry['et'], CST)

			fHandle.write('<programme start="{0}" stop="{1}" channel="{2}">\n'.format(formatDate(startTime), formatDate(stopTime), channelID))
			fHandle.write('<title lang="cn">{0}</title>\n'.format(entry['t'].encode("utf-8")))
			fHandle.write('</programme>\n')
	except Exception:
		print(traceback.format_exc())


def formatDate(obj):
	return obj.strftime("%Y%m%d%H%M00")


def doUpdate():
	print("Updating EPG")

	try:
		fHandle = open(xbmc.translatePath("special://temp/epg2.xml"), "w")
		fHandle.write('<?xml version="1.0" encoding="utf-8" ?>\n')
		fHandle.write('<tv>\n')

		if addon.getSettingBool("epgYangshi"):
			updateChannel(fHandle, "cctv1", "CCTV-1 综合")
			updateChannel(fHandle, "cctv2", "CCTV-2 财经")
			updateChannel(fHandle, "cctv3", "CCTV-3 综艺")
			updateChannel(fHandle, "cctv4", "CCTV-4 (亚洲)")
			updateChannel(fHandle, "cctveurope", "CCTV-4 (欧洲)")
			updateChannel(fHandle, "cctvamerica", "CCTV-4 (美洲)")
			updateChannel(fHandle, "cctv5", "CCTV-5 体育")
			updateChannel(fHandle, "cctv6", "CCTV-6 电影")
			updateChannel(fHandle, "cctv7", "CCTV-7 军事 农业")
			updateChannel(fHandle, "cctv8", "CCTV-8 电视剧")
			updateChannel(fHandle, "cctvjilu", "CCTV-9 纪录")
			updateChannel(fHandle, "cctvdoc", "CCTV-9 纪录(英)")
			updateChannel(fHandle, "cctv10", "CCTV-10 科教")
			updateChannel(fHandle, "cctv11", "CCTV-11 戏曲")
			updateChannel(fHandle, "cctv12", "CCTV-12 社会与法")
			updateChannel(fHandle, "cctv13", "CCTV-13 新闻")
			updateChannel(fHandle, "cctvchild", "CCTV-14 少儿")
			updateChannel(fHandle, "cctv15", "CCTV-15 音乐")
			updateChannel(fHandle, "cctv9", "CCTV-NEWS")
			updateChannel(fHandle, "cctv5plus", "CCTV体育赛事")

		if addon.getSettingBool("epgWeishi"):
			updateChannel(fHandle, "anhui", "安徽卫视")
			updateChannel(fHandle, "btv1", "北京卫视")
			updateChannel(fHandle, "bingtuan", "兵团卫视")
			updateChannel(fHandle, "chongqing", "重庆卫视")
			updateChannel(fHandle, "dongfang", "东方卫视")
			updateChannel(fHandle, "dongnan", "东南卫视")
			updateChannel(fHandle, "gansu", "甘肃卫视")
			updateChannel(fHandle, "guangdong", "广东卫视")
			updateChannel(fHandle, "guangxi", "广西卫视")
			updateChannel(fHandle, "guizhou", "贵州卫视")
			updateChannel(fHandle, "hebei", "河北卫视")
			updateChannel(fHandle, "henan", "河南卫视")
			updateChannel(fHandle, "heilongjiang", "黑龙江卫视")
			updateChannel(fHandle, "hubei", "湖北卫视")
			updateChannel(fHandle, "jilin", "吉林卫视")
			updateChannel(fHandle, "jiangxi", "江西卫视")
			updateChannel(fHandle, "kangba", "康巴卫视")
			updateChannel(fHandle, "liaoning", "辽宁卫视")
			updateChannel(fHandle, "travel", "旅游卫视")
			updateChannel(fHandle, "neimenggu", "内蒙古卫视")
			updateChannel(fHandle, "ningxia", "宁夏卫视")
			updateChannel(fHandle, "qinghai", "青海卫视")
			updateChannel(fHandle, "shandong", "山东卫视")
			updateChannel(fHandle, "sdetv", "山东教育台")
			updateChannel(fHandle, "shenzhen", "深圳卫视")
			updateChannel(fHandle, "shan1xi", "山西卫视")
			updateChannel(fHandle, "shan3xi", "陕西卫视")
			updateChannel(fHandle, "shenzhen", "深圳卫视")
			updateChannel(fHandle, "sichuan", "四川卫视")
			updateChannel(fHandle, "tianjin", "天津卫视")
			updateChannel(fHandle, "xizang", "西藏卫视")
			updateChannel(fHandle, "xiamen", "厦门卫视")
			updateChannel(fHandle, "xianggangweishi", "香港卫视")
			updateChannel(fHandle, "xinjiang", "新疆卫视")
			updateChannel(fHandle, "yanbian", "延边卫视")
			updateChannel(fHandle, "yunnan", "云南卫视")
			updateChannel(fHandle, "zhejiang", "浙江卫视")

		fHandle.write('</tv>\n')
		fHandle.close()

		os.rename(xbmc.translatePath("special://temp/epg2.xml"), xbmc.translatePath("special://temp/epg.xml")) #Good programming practices, yo!
	except Exception:
		print(traceback.format_exc())

	print("Finished updating EPG")


def startTimer(delay): #minutes
	xbmc.executebuiltin("AlarmClock({0},RunScript({1}),{2},True)".format("EPGUpdate", addon_path + "/epgservice.py", delay))


if __name__ == '__main__':
	if addon.getSettingBool("epg"):
		doUpdate()

	#Set a timer for the next update
	startTimer(30)
