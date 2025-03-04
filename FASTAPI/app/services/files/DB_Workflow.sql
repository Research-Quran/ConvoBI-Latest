-- Active: 1736913254079@@localhost@5432@postgres@genaipoc
-- Create schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS "genaipoc";

--"genaipoc"."SRC1_STG1"
CREATE TABLE IF NOT EXISTS "genaipoc"."SRC1_STG1"
(
    acc_ctl1 character varying(5000) COLLATE pg_catalog."default",
    acc_ctl2 character varying(5000) COLLATE pg_catalog."default",
    acc_ctl3 character varying(5000) COLLATE pg_catalog."default",
    acc_ctl4 character varying(5000) COLLATE pg_catalog."default",
    acc_acct character varying(5000) COLLATE pg_catalog."default",
    acc_ccyyddd character varying(5000) COLLATE pg_catalog."default",
    acc_rec_seq character varying(5000) COLLATE pg_catalog."default",
    acc_id character varying(5000) COLLATE pg_catalog."default",
    acc_amt character varying(5000) COLLATE pg_catalog."default",
    acc_pst_dt character varying(5000) COLLATE pg_catalog."default",
    acc_usr_tr_cd character varying(5000) COLLATE pg_catalog."default",
    acc_type character varying(5000) COLLATE pg_catalog."default",
    acc_desc character varying(5000) COLLATE pg_catalog."default",
    acc_2_ctl1 character varying(5000) COLLATE pg_catalog."default",
    acc_2_ctl2 character varying(5000) COLLATE pg_catalog."default",
    acc_2_ctl3 character varying(5000) COLLATE pg_catalog."default",
    acc_2_ctl4 character varying(5000) COLLATE pg_catalog."default",
    acc_2_acct character varying(5000) COLLATE pg_catalog."default",
    acc_2_ccyyddd character varying(5000) COLLATE pg_catalog."default",
    acc_2_rec_seq character varying(5000) COLLATE pg_catalog."default",
    acc_2_amt character varying(5000) COLLATE pg_catalog."default",
    acc_2_pst_dt character varying(5000) COLLATE pg_catalog."default",
    acc_2_usr_tr_cd character varying(5000) COLLATE pg_catalog."default",
    acc_2_type character varying(5000) COLLATE pg_catalog."default",
    acc_2_univ_desc character varying(5000) COLLATE pg_catalog."default",
    acc_3_ctl1 character varying(5000) COLLATE pg_catalog."default",
    acc_3_ctl2 character varying(5000) COLLATE pg_catalog."default",
    acc_3_ctl3 character varying(5000) COLLATE pg_catalog."default",
    acc_3_ctl4 character varying(5000) COLLATE pg_catalog."default",
    acc_3_acct character varying(5000) COLLATE pg_catalog."default",
    acc_3_ccyyddd character varying(5000) COLLATE pg_catalog."default",
    acc_3_rec_seq character varying(5000) COLLATE pg_catalog."default",
    acc_3_amt character varying(5000) COLLATE pg_catalog."default",
    acc_3_usr_tr_cd character varying(5000) COLLATE pg_catalog."default",
    acc_3_type character varying(5000) COLLATE pg_catalog."default",
    acc_3_emp_id character varying(5000) COLLATE pg_catalog."default",
    acc_3_id character varying(5000) COLLATE pg_catalog."default",
    acc_ent_desc character varying(5000) COLLATE pg_catalog."default",
    acc_ent_dt character varying(5000) COLLATE pg_catalog."default",
    acc_9_ctl1 character varying(5000) COLLATE pg_catalog."default",
    acc_9_ctl2 character varying(5000) COLLATE pg_catalog."default",
    acc_9_ctl3 character varying(5000) COLLATE pg_catalog."default",
    acc_9_ctl4 character varying(5000) COLLATE pg_catalog."default",
    acc_9_acct character varying(5000) COLLATE pg_catalog."default",
    acc_9_ccyyddd character varying(5000) COLLATE pg_catalog."default",
    acc_9_rec_seq character varying(5000) COLLATE pg_catalog."default",
    acc_9_amt character varying(5000) COLLATE pg_catalog."default",
    acc_9_usr_tr_cd character varying(5000) COLLATE pg_catalog."default",
    acc_9_type character varying(5000) COLLATE pg_catalog."default",
    acc_desc_cd character varying(5000) COLLATE pg_catalog."default",
    acc_dt_cd character varying(5000) COLLATE pg_catalog."default",
    acc_9_univ_desc character varying(5000) COLLATE pg_catalog."default",
    acc_10_ctl1 character varying(5000) COLLATE pg_catalog."default",
    acc_10_ctl2 character varying(5000) COLLATE pg_catalog."default",
    acc_10_ctl3 character varying(5000) COLLATE pg_catalog."default",
    acc_10_ctl4 character varying(5000) COLLATE pg_catalog."default",
    acc_10_acct character varying(5000) COLLATE pg_catalog."default",
    acc_10_ccyyddd character varying(5000) COLLATE pg_catalog."default",
    acc_10_emp_id character varying(5000) COLLATE pg_catalog."default",
    acc_10_id character varying(5000) COLLATE pg_catalog."default",
    acc_10_rec_seq character varying(5000) COLLATE pg_catalog."default",
    acc_10_amt character varying(5000) COLLATE pg_catalog."default",
    acc_10_usr_tr_cd character varying(5000) COLLATE pg_catalog."default",
    acc_10_type character varying(5000) COLLATE pg_catalog."default",
    acc_ud_desc character varying(5000) COLLATE pg_catalog."default",
    dl_as_of_dt character varying(5000) COLLATE pg_catalog."default",
    dl_source_cd character varying(5000) COLLATE pg_catalog."default",
    acc_ident character varying(5000) COLLATE pg_catalog."default"
);



