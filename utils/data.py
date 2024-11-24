"""
Nombre del archivo: data.py
Autores: Montserrat Lopez, Victor Bassas,  Andres  Henao
Descripción: Archivo que contiene código útil para tranformar datos para
            proyecto de curso Data Scientist de la UOC
Creado: 28/10/2024
Versión: 1.0
Correos: cutmountain@uoc.edu, vbassasb@uoc.edu, ahenaoa@uoc.edu
"""

#importes de librerías externas
import pandas as pd
import numpy as np
import os
import warnings

#cash_orig = pd.read_csv('../data/cash_request.csv')
#fees_orig = pd.read_csv('../data/fees.csv')


class Datasets:
    """
    Class for loading and processing the cash and fees datasets.
    It provides methods to create the cash_cohorts DataFrame,
    return the original datasets, and return users by cohort information.
    """

    def __init__(self):
        """
        Initialize the Datasets class by automatically setting paths to the cash and fees CSV files.
        The paths are dynamically generated based on the current working directory.

        Sets:
        - cash_path (str): Path to the cash dataset CSV.
        - fees_path (str): Path to the fees dataset CSV.
        """
        # Get current working directory
        current_path = os.getcwd()

        # Approach 1) Locate the project root directory by finding "monayvi"        
        # Locate the project root directory by finding "monayvi"        
        # aguacate_index = current_path.find("monayvi")
        # if aguacate_index != -1:
        #     project_root = current_path[:aguacate_index + len("monayvi")]
        # else:
        #     raise FileNotFoundError("The directory 'monayvi' was not found in the path.")
        
        # Approach 2) Locate the project root directory by finding "monayvi" or "MONAYVI"              
        # project_name = 'monayvi'
        # aguacate_index = current_path.find(project_name)
        # if aguacate_index == -1:
        #     project_name = project_name.upper()
        #     aguacate_index = current_path.find(project_name)
        # if aguacate_index != -1:
        #     #project_root = current_path[:aguacate_index + len("monayvi")]
        #     project_root = current_path[:aguacate_index + len(project_name)]
        # else:
        #     raise FileNotFoundError("The directory 'monayvi' was not found in the path.")
        
        # Approach 3) Locate the project root directory by finding the last slash "/"
        last_slash_index = current_path.rfind('/')
        if last_slash_index != -1:
            project_root = current_path[:last_slash_index]
        else:
            raise FileNotFoundError("The project directory was not found in the path.")  

        # If we want to check paths externally
        self.cwd = current_path
        self.project_directory = project_root          

        # Set the paths for the cash and fees CSVs
        self.cash_path = os.path.join(project_root, 'data', 'cash_request.csv')
        self.fees_path = os.path.join(project_root, 'data', 'fees.csv')

        # Read the original datasets
        self.dataset_cash_original_df = pd.read_csv(self.cash_path)
        self.dataset_fees_original_df = pd.read_csv(self.fees_path)

        # Initialize the cash and fees DataFrames with copies of the originals...
        self.cash = self.dataset_cash_original_df.copy()
        self.fees = self.dataset_fees_original_df.copy()

        # ... and apply standard treatment:     
        #   cash_request   
        #   - Column cash.id renamed to cash.cash_request_id;
        #   - Column 'id_usurio' added and populated from the combination of cash.user_id and cash.deleted_account_id;
        #   - Column cash.created_at converted to datetime;
        #   - Other columns converted to datetime:
                # created_at (already converted)
                # updated_at
                # moderated_at
                # reimbursement_date
                # cash_request_received_date
                # money_back_date
                # send_at
                # reco_creation
                # reco_last_update        
        #   fees
        #   - Recuperar el valor de 'cash_request_id' a partir de 'reason', para 4 filas con NaN en 'cash_request_id'
        #   - Conversión de 'cash_request_id' de float a int, para poder enlazarlo con la tabla cash
        #   - Columns converted to datetime:
                # created_at
                # updated_at
                # paid_at
                # from_date
                # to_date   
        
        # -- cash_request -----------------------------------------
        # Rename 'id' to 'cash_request_id'
        self.cash.rename(columns={'id': 'cash_request_id'}, inplace=True)

        # Create 'id_usuario' column based on 'user_id' and 'deleted_account_id'
        self.cash['id_usuario'] = self.cash['user_id'].fillna(self.cash['deleted_account_id'])
        self.cash['id_usuario'] = self.cash['id_usuario'].astype(int)

        # Convert 'created_at' to datetime
        self.cash['created_at'] = pd.to_datetime(self.cash['created_at'])        
        self.cash['updated_at'] = pd.to_datetime(self.cash['updated_at'])        
        self.cash['moderated_at'] = pd.to_datetime(self.cash['moderated_at'], format='mixed')        
        self.cash['reimbursement_date'] = pd.to_datetime(self.cash['reimbursement_date'], format='mixed')        
        self.cash['cash_request_received_date'] = pd.to_datetime(self.cash['cash_request_received_date'])        
        self.cash['money_back_date'] = pd.to_datetime(self.cash['money_back_date'], format='mixed')        
        self.cash['send_at'] = pd.to_datetime(self.cash['send_at'], format='mixed')        
        self.cash['reco_creation'] = pd.to_datetime(self.cash['reco_creation'])        
        self.cash['reco_last_update'] = pd.to_datetime(self.cash['reco_last_update'])      

        # -- fees -----------------------------------------
        # Recuperar el valor de 'cash_request_id' a partir de 'reason', para 4 filas con NaN
        extract_crid = lambda x: float(x.split(" ")[-1])
        crid_values = self.fees[self.fees['cash_request_id'].isna()]['reason'].transform(extract_crid)
        reason_dic = { 'cash_request_id' : crid_values}
        self.fees.fillna(reason_dic, inplace=True)

        # Conversión de 'cash_request_id' de float a int, para poder enlazarlo con la tabla cash
        self.fees['cash_request_id'] = self.fees['cash_request_id'].astype(int)

        # Convert to datetime         
        self.fees['created_at'] = pd.to_datetime(self.fees['created_at'])         
        self.fees['updated_at'] = pd.to_datetime(self.fees['updated_at'])         
        self.fees['paid_at'] = pd.to_datetime(self.fees['paid_at'], format='mixed')         
        self.fees['from_date'] = pd.to_datetime(self.fees['from_date'], format='mixed')         
        self.fees['to_date'] = pd.to_datetime(self.fees['to_date'], format='mixed')         

    def merge_tables(self):
        """
        Merge DataFrames 'cash_request' and 'fees', prefixing all columns of 'fees' with 'fee_'
         and on the basis of a 'cash_request_id' common key.

        Returns:
        pd.DataFrame: the result of merging DataFrames 'cash_request' and 'fees'
        """
        # Añadir prefijo a columnas tabla fees
        cash_copy = self.cash.copy()
        fees_copy = self.fees.copy()        
        
        fees_prefixed = fees_copy.add_prefix('fee_')

        self.merged = pd.merge(cash_copy, fees_prefixed, left_on='cash_request_id', right_on='fee_cash_request_id', how='outer') # 32098 rows

        return

    def create_cash_cohorts(self):
        """
        Process the cash DataFrame to create the 'cash_cohorts' DataFrame.

        This method performs the following steps:
        - Renames the 'id' column to 'cash_request_id' in the cash DataFrame.
        - Creates a new 'id_usuario' column based on 'user_id' and 'deleted_account_id'.
        - Converts the 'created_at' column to datetime.
        - Creates a pivot table to group by 'id_usuario' and gets the minimum 'created_at' date.
        - Adds a 'cohorte' column by converting the 'created_at' to period format.
        - Generates readable cohort labels and merges them into the cash DataFrame.
        - Returns the final 'cash_cohorts' DataFrame.

        Returns:
        pd.DataFrame: A DataFrame with the 'cohorte' and 'cohorte_lbl' columns added.
        """
        # # Rename 'id' to 'cash_request_id'
        # self.cash.rename(columns={'id': 'cash_request_id'}, inplace=True)

        # # Create 'id_usuario' column based on 'user_id' and 'deleted_account_id'
        # self.cash['id_usuario'] = self.cash['user_id'].fillna(self.cash['deleted_account_id'])
        # self.cash['id_usuario'] = self.cash['id_usuario'].astype(int)

        # # Convert 'created_at' to datetime
        # self.cash['created_at'] = pd.to_datetime(self.cash['created_at'])

        # Group by 'id_usuario' and find the minimum 'created_at'
        grouped1st = self.cash.pivot_table(
            values="created_at",
            index="id_usuario",
            aggfunc="min"
        )

        # Convert 'created_at' to period (cohorte) and suppress warnings
        warnings.filterwarnings('ignore', category=UserWarning)
        grouped1st['cohorte'] = grouped1st['created_at'].dt.to_period('M')
        warnings.resetwarnings()

        # Create readable cohort labels
        claves = list(np.sort(grouped1st['cohorte'].unique()))
        valores = []
        for index, value in enumerate(claves):
            #valores.append(f'COH-{index + 1:02}.{value.strftime("%b")}')
            valores.append(f'COH-{index+1:02}.{value.strftime("%b")}/{str(value.strftime("%y"))}')

        labels = dict(zip(claves, valores))

        # Merge 'cohorte' information into the original cash DataFrame
        cash_cohorts = pd.merge(self.cash, grouped1st[['cohorte']], on='id_usuario')

        # Add 'cohorte_lbl' column
        cash_cohorts['cohorte_lbl'] = cash_cohorts['cohorte'].transform(lambda x: labels[x])

        # Convert 'cohorte' column to string for consistency
        cash_cohorts['cohorte'] = cash_cohorts['cohorte'].astype(str)

        return cash_cohorts

    def get_original_datasets(self):
        """
        Return the original cash and fees DataFrames.

        Returns:
        tuple: A tuple containing the original cash DataFrame and the original fees DataFrame.
        """
        return self.dataset_cash_original_df, self.dataset_fees_original_df

    def get_users_by_cohort(self):
        """
        Calculate the number of users by cohort and return the result.

        This method assumes that the 'cash_cohorts' DataFrame has already been created
        using the 'create_cash_cohorts' method.

        Returns:
        pd.DataFrame: A DataFrame containing the number of unique users for each cohort.
        """
        # First, ensure 'cash_cohorts' is available
        cash_cohorts = self.create_cash_cohorts()

        # Calculate the number of users by cohort
        users_by_cohort = cash_cohorts.groupby('cohorte_lbl')['id_usuario'].nunique().reset_index()
        users_by_cohort.rename(columns={'id_usuario': 'num_usuarios'}, inplace=True)

        # Set 'cohorte_lbl' as the index
        users_by_cohort.set_index('cohorte_lbl', inplace=True)

        return users_by_cohort