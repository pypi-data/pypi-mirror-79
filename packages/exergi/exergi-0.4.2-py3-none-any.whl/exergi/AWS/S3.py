""" This module defines all exergi functions within the AWS.S3 module"""

def exportFileToS3(obj,bucket: str,s3key: str,**kwargs) -> None:
    """ This module exports a pandas.DataFrame to specified bucket/s3key. 

    Keyword Arguments:
        - obj       - Python object to be exported
        - bucket    - S3 export bucket,no trailing / like "stage-data-scientist"
        - s3key     - S3 export key, no leading "/". String should end with the
                      desired file format. "public/.../example.csv". 
                      Currently supported fileformats are
                        - .csv
                            - pandas.DataFrame()
                        - .xlsx
                            - pandas.DataFrame()
                        - .pkl
                            - pandas.DataFrame()
                            - sklearn
                        - .h5
                            - pandas.DataFrame()
                        - .npy
                            - numpy (arrays)
        - **kwargs
    Returns:
        None (Maybe confirmation should be returned in future versions)
    """

    from boto3 import resource
    from pickle import dumps
    from os.path import splitext
    from io import BytesIO,StringIO

    import pandas as pd
    import numpy as np
    import tempfile
    import json
    import logging
    import time
    
    
    # Initiate Logger
    logger = logging.getLogger(__name__)
    start = time.time()

    # Connect to S3
    s3resource = resource("s3")   

    # Extra file name, file format and export object type
    _, file_fmt = splitext(s3key)
    obj_class = obj.__class__.__module__.split(".")[0]

    logger.info(f'Load settings:\n\t{obj_class=}\n\t{bucket=}\n\t{s3key=}')
    logger.info(f'Exporting {file_fmt}-data to S3:')

    # Comma separated files 
    if (file_fmt == ".csv")&(obj_class == "pandas"):
        buffer = StringIO()
        obj.to_csv(buffer,index=False)    
        s3resource.Object(bucket, s3key).put(Body=buffer.getvalue())

    # Excel files 
    elif (file_fmt == ".xlsx")&(obj_class == "pandas"):
        with BytesIO() as output:
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:     # pylint: disable=abstract-class-instantiated
                obj.to_excel(writer)
            data = output.getvalue()
            s3resource.Object(bucket, s3key).put(Body=data)

    # Pickle files 
    elif file_fmt == ".pkl":
    
        if obj_class == "sklearn":

            from sklearn.externals import joblib
    
            with tempfile.TemporaryFile() as fp:
                joblib.dump(obj, fp)
                fp.seek(0)
                s3resource.Object(bucket, s3key).put(Body=fp.read())
        
        elif obj_class == "pandas":
            serializedMyData = dumps(obj)
            s3resource.Object(bucket, s3key).put(Body=serializedMyData)

    # HDF5 files 
    elif (file_fmt == ".h5") & (obj_class == "pandas"):
        with tempfile.NamedTemporaryFile(suffix=".h5") as fp:
            hdf = pd.HDFStore(fp.name)
            hdf.put(value=obj, format='table', data_columns=True,**kwargs)
            hdf.close()
            fp.seek(0)
            s3resource.Object(bucket, s3key).put(Body=fp.read())

    # npy files 
    elif (file_fmt == ".npy") & (obj_class == "numpy"):
        with tempfile.TemporaryFile()  as fp:
            np.save(fp,obj) 
            fp.seek(0)
            s3resource.Object(bucket, s3key).put(Body=fp.read())

    # npz files- This exports each pandas column to a compressed numpy array
    # as a "key-value pair". See numpy documentation for more information
    elif (file_fmt == ".npz") & (obj_class == "pandas"):
        with tempfile.TemporaryFile()  as fp:
            np.savez(fp,**obj.to_dict())
            fp.seek(0)
            s3resource.Object(bucket, s3key).put(Body=fp.read())

    else:
        raise_str = f"""Failed! {file_fmt} export of {obj_class} objects not 
            implemented."""
        logger.info(f'\tFailed! {raise_str}')
        raise Exception()

    logger.info(f'\tOK! Exported data in {time.time()-start} [s]')

