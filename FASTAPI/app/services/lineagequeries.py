from langchain_community.utilities.sql_database import SQLDatabase
import pandas as pd

from services import SQLUtility
from services import PlotGraph as pg
import datetime
import json
import sqlalchemy
from sqlalchemy.types import DECIMAL
from  services.LineageType import LineageType

# from LineageType import StrEnum
from services import cypher_template


mapping_gui_template=r"MATCH(N:{0}) WHERE N.TRAN_AMT={1} and N.TRAN_ACCT='{2}' AND N.TRAN_DT='{3}' RETURN N"	

mapping_template_expanded='''MATCH  (A:SRC1_INPUT1)- [:Extr_from_Src1data1_to_stg1]->(B:SRC1_STG)
MATCH  (E:SRC2_INPUT1)- [:Extr_from_Src2File1_to_src2st1]->(G:SRC2_STG1)
MATCH  (F:SRC2_INPUT2)- [:Extr_from_Src2File2_to_src2stg2]->(H:SRC2_STG2)
MATCH  (G:SRC2_STG1)- [:Extr_from_Src2Stg1_to_kde2]->(I:KDE2)
MATCH  (H:SRC2_STG2)- [:Extr_from_Src2Stg2_to_kde2]->(I:KDE2)
MATCH  (B:SRC1_STG)- [:Extr_from_Src1Stg1_to_kde1]->(C:KDE1)
MATCH  (C:KDE1)- [:Extr_from_kde1_to_stich]->(D:STITCH)
MATCH  (I:KDE2)- [:Extr_from_kde2_to_Stitch]->(D:STITCH)
MATCH  (D:STITCH)- [:Extr_from_stitch]->(J:PRECSA)
MATCH  (J:PRECSA)- [:Extr_from_precsa]->(K:CSA)
WHERE (substring('0000',0,case size(A.acc_9_ctl1)  when 1 then 3   when 2 then 2  when 3 then 1  when 4 then 0  end)+ 
A.acc_9_ctl1   + substring('0000',0,CASE size(A.acc_9_ctl2)   when 1 then 3   when 2 then 2  when 3 then 1  when 4 then 0   end)
+ A.acc_9_ctl2    + substring('0000',0,CASE size(A.acc_9_ctl3)   when 1 then 3   when 2 then 2  when 3 then 1  when 4 then 0   end)
+ A.acc_9_ctl3   + substring('0000',0, CASE size(A.acc_9_ctl4)  when 1 then 3   when 2 then 2  when 3 then 1  when 4 then 0   end) + 
A.acc_9_ctl4  + substring('0000000000',0,CASE size(A.acc_9_acct) when 1 then 9   when 2 then 8  when 3 then 7  when 4 then 6 when 5 then 5 
when 6 then 4  when 7 then 3  when 8 then 2  when 9 then 1   when 10 then 0 end ) + A.acc_9_acct  + A.acc_9_ccyyddd + A.acc_9_rec_seq )
='{0}'
Return A, B,C,D,E,F,G,H,I,J,K''' 

shortenned_cypher_query='''match(n:CSA) where n.txn_ref_no='{0}' return n'''

stg_src1_query='SELECT * \
    from	"genaipoc"."STG_SRC1_STITCHED" \
where  "TRAN_AMT" = cast(:tranamt as varchar(20)) 	'''


#
query='''SELECT 'CSA' as mapping , txn_ref_no, fic_mis_date, account_number, txn_value_date, drcr_indicator, txn_desc,\
tran_prod_type_cd_tmp, txn_amt, txn_amt_acy	\
    FROM "genaipoc"."FIN_ACCT_TXNS"\
    where txn_ref_no= cast(:txn_ref_no as varchar(500))'''

#PRE-CSA TO CSA FIN_ACCT_TXNS:
#############################

precsa_csa= '''SELECT  'CSA' as mapping , txn_ref_no, fic_mis_date, account_number, txn_value_date, drcr_indicator,\
txn_desc, tran_prod_type_cd_tmp, txn_amt, txn_amt_acy\
    FROM "genaipoc"."FIN_ACCT_TXNS"\
    where txn_ref_no=cast(:txn_ref_no as varchar(500))\
    UNION \
SELECT 'PRE CSA' as mapping , txn_ref_no, fic_mis_date, account_number, txn_value_date, drcr_indicator, txn_desc,\
tran_prod_type_cd_tmp, txn_amt, txn_amt_acy\
    FROM "genaipoc"."PRE_FIN_ACC_TXNS"\
    where txn_ref_no=cast(:txn_ref_no as varchar(500))'''




#STITCH TO PRE-CSA;
###################

stitch_to_precsa_query=	'''SELECT 'PRE CSA' as mapping , txn_ref_no, fic_mis_date, account_number,tran_grp_cd_tmp, txn_value_date, drcr_indicator, txn_desc, 
tran_prod_type_cd_tmp, txn_amt, txn_amt_acy
    FROM "genaipoc"."PRE_FIN_ACC_TXNS"
    where txn_ref_no=cast(:txn_ref_no as varchar(500))
    UNION 
    select * from ( 
SELECT 'SRC 1 STITCHING' as mapping , tran_ref_no, dl_as_of_dt as fic_mis_date, 
    case when drcr_in='C' then bnf_acct_id else origintr_acct_id end as 
    account_number,tran_grp_cd_tmp, tran_val_dt, drcr_in, tran_desc, tran_prod_type_cd_tmp, txn_amt, tran_amnt_act_cur 
    FROM 	( 
    SELECT bnf_acct_id, drcr_in, tran_val_dt, origintr_acct_id, tran_desc, tran_prod_type_cd_tmp, 
              tran_ref_no, orig_dl_as_of_dt, dl_as_of_dt, dl_source_cd, txn_amt, tran_grp_cd_tmp, stitch_flag, 
     tran_acct1_tmp, tran_amt_tmp, tran_dt_tmp, tran_type_cd_tmp,
    tran_amnt_act_cur 
    FROM "genaipoc"."SRC1_STITCHED"
) TMP)
    where  tran_ref_no=cast(:txn_ref_no as varchar(500))'''

GET_ADDITIONAL_PARAMS='''select lkp_tran_ref_no from 	"genaipoc"."SRC1_STITCHED"
    where tran_ref_no=cast(:txn_ref_no as varchar(500))'''
 
 
GET_NACHA_PARAMS='''select nacha_5,nacha_6 from "genaipoc"."SRC2_KDE" where "tran_ref_no"=cast(:lkp_tran_ref_no as varchar(500))
 '''

#KDE to Stitch

