import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime as dt
slash = '/'
path = os.getcwd()
class NarcoAnalytics():
    #APPEARANCE
    def color_list(category_list,colors='basic'):
        sets = {'basic':['#FFA89E','#A4DEF5','#ACE1AD'],
                'one':['#60FA5A','#75AEFA','#FF8791','#FAF682','#FA69B9','#9B70A4','#FACC75']
               }
        a = len(category_list)
        col = ['lightslategray',] * a
        color_set = sets[colors]
        color_set = color_set[:a]
        for i in color_set:
            col[color_set.index(i)] = i
        return col
    
    #GENERAL
    def column_set(df,group,group_by,ascending=True):
        df = df.sort_values(group_by,ascending=ascending)
        a = pd.Series(df[group].unique()).to_list()
        return a
    
    #DATES/TIMES
    def set_dates(df:pd.DataFrame,date_name='date',date_index=False):
        #If date index == True...
        df[date_name] = pd.to_datetime(df[date_name], dayfirst = True)
        df.sort_values(by=date_name,inplace=True)           
        df.reset_index(inplace=True,drop=True)
        return df
    
    def split_dates(df:pd.DataFrame,date_column='date',format='numeric'):
        #If column type == index...
        if format == 'period':
            new_columns = {'year':pd.to_datetime(df[date_column]).dt.to_period('Y'),
                           'quarter':pd.to_datetime(df[date_column]).dt.to_period('Q'),
                           'month':pd.to_datetime(df[date_column]).dt.to_period('M'),
                           'week':df[date_column].dt.isocalendar().week,
                           'day':df[date_column].dt.day,
                           'weekday':df[date_column].dt.weekday
                           #'weekday':df[date_column].dt.day_name()
                          }
        elif format == 'numeric':
            new_columns = {'year':df[date_column].dt.year,
                           'quarter':df[date_column].dt.quarter,
                           'month':df[date_column].dt.month,
                           'week':df[date_column].dt.isocalendar().week,
                           'day':df[date_column].dt.day,
                           'weekday':df[date_column].dt.weekday
                          }
        elif format == 'named_period':
            new_columns = {'year':pd.to_datetime(df[date_column]).dt.to_period('Y'),
                           'quarter':pd.to_datetime(df[date_column]).dt.to_period('Q'),
                           'month':df[date_column].dt.month_name(),
                           'week':df[date_column].dt.isocalendar().week,
                           'day':df[date_column].dt.day,
                           'weekday':df[date_column].dt.day_name()
                          }
        elif format == 'named_numeric':
            new_columns = {'year':df[date_column].dt.year,
                           'quarter':df[date_column].dt.quarter,
                           'month':df[date_column].dt.month_name(),
                           'week':df[date_column].dt.isocalendar().week,
                           'day':df[date_column].dt.day,
                           'weekday':df[date_column].dt.day_name()
                          }
        keys = list(new_columns.keys())
        for i in keys:
            df.insert(loc = 1,
                      column = i,
                      value = new_columns[i])
        return df
    
    def create_date_range(first_date,last_date="today",split_dates=True,split_format='named_numeric',date_index=False):
        #Date Index
        dates = pd.date_range(first_date,pd.to_datetime("today"))
        date_range = pd.DataFrame(dates)
        date_range = date_range.rename(columns={0: 'date'})
        date_range['date'] = pd.to_datetime(date_range['date'])
        if date_index:
            date_range.set_index('date',inplace=True)
        if split_dates == True:
            date_range = split_dates(date_range,format=split_format)
        return date_range
    
    def filter_date_range_(data:pd.DataFrame,start_date,end_date):
        date_range = (data.index > start_date) & (data.index <= end_date)
        return data[date_range]
    
    def filter_date_range(df:pd.DataFrame, start_date, end_date, date_column='date'):
        if date_column not in df.columns:
            date_series = df.index
        else:
            date_series = df[date_column]
        df = df[(date_series >= start_date) & (date_series <= end_date)]
        return df
    
    #METRICS
    def metric_n(df,group_by,number_column,metric):
        df2 = pd.DataFrame()
        met = {'sum':df2.groupby(df[group_by])[number_column].sum(number_column),
               'mean':df2.groupby(df[group_by])[number_column].mean(number_column),
               'max':df2.groupby(df[group_by])[number_column].mean(number_column),
               'min':df2.groupby(df[group_by])[number_column].min(number_column),
               'count':df2.groupby(df[group_by])[number_column].count().astype(int)
              }
        return met[metric]
    def metric_column_single(df,column_name,metric='sum'):
        met = {'sum':df[column_name].sum(),
               'mean':df[column_name].mean(),
               'max':df[column_name].mean(),
               'min':df[column_name].min(),
               'count':df[column_name].count().astype(int)
              }
        return met[metric]
    
    def metric_columns(df,metric='sum'):
        output = {'sum':df.sum(),
                  'mean':df.mean(),
                  'max':df.max(),
                  'min':df.min(),
                  'std':df.std(),
                  'var':df.var(),
                  'mode':df.mode(),
                  'count':df.count()
                 }
        df2 = output[metric]
        df2 = pd.DataFrame(df2)
        return df2
    
    #AGGREGATE
    def aggregate_category(df,group_by,column_name,number_column,order_list,metric='sum'):
        '''
        level 1
        '''
        #DateIndex
        #Month,Year,Quarter
        a = order_list
        b = []
        for i in a:
            s = df.loc[df[column_name] == i]
            met = {'sum':s.groupby(df[group_by])[number_column].sum(number_column),
                   'mean':s.groupby(df[group_by])[number_column].mean(number_column),
                   'max':s.groupby(df[group_by])[number_column].mean(number_column),
                   'min':s.groupby(df[group_by])[number_column].min(number_column),
                   'count':s.groupby(df[group_by])[number_column].count().astype(int)
                  }
            s = met[metric]
            b.append(s.rename(i))

        df = pd.concat(b, axis=1)
        df = df.fillna(0)
        df = df.sort_values(by=group_by)
        return df
    
    def graph_index_columns(df,colors='one',barmode='group'):
        '''
        level 2

        '''
        if df.index.dtype == 'period[M]':
                df.index = df.index.strftime("%Y-%m").to_list()
        col_names = df.columns.values.tolist()
        index_names = df.index.values.tolist()
        index_names = list(map(str, index_names))
        colors = NarcoAnalytics.color_list(col_names,colors=colors)
        bars = []
        for i in col_names:
            bar = go.Bar(name=i, x=index_names, y=df[i], marker_color=colors[col_names.index(i)])
            bars.append(bar)
        fig = go.Figure(bars)
        fig.update_layout(barmode=barmode)
        #fig.update_layout(xaxis_type='date', xaxis_tickformat='%Y-%m')
        return fig
    
    def graph_metrics(df,graph_type='bar',colors='one'):
        index_names = df.index.values.tolist()
        index_names = list(map(str, index_names))
        values = df[0].tolist()
        colors = NarcoAnalytics.color_list(index_names,colors=colors)
        fig_type = {'pie': go.Pie(labels=index_names, values=values, marker_colors=colors, sort=False),
                    'bar': go.Bar(x=index_names, y=values, marker_color=colors)}
        fig = go.Figure(data=fig_type[graph_type])
        #if graph_type == 'pie':
            #fig = go.Figure(data=[go.Pie(labels=index_names, values=values, marker_colors=colors, sort=False)])
        return fig

    #CASH FLOW
    def gross_profit(df:pd.DataFrame):
        df["gross profit"] = df["revenue"] - df["expenditure"]
        return df
    
    def cash_cumulate(df:pd.DataFrame,gross_profit=True,expenditure=True,revenue=True,profit=True,gross_return=True):
        '''
        Requires Columns Named:
            'Expenditure'
            'Revenue'
            'Gross Profit'
            'Gross Return (%)'
        '''
        if expenditure:
            df["cumulative expenditure"] = df["expenditure"].cumsum()
        if revenue:
            df["cumulative revenue"] = df["revenue"].cumsum()
        if profit:
            df["cumulative profit"] = df["cumulative revenue"] - df["cumulative expenditure"]
        if gross_return:
            df["gross return (%)"] = df["cumulative profit"]/df["cumulative expenditure"] * 100
            df["gross return (%)"] = df["gross return (%)"].fillna(0)
        return df
    
    def metric(column,metric):
        if metric == 'sum':
            x = column.sum()
        elif metric == 'mean':
            x = column.mean()
        elif metric == 'max':
            x = column.max()
        elif metric == 'min':
            x = column.min()
        elif metric == 'std':
            x = column.std()
        elif metric == 'var':
            x = column.var()
        elif metric == 'mode':
            x = column.mode()
        elif metric == 'count':
            x = column.count()
        else:
            return 'error: incorrect metric input'
        return x

