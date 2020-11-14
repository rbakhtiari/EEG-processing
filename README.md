# EEG-processing
Tools for various stage of EEG data analysis


ERP Peak-picking algorithm, to look for peaks within a time range, identified by range=( start_time_In, end_time_In). As some peaks may happen a little bit earlier or later than the range if the points on the range boarder, are greater than peaks inside the range, then the algorithm allows looking for a peak within ExtensionTime points outside of the range.
