import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import datetime, timedelta
from QueryJobs import QueryJobs

class MapAllLeads():

    def __init__(self,
                 queryAllLeads,
                 queryAllDeals):
        self.queryAllLeads = queryAllLeads
        self.queryAllDeals = queryAllDeals

    def pull_jobs_db(self,query_string):
        query_string = " ".join(map(str,query_string))
        qs = QueryJobs(query_string)
        df = qs.getData()
        return df

    def readAllLeads(self):

        df_leads = self.pull_jobs_db(self.queryAllLeads)
        df_deals = self.pull_jobs_db(self.queryAllDeals)
        return df_leads, df_deals

    def processDealsAndLeads(self):
        plot = True
        df_leads, df_deals = self.readAllLeads()
        #identify time in which leads were uploaded
        df_leads1 = df_leads[df_leads.lead_source == 'Propensity Model']
        df_leads1['created_time_'] = pd.to_datetime(df_leads1.created_time).dt.date
        df_leads_report = pd.DataFrame(df_leads1.groupby(['created_time_','lead_status'])['created_time_'].count())
        df_leads_report.rename(columns={'created_time_':'count'},inplace=True)
        df_leads_report.reset_index(inplace=True)
        df_leads_report.set_index('created_time_',inplace=True)
        df_leads_report1 = pd.pivot(df_leads_report, columns='lead_status', values='count')
        fig, ax = plt.subplots()
        if(plot):
            for nm in ['Contact in Future','Convert','Customer Interested?','Lost','Lost lead','Not Contacted','Re-initiate contact']:
                ax.plot(df_leads_report1[nm],label=nm)
                ax.axvline('2021-04-')
                plt.xticks(rotation=45)
                ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
                ax.legend()
                ax.set_ylabel('count')
                ax.set_title('Leads performance metrics')
        df_leads1_actioned = df_leads1[(df_leads1.lead_status != 'Lost') & (df_leads1.lead_status.notnull())] #track these leads in deals from the creating date to date in whic deal was concluded
        #14 days since creation date
        df_leads1_actioned = df_leads1_actioned.copy(True)
        df_leads1_actioned['created_time_frwd'] = np.nan
        df_leads1_actioned['created_time_frwd'] = df_leads1_actioned.created_time_.apply(lambda x: x + timedelta(days=21))#next 21 days leads should convert into deal
        df_leads1_actioned = df_leads1_actioned[['company','last_name','business_reg_no','created_time_','created_time_frwd']]
        df_deals1 = df_deals[
            ['amount', 'business_reg_no', 'lead_source', 'created_time', 'modified_time']]
        df_leadsDeals = pd.merge(df_leads1_actioned,df_deals1,on='business_reg_no',how='left')
        #joining deals table only if the deal was created after create_time_ and before create_time_frwd