INSERT INTO "genaipoc"."SRC1_STG1"
SELECT  * FROM "genaipoc"."SRC1_INPUT1";



CREATE TABLE IF NOT EXISTS genaipoc."SRC2_STG1"
(
    nacha_050_coll_file_no character varying(5000) COLLATE pg_catalog."default",
	dl_as_of_dt character varying(5000) COLLATE pg_catalog."default",
	dl_source_cd character varying(5000) COLLATE pg_catalog."default",
    nacha_050_dtl_par character varying(5000) COLLATE pg_catalog."default",
   nacha_050_coll_btch_no character varying(5000) COLLATE pg_catalog."default",
    ifw_eff_dt character varying(5000) COLLATE pg_catalog."default",    
    nacha_050_coll_pt character varying(5000) COLLATE pg_catalog."default",
    nacha_5 character varying(5000) COLLATE pg_catalog."default"
);

INSERT INTO "genaipoc"."SRC2_STG1"
SELECT  * FROM "genaipoc"."SRC2_INPUT1";

CREATE TABLE IF NOT EXISTS "genaipoc"."SRC2_STG2"
(
    nacha_060_coll_file_no character varying(5000) COLLATE pg_catalog."default",
    dl_as_of_dt character varying(5000) COLLATE pg_catalog."default",
    dl_source_cd character varying(5000) COLLATE pg_catalog."default",
    nacha_060_dtl_par character varying(5000) COLLATE pg_catalog."default",
    nacha_060_coll_btch_no character varying(5000) COLLATE pg_catalog."default",
    ifw_eff_dt character varying(5000) COLLATE pg_catalog."default",
    nacha_060_coll_pt character varying(5000) COLLATE pg_catalog."default",
    nacha_6 character varying(5000) COLLATE pg_catalog."default"

);




INSERT INTO "genaipoc"."SRC2_STG2"
SELECT  * FROM "genaipoc"."SRC2_INPUT2";




CREATE TABLE IF NOT EXISTS "genaipoc"."SRC1_KDE"
(
    tran_amnt character varying(5000) COLLATE pg_catalog."default",
    bnf_acct_id character varying(5000) COLLATE pg_catalog."default",
    drcr_in character varying(5000) COLLATE pg_catalog."default",
    tran_val_dt character varying(5000) COLLATE pg_catalog."default",
    origntr_acct_id character varying(5000) COLLATE pg_catalog."default",
    tran_desc character varying(5000) COLLATE pg_catalog."default",
    tran_ref_no character varying(5000) COLLATE pg_catalog."default",
    tran_prod_type_cd_tmp character varying(5000) COLLATE pg_catalog."default",
    tran_acct1_tmp character varying(5000) COLLATE pg_catalog."default",
    tran_amt_tmp character varying(5000) COLLATE pg_catalog."default",
    tran_dt_tmp character varying(5000) COLLATE pg_catalog."default",
    tran_type_cd_tmp character varying(5000) COLLATE pg_catalog."default",
    dl_as_of_dt character varying(5000) COLLATE pg_catalog."default",
    dl_source_cd character varying(5000) COLLATE pg_catalog."default",
    bnf_acct_id_type character varying(5000) COLLATE pg_catalog."default",
    origntr_acct_id_type character varying(5000) COLLATE pg_catalog."default",
    acc_ident character varying(5000) COLLATE pg_catalog."default",
    tran_amnt_act_cur character varying(5000) COLLATE pg_catalog."default"
);