class Montana():
    def input_dropdown_micro(macro_period):
        micro_periods = {'year':['quarter','month','week','day','weekday'],
                         'quarter':['month','week','day','weekday','date'],
                         'month':['week','day','weekday','date'],
                         'week':['day','weekday','date'],
                        }
        options=[]
        for i in micro_periods[macro_period]:
            options.append({'label':i,'value':i})
        return options

    def input_dropdown_column_set(df,column):
        a = pd.Series(df[column].unique().astype(str)).to_list()
        options = []
        for i in a:
            options.append({'label':i,'value':i})
        return options
    
class TaxTools():
    def get_csv_for_dataframe(tax_name,tax_year='2021/2022'):
        '''options for UK tax_name
                'income tax'
                'employee ni'
                'corporate ni'
                'dividend rates'
                'student loans'
                'corporation tax'
                'employee ni bands'
                'corporate ni bands'
                'high income threshold'
                'dividend tax free allowance'
            options for tax_year
                '2021/2022'
                '2022/2023'
        '''
        path = os.getcwd()
        log_folder = path + '\\UK Tax Tables'
        tax_table_log = pd.read_csv(log_folder + '\\tax_name_log.csv')
        year = tax_table_log.loc[tax_table_log['tax name'] == tax_name, tax_year].item()
        tax = tax_table_log.loc[tax_table_log['tax name'] == tax_name, 'filename'].item()
        file_path = log_folder + year + tax
        a = pd.read_csv(file_path)
        return a

    #Universal Tax Tools LEVEL 0
    def create_table(tax_rates:pd.DataFrame):
        a = tax_rates.copy()
        a['threshold max'] = a['threshold min'].shift(-1)
        a = a[['threshold min','threshold max','rate']]
        a = a.fillna(np.inf)
        return a

    def marginal(cash,tax_table:pd.DataFrame):
        a = tax_table.copy()
        a.loc[-1] = [cash,cash,np.NaN]
        a.index = a.index + 1
        a = a.sort_index()
        a = a.sort_values(by=['threshold min'])
        a['threshold max'] = a['threshold max'].sort_values().values
        a = a.reset_index(drop=True)
        cut = a.index[a['threshold max'] == cash].tolist()
        cut = cut[0]
        a = a[a.index <= cut].copy()
        a['tax'] = (a['threshold max'] - a['threshold min']) * a['rate']
        a_total = a['tax'].sum()
        return a_total

    def marginalise(cash,table:pd.DataFrame):
        a = create_table(table)
        b = marginal(cash,a)
        return(b)

    def replace_threshold_rates(threshold_table:pd.DataFrame,rates:pd.DataFrame):
        a = threshold_table.copy()
        b = rates.copy()
        a['rate'] = b['rate']
        return a

    def interpret_single_df_value(df:pd.DataFrame):
        return int(df['value'])

    #UK Tax Tools LEVEL 1
    def interpret_tax_code_allowance(tax_code):
        a = ''.join([i for i in tax_code if i.isdigit()])
        a = int(a)
        a = a * 10
        return a

    def interpret_tax_code_ni_band(tax_code):
        a = ''.join([i for i in tax_code if not i.isdigit()])
        return a

    def adjust_allowance(salary,tax_allowance,tax_table:pd.DataFrame,tax_year):
        a = tax_table
        allowance_reduction = a.loc[1,'threshold min'] - tax_allowance
        a.loc[1,'threshold min'] = a.loc[1,'threshold min'] - allowance_reduction
        a.loc[2,'threshold min'] = a.loc[2,'threshold min'] - allowance_reduction
        b = get_csv_for_dataframe('high income threshold',tax_year)
        c = interpret_single_df_value(b)
        if salary > c:
            change_range = c + 2 * tax_allowance
            d = {'numbers': list(range(c,change_range + 1,2))}
            change_df = pd.DataFrame(data=d)
            change_df = change_df[change_df['numbers'] <= salary]
            allowance_chg = change_df.index[-1]
        else:
            allowance_chg = 0 
        a.loc[1,'threshold min'] = a.loc[1,'threshold min'] - allowance_chg
        a.loc[2,'threshold min'] = a.loc[2,'threshold min'] - allowance_chg
        return a

    def adjust_ni_band(tax_table:pd.DataFrame,ni_band_table:pd.DataFrame,ni_band):
        a = ni_band_table.copy()
        a = a[a['category'] == ni_band]
        a = a.transpose()
        a.columns = ['rate']
        a = a.reset_index(drop=True)
        a.drop([0], axis=0, inplace=True)
        a = a.reset_index(drop=True)
        b = tax_table.copy()
        b['rate'] = a['rate']
        return b

    def create_dividend_table(salary,tax_free_amount,tax_table:pd.DataFrame):
        a = tax_table.copy()
        a.loc[-1] = [(salary + tax_free_amount),np.NaN]
        a = a.sort_values(by=['threshold min'])
        a = a.reset_index(drop=True)
        a = a.fillna(method='ffill')
        cut = a.index[a['threshold min'] == salary + tax_free_amount].tolist()
        cut = cut[0]
        a = a[a.index >= cut]
        return a

    def create_student_loan_table(table:pd.DataFrame,plan):
        a = table.copy()
        a = a[a['category'] == plan]
        a = a[['threshold min','rate']]
        return a

    #UK Tax Laws LEVEL 2
    def employee_ni(salary,tax_code,tax_year):
        a = get_csv_for_dataframe('employee ni',tax_year)
        b = interpret_tax_code_ni_band(tax_code)
        c = get_csv_for_dataframe('employee ni bands',tax_year)
        d = adjust_ni_band(a,c,b)
        e = marginalise(salary,d)
        return e

    def income_tax(salary,tax_code,tax_year):
        a = get_csv_for_dataframe('income tax',tax_year)
        b = interpret_tax_code_allowance(tax_code)
        c = adjust_allowance(salary,b,a,tax_year)
        d = marginalise(salary,c)
        return d

    def corporate_ni(salary,tax_code,tax_year):
        a = get_csv_for_dataframe('corporate ni',tax_year)
        b = get_csv_for_dataframe('corporate ni bands',tax_year)
        c = interpret_tax_code_ni_band(tax_code)
        d = adjust_ni_band(a,b,c)
        e = marginalise(salary,d)
        return e

    def corporation_tax(gross_profit,tax_year):
        a = get_csv_for_dataframe('corporation tax',tax_year)
        b = marginalise(gross_profit,a)
        return b

    def dividend_tax(salary,dividend,tax_code,tax_year):
        a = get_csv_for_dataframe('income tax',tax_year)
        b = interpret_tax_code_allowance(tax_code)
        c = adjust_allowance(salary,b,a,tax_year)
        d = get_csv_for_dataframe('dividend rates',tax_year)
        e = replace_threshold_rates(c,d)
        f = get_csv_for_dataframe('dividend tax free allowance',tax_year)
        g = interpret_single_df_value(f)
        h = create_dividend_table(salary,g,e)
        take = salary + dividend
        i = marginalise(take,h)
        return i

    def student_loans(cash,plan,tax_year):
        a = get_csv_for_dataframe('student loans',tax_year)
        b = create_student_loan_table(a,plan)
        c = marginalise(cash,b)
        return c

    #UK Tax Calculation LEVEL 3
    def salary_taxes(salary,tax_code,student_loan_plan,tax_year,student_loan_second_plan='plan 0'):
        a = employee_ni(salary,tax_code,tax_year)
        b = income_tax(salary,tax_code,tax_year)
        c = corporate_ni(salary,tax_code,tax_year)
        d = student_loans(salary,student_loan_plan,tax_year)
        e = student_loans(salary,student_loan_second_plan,tax_year)
        total_student_loans = d + e
        salary_take = salary - a - b - total_student_loans
        employee_cost = salary + c
        d = {'Salary':[salary],
            'Employee National Insurance':[a],
            'Income Tax':[b],
            'Employer National Insurance':[c],
            'Student Loans':[total_student_loans],
            'Salary Takehome':[salary_take],
            'Total Employee Cost':[employee_cost]
            }
        return pd.DataFrame(data=d)

    #UK Tax Corporate Calculation LEVEL 4
    def ltd_owner_full_take(turnover,salary,expenses,tax_code,tax_year='2021/2022',student_loan_plan='plan 0',student_loan_second_plan='plan 0'):
        a = salary_taxes(salary,tax_code,'plan 0',tax_year).copy()
        turnover_deduct_expenses = turnover - expenses
        gross_profit = turnover - (expenses + salary)
        c = corporation_tax(gross_profit,tax_year)
        net_profit = gross_profit - c
        gross_take = salary + net_profit
        d = dividend_tax(salary,net_profit,tax_code,tax_year)
        div_take = net_profit - d
        e = student_loans(gross_take,student_loan_plan,tax_year)
        f = student_loans(gross_take,student_loan_second_plan,tax_year)
        total_student_loans = e + f
        a['Student Loans'] = total_student_loans
        total_take = int(a['Salary Takehome']) + div_take - total_student_loans
        percentage = total_take/turnover * 100
        i = {'Usable Funds':[turnover_deduct_expenses],
            'Corporation Tax':[c],
            'Dividend':[net_profit],
            'Dividend Tax':[d],
            'Dividend Takehome':[div_take],
            'Gross Take':[gross_take],
            'Total Takehome':[total_take],
            'Percentage Take':[percentage]
            }
        j = pd.DataFrame(i)
        a = a.join(j)
        return a

    #UK Tax Corporate Scenario Iteration LEVEL 5
    def iterate_salaries_ltd_take(turnover,min_salary,max_salary,expenses,iteration_step=1,tax_code='1257A',tax_year='2021/2022',student_loan_plan='plan 0',student_loan_second_plan='plan 0'):
        a = pd.DataFrame()
        for i in range(min_salary,max_salary + 1,iteration_step):
            b = ltd_owner_full_take(turnover,i,expenses,tax_code)
            a = pd.concat([a,b])
        a = a.reset_index(drop=True)
        return a

    def iterate_ltd_owner_full_take(turnover,expenses,tax_code='1257A',tax_year='2021/2022',student_loan_plan='plan 0',student_loan_second_plan='plan 0'):
        turnover_deduct_expenses = turnover - expenses
        a = iterate_salaries_ltd_take(turnover,0,turnover_deduct_expenses,expenses,1,tax_code,tax_year,student_loan_plan,student_loan_second_plan)
        return a

    #UK Tax Corporate Optimisation LEVEL 6
    def optimal_take(options:pd.DataFrame):
        a = options.copy()
        b = a[a['Total Takehome'] == a['Total Takehome'].max()]
        return b

    def optimise_ltd_owner_full_take(turnover,expenses,tax_code,tax_year='2021/2022',student_loan_plan='plan 0',student_loan_second_plan='plan 0'):
        a = iterate_ltd_owner_full_take(turnover,expenses,tax_code,tax_year,student_loan_plan)
        b = optimal_take(a)
        return(b)

    def optimise_lite_ltd_owner_full_take(turnover,expenses,tax_code,iteration_step=500,tax_year='2021/2022',student_loan_plan='plan 0',student_loan_second_plan='plan 0'):
        turnover_deduct_expenses = turnover - expenses
        a = iterate_salaries_ltd_take(turnover,0,turnover_deduct_expenses,expenses,iteration_step,tax_code,tax_year,student_loan_plan,student_loan_second_plan)
        optimal_row = a.index[a['Total Takehome'] == a['Total Takehome'].max()].tolist()
        optimal_range = [*range(optimal_row[0]-1,optimal_row[0]+2)]
        optimal_options = a.iloc[optimal_range]
        minn = int(optimal_options.iloc[[0]]['Salary'])
        maxx = int(optimal_options.iloc[[2]]['Salary'])
        b = iterate_salaries_ltd_take(turnover,minn,maxx,expenses,1,tax_code,tax_year,student_loan_plan,student_loan_second_plan)
        c = optimal_take(b)
        return c