from ezdate as d


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


input('\nBezárás: enter')