INSERT INTO "genaipoc"."SRC1_KDE" (tran_amnt, bnf_acct_id, drcr_in, tran_val_dt, origntr_acct_id, tran_desc, 
	tran_ref_no, tran_prod_type_cd_tmp, tran_acct1_tmp, tran_amt_tmp, tran_dt_tmp, tran_type_cd_tmp, dl_as_of_dt, 
	dl_source_cd, bnf_acct_id_type, origntr_acct_id_type, acc_ident, tran_amnt_act_cur
	)
	
select tran_amnt, bnf_acct_id, drcr_in, tran_val_dt, origntr_acct_id, tran_desc, 
	tran_ref_no, tran_prod_type_cd_tmp, tran_acct1_tmp, tran_amt_tmp, tran_dt_tmp, tran_type_cd_tmp, dl_as_of_dt, 
	dl_source_cd, bnf_acct_id_type, origntr_acct_id_type, acc_ident, tran_amnt_act_cur
	from (
	select 
	tran_amnt, bnf_acct_id, drcr_in, to_date(tran_val_dt,'YYYYMMDD') as tran_val_dt	, origntr_acct_id, tran_desc, 
	tran_ref_no, tran_prod_type_cd_tmp, tran_acct1_tmp, tran_amt_tmp, tran_dt_tmp as tran_dt_tmp	,
	tran_type_cd_tmp, dl_as_of_dt, dl_source_cd,
		case when bnf_acct_id is not null then 'IA' else null end as bnf_acct_id_type,
	case when origntr_acct_id is not null then 'IA' else null end as origntr_acct_id_type,
	acc_ident, tran_amnt_act_cur
	
	from (
select  
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
	cast(acc_amt as decimal(17,2)) end as  tran_amt_tmp,
	case when (acc_3_emp_id='EPIM' and acc_3_id='3') or (acc_10_emp_id='EPIM' and acc_10_id='10') then 
	to_date(lpad(cast(acc_pst_dt as varchar(6)),6,'0'),'MMDDYY')
	end as  tran_dt_tmp,
	
	case when (acc_3_emp_id='EPIM' and acc_3_id='3') or (acc_10_emp_id='EPIM' and acc_10_id='10')
    then 'SRC1_SRC2_ACH' else 'SRC1_UNLINKED' end
     as tran_type_cd_tmp,
	to_date(dl_as_of_dt,'dd-MON-YY') as dl_as_of_dt,
	'SRC1' as dl_source_cd,

	acc_ident,
	case when acc_id='1' then acc_amt 
	when acc_id='3' then acc_3_amt
	when acc_id='10' then acc_10_amt
	when acc_id='9' then acc_9_amt
	when acc_id='2' then acc_2_amt
	else null end as tran_amnt_act_cur
	from (
SELECT 
	acc_ctl1, acc_ctl2, acc_ctl3, acc_ctl4, acc_acct, acc_ccyyddd, acc_rec_seq, acc_id, acc_amt,
	acc_pst_dt, acc_usr_tr_cd, acc_type, acc_desc, acc_2_ctl1, acc_2_ctl2, acc_2_ctl3, acc_2_ctl4, 
	acc_2_acct, acc_2_ccyyddd, acc_2_rec_seq, acc_2_amt, acc_2_pst_dt, acc_2_usr_tr_cd, acc_2_type, 
	acc_2_univ_desc, acc_3_ctl1, acc_3_ctl2, acc_3_ctl3, acc_3_ctl4, acc_3_acct, acc_3_ccyyddd, 
	acc_3_rec_seq, acc_3_amt, acc_3_usr_tr_cd, acc_3_type, acc_ent_desc, acc_ent_dt, acc_9_ctl1,
	acc_9_ctl2, acc_9_ctl3, acc_9_ctl4, acc_9_acct, acc_9_ccyyddd, acc_9_rec_seq, acc_9_amt,
	acc_9_usr_tr_cd, acc_9_type, acc_desc_cd, acc_dt_cd, acc_9_univ_desc, acc_10_ctl1, acc_10_ctl2, 
	acc_10_ctl3, acc_10_ctl4, acc_10_acct, acc_10_ccyyddd, acc_10_rec_seq, acc_10_amt, acc_10_usr_tr_cd, 
	acc_10_type, acc_ud_desc, dl_as_of_dt, dl_source_cd, acc_ident,acc_10_emp_id,acc_10_id,acc_3_emp_id	,acc_3_id

	FROM "genaipoc"."SRC1_STG1")STAGING1))t;

