from extract_indeed import get_jobs as get_indeed_jobs #indeed 사이트에서 얻어오는 job
from so import get_jobs as get_so_jobs #stackoverflow 에서 얻어오는 job
from make_csv import save_to_file # csv로 저장하는 로직


#indeed_jobs = get_indeed_jobs()
so_jobs = get_so_jobs() 
indeed_jobs = get_indeed_jobs()
jobs = so_jobs+indeed_jobs
save_to_file(jobs)  