KDE_To_Stitch_query='''WITH KDE1_CTE AS(
    SELECT tran_amnt, bnf_acct_id, drcr_in, tran_val_dt, origntr_acct_id, tran_desc, tran_ref_no, tran_prod_type_cd_tmp, tran_acct1_tmp, tran_amt_tmp, tran_dt_tmp, tran_type_cd_tmp, dl_as_of_dt, dl_source_cd, bnf_acct_id_type, origntr_acct_id_type, acc_ident, tran_amnt_act_cur
    FROM "genaipoc"."SRC1_KDE"
)
    ,
KDE2_CTE AS(
SELECT drcr_in, origntr_acct_id, tran_acct1_tmp, tran_amt_tmp, tran_dt_tmp, dl_as_of_dt, dl_source_cd, txn_amt, acc_ident_nbr
FROM "genaipoc"."SRC2_KDE"
)
,
    KDE_JOINS AS
    (
    SELECT KDE1.tran_desc, 
    CASE WHEN KDE1.drcr_in ='D' THEN KDE1.origntr_acct_id ELSE KDE2.origntr_acct_id END AS origntr_acct_id,
    CASE WHEN KDE1.drcr_in ='C' THEN KDE1.bnf_acct_id ELSE NULL END AS bnf_acct_id,
    KDE1.tran_prod_type_cd_tmp  tran_prod_type_cd_tmp,
    KDE1.drcr_in AS drcr_in
    , KDE1.tran_amnt AS tran_amnt
    , KDE1.tran_val_dt AS tran_val_dt
    , KDE1.tran_acct1_tmp AS tran_acct1_tmp  
    ,KDE1.tran_ref_no,'' as tran_grp_cd_tmp

    
    FROM
    "genaipoc"."SRC1_KDE" KDE1 JOIN "genaipoc"."SRC2_KDE" KDE2
    ON KDE1.tran_acct1_tmp = KDE2.tran_acct1_tmp AND
    KDE1.tran_amt_tmp = KDE2.tran_amt_tmp AND
    KDE1.tran_dt_tmp = KDE2.tran_dt_tmp 
    )  
    SELECT 'KDE1-2' as map	,	* FROM KDE_JOINS
where 
    
    tran_ref_no=cast(:txn_ref_no as varchar(500))
    
union
    
select 'STITCH' as map,tran_desc,origintr_acct_id,bnf_acct_id,tran_prod_type_cd_tmp,drcr_in,
    txn_amt,tran_val_dt,tran_acct1_tmp,tran_ref_no,tran_grp_cd_tmp
    from "genaipoc"."SRC1_STITCHED"
where tran_ref_no=cast(:txn_ref_no as varchar(500))'''



#SRC1_STAGING_DATA TO STG_SRC1_KDE
#########################################
    
