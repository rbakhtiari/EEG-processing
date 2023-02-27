def find_maximum_and_mean_value_in_time_window(time_series, start_time_In, end_time_In):
#     from matplotlib.pyplot import plot, scatter, show
    
    ExtensionTime = 70 #ms
    peak_res = .01 
    
    time_slice = time_series.loc[start_time_In-1:end_time_In]
    start_time = time_slice.index[0]
    end_time = time_slice.index[-1]
#     print(start_time,end_time)
    maxtab, mintab = peakdet(time_slice,peak_res)
    if len(array(maxtab))>0:
        myindexmax = [int(x) for x in floor(array(maxtab)[:,0])]
#         scatter(time_slice.index[myindexmax], array(maxtab)[:,1], color='blue',marker='x')
        LeftMax=array([time_slice.index[myindexmax], array(maxtab)[:,1]])
    else: 
        LeftMax = np.array([(),()]) 
        
    time_slice_rev = time_series.loc[end_time:start_time:-1]
    maxtab_rev, mintab_rev = peakdet(time_slice_rev,peak_res)
    if len(array(maxtab_rev))>0:
        myindexmax_rev = [int(x) for x in floor(array(maxtab_rev)[:,0])]
#         scatter(time_slice_rev.index[myindexmax_rev], array(maxtab_rev)[:,1], color='cyan',marker='x')
        RightMax=array([time_slice_rev.index[myindexmax_rev], maxtab_rev[:,1]])
    else: 
        RightMax = np.array([(),()])  
        
#     print('888888888888888888888888888888888888888888888888888888888888')
#     print(time_slice)
#     print(time_slice_rev)
#     print('maxtab =',maxtab)
#     print('maxtab_rev =',maxtab_rev)

#     plot(time_slice)
    maxtabConc=np.concatenate((LeftMax,RightMax),axis=1)
#     print('LeftMax=',LeftMax)
#     print('RightMax=',RightMax)
#     print('maxtabConc=',maxtabConc)
    
    maxLocalInd = maxtabConc[1,:].argmax()
    maxLocalMax = maxtabConc[1,maxLocalInd];
    maxLocalIndOut = maxtabConc[0,maxLocalInd] 
#     print('maxLocalMax = ',maxLocalMax)
#     print('maxLocalInd = ',maxtabConc[0,maxLocalInd])

#     print('tmp:',maxtabConc[0,maxLocalInd])
#     print('tt:',time_slice.index[0])
    if maxLocalIndOut == start_time: # Peak at start point
        # Extend to the left and look for the first peak
        time_sliceExt_rev = time_series.loc[start_time:start_time-ExtensionTime:-1]  
#         plot(time_sliceExt_rev)
        maxtabExt_rev, mintabExt_rev = peakdet(time_sliceExt_rev,peak_res)
        if len(array(maxtabExt_rev))>0: # peak was found by extending to the left
            maxLocalMax = maxtabExt_rev[0,1]
            myindexmaxExt_rev = [int(x) for x in floor(array(maxtabExt_rev)[:,0])]
            maxLocalIndOut = time_sliceExt_rev.index[myindexmaxExt_rev[0]]
#             print('haha!! myindexmaxExt_rev=',myindexmaxExt_rev)
#             scatter(time_sliceExt_rev.index[myindexmaxExt_rev[0]], array(maxtabExt_rev)[0,1], color='purple',marker='o')
            Status = 'L'
        else: # peak was NOT found by extending to the left 
            # check again for the local max in the main area
            LeftMax = np.delete(LeftMax, 0, axis=1) # remove the first column which was left boundry max
            maxtabConc = np.concatenate((LeftMax,RightMax),axis=1)
            if len(array(maxtabConc[1,:]))>0:
                maxLocalInd = maxtabConc[1,:].argmax()
                maxLocalMax = maxtabConc[1,maxLocalInd];
                maxLocalIndOut = maxtabConc[0,maxLocalInd] 
    #             print('tmp,maxlocalMax=',maxLocalMax)
    #             print('boundry=',time_series.loc[end_time:end_time+sample_interval-1].mean())
                if  maxLocalIndOut == end_time:# Peak at end point:
                    # Extend to the right and look for peak
                    time_sliceExt = time_series.loc[end_time:end_time+ExtensionTime]
    #                 plot(time_sliceExt)
                    maxtabExt, mintabExt = peakdet(time_sliceExt,peak_res)
                    if len(array(maxtabExt))>0:
                        maxLocalMax = maxtabExt[0,1]            
                        myindexmaxExt = [int(x) for x in floor(array(maxtabExt)[:,0])]
                        maxLocalIndOut = time_sliceExt.index[myindexmaxExt[0]]
    #                     scatter(time_sliceExt.index[myindexmaxExt], array(maxtabExt)[:,1], color='purple',marker='o')
                        Status = 'R'
                    else: 
                        # check again for the local max in the boundry
                        RightMax = np.delete(RightMax, 0, axis=1) # remove the first column which was right boundry max
    #                     print(RightMax)
                        maxtabConc=np.concatenate((LeftMax,RightMax),axis=1)
    #                     print(maxtabConc)
                        if len(array(maxtabConc[1,:]))>0:
                            maxLocalInd = maxtabConc[1,:].argmax()
                            maxLocalMax = maxtabConc[1,maxLocalInd];
                            maxLocalIndOut = maxtabConc[0,maxLocalInd] 
    #                         scatter(maxtabConc[0,maxLocalInd], maxLocalMax, color='purple',marker='o')
                            Status = 'G'
                        else:
                            #Nothing is found!
                            maxLocalMax = 999
                            maxLocalIndOut = 999
                            Status = 'NaN'            
                else: 
    #                 scatter(maxtabConc[0,maxLocalInd], maxLocalMax, color='purple',marker='o')
                    Status = 'G'
            else:
                #Nothing is found!
                maxLocalMax = 999
                maxLocalIndOut = 999
                Status = 'NaN'                                 
            
    elif maxLocalIndOut == end_time:# Peak at end point
        # Extend to the right and look for the first peak
        
        time_sliceExt = time_series.loc[end_time:end_time+ExtensionTime]
