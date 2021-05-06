import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import datetime, timedelta
from QueryJobs import QueryJobs
pd.set_option('display.max_rows',100)
pd.set_option('display.max_columns',100)

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
    def create_plot(self,
                    leads_plot_legends,
                    df):
        fig, ax = plt.subplots()
        for nm in leads_plot_legends:
            ax.plot(df[nm], label=nm)
            # ax.axvline('2021-04-')
            plt.xticks(rotation=45)
            ax.xaxis.set_major_locator(plt.MaxNLocator(20))
            ax.legend()
            ax.set_ylabel('count')
            ax.set_title('Leads performance metrics')
        plt.show()

    def processDealsAndLeads(self):
        # plot = True
        df_leads, df_deals = self.readAllLeads()
        #identify time in which leads were uploaded
        df_leads1 = df_leads[df_leads.lead_source == 'Propensity Model']
        df_leads1['created_time_'] = pd.to_datetime(df_leads1.created_time).dt.date

        df_deals1 = df_deals[['business_reg_no', 'lead_source', 'deal_source', 'created_time']]
        df_deals1 = df_deals1.copy(True)
        df_deals1['created_time_'] = pd.to_datetime(df_deals1.created_time).dt.date
        df_deals_report = pd.DataFrame(df_deals1.groupby(['created_time_','deal_source'])['created_time_'].count())
        df_deals_report.rename(columns={'created_time_':'count'},inplace=True)
        df_deals_report.reset_index(inplace=True)
        df_deals_report.set_index('created_time_',inplace=True)
        #set start date
        df_deals_report = df_deals_report.iloc[-100:,:]
        df_deals_report= df_deals_report.copy(True)
        df_deals_report1 = pd.pivot(df_deals_report,columns='deal_source', values='count').fillna(0)
        deals_plot_legends = df_deals_report.deal_source.unique().tolist()
        self.create_plot(deals_plot_legends, df_deals_report1)

        #converted leads
        converted_leads2 = pd.read_csv(
            "/home/simon/commerce_cube/ecom-ds-PropensityReporting/data/Leads_1620298191533_Sheet1.csv")
        converted_leads1 = pd.read_csv(
            "/home/simon/commerce_cube/ecom-ds-PropensityReporting/data/Leads_1620298033201_Sheet1.csv")
        converted_leads = pd.concat([converted_leads1, converted_leads2], axis=0)
        converted_leads.rename(columns={'Business Reg No':'business_reg_no','Created Time':'created_time_conv','Lead Status':'lead_status_conv',
                                        'Lead Source':'lead_source_conv'},inplace=True)
        df_deals1.business_reg_no = df_deals1.business_reg_no.astype('float')
        df_deals1.business_reg_no = df_deals1.business_reg_no.fillna(0).astype('int')
        df_deals1 = df_deals1[df_deals1.business_reg_no != 0]
        converted_leads.business_reg_no = converted_leads.business_reg_no.astype('int')
        #TODO: fuzzy match company in leads to account name in deals
        #TODO: fuzzy match company in converted leads custom view to deals
        #When deals are created, business_reg_no is not filled, but account_name has significant representation
        conv_leads_deals = pd.merge(converted_leads,df_deals1,on='business_reg_no',how='inner')

        df_leads_report = pd.DataFrame(df_leads1.groupby(['created_time_','lead_status'])['created_time_'].count())
        df_leads_report.rename(columns={'created_time_':'count'},inplace=True)
        df_leads_report.reset_index(inplace=True)
        df_leads_report.set_index('created_time_',inplace=True)
        df_leads_report1 = pd.pivot(df_leads_report, columns='lead_status', values='count').fillna(0)
        leads_plot_legends = ['Contact in Future','Convert','Customer Interested?','Lost','Lost lead','Not Contacted','Re-initiate contact']
        deals_plot_legends = []
        # self.create_plot(leads_plot_legends,df_leads_report1)
        # fig, ax = plt.subplots()
        # if(plot):
        #     for nm in ['Contact in Future','Convert','Customer Interested?','Lost','Lost lead','Not Contacted','Re-initiate contact']:
        #         ax.plot(df_leads_report1[nm],label=nm)
        #         # ax.axvline('2021-04-')
        #         plt.xticks(rotation=45)
        #         ax.xaxis.set_major_locator(plt.MaxNLocator(20))
        #         ax.legend()
        #         ax.set_ylabel('count')
        #         ax.set_title('Leads performance metrics')
        #     plt.show()
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
