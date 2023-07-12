import os
import subprocess

ARPCache = subprocess.getstatusoutput('arp -a')
ARPCache = str(ARPCache)
findtype = ARPCache.find("유형")
ARPCache = ARPCache[findtype + 6:-2]
ARPCache = ARPCache.replace("\\n",",")
ARPCache = ARPCache.replace("     ",",")
ARPCache = ARPCache.replace(" ","")
ARPCache = ARPCache.replace(",,",",")
ARPCache = ARPCache[:-1]
ARPCacheTable = ARPCache.split(',')

getNetshInterface = subprocess.getstatusoutput('netsh interface show interface')
getNetshInterface = str(getNetshInterface)
findonly = getNetshInterface.find("전용")
getNetshInterface = getNetshInterface[findonly + 17:-2]
getNetshInterface = getNetshInterface.replace("\\n", ",")
getNetshInterface = getNetshInterface[:-1]
getNetshInterface = getNetshInterface.split(',')

tableLen = len(ARPCacheTable)
IPtable = []
MACtable = []
typeTable = []
i = 0
while(True):
    IPtable.append(ARPCacheTable[3 * i])
    MACtable.append(ARPCacheTable[(3 * i) + 1])
    typeTable.append(ARPCacheTable[(3 * i) + 2])
    i += 1
    if((tableLen/3) == i):
        break

print("프로그램이 정상 작동하려면 관리자 권한으로 실행되어야 합니다.")

def ARPSpoofingWarning(l):
    if len(l) != len(set(l)):
        return True 
    else:
        return False

if(ARPSpoofingWarning(MACtable)):
    print("경고! 당신의 컴퓨터는 ARP 스푸핑에 의해 공격받았을 가능성이 높습니다. ARP 테이블을 초기화하는 것을 권장합니다. ARP 테이블을 초기화하시겠습니까?")
    while(True):
        yorn = str(input('[y/n]: '))
        if yorn == "y" or yorn == "Y":
            os.system('arp -d')
            print("ARP 테이블이 성공적으로 초기화되었습니다.")
            break
        elif yorn == "n" or yorn == "N":
            print("ARP 테이블을 초기화하지 않았습니다.")
            break
        else:
            print("잘못된 입력입니다. 다시 시도해주세요.")

elif(ARPSpoofingWarning(MACtable) == False):
    print("ARP 스푸핑에 의해 공격받지 않았습니다. ARP type을 정적으로 설정하면 ARP 스푸핑을 예방할 수 있습니다. 동적으로 설정된 요소들을 정적으로 재설정하시겠습니까?")
    while(True):
        yorn = str(input('[y/n]: '))
        if yorn == "y" or yorn == "Y":
            i = 0
            b = False
            for i in range(len(typeTable)):
                if(typeTable[i] == "동적"):
                    b = True
            if(b):
                i = 0
                for i in range(len(typeTable)):
                    if(typeTable[i] == "동적"):
                        j = 0
                        for j in range(len(getNetshInterface)):
                            getResult = subprocess.getstatusoutput(f'netsh interface ipv4 add neighbors {getNetshInterface[j]} {IPtable[i]} {MACtable[i]}')
                            if(str(getResult[0:1]) == "개체"):
                                continue
                print("모든 요소들을 정적으로 설정하였습니다.")
                break

            else:
                print("동적으로 설정된 요소가 없습니다.")
                break
                
        elif yorn == "n" or yorn == "N":
            print("ARP 테이블 설정을 그대로 유지합니다.")
            break
        else:
            print("잘못된 입력입니다. 다시 시도해주세요.")
            