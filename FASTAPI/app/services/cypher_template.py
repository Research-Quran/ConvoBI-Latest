TOP_TO_BOTTOM_FULL_LINEAGE='''MATCH  (A:SRC1_INPUT1)- [:Extr_from_Src1data1_to_stg1]->(B:SRC1_STG) 
MATCH  (E:SRC2_INPUT1)- [:Extr_from_Src2File1_to_src2st1]->(G:SRC2_STG1)
MATCH  (F:SRC2_INPUT2)- [:Extr_from_Src2File2_to_src2stg2]->(H:SRC2_STG2) 
MATCH  (G:SRC2_STG1)- [:Extr_from_Src2Stg1_to_kde2]->(I:KDE2) 
MATCH  (H:SRC2_STG2)- [:Extr_from_Src2Stg2_to_kde2]->(I:KDE2)  
MATCH  (B:SRC1_STG)- [:Extr_from_Src1Stg1_to_kde1]->(C:KDE1) 
MATCH  (C:KDE1)- [:Extr_from_kde1_to_stich]->(D:STITCH) 
MATCH  (I:KDE2)- [:Extr_from_kde2_to_Stitch]->(D:STITCH)  
MATCH  (D:STITCH)- [:Extr_from_stitch]->(J:PRECSA) 
MATCH  (J:PRECSA)- [:Extr_from_precsa]->(K:CSA) 
WHERE (substring('0000',0,
case size(A.acc_9_ctl1)  when 1 then 3   when 2 then 2  when 3 then 1  when 4 then 0  end)+
A.acc_9_ctl1   + substring('0000',0,CASE size(A.acc_9_ctl2)   when 1 then 3   when 2 then 2  when 3 then 1  when 4 then 0   end) +
A.acc_9_ctl2    + substring('0000',0,CASE size(A.acc_9_ctl3)   when 1 then 3   when 2 then 2  when 3 then 1  when 4 then 0   end) +
A.acc_9_ctl3   + substring('0000',0, CASE size(A.acc_9_ctl4)  when 1 then 3   when 2 then 2  when 3 then 1  when 4 then 0   end) +
A.acc_9_ctl4  + substring('0000000000',0,CASE size(A.acc_9_acct) when 1 then 9   when 2 then 8  when 3 then 7  when 4 then 6 when 5 then 5  
when 6 then 4  when 7 then 3  when 8 then 2  when 9 then 1   when 10 then 0 end ) + 
A.acc_9_acct  + A.acc_9_ccyyddd + A.acc_9_rec_seq )='{0}'
Return A, B,C,D,E,F,G,H,I,J,K'''

TOP_TO_BOTTOM_STITCH_EXPECTION='''MATCH  (A:SRC1_INPUT1)- [:Extr_from_Src1data1_to_stg1]->(B:SRC1_STG)
MATCH  (B:SRC1_STG)- [:Extr_from_Src1Stg1_to_kde1]->(C:KDE1)
MATCH  (B:SRC1_STG)- [:Extr_from_Src1Stg_to_excp]->(D:EXCEPTION)
WHERE (substring('0000',0,case size(A.acc_9_ctl1)  when 1 then 3   when 2 then 2  when 3 then 1  when 4 then 0  end)+
A.acc_9_ctl1   + substring('0000',0,CASE size(A.acc_9_ctl2)   when 1 then 3   when 2 then 2  when 3 then 1  when 4 then 0   end) +
A.acc_9_ctl2    + substring('0000',0,CASE size(A.acc_9_ctl3)   when 1 then 3   when 2 then 2  when 3 then 1  when 4 then 0   end) + 
A.acc_9_ctl3   + substring('0000',0, CASE size(A.acc_9_ctl4)  when 1 then 3   when 2 then 2  when 3 then 1  when 4 then 0   end) +
A.acc_9_ctl4  + substring('0000000000',0,CASE size(A.acc_9_acct) when 1 then 9   when 2 then 8  when 3 then 7  when 4 then 6 when 5 then 5  
when 6 then 4  when 7 then 3  when 8 then 2  when 9 then 1   when 10 then 0 end ) + A.acc_9_acct  +
A.acc_9_ccyyddd + A.acc_9_rec_seq )='{0}'
Return A, B,C,D
'''