CREATE TABLE IF NOT EXISTS "genaipoc"."SRC2_KDE"
(
    drcr_in character varying(5000) COLLATE pg_catalog."default",
    origntr_acct_id character varying(5000) COLLATE pg_catalog."default",
    tran_acct1_tmp character varying(5000) COLLATE pg_catalog."default",
    tran_amt_tmp character varying(5000) COLLATE pg_catalog."default",
    tran_dt_tmp character varying(5000) COLLATE pg_catalog."default",
    dl_as_of_dt character varying(5000) COLLATE pg_catalog."default",
    dl_source_cd character varying(5000) COLLATE pg_catalog."default",
    txn_amt character varying(5000) COLLATE pg_catalog."default",
    acc_ident_nbr character varying(5000) COLLATE pg_catalog."default",
    tran_ref_no character varying(5000) COLLATE pg_catalog."default",
    nacha_5 character varying(5000) COLLATE pg_catalog."default",
    nacha_6 character varying(5000) COLLATE pg_catalog."default"
);




INSERT INTO "genaipoc"."SRC2_KDE" (
	DRCR_IN,ORIGNTR_ACCT_ID,TRAN_ACCT1_TMP,TRAN_AMT_TMP,TRAN_DT_TMP,DL_AS_OF_DT,DL_SOURCE_CD,TXN_AMT,ACC_IDENT_NBR,TRAN_REF_NO,NACHA_5,NACHA_6)

WITH SRC2_STG1_CTE AS (
SELECT nacha_050_coll_file_no, nacha_5, dl_as_of_dt, dl_source_cd, nacha_050_coll_btch_no, ifw_eff_dt, nacha_050_coll_pt
	FROM "genaipoc"."SRC2_STG1"
),
SRC2_STG2_CTE AS (	
SELECT nacha_060_coll_file_no,nacha_6, dl_as_of_dt, dl_source_cd, nacha_060_dtl_par, nacha_060_coll_btch_no, ifw_eff_dt, nacha_060_coll_pt
	FROM "genaipoc"."SRC2_STG2"
),
JOINS_SRC_CTES AS ( select b.*,a.* from SRC2_STG1_CTE a 
	join  SRC2_STG2_CTE b
	on a.nacha_050_coll_file_no=b.nacha_060_coll_file_no
	and a.nacha_050_coll_btch_no=b.nacha_060_coll_btch_no
	)
	select 
	drcr_in,origntr_acct_id,tran_acct1_tmp,tran_amt_tmp,tran_dt_tmp,dl_as_of_dt,dl_source_cd,txn_amt,acc_ident_nbr
	,tran_ref_no,nacha_5,nacha_6 
	from (
Select
drcr_in,
case when drcr_in='C' then substr(nacha_5,41,10)
		when drcr_in='D' and IAT_ind='Y' then substr(nacha_6, 40, 35)
		when drcr_in='D' and IAT_ind!='Y' then substr(nacha_6, 13, 17)
		end origntr_acct_id,
Case when IAT_ind='Y' then substr(substr(nacha_6,40,35),-17)
	else lpad(substr(nacha_6,13,17),17,'0')
	end tran_acct1_tmp,
case trim(substr(nacha_6, 30, 10))::text when '' then '0'	
	else cast(cast(trim(substr(nacha_6, 30, 10)) as bigint) /100.00 as decimal(17,2)) end  as tran_amt_tmp,

to_date(substr(nacha_5,70,6),'YYMMDD') as tran_dt_tmp,
(CURRENT_DATE-11) as dl_as_of_dt,
'SRC1' as dl_source_cd,
case trim(substr(nacha_6, 30, 10))::text when '' then '0'	
	else trim(substr(nacha_6, 30, 10))::text::integer/100 end as txn_amt,
Case when substr(nacha_5,51,3) in ('CIE','MTE') then trim(substr(nacha_6,55,15))
	when substr(nacha_5,51,3) ='POP' then trim(substr(nacha_6,40,15))
	when substr(nacha_5,51,3) ='SHR' then trim(substr(nacha_6,44,11))
	when substr(nacha_5,51,3) = 'IAT' then trim(substr(nacha_6 ,4,15)) 
	else  trim(substr(nacha_6,40,15)) end as  acc_ident_nbr,
 nacha_5,nacha_6, nacha_060_dtl_par  AS tran_ref_no
From
(
select case when substr(nacha_6,2,2) in ('21','62','23','22','54','53','52','51','44','43','42','41','34','33','32','31') then 'C'
	else 'D' end drcr_in,
	case when substr (nacha_5,51,3)='IAT' then 'Y'
	else 'N' end IAT_ind,
	a.*
from JOINS_SRC_CTES a
))  TMP ;







