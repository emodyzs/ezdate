from datetime import datetime,date,timedelta
from dateutil.relativedelta import relativedelta

from ezhelper import *


def fn_today(format='.'):
    # date.today() is jó
    if format=='c10.' or format=='.':
        return datetime.now().strftime('%Y.%m.%d')
    elif format=='c10-' or format=='-':
        return datetime.now().strftime('%Y-%m-%d')
    elif format=='c8':
        return datetime.now().strftime('%Y%m%d')

def fn_dateadd(dt,nToAdd,unit='day'):
    if unit=='month':
        return dt + relativedelta(months=nToAdd)
    elif unit=='year':
        return dt.replace(year=dt.year+nToAdd)
    elif unit=='week':
        return dt + timedelta(weeks=nToAdd)
    elif unit=='day':
        return dt + timedelta(days=nToAdd)

def fn_daydiff(dt1,dt2):
    return (dt1-dt2) / timedelta(days=1)

def fn_monthlastday(dt):
    # A megadott nap hónapjának utolsó napja
    return fn_dateadd(fn_dateadd(dt,1,'month'),-1)

def fn_monday(dt='today'):
    # A megadott nap hetének hétfői napja
    if dt=='today': dt=date.today()
    return fn_dateadd(dt,-dt.weekday())         # 0 bázisú