stg_src1_KDE_query='''SELECT 'SRC1-KDE' as mapping,tran_amnt, bnf_acct_id, drcr_in,
    cast(to_date(tran_val_dt,'yyyy-mm-dd') as varchar(10))	as tran_val_dt	, origntr_acct_id, tran_desc,
    tran_ref_no, tran_prod_type_cd_tmp, tran_acct1_tmp, 
 cast(cast(tran_amt_tmp as numeric) as varchar(10)) as tran_amt_tmp,
    cast(to_date(tran_dt_tmp,'yyyy-mm-dd') as varchar(10))	as tran_dt_tmp	, tran_type_cd_tmp,
    cast(to_date(	dl_as_of_dt	,'yyyy-mm-dd') as varchar(10)) as dl_as_of_date,
    dl_source_cd, bnf_acct_id_type, origntr_acct_id_type, acc_ident, tran_amnt_act_cur
    FROM "genaipoc"."SRC1_KDE"
    where 	tran_ref_no=cast(:txn_ref_no as varchar(500))
    UNION
    
select * from (
    select 
    
    mapping,
    tran_amnt, bnf_acct_id, drcr_in, cast(to_date(tran_val_dt,'yyyymmdd')  as varchar(10)) as tran_val_dt	, 
 origntr_acct_id, tran_desc, 
    tran_ref_no, tran_prod_type_cd_tmp, cast(tran_acct1_tmp as varchar(10)), cast(tran_amt_tmp as varchar(10)), cast(tran_dt_tmp as varchar(10))	,
    tran_type_cd_tmp, cast(dl_as_of_dt as varchar(10)), dl_source_cd,
        case when bnf_acct_id is not null then 'IA' else null end as bnf_acct_id_type,
    case when origntr_acct_id is not null then 'IA' else null end as origntr_acct_id_type,
    acc_ident, tran_amnt_act_cur
    
    from (
select mapping, 
    case when acc_id ='1' then acc_amt
    when acc_id='3' then acc_3_amt
    when acc_id='10' then acc_10_amt
    when acc_id='09' then acc_9_amt
    when acc_id='02' then acc_2_amt
    else null end as tran_amnt,
    case 
    when acc_id='3' and acc_3_type in ('1','2','5','7') then 
    'SRC1-'||lpad(acc_3_ctl1,4,'0')||lpad(acc_3_ctl2,4,'0')||lpad(acc_3_ctl3,4,'0')||lpad(acc_3_ctl4,4,'0')||
    lpad(acc_3_acct	,10,'0')
    when acc_id='10' and acc_10_type in ('1','2','5','7') then 
    'SRC1-'||lpad(acc_10_ctl1,4,'0')||lpad(acc_10_ctl2,4,'0')||lpad(acc_10_ctl3,4,'0')||lpad(acc_10_ctl4,4,'0')||
    lpad(acc_10_acct	,10,'0')
 
    when acc_id='9' and acc_9_type in ('1','2','5','7') then 
    'SRC1-'||lpad(acc_9_ctl1,4,'0')||lpad(acc_9_ctl2,4,'0')||lpad(acc_9_ctl3,4,'0')||lpad(acc_9_ctl4,4,'0')||
    lpad(acc_9_acct	,10,'0')
 
    when acc_id='1' and acc_type in ('1','2','5','7') then 
    'SRC1-'||lpad(acc_ctl1,4,'0')||lpad(acc_ctl2,4,'0')||lpad(acc_ctl3,4,'0')||lpad(acc_ctl4,4,'0')||
    lpad(acc_acct	,10,'0')
    when acc_id='2' and acc_2_type in ('1','2','5','7') then 
    'SRC1-'||lpad(acc_2_ctl1,4,'0')||lpad(acc_2_ctl2,4,'0')||lpad(acc_2_ctl3,4,'0')||lpad(acc_2_ctl4,4,'0')||
    lpad(acc_2_acct	,10,'0')
    else
    null end  as bnf_acct_id,
    case when acc_id='3' then acc_3_type
    when acc_id='10' then acc_10_type
    when acc_id='9' then acc_9_type
    when acc_id='1' then acc_type
    when acc_id='2' then acc_2_type
end	as drcr_in,
    case when acc_id='3' then to_char(to_date(lpad(acc_ent_dt,6,'0'), 'MMDDYY'), 'YYYYMMDD') 
    when acc_id='10' then to_char(to_date(lpad(acc_ent_dt,6,'0'), 'MMDDYY'), 'YYYYMMDD')
    when acc_id='09' then to_char(to_date(lpad(acc_dt_cd ,6,'0'), 'MMDDYY'), 'YYYYMMDD')   
    when acc_id='1' then to_char(to_date(lpad(  acc_pst_dt   ,6,'0'), 'MMDDYY'), 'YYYYMMDD')   
    when acc_id='2' then NULL
    else NULL
    end as tran_val_dt,
    case 
    when acc_id='3' and acc_3_type in ('3','4','6','8') then 'SRC1-'||lpad(acc_3_ctl1,4,'0')||lpad(acc_3_ctl2,4,'0')||
    lpad(acc_3_ctl3,4,'0')||lpad(acc_3_ctl4,4,'0')||lpad(acc_3_acct,10,'0')
    when acc_id='10' and acc_3_type in ('3','4','6','8') then 'SRC1-'||lpad(acc_10_ctl1,4,'0')||lpad(acc_10_ctl2,4,'0')||
    lpad(acc_10_ctl3,4,'0')||lpad(acc_10_ctl4,4,'0')||lpad(acc_10_acct,10,'0')
    when acc_id='9' and acc_3_type in ('3','4','6','8') then 'SRC1-'||lpad(acc_9_ctl1,4,'0')||lpad(acc_9_ctl2,4,'0')||
    lpad(acc_9_ctl3,4,'0')||lpad(acc_9_ctl4,4,'0')||lpad(acc_9_acct,10,'0')
    when acc_id='1' and acc_3_type in ('3','4','6','8') then 'SRC1-'||lpad(acc_ctl1,4,'0')||lpad(acc_ctl2,4,'0')||
    lpad(acc_ctl3,4,'0')||lpad(acc_ctl4,4,'0')||lpad(acc_acct,10,'0')
    when acc_id='2' and acc_2_type in ('3','4','6','8') then 'SRC1-'||lpad(acc_2_ctl1,4,'0')||lpad(acc_2_ctl2,4,'0')||
    lpad(acc_2_ctl3,4,'0')||lpad(acc_2_ctl4,4,'0')||lpad(acc_2_acct,10,'0')
    else null end
    as origntr_acct_id, 
    case when acc_id in ('1','3','2','9','10') then 
    concat(acc_ent_desc,'|',acc_2_univ_desc) else null end as tran_desc,--acc_cust_desc is missing
    case 
    when acc_id='3' then 
        concat(lpad(acc_3_ctl1,4,'0'),lpad(acc_3_ctl2	,4,'0'),lpad(acc_3_ctl3	,4,'0'),lpad(acc_3_ctl4	,4,'0'),lpad(acc_3_acct	,10,'0'),acc_3_ccyyddd,acc_3_rec_seq)
    when acc_id='10' then 
        concat(lpad(acc_10_ctl1,4,'0'),lpad(acc_10_ctl2	,4,'0'),lpad(acc_10_ctl3	,4,'0'),lpad(acc_10_ctl4	,4,'0'),lpad(acc_10_acct	,10,'0'),acc_10_ccyyddd,acc_10_rec_seq)
    when acc_id='9' then 
        concat(lpad(acc_9_ctl1,4,'0'),lpad(acc_9_ctl2	,4,'0'),lpad(acc_9_ctl3	,4,'0'),lpad(acc_9_ctl4	,4,'0'),lpad(acc_9_acct	,10,'0'),acc_9_ccyyddd,acc_9_rec_seq)
    when acc_id='1' then 
        concat(lpad(acc_ctl1,4,'0'),lpad(acc_ctl2	,4,'0'),lpad(acc_ctl3	,4,'0'),lpad(acc_ctl4	,4,'0'),lpad(acc_acct	,10,'0'),acc_ccyyddd,acc_rec_seq)
    when acc_id='2' then 
        concat(lpad(acc_2_ctl1,4,'0'),lpad(acc_2_ctl2	,4,'0'),lpad(acc_2_ctl3	,4,'0'),lpad(acc_2_ctl4	,4,'0'),lpad(acc_2_acct	,10,'0'),acc_2_ccyyddd,acc_2_rec_seq)
    
    else
    NULL end as tran_ref_no,
    case 
    when acc_id='1' then acc_usr_tr_cd 
    when acc_id='3' then acc_3_usr_tr_cd
    when acc_id='10' then acc_10_usr_tr_cd
    when acc_id='09' then acc_9_usr_tr_cd
    when acc_id='2' then acc_2_usr_tr_cd
    
    else NULL end as tran_prod_type_cd_tmp,
    
    
case when (acc_3_emp_id='EPIM' and acc_3_id='3') or (acc_10_emp_id='EPIM' and acc_10_id='10') then lpad(trim(acc_acct),17,'0')
    end as tran_acct1_tmp,
    case when (acc_3_emp_id='EPIM' and acc_3_id='3') or (acc_10_emp_id='EPIM' and acc_10_id='10') then 
    cast(acc_amt as numeric) end as  tran_amt_tmp,
    case when (acc_3_emp_id='EPIM' and acc_3_id='3') or (acc_10_emp_id='EPIM' and acc_10_id='10') then 
    to_date(lpad(cast(acc_pst_dt as varchar(6)),6,'0'),'MMDDYY')
    end as  tran_dt_tmp,
 
 
 null as tran_type_cd_tmp,
    current_date as dl_as_of_dt,
    'SRC1' as dl_source_cd,

    acc_ident,
    case when acc_id='1' then acc_amt 
    when acc_id='3' then acc_3_amt
    when acc_id='10' then acc_10_amt
    when acc_id='9' then acc_9_amt
    when acc_id='2' then acc_2_amt
    else null end as tran_amnt_act_cur
    from (
SELECT 'SRC1_STG1' as mapping,
    acc_ctl1, acc_ctl2, acc_ctl3, acc_ctl4, acc_acct, acc_ccyyddd, acc_rec_seq, acc_id, acc_amt,
    acc_pst_dt, acc_usr_tr_cd, acc_type, acc_desc, acc_2_ctl1, acc_2_ctl2, acc_2_ctl3, acc_2_ctl4, 
    acc_2_acct, acc_2_ccyyddd, acc_2_rec_seq, acc_2_amt, acc_2_pst_dt, acc_2_usr_tr_cd, acc_2_type, 
    acc_2_univ_desc, acc_3_ctl1, acc_3_ctl2, acc_3_ctl3, acc_3_ctl4, acc_3_acct, acc_3_ccyyddd, 
    acc_3_rec_seq, acc_3_amt, acc_3_usr_tr_cd, acc_3_type, acc_ent_desc, acc_ent_dt, acc_9_ctl1,
    acc_9_ctl2, acc_9_ctl3, acc_9_ctl4, acc_9_acct, acc_9_ccyyddd, acc_9_rec_seq, acc_9_amt,
    acc_9_usr_tr_cd, acc_9_type, acc_desc_cd, acc_dt_cd, acc_9_univ_desc, acc_10_ctl1, acc_10_ctl2, 
    acc_10_ctl3, acc_10_ctl4, acc_10_acct, acc_10_ccyyddd, acc_10_rec_seq, acc_10_amt, acc_10_usr_tr_cd, 
    acc_10_type, acc_ud_desc, dl_as_of_dt, dl_source_cd, acc_ident,acc_10_emp_id,acc_10_id,acc_3_emp_id	,acc_3_id
    FROM "genaipoc"."SRC1_STG1")STAGING1))t
where	tran_ref_no=cast(:txn_ref_no as varchar(500))
'''

#SRC1 KDE to SRC1 Orphan