CREATE TABLE IF NOT EXISTS "genaipoc"."SRC1_STITCHED"
(
    bnf_acct_id character varying(5000) COLLATE pg_catalog."default",
    drcr_in character varying(5000) COLLATE pg_catalog."default",
    tran_val_dt character varying(5000) COLLATE pg_catalog."default",
    origintr_acct_id character varying(5000) COLLATE pg_catalog."default",
    tran_desc character varying(5000) COLLATE pg_catalog."default",
    tran_prod_type_cd_tmp character varying(5000) COLLATE pg_catalog."default",
    tran_ref_no character varying(5000) COLLATE pg_catalog."default",
    orig_dl_as_of_dt character varying(5000) COLLATE pg_catalog."default",
    dl_as_of_dt character varying(5000) COLLATE pg_catalog."default",
    dl_source_cd character varying(5000) COLLATE pg_catalog."default",
    txn_amt character varying(5000) COLLATE pg_catalog."default",
    tran_grp_cd_tmp character varying(5000) COLLATE pg_catalog."default",
    stitch_flag character varying(5000) COLLATE pg_catalog."default",
    tran_acct1_tmp character varying(5000) COLLATE pg_catalog."default",
    tran_amt_tmp character varying(5000) COLLATE pg_catalog."default",
    tran_dt_tmp character varying(5000) COLLATE pg_catalog."default",
    tran_type_cd_tmp character varying(5000) COLLATE pg_catalog."default",
    tran_amnt_act_cur character varying(5000) COLLATE pg_catalog."default",
    lkp_tran_ref_no character varying(5000) COLLATE pg_catalog."default"
);




INSERT INTO "genaipoc"."SRC1_STITCHED" (
	bnf_acct_id, drcr_in, tran_val_dt,  origintr_acct_id, tran_desc, tran_prod_type_cd_tmp 
	,tran_ref_no,  orig_dl_as_of_dt, dl_as_of_dt, dl_source_cd,  txn_amt
	,tran_acct1_tmp,  tran_amt_tmp,  tran_dt_tmp,lkp_tran_ref_no,stitch_flag,tran_grp_cd_tmp

	--	, tran_type_cd_tmp, tran_amnt_act_cur, lkp_tran_ref_no, tran_grp_cd_tmp, stitch_flag
)
	
WITH KDE1_CTE AS(
	SELECT tran_amnt, bnf_acct_id, drcr_in, tran_val_dt, origntr_acct_id, tran_desc, tran_ref_no, tran_prod_type_cd_tmp, tran_acct1_tmp, 
	tran_amt_tmp, tran_dt_tmp, tran_type_cd_tmp, dl_as_of_dt, dl_source_cd, bnf_acct_id_type, origntr_acct_id_type,
     acc_ident, tran_amnt_act_cur
	FROM "genaipoc"."SRC1_KDE"
)
,
KDE2_CTE AS(
SELECT drcr_in, origntr_acct_id, tran_acct1_tmp, tran_amt_tmp, tran_dt_tmp, dl_as_of_dt, dl_source_cd, txn_amt, acc_ident_nbr
	,tran_ref_no, nacha_5, nacha_6
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
,KDE1.tran_ref_no, KDE1.DL_AS_OF_DT , KDE1.dl_source_cd,KDE2.tran_ref_no as lkp_tran_ref_no
FROM "genaipoc"."SRC1_KDE" KDE1 JOIN "genaipoc"."SRC2_KDE" KDE2
ON  KDE1.tran_acct1_tmp = KDE2.tran_acct1_tmp AND 
	KDE1.tran_amt_tmp = KDE2.tran_amt_tmp 
    and KDE1.tran_dt_tmp = KDE2.tran_dt_tmp 
)  
SELECT bnf_acct_id, drcr_in, tran_val_dt, origntr_acct_id as origintr_acct_id, tran_desc, tran_prod_type_cd_tmp 
	,tran_ref_no, DL_AS_OF_DT AS orig_dl_as_of_dt, dl_as_of_dt, dl_source_cd, tran_amnt AS txn_amt
	,tran_acct1_tmp, tran_amnt as tran_amt_tmp, tran_val_dt  as tran_dt_tmp  ,
     lkp_tran_ref_no,1 as stitch_flag,'SRC1_SRC2_KDE' as tran_grp_cd_tmp
	--	, tran_type_cd_tmp, tran_amnt_act_cur, lkp_tran_ref_no, tran_grp_cd_tmp, stitch_flag
