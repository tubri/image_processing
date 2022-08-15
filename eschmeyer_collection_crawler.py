import json
import random
import re
import time
import urllib
from bs4 import BeautifulSoup
import xlwt
import requests

# save to excel
from fake_useragent import UserAgent

#institution_string = "[MLS],ABE,ACAP,AFAQ,AFDZ,AFY,AHF,AI,AIM,AKPM,AL,ALA,AMCK,AMG,AMNH,AMS,ANC,ANDES,ANIRO,ANSP,APFS/ZSI/P,APM,APRC,ARC,ARI,ASB,ASIO,ASIZB,ASIZP,ASIZT,ASK,ASU,ASUM,AUM,AZUSC,BAH,BAMZ,BCFH,BCPM,BCU,BEKU,BELUM,BFRIRS,BFSU,BFU,BIK,BIOONE,BIP,BIRCUM,BKNU,BLIH,BLIP,BLUZ,BM,BMAM,BMNH,BMRI,BMVU,BNHM,BNHS,BNHS FWF,BOC,BPBM,BRT-I,BSKU,BSMP,BSNH,BSRM,BU,BUI,BVIEER,BYU,BZS,CAC-CDMB,CAGC,CAHUP,CAM,CAP,CAR,CAS,CAS-GVF,CAS-IU,CAS-SU,CAUSC,CBC,CBD,CBF,CBM,CBS,CBSIZA,CCB,CCML,CEMBP,CEPFL,CFA-IC,CFB,CFM_IEOMA,CGE,CHIFF,CIACOL,CIAD,CIARI,CIB,CIBM,CICCA,CICCAA,CICIB-UAEM,CICIMAR,CIFE,CIFI,CI-FML,CIFRI,CIMAR,CIP,CIPA,CIPBV,CIRA-UTB,CIRUV,CIUA,CIUFES,CI-UFES,CIUNB,CIZ,CM,CMA,CMC,CMFRI,CMFRI GB,CMIZASDPRK,CMK,CMLRE,CMNFI,CMNH,CMNH-ZF,CMS,CMV,CNGZNU,CNHM,CNP-IBUNAM,CNR,CNRO,CNU,CNUC,CNUCK,CPUCLA,CP-UCO,CPUFMA,CPUFMT,CPUM,CPZM,CRDOA,CRG-SAC,CRH,CRHU,CRRHA,CRS/ZSI,CSBD,CSIRO,CSU,CSULB,CUB,CUBK,CUKMNH,CUMV,CUMZ,CUP,CU-RY,CUSAT,CWNU,CZACC,CZCEN,CZUT-IC,DAVK,DBCUCH,DBFFEUCS,DBLU,DBSCNU,DDUGU,DFI,DFV,DHFRI,DHISUB,DHMB,DMM,DOS,DSZ,DU,DUM,DVZUT,DZ,DZAUT,DZSASP,DZSJRP,DZUFMG,DZUFRGS,DZUH,DZVU,EAMFRO,EAWAG,EBFS,EBMC,EBMTV,EBRC/ZSI,EBRG,ECOCH,ECO-CH,ECOSC,ECSFI,EDULP,EEBP,EKU,EKZNW,ENCB,ENCB-IPN,EPN,ERS/ZSI,ESFM,EUB,EWNHM,F/GUZ,FACEN,FACQR,FAK,FAKOU,FAKU,FAMB,FAQ,FAQB,FAUMM,FBD,FBGN-SAU,FBQ,FBRC/ZSI,FCFUK,FCLR,FCRM,FCSCNU,FCSNU,FDNR,FEMBSNR,FESC,FFM,FFNU,FFR,FFSUC,FLBS,FM,FMIB,FML,FMNH,FMRI,FMS/CASMD,FMUL,FNU,FOSJ,FRC,FRCL,FRDFM,FRI,FRIGL,FRIHP,FRLM,FRSKU,FSBC,FSFL,FSFRL,FSI,FSIU,FSJF,FSKU,FSM,FSU,FTRC/FSRS,FUMT,GAFS,GCM,GCRL,GCRLM,GDOU,GIF,GMBL,GMNGZ,GMNH,GNHM,GNHNA,GNM,GNMG,GNMGG,GNUZ,GP,GRWQ,GTEU,GUIC,GUMF,GUZ,GVF,GXIF,GZIG,HACW,HAF,HBOM,HCMR,HDBI,HHNNR,HIFIRE,HKFRS,HLM,HMG,HML,HNHU,HNU,HNUE,HRA,HSU,HU,HUIC,HUJ,HUMZ,HVMSH,HZM,IAA,IADIZA,IAMC-CMR,IAPG,IAVHP,IAVH-P,IBA,IBAB,IBAUNC,IBH,IBIGEO,IBRP,IBSD,IBTS,IBUNAM,ICDD,ICM,ICMN,ICNMHN,ICN-MHN,ICNMNH,IDSM,IEBMT,IEBR,IEOV,IEPA,IFAN,IFC-ESUF,IFI,IFP,IFREDI,IFREMER,IHASW,IHB,IHCAS,IIAP,IIPB,IKC,ILPLA,IMARPE,IMCN,IMNH,IMNRF-UT,INALI,INHS,INIBP,INIDEP,INIP,INP,INPA,INVEMAR,IO,IOCAS,IOH,IOI,IOM,IOP,IOPM,IORD,IOS,IPMB,IPN,IPNM,IPPS,IRET,IRSM,IRSMNB,IRSNB,ISAM MB,ISBB,ISBN,ISC,ISER,ISH,ISNM,ISTPM,ISU,ISZZ,IU,IUQ,IUSHM,IZA,IZAB,IZAC,IZPAN,IZUA,IZUC,IZUCS,JAMSTEC,JFBM,JNBR,JNC,JNMP,JNU,JPC,JS,JUDES/FSD,KAUM-I,KAUMM,KBF-I,KFRI,KFRS,KFUPM,KHMM,KIEL,KIFB,KIU,KIZ,KMAG,KMPC,KPM,KPM-NI,KSHS,KU,KUFOS,KUMF,KUN,LACM,LACMNH,LaGEEvo,LARREC,LARRI,LBM,LBN,LBP,LBRC,LBRP,LEMUR,LESCI,LFBKU,LFRH,LGEP,LHC,LHUC,LIA,LIAIP,LICPP,LIG,LIOP.UFAM,LIPI,LIRP,LISDEBE,LJG,LLFS-UCH,LMH,LMM,LNEP-UFF,LNHNY,LNHSM,LOC-DBEZ-UFR,LON,LON NCIP,LS,LSJUM,LSL,LSUMZ,LU,LV,LZUT,MAC,MAC-APU,MACLPI,MACN,MACN-ICH,MAC-PAY,MAD,MAK,MAMU,MAN,MAPA,MARC/ZSI,MARNM,MB,MB-HUNE,MBLUZ,MBML,MBSH,MBUCV,MCCDRS,MCCI,MCLSBB,MCM,MCMI,MCMK,MCN,MCNCH,MCNCT,MCNG,MCNI,MCNIP,MCP,MCSBCN,MCSNH,MCT-PUCRS,MCVR,MCZ,MCZH,MCZR,MD,MDZAU,MECN,MEPAN,MEPN,MFA,MFA-ZV,MFLB,MFRU,MG,MGAB,MGH,MGHNL,MGHSJ,MHNCI,MHNG,MHNI,MHNIB,MHNJP,MHNL,MHNLR,MHNLS,MHNM,MHNMM,MHNN,MHNNICE,MHNP,MHNRUN,MHNUC,MHNUNC,MHN-UNC,MHNV,MHV,MIKU,MIMB,MJAS,MKC,ML,MLP,MLS,MLS (2),MM,MMB,MMF,MMG,MMGPE,MMM,MMNHN,MMNHS,MMNS,MMPEAA,MMSU,MMTT,MMUS,MN,MNCN,MNH,MNHA,MNHLS,MNHN,MNHN (2),MNHNBA,MNHNC,MNHNCH,MNHNLU,MNHNM,MNHNP,MNHNSD,MNHPA,MNHRE,MNHSC,MNHV,MNHW,MNKHNU,MNKP,MNKRNU,MNM,MNRJ,MNS,MNSB,MNUL,MNW,MOBR-EDIMAY,MOCH,MOFUNG,MOFURG,MOM,MOSU,MOVI,MPEG,MPM,MPMJ,MPUJ,MRAC,MRSNT,MSI,MSINR,MSLH,MSM,MSNG,MSNM,MSNT,MSNVE,MSNVR,MSR,MSSA,MSTFM,MSUI,MSUM,MSUMNH,MTD,MTH,MTKD,MTUF,MU,MUFM,MUFS,MUI,MUMF,MUNHINA,MUS,MUSM,MUSNM,MUT,MUVS-V,MUZFV,MVZ,MW,MZB,MZ-FISBUK,MZFS,MZGZ,MZH,MZICT,MZMLC,MZN,MZP,MZPA,MZS,MZSP,MZUABCS,MZUB,MZUC,MZUEL,MZUF,MZUFBA,MZUL,MZULG,MZUSP,MZUT,MZUTH,MZUVN,MZYU,NARA,NBC,NBFGR,NBU,NCIP,NCIV,NCMR,NCSM,NERC,NGIL,NHCY,NHGC,NHM,NHMB,NHMG,NHMGZAR,NHMI,NHMM,NHMR,NHRM,NHVUIC,NICA,NIFI,NIG,NIGL,NIGLAS,NIISM,NIWA,NIZBN,NKMC,NLU,NMB,NMBA,NMBE,NMBZ,NMC,NMCI,NMFSH,NMH,NMI,NMK,NML,NMMBP,NMMH,NMMST,NMNHI,NMNHS,NMNHU,NMNW,NMNZ,NMP,NMP/NPB,NMS,NMSA,NMSL,NMSMP,NMSZ,NMV,NMW,NNU,NOI,NPIB,NPM,NPRI,NPTS,NRIBAS,NRM,NRS/ZSI,NSMT,NSYSU,NSYU,NTM,NTMP,NTOU,NTUM,NULFO,NUMZ,NUOL,NUP,NUPEC,NUPELIA,NUSMBS,NWIPB,NYSM,NYZS,NZCS,NZMC,NZOI,OBBFUL,OCA,OCF-P,OCM,OHG,OIM,OKU,OLL,OM,OMMSFC,OMNH,ONHM,ONUZM,OPM,ORI,ORIT,ORSTOM,OS,OSM,OSU,OSUM,OSUO,OSUS,OUC,OUC_FEL,OUM,PEM,PHGM,PKU,PMBC,PMF,PMJ,PMNH,PMR,PNGM,PNI,PNM,PPSIO,PRFRI,PSMC,PSU,PSUZC,PU,PUCMF,PZC,QAMS,QM,QMB,QVM,QVMS,RBCM,RC/RGCA,RCSE,RCSHC,RCSL,RGUMF,RHL,RHLCY,RHS,RIAH,RIFFL,RLIKU,RMBR,RMNH,RNHG,RNLK,ROM,RUSI,RUSM,SACON,SADC/GEF,SAHIMEL,SAIAB,SAM,SAMA,SASM,SATYABHAMAU,SAU,SAUS,SBC,SBM,SCAU,SCFK-SDU,SCI-CLT,SCN,SCNU,SCSFRI,SCSMBC,SDSU,SEABRI,SEVIN,SFC,SFRS,SFU,SHK,SIO,SIU,SIUC,SIZ,SLUB,SM,SMAG,SMBL,SMEC,SMF,SMK,SMNH,SMNHTAU,SMNS,SMU,SMWU,SNC,SNFR,SNHM,SNHMK,SNM,SNMB,SNMBR,SNMNH,SNP,SNU,SNUIZ,SOU,SPKCES,SPMN,SPNRI,SPSU,SRC/ZSI,SRS/ZSI,SSCN,SSMKL,SSOFM,STC/DOZ,STRI,STUM,SU,SUB,SUBC,SUC,SUF,SUML,SW,SWFC,SWU,SWUF,SYSU,TABL,TAFIRI,TCWC,TDHSP,TFMC,TFRI,THNHM,THUB,THUP,TINRO,TISTR,TKPM,TMBC,TMBS,TMBU,TMF,TMFE,TMH,TMNH,TMP,TNHC,TNZ,TOU-AE,TOYA,TU,TUFIL,TUIC,UAB,UADBA,UAIC,UAM,UAMNH,UAMZ,UANL,UARC-IC,UAZ,UAZM,UBC,UBD,UBJTL,UBMZ,UCBL,UCBLZ,UCD,UCDZ,UCFP,UCLA,UCR,UDONECI,UEFS,UERJ,UF,UFAM,UFBA,UFC,UFES,UF-FSU,UFJF,UFOPA,UFPB,UFPI,UFRGS,UFRJ,UFRN,UFRO,UG,UG/CSBD,UGAMNH,UGM,UH,UI,UIST,UIS-T,ULIZ,UMB,UMBC,UMFSP,UMIM,UMKL,UMML,UMMZ,UMOC,UMSS,UMZC,UNAL,UNAM,UNEFM,UNICACH-MZ-P,UNIMAS,UNM,UNMDP,UNMF,UNO,UNOAL,UNOVC,UNR,UNS,UNT,UOK,UOMZ,UPL,UPLB,UPR,UPVMI,UPZM,URB,URM,URM-P,USA,USBCF,USBF,USFC,USM,USNM,USP,USPS,USU,UT,UTAI,UTEP,UTU,UTZI,UUZM,UV,UW,UWF,UWIZM,UWZM,UZA,V/A/ERS,V/APRC/ZSI,VBCM,VIMS,VMFC,VMM,VMMB,VNIROA,VNMN,VSM,VUW,WAM,WFC,WGNHS,WGRS,WGRS/ZSI,WHOI,WHT,WIAP,WILD,WIRI,WLMH,WML,WMNH,WMSA,WPU,WPU-PPC,WUM,WURC,XFCFC,YCM,YPM,YQAMS,YU,YUGNIRO,ZFMK,ZIAS,ZIAZ,ZICT,ZICUP,ZIHU,ZIK,ZIKU,ZIM,ZIN,ZISP,ZJOU,ZLSYU,ZM/UI,ZMA,ZMAU,ZMB,ZMBJ,ZMC,ZM-CBSU,ZMCC,ZMFESU,ZMFMIB,ZMFUM,ZMH,ZMHU,ZMISU,ZML,ZMMGU,ZMMU,ZMNH,ZMP PGU,ZMT,ZMTU,ZMUA,ZMUAS,ZMUB,ZMUC,ZMUI,ZMUL,ZMULB,ZMUO,ZMUT,ZMUU,ZMV PSU,ZMYU,ZMZ,ZRC,ZRCS,ZSI,ZSI PUNE,ZSI/ANRC,ZSI/APRC,ZSI/MNRC,ZSI/NRS,ZSI/SRS,ZSI/WGFR,ZSI/WGRS,ZSIF,ZSL,ZSM,ZSM/CMK,ZSM/LIPI,ZSP,ZUEC,ZUFES,ZUFMS,ZUMH,ZUMT,ZVC,ZVC-P,ZZSZ"
institution_string = "Angola,Argentina,Australia,Austria,Azerbaijan,Bangladesh,Belgium,Bénin,Bermuda,Bhutan,Bolivia,Botswana,Brasil,Brazil,Brunei,Bulgaria,Burkina Faso,Burundi,Cambodia,Canada,Chad,Chile,China,Colombia,Costa Rica,Côte d’Ivoire,Croatia,Cuba,Czech Republic,D. R. Congo,D.P.R. Korea,Denmark,Dominican Republic,Ecuador,Egypt,Fiji,Finland,France,Gabon,Georgia,Germany,Greece,Grenada,Guam,Guyana,Honduras,Hungary,Iceland,India,Indonesia,Iran,Ireland,Israel,Italy,Japan,Kenya,Korea,Laos,Luxembourg,Macedonia,Madagascar,Madeira,Malawi,Malaysia,Mauritius,Mexico,Monaco,Montenegro,Mozambique,Myanmar,Namibia,Nepal,Netherlands,New Zealand,Nigeria,Norway,Oman,Pakistan,Palestine,Panama,Papua New Guinea,Paraguay,Peru,Philippines,Poland,Portugal,Puerto Rico,Romania,Russia,Saudi Arabia,Scotland,Senegal,Serbia,Seychelles,Singapore,Slovakia,Slovenia,South Africa,Spain,Sri Lanka,Sudan,Sweden,Switzerland,Taiwan,Tanzania,Thailand,Trinidad and Tobago,Turkey,U.K.,U.S.A.,Ukraine,United Kingdom,Uruguay,Venezuela,Vietnam,Yemen,Zimbabwe"
institution_list = institution_string.split(",");
book = xlwt.Workbook()
sheet1 = book.add_sheet('sheet1', cell_overwrite_ok=True)