#         plot(time_sliceExt)
        maxtabExt, mintabExt = peakdet(time_sliceExt,peak_res)
        if len(array(maxtabExt))>0: # peak was found by extending to the right
            maxLocalMax = maxtabExt[0,1]            
            myindexmaxExt = [int(x) for x in floor(array(maxtabExt)[:,0])]
            maxLocalIndOut = time_sliceExt.index[myindexmaxExt[0]]
#             print('haha!! myindexmaxExt=',myindexmaxExt)
#             scatter(time_sliceExt.index[myindexmaxExt[0]], array(maxtabExt)[0,1], color='purple',marker='o')
            Status = 'R'
        else: # peak was NOT found by extending to the right 
            # check again for the local max in the main area
            RightMax = np.delete(RightMax, 0, axis=1) # remove the first column which was right boundry max
            # check again for the local max in the boundry
            maxtabConc = np.concatenate((LeftMax,RightMax),axis=1)
#             print('RightMaxNew=',RightMax)

            if len(array(maxtabConc[1,:]))>0:
                maxLocalInd = maxtabConc[1,:].argmax()
                maxLocalMax = maxtabConc[1,maxLocalInd];
                maxLocalIndOut = maxtabConc[0,maxLocalInd] 
    #             print('tmp,maxlocalMax=',maxLocalMax)
    #             print('boundry=',time_series.loc[start_time:start_time+sample_interval-1].mean())
                if maxLocalIndOut == time_slice.index[0]:# Peak at start point:
                    # Extend to the left and look for the first peak
                    time_sliceExt_rev = time_series.loc[start_time:start_time-ExtensionTime:-1]   
    #                 plot(time_sliceExt_rev)
                    maxtabExt_rev, mintabExt_rev = peakdet(time_sliceExt_rev,peak_res)                
                    if len(array(maxtabExt_rev))>0:
                        maxLocalMax = maxtabExt_rev[0,1]            
                        myindexmaxExt = [int(x) for x in floor(array(maxtabExt_rev)[:,0])]
                        maxLocalIndOut = time_sliceExt_rev.index[myindexmaxExt[0]]
    #                     scatter(time_sliceExt_rev.index[myindexmaxExt], array(maxtabExt_rev)[:,1], color='purple',marker='o')
                        Status = 'L'
                    else:
                        # check again for the local max in the boundry
                        LeftMax = np.delete(LeftMax, 0, axis=1) # remove the first column which was left boundry max
    #                     print(LeftMax)
                        maxtabConc=np.concatenate((LeftMax,RightMax),axis=1)
    #                     print(maxtabConc)
                        if len(array(maxtabConc[1,:]))>0:
                            maxLocalInd = maxtabConc[1,:].argmax()
                            maxLocalMax = maxtabConc[1,maxLocalInd];
                            maxLocalIndOut = maxtabConc[0,maxLocalInd] 
    #                         scatter(maxtabConc[0,maxLocalInd], maxLocalMax, color='purple',marker='o')
                            Status = 'G'
                        else:
                            #Nothing is found!
                            maxLocalMax = 999
                            maxLocalIndOut = 999
                            Status = 'NaN'            
                else: 
    #                 scatter(maxtabConc[0,maxLocalInd], maxLocalMax, color='purple',marker='o')
                    Status = 'G'        
            else:
                #Nothing is found!
                maxLocalMax = 999
                maxLocalIndOut = 999
                Status = 'NaN'                
    else:
#         scatter(maxtabConc[0,maxLocalInd], maxLocalMax, color='purple',marker='o')
        Status = 'G'
#     show()
#     print(time_series.loc[start_time:start_time+sample_interval-1])
#     print('1st sample =',time_series.loc[start_time:start_time+sample_interval-1].mean())
#     print('Overal Max =',maxLocalMax)
#     print(Status)
    
       
    #return Event(timestamp=time_slice.idxmax(), value=time_slice.max(), mean=time_slice.mean()) # old
    return Event(timestamp=int(maxLocalIndOut), value=maxLocalMax, mean=time_slice.mean(), status=Status) # new
