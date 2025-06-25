select 
s.spriden_id GID,
s.spriden_pidm P_PIDM,
case 
when p.spbpers_pref_first_name is not null 
  then 
  p.spbpers_pref_first_name || '[' || s.spriden_first_name || ']'
  else s.spriden_first_name end as first,
s.spriden_mi middle,
s.spriden_last_name last 
from spriden s, spbpers p
where s.spriden_change_ind is null
and s.spriden_id =:gid
and s.spriden_pidm = p.spbpers_pidm