TOP_TO_BOTTOM_FILTERED_TRANSACTIONS='''MATCH  (A:SRC1_INPUT1)- [:Extr_from_Src1data1_to_stg1]->(B:SRC1_STG)
WHERE (substring('0000',0,case size(A.acc_9_ctl1)  when 1 then 3   when 2 then 2  when 3 then 1  when 4 then 0  end)+ 
A.acc_9_ctl1   + substring('0000',0,CASE size(A.acc_9_ctl2)   when 1 then 3   when 2 then 2  when 3 then 1  when 4 then 0   end) + 
A.acc_9_ctl2    + substring('0000',0,CASE size(A.acc_9_ctl3)   when 1 then 3   when 2 then 2  when 3 then 1  when 4 then 0   end) + 
A.acc_9_ctl3   + substring('0000',0, CASE size(A.acc_9_ctl4)  when 1 then 3   when 2 then 2  when 3 then 1  when 4 then 0   end) + 
A.acc_9_ctl4  + substring('0000000000',0,CASE size(A.acc_9_acct) when 1 then 9   when 2 then 8  when 3 then 7  when 4 then 6 when 5 then 5   
when 6 then 4  when 7 then 3  when 8 then 2  when 9 then 1   when 10 then 0 end ) + A.acc_9_acct  + 
A.acc_9_ccyyddd + A.acc_9_rec_seq )='{0}'
Return A, B'''

TOP_TO_BOTTOM_ORPHAN='''MATCH  (A:SRC1_INPUT1)- [:Extr_from_Src1data1_to_stg1]->(B:SRC1_STG)
MATCH  (B:SRC1_STG)- [:Extr_from_Src1Stg1_to_kde1]->(C:KDE1)
MATCH  (C:KDE1)- [:Extr_from_kde1_to_stich]->(D:STITCH)
MATCH  (C:KDE1)- [:Extr_from_KD1_to_orphan]->(E:ORPHAN)
MATCH  (D:STITCH)- [:Extr_from_stitch]->(F:PRECSA)
MATCH  (F:PRECSA)- [:Extr_from_precsa]->(G:CSA)
WHERE (substring('0000',0,case size(A.acc_9_ctl1)  when 1 then 3   when 2 then 2  when 3 then 1  when 4 
then 0  end)+ A.acc_9_ctl1   + substring('0000',0,CASE size(A.acc_9_ctl2)   when 1 then 3   when 2 then 2 
when 3 then 1  when 4 then 0   end) + A.acc_9_ctl2    + substring('0000',0,CASE size(A.acc_9_ctl3)  
when 1 then 3   when 2 then 2  when 3 then 1  when 4 then 0   end) + A.acc_9_ctl3   + 
substring('0000',0, CASE size(A.acc_9_ctl4)  when 1 then 3   when 2 then 2  when 3 then 1  when 4 then 0  
end) + A.acc_9_ctl4  + substring('0000000000',0,CASE size(A.acc_9_acct) when 1 then 9   when 2 then 8 
when 3 then 7  when 4 then 6 when 5 then 5   when 6 then 4  when 7 then 3  when 8 then 2  when 9 then 1  
when 10 then 0 end ) + A.acc_9_acct  + A.acc_9_ccyyddd + A.acc_9_rec_seq )='{0}'
Return A, B,C,D,E,F,G
'''


