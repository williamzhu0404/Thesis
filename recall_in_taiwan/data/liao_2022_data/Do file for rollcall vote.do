***Recoding of variables***
tab order
lab define a 5"5th term" 6"6th term" 7"7th term" 8"8th term"
lab val order a
tab order

tab edu
recode edu (1 2 3 4=1)(5=2)(6=3), gen(edu3)
lab define b 1"high school and below" 2"undergraduate" 3"graduate"
lab val edu3 b
tab edu3

tab gender
lab define c 1"male" 2"female"
lab val gender c
tab gender

tab category
recode category (1 5=1)(2=2)(3 4 =3), gen(tier3)
lab define d 1"local district" 2"aboriginal" 3"PR-list"
lab val tier3 d
tab tier3

recode category (1 5 2=1)(3 4 =2), gen(tier2)
lab define e 1"local district" 2"PR-list"
lab val tier2 e
tab tier2
label variable tier2 "Electoral Tier 2: Elected or PR"

recode category (1 5 =1)(3 4 =2)(2=.), gen(tier2n)
lab val tier2n e
tab tier2n, gen(dtier2n)
label variable tier2n "Electoral Tiers: Local or PR"

lab define f 0"Not local faction" 1"local faction"
lab val faction f
tab faction

recode party(1=1)(2=2)(4=3)(8=4)(else=.), gen(party4)
lab define g 1"KMT" 2"DPP" 3"PFP" 4"TSU"
lab val party4 g
tab party4n

lab define h 1"Yes" 0"No"
lab val lcpolitics2 h
tab lcpolitics2

recode csm(else=0)(5=1), gen(csm2)
lab define i 0"Inclusive" 1"Inclusive"
lab val csm2 i
label variable csm2 "Inclusive or Exclusive CSM"

recode order(5 6=0)(7 8=1), gen(reform)
lab define j 0"Before Electoral Reform" 1"After Electoral Reform"
lab val reform j
lab variable reform "Before or After Reform"

* Electoral Tiers
gen sntv=1 if reform==0 & dtier2n1==1
replace sntv=0 if sntv==.

gen sntvlowdm=0
replace sntvlowdm=1 if sntv==1 & con_size<8

gen sntvhighdm=0
replace sntvhighdm=1 if sntv==1 & con_size>7

gen aboriginal=0
replace aboriginal=1 if tier3==2 

generate pluralitysmd=0
replace pluralitysmd=1 if reform==1 & dtier2n1==1

gen prlinked=0
replace prlinked=1 if reform==0 & dtier2n2==1

generate prindep=0
replace prindep=1 if reform==1 & dtier2n2==1

tab con_soze
gen lndm=ln(con_size)
tab lndm
lab variable lndm "Log of DM"

***Analysis of Deviation Rates***
** If you cannot run asdoc, install and set the directory.
ssc install asdoc
cd c:/results

** voting against & abstention
reg abstain2 sntvlowdm sntvhighdm aboriginal          i.csm2             i.party4 i.edu3 i.gender c.term c.chairtime i.faction i.lcpolitics2 i.order if reform==0, cluster(personid)
reg abstain2 pluralitysmd         aboriginal                             i.party4 i.edu3 i.gender c.term c.chairtime i.faction i.lcpolitics2 i.order if reform==1, cluster(personid)
reg abstain2 sntv pluralitysmd    aboriginal prlinked        i.govmember i.party4 i.edu3 i.gender c.term c.chairtime i.faction i.lcpolitics2 i.order,              cluster(personid)

margin dtier31, at (reform=(0 1) dtier32=0) atmeans pwcompare l(95)

asdoc reg abstain2 sntvlowdm sntvhighdm aboriginal          i.csm2                   i.party4 i.edu3 i.gender c.term c.chairtime i.faction i.lcpolitics2 i.order if reform==0, cluster(personid) replace nest cnames(Pre-reform) save(abstain)
asdoc reg abstain2 pluralitysmd         aboriginal                                   i.party4 i.edu3 i.gender c.term c.chairtime i.faction i.lcpolitics2 i.order if reform==1, cluster(personid) cnames(Post-reform) nest save(abstain) 
asdoc reg abstain2 sntv pluralitysmd    aboriginal prlinked              i.govmember i.party4 i.edu3 i.gender c.term c.chairtime i.faction i.lcpolitics2 i.order,              cluster(personid) cnames(All Periods) nest save(abstain)