src1_KDE_Orphan='''select 
    'SRC1- ORPHAN' as mapping,tran_amnt,bnf_acct_id,drcr_in,tran_val_dt,origntr_acct_id,tran_desc,tran_ref_no,tran_prod_type_cd_tmp,
        tran_acct1_tmp,	tran_amt_tmp,tran_dt_tmp,tran_type_cd_tmp,dl_as_of_dt,dl_source_cd,origntr_acct_id_type,acc_ident
    from "genaipoc"."SRC1_ORPHAN"
    where tran_ref_no=cast(:txn_ref_no as varchar(500))'''

#SRC2_STAGING_DATA1 & SRC2_STAGING_DATA2  TO STG_SRC2_KDE
########################################################

stg_src2_KDE_query='''SELECT 'SRC2_KDE' as mapping, drcr_in, origntr_acct_id, tran_acct1_tmp, 
    cast(cast(tran_amt_tmp as numeric)/100.0 as varchar(20))  as tran_amt_tmp
--	,to_date(tran_dt_tmp,'dd-mon-yy') as tran_dt_tmp
--	, to_date(dl_as_of_dt,'dd-mon-yy') as dl_as_of_dt

    ,cast(tran_dt_tmp as date) as tran_dt_tmp
    , cast(dl_as_of_dt as date) as dl_as_of_dt

    , dl_source_cd, txn_amt	, acc_ident_nbr   ,nacha_5,nacha_6
    FROM "genaipoc"."SRC2_KDE"
    where nacha_5=:nacha_5 and nacha_6 =:nacha_6 
    
    
UNION
    
(
    
WITH SRC2_STG1_CTE AS (
SELECT 'SRC2_STG1' as mapping, nacha_050_coll_file_no, nacha_5, dl_as_of_dt, dl_source_cd, nacha_050_coll_btch_no, ifw_eff_dt, nacha_050_coll_pt
    FROM "genaipoc"."SRC2_STG1"
),
SRC2_STG2_CTE AS (	
SELECT 'SRC2_STG2' as mapping,nacha_060_coll_file_no,nacha_6, dl_as_of_dt, dl_source_cd, nacha_060_dtl_par, nacha_060_coll_btch_no, ifw_eff_dt, nacha_060_coll_pt
    FROM "genaipoc"."SRC2_STG2"
),
JOINS_SRC_CTES AS ( select b.*,a.* from SRC2_STG1_CTE a 
    join  SRC2_STG2_CTE b
    on a.nacha_050_coll_file_no=b.nacha_060_coll_file_no
    and a.nacha_050_coll_btch_no=b.nacha_060_coll_btch_no
    )
    select * from (
Select
'SRC2-STG2' ,

drcr_in,
case when drcr_in='C' then substr(nacha_5,41,10)
        when drcr_in='D' and IAT_ind='Y' then substr(nacha_6, 40, 35)
        when drcr_in='D' and IAT_ind!='Y' then substr(nacha_6, 13, 17)
        end origntr_acct_id,
Case when IAT_ind='Y' then substr(substr(nacha_6,40,35),-17)
    else lpad(substr(nacha_6,13,17),17,'0')
    end tran_acct1_tmp,
--cast(cast(substr(nacha_6, 30, 10) as int)/100.0 as varchar(10)) as tran_amt_tmp,
''  as tran_amt_tmp,
--to_date(substr(nacha_5,70,6),'yyMMdd') as tran_dt_tmp,
CURRENT_DATE as tran_dt_tmp,
CURRENT_DATE as dl_as_of_dt,
'SRC1' as dl_source_cd,
--cast(cast(substr(nacha_6, 30, 10) as int)/100.0  as varchar(20)) as txn_amt,
NULL as txn_amt,
Case when substr(nacha_5,51,3) in ('CIE','MTE') then trim(substr(nacha_6,55,15))
    when substr(nacha_5,51,3) ='POP' then trim(substr(nacha_6,40,15))
    when substr(nacha_5,51,3) ='SHR' then trim(substr(nacha_6,44,11))
    when substr(nacha_5,51,3) = 'IAT' then trim(substr(nacha_6 ,4,15)) 
    else  trim(substr(nacha_6,40,15)) end as  acc_ident_nbr,
 nacha_5,nacha_6
From
(
select case when substr(nacha_6,2,2) in ('21','62','23','22','54','53','52','51','44','43','42','41','34','33','32','31') then 'C'
    else 'D' end drcr_in,
    case when substr (nacha_5,51,3)='IAT' then 'Y'
    else 'N' end IAT_ind,
    a.*
from JOINS_SRC_CTES a
))
     where nacha_5=:nacha_5 and nacha_6=:nacha_6
    );'''


#SRC 1 KDE to SRC 1 HOLDING

src1_kde_to_holding='''select
    'SRC 1 HOLD' as mapping,tran_amnt,bnf_acct_id,drcr_in,tran_val_dt,origntr_acct_id,tran_desc,tran_ref_no,tran_prod_type_cd_tmp,tran_acct1_tmp,tran_amt_tmp,
    tran_dt_tmp,
    tran_type_cd_tmp,
    bnf_acct_id_type,
    origntr_acct_id_type,
    acc_ident
    from "genaipoc"."SRC1_HOLD"
where tran_ref_no=:tran_ref_no

'''

#SRC1_FILE TO SRC1_STAGING_DATA;
###################################