FROM KDE_JOINS

UNION

SELECT bnf_acct_id, drcr_in, tran_val_dt, origntr_acct_id as origintr_acct_id, tran_desc, tran_prod_type_cd_tmp 
	,tran_ref_no, DL_AS_OF_DT AS orig_dl_as_of_dt, dl_as_of_dt, dl_source_cd, tran_amnt AS txn_amt
	,tran_acct1_tmp, tran_amnt as tran_amt_tmp, tran_val_dt  as tran_dt_tmp 
	, tran_ref_no as lkp_tran_ref_no,0 as stitch_flag, 'SRC1_UNLINKED' as tran_grp_cd_tmp
FROM "genaipoc"."SRC1_KDE"
where tran_type_cd_tmp like '%UNLINKED';



CREATE TABLE IF NOT EXISTS "genaipoc"."PRE_FIN_ACC_TXNS"
(
    txn_ref_no character varying(5000) COLLATE pg_catalog."default",
    txn_value_date character varying(5000) COLLATE pg_catalog."default",
    account_number character varying(5000) COLLATE pg_catalog."default",
    drcr_indicator character varying(5000) COLLATE pg_catalog."default",
    txn_desc character varying(5000) COLLATE pg_catalog."default",
    tran_prod_type_cd_tmp character varying(5000) COLLATE pg_catalog."default",
    txn_amt character varying(5000) COLLATE pg_catalog."default",
    fic_mis_date character varying(5000) COLLATE pg_catalog."default",
    dl_source_cd character varying(5000) COLLATE pg_catalog."default",
    tran_grp_cd_tmp character varying(5000) COLLATE pg_catalog."default",
    txn_amt_acy character varying(5000) COLLATE pg_catalog."default"
);




INSERT INTO "genaipoc"."PRE_FIN_ACC_TXNS" (
txn_ref_no, txn_value_date, account_number, drcr_indicator, txn_desc, tran_prod_type_cd_tmp,
	txn_amt, fic_mis_date, dl_source_cd, tran_grp_cd_tmp, txn_amt_acy
)
	
select tran_ref_no as txn_ref_no, fic_mis_date as txn_value_date, account_number, drcr_in as drcr_indicator, 
	tran_desc as txn_desc, tran_prod_type_cd_tmp,txn_amt, fic_mis_date, dl_source_cd, tran_grp_cd_tmp, 
	 tran_amnt_act_cur as txn_amt_acy
from ( 
SELECT tran_ref_no, dl_as_of_dt as fic_mis_date, 
	case when drcr_in='C' then bnf_acct_id else origintr_acct_id end as 
	account_number,tran_grp_cd_tmp, tran_val_dt, drcr_in, tran_desc, tran_prod_type_cd_tmp, txn_amt, tran_amnt_act_cur 
	, dl_source_cd
    FROM 	( 
	SELECT bnf_acct_id, drcr_in, tran_val_dt, origintr_acct_id, tran_desc, tran_prod_type_cd_tmp, 
          	tran_ref_no, orig_dl_as_of_dt, dl_as_of_dt, dl_source_cd, txn_amt, tran_grp_cd_tmp, stitch_flag, 
     tran_acct1_tmp, tran_amt_tmp, tran_dt_tmp, tran_type_cd_tmp,	tran_amnt_act_cur 
	FROM "genaipoc"."SRC1_STITCHED"
    where stitch_flag='1'
) TMP) tmp;


CREATE TABLE IF NOT EXISTS "genaipoc"."FIN_ACCT_TXNS"
(
    txn_ref_no character varying(5000) COLLATE pg_catalog."default",
    fic_mis_date character varying(5000) COLLATE pg_catalog."default",
    account_number character varying(5000) COLLATE pg_catalog."default",
    txn_value_date character varying(5000) COLLATE pg_catalog."default",
    drcr_indicator character varying(5000) COLLATE pg_catalog."default",
    txn_desc character varying(5000) COLLATE pg_catalog."default",
    tran_prod_type_cd_tmp character varying(5000) COLLATE pg_catalog."default",
    txn_amt character varying(5000) COLLATE pg_catalog."default",
    txn_amt_acy character varying(5000) COLLATE pg_catalog."default"
);


