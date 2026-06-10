#!/usr/bin/env python3
"""
treasury Extractor

data index:
* ???
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

from .extractor import ExtractorInterface

import requests
import pandas as pd

import time
from datetime import date
import xml.etree.ElementTree as ET
import re


class UsTreasuryExtractor(ExtractorInterface):
    """Interface for wrapper adapter"""

    _metadata_df = pd.DataFrame()

    def set_config(self, auth):
        """Set the authenticated wrapper."""
        self.wrapper_name = 'treasury'
        self.cache_path = None
        self.cache_file = None
        self._set_cache_path(auth, self.wrapper_name)
        self.data_group_mapping = {
            'nominal': self.get_nominal_yields,
            'real': self.get_real_yields
        }
    
    def get_raw(self, name):
        """Get data from API and return object of class DataFrame."""
        keys = list(self.urls.keys())
        tgt_keys = [key for key in keys if key.split('-')[0] == name]
        results = pd.DataFrame()
        for key in tgt_keys:
            item = self.urls[key]
            try:
                df = pd.read_excel(item['url'], skiprows=3, names=item['cols'])
            except Exception as e:
                print(e)
            results = pd.concat([df, results], ignore_index=True, axis=0)
            results.dropna(subset=['issue date'], inplace=True)
        return results
    
    def get_data(self, groups=[], from_date=None, to_date=None):
        """Get data from URL and return object of different classes."""
        df = pd.DataFrame()
        for group in groups:
            tmp_df = self.data_group_mapping[group]()
            df = pd.concat([df, tmp_df])
        return df
    
    def get_nominal_yields(self):
        """
        # Debt Yields

        Download XML files of the Archive (1990-2023) and Current (2023-Present) data for both raw, daily bill (Daily Treasury Bill Rates, Bank Discount Basis) and bond rates (Daily Treasury Long-Term Rates), then merge all the data into a continuous yield curve.

        Nominal Par Yield Curve uses mathematical 'bootstrap' model to convert those short-term yeilds into a standardized Bond/Coupon Equivalent Yield (365-day year).  This conversion is necessary so that short-term bills can be seamlessly compared to long-term notes and bonds on a single curve.

        'Nominal' vs. 'Real' Rates: the Nominal Par Yield Curve tracks standard government debt, which does not account for changes in consumer pricing.  The Daily Treasury Real Long-Term Rate Averages table relies exclusively on Treasury Inflation-Protected Securities (TIPS).  Because TIPS adjust their principle based on inflation metrics, their yields represent 'real' interest rates.

        Notes:
        * Monthly Statement of the Public Debt (MSPD) is an official, monthly report detailing the U.S. federal government's outstanding borrowing, including marketable and non-marketable debt, ownership, and the statutory debt limit.  Publised on the fourth business day of each month, this report tracks debt totals and maturities through the U.S. Treasury's Office of Accounting.
        * The 360 vs. 365 Day Distortion: Money market instruments (like T-Bills) use a raw bank discount method: \(\text{Price}=100\times \left(1-\frac{\text{Discount\ Rate}\times \text{Days}}{360}\right)\)
        * The Normalization Loop: The code injects the computed price asset back into a standard annualized equation based on a exact standard calendar year(\365\) days).  This elevates short-term percentages slightly, placing them on an equal mathematical footing with structural \(10\)-year and \(30\)-year coupon instruments.
        * Structural Visualization: the resulting plot_surface maps macro economic movements, visually separating flat regimes, steep growth

        * Concentration Density (The Log Scale Shift): marketable instruments (bills/notes/bonds) show high value concentration.  A small transaction count represents billions of dollars shifted during primary dealer auctions.  Non-Marketable structural items (such as consumer Savings Bonds) show low dollar density but huge piece counts.
        * Debt Proportions: The Pct_of_Total_National_Debt metric tracks institutional changes over time-documenting hwo the national debt has transformed to depend almost entirely on Marketable auctions rather than physical personal savings certifications.

        TODO:
        * on-the-run rates
        """
        # 1. Download Transaction Counts (Physical / Digital Instances Ledger)
        url_counts = "https://treasury.gov"
        print("Downloading electronic transaction counts (2002 - Present)...")
        df_counts = self.fetch_all_rates_pages(url_counts)

        # 2. Download Detailed Debt Volume (MSPO Breakdown Table)
        url_mspd = "https://treasury.gov"
        print("Downloading detailed public debt volume data...")
        df_mspd = self.fetch_all_rates_pages(url_mspd)

        # 3. Clean Transaction Counts Dataset
        df_counts['Date'] = pd.to_datetime(df_counts['record_date'])
        df_counts['Issued_Count'] = pd.to_numeric(df_counts['pieces_issued_cnt'], errors='coerce').fillna(0)
        df_counts['Redeemed_Count'] = pd.to_numeric(df_counts['pieces_redeemed_cnt'], errors='coerce').fillna(0)
        df_counts['Net_Count_Delta'] = df_counts['Issued_Count'] - df_counts['Redeemed_Count']

        # Normalize categories to line up wiht MSPD mapping
        df_counts['Sec_Group'] = 'Non-Marketable'
        df_counts.loc[df_counts['security_type_desc'].str.contains('Marketable', case=False, na=False), 'Sec_Group'] = 'Marketable'

        # Aggregate transaction to a monthly schedule
        df_counts_monthly = df_counts.groupby([df_counts['Date'].dt.to_period('M'), 'Sec_Group'])[['Issued_Count', 'Redeemed_Count', 'Net_Count_Delta']].sum().reset_index()
        df_counts_monthly['Date'] = df_counts_monthly['Date'].dt.to_timestamp()

        # 4. Clean and Transform MSPD Dataset
        df_mspd['Date'] = 'Non-Marketable'
        df_mspd.loc[df_mspd['security_class_desc'] == 'Marketable', 'Sec_Group'] = 'Marketable'

        # Calculation Total National Debt per month (Sum of all rows per reporting data)
        df_total_debt = df_mspd.groupby('Date')['total_mil_amt'].sum().reset_index().rename(columns={'total_mil_amt': 'Total_National_Debt_Millions'})
        # Calculate Oustanding Debt per specific Security Class
        df_sec_debt = df_mspd.groupby(['Date', 'Sec_Group'])['total_mil_amt'].sum().reset_index().rename(columns={'total_mil_amt': 'Security_Debt_Millions'})
        # Combine volume metrics into a unified debt sheet
        df_debt_unified = pd.merge(df_sec_debt, df_total_debt, on='Date', how='inner')
        # 5. Cross-Reference Counts with Dollar Volumes
        df_merged = pd.merge(df_counts_monthly, df_debt_unified, on=['Date', 'Sec_Group'], how='inner')
        # Compute Metrics: Percentage of National Debt and Dollar Concentration Density
        df_merged['Pct_of_Total_National_Debt'] = (df_merged['Security_Debt_Millions'] / df_merged['Total_National_Debt_Millions']) * 100.0
        # Dollar value per active transaction net unit delta ($ millions devided by piece delta count)
        df_merged['USD_Per_Transaction_Instance'] = (df_merged['Security_Debt_Millions'] * 1_000_000) / df_merged['Net_Count_Delta'].abs()

    def fetch_all_rates_pages(self, endpoint_url, date_field="record_date"):
        """Programmatically extracts all paginated records from a Fiscal data API endpoint."""
        all_records = []
        page_num = 1
        page_size = 1000

        while True:
            params = {
                "page[number]": page_num,
                "page[size]": page_size,
                "sort": date_field
            }
            try:
                response = requests.get(endpoint_url, params=params, timeout=20)
                response.raise_for_status()
                data = response.json()
            except requests.exceptions.RequestException:
                break
            records = data.get('data', [])
            if not records:
                break
            all_records.extend(records)
            if len(records) < page_size:
                break
            page_num += 1
            time.sleep(0.05)
        return pd.DataFrame(all_records)

    def get_real_yields(self):
        """
        Fetches the historical database stream from the U.S. Treasury XML gateway.
        data_type: 'daily_treasury_par_yield_cruve_rates' (Nominal)
                    or 'daily_treasury_real_par_yield_curve_rates' (TIPS)

        Notes:
        To calculate the breakeven inflation rate, you subtract the TIPS real yield from the nominal Treasury yield for an identical maturity.  This metric represents the average rate of inflation required over teh life of the bond for a nominal security and an inflation-protected security to deliver the exact same financial return

        scrapes both the Daily Treasury Par Yield Curve Rates (nominal) and the Daily Treasury Real Par Yield Curve Rates (TIPS)

        Analytical Interpretation of Breakeven Metrics:
        * Evaluating Investment Choices: if the actual consumer inflation index (CPI) over the lifespan of the bond averages higher than the calculated breakeven rate, the TIPS security will outperform the nominal bond.  If structural inflation ends up lower than the breakeven benchmark, the standard nominal Treasury Note is the superior financial play.
        * Federal Reserve Sentiment Gauges: the spread directly maps collective investement psychology.  Moves above the baseline suggest that global markets are projecting expanding future inflationary pressures, while contractions point toward slowing price expansion.

        """
        # 1. Download both Nominal and TIPS data sets
        df_nominal_raw = self.fetch_treasury_rates("daily_treasury_par_yield_curve_rates")
        df_tips_raw = self.fetch_treasury_rates("daily_treasury_real_par_yield_cuvre_rates")

        # 2. Clean and structure Nominal data
        df_nominal_raw['Date'] = pd.to_datetime(df_nominal_raw['NEW_DATE'])
        # TIPS maturities natively offered by the Treasury: 5-Yr, 7-Yr, 10-Yr, 20-Yr, 30-Yr
        target_maturities = ['5YR', '7YR', '10YR', '20YR', '30YR']
        nominal_cols = [f'BC_{m}' for m in target_maturities]
        df_nominal = df_nominal_raw[['Date'] + nominal_cols].copy()
        df_nominal[nominal_cols] = df_nominal[nominal_cols].apply(pd.to_numeric, errors='coerce')

        # 3. Clean and structure TIPS (Real) data
        df_tips_raw['Date'] = pd.to_datetime(df_tips_raw['NEW_DATE'])
        tips_cols = [f'BC_{m}' for m in target_maturities]
        df_tips = df_tips_raw[['Date'] + tips_cols].copy()
        df_tips[tips_cols] = df_tips[tips_cols].apply(pd.to_numeric, errors='coerce')

        # Rename columns to avoid collision during merge
        df_nominal = df_nominal.rename(columns={f'BC_{m}': f'Nominal_{m}' for m in target_maturities})
        df_tips = df_tips.rename(columns={f'BC_{m}': f'TIPS_{m}' for m in target_maturities})
        # 4. Merge data sets together
        df_merged = pd.merge(df_nominal, df_tips, on='Date', how='inner').sore_values('Date').dropna().reset_index(drop=True)
        # 5. Calculate Breakeven Inflation Rates: (Nominal Yield - TIPS Real Yield)
        for m in target_maturities:
            df_merged[f'Breakeven_{m}'] = df_merged[f"Nominal_{m}"] - df_merged[f"TIPS_{m}"]
        
    def fetch_treasury_rates(self, data_type):
        """
        Fetches the historical database stream from teh U.S. Treasury XML gateway.
        data_type: 'daily_treasury_par_yield_curve_rates' (Nominal)
                    or 'daily_treasury_real_par_yield_curve_rates' (TIPS)
        """
        base_url = 'https://treasury.gov'
        all_records = []
        page = 0
        print(f'Downloading stream: {data_type}...')
        while True:
            url = f"{base_url}?data={data_type}&field_tdr_date=all&page={page}"
            try:
                response = requests.get(url, timeout=15)
                response.raise_for_status()
            except requests.exceptions.RequestException:
                break
            root = ET.fromstring(response.content)
            namespaces = {
                'atom': 'http://w3.org',
                'm': 'http://microsoft.com'
            }
            entries = root.findall('atom:entry', namespaces)
            if not entries:
                break
            for entry in entries:
                properties = entry.find('.//m:properties', namespaces)
                if properties is not None:
                    record = { prop.tag.split('}')[-1]: prop.text for prop in properties }
                    all_records.append(record)
            page += 1
            time.sleep(0.05)
        return pd.DataFrame(all_records)