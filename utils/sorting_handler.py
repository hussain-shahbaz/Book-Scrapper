

import time
from .algorithms import Algorithm


def applySortingAlgorithm(colValues, algo, selectedAlgo):
    try:
        if selectedAlgo == "BubbleSort":
            return algo.BubbleSort(colValues)
        elif selectedAlgo == "InsertionSort":
            return algo.InsertionSort(colValues)
        elif selectedAlgo == "SelectionSort":
            return algo.SelectionSort(colValues)
        elif selectedAlgo == "MergeSort":
            return algo.MergeSort(colValues)
        elif selectedAlgo == "QuickSort":
            return algo.QuickSort(colValues)
        elif selectedAlgo == "CountSort":
            try:
                numericValues = [int(float(v)) for v in colValues]
                return algo.CountSort(numericValues)
            except:
                return None
    except Exception as e:
        return None


def getSortedIndices(colValues, sortedValues, selectedAlgo):
    if sortedValues is None:
        return None
    
    if selectedAlgo == "CountSort":
        sortedIndices = []
        tempValues = colValues.copy()
        for sv in sortedValues:
            try:
                idx = tempValues.index(str(sv))
                sortedIndices.append(idx)
                tempValues[idx] = None  # Mark as used
            except:
                pass
        return sortedIndices
    else:
        # Standard handling for other algorithms
        sortedIndices = []
        try:
            for v in sortedValues:
                idx = colValues.index(v)
                sortedIndices.append(idx)
                colValues[idx] = None  # Mark as used to handle duplicates
            return sortedIndices
        except:
            return None


def sortDataFrameByColumns(displayDf, sortColumns, selectedAlgo, reverseSort):
    if not sortColumns or len(displayDf) == 0:
        return displayDf, 0
    
    sortStart = time.time()
    algo = Algorithm()
    
    try:
        df = displayDf.copy()
        indices = list(range(len(df)))
        
        for col in sortColumns:
            colValues = df[col].astype(str).tolist()
            sortedValues = applySortingAlgorithm(colValues, algo, selectedAlgo)
            
            if sortedValues is not None:
                sortedIndices = getSortedIndices(colValues.copy(), sortedValues, selectedAlgo)
                
                if sortedIndices is not None and len(sortedIndices) == len(df):
                    indices = [indices[i] for i in sortedIndices]
        
        df = displayDf.iloc[indices].reset_index(drop=True)
        
        if reverseSort:
            df = df.iloc[::-1].reset_index(drop=True)
        
        sortTime = time.time() - sortStart
        return df, sortTime
        
    except Exception as e:
        return displayDf, 0



