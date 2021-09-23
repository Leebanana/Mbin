from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import time 
import pathlib
import tkinter.messagebox
import struct
import re
class MBinTool:

    def __init__(self, root):

        root.title("MBin Tool")

        self.mainframe = ttk.Frame(root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        self.fileframe = ttk.Frame(root, padding="3 3 12 12")
        self.fileframe.grid(column=0, row=1024, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
       
        self.tree_view = ttk.Treeview(self.mainframe)
        self.tree_view['columns'] = ["id","file_name", "file_size", "offset","align","convert"]

        #self.tree_view.column("id",width = 100)
        self.tree_view.column("id",width = 100)
        self.tree_view.column("file_name",width = 400)
        self.tree_view.column("file_size",width = 100)
        self.tree_view.column("offset",width = 100)
        self.tree_view.column("align",width = 100)
        self.tree_view.column("convert",width = 100)

        self.tree_view.heading("id",text = "序号")
        self.tree_view.heading("file_name",text = "文件名")
        self.tree_view.heading("file_size",text = "文件大小")
        self.tree_view.heading("offset",text = "偏移地址")
        self.tree_view.heading("align",text = "字节对齐")
        self.tree_view.heading("convert",text = "转换字节序")

        #self.tree_view.insert('',0,text=str(0),values=("bin1",0x123456,0x123,"y"))
        self.tree_view.bind('<Double-1>', self.set_cell_value)
        
        self.text_src = ttk.Label(self.fileframe, text="源文件").grid(column=0, row=1024, sticky=W)
        self.bottonfile = StringVar()
        self.file_entry = ttk.Entry(self.fileframe, width=64, textvariable=self.bottonfile)
        self.file_entry.grid(column=4, row=1024, sticky=(W, E))
        self.open_botton = ttk.Button(self.fileframe, text="浏览", command=self.openfile).grid(column=64, row=1024, sticky=W)
        self.add_botton =  ttk.Button(self.fileframe, text="添加", command=self.add_bin_file).grid(column=68, row=1024, sticky=W)
        self.delete_all_botton =  ttk.Button(self.fileframe, text="删除", command=self.delete_bin_file).grid(column=72, row=1024, sticky=W)
        
        self.text_dst = ttk.Label(self.fileframe, text="目标文件").grid(column=0, row=1028, sticky=W)
        self.dstfile = StringVar()
        self.dstfile.set((os.getcwd()+"\\result.bin").replace("\\","/"))
        self.dst_file_entry = ttk.Entry(self.fileframe, width=64, textvariable=self.dstfile)
        self.dst_file_entry.grid(column=4, row=1028, sticky=(W, E))
        self.open_botton = ttk.Button(self.fileframe, text="浏览", command=self.open_dstfile).grid(column=64, row=1028, sticky=W)
        self.combine_botton =  ttk.Button(self.fileframe, text="合并", command=self.combine).grid(column=68, row=1028, sticky=W) 
        self.delete_botton =  ttk.Button(self.fileframe, text="清除", command=self.delete_all_bin_file).grid(column=72, row=1028, sticky=W)  
        #self.add_botton = ttk.Button(self.mainframe, text="添加", command=self.openfile).grid(column=64, row=64, sticky=W)

        self.bin_list = []
        self.file_num = 0
        self.frames = []
        self.gAlloffset = 0
        self.gAllalign = 0
        self.gAllconvert = False
        self.dir_path = "./"
        self.offset = 0
        self.select_file_id = 0
        self.dst_file = ""
        self.dst_file_text = StringVar()
        self.offset_count = 0
        self.temp_file = "./temp.bin"
        for child in self.mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)
    def openfile(self):

        if(self.dir_path  == ""):
            self.bottonfile = filedialog.askopenfilename(title=u'选择文件')
        else:
            self.bottonfile = filedialog.askopenfilename(title=u'选择文件',initialdir=self.dir_path)
        print(self.bottonfile)
        self.file_entry.delete(0,'end')
        self.file_entry.insert(0,self.bottonfile)
    def open_dstfile(self):

        if(self.dir_path  == ""):
            self.dst_file = filedialog.askdirectory(title=u'选择文件')+"/"
        else:
            self.dst_file = filedialog.askdirectory(title=u'选择文件',initialdir=self.dir_path)+"/"
        print(self.dstfile)
        self.dst_file_entry.delete(0,'end')
        self.dst_file_entry.insert(0,self.dst_file)
        #e_path.delete(0, tk.END)
        #e_path.insert(0, dirpath)
        #file_dir_divider(dirpath)

    def add_bin_file(self):
        if(os.path.exists(str(self.bottonfile))):
            time_value = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            offset_addr = "0x0000"
            print(self.bin_list)
            self.file_num += 1 
            if(len(self.bin_list)>0):
                if(int(self.bin_list[-1][5],16)>0):
                    temp = (int(self.bin_list[-1][3],16) + self.offset_count) %int(self.bin_list[-1][5],16)
                    if temp == 0 :
                        self.offset_count = int(self.bin_list[-1][3],16) + int(self.bin_list[-1][4],16)
                    else:
                        zero_num = int(self.bin_list[-1][5],16) - temp
                        self.offset_count = int(self.bin_list[-1][3],16) + zero_num + int(self.bin_list[-1][4],16)
                else:
                    self.offset_count = int(self.bin_list[-1][3],16)+int(self.bin_list[-1][4],16)
                offset_addr = str(hex(self.offset_count))
            self.bin_list.append([time_value, str(self.file_num), self.bottonfile, str(hex(os.path.getsize(self.bottonfile))), offset_addr, "0x0004", "y"])
            #self.tree_view.insert("",len(self.bin_list),text=str(len(self.bin_list)),values = (self.bottonfile, os.path.getsize(self.bottonfile), 0, 0, "y"))
            self.tree_view.insert("",len(self.bin_list),text= time_value,values = (str(self.file_num),self.bottonfile, str(hex(os.path.getsize(self.bottonfile))), offset_addr, "0x0004", "y"))
            self.tree_view.update()
    def delete_all_bin_file(self):
        self.bin_list.clear()
        x=self.tree_view.get_children()
        for item in x:
            self.tree_view.delete(item)
        self.offset_count = 0
        self.file_num = 0
        print(self.bin_list)
    def delete_bin_file(self):
        self.bin_list.pop()
        x=self.tree_view.get_children()
        item_last = 0
        for item in x:
            item_last = item
        #self.offset_count = 0
        self.tree_view.delete(item_last)
        self.file_num -= 1 
        print(self.bin_list)

    def set_cell_value(self, event): # 双击进入编辑状态
        
        #column= self.tree_view.identify_column(event.x)# 列
        #row = self.tree_view.identify_row(event.y)  # 行
        #cn = int(str(column).replace('#',''))
        #rn = int(str(row).replace('I',''))
        #print(cn,rn)

        for item in self.tree_view.selection():
                #item = I001
                item_text = self.tree_view.item(item, "values")
                print(item_text)  # 输出所选行的值
        setting_window = Toplevel(root)
        #setting_window.geometry('300x200')
        setting_window.title("设置")
        ttk.Label(setting_window,text = "偏移地址").grid(column=0, row=0, sticky=W)
        ttk.Label(setting_window,text = "字节对齐").grid(column=4, row=0, sticky=W)
        ttk.Label(setting_window,text = "转换字节序").grid(column=8, row=0, sticky=W)
        offset_entry_text = StringVar()
        offset_entry_text.set(item_text[3])
        print(offset_entry_text)
        offset_entry = ttk.Entry(setting_window, textvariable=offset_entry_text)
        offset_entry.grid(column=0, row=1, sticky=W)
        align_entry_text = StringVar()
        align_entry_text.set(item_text[4])
        align_entry = ttk.Entry(setting_window, textvariable=align_entry_text)
        align_entry.grid(column=4, row=1, sticky=W)
        convert_entry_text = StringVar()
        convert_entry_text.set(item_text[5])
        convert_entry = ttk.Entry(setting_window, textvariable=convert_entry_text)
        convert_entry.grid(column=8, row=1, sticky=W)

        def confir_func():
            offset = offset_entry_text.get()
            align = align_entry_text.get()
            convert = convert_entry_text.get()
            print(offset,align,convert)
            #print( self.is_hex(offset.replace('0x','')),self.is_hex(align.replace('0x','')))
            try:
                offsetint = int(offset,16)
                alignint = int(align,16)
                #print(offsetint)
                #print(alignint)
            except ValueError:
                tkinter.messagebox.showinfo(title='error', message='偏移量或者字节对齐参数错误！')
                return
            if(offset == "" or align == ""):
                tkinter.messagebox.showinfo(title='error', message='偏移量或者字节对齐参数错误！')
                return
            if(convert != "y" and convert != "n"):
                tkinter.messagebox.showinfo(title='error', message='字节序转换只能设置参数\'y\'或者\'n\'！')
                return
            time_value = ""
            for bin in self.bin_list:
                if(item_text[0] in bin[1]):
                    bin[2] = item_text[1]
                    bin[3] = item_text[2]
                    bin[4] = offset
                    bin[5] = align
                    bin[6] = convert
                    time_value = bin[0]
            self.tree_view.item(item,text=time_value,values = (item_text[0],item_text[1],item_text[2],offset,align,convert))
            print(self.bin_list)
                
                
        confir_botton = ttk.Button(setting_window, text="确认", command=confir_func).grid(column=48, row=1, sticky=(W,E))

    def combine(self):
        if(len(self.bin_list) == 0):
           tkinter.messagebox.showinfo(title='error', message='请先添加文件！')
           return
        print(self.dstfile)
        if(self.dstfile.get() == ""):
            tkinter.messagebox.showinfo(title='error', message='请先设置目标文件！')
            return
        self.dst_file = str(self.dst_file_entry.get())
        if(os.path.exists(self.dst_file)==True):
            print("remove dst file")
            os.remove(self.dst_file)
        if(os.path.exists(self.temp_file)==True):
            print("remove dst file")
            os.remove(self.temp_file)
        pathlib.Path(self.dst_file).touch()
        
        print(self.bin_list)
        for bin_it in self.bin_list:
            print(int(bin_it[4],16),os.path.getsize(self.dst_file))
            if(int(bin_it[4],16)>=os.path.getsize(self.dst_file)):
                print("add zero size",int(bin_it[4],16) - os.path.getsize(self.dst_file))
                self.add_zero(self.dst_file,int(bin_it[4],16) - os.path.getsize(self.dst_file))
                if(bin_it[6] == 'y'):
                    print("convert file",bin_it[2])
                    pathlib.Path(self.temp_file).touch()
                    self.convert(bin_it[2],self.temp_file)
                    self.add_bin(self.dst_file,self.temp_file)
                    os.remove(self.temp_file)
                else:
                    self.add_bin(self.dst_file,bin_it[2])

                if(int(bin_it[5],16)>0):
                    self.bin_set_align(self.dst_file, int(bin_it[4],16), int(bin_it[5],16))
                    print("set offset", int(bin_it[5],16))
            else:
                tkinter.messagebox.showinfo(title='error', message='请检查文件的偏移地址！')
                os.remove(self.dst_file)
                break

    def set_all_offset(self, all_offset):
        self.gAlloffset = all_offset
    def set_all_align(self, all_align):
        self.gAllalign = all_align
    def set_all_convert(self, all_convert):
        self.set_all_convert = all_convert
    #def generate(self, file_result):

    def add_bin(self, src_file, sound_file):
        dst_bin = open(src_file, 'ab+')
        sound_bin = open(sound_file, 'rb')
        sound_file_size = os.path.getsize(sound_file)
        for i in range(sound_file_size):
            data = sound_bin.read(1)
            dst_bin.write(data)
        sound_bin.close

    def add_zero(self,src_file, dst_zero_size):
        src_file_size = os.path.getsize(src_file)
        #src_bin = open(src_file, 'rb')
        dst_bin = open(src_file, 'ab+')
        data = struct.pack('b',0)
        #copy src bin to dst bin
        for i in range(dst_zero_size):
            dst_bin.write(data)
        dst_bin.close()
    def bin_set_align(self, src_file, file_offset, align_num):
        bin_size = os.path.getsize(src_file)
        #print("algin size before:0x%x"%bin_size)
        temp = (bin_size+file_offset)%align_num
        if temp == 0 :
            return
        zero_num = align_num - temp
        self.add_zero(src_file, zero_num)
    def convert(self,src_file,dst_file):
        file_datas =[]
        bin_src = open(src_file, 'rb')
        dst_bin = open(dst_file, 'ab+')
        for i in range(os.path.getsize(src_file)):
            data = bin_src.read(1)
            file_datas.append(data)
        bin_src.close
        alin = len(file_datas)%4
        len_after_alin  = 0 #? DUAL_TALK_CFG_LEN : (DUAL_TALK_CFG_LEN + (4-alin))
        if((alin == 0)):
            len_after_alin = len(file_datas)
        else:
            len_after_alin = len(file_datas) + (4-alin)
            for i in range((4-alin)):
                file_datas.append(struct.pack('b',0))
        for i in range(0,len_after_alin,4):
            temp = file_datas[i]
            file_datas[i] = file_datas[i+3]
            file_datas[i+3] = temp
            temp = file_datas[i+1]
            file_datas[i+1] = file_datas[i+2]
            file_datas[i+2] = temp
        for i in range(len(file_datas)):
            dst_bin.write(file_datas[i])
        dst_bin.close()
    def calculate(self, *args):
        try:
            value = float(self.feet.get())
            self.meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0)
        except ValueError:
            pass
    def is_hex(self,s):
        return print(re.match(r"^[0-9a-fA-F]$", s))
root = Tk()
MBinTool(root)
root.mainloop()