#create ip proxy pool
ua = UserAgent()
"http://greatlakesinvasives.org/portal/imagelib/search.php?nametype=2&taxtp=2&taxa=&common=&photographer=&tags=&keywords=&uploaddate1=1000&uploaddate2=2020&imagecount=all&imagedisplay=thumbnail&imagetype=all&taxastr=&countrystr=&statestr=&keywordstr=&phuidstr=&phjson=&submitaction=Load+Images&db%5B%5D=48"
"http://greatlakesinvasives.org/portal/imagelib/search.php?nametype=2&taxtp=2&taxa=&common=&photographer=&tags=&keywords=&uploaddate1=1000&uploaddate2=2020&imagecount=all&imagedisplay=thumbnail&imagetype=all&taxastr=&countrystr=&statestr=&keywordstr=&phuidstr=&phjson=&submitaction=Load+Images&db%5B%5D=48#"
ippool_req = requests.get("https://www.proxy-list.download/api/v1/get?type=http") # This ip pool is updated every 2 hours
#ippool_response = requests.urlopen(ippool_req)
ippool_content = ippool_req.content.decode()
ip_list = str.split(ippool_content,sep='\r\n')

def get_random_ip():
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies
string_json={}
for institution in institution_list:
    url = "http://researcharchive.calacademy.org/research/ichthyology/catalog/collections.asp"
    #Mus = AFAQ & Country = % 5
    #Bany % 5
    #D & Mus_name = & xAction = Search#
    data = {
        "Mus":"[any]",
        "Country":institution,
        "Mus_name":"",
        "xAction":"Search"
    }

    #generate fake random user agent
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    ### start web crawling
    html = ""
    # get one random ip from ip pool, if the ip is blocked by tennfish website, select another ip from the pool
    while True:
       proxies = get_random_ip()
       try:
            #response = requests.post(url,data=data, headers = headers,proxies = proxies)
            response = requests.post(url,data=data, headers = headers)

            html = response.text
            break
       except requests.exceptions.RequestException as e:
            print(e)
            continue

    #html = html.decode("utf-8")
    #html = '<table width="100%" border="0" cellspacing="0" cellpadding="20" class="bodytext"><tr><td><b>[ 1 ]</b> record where abbreviation = <b>MAMU</b><hr noshade size="1"><table cellspacing="5"><tr><td valign="top" class="dispdata"><b>MAMU&nbsp;&nbsp;&nbsp;</b></td><td class="dispdata"><b>University of Sydney, Macleay Museum, Sydney, New South Wales, Australia.  Types are at AMS.</b></td></tr><tr><td>&nbsp;</td><td class="dispdata"><b>Other Abbrev.:</b> MU,MMUS. <b>Country:</b> Australia</td></tr><tr><td>&nbsp;</td><td class="dispdata"><b>WWW sites:</b> <b>Main site:</b> <a href="http://sydney.edu.au/museums/collections/macleay.shtml" target=_>http://sydney.edu.au/museums/collections/macleay.shtml</a>&nbsp;&nbsp;&nbsp;</td></tr><tr><td>&nbsp;</td><td class="dispdata"><b>Publications:</b> <a href="getref.asp?id=19518">19518</a></td></tr></table><hr size="1" noshade></td></tr></table>'
    bs = BeautifulSoup(html, 'lxml')
    institution_table_list = bs.find_all(name='table', attrs={"cellspacing": 5})
    for table in institution_table_list:
        tr_lists = table.find_all(name="tr")

        for index, tr in enumerate(tr_lists):
            if index==0:
                institution_abbrev_tr = tr.contents[0].text
                string_json[institution_abbrev_tr] = {}
                full_name_tr = tr.contents[1].text
                string_json[institution_abbrev_tr]["Full_Name"] =full_name_tr
            else:
                b_lists = tr.find_all(name="b")
                for b_index, b in enumerate(b_lists):
                    b_next = b.find_next_sibling()
                    if b_next is not None:
                        if b_next.name == 'b' and b.nextSibling.strip() == '':
                            string_json[institution_abbrev_tr][b.text] = 'None'
                        elif b_next.name == 'b' and b.nextSibling.strip() != '':
                            string_json[institution_abbrev_tr][b.text] = b.nextSibling
                        else:
                            string_json[institution_abbrev_tr][b.text] = b_next.text
                    else:
                        string_json[institution_abbrev_tr][b.text] = b.nextSibling
    print(string_json)


with open('data_country.txt', 'w') as outfile:
    json.dump(string_json, outfile)