TOP_TO_BOTTOM_HOLDING='''MATCH  (A:SRC1_INPUT1)- [:Extr_from_Src1data1_to_stg1]->(B:SRC1_STG)
MATCH  (E:SRC2_INPUT1)- [:Extr_from_Src2File1_to_src2st1]->(G:SRC2_STG1)
MATCH  (F:SRC2_INPUT2)- [:Extr_from_Src2File2_to_src2stg2]->(H:SRC2_STG2)
MATCH  (G:SRC2_STG1)- [:Extr_from_Src2Stg1_to_kde2]->(I:KDE2)
MATCH  (H:SRC2_STG2)- [:Extr_from_Src2Stg2_to_kde2]->(I:KDE2)
MATCH  (B:SRC1_STG)- [:Extr_from_Src1Stg1_to_kde1]->(C:KDE1)
MATCH  (C:KDE1)- [:Extr_from_kde1_to_stich]->(D:STITCH)
match(C:KDE1)- [:Extr_from_kde_to_hld] -> (L:HOLDING)
MATCH  (I:KDE2)- [:Extr_from_kde2_to_Stitch]->(D:STITCH)
MATCH  (D:STITCH)- [:Extr_from_stitch]->(J:PRECSA)
MATCH  (J:PRECSA)- [:Extr_from_precsa]->(K:CSA)
WHERE (substring('0000',0,case size(A.acc_9_ctl1)  when 1 then 3   when 2 then 2  when 3 then 1 
when 4 then 0  end)+ A.acc_9_ctl1   + substring('0000',0,CASE size(A.acc_9_ctl2)   when 1 then 3  
when 2 then 2  when 3 then 1  when 4 then 0   end) + A.acc_9_ctl2    + substring('0000',0,CASE size(A.acc_9_ctl3)   when 1 then 3 
when 2 then 2  when 3 then 1  when 4 then 0   end) + A.acc_9_ctl3   + substring('0000',0, CASE size(A.acc_9_ctl4)  when 1 then 3   
when 2 then 2  when 3 then 1  when 4 then 0   end) + A.acc_9_ctl4  + substring('0000000000',0,CASE size(A.acc_9_acct) when 1 then 9  
when 2 then 8  when 3 then 7  when 4 then 6 when 5 then 5   when 6 then 4  when 7 then 3  when 8 then 2 
when 9 then 1   when 10 then 0 end ) + A.acc_9_acct  + A.acc_9_ccyyddd + 
A.acc_9_rec_seq )='{0}'
Return A, B,C,D,E,F,G,H,I,J,K,L'''

SOURCE1_GENERIC_QUERY='''MATCH  (A:SRC1_INPUT1 ) WHERE (substring('0000',0,case size(A.acc_9_ctl1)
when 1 then 3   when 2 then 2  when 3 then 1  when 4 then 0  end)+ A.acc_9_ctl1   + 
substring('0000',0,CASE size(A.acc_9_ctl2)   when 1 then 3   when 2 then 2  when 3 then 1
when 4 then 0   end) + A.acc_9_ctl2    + substring('0000',0,CASE size(A.acc_9_ctl3) 
when 1 then 3   when 2 then 2  when 3 then 1  when 4 then 0   end) + A.acc_9_ctl3  
+ substring('0000',0, CASE size(A.acc_9_ctl4)  when 1 then 3   when 2 then 2  when 3 then 1 
when 4 then 0   end) + A.acc_9_ctl4  + substring('0000000000',0,CASE size(A.acc_9_acct) when 1 then 9  
when 2 then 8  when 3 then 7  when 4 then 6 when 5 then 5   when 6 then 4  when 7 then 3  when 8 then 2 
when 9 then 1   when 10 then 0 end ) + A.acc_9_acct  + A.acc_9_ccyyddd + A.acc_9_rec_seq )= '{0}'
MATCH (A)-[:Extr_from_Src1data1_to_stg1]->(B:SRC1_STG)
OPTIONAL MATCH (B)-[:Extr_from_Src1Stg1_to_kde1]->(C:KDE1)
OPTIONAL MATCH  (C)- [:Extr_from_kde1_to_stich]->(D:STITCH)
OPTIONAL MATCH  (D)- [:Extr_from_stitch]->(F:PRECSA)
OPTIONAL MATCH  (F)- [:Extr_from_precsa]->(G:CSA)
OPTIONAL MATCH  (L:KDE2)- [:Extr_from_kde2_to_Stitch]->(D)
OPTIONAL MATCH  (C)- [:Extr_from_KD1_to_orphan]->(M:ORPHAN)
OPTIONAL MATCH  (K:SRC2_STG2)- [:Extr_from_Src2Stg2_to_kde2]->(L)
OPTIONAL MATCH  (J:SRC2_STG1)- [:Extr_from_Src2Stg1_to_kde2]->(L)
OPTIONAL MATCH  (B)- [:Extr_from_Src1Stg_to_excp]->(E:EXCEPTION)
OPTIONAL MATCH  (H:SRC2_INPUT1) - [:Extr_from_Src2File1_to_src2st1]->(J)
OPTIONAL MATCH  (I:SRC2_INPUT2) - [:Extr_from_Src2File2_to_src2stg2]->(K)
Return A,B,C,D,F,G,L,K,J,E,H,I,M'''