**absence rate 
reg absence sntvlowdm sntvhighdm aboriginal           i.csm2             i.party4 i.edu3 i.gender c.term c.chairtime i.faction i.lcpolitics2 i.order if reform==0, cluster(personid)
reg absence pluralitysmd         aboriginal                              i.party4 i.edu3 i.gender c.term c.chairtime i.faction i.lcpolitics2 i.order if reform==1, cluster(personid)
reg absence sntv pluralitysmd    aboriginal prlinked         i.govmember i.party4 i.edu3 i.gender c.term c.chairtime i.faction i.lcpolitics2 i.order,              cluster(personid)

margin dtier31, at (reform=(0 1) dtier32=0) atmeans pwcompare l(95)

asdoc reg absence sntvlowdm sntvhighdm aboriginal          i.csm2             i.party4 i.edu3 i.gender c.term c.chairtime i.faction i.lcpolitics2 i.order if reform==0, cluster(personid) replace nest cnames(Pre-reform) save(absence)
asdoc reg absence pluralitysmd         aboriginal                             i.party4 i.edu3 i.gender c.term c.chairtime i.faction i.lcpolitics2 i.order if reform==1, cluster(personid) cnames(Post-reform) nest save(absence)
asdoc reg absence sntv pluralitysmd    aboriginal prlinked        i.govmember i.party4 i.edu3 i.gender c.term c.chairtime i.faction i.lcpolitics2 i.order,              cluster(personid) cnames(All Periods) nest save(absence)

*margine of periods
reg abstain2 i.sntv pluralitysmd aboriginal i.prlinked i.govmember i.party4 i.edu3 i.gender c.term c.chairtime i.faction i.lcpolitics2 i.order, cluster(mpid)
margin order,  pwcompare l(95)

*** Analysis of local MPs only*** 

**Defection Rate**
reg abstain2          i.party4 i.edu3 i.gender c.term c.chairtime i.faction i.lcpolitics2 lndm  elecsecurity  i.order if reform==0 & tier3==1, cluster(personid) 
reg abstain2          i.party4 i.edu3 i.gender c.term c.chairtime i.faction i.lcpolitics2       elecsecurity  i.order if reform==1 & tier3==1, cluster(personid) 

asdoc reg abstain2    i.party4 i.edu3 i.gender c.term c.chairtime i.faction i.lcpolitics2 lndm  elecsecurity i.order if reform==0 & tier3==1, cluster(personid) replace nest cnames(Pre-reform 1) save(rc_local)
asdoc reg abstain2    i.party4 i.edu3 i.gender c.term c.chairtime i.faction i.lcpolitics2       elecsecurity i.order if reform==1 & tier3==1, cluster(personid) cnames(Post-reform 1) nest save(rc_local)

**Absence Rate**
reg absence           i.party4 i.edu3 i.gender c.term c.chairtime i.faction i.lcpolitics2 lndm elecsecurity i.order if reform==0 & tier3==1, cluster(personid)
reg absence           i.party4 i.edu3 i.gender c.term c.chairtime i.faction i.lcpolitics2      elecsecurity i.order if reform==1 & tier3==1, cluster(personid)

asdoc reg absence     i.party4 i.edu3 i.gender c.term c.chairtime i.faction i.lcpolitics2 lndm elecsecurity i.order if reform==0  & tier3==1, cluster(personid) replace nest cnames(Pre-reform 1) save(absence_local)
asdoc reg absence     i.party4 i.edu3 i.gender c.term c.chairtime i.faction i.lcpolitics2      elecsecurity i.order if reform==1  & tier3==1, cluster(personid) cnames(Post-reform) nest save(absence_local)