INSERT INTO "genaipoc"."FIN_ACCT_TXNS" (
txn_ref_no, fic_mis_date, account_number, txn_value_date, drcr_indicator, txn_desc, tran_prod_type_cd_tmp, txn_amt, txn_amt_acy
	
)
	
select txn_ref_no, fic_mis_date, account_number, txn_value_date, drcr_indicator, txn_desc, tran_prod_type_cd_tmp, txn_amt, txn_amt_acy
	from
"genaipoc"."PRE_FIN_ACC_TXNS";


CREATE TABLE IF NOT EXISTS "genaipoc"."SRC1_ORPHAN"
(
    tran_amnt character varying(5000) COLLATE pg_catalog."default",
    bnf_acct_id character varying(5000) COLLATE pg_catalog."default",
    drcr_in character varying(5000) COLLATE pg_catalog."default",
    tran_val_dt character varying(5000) COLLATE pg_catalog."default",
    origntr_acct_id character varying(5000) COLLATE pg_catalog."default",
    tran_desc character varying(5000) COLLATE pg_catalog."default",
    tran_ref_no character varying(5000) COLLATE pg_catalog."default",
    tran_prod_type_cd_tmp character varying(5000) COLLATE pg_catalog."default",
    tran_acct1_tmp character varying(5000) COLLATE pg_catalog."default",
    tran_amt_tmp character varying(5000) COLLATE pg_catalog."default",
    tran_dt_tmp character varying(5000) COLLATE pg_catalog."default",
    tran_type_cd_tmp character varying(5000) COLLATE pg_catalog."default",
    dl_as_of_dt character varying(5000) COLLATE pg_catalog."default",
    dl_source_cd character varying(5000) COLLATE pg_catalog."default",
    tran_grp_cd_stc character varying(5000) COLLATE pg_catalog."default",
    upd_dl_as_of_dt character varying(5000) COLLATE pg_catalog."default",
    bnf_acct_id_type character varying(5000) COLLATE pg_catalog."default",
    origntr_acct_id_type character varying(5000) COLLATE pg_catalog."default",
    acc_ident character varying(5000) COLLATE pg_catalog."default"
);

CREATE TABLE IF NOT EXISTS "genaipoc"."SRC1_HOLD"
(
    tran_amnt character varying(5000) COLLATE pg_catalog."default",
    bnf_acct_id character varying(5000) COLLATE pg_catalog."default",
    drcr_in character varying(5000) COLLATE pg_catalog."default",
    tran_val_dt character varying(5000) COLLATE pg_catalog."default",
    origntr_acct_id character varying(5000) COLLATE pg_catalog."default",
    tran_desc character varying(5000) COLLATE pg_catalog."default",
    tran_ref_no character varying(5000) COLLATE pg_catalog."default",
    tran_prod_type_cd_tmp character varying(5000) COLLATE pg_catalog."default",
    tran_acct1_tmp character varying(5000) COLLATE pg_catalog."default",
    tran_amt_tmp character varying(5000) COLLATE pg_catalog."default",
    tran_dt_tmp character varying(5000) COLLATE pg_catalog."default",
    tran_type_cd_tmp character varying(5000) COLLATE pg_catalog."default",
    bnf_acct_id_type character varying(5000) COLLATE pg_catalog."default",
    origntr_acct_id_type character varying(5000) COLLATE pg_catalog."default",
    acc_ident character varying(5000) COLLATE pg_catalog."default",
    dl_as_of_dt character varying(5000) COLLATE pg_catalog."default"
);


CREATE TABLE IF NOT EXISTS "genaipoc"."SRC2_HOLD"
(
    tran_amnt character varying(5000) COLLATE pg_catalog."default",
    bnf_acct_id character varying(5000) COLLATE pg_catalog."default",
    drcr_in character varying(5000) COLLATE pg_catalog."default",
    tran_val_dt character varying(5000) COLLATE pg_catalog."default",
    origntr_acct_id character varying(5000) COLLATE pg_catalog."default",
    tran_desc character varying(5000) COLLATE pg_catalog."default",
    tran_ref_no character varying(5000) COLLATE pg_catalog."default",
    tran_prod_type_cd_tmp character varying(5000) COLLATE pg_catalog."default",
    tran_acct1_tmp character varying(5000) COLLATE pg_catalog."default",
    tran_amt_tmp character varying(5000) COLLATE pg_catalog."default",
    tran_dt_tmp character varying(5000) COLLATE pg_catalog."default",
    tran_type_cd_tmp character varying(5000) COLLATE pg_catalog."default",
    bnf_acct_id_type character varying(5000) COLLATE pg_catalog."default",
    origntr_acct_id_type character varying(5000) COLLATE pg_catalog."default",
    acc_ident character varying(5000) COLLATE pg_catalog."default"
);