src1_Staging_data='''
    SELECT 'SRC1_INPUT1' as map, cast(acc_ctl1 as varchar(500)), cast(acc_ctl2 as varchar(500)),cast( acc_ctl3 as varchar(500)), 
cast(acc_ctl4 as varchar(500)), cast(acc_acct as varchar(500)), cast(acc_ccyyddd as varchar(500)),
        cast(acc_rec_seq as varchar(500)), cast(acc_id as varchar(500)), cast(acc_amt as varchar(500)),
  cast(acc_pst_dt as varchar(500)),cast( acc_usr_tr_cd as varchar(500)),cast( acc_type as varchar(500)), cast(acc_desc as varchar(500)),
        cast(acc_2_ctl1 as varchar(500)),cast( acc_2_ctl2 as varchar(500)), cast(acc_2_ctl3 as varchar(500)),
  cast(acc_2_ctl4 as varchar(500)),cast( acc_2_acct as varchar(500)),cast( acc_2_ccyyddd as varchar(500)), 
        cast(acc_2_rec_seq as varchar(500)), cast(acc_2_amt as varchar(500)), cast(acc_2_pst_dt as varchar(500)), 
  cast(acc_2_usr_tr_cd as varchar(500)), cast(acc_2_type as varchar(500)), cast(acc_2_univ_desc as varchar(500)), 
        cast(acc_3_ctl1 as varchar(500)), cast(acc_3_ctl2 as varchar(500)), cast(acc_3_ctl3 as varchar(500)), 
  cast(acc_3_ctl4 as varchar(500)), cast(acc_3_acct as varchar(500)), cast(acc_3_ccyyddd as varchar(500)), cast(acc_3_rec_seq as varchar(500)),
        cast(acc_3_amt as varchar(500)), cast(acc_3_usr_tr_cd as varchar(500)), cast(acc_3_type as varchar(500)), 
  cast(acc_ent_desc as varchar(500)), cast(acc_ent_dt as varchar(500)), cast(acc_9_ctl1 as varchar(500)), cast(acc_9_ctl2 as varchar(500)),
        cast(acc_9_ctl3 as varchar(500)), cast(acc_9_ctl4 as varchar(500)), cast(acc_9_acct as varchar(500)), cast(acc_9_ccyyddd as varchar(500)), cast(acc_9_rec_seq as varchar(500)), cast(acc_9_amt as varchar(500)), 
  cast(acc_9_usr_tr_cd as varchar(500)),
        cast(acc_9_type as varchar(500)), cast(acc_desc_cd as varchar(500)), cast(acc_dt_cd as varchar(500)), 
  cast(acc_9_univ_desc as varchar(500)), cast(acc_10_ctl1 as varchar(500)), cast(acc_10_ctl2 as varchar(500)), cast(acc_10_ctl3 as varchar(500)), 
        cast(acc_10_ctl4 as varchar(500)), cast(acc_10_acct as varchar(500)), cast(acc_10_ccyyddd as varchar(500)), 
  cast(acc_10_rec_seq as varchar(500)), cast(acc_10_amt as varchar(500)), cast(acc_10_usr_tr_cd as varchar(500)), 
        cast(acc_10_type as varchar(500)), cast(acc_ud_desc as varchar(500)), cast(dl_as_of_dt as varchar(500)), 
  cast(dl_source_cd as varchar(500)), cast(acc_ident as varchar(500))
    FROM "genaipoc"."SRC1_INPUT1"
    where (
(concat(lpad(cast(acc_3_ctl1 as varchar(10)),4,'0'),lpad(cast(acc_3_ctl2 as varchar(10)),4,'0'),lpad(cast(acc_3_ctl3 as varchar(10)),4,'0'),
lpad(cast(acc_3_ctl4 as varchar(10)),4,'0'),lpad(cast(acc_3_acct as varchar(10))	,10,'0'),
acc_3_ccyyddd,acc_3_rec_seq)
=cast(:txn_ref_no as varchar(500)))
or
(concat(lpad(cast(acc_10_ctl1 as varchar(10)),4,'0'),
lpad(cast(acc_10_ctl2 as varchar(10)),4,'0'),lpad(cast(acc_10_ctl3 as varchar(10)),4,'0'),lpad(cast(acc_10_ctl4 as varchar(10)),4,'0'),
        lpad(cast(acc_10_acct as varchar(10))	,10,'0'),acc_10_ccyyddd,acc_10_rec_seq)
=cast(:txn_ref_no as varchar(500)))
or
(concat(lpad(cast(acc_9_ctl1 as varchar(10)),4,'0'),lpad(cast(acc_9_ctl2 as varchar(10)),4,'0'),
lpad(cast(acc_9_ctl3 as varchar(10)),4,'0'),lpad(cast(acc_9_ctl4 as varchar(10)),4,'0'),
        lpad(cast(acc_9_acct as varchar(10)),10,'0'),acc_9_ccyyddd,acc_9_rec_seq)
=cast(:txn_ref_no as varchar(500)))
or
(concat(lpad(cast(acc_2_ctl1 as varchar(10)),4,'0'),lpad(cast(acc_2_ctl2 as varchar(10)),4,'0'),lpad(cast(acc_2_ctl3 as varchar(10)),4,'0'),
lpad(cast(acc_2_ctl4 as varchar(10)),4,'0'),
        lpad(cast(acc_2_acct as varchar(10)),10,'0'),acc_2_ccyyddd,acc_2_rec_seq)
=cast(:txn_ref_no as varchar(500)))
or
(concat(lpad(cast(acc_ctl1 as varchar(10)),4,'0'),lpad(cast(acc_ctl2 as varchar(10)),4,'0'),lpad(cast(acc_ctl3 as varchar(10)),4,'0'),
lpad(cast(acc_ctl4 as varchar(10)),4,'0'),
        lpad(cast(acc_acct as varchar(10)),10,'0'),acc_ccyyddd,acc_rec_seq)
=cast(:txn_ref_no as varchar(500)))


        )

    
    UNION
        
SELECT 'SRC1_STG1',
cast(acc_ctl1 as varchar(500)), cast(acc_ctl2 as varchar(500)),cast( acc_ctl3 as varchar(500)), 
cast(acc_ctl4 as varchar(500)), cast(acc_acct as varchar(500)), cast(acc_ccyyddd as varchar(500)),
        cast(acc_rec_seq as varchar(500)), cast(acc_id as varchar(500)), cast(acc_amt as varchar(500)),
  cast(acc_pst_dt as varchar(500)),cast( acc_usr_tr_cd as varchar(500)),cast( acc_type as varchar(500)), cast(acc_desc as varchar(500)),
        cast(acc_2_ctl1 as varchar(500)),cast( acc_2_ctl2 as varchar(500)), cast(acc_2_ctl3 as varchar(500)),
  cast(acc_2_ctl4 as varchar(500)),cast( acc_2_acct as varchar(500)),cast( acc_2_ccyyddd as varchar(500)), 
        cast(acc_2_rec_seq as varchar(500)), cast(acc_2_amt as varchar(500)), cast(acc_2_pst_dt as varchar(500)), 
  cast(acc_2_usr_tr_cd as varchar(500)), cast(acc_2_type as varchar(500)), cast(acc_2_univ_desc as varchar(500)), 
        cast(acc_3_ctl1 as varchar(500)), cast(acc_3_ctl2 as varchar(500)), cast(acc_3_ctl3 as varchar(500)), 
  cast(acc_3_ctl4 as varchar(500)), cast(acc_3_acct as varchar(500)), cast(acc_3_ccyyddd as varchar(500)), cast(acc_3_rec_seq as varchar(500)),
        cast(acc_3_amt as varchar(500)), cast(acc_3_usr_tr_cd as varchar(500)), cast(acc_3_type as varchar(500)), 
  cast(acc_ent_desc as varchar(500)), cast(acc_ent_dt as varchar(500)), cast(acc_9_ctl1 as varchar(500)), cast(acc_9_ctl2 as varchar(500)),
        cast(acc_9_ctl3 as varchar(500)), cast(acc_9_ctl4 as varchar(500)), cast(acc_9_acct as varchar(500)), cast(acc_9_ccyyddd as varchar(500)), cast(acc_9_rec_seq as varchar(500)), cast(acc_9_amt as varchar(500)), 
  cast(acc_9_usr_tr_cd as varchar(500)),
        cast(acc_9_type as varchar(500)), cast(acc_desc_cd as varchar(500)), cast(acc_dt_cd as varchar(500)), 
  cast(acc_9_univ_desc as varchar(500)), cast(acc_10_ctl1 as varchar(500)), cast(acc_10_ctl2 as varchar(500)), cast(acc_10_ctl3 as varchar(500)), 
        cast(acc_10_ctl4 as varchar(500)), cast(acc_10_acct as varchar(500)), cast(acc_10_ccyyddd as varchar(500)), 
  cast(acc_10_rec_seq as varchar(500)), cast(acc_10_amt as varchar(500)), cast(acc_10_usr_tr_cd as varchar(500)), 
        cast(acc_10_type as varchar(500)), cast(acc_ud_desc as varchar(500)), cast(dl_as_of_dt as varchar(500)), 
  cast(dl_source_cd as varchar(500)), cast(acc_ident as varchar(500))
    FROM "genaipoc"."SRC1_STG1"

where 
(
(concat(lpad(acc_3_ctl1,4,'0'),lpad(acc_3_ctl2,4,'0'),lpad(acc_3_ctl3,4,'0'),lpad(acc_3_ctl4,4,'0'),lpad(acc_3_acct	,10,'0'),acc_3_ccyyddd,acc_3_rec_seq)
=cast(:txn_ref_no as varchar(500)))
or
(concat(lpad(acc_10_ctl1,4,'0'),lpad(acc_10_ctl2,4,'0'),lpad(acc_10_ctl3,4,'0'),lpad(acc_10_ctl4,4,'0'),
        lpad(acc_10_acct	,10,'0'),acc_10_ccyyddd,acc_10_rec_seq)
=cast(:txn_ref_no as varchar(500)))
or
(concat(lpad(acc_9_ctl1,4,'0'),lpad(acc_9_ctl2,4,'0'),lpad(acc_9_ctl3,4,'0'),lpad(acc_9_ctl4,4,'0'),
        lpad(acc_9_acct,10,'0'),acc_9_ccyyddd,acc_9_rec_seq)
=cast(:txn_ref_no as varchar(500)))
or
(concat(lpad(acc_2_ctl1,4,'0'),lpad(acc_2_ctl2,4,'0'),lpad(acc_2_ctl3,4,'0'),lpad(acc_2_ctl4,4,'0'),
        lpad(acc_2_acct,10,'0'),acc_2_ccyyddd,acc_2_rec_seq)
=cast(:txn_ref_no as varchar(500)))
or
(concat(lpad(acc_ctl1,4,'0'),lpad(acc_ctl2,4,'0'),lpad(acc_ctl3,4,'0'),lpad(acc_ctl4,4,'0'),
        lpad(acc_acct,10,'0'),acc_ccyyddd,acc_rec_seq)
=cast(:txn_ref_no as varchar(500)))

        
)
    ;'''



