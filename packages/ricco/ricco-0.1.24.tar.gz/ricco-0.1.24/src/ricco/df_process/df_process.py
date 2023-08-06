# encoding:GBK
import geopandas as gpd
import pandas as pd
from ricco import rdf
from ricco import reset2name


class Base(object):
    def __init__(self, df):
        if isinstance(df, str):
            self.df = rdf(df)
        elif isinstance(df, pd.DataFrame):
            self.df = df
        else:
            ValueError('������Dataframe��·��')


class Geo_data_process(Base):
    '''������'''
    def to_geo_df(self):
        self.df = gpd.GeoDataFrame(self.df)
        return self.df


class Data_process(Base, Geo_data_process):
    '''Dataframe��������'''

    # ��������
    def reset2name(self):
        '''���������в�������Ϊname'''
        self.df = reset2name(self.df)
        return self.df

    def rename(self, dic: dict):
        '''��������'''
        self.df.rename(columns=dic, inplace=True)
        return self.df

    # �����ļ�
    def to_gbk(self, filename: str):
        '''����codingΪgbk��csv�ļ�'''
        self.df.to_csv(filename, index=False, encoding='GBK')
        return self.df

    def to_utf8(self, filename: str):
        '''����codingΪgbk��csv�ļ�'''
        self.df.to_csv(filename, index=False, encoding='utf-8')
        return self.df

# if __name__ == '__main__':
    # df = rdf('�Ϻ����ص�λ.csv')
    # df = '�Ϻ����ص�λ.csv'
    #
    # a = Data_process(df)
    # a.reset2name()
    # a.to_gbk('tes2.csv')
    # a.rename({})
    # a.to_geo_df()
    # print(a.df)
