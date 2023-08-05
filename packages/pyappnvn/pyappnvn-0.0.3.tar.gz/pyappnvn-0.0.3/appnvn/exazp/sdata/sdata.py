from pynvn.excel.crelistadict import credict
from pynvn.dict.csv import dicttocsv
from pynvn.path.ppath import parentdirectory,refullpath
from pynvn.excel.path import returnactivewbpath
from pynvn.csv.rcsv import returndictrowforcsv
from pynvn.list.tocsv import listocsvver
from pynvn.excel import col2num,activeworkbook_fullname
class covertcsvexcel:
    """ convert data to csv and to excel """
    def __init__ (self,pathconf = None):
        self.__pathconf = pathconf
        dirparhconf = parentdirectory(self.__pathconf)
        dicrowconf = returndictrowforcsv(path=pathconf)
        self.__sheetnametor=dicrowconf["khns_sheetnamekhns"]
        self.__khns_namfile=dicrowconf["khns_namfile"]
        self.__khns_rangenumbermct_ptvt =dicrowconf["khns_rangenumbermct_ptvt"]
        self.__valuenotnone =dicrowconf["valuenotnone"]
        self.__valueall =dicrowconf["valueall"]
        self.__dictvalue =dicrowconf["dictvalue"]
        self.__mvta = (dicrowconf["khns_mavatu"])
        self.__mvt  = col2num(self.__mvta)
        
        #self.__fpath = returnactivewbpath(namefile=self.__khns_namfile)
        self.__fpath = activeworkbook_fullname()

        self.__rel = credict(pathfull=self.__fpath,
                    namesheet=self.__sheetnametor,
                    engine="xlwings",
                    rangea=self.__khns_rangenumbermct_ptvt
                    )
        # csv for dict 
        self.pathtovalue = refullpath(dirparhconf,self.__dictvalue)
        # csv for value 
        self.valuenotnone = refullpath(dirparhconf,self.__valuenotnone)

        # csv for all value 
        self.pathvalueall = refullpath(dirparhconf,self.__valueall)

        
        # get all key redic incule len != 0 
        self.redic_all =self.__rel.redictvaluesandvaluecol(columnumber=self.__mvt,
                                                            removeemtyvalue= False)


        #self.redic =self.__rel.redictvaluesandvaluecol(columnumber=self.__mvt)
        
        self.redic = {key:val for key, val in self.redic_all.items() if len(val) != 0} 

        self.valueredicttocsv()
        self.valuelisttocsv()
    def valueredicttocsv(self):
        """ return value and key follow dict"""
        dicttocsv(dictl=self.redic,
                    path=self.pathtovalue
                    )
    def valuelisttocsv (self):
        """ value list to csv """
        # convert to csv value chuan 
        getvaluelist = list(self.redic.keys())
        listva = listocsvver(pathtow=self.valuenotnone,listv=getvaluelist)
        # convert to csv all value
        lvalueall = list(self.redic_all.keys())
        listva = listocsvver(pathtow=self.pathvalueall,listv=lvalueall)