#SRC2_FILE1 TO SRC2_STAGING_DATA1
###################################


src2_Staging_data='''SELECT 'SRC2_INPUT1' as "Type", 
cast(nacha_050_coll_file_no as varchar(5000)) as nacha_050_coll_file_no,
cast(dl_as_of_dt as varchar(5000)) as dl_as_of_dt,
cast(dl_source_cd as varchar(5000)) as dl_source_cd,
cast(nacha_050_dtl_par as varchar(5000)) as nacha_050_dtl_par,
cast(nacha_050_coll_btch_no as varchar(5000)) as nacha_050_coll_btch_no,
cast(ifw_eff_dt as varchar(5000)) as ifw_eff_dt,
cast(nacha_050_coll_pt as varchar(5000)) as nacha_050_coll_pt,
cast(nacha_5 as varchar(5000)) as nacha_5

    FROM "genaipoc"."SRC2_INPUT1"
    WHERE 
 "nacha_5" = cast(:nacha_5 as varchar(100))	\
        
    
UNION 
SELECT 'SRC2_STG1',
nacha_050_coll_file_no,
dl_as_of_dt,
dl_source_cd,
nacha_050_dtl_par,
nacha_050_coll_btch_no,
ifw_eff_dt,
nacha_050_coll_pt,
nacha_5
    FROM "genaipoc"."SRC2_STG1"
    WHERE 
     "nacha_5" = cast(:nacha_5 as varchar(100))	\
    ;'''


#SRC2_FILE2 TO SRC2_STAGING_DATA2	

src2_Staging_data2='''SELECT 'STG2_INPUT2' as "Type",
cast(nacha_060_coll_file_no as varchar(5000)) as nacha_060_coll_file_no,
cast(dl_as_of_dt  as varchar(5000)) as dl_as_of_dt,
cast(dl_source_cd as varchar(5000)) as dl_source_cd,
cast(nacha_060_dtl_par as varchar(5000)) as nacha_060_dtl_par,
cast(nacha_060_coll_btch_no  as varchar(5000)) as nacha_060_coll_btch_no,
cast(ifw_eff_dt as varchar(5000)) as ifw_eff_dt,
cast(nacha_060_coll_pt as varchar(5000)) as nacha_060_coll_pt,
cast(nacha_6 as varchar(5000)) as nacha_6

    FROM "genaipoc"."SRC2_INPUT2"
    WHERE 
     "nacha_6" = cast(:nacha_6 as varchar(100))	\
    
UNION 
SELECT 'SRC2_INPUT2',*
    FROM "genaipoc"."SRC2_STG2"
WHERE 
     "nacha_6" = cast(:nacha_6 as varchar(100))	\
    ;'''

src_stg_Exception='''select * from "genaipoc"."EXCEPTION_TBL"
where tran_ref_no=:tran_ref_no ;
'''

lineage={}

def print_response(db_response: str, description: str):
    """
    Processes the database response and sends data as JSON.
    """
    try:
        if db_response and len(db_response) > 0:
            # Convert db_response string to a DataFrame
            choice_default_mod = pd.DataFrame.from_dict(eval(db_response))
            # Convert the DataFrame to a list of dictionaries
            data = choice_default_mod.to_dict(orient="records")
        else:
            data = None  # No data available
        
        # Update the lineage dictionary with description and data
        # lineage['lineage'] = {"description": description, "data": data}

        # Return the response
        return {"description": description, "data": data}
    
    except Exception as e:
        # Handle errors and return error description
        return {"description": f"Error: {str(e)}", "data": None}
    