WITH NOT_STITCHED as
(
select tran_ref_no from "genaipoc"."SRC1_KDE"
where tran_type_cd_tmp like '%UNLINKED'
-- except
-- select tran_ref_no from "genaipoc"."SRC1_STITCHED"
)
INSERT INTO "genaipoc"."SRC1_HOLD"
SELECT 
tran_amnt,bnf_acct_id,drcr_in,tran_val_dt,origntr_acct_id,tran_desc,tran_ref_no,tran_prod_type_cd_tmp,tran_acct1_tmp,tran_amt_tmp,
	tran_dt_tmp,
	tran_type_cd_tmp,
	bnf_acct_id_type,
	origntr_acct_id_type,
	acc_ident	,
    dl_as_of_dt
FROM "genaipoc"."SRC1_KDE"
WHERE tran_ref_no in (select tran_ref_no from NOT_STITCHED);


INSERT INTO "genaipoc"."SRC1_ORPHAN"
SELECT * FROM "genaipoc"."SRC1_HOLD"
WHERE CASE 
    WHEN DL_AS_OF_DT ~ '^\d{4}-\d{2}-\d{2}$' 
    THEN CURRENT_DATE - cast(DL_AS_OF_DT as date) > 7
    ELSE false
    END;

UPDATE "genaipoc"."SRC1_ORPHAN" 
SET upd_dl_as_of_dt = CASE
    WHEN DL_AS_OF_DT ~ '^\d{4}-\d{2}-\d{2}$' 
    THEN cast(DL_AS_OF_DT as date) + 7
    ELSE NULL
    END;

DELETE FROM "genaipoc"."SRC1_HOLD"
WHERE CASE 
    WHEN DL_AS_OF_DT ~ '^\d{4}-\d{2}-\d{2}$' 
    THEN CURRENT_DATE - cast(DL_AS_OF_DT as date) > 7
    ELSE false
    END;


-- INSERT INTO "genaipoc"."SRC2_ORPHAN"
-- select * from "genaipoc"."SRC2_HOLD"
-- where CURRENT_DATE -  cast(DL_AS_OF_DT as date) > 7;



CREATE TABLE IF NOT EXISTS "genaipoc"."EXCEPTION_TBL"
(
    excpt_id character varying(5000) COLLATE pg_catalog."default",
    entity_cd character varying(5000) COLLATE pg_catalog."default",
    qc_id character varying(5000) COLLATE pg_catalog."default",
    concat_fld_val character varying(5000) COLLATE pg_catalog."default",
    col_nm character varying(5000) COLLATE pg_catalog."default",
    col_val character varying(5000) COLLATE pg_catalog."default",
    dl_as_of_dt character varying(5000) COLLATE pg_catalog."default",
    create_dt character varying(5000) COLLATE pg_catalog."default",
    run_id character varying(5000) COLLATE pg_catalog."default",
    tran_amnt character varying(5000) COLLATE pg_catalog."default",
    tran_ref_no character varying(5000) COLLATE pg_catalog."default"
);



insert into "genaipoc"."EXCEPTION_TBL" (excpt_id, entity_cd, qc_id, concat_fld_val, col_nm, col_val, dl_as_of_dt, create_dt, 
	run_id, tran_amnt, tran_ref_no)
select 
'excp1', 'entity_cd', 'qc_id', 
concat(tran_amnt, bnf_acct_id, drcr_in, tran_val_dt, origntr_acct_id, tran_desc, tran_ref_no, tran_prod_type_cd_tmp, tran_acct1_tmp, tran_amt_tmp, tran_dt_tmp, tran_type_cd_tmp, dl_as_of_dt, dl_source_cd ) as  concat_fld_val, 
'acc_ident' as col_nm, acc_ident  as col_val, dl_as_of_dt, dl_as_of_dt as create_dt, '21343' as run_id, tran_amnt, tran_ref_no
from  "genaipoc"."SRC1_KDE" where acc_ident is null
