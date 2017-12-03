from scapy.all import *
import os
listOfAdresses={}
def main():     
    adress="192.168.1.0/24"
    ans,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=adress),timeout=2)
    dosya = open('/home/serdar/kayit','r+')
    if os.stat('/home/serdar/kayit').st_size==0:
        listOfAdresses.clear()
        print("Kayit dosyasi bos ilk kayitlar giriliyor \n")
        for s,r in ans:
            listOfAdresses[r.sprintf("%ARP.psrc%")] = r.sprintf("%Ether.src%")
            firstlaunch=1
        for i,j in listOfAdresses.items():
            print(i+'|'+j+'\n')
            dosya.write(i+'|' +j+ '\n')
        print("Kayitlari dosyaya yazildi")
    else:
        print("Kayit dosyasi bos degil kayitlar okunuyor \n")
        array = []
        for line in dosya:
            array.append(line)
        for i in array:
            ip,mac=i.split("|")
            print(ip+'|'+mac.rstrip()+'\n')
            listOfAdresses[ip]=mac.rstrip()
        control=2
        print("Kayitlari okundu")      
        for s,r in ans:
            control=0
            for i,j in listOfAdresses.items():
                if r.sprintf("%Ether.src%")==j:
                    control=1
                    if r.sprintf("%ARP.psrc%")!=i:
                        secim=raw_input(j+" Mac adresine sahip makinenin ip adresi degisti guncellensin mi? E/H ")
                        if secim=='e' or secim=='E':
                            dosya2 = open('/home/serdar/kayit','r+')
                            for line in array:
                                if line==i+'|'+j+'\n':
                                    del listOfAdresses[i]
                                    listOfAdresses[r.sprintf("%ARP.psrc%")] = r.sprintf("%Ether.src%")
                                    dosya2.write(r.sprintf("%ARP.psrc%")+'|'+r.sprintf("%Ether.src%")+'\n')
                                else:
                                    dosya2.write(line)
                            print("Guncellendi \n")
                            dosya2.close()
                        elif secim=='h' or secim=='H':
                            print("Guncellenmeyecek \n")
                        else:
                            print("Yanlis bir secim yaptiniz guncellenmeyecek \n")
         
                        
        if control==0:
            ekle=raw_input(r.sprintf("%Ether.src%")+ "Mac Adresine sahip Yeni Makine Bulundu Eklenilsin mi? E/H ")
            if ekle=='E'or ekle=='e':
                dosya.write(r.sprintf("%ARP.psrc%")+'|'+r.sprintf("%Ether.src%")+'\n')
                print(" \n Eklendi")
            elif ekle=='H'or ekle=='h':
                print("Eklenmeyecek \n")
            else:
                print("Yanlis bir secim yaptiniz eklenmeyecek")
        dosya.close()
        repeat()
def repeat():
    secim2=raw_input("Tekrar tarama yapmak ister misiniz? E/H ")
    if secim2=='e' or secim2=='E':
        main()
    elif secim2=='h' or secim2=='H':
        print("Program Kapatiliyor \n")
    else:
        print("Yanlis bir secim yaptiniz \n")
        repeat()                   
if __name__ == "__main__": main()            