def display_lineage(order,txn_ref_no):
    lineage['lineage'] = []  # Clear the 'lineage' list
    lineage['cypher'] = []  # Clear the 'cypher' list
    lkp_tran_ref_no=dict()
    nacha_5=''
    nacha_6=''
    lkp_tran_ref_no_Values=SQLUtility.execute(GET_ADDITIONAL_PARAMS,parameters={'txn_ref_no':txn_ref_no})
    lst_value=[]
    if(lkp_tran_ref_no_Values is not None and len(lkp_tran_ref_no_Values)>0):
         lst_value=eval(lkp_tran_ref_no_Values)
         print(len(lst_value))
    if(len(lst_value)==0):
        lineage['lineage'].append(print_response(None,'No Matching records found for '+txn_ref_no))
       # exit(0)
    else:
        lkp_tran_ref_no=lst_value[0]['lkp_tran_ref_no']
        nacha_value=SQLUtility.execute(GET_NACHA_PARAMS,parameters={'lkp_tran_ref_no':lkp_tran_ref_no})
        lst_nacha_values=[]
        if(nacha_value is not None and len(nacha_value)>0):
            lst_nacha_values=eval(nacha_value)
            if(len(lst_nacha_values)==0):
                lineage['lineage'].append(print_response(None,'Nacha Params unavailable'))
                #exit(0)
            else:
                nacha_5=lst_nacha_values[0]['nacha_5']
                nacha_6=lst_nacha_values[0]['nacha_6']
    #st.markdown('**Values Parsed**: txn_ref_no:{0} ,lkp_tran_ref_no:{1}, nacha5:{2} , nacha6:{3}'
     #        .format(txn_ref_no,lkp_tran_ref_no,nacha_5,nacha_6))
    
    #print(json.loads(param_value))
    #Bottom to Top
    is_full_lineage=True
    request_type=LineageType.get_lineage_type(LineageType.TOP_TO_BOTTOM_FULL_LINEAGE.value)
    csa_fl=0,
    # pre_csa=0,stitch=0,kde1=0,kde2=0,stg2=0,stg1=0,src1=0,src2=0
    if(order == 1):
        request_type=LineageType.get_lineage_type(LineageType.BOTTOM_TO_TOP_FULL_LINEAGE.value)
        
        # response=SQLUtility.execute(stg_src1_query,parameters={'txn_ref_no':txn_ref_no})
        # print_response(response,'Source 1 to Stage')
        
        response=SQLUtility.execute(src1_Staging_data,parameters={'txn_ref_no':txn_ref_no})
        lineage['lineage'].append(print_response(response,'Source 1 Staging data'))
       
        response=None
        if(len(nacha_6)>0 ):
            response=SQLUtility.execute(src2_Staging_data2,parameters={'nacha_6':nacha_6})
        lineage['lineage'].append(print_response(response,'Source 2 to Staging Data - 2'))
       
        response=None
        if (len(nacha_5) >0):
            response=SQLUtility.execute(src2_Staging_data,parameters={'nacha_5':nacha_5})
        lineage['lineage'].append(print_response(response,'Source 2 to Staging Data - 1' ))
     
        response=SQLUtility.execute(stg_src2_KDE_query,parameters={'nacha_5':nacha_5,'nacha_6':nacha_6})
        lineage['lineage'].append(print_response(response,'Stage Source 2 to KDE'))
        
        response=SQLUtility.execute(stg_src1_KDE_query,parameters={'txn_ref_no':txn_ref_no})
        lineage['lineage'].append(print_response(response,'Stage Source 1 to KDE'))

        response=SQLUtility.execute(KDE_To_Stitch_query,parameters={'txn_ref_no':txn_ref_no})
        lineage['lineage'].append(print_response(response,'KDE to Stitching'))
        
        response= SQLUtility.execute(src1_kde_to_holding,parameters={'tran_ref_no':txn_ref_no})
        lineage['lineage'].append(print_response(response,'KDE 1 to Holding table'))
        if(response is not None):
            is_full_lineage=False 
        
        response= SQLUtility.execute(src1_KDE_Orphan,parameters={'txn_ref_no':txn_ref_no})
        lineage['lineage'].append(print_response(response,'KDE 1 to Orphan table'))
        if(response is not None and len(response)>0):
            request_type=LineageType.TOP_TO_BOTTOM_ORPHAN.name
            is_full_lineage=False

        response=SQLUtility.execute(stitch_to_precsa_query,parameters={'txn_ref_no':txn_ref_no})
        lineage['lineage'].append(print_response(response,'Stitching to Pre CSA'))

        response=SQLUtility.execute(precsa_csa,parameters={'txn_ref_no':txn_ref_no})
        lineage['lineage'].append(print_response(response,'Pre CSA to CSA'))

        resp=SQLUtility.execute(query,parameters={'txn_ref_no':txn_ref_no})
        lineage['lineage'].append(print_response(resp,'CSA'))
        if resp is not None and len(csa_fl)>0:
            csa_fl=1
        #Top to Bottom
        
        # st.markdown("**Cypher Query**")
        # print(request_type)
        qq=''
        qq=cypher_template.SOURCE1_GENERIC_QUERY
        val1=qq.format(txn_ref_no)
        # st.code(val1, language="cypher")
        lineage['cypher'].append(val1)
        if(is_full_lineage==True):
            request_type=LineageType.get_lineage_type(LineageType.TOP_TO_BOTTOM_FULL_LINEAGE.value)

        return lineage
            
    elif order == 2:
        resp=SQLUtility.execute(query,parameters={'txn_ref_no':txn_ref_no})
        lineage['lineage'].append(print_response(resp,'CSA'))
        if resp is not None and len(csa_fl)>0:
            csa_fl=1
       
        response=SQLUtility.execute(precsa_csa,parameters={'txn_ref_no':txn_ref_no})
        lineage['lineage'].append(print_response(response,'Pre CSA to CSA'))

        response=SQLUtility.execute(stitch_to_precsa_query,parameters={'txn_ref_no':txn_ref_no})
        lineage['lineage'].append(print_response(response,'Stitching to Pre CSA'))

        response=SQLUtility.execute(KDE_To_Stitch_query,parameters={'txn_ref_no':txn_ref_no})
        lineage['lineage'].append(print_response(response,'KDE to Stitching'))
        
        response=None
        response= SQLUtility.execute(src1_KDE_Orphan,parameters={'txn_ref_no':txn_ref_no})
        lineage['lineage'].append(print_response(response,'KDE 1 to Orphan table'))
        if(response is not None and len(response)>0):
            request_type=LineageType.TOP_TO_BOTTOM_ORPHAN.name
            is_full_lineage=False
        
        response= SQLUtility.execute(src1_kde_to_holding,parameters={'tran_ref_no':txn_ref_no})
        lineage['lineage'].append(print_response(response,'KDE 1 to Holding table'))
        if(response is not None and  len(response)>0):
            request_type=LineageType.TOP_TO_BOTTOM_HOLDING.name
            is_full_lineage=False

        
        response=SQLUtility.execute(stg_src1_KDE_query,parameters={'txn_ref_no':txn_ref_no})
        lineage['lineage'].append(print_response(response,'Stage Source 1 to KDE'))
        
        response=None
        if (len(nacha_5) >0 and len(nacha_6)>0):
            response=SQLUtility.execute(stg_src2_KDE_query,parameters={'nacha_5':nacha_5,'nacha_6':nacha_6})
        lineage['lineage'].append(print_response(response,'Stage Source 2 to KDE'))
        
        response=SQLUtility.execute(src_stg_Exception,parameters={'tran_ref_no':txn_ref_no})
        lineage['lineage'].append(print_response(response,'Source to Stage Exception'))
        
        if(response is not None and len(response)>0):
            request_type=LineageType.TOP_TO_BOTTOM_STITCH_EXCEPTION.name
            is_full_lineage=False
            
        
        response=None
        if (len(nacha_5) >0):
            response=SQLUtility.execute(src2_Staging_data,parameters={'nacha_5':nacha_5})
        lineage['lineage'].append(print_response(response,'Source 2 to Staging Data - 1' ))
        response=None
        if(len(nacha_6)>0 ):
            response=SQLUtility.execute(src2_Staging_data2,parameters={'nacha_6':nacha_6})
        lineage['lineage'].append(print_response(response,'Source 2 to Staging Data - 2'))
        
        response=SQLUtility.execute(src1_Staging_data,parameters={'txn_ref_no':txn_ref_no})
        lineage['lineage'].append(print_response(response,'Source 1 to Staging data'))
       # response=SQLUtility.execute(stg_src1_query,parameters={'txn_ref_no':txn_ref_no})
        #print_response(response,'Stage to Source 1')
        
        # st.markdown("**Cypher Query**")
        print(request_type)
        qq=''
        # match request_type:
        #     case LineageType.TOP_TO_BOTTOM_FULL_LINEAGE.name:
        #         qq= cypher_template.TOP_TO_BOTTOM_FULL_LINEAGE
        #     case LineageType.TOP_TO_BOTTOM_FILTER.name:
        #         qq=cypher_template.TOP_TO_BOTTOM_FILTERED_TRANSACTIONS
        #     case LineageType.TOP_TO_BOTTOM_HOLDING.name:
        #         qq=cypher_template.TOP_TO_BOTTOM_HOLDING
        #     case LineageType.TOP_TO_BOTTOM_STITCH_EXCEPTION.name:
        #         qq=cypher_template.TOP_TO_BOTTOM_STITCH_EXPECTION
        #     case LineageType.TOP_TO_BOTTOM_ORPHAN.name:
        #         qq=cypher_template.TOP_TO_BOTTOM_ORPHAN
        #print(qq)
        qq=cypher_template.SOURCE1_GENERIC_QUERY
        val1=qq.format(txn_ref_no)
        # st.code(val1, language="cypher")
        lineage['cypher'].append(val1)

        if(is_full_lineage==True):
            request_type= LineageType.TOP_TO_BOTTOM_FULL_LINEAGE.name

        return lineage
    
    # if (csa_fl==1 and (request_type== LineageType.TOP_TO_BOTTOM_FULL_LINEAGE.name or request_type== LineageType.BOTTOM_TO_TOP_FULL_LINEAGE.name)):
    #     try:
    #         print('Plotting Graph')
    #         # Use a simpler query that only uses existing nodes and relationships
    #         var2 = """
    #         MATCH  (A:SRC1_INPUT1)- [:Extr_from_Src1data1_to_stg1]->(B:SRC1_STG)
    #         MATCH  (E:SRC2_INPUT1)- [:Extr_from_Src2File1_to_src2st1]->(G:SRC2_STG1)
    #         MATCH  (F:SRC2_INPUT2)- [:Extr_from_Src2File2_to_src2stg2]->(H:SRC2_STG2)
    #         MATCH  (G:SRC2_STG1)- [:Extr_from_Src2Stg1_to_kde2]->(I:KDE2)
    #         MATCH  (H:SRC2_STG2)- [:Extr_from_Src2Stg2_to_kde2]->(I:KDE2)
    #         MATCH  (B:SRC1_STG)- [:Extr_from_Src1Stg1_to_kde1]->(C:KDE1)
    #         MATCH  (C:KDE1)- [:Extr_from_kde1_to_stich]->(D:STITCH)
    #         MATCH  (I:KDE2)- [:Extr_from_kde2_to_Stitch]->(D:STITCH)
    #         MATCH  (D:STITCH)- [:Extr_from_stitch]->(J:PRECSA)
    #         MATCH  (J:PRECSA)- [:Extr_from_precsa]->(K:CSA)
    #         WHERE (substring('0000',0,case size(A.acc_9_ctl1)  when 1 then 3   when 2 then 2  when 3 then 1  when 4 then 0  end)+ 
    #         A.acc_9_ctl1   + substring('0000',0,CASE size(A.acc_9_ctl2)   when 1 then 3   when 2 then 2  when 3 then 1  when 4 then 0   end)
    #         + A.acc_9_ctl2    + substring('0000',0,CASE size(A.acc_9_ctl3)   when 1 then 3   when 2 then 2  when 3 then 1  when 4 then 0   end)
    #         + A.acc_9_ctl3   + substring('0000',0, CASE size(A.acc_9_ctl4)  when 1 then 3   when 2 then 2  when 3 then 1  when 4 then 0   end) + 
    #         A.acc_9_ctl4  + substring('0000000000',0,CASE size(A.acc_9_acct) when 1 then 9   when 2 then 8  when 3 then 7  when 4 then 6 when 5 then 5 
    #         when 6 then 4  when 7 then 3  when 8 then 2  when 9 then 1   when 10 then 0 end ) + A.acc_9_acct  + A.acc_9_ccyyddd + A.acc_9_rec_seq )
    #         ='{0}'
    #         Return A, B,C,D,E,F,G,H,I,J,K
    #         """.format(txn_ref_no)
            
    #         # Get the graph visualization
    #         fig = pg.get_graph_in_streamlit(var2, order)
            
    #         # Check if fig is None before using it
    #         if fig is not None:
    #             fig.update_layout(coloraxis_showscale=False)
    #             st.plotly_chart(fig, use_container_width=True)
    #         else:
    #             st.warning("No graph data available to visualize. Please check Neo4j connection and data.")
                
    #     except Exception as ex:
    #         print("Error plotting Graph: " + str(ex))
    #         st.error(f"Error plotting graph: {str(ex)}")
        
        
