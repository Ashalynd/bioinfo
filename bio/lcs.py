def LCS(v, w, scores, indel):
    #indel is positive because it's supposed to be subtracted
    lv = len(v)
    lw = len(w)
    s = [[ None for mm in range(lw+1)] for nn in range(lv+1)]
    backtrack = [[ None for mm in range(lw+1)] for nn in range(lv+1)]
    for i in range(lv+1):
        s[i][0] = -i*indel
    for j in range(lw+1):
        s[0][j] = -j*indel
    for i in range(1,lv+1):
        for j in range(1,lw+1):
            (local_max_ind, local_max) = (0, -1000)
            for (ind, sc) in zip (range(3), [s[i-1][j] - indel, s[i][j-1] - indel, s[i-1][j-1]+scores[(v[i-1],w[j-1])]]):
                if sc >= local_max:
                    local_max_ind = ind
                    local_max = sc
            s[i][j] = local_max
            if local_max_ind == 0:
                backtrack[i][j]='|'
            if local_max_ind == 1:
                backtrack[i][j]='-'
            if local_max_ind == 2:
                backtrack[i][j] = '\\'
#   print s
    return s[lv][lw], backtrack

def LCS_local(v, w, scores, indel):
    #indel is positive because it's supposed to be subtracted
    lv = len(v)
    lw = len(w)
    s = [[ None for mm in range(lw+1)] for nn in range(lv+1)]
    backtrack = [[ None for mm in range(lw+1)] for nn in range(lv+1)]
    for i in range(lv+1):
        s[i][0] = -i*indel
    for j in range(lw+1):
        s[0][j] = -j*indel

    global_max = 0
    global_i = lv
    global_j = lw

    for i in range(1,lv+1):
        for j in range(1,lw+1):
            (local_max_ind, local_max) = (0, -1000)
            for (ind, sc) in zip (range(3), [ \
                s[i-1][j] - indel, \
                s[i][j-1] - indel, \
                s[i-1][j-1]+scores[(v[i-1],w[j-1])] \
                ]):
                if sc >= local_max:
                    local_max_ind = ind
                    local_max = sc
            if local_max<0:
                local_max = 0
                local_max_ind = 3
            s[i][j] = local_max
            if local_max>global_max:
                global_max = local_max
                global_i = i
                global_j = j
            if local_max_ind == 0:
                backtrack[i][j]='|'
            if local_max_ind == 1:
                backtrack[i][j]='-'
            if local_max_ind == 2:
                backtrack[i][j] = '\\'
            if local_max_ind == 3:
                backtrack[i][j] = '*'
#   print s
    return s[global_i][global_j], backtrack, global_i, global_j


def LCS_fitting(v, w, scores, indel, overlap = False):
    #indel is positive because it's supposed to be subtracted
    lv = len(v)
    lw = len(w)
    s = [[ None for mm in range(lw+1)] for nn in range(lv+1)]
    backtrack = [[ "" for mm in range(lw+1)] for nn in range(lv+1)]
    s[0][0]=0
    for i in range(1,lv+1):
        s[i][0] = -i*indel
    for j in range(1,lw+1):
        s[0][j] = -j*indel

    global_max = 0
    global_i = lv
    global_j = lw

    for i in range(1,lv+1):
        for j in range(1,lw+1):
            (local_max_ind, local_max) = (0, -1000)
            arr = [ \
            s[i-1][j] - indel, \
            s[i][j-1] - indel, \
            s[i-1][j-1]+scores[(v[i-1],w[j-1])] \
            ]
            if j==1:
                arr.append(scores[(v[i-1],w[j-1])])
            for (ind, sc) in zip (range(len(arr)),arr):
                if sc >= local_max:
                    local_max_ind = ind
                    local_max = sc
            s[i][j] = local_max
            end_condition = ((not overlap) and j==lw) or (overlap and i==lv)
            if local_max>global_max and end_condition:
                global_max = local_max
                global_i = i
                global_j = j
                print global_max, global_i, global_j
            if local_max_ind == 0:
                backtrack[i][j]='|'
            if local_max_ind == 1:
                backtrack[i][j]='-'
            if local_max_ind == 2:
                backtrack[i][j] = '\\'
            if local_max_ind == 3:
                backtrack[i][j] = '*'
#   for (bb,ss) in zip(backtrack, s):
#       print "\t".join(["%s:%s" % (bbb,sss) for (bbb,sss) in zip(bb,ss)])
#   for r in backtrack:
#       print "\t".join(r)
#   for r in s:
#       print "\t".join([str(rr) for rr in r])
    print global_i, global_j
    return s[global_i][global_j], backtrack, global_i, global_j


def outputLCS(backtrack, v, w, i, j, fitting = False):
    acc = ""
    vv = ""
    ww = ""
    while True:
        if backtrack[i][j]=='*' and not fitting:
            return (acc, vv, ww)
        if i==0 or j==0:
            if i==0:
                ww = "".join(w[:j]) + ww
                vv = '-' * j + vv
            if j==0 and not fitting:
                vv = "".join(v[:i]) + vv
                ww = '-' * i + ww
            return (acc, vv, ww)
        if backtrack[i][j]=='|':
            i -=1
            vv = v[i] + vv
            ww = '-' + ww
            #outputLCS(backtrack, v, i-1, j)
            continue
        elif backtrack[i][j]=='-':
            j-=1
            vv = '-' + vv
            ww = w[j] + ww
            continue
            #outputLCS(backtrack, v, i, j-1)
        else:
            #outputLCS(backtrack, v, i-1, j-1)
            acc =v[i-1] + acc
            vv = v[i-1] + vv
            ww = w[j-1] + ww
            i-=1
            j-=1
            continue
