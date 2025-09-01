select 
rank() over(partition by year(C.Dt) order by c.per_change desc) as [rnk]
,c.Per_Change
,c.Dt
from 
dbo.CPI_Data c 
order by [rnk] asc 
select 
row_number() over(order by c.per_change) as [row_num]
,c.Per_Change
,c.Dt
,dateadd(month, -4, getdate())
,datediff(MONTH, getdate(),dateadd(month, -4, getdate()))
from dbo.Labor_Force c 
--past 6 months
where  datediff(MONTH, c.Dt,dateadd(month, -6, getdate()))>=-6
and datediff(MONTH, c.Dt,dateadd(month, -6, getdate()))<=0
order by 
c.Dt desc 

insert into dbo.Labor

select Dt, count(*)
from dbo.Labor_Force f 
group by Dt
having count(*)=1


select 
*
into dbo.dups
from 
dbo.Active_WorkForce c 
where Month(c.Dt) between 1 and 6  and YEAR(c.Dt)=Year(getdate())
order by Dt desc 

select * from dbo.dups order by Dt desc

insert into dbo.dups values(6 , 'LNS11000000','2025-01-01'	,16054,	2)

select * from dbo.dups
select 
rank() over(order by Id asc )
,row_number() over(order by Dt asc)
,Per_Change
,Dt
from 
drop table dbo.dups
select * from dbo.dups 
order by Dt desc
select 
*
into dups
from dbo.Labor_Force
where datediff(month, dt, dateadd(month, -6, getdate()))>-6
and datediff(month, dt, dateadd(month, -6, getdate()))<=0

select * 
from dbo.dups

truncate table dbo.dups


--
select 
rank() over (order by Value desc)
,Value
from 
dbo.dups



select lag(c.Dt) over (order by c.Dt)
from dbo.dups c 
select 
row_number() over( partition by  Series_ID order by Dt)
,Value
from dbo.CPI_Data

select distinct Series_ID from dbo.CPI_Data

select Dt, count(*)
from 
dbo.dups
group by Dt
having count(*)>1

with x 
as 
(
select 
rank() over (order by Value) as [rnk]
,Dt
,Per_Change
,Value
from 
dbo.dups
order by [rnk]
select * from x where rnk=1
drop table #d
select 
*
into #d 
from dbo.dups
select count(*), Dt, Value, Per_Change from #d group by Dt, Value


select Dt, count(*)
from dbo.dups 
group by Dt
having count(*)>1

select * from dbo.dups order by Dt

delete from dbo.dups where Value=16054