def importFileFromS3(bucket: str, s3key: str, obj_class: str ="pandas",**kwargs):
    """ This module imports a pandas.DataFrame from specified bucket/s3key. 

    Arguments:
        - bucket    -   S3 export bucket, no trailing / - "stage-data-scientist"
        - s3key     -   S3 export key, no leading / . String should end with the
                        desired file format like "public/.../example.csv". 
                        Currently supported fileformats is:
                            - .csv
                                - pandas.DataFrame()
                            - .xlsx
                                - pandas.DataFrame()
                            - .pkl
                                - pandas.DataFrame()
                                - sklearn.joblib
                            - .h5
                                - pandas.DataFrame()
                            - .npy
                                - numpy (array)
                            - .npz
                                - numpy-zip (arrays)        
        - obj_class  -  String explaining what object type file should be loaded 
                        as (default = "pandas")
    Keyword Arguments:
        - **kwargs  -   Keyword arguments import function. Import function 
                        varies for each file format: 
                            - .csv  = pd.read_csv()
                            - .xlsx = pd.read_excel()
                            - .pkl  = pd.read_pickle()
                            - .h5   = pd.read_hdf()
    Returns:
        - obj       -   Imported 
    """

    import boto3
    from io import BytesIO
    import os
    import pandas as pd
    import numpy as np
    import tempfile   
    import logging
    import time
    
    # Initiate Logger
    logger = logging.getLogger(__name__)
    start = time.time()

    # Extra file name, file format and export object type
    _, file_fmt = os.path.splitext(s3key)
    s3client = boto3.client("s3")

    logger.info(f'Load settings:\n\t{bucket=}\n\t{s3key=}\n\t{obj_class=}')
    logger.info(f'Loading {file_fmt}-data from S3:')

    # CSV files 
    if (file_fmt == ".csv") & (obj_class == "pandas"):
        with s3client.get_object(Bucket=bucket,Key=s3key) as S3obj:
            obj = pd.read_csv(BytesIO(S3obj["Body"].read()),**kwargs)

    # Excel files 
    elif (file_fmt == ".xlsx") & (obj_class == "pandas"):
        with s3client.get_object(Bucket=bucket,Key=s3key) as S3obj:
            obj = pd.read_excel(BytesIO(S3obj["Body"].read()), **kwargs)

    # Pickle files 
    elif (file_fmt == ".pkl") & (obj_class == "pandas"):
        with s3client.get_object(Bucket=bucket,Key=s3key) as S3obj:
            obj = pd.read_pickle(BytesIO(S3obj["Body"].read()), **kwargs)
        
    elif (file_fmt == ".pkl") & (obj_class == "sklearn"):
        from sklearn.externals import joblib
        with tempfile.TemporaryFile() as fp:
            s3client.download_fileobj(Bucket=bucket, Key=s3key,Fileobj=fp)
            fp.seek(0)
            obj = joblib.load(fp)          
    
    # HDF5 files 
    elif (file_fmt == ".h5") & (obj_class == "pandas"):
        with tempfile.NamedTemporaryFile()  as fp:
            s3client.download_fileobj(Bucket=bucket, Key=s3key,Fileobj=fp)
            fp.seek(0)
            obj = pd.read_hdf(fp.name,**kwargs)

    # npy files 
    elif (file_fmt == ".npy") & (obj_class == "numpy"):
        with tempfile.NamedTemporaryFile()  as fp:
            s3client.download_fileobj(Bucket=bucket, Key=s3key,Fileobj=fp)
            fp.seek(0)
            obj = np.load(fp.name)

    # npz files- This exports each pandas column to a compressed numpy array
    # as a "key-value pair". See numpy documentation for more information
    elif (file_fmt == ".npz") & (obj_class == "numpy"):
        with tempfile.NamedTemporaryFile()  as fp:
            s3client.download_fileobj(Bucket=bucket, Key=s3key,Fileobj=fp)
            fp.seek(0)
            obj = np.load(fp.name)

    # If none of the above file_fmt and obj_class combination are true. Raise!
    else:
        raise_str = f"""Failed! {file_fmt} export of {obj_class} objects not 
            implemented."""
        logger.critical(f'\tFailed! {raise_str}')
        raise Exception(raise_str)

    logger.info(f'\tOK! {obj.shape[0]} loaded in {time.time()-start} [s]')
    return obj

def listFilesInPath(bucket,prefix,dropSubFolders=True,
                    removePrefix=True,subsetExt=None, removeExt=False,):
    """ List all files (sorted) in the specified bucket and prefix
    
    Arguments:
        - bucket [str]          -   S3 bucket where path i located,
                                    no trailing "/" like "stage-data-scientist"
        - prefix [str]          -   S3 prefix where files should be listed, "/". 
        - dropSubFolders [bool] -   Switch if files in subfolders should 
                                    be dropped (default = True)
        - removePrefix [bool]   -   Switch if strings in listOfFiles should 
                                    have file prefix removed (default = True)
        - subsetExt [str]           String ('.csv','.xlsx',...) to subset file 
                                    extension with. If provided (default = None)
                                    listOfFiles will only return files
                                    with the specified file extension.
        - removeExt [bool]      -   Switch if strings in listOfFiles should 
                                    have file extension ('.csv','.xlsx',...)
                                    removed (default = False)
    Returns:
        - listOfFiles [lst]     -   List of files in bucket-prefix. 
    """
    
    import pandas as pd
    from io import BytesIO
    import boto3
    import os
    import logging 
    import time

    # Initiate Logger
    logger = logging.getLogger(__name__)
    start = time.time()

    # Remove filename from prefix
    if prefix != "":
        prefix = os.path.dirname(prefix)+"/"
        
    logger.info(f'Load settings:\n\t{bucket=}\n\t{prefix=}')
        
    # List all s3keys 
    listOfFiles = []
    for objectSummary in list(boto3.resource("s3").Bucket(bucket).objects.filter(
            Prefix=prefix))[0:]:
        listOfFiles.append(objectSummary.key)
    listOfFiles = [fileName for fileName in listOfFiles if fileName != prefix]
    
    # Drop all files in subfolders
    if dropSubFolders:
        listOfFiles = [fileName for fileName in listOfFiles if 
            (os.path.dirname(fileName) == os.path.dirname(prefix))]
    
    if removePrefix:
        listOfFiles = [fileName.replace(prefix,"") for fileName in listOfFiles]

    # Subset only files ending with provided subsetExt 
    if subsetExt:
        listOfFiles = [fileName for fileName in listOfFiles if 
            subsetExt in fileName]

    # Remove all file extensions 
    if removeExt:
        listOfFiles = [os.path.splitext(fileName)[0] for fileName in listOfFiles]
    
    logger.info(f'\tOK! Elapsed time {time.time()-start} [s]')
    return sorted(listOfFiles)