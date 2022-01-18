import ezdate as d

from datetime import datetime,date,timedelta

d.text2date('Kérek egy kimutatást 2020 második féléve harmadik hetének közepéről. A nyári hónapokban lényegesen nagyobb volt a forgalom, ' +
            'mint az előző években. Ha ugyanez a trend érvényesül, akkor idén nyáron még nagyobb forgalommal kell számolnunk.',outtype='all')



d.text2date('2022 utáni 3 év',outtype='first+')     
d.text2date('január 16 előtti első hétvége',outtype='first+')     
d.text2date('jövő hónap első hétfőjén',outtype='first+')     


d.text2date("két évvel ezelőtt 10-én",outtype='first+')     
d.text2date("jövő hónap harmadikán",outtype='first+')     
d.text2date("három évvel ezelőtt decemberben",outtype='first+')     
d.text2date("március hónapban 5-én",outtype='first+')     

d.text2date("2022 előtt",outtype='first+')     
d.text2date("péntek előtt",outtype='first+')     
d.text2date('múlt év előtt',outtype='first+')     
d.text2date('jövő hónap után',outtype='first+')     
d.text2date('holnap után',outtype='first+')     



d.text2date("XIX. század 20-as éveiben",outtype='first+')     
d.text2date("előző évszázad 20-as éveiben",outtype='first+')     
d.text2date('1900-as évek',outtype='first+')     
d.text2date('1990-es évek',outtype='first+')     
d.text2date('2020-as évek',outtype='first+')     
d.text2date("'20-as évek",outtype='first+')     
d.text2date("huszas évek",outtype='first+')     
d.text2date("90-es évek",outtype='first+')     
d.text2date("30-as évek",outtype='first+')     

d.text2date('két hónappal ezelőtt harmincadikán',outtype='first+')     
d.text2date('három évvel ezelőtt decemberben',outtype='first+')
d.text2date('három héttel ezelőtt szombaton',outtype='first+')

# [szám] [időtartam] [múlvaezelőtt] [hónapnév]
# [szám] [időtartam] [múlvaezelőtt] [hétnapja]

d.text2date('három éve decemberben',outtype='first+')
d.text2date('két hónapja hatodikán',outtype='first+')
d.text2date('három hete pénteken',outtype='first+')

d.text2date('három évvel ezelőtt december 5-én',outtype='first+')
# [szám] [időtartam] [múlvaezelőtt] [hónapnév] [szám]

d.text2date('két év múlva decemberben',outtype='first+')
d.text2date('három hete pénteken',outtype='first+')

d.text2date('két napja',outtype='first+')



d.text2date('péntek előtt 3 héttel',outtype='first+')
d.text2date('mától kezdve egy hét',outtype='first+')
d.text2date('öt nappal március után',outtype='first+')
d.text2date('jövő május második hetében',outtype='first+')
d.text2date('jövő hétvége utáni második nap',outtype='first+')
d.text2date('2023 második hónapjának harmadik hete',outtype='first+')

h.fn_round(2.34)
'01234'.isdigit()
dt1=datetime.now()
dt2=d.fn_dateadd(dt1,4)
d.fn_daydiff(dt2,dt1)
((dt2-dt1)/3) / timedelta(days=1)


h.endwith('2.a',r'\.a')
dt1=datetime(2022,2,1)
dt1.weekday()
d.fn_dateadd(dt1, (7 + (dt1.weekday()+1) - int(3)) % 7)

15 % 4
2010 % 10

h.vanbenne('sokadik másodikán sok','kán|diká')
samples='so|diká'
m=re.search(r'(' + samples + ')','sokadik másodikán sok')
m.group()

(datetime(2022,3,31)-datetime(2022,1,1))/timedelta(days=1)

8.4//7


d_annotate('hétvége utáni nap',config.lookup_text2dateG,True)

config.lookup_text2dateG

h.kodto('3','1:egy//2:kettő')


tesztesetek=['ma',
       'február 4-én','másodikán','március elsején','május hónapban',
       'tavaly január 10-én','tavaly februárban','jövő nyáron','jövő május 12-én','jövő év tavaszán',
       'hétfőn','jövő pénteken','hétvégén','múlt kedden','jövő hét szombaton',
       '2015-2018','2015 és 2022 között','2022 előtt',
       'MMXXI. II. hónapban','XIX. században',"'90-es években",'2010-es években','1900-as években','múlt század közepén',
       'idén','jövőre','jövő évben','tavaly','múlt évben','elmúlt évben','előző hónapban','következő hónapban','múlt félévben',
       'két év múlva','három évre rá','4 hónappal ezelőtt',
       'jövő hónap harmadikán','e hónapban','múlt hónap közepén','idei év végén','következő tavasz elején','következő év szeptember közepén',
       'második negyedévben','most szerdán','múlt év második negyedéve előtt',
       'az év első hetében','2023 második félév harmadik hetének közepén',
       'két nappal ezelőtt','10 hét múlva','3 éve','öt napja',
       'három évvel ezelőtt decemberben','két hét múlva pénteken','három hete hétfőn','két hónappal ezután 5-én','két éve januárban',
       'múlt péntek előtt két héttel','jövő hétvége után két nappal','december 1 előtt 12 nappal',
       'hétvége utáni második nap','múlt hét péntek előtti 2 hét','2022 utáni 3 év',
       'karácsonykor','jövő karácsony utáni második hétvégén','tavaly szilveszter előtti szerdán',
       'most','mai napon','tegnap','tegnapelőtt','tegnap előtt','holnap','holnapután','holnap után',
       '2022.01.02','2022-01-03','20220104','2022 01 02','0105','02 03','2022. január 10','2022. II.hó 3.'
       ]
for teszt in tesztesetek:
    print('"' + teszt + '"    ' + d.text2date(teszt))




d_annotate('holnap után két nappal',config.lookup_text2dateG,True)