# def get_the_results(order,txn_ref_no):
    
#     results_counter=st.session_state.get('get_results',0)
#     print(results_counter)
#     if(results_counter>=1):
#         exit()
#     st.session_state.get_results=1
    
#     print('=================================================')
#     parsed_order=''
#     parsed_txnrefno=''
#     print(order)
#     print(txn_ref_no)
#     if(type(order) is dict):
#         print('Order is DICT')
#         parsed_order=order['title']
#         if type(parsed_order) is not int and 'type' in order:
#             parsed_order=order['type']
#     else:
#         parsed_order=order
    
#     if(type(txn_ref_no) is dict):
#         print('txn_ref_no is DICT')
#         parsed_txnrefno=txn_ref_no['title']
#     else:
#         parsed_txnrefno=txn_ref_no
    
#     display_lineage(parsed_order,parsed_txnrefno)
    
# def look_for_records(q):
#     try:
#         print(q)
#         print('inside look_for_records')

#     except:
#          print('exception occured')


def get_the_results(order, txn_ref_no):
    results_counter = 0  # Removed Streamlit session state dependency
    print(results_counter)
    
    if results_counter >= 1:
        exit()
    
    results_counter = 1  # Removed Streamlit session state update

    print('=================================================')
    parsed_order = ''
    parsed_txnrefno = ''
    print(order)
    print(txn_ref_no)

    if isinstance(order, dict):
        print('Order is DICT')
        parsed_order = order.get('title', '')
        if not isinstance(parsed_order, int) and 'type' in order:
            parsed_order = order['type']
    else:
        parsed_order = order

    if isinstance(txn_ref_no, dict):
        print('txn_ref_no is DICT')
        parsed_txnrefno = txn_ref_no.get('title', '')
    else:
        parsed_txnrefno = txn_ref_no

    lineage_result= display_lineage(parsed_order, parsed_txnrefno)
    # return json.dumps(lineage_result, indent=4)
    return lineage_result



def look_for_records(q):
    try:
        print(q)
        print('inside look_for_records')
    except Exception as e:
        print('Exception occurred:', e)
