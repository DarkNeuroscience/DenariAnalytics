class NarcoAnalytics_superseded():
    def filter_tax_year(data:pd.DataFrame,start_year,country='uk'):
        tax_dates = pd.read_csv(path + slash + "tax_years.csv")
        tax_dates['start date'] = tax_dates['start date'].fillna("01-01")
        tax_dates['end date'] = tax_dates['end date'].fillna("12-31")
        tax_dates['start date'] = '-' + tax_dates['start date']
        tax_dates['end date'] = '-' + tax_dates['end date']
        if pd.DataFrame(tax_dates.loc[tax_dates['nation'] == country]['tax year type'] == 'year').bool():
            end_year = str(start_year)
        else:
            end_year = str(start_year + 1)
        start_year = str(start_year)
        start_date = tax_dates.loc[tax_dates['nation'] == country]['start date'].values[0]
        end_date = tax_dates.loc[tax_dates['nation'] == country]['end date'].values[0]
        full_start_date = start_year + start_date
        full_end_date = end_year + end_date
        #data_output = NarcoAnalytics.filter_date_range(data,full_start_date,full_end_date)
        data_output = filter_date_range(data,full_start_date,full_end_date)
        return data_output
    
    def gr_totals(df,order_list,graph_type='pie'):
        df = pd.DataFrame(NarcoAnalytics.metric(df,'sum'))
        a = []
        # if len(order_list) == 0:
        #     b = pd.Series(df.index.unique()).sort_values().to_list()
        if graph_type == 'pie':
            for i in order_list:
                c = float(df[df.index == i][0])
                a.append(c)
                fig = go.Figure(data=[go.Pie(labels=order_list, values=df.loc[i], textinfo='label+percent',
                                             insidetextorientation='radial')])
        elif graph_type == 'bar':
            for i in order_list:
                c = go.Bar(name=i, x=order_list, y=df.loc[i])
                a.append(c)
            fig = go.Figure(data=a)
        elif graph_type == 'table':
            pass
        return fig
    
    def gr_t(df,metric='sum',colors='light-mild'):
        '''
        level 2

        '''
        df = pd.DataFrame(metric(df,metric))
        groups = df[0].tolist()
        x_ax = list(df.index.values)
        c = color_list(groups,color_pick(colors))
        fig = go.Figure(go.Bar(name='package', x=x_ax, y=groups, marker_color=c))
        fig.update_layout(barmode='group')
        return fig
    
    def group_period(df:pd.DataFrame,time_period,totals=["expenditure", "revenue","gross profit"],metric='sum'):
        if metric == 'sum':
            df = df.groupby([time_period])[totals].apply(lambda x : x.astype(float).sum())
        return df
    
class Montana_superseded():

    def gr_aggregate(df, time_column, categorised_column, number_column, metric='sum'):
    # Convert index to string
        if df.index.dtype == 'period[M]':
            df.index = df.index.strftime("%Y-%m")
        x_ax = list(df.index.values)

        # Group data by categorised_column and apply specified metric to number_column
        grouped = df.groupby(categorised_column)[number_column].agg(metric)

        # Create a single go.Bar object and update the y data for each group
        data = [go.Bar(name=group, x=x_ax, y=values) for group, values in grouped.items()]

        # Create go.Figure object and update layout
        fig = go.Figure(data)
        fig.update_layout(barmode='group')
        return fig