def text2date(text,dt0=None,tense='',outtype='first'):
    ''' Magyar nyelvű időmeghatározások lefordítása egy dátumra vagy dátum tartományra
    text:  általában több szavas
        A mondatban dátum-meghatározástól független szavak is lehetnek
    dt0:  relációs dátummeghatározások esetén a kiinduló dátum.
        Ha nincs megadva, akkor a mai nap.
    tense: 'future' / 'past'.  A nem egyértelmű időmeghatározások esetén jövőbeli vagy múltbeli dátumot preferáljon a függvény
        Ha üres, akkor az aktuális évben/hónapban/héten
    outtype:
      'first':    return =  '',   '2021.10.12',  '2021.12.10-2021.12.20'     Az első előforduló dátum vagy dátumtartomány.
      'first+':   ugyanaz mint a first, de a string végére beírja a pattern-t is   Példa: '2021.10.12   pattern: [szám] [hónapnév] [szám]
      'all':      '2021.10.12,2021.12.10-2021.12.20'
    '''
    
    # Annnotálás
    pattern,invalues,outvalues = d_annotate(text,lookup_text2dateG,True)
    

    def sub_sorszam(szám_in):
        return  szám_in and endwith(szám_in,r'\.|dik|első')


    def sub_patterns(patternL,invaluesL,outvaluesL,nCycle,dt0):   # -> (date1, date2)  vagy None 

        if dt0==None: dt0=datetime.now()

        dtout=None
        dtout2=None

        # első körös mintázatok
        if nCycle==1:

            if patternL=='[szám] [szám] [szám]':
                n1,n2,n3=outvaluesL
                if (n1>=1000 and n1<=2100) and (n2>=1 and n2<=12) and (n3>=1 and n2<=31): 
                    try: dtout=datetime(n1,n2,n3)
                    except: dtout=None

            elif patternL=='[szám] [szám] [időtartam] [szám]':     # 2022. II.hó 4.
                n1,n2,időtartam,n3=outvaluesL
                if időtartam=='hónap':
                    if (n1>=1000 and n1<=2100) and (n2>=1 and n2<=12) and (n3>=1 and n2<=31): 
                        szám_in=invaluesL[3]
                        if not endwith(szám_in,'dik|első'):
                            try: dtout=datetime(n1,n2,n3)
                            except: dtout=None

            elif patternL=='[szám] [hónapnév] [szám]':
                n1,honap,n2=outvaluesL
                # "első", "második", ... nem megengedett  (pl. "2022 március első péntek")
                szám_in=invaluesL[2]
                if not endwith(szám_in,'dik|első'):
                    try: dtout=datetime(n1,int(honap),n2)
                    except: dtout=None

            elif patternL=='[szám] [hónapnév]':
                n1,honap=outvaluesL
                n2=int(honap)
                if (n1>=1000 and n1<=2100) and (n2>=1 and n2<=12): 
                    dtout=datetime(n1,n2,1)
                    dtout2=fn_monthlastday(dtout)

            elif patternL=='[hónapnév] [szám]':
                honap,n2=outvaluesL
                szám_in = invaluesL[1]
                if not (endwith(szám_in,'dik') or szám_in=='első'):     # "január első fele" ne "január 1." legyen
                    try: dtout=datetime(dt0.year,int(honap),n2)
                    except: dtout=None

            elif patternL=='[szám] [szám]':
                n1,n2=outvaluesL
                # "2022 01"   
                if (n1>=1000 and n1<=2100) and (n2>=1 and n2<=12): 
                    szám_in = invaluesL[1]
                    if len(szám_in)==2 and szám_in.isdigit():    # fontos, hogy a "2021 2. ne kerüljön ide (pl. nem működne a "2021. második fele" beazonosítása)
                        dtout=datetime(n1,n2,1)
                        dtout2=fn_monthlastday(dtout)
                # "01 12"    hónap nap
                elif (n1>=1 and n1<=12) and (n2>=1 and n2<=31):
                    try: dtout=datetime(dt0.year,n1,n2)
                    except: dtout=None
                # "2012-2014"
                elif (n1>=1000 and n1<=2100) and (n2>=1000 and n2<=2100) and (n2>n1):
                    dtout=datetime(n1,1,1)
                    dtout2=datetime(n2,12,31)

            elif patternL=='[szám] [évszak]':   # "2015 tavasz"   "tavaly télen"   "jövőre nyáron"
                n,évszak=outvaluesL         # évszak: 3,6,9,12

                if n>=1 and n<=2100:
                    if évszak=='12': n-=1    # a tél átnyúlik az évhatáron, a kezdődátuma előző évi
                    dtout=datetime(n,int(évszak),1)    
                    dtout2=fn_monthlastday(fn_dateadd(dtout,2,'month'))

            elif patternL=='[szám]':
                n,=outvaluesL
                szám_in,=invaluesL
                # évszám
                if n>=1000 and n<=2100:
                    dtout=datetime(n,1,1)
                    dtout2=datetime(n,12,31)
                # másodikán, másodikától, ...  (de "első" "második" ne kerüljön ide)
                elif n>=1 and n<=31 and vanbenne(szám_in,'dika|dike|diká|diké|elsej'):
                    try: dtout=datetime(dt0.year,dt0.month,n)
                    except: dtout=None
                # '20220102'  '19551211'
                elif len(szám_in)==8:
                    if beginwith(szám_in,'19|20'): 
                        try: dtout=datetime(int(szám_in[:4]),int(szám_in[4:6]),int(szám_in[6:]))
                        except: dtout=None
                # '0203'  '1201'
                elif len(szám_in)==4:
                    if beginwith(szám_in,'0|1'): 
                        try: dtout=datetime(dt0.year,int(szám_in[:2]),int(szám_in[2:]))
                        except: dtout=None

            elif patternL=='[maholnap]':
                n,=outvaluesL
                dtout=fn_dateadd(dt0,int(n))       

            elif patternL=='[maholnap] [időtartam]':     # 'mai napon', 'holnapi napon', 
                maholnap,időtartam=outvaluesL
                n=int(maholnap)
                if időtartam=='nap':
                    dtout=fn_dateadd(dt0,n)       

            elif patternL=='[maholnap] [utánelőtt]':     # 'holnap után', 'tegnap előtt', 
                maholnap,utánelőtt=outvaluesL
                n=int(maholnap)
                if n==1 and utánelőtt=='után': dtout=fn_dateadd(dt0,2)       
                elif n==-1 and utánelőtt=='előtt': dtout=fn_dateadd(dt0,-2)       

            elif (patternL=='[hónapnév]' or
                  patternL=='[hónapnév] [időtartam]'):          # február hónap
            
                if '[időtartam]' in patternL:
                    n,időtartam = outvaluesL
                else:
                    n,=outvaluesL
                    időtartam='hónap'

                if időtartam=='hónap':
                    n=int(n)


                    dtout=datetime(dt0.year,n,1)         # aktuális évben
                    # Ha van kontextus, akkor eltolásra lehet szükség
                    if tense=='future' and n<dt0.month: dtout=fn_dateadd(dtout,1,'year')
                    elif tense=='past' and n>dt0.month: dtout=fn_dateadd(dtout,-1,'year')
                    dtout2=fn_monthlastday(dtout)

            elif patternL=='[hétnapja]':
                hétnapja,=outvaluesL        # '1', ..., '7', 'hétvége'
                dtMonday=fn_monday(dt0)
                # Az aktuális héten
                if hétnapja=='hétvége': 
                    dtout=fn_dateadd(dtMonday,5)    # szombat
                    if tense=='past' and dtout>dt0: dtout=fn_dateadd(dtout,-7)
                    dtout2=fn_dateadd(dtout,1)
                else:
                    dtout=fn_dateadd(dtMonday,int(hétnapja)-1)
                    # Ha van kontextus, akkor eltolásra lehet szükség
                    if tense=='future' and dtout<dt0: dtout=fn_dateadd(dtout,7)
                    elif tense=='past' and dtout>dt0: dtout=fn_dateadd(dtout,-7)

            elif patternL=='[évszak]':
                value,=outvaluesL
            
                year=dt0.year
                if value=='12' and dt0.month<6: year-=1    # a tél átnyúlik az évhatáron, ezért nem teljesen egyértelmű az "ezen a télen" ... jelentése

                dtout=datetime(year,int(value),1)    # kezdődátum
                dtout2=fn_monthlastday(fn_dateadd(dtout,2,'month'))

                # Ha van kontextus, akkor eltolásra lehet szükség
                if tense=='future' and dt0>dtout2:   # "télen hideg lesz",  az aktuális tél után vagyunk
                    dtout=fn_dateadd(dtout,1,'year')
                    dtout2=fn_monthlastday(fn_dateadd(dtout,2,'month'))
                elif tense=='past' and dt0<dtout:   # "télen hideg volt",  az aktuális tél előtt vagyunk
                    dtout=fn_dateadd(dtout,-1,'year')
                    dtout2=fn_monthlastday(fn_dateadd(dtout,2,'month'))
            
            elif (patternL=='[évnapja]' or              # karácsony, újév
                  patternL=='[dátum] [évnapja]' or
                  patternL=='[múltjövő] [évnapja]'):       # 2023 karácsony
                
                year=None
                if patternL=='[évnapja]':              # karácsony, újév
                    évnapja, = outvaluesL
                    year=dt0.year
                elif patternL=='[dátum] [évnapja]':
                    dátum,évnapja = outvaluesL
                    dt1,dt2 = dátum
                    year=dt1.year
                elif patternL=='[múltjövő] [évnapja]':
                    múltjövő,évnapja = outvaluesL
                    year=dt0.year
                    if múltjövő=='múlt': year=year-1
                    elif múltjövő=='jövő': year=year+1

                if évnapja=='karácsony':
                    dtout=datetime(year,12,25)
                    dtout2=datetime(year,12,26)
                elif évnapja=='szenteste':
                    dtout=datetime(year,12,24)
                elif évnapja=='szilveszter':
                    dtout=datetime(year,12,31)
                elif évnapja=='újév':
                    dtout=datetime(year,1,1)



            elif patternL=='[múltjövő]':    # 'most'
                múltjövő, = outvaluesL
                if múltjövő=='most': dtout=date.today()

            elif patternL=='[szám] [időtartam] [múlvaezelőtt]':       # 2 nap múlva, 3 év múlva,  négy hét múlva,  egy évvel ezelőtt
                # FONTOS:  a "[szám] [időtartam]" mintázatnál van egy hasonló eset:   "3 éve",  "két hónapja",   "5 hete" 
                szám,időtartam,múlvaezelőtt=outvaluesL
                if múlvaezelőtt=='ezelőtt': szám=-szám
                
                if időtartam=='nap':
                    dtout=fn_dateadd(dt0,szám)
                elif időtartam=='hét':
                    dtout=fn_dateadd(dt0,7*szám)
                elif időtartam=='hónap':
                    dtout=fn_dateadd(dt0,szám,'month')
                elif időtartam=='év':
                    dtout=fn_dateadd(dt0,szám,'year')

            elif patternL=='[szám] [időtartam]':            # "2022 év", "XIX. században", "90-es években", "két hete", "12 éve", "20 napja"
                # [sorszám] [időtartam] nélkül (csak a második körben lesz kezelve)
                szám,időtartam = outvaluesL

                szám_in = invaluesL[0]
                időtartam_in=invaluesL[1]
                #  "két hete",  "három hónapja",  "12 éve"   "20 napja"  (kétértelmű, de időpontot is jelenthet, "... ezelőtt" jelentéssel) 
                if időtartam_in in ['éve','hónapja','hete','napja']: 
                    szám=-szám
                    if időtartam=='nap':
                        dtout=fn_dateadd(dt0,szám)
                    elif időtartam=='hét':
                        dtout=fn_dateadd(dt0,7*szám)
                    elif időtartam=='hónap':
                        dtout=fn_dateadd(dt0,szám,'month')
                    elif időtartam=='év':
                        dtout=fn_dateadd(dt0,szám,'year')

                # "'90-es évek", "1870-es évek", "1200-as évek",
                elif beginwith(időtartam_in,'évek|évei') and (szám % 10)==0:
                    if (szám % 100) ==0:
                        dtout=datetime(szám,1,1)
                        dtout2=datetime(szám+99,12,31)
                    elif szám<100:      # jelen vagy múltbelinek tekintem ('30-as évek: 1930-as évek)
                        évszázad0 = dt0.year//100
                        évtized0 = (dt0.year - évszázad0*100)//10
                        évtized = szám//10
                        if évtized>évtized0: évszázad0-=1
                        dtout=datetime(évszázad0*100 + szám,1,1)
                        dtout2=datetime(évszázad0*100 + szám + 9,12,31)
                    else:
                        dtout=datetime(szám,1,1)
                        dtout2=datetime(szám + 9,12,31)
               
                elif időtartam=='év' and szám>1900 and szám<=2100:      # ha nincs utána pont, akkor is tekintse konkrét évszámnak
                    dtout=datetime(szám,1,1)
                    dtout2=datetime(szám,12,31)

                elif időtartam=='évszázad':          # időszámítás kezdete óta
                    if szám>=1 or szám<=30:
                        dtout=datetime((szám-1)*100,1,1)
                        dtout2=datetime((szám-1)*100 + 99,12,31)

            elif (patternL=='[szám] [időtartam] [múlvaezelőtt] [hónapnév]' or       # 3 évvel ezelőtt decemberben, két év múlva októberben
                  patternL=='[szám] [időtartam] [hónapnév]'):                       # 3 éve decemberben, két éve októberben
                
                if patternL=='[szám] [időtartam] [múlvaezelőtt] [hónapnév]':
                    szám,időtartam,múlvaezelőtt,hónap=outvaluesL
                    if múlvaezelőtt=='ezelőtt': szám=-szám
                elif patternL=='[szám] [időtartam] [hónapnév]':
                    szám,időtartam,hónap=outvaluesL
                    időtartam_in=invaluesL[1]
                    if időtartam_in!='éve': időtartam=''
                    szám=-szám
                if időtartam=='év':
                    if int(hónap)>=1 and int(hónap)<=12:
                        dtout=datetime(dt0.year+szám,int(hónap),1)
                        dtout2=fn_monthlastday(dtout)

            elif (patternL=='[szám] [időtartam] [múlvaezelőtt] [szám]' or       # 2 hónappal ezelőtt 5-én, három hónap múlva hatodikán
                  patternL=='[szám] [időtartam] [szám]'):                       # három hónapja negyedikén

                if patternL=='[szám] [időtartam] [múlvaezelőtt] [szám]':
                    szám,időtartam,múlvaezelőtt,n=outvaluesL
                    szám_in=invaluesL[3]
                    if múlvaezelőtt=='ezelőtt': szám=-szám
                elif patternL=='[szám] [időtartam] [szám]':
                    szám,időtartam,n=outvaluesL
                    szám_in=invaluesL[2]
                    időtartam_in=invaluesL[1]
                    if időtartam_in!='hónapja': időtartam=''
                    szám=-szám

                if időtartam=='hónap':
                    dt0=fn_dateadd(dt0,szám,'month')
                    if n>=1 and n<=31:   # and (endwith(szám_in,'\.') or vanbenne(szám_in,'dika|dike|diká|diké|elsej')):
                        try: dtout=datetime(dt0.year,dt0.month,n)
                        except: dtout=None

            elif (patternL=='[szám] [időtartam] [múlvaezelőtt] [hétnapja]' or       # 4 héttel korábban pénteken, két hét múlva hétvégén
                  patternL=='[szám] [időtartam] [hétnapja]'):        # két hete szombaton
                
                if patternL=='[szám] [időtartam] [múlvaezelőtt] [hétnapja]':
                    szám,időtartam,múlvaezelőtt,hétnapja=outvaluesL
                    if múlvaezelőtt=='ezelőtt': szám=-szám
                elif patternL=='[szám] [időtartam] [hétnapja]':
                    szám,időtartam,hétnapja=outvaluesL
                    szám=-szám
                    időtartam_in=invaluesL[1]
                    if időtartam_in!='hete': időtartam=''
                
                if időtartam=='hét':
                    dt0=fn_dateadd(dt0,7*szám)
                    dtMonday=fn_monday(dt0)
                    if hétnapja=='hétvége': 
                        dtout=fn_dateadd(dtMonday,5)    # szombat
                        dtout2=fn_dateadd(dtout,1)
                    else:
                        dtout=fn_dateadd(dtMonday,int(hétnapja)-1)


            elif patternL=='[múltjövő] [időtartam]':           # múlt pénteken, előző évben, következő hónapban, jövő félévben, következő héten
                múltjövő,időtartam=outvaluesL
        
                szám=1
                if múltjövő=='múlt': szám=-1
                elif múltjövő=='most': szám=0
        
                if időtartam=='nap':
                    dtout=fn_dateadd(dt0,szám)
                elif időtartam=='hét':
                    dtMonday=fn_monday(dt0)             # az aktuális hét első napja
                    dtout=fn_dateadd(dtMonday,7*szám)   # előző, aktuális, következő
                    dtout2=fn_dateadd(dtout,6)          
                elif időtartam=='hónap':
                    dtMonthfirst=dt0.replace(day=1)
                    dtout=fn_dateadd(dtMonthfirst,szám,'month')
                    dtout2=fn_monthlastday(dtout)
                elif időtartam=='negyedév':
                    dtFirst=dt0.replace(month=(1 + ((dt0.month-1)//3) * 3))
                    dtFirst=dt0.replace(day=1)
                    dtout=fn_dateadd(dtFirst,3*szám,'month')
                    dtout2=fn_monthlastday(fn_dateadd(dtout,2,'month'))
                elif időtartam=='félév':
                    dtFirst=dt0.replace(month=(1 + ((dt0.month-1)//6) * 6))
                    dtFirst=dt0.replace(day=1)
                    dtout=fn_dateadd(dtFirst,6*szám,'month')
                    dtout2=fn_monthlastday(fn_dateadd(dtout,5,'month'))
                elif időtartam=='év':
                    dtFirst=datetime(dt0.year,1,1)
                    dtout=fn_dateadd(dtFirst,szám,'year')
                    dtout2=datetime(dtout.year,12,31)
                elif időtartam=='évtized':
                    dtFirst=datetime((dt0.year//10)*10,1,1)
                    dtout=fn_dateadd(dtFirst,szám*10,'year')
                    dtout2=datetime(dtout.year+9,12,31)
                elif időtartam=='évszázad':
                    dtFirst=datetime((dt0.year//100)*100,1,1)
                    dtout=fn_dateadd(dtFirst,szám*100,'year')
                    dtout2=datetime(dtout.year+99,12,31)
                elif időtartam=='évezred':
                    dtFirst=datetime((dty.year//1000)*1000,1,1)
                    dtout=fn_dateadd(dtFirst,szám*1000,'year')
                    dtout2=datetime(dtout.year+999,12,31)

            elif (patternL=='[múltjövő] [évszak]' or                       # múlt nyáron, ezen a télen, jövő tavasszal
                  patternL=='[múltjövő] [időtartam] [évszak]'):           # múlt év nyarán, jövő év tavasszal
                időtartam=''
                if '[időtartam]' in patternL:
                    múltjövő,időtartam,évszak = outvaluesL
                else: 
                    múltjövő,évszak = outvaluesL        # évszak: '3','6','9','12'
            
                if időtartam=='' or időtartam=='év':
                    year=dt0.year
                    if évszak=='12' and dt0.month<6: year-=1    # a tél átnyúlik az évhatáron, ezért nem teljesen egyértelmű az "ezen a télen" ... jelentése

                    if múltjövő=='múlt': year-=1
                    elif múltjövő=='jövő': year+=1

                    dtout=datetime(year,int(évszak),1)
                    dtout2=fn_monthlastday(fn_dateadd(dtout,2,'month'))

            elif (patternL=='[múltjövő] [hónapnév]' or           # jövő májusban, múlt szeptemberben  (nem "következő"/"előző" a jelentése, hanem "jövőre","tavaly")
                  patternL=='[múltjövő] [időtartam] [hónapnév]'):  # jövő év február
                
                időtartam=''
                if '[időtartam]' in patternL:
                    múltjövő,időtartam,honap = outvaluesL
                else: 
                    múltjövő,honap=outvaluesL      
            
                if időtartam=='' or időtartam=='év':
                    year=dt0.year
                    if múltjövő=='múlt': year=year-1
                    elif múltjövő=='jövő': year=year+1

                    n2=int(honap)
                    dtout=datetime(year,n2,1)
                    dtout2=fn_monthlastday(dtout)

            elif patternL=='[múltjövő] [hónapnév] [szám]':     # jővő május 3-án, előző február 4-én  (nem "következő"/"előző" a jelentése, hanem "jövőre","tavaly")
                múltjövő,honap,szám=outvaluesL      
            
                year=dt0.year
                if múltjövő=='múlt': year=year-1
                elif múltjövő=='jövő': year=year+1

                szám_in=invaluesL[2]
                if not endwith(szám_in,'dik|első'):
                    try: dtout=datetime(year,int(honap),szám)
                    except: dtout=None

            elif (patternL=='[múltjövő] [hétnapja]' or                      # "jövő szombaton"
                  patternL=='[múltjövő] [időtartam] [hétnapja]'):           # "múlt hét pénteken"
                időtartam=''
                if '[időtartam]' in patternL:
                    múltjövő,időtartam,hétnapja = outvaluesL
                else: 
                    múltjövő,hétnapja = outvaluesL

                if időtartam=='' or időtartam=='hét':
                    dtMonday=fn_monday(dt0)
                    if múltjövő=='múlt': dtMonday=fn_dateadd(dtMonday,-7) 
                    elif múltjövő=='jövő': dtMonday=fn_dateadd(dtMonday,7) 

                    if hétnapja=='hétvége': 
                        dtout=fn_dateadd(dtMonday,5)    # szombat
                        dtout2=fn_dateadd(dtout,1)
                    else: dtout=fn_dateadd(dtMonday,int(hétnapja)-1)

            elif (patternL=='[dátum] [utánelőtt]'):
                dátum,utánelőtt = outvaluesL
                dt1,dt2 = dátum
                if dt2==None: dt2=dt1

                if utánelőtt=='előtt':
                    dtout=datetime(1,1,1)
                    dtout2=fn_dateadd(dt1,-1)
                elif utánelőtt=='után':
                    dtout=fn_dateadd(dt2,1)
                    dtout2=datetime(9999,12,31)



            elif (patternL=='[dátum] [utánelőtt] [szám] [időtartam]' or   # szombat után két nappal      január 10 előtt 2 héttel
                  patternL=='[szám] [időtartam] [dátum] [utánelőtt]'):    # két nappal március után
                
                if patternL=='[dátum] [utánelőtt] [szám] [időtartam]':
                    dátum,utánelőtt,szám,időtartam = outvaluesL
                elif patternL=='[szám] [időtartam] [dátum] [utánelőtt]':
                    szám,időtartam,dátum,utánelőtt = outvaluesL
            
                dt1,dt2 = dátum
                if dt2==None: dt2=dt1

                if utánelőtt=='után':
                    előjel=1
                    dt0=dt2
                elif utánelőtt=='előtt':
                    előjel=-1
                    dt0=dt1

                szám=int(szám)

                if időtartam=='nap': dtout=fn_dateadd(dt0,szám*előjel)
                elif időtartam=='hét': dtout=fn_dateadd(dt0,7*szám*előjel)   
                elif időtartam=='hónap': dtout=fn_dateadd(dt0,szám*előjel,'month')
                elif időtartam=='negyedév':  dtout=fn_dateadd(dt0,3*szám*előjel,'month')
                elif időtartam=='félév': dtout=fn_dateadd(dt0,6*szám*előjel,'month')
                elif időtartam=='év': dtout=fn_dateadd(dt0,szám*előjel,'year')
                elif időtartam=='évtized':  dtout=fn_dateadd(dt0,szám*10*előjel,'year')
                elif időtartam=='évszázad':  dtout=fn_dateadd(dt0,szám*100*előjel,'year')
                elif időtartam=='évezred':  dtout=fn_dateadd(dtFirst,szám*1000*előjel,'year')

            elif (patternL=='[dátum] [utánielőtti] [szám] [időtartam]' or    # "szombat utáni első hét"  "január 10 előtti 2 nap"
                  patternL=='[dátum] [utánielőtti] [időtartam]'):            # "jövő hét utáni hét"
                if '[szám]' in patternL:
                    dátum,utánielőtti,szám,időtartam = outvaluesL
                    szám_in = invaluesL[2]
                else:
                    dátum,utánielőtti,időtartam = outvaluesL
                    szám = 1
                    szám_in=''

                dt1,dt2 = dátum
                if dt2==None: dt2=dt1

                if utánielőtti=='utáni':
                    előjel=1
                    dt0=dt2
                elif utánielőtti=='előtti':
                    előjel=-1
                    dt0=dt1

                szám=int(szám)
                # sorszám vagy normál szám?
                if sub_sorszam(szám_in):   # szombat utáni első nap,   tavasz előtti utolsó hét  (naptári hét, naptári hónap, ...)
                    if időtartam=='nap': dtout=fn_dateadd(dt0,szám*előjel)
                    elif időtartam=='hét':
                        dtMonday=fn_monday(dt0)             # az aktuális hét első napja
                        dtout=fn_dateadd(dtMonday,7*szám*előjel)   # előző, aktuális, következő
                        dtout2=fn_dateadd(dtout,6)          
                    elif időtartam=='hónap':
                        dtMonthfirst=dt0.replace(day=1)
                        dtout=fn_dateadd(dtMonthfirst,szám*előjel,'month')
                        dtout2=fn_monthlastday(dtout)
                    elif időtartam=='negyedév':
                        dtFirst=dt0.replace(month=(1 + ((dt0.month-1)//3) * 3))
                        dtFirst=dt0.replace(day=1)
                        dtout=fn_dateadd(dtFirst,3*szám*előjel,'month')
                        dtout2=fn_monthlastday(fn_dateadd(dtout,2,'month'))
                    elif időtartam=='félév':
                        dtFirst=dt0.replace(month=(1 + ((dt0.month-1)//6) * 6))
                        dtFirst=dt0.replace(day=1)
                        dtout=fn_dateadd(dtFirst,6*szám*előjel,'month')
                        dtout2=fn_monthlastday(fn_dateadd(dtout,5,'month'))
                    elif időtartam=='év':
                        dtFirst=datetime(dt0.year,1,1)
                        dtout=fn_dateadd(dtFirst,szám*előjel,'year')
                        dtout2=datetime(dtout.year,12,31)
                    elif időtartam=='évtized':
                        dtFirst=datetime((dty.year//10)*10,1,1)
                        dtout=fn_dateadd(dtFirst,szám*10*előjel,'year')
                        dtout2=datetime(dtout.year+9,12,31)
                    elif időtartam=='évszázad':
                        dtFirst=datetime((dty.year//100)*100,1,1)
                        dtout=fn_dateadd(dtFirst,szám*100*előjel,'year')
                        dtout2=datetime(dtout.year+99,12,31)
                    elif időtartam=='évezred':
                        dtFirst=datetime((dty.year//1000)*1000,1,1)
                        dtout=fn_dateadd(dtFirst,szám*1000*előjel,'year')
                        dtout2=datetime(dtout.year+999,12,31)
            
                else:   # szombat utáni 2 nap      január 3 előtti 3 hét
                    if időtartam=='nap': dt1=fn_dateadd(dt0,szám*előjel)
                    elif időtartam=='hét': dt1=fn_dateadd(dt0,7*szám*előjel)   
                    elif időtartam=='hónap': dt1=fn_dateadd(dt0,szám*előjel,'month')
                    elif időtartam=='negyedév':  dt1=fn_dateadd(dt0,3*szám*előjel,'month')
                    elif időtartam=='félév': dt1=fn_dateadd(dt0,6*szám*előjel,'month')
                    elif időtartam=='év': dt1=fn_dateadd(dt0,szám*előjel,'year')
                    elif időtartam=='évtized':  dt1=fn_dateadd(dt0,szám*10*előjel,'year')
                    elif időtartam=='évszázad':  dt1=fn_dateadd(dt0,szám*100*előjel,'year')
                    elif időtartam=='évezred':  dt1=fn_dateadd(dtFirst,szám*1000*előjel,'year')

                    if dt1<dt0:
                        dtout=dt1
                        dtout2=fn_dateadd(dt0,-1)
                    else:
                        dtout=fn_dateadd(dt0,1)
                        dtout2=dt1

            elif (patternL=='[dátum] [utánielőtti] [szám] [hétnapja]' or    # "december 1 utáni második hétvége"
                  patternL=='[dátum] [utánielőtti] [hétnapja]'):
                if '[szám]' in patternL:
                    dátum,utánielőtti,szám,hétnapja = outvaluesL
                    szám_in = invaluesL[2]
                else:
                    dátum,utánielőtti,hétnapja = outvaluesL
                    szám = 1
                    szám_in=''

                dt1,dt2 = dátum
                if dt2==None: dt2=dt1

                szám=int(szám)
                if sub_sorszam(szám_in):   # szombat utáni első hétvége,   karácsony előtti második hétvége
                    length=1
                    if hétnapja=='hétvége':
                        length=2
                        hétnapja='6'
                    if utánielőtti=='utáni':
                        dt0=fn_dateadd(dt2,1)
                        # Az első megfelelő nap az időszakban
                        dtMonday=fn_monday(dt0)
                        dtFirst=fn_dateadd(dtMonday,int(hétnapja)-1)
                        if dtFirst<dt0: dtFirst=fn_dateadd(dtFirst,7)
                        dtout = fn_dateadd(dtFirst,(szám-1)*7)
                        if length==2: dtout2=fn_dateadd(dtout,1)
                    elif utánielőtti=='előtti':
                        dt0=fn_dateadd(dt1,-1)
                        # Az első megfelelő nap az időszakban
                        dtMonday=fn_monday(dt0)
                        dtFirst=fn_dateadd(dtMonday,int(hétnapja)-1)
                        if dtFirst>dt0: dtFirst=fn_dateadd(dtFirst,-7)
                        dtout=fn_dateadd(dtFirst,-(szám-1)*7)
                        if length==2: dtout2=fn_dateadd(dtout,1)



            elif (patternL=='[dátum] [szám] [törtrész]' or    # "2022. első felében", "XIX. század második felében", "január harmadik hamadában",  "múlt hét első felében"
                  patternL=='[dátum] [elejevége]'):         # "2022. elején","február közepén","XIX. század végén", "jövő hét elején"   
            
                dátum=None
                if patternL=='[dátum] [szám] [törtrész]':
                    dátum,szám,törtrész = outvaluesL
                    szám_in = invaluesL[1]
                    if sub_sorszam(szám_in): dátum=None

                elif patternL=='[dátum] [elejevége]':
                    dátum,elejevége = outvaluesL
                    törtrész=3
                    if elejevége=='eleje': szám=1            # első harmad
                    elif elejevége=='közepe': szám=2         # második harmad
                    elif elejevége=='vége': szám=3           # harmadik harmad

                if dátum!=None:
                    dt1,dt2 = dátum
                    if dt2!=None and dt2>dt1:       # időszak szerepel a dátumban
                        oszto=int(törtrész)
                        if szám>=1 and szám<=oszto:
                            unit=fn_daydiff(dt2,dt1)/oszto
                            if szám==oszto:
                                dtout=fn_dateadd(dt2,-fn_round(unit),'day')
                                dtout2=dt2
                            else:
                                dtout=fn_dateadd(dt1,fn_round(unit*(szám-1)),'day')
                                dtout2=fn_dateadd(dtout,fn_round(unit),'day')
                

            elif (patternL=='[dátum] [szám] [időtartam]' or     # "jövő év második félévében", "XIX. század harmadik évtizedében", "február első hetében"
                  patternL=='[dátum] [utolsó] [időtartam]'):    # "jövő év utolsó napján", "XIX. század utolsó évtizedében", "február első hetében"

                bUtolso = vanbenne(patternL,'utolsó')
                patternL=patternL.replace('utolsó','szám')

                dt1=None
                if patternL=='[dátum] [szám] [időtartam]':
                    dátum,szám,időtartam = outvaluesL
                    dt1,dt2 = dátum
                #elif patternL=='[szám] [szám] [időtartam]':
                #    évszám,szám,időtartam = outvaluesL
                #    if évszám>1000 and évszám<2100:
                #        dt1=datetime(évszám,1,1)
                #        dt2=datetime(évszám,12,31)
                #elif patternL=='[hónapnév] [szám] [időtartam]':
                #    hónap,szám,időtartam = outvaluesL
                #    dt1=datetime(dt0.year,int(hónap),1)
                #    dt2=fn_monthlastday(dt1)

                if dt1!=None and dt2!=None and dt2>dt1:       # időszak szerepel a dátumban
                    szám_in = invaluesL[1]
                    időtartam_in=invaluesL[2]
                    if sub_sorszam(szám_in) or bUtolso:
                        if időtartam=='évtized' and (dt1.year % 10)==0 and dt1.month==1 and dt1.day==1:            
                            if bUtolso: szám=(dt2.year-dt1.year)//10 + 1
                            dtout=datetime(dt1.year + 10*(szám-1),1,1)
                            dtout2=datetime(dt1.year + 10*(szám-1) + 9,12,31)
                        elif időtartam=='év' and dt1.month==1 and dt1.day==1:            
                            if bUtolso: szám=(dt2.year-dt1.year)+1
                            dtout=datetime(dt1.year + (szám-1),1,1)
                            dtout2=datetime(dt1.year + (szám-1),12,31)
                        elif időtartam=='félév' and dt1.month==1 and dt1.day==1:            
                            if bUtolso: szám=(dt2.month-dt1.month)//6 + 1
                            dtout=datetime(dt1.year,1+(szám-1)*6,1)
                            dtout2=fn_monthlastday(fn_dateadd(dtout,5,'month'))
                        elif időtartam=='negyedév' and dt1.month==1 and dt1.day==1:         
                            if bUtolso: szám=(dt2.month-dt1.month)//3 + 1
                            dtout=datetime(dt1.year,1+(szám-1)*3,1)
                            dtout2=fn_monthlastday(fn_dateadd(dtout,2,'month'))
                        elif időtartam=='hónap' and dt1.day==1:            
                            if bUtolso: szám=(dt2.month-dt1.month) + 1
                            dtout=datetime(dt1.year,dt1.month + (szám-1),1)
                            dtout2=fn_monthlastday(dtout)
                        elif időtartam=='hét':              
                            dtMonday=fn_monday(dt1)   # az időszak első hetének hétfői napja (általában korábra esik az időszak első napjánál)
                            if bUtolso: szám=fn_daydiff(dt2,dtMonday)//7 + 1
                            dtout=fn_dateadd(dtMonday,(szám-1)*7,'day')
                            dtout2=fn_dateadd(dtout,6,'day')
                        elif időtartam=='nap':              
                            if bUtolso: szám=fn_daydiff(dt2,dt1) + 1
                            dtout=fn_dateadd(dt1,szám-1,'day')
                            dtout2=dtout

                        if dtout!=None:
                            if dtout>dt2: dtout=None     # a kezdődátum nem lehet későbbi az időszaknál
                            else: 
                                if dtout<dt1: dtout=dt1
                                if dtout2>dt2: dtout2=dt2
                                if dtout2<dtout: dtout=None
                    
                    elif beginwith(időtartam_in,'évei|évek'):       # "XIX. század 20-as éveiben"
                        if dt1.year%100==0 and dt1.month==1 and dt1.day==1 and szám%10==0:
                            dtout=datetime(dt1.year + szám,1,1)
                            dtout2=datetime(dt1.year + szám + 9,12,31)

            
            elif (patternL=='[dátum] [szám] [hétnapja]' or     # jövő hónap első hétfőjén"
                  patternL=='[dátum] [utolsó] [hétnapja]'):   # "február utolsó hétvégéjén"

                bUtolso = vanbenne(patternL,'utolsó')
                patternL=patternL.replace('utolsó','szám')

                dt1=None
                if patternL=='[dátum] [szám] [hétnapja]':
                    dátum,szám,hétnapja = outvaluesL
                    dt1,dt2 = dátum
                elif patternL=='[szám] [szám] [hétnapja]':
                    évszám,szám,hétnapja = outvaluesL
                    if évszám>1000 and évszám<2100:
                        dt1=datetime(évszám,1,1)
                        dt2=datetime(évszám,12,31)
                elif patternL=='[hónapnév] [szám] [hétnapja]':
                    hónap,szám,hétnapja = outvaluesL
                    dt1=datetime(dt0.year,int(hónap),1)
                    dt2=fn_monthlastday(dt1)

                if dt1!=None and dt2!=None and dt2>dt1:       # időszak szerepel a dátumban
                    szám_in = invaluesL[1]
                    if sub_sorszam(szám_in) or bUtolso:
                        length=1
                        if hétnapja=='hétvége':
                            length=2
                            hétnapja='6'
                        # Az első megfelelő nap az időszakban
                        dtFirst = fn_dateadd(dt1, (7 + int(hétnapja) - (dt1.weekday()+1)) % 7)
                        if bUtolso: szám=fn_daydiff(dt2,dtFirst)//7 + 1

                        dtout = fn_dateadd(dtFirst,(szám-1)*7)
                        dtout2=fn_dateadd(dtout,length-1)

                        if dtout!=None:
                            if dtout>dt2: dtout=None     # a kezdődátum nem lehet későbbi az időszaknál
                            else: 
                                if dtout<dt1: dtout=dt1
                                if dtout2>dt2: dtout2=dt2
                                if dtout2<dtout: dtout=None

        
        # Második kör:  "[dátum] ..." mintákban és önállóan is előforduló több szavas utózmányok
        elif nCycle==2:
            if patternL=='[szám] [időtartam]':            # XIX. században, második félévben, utolsó negyedévben, 12. héten, 120. napon
                szám,időtartam = outvaluesL

                szám_in = invaluesL[0]
                időtartam_in=invaluesL[1]

                # [sorszám] [időtartam]
                if sub_sorszam(szám_in):          # csak sorszám esetén fordítható le dátumra (egy kivétel lejjebb: 2022 évben)
                    if időtartam=='évtized':       # aktuális évszázadban
                        if szám>=1 or szám<=10:
                            year=(dt0.year//100) * 100
                            dtout=datetime(year + (szám-1)*10,1,1)
                            dtout2=datetime(year + (szám-1)*10 + 9,12,31)
                    elif időtartam=='év':            # időszámítás kezdete óta
                        if szám>=1 or szám<=2100:
                            dtout=datetime(szám,1,1)
                            dtout2=datetime(szám,12,31)
                    elif időtartam=='félév':            # aktuális évben
                        if szám==1 or szám==2:
                            dtout=datetime(dt0.year,1+(szám-1)*6,1)
                            dtout2=fn_monthlastday(fn_dateadd(dtout,5,'month'))
                    elif időtartam=='negyedév':         # aktuális évben
                        if szám>=1 and szám<=4:
                            dtout=datetime(dt0.year,1+(szám-1)*3,1)
                            dtout2=fn_monthlastday(fn_dateadd(dtout,2,'month'))
                    elif időtartam=='hónap':            # aktuális évben
                        if szám>=1 and szám<=12:
                            dtout=datetime(dt0.year,szám,1)
                            dtout2=fn_monthlastday(dtout)
                    elif időtartam=='hét':              # aktuális évben
                        if szám>=1 and szám<=53:
                            dtMonday=fn_monday(datetime(dt0.year,1,1))   # az év első hetének hétfői napja (általában az előző év végére esik)
                            dtout=fn_dateadd(dtMonday,(szám-1)*7,'day')
                            dtout2=fn_dateadd(dtout,6,'day')
                            if dtout.year<dt0.year: dtout=datetime(dt0.year,1,1)
                            if dtout2.year>dt0.year: dtout2=datetime(dt0.year,12,31)
                            if dtout>dtout2: dtout=None         # szám=53 esetén fordulhat elő
                    elif időtartam=='nap':              # aktuális évben
                        if szám>=1 and szám<=366:
                            dtout=fn_dateadd(datetime(dt0.year,1,1),szám-1,'day')
                            if dtout.year>dt0.year: dtout=None
                


        if dtout==None: return None
        else: return dtout,dtout2


    def sub_findpattern(pattern,invalues,outvalues,nCycle):
        # ciklus az ablakméretre:  összes szó, összes-1 szó, összes-2 szó, ...
        patternwords=pattern.split()
        nWords=len(patternwords)
        # invalues és outvalues összehangolása a patternwords-szel (nem azonos az elemszámuk)
        invalues_sync=[None]*nWords
        outvalues_sync=[None]*nWords
        i_value=0
        for i,patternword in enumerate(patternwords):
            if patternword[0]=='[':
                invalues_sync[i]=invalues[i_value]
                outvalues_sync[i]=outvalues[i_value]
                i_value+=1
        for nWindowLen in reversed(range(nWords+1)):   
            # ablak-pásztázási ciklus
            for nWindowStart in range(nWords-nWindowLen+1):
                # patternL,invaluesL,outvaluesL beállítása
                patternL=' '.join(patternwords[nWindowStart:nWindowStart+nWindowLen])
                invaluesL=[]
                for value in invalues_sync[nWindowStart:nWindowStart+nWindowLen]:
                    if value: invaluesL.append(value)    # a None értékek nem kellenek
                outvaluesL=[]
                for value in outvalues_sync[nWindowStart:nWindowStart+nWindowLen]:
                    if value: outvaluesL.append(value)   # a None értékek nem kellenek
                # beazonosítható-e dátumként
                dates=sub_patterns(patternL,invaluesL,outvaluesL,nCycle,dt0)
                if dates:
                    pattern=' '.join([*patternwords[:nWindowStart],'[dátum]',*patternwords[nWindowStart+nWindowLen:]])
                    pattern=trim(pattern)
                    invalues_sync=[*invalues_sync[:nWindowStart],patternL,*invalues_sync[nWindowStart+nWindowLen:]]
                    outvalues_sync=[*outvalues_sync[:nWindowStart],dates,*outvalues_sync[nWindowStart+nWindowLen:]]
                    invalues=[]
                    for value in invalues_sync:
                        if value: invalues.append(value)    # a None értékek nem kellenek
                    outvalues=[]
                    for value in outvalues_sync:
                        if value: outvalues.append(value)   # a None értékek nem kellenek
                    return (pattern,invalues,outvalues)
        return None

    
    nCycle=1        # két kör lesz
    while True:
        result=sub_findpattern(pattern,invalues,outvalues,nCycle)
        # Ha nincs további beazonosítás
        if result==None:
            if nCycle==1:
                nCycle=2
            elif nCycle==2:
                # Megnézendő, hogy volt-e sikeres dátumbeazonosítás (az első lesz a return)
                dátumok=[]
                nValueIndex=-1
                patternwords=pattern.split()
                for patternword in patternwords:
                    if patternword[0]=='[': nValueIndex+=1
                    if patternword=='[dátum]':
                        date1,date2 = outvalues[nValueIndex]
                        if date2 and date2!=date1: result=date1.strftime('%Y.%m.%d') + '-' + date2.strftime('%Y.%m.%d')
                        else: result=date1.strftime('%Y.%m.%d')
                        if outtype=='first+': result=result + '    pattern: ' + pattern + '  outvalues: ' + str(outvalues)
                        if outtype in ['first','first+']:
                            return result
                        dátumok.append(result)
                if len(dátumok)>0:
                    return ','.join(dátumok)

                # sikertelen  (egyetlen dátum sem volt a szövegben)
                if outtype=='first':  result=''
                elif outtype=='first+':  result='sikertelen     pattern: ' + pattern + '  outvalues: ' + str(outvalues)
                return result

        else:
            pattern,invalues,outvalues = result
            # Ha a teljes szöveget sikerült dátumként beazonosítani
            if pattern=='[dátum]': 
                date1,date2 = outvalues[0]
                if date2 and date2!=date1: result=date1.strftime('%Y.%m.%d') + '-' + date2.strftime('%Y.%m.%d')
                else: result=date1.strftime('%Y.%m.%d')
                if outtype=='first+': result=result + '    pattern: ' + pattern + '  outvalues: ' + str(outvalues)
                return result
            # egyébként újrakezdi a ciklust

lookup_text2dateG={
    'hétfő|h.':'hétnapja,1',
    'kedd|k.':'hétnapja,2',
    'szerd|sze.|szer.':'hétnapja,3',
    'csüt|cs.':'hétnapja,4',
    'pént|p.':'hétnapja,5',
    'szomb|szo.':'hétnapja,6',
    'vasár|vas.|v.':'hétnapja,7',
    'hétvég':'hétnapja,hétvége',

    'január|jan.':'hónapnév,1',
    'február|febr.':'hónapnév,2',
    'március|márc.':'hónapnév,3',
    'április|ápr.':'hónapnév,4',
    'május|máj.':'hónapnév,5',
    'június|jún.|júni.':'hónapnév,6',
    'július|júl.|júli.':'hónapnév,7',
    'augusztus|aug.':'hónapnév,8',
    'szeptember|szept.':'hónapnév,9',
    'október|okt.':'hónapnév,10',
    'november|nov.':'hónapnév,11',
    'december|dec.':'hónapnév,12',

    'ma.|mai.|má':'maholnap,0',
    'holnap':'maholnap,1',
    'holnapután':'maholnap,2',
    'tegnap':'maholnap,-1',
    'tegnapelőtt':'maholnap,-2',

    'idén':'szám,' + str(datetime.now().year),
    'jövőre':'szám,' + str(datetime.now().year+1),
    'tavaly':'szám,' + str(datetime.now().year-1),
    'tavalyelőtt':'szám,' + str(datetime.now().year-2),

    'évszázad|század|szd.':'időtartam,évszázad',
    'évtized':'időtartam,évtized',
    'év.|éve.|évek|évei|évtől|évig|évben|évvel|évé|évre':'időtartam,év',
    'félév':'időtartam,félév',
    'negyedév':'időtartam,negyedév',
    'hónap|hó.':'időtartam,hónap',
    'hét|hete.|heté':'időtartam,hét',
    'nap':'időtartam,nap',

    'tavasz|tavasszal':'évszak,3',
    'nyár|nyarán':'évszak,6',
    'ősz|ősszel':'évszak,9',
    'tél|telén':'évszak,12',

    'múlt|elmúlt|előző|legutóbbi':'múltjövő,múlt',
    'jövő|következő|legközelebbi':'múltjövő,jövő',
    'most|ezen|idei|aktuális|e.|ebben':'múltjövő,most',

    'múlva|ezután|azután|később|rá.|követően':'múlvaezelőtt,múlva',
    'ezelőtt|azelőtt|korábban|megelőzően':'múlvaezelőtt,ezelőtt',

    'után':'utánelőtt,után',
    'előtt':'utánelőtt,előtt',

    'utáni|követő|kezdve':'utánielőtti,utáni',
    'előtti|megelőző':'utánielőtti,előtti',

    'utolsó': 'utolsó,utolsó',
    'utolsó előtti':'utolsó,utolsóelőtti',

    'fele.|felében|felétől|feléig':'törtrész,2',
    'harmada|harmadá':'törtrész,3',
    'negyede|negyedé':'törtrész,4',

    'elej|kezdőnap':'elejevége,eleje',
    'közepe.|közepé':'elejevége,közepe',
    'vége.|végé|zárónap':'elejevége,vége',

    'karácsony':'évnapja,karácsony',
    'szenteste':'évnapja,szenteste',
    'szilveszter':'évnapja,szilveszter',
    'újév':'évnapja,újév',
    'húsvét':'évnapja,húsvét',
    'pünkösd':'évnapja,pünkösd',
    'halottak nap':'évnapja,halottaknapja',
    'mindenszentek':'évnapja,mindenszentek',


    'a.|az.|és.|ezt.|azt.|tól.|től.|ig.|áig.|éig.|i.|ai.|ei.|án.|én.|jén.|jei.|ji.|tól.|től.|as.|es.':'stopword'
    }


