# windows日志分析
'''
author: rocky chen
公众号：可转债量化分析
'''
import mmap
import contextlib
from Evtx.Evtx import FileHeader
from Evtx.Views import evtx_file_xml_view
from xml.dom import minidom
from ip_convertor import IP
import re

class WindowsLogger():

    def __init__(self, path):
        self.path = path
        self.formator = 'Date:{:10}\tIP:{}\tPort:{}\tlocation:{:20}\tUser:{:15}\tProcess:{}'

    def read_file(self):
        with open(self.path, 'r') as f:
            with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as buf:
                fh = FileHeader(buf, 0)
                return fh

        return None

    def parse_log_detail(self, filteID):
        with open(self.path, 'r') as f:
            with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as buf:
                fh = FileHeader(buf, 0)
                for xml, record in evtx_file_xml_view(fh):
                    # 只输出事件ID为4624的内容
                    # InterestEvent(xml,4624)
                    for time_create,IpAddress, ip, IpPort,targetUsername, ProcessName in self.filter_event(xml, filteID):
                        self.printer(
                            time_create,IpAddress, IpPort,ip, targetUsername, ProcessName)

    def printer(self, time_create,IpAddress, ip, IpPort,targetUsername, ProcessName):
        print(self.formator.format(time_create,IpAddress, ip, IpPort,targetUsername, ProcessName))

    # 过滤掉不需要的事件，输出感兴趣的事件
    def filter_event(self, xml, EventID, use_filter=True):
        xmldoc = minidom.parseString(xml)
        collections = xmldoc.documentElement
        events = xmldoc.getElementsByTagName('Event')
        for evt in events:
            eventId = evt.getElementsByTagName('EventID')[0].childNodes[0].data
            time_create = evt.getElementsByTagName(
                'TimeCreated')[0].getAttribute('SystemTime')
            eventData = evt.getElementsByTagName('EventData')[0]

            for data in eventData.getElementsByTagName('Data'):
                if data.getAttribute('Name') == 'IpAddress':
                    IpAddress = data.childNodes[0].data
                if data.getAttribute('Name') == 'IpPort':
                    IpPort = data.childNodes[0].data

                if data.getAttribute('Name') == 'TargetUserName':
                    targetUsername = data.childNodes[0].data

                if data.getAttribute('Name') == 'ProcessName':
                    ProcessName = data.childNodes[0].data

            if use_filter is True and eventId == EventID:
                ip = ''
                if re.search('^\d+', IpAddress):
                    ip = IP(IpAddress).ip_address

                yield time_create,IpAddress, ip, IpPort,targetUsername, ProcessName


def main():
    # evtx file path
    path = r'D:\share\failed.evtx'
    # filter idd
    filter_id = '4625'

    app = WindowsLogger(path)
    app.parse_log_detail(filter_id)

if __name__ == '__main__